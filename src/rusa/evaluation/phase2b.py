"""Phase 2B: compute-matched comparison of null-screening and certification procedures.

Every procedure in one Monte Carlo experiment uses instances from the same disjoint block:
  block[:r_dev]                       development instances (screening / allocation / stage 1)
  block[r_dev : r_dev + n_conf_max]   confirmatory instances
and the same total model-fit budget B = b * (2 + K), where K is the number of candidate nulls.

Scope of each certificate (column ``scope``):
  "full"     -> valid for theta_full = min over {empty} + all K candidates;
  "selected" -> valid only for min over {empty} + the frozen selected nulls;
  "L3"       -> PCGA-L edge step (real vs strat:block) only.

Development contrasts use the test-node score on *development instances*. These instances are
disjoint from, and independent of, the confirmatory instances, so selection and allocation are
independent of confirmatory data (docs/phase2b_math.md, section 2).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..inference.allocation import allocation_cost, fullset_adaptive, fullset_two_stage, optimal_allocation
from ..inference.certificates import iut_certificate
from ..inference.tests import wilcoxon_two_sided
from ..nulls.search import ALGORITHMS, PoolOracle
from ..utils.seeding import rng_for
from .methods import PoolArrays, _drop_nan, _holm, _pcga_verdict, contrasts


def arms_for(P: PoolArrays, attrs: list[str]) -> list[str]:
    """Candidate set restricted to stratifications over ``attrs`` (+ er, degree, perm:block)."""
    out = []
    for k in P.names:
        if ":" not in k or k.startswith("perm:"):
            out.append(k)
        elif all(a in attrs for a in k.split(":", 1)[1].split("+")):
            out.append(k)
    return out


def variant_seconds(df: pd.DataFrame) -> dict:
    """Mean wall-clock seconds per fit (placebo generation included) by variant."""
    t = df.assign(sec=df["fit_seconds"] + df.get("gen_seconds", 0).fillna(0))
    return t.groupby("variant")["sec"].mean().to_dict()


def _seconds(counts: dict, sec: dict) -> float:
    return float(sum(n * sec.get(k, 0.0) for k, n in counts.items()))


def run_experiment_2b(P: PoolArrays, block: np.ndarray, tr: pd.DataFrame, arms: list[str], b: int, *,
                      sec: dict, r_dev: int = 20, n_conf_max: int = 100, top_m: int = 2,
                      search_frac: float = 1 / 3, alpha: float = 0.05, alpha1: float = 0.01,
                      eps: float = 0.005, hit_tol: float = 0.002, n_min: int = 5, d_floor: float = 0.003,
                      master_seed: int = 0, method: str = "t") -> list[dict]:
    K = len(arms)
    B = b * (2 + K)
    dev = block[:r_dev]
    conf = block[r_dev:r_dev + n_conf_max]
    comps_full = ["empty"] + arms
    theta_full = float(tr.loc[comps_full, "delta"].min())
    binding = set(tr.loc[comps_full].index[tr.loc[comps_full, "delta"] <= theta_full + hit_tol])
    arg_true = tr.loc[arms, "delta"].idxmin()
    rows = []

    def record(proc, scope, comps, claim, L, theta_hat, fits, n_inst, counts, extra=None):
        th_t = float(tr.loc[comps, "delta"].min())
        rows.append({
            "procedure": proc, "scope": scope, "claim": bool(claim), "L": float(L), "theta_hat": float(theta_hat),
            "theta_target": th_t, "theta_full": theta_full, "fits": int(fits), "budget": B,
            "n_instances": int(n_inst), "seconds": _seconds(counts, sec),
            "covered_target": bool(L <= th_t) if np.isfinite(L) else np.nan,
            "covered_full": bool(L <= theta_full) if np.isfinite(L) else np.nan,
            "false_vs_full": bool(claim and theta_full <= eps), "false_vs_target": bool(claim and th_t <= eps),
            "est_error": float(theta_hat - theta_full) if np.isfinite(theta_hat) else np.nan,
            "n_comparators": len(comps), **(extra or {})})

    def iut(idx_by_comp):
        D = {k: contrasts(P, idx, [k])[k] for k, idx in idx_by_comp.items()}
        D = _drop_nan(D)
        c = iut_certificate(D, method, alpha, eps)
        th = min(float(np.mean(v)) for v in D.values())
        return c, th

    # 1. PCGA-L (fixed ladder; PCGA verdict rule) -------------------------------------------
    n = min(len(conf), B // 5)
    idx = conf[:n]
    Dl = contrasts(P, idx, ["er", "degree", "strat:block"])
    S = {"L0": P.empty_test[idx], "L4": P.real_test[idx]}
    S["L1"], S["L2"], S["L3"] = (P.real_test[idx] - Dl[k] for k in ("er", "degree", "strat:block"))
    steps = {"density": S["L1"] - S["L0"], "degree": S["L2"] - S["L1"], "block": S["L3"] - S["L2"],
             "edge": S["L4"] - S["L3"]}
    padj = _holm([wilcoxon_two_sided(v) for v in steps.values()])
    verd = {k: _pcga_verdict(v, pa, alpha) for (k, v), pa in zip(steps.items(), padj)}
    record("pcga_l", "L3", ["strat:block"], verd["edge"] == "supported", np.nan, float(np.mean(steps["edge"])),
           5 * n, n, {"real": n, "empty": n, "er": n, "degree": n, "strat:block": n})

    # 2. exhaustive IUT over all K (+empty), uniform allocation --------------------------------
    n = min(len(conf), b)
    c, th = iut({k: conf[:n] for k in comps_full})
    record("exhaustive_iut", "full", comps_full, c.certified, c.L_robust, th, n * (2 + K), n,
           {"real": n, **{k: n for k in comps_full}}, {"argmin": c.argmin_L})

    # 3-5. screen-then-confirm (selected-set) ----------------------------------------------------
    B_s = int(round(search_frac * B))
    for alg in ("random", "uniform", "successive_halving"):
        oracle = PoolOracle(P.real_test[dev], {a: P.cand_test[a][dev] for a in arms})
        kw = {"rng": rng_for(master_seed, P.scenario, int(block[0]), "random_search")} if alg == "random" else {}
        res = ALGORITHMS[alg](oracle, arms, B_s, top_m=top_m, **kw)
        comps = ["empty"] + res.selected
        n = min(len(conf), (B - res.fits_used) // (1 + len(comps)))
        c, th = iut({k: conf[:n] for k in comps})
        counts = {"real": n + len(oracle.paid), **{k: n for k in comps}}
        for e in res.log:
            counts[e["arm"]] = counts.get(e["arm"], 0) + 1
        name = {"random": "screen_random", "uniform": "screen_uniform", "successive_halving": "screen_sh"}[alg]
        record(name, "selected", comps, c.certified, c.L_robust, th, res.fits_used + n * (1 + len(comps)), n, counts,
               {"argmin": c.argmin_L, "selected": "|".join(res.selected),
                "discovered": bool(set(res.selected) & binding), "hit_argmin": arg_true in res.selected,
                "search_fits": res.fits_used})

    # 6. oracle selection (knows the true hardest arm; no search cost) -----------------------
    comps = ["empty", arg_true]
    n = min(len(conf), B // 3)
    c, th = iut({k: conf[:n] for k in comps})
    record("oracle_select", "selected", comps, c.certified, c.L_robust, th, 3 * n, n,
           {"real": n, "empty": n, arg_true: n}, {"argmin": c.argmin_L, "discovered": True})

    # 7-9. full-set procedures: every comparator is tested (scope "full") -------------------
    R1 = max(2, min(r_dev, B_s // (2 + K)))
    d1 = dev[:R1]
    dev_cost = R1 * (2 + K)
    D_dev = _drop_nan(contrasts(P, d1, comps_full))
    sig = float(np.sqrt(np.mean([np.var(v, ddof=1) for v in D_dev.values() if len(v) > 1])))
    se = {k: float(np.std(v, ddof=1) / np.sqrt(len(v))) for k, v in D_dev.items()}
    w1 = float(np.sqrt(search_frac))  # inverse-normal weight fixed in advance (stage-1 budget share)
    for name, a1 in (("fullset_alloc", 0.0), ("fullset_elim", alpha1), ("fullset_adaptive", alpha1)):
        a2 = alpha - a1
        elim = set()
        if a1 > 0:
            st = fullset_two_stage(D_dev, {}, a1, a2, eps, method)
            elim = {k for k, v in st["stage"].items() if v == "dev"}
        rest = [k for k in comps_full if k not in elim]
        base_counts = {"real": R1, **{k: R1 for k in comps_full}}
        if not rest:  # every comparator certified at stage 1
            out = fullset_two_stage(D_dev, {}, a1, a2, eps, method)
            record(name, "full", comps_full, out["certified"], out["L_robust"],
                   min(float(np.mean(v)) for v in D_dev.values()), dev_cost, R1, base_counts,
                   {"argmin": out["argmin"], "n_eliminated": out["n_eliminated"], "discovered": np.nan,
                    "binding_share": np.nan, "n_binding_alloc": 0, "dev_instances": R1, "infeasible": False})
            continue
        alloc = optimal_allocation({k: float(np.mean(D_dev[k])) for k in rest}, sig, eps, B - dev_cost,
                                   se_hat=se, n_min=n_min, n_max=len(conf), d_floor=d_floor, alpha=a2)
        if alloc is None:
            record(name, "full", comps_full, False, -np.inf, np.nan, dev_cost, R1, base_counts,
                   {"infeasible": True, "dev_instances": R1})
            continue
        D_conf = _drop_nan({k: contrasts(P, conf[:alloc[k]], [k])[k] for k in rest})
        if name == "fullset_adaptive":
            out = fullset_adaptive(D_dev, D_conf, w1, a1, a2, eps)
            means = {k: float(np.mean(np.concatenate([D_dev[k], D_conf.get(k, [])]))) for k in comps_full}
        else:
            out = fullset_two_stage(D_dev if a1 > 0 else {k: np.array([]) for k in comps_full}, D_conf, a1, a2, eps, method)
            means = {k: float(np.mean(D_dev[k] if out["stage"][k] == "dev" else D_conf[k])) for k in comps_full}
        top = max(alloc, key=lambda k: (alloc[k], k))
        counts = {"real": R1 + max(alloc.values()), **{k: R1 + alloc.get(k, 0) for k in comps_full}}
        record(name, "full", comps_full, out["certified"], out["L_robust"], min(means.values()),
               dev_cost + allocation_cost(alloc), R1 + max(alloc.values()), counts,
               {"argmin": out["argmin"], "n_eliminated": out["n_eliminated"], "discovered": top in binding,
                "binding_share": float(sum(alloc.get(k, 0) for k in binding) / max(1, sum(alloc.values()))),
                "n_binding_alloc": int(max([alloc.get(k, 0) for k in binding] or [0])), "dev_instances": R1,
                "infeasible": False})

    for r in rows:
        r.update({"scenario": P.scenario, "first_instance": int(block[0]), "K": K, "b": b, "eps": eps,
                  "alpha": alpha, "arg_true": arg_true, "n_binding": len(binding)})
    return rows


def run_grid_2b(P: PoolArrays, tr: pd.DataFrame, sec: dict, configs: list[dict], eps_list, block_size: int,
                master_seed: int, **kw) -> pd.DataFrame:
    """All (K-config, budget, eps) analyses on one pool; experiments are disjoint blocks."""
    rows = []
    for cfg in configs:
        arms = arms_for(P, cfg["attrs"])
        for b in cfg["budgets"]:
            for eps in eps_list:
                for e in range(P.N // block_size):
                    blk = np.arange(e * block_size, (e + 1) * block_size)
                    rr = run_experiment_2b(P, blk, tr, arms, b, sec=sec, eps=eps, master_seed=master_seed, **kw)
                    for r in rr:
                        r["k_config"] = cfg["name"]
                    rows += rr
    return pd.DataFrame(rows)
