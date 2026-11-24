"""Phase 2C: final synthetic validation with one isolated binding null (S7/S8).

Same experimental unit and budget accounting as Phase 2B (``phase2b.py``): one Monte Carlo
experiment is a disjoint block of instances, with ``block[:r_dev]`` for development and the
following ``n_conf_max`` instances for confirmation. Every procedure gets the same total fit
budget B = b (2 + K).

Procedures and the estimand each one certifies (column ``scope``):

| procedure            | scope    | estimand                                                     |
|----------------------|----------|--------------------------------------------------------------|
| pcga_l               | L3       | Delta_{strat:block} (PCGA-L edge step); NOT a full-set claim  |
| exhaustive_iut       | full     | theta_full = min over {empty} + all K candidates             |
| screen_uniform       | selected | theta_sel  = min over {empty} + the 2 screened nulls          |
| screen_random        | selected | as above (random visiting order)                              |
| screen_sh            | selected | as above (successive halving; secondary, not in the framework)|
| oracle_select        | selected | {empty, true argmin}; an unattainable upper bound             |
| fullset_adaptive     | full     | Phase 2B rule: n_min = 5, no fallback                         |
| fullset_adaptive_fb  | full     | n_min = 5, a-priori feasibility fallback to exhaustive_iut    |
| fullset_adaptive_s   | full     | n_min = 3, a-priori feasibility fallback to exhaustive_iut    |

The feasibility fallback is decided from (b, K, R1, n_min) only, i.e. before any data are
seen: if the stage-2 budget cannot give every comparator n_min replicates, the procedure is
exactly ``exhaustive_iut`` with the whole budget. It therefore has the level of whichever
branch runs.

Binding-null audit columns (``bind_*``) record, for the known binding comparator, the stage-1
and stage-2 one-sided t p-values, the combined p-value and the data-dependent stage-2 size.
These feed the combination-test audit in docs/phase2c_report.md section 6.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..inference.allocation import (_summ, _t_p_s, allocation_cost, fullset_adaptive, fullset_two_stage,
                                    optimal_allocation)
from ..inference.certificates import iut_certificate
from ..inference.tests import wilcoxon_two_sided
from ..nulls.search import ALGORITHMS, PoolOracle
from ..utils.seeding import rng_for
from .methods import PoolArrays, _drop_nan, _holm, _pcga_verdict, contrasts
from .phase2b import _seconds, arms_for, variant_seconds  # noqa: F401  (re-exported)

FULLSET_VARIANTS = {  # name -> (n_min, a-priori feasibility fallback)
    "fullset_adaptive": (5, False),
    "fullset_adaptive_fb": (5, True),
    "fullset_adaptive_s": (3, True),
}


def fullset_feasible(K: int, B: int, R1: int, n_min: int) -> bool:
    """A-priori feasibility (data-free): stage 1 plus n_min stage-2 replicates for all K+1 comparators."""
    return R1 * (2 + K) + allocation_cost({i: n_min for i in range(K + 1)}) <= B


def stage1_size(b: int, K: int, r_dev: int, search_frac: float) -> int:
    B = b * (2 + K)
    return max(2, min(r_dev, int(round(search_frac * B)) // (2 + K)))


def run_experiment_2c(P: PoolArrays, block: np.ndarray, tr: pd.DataFrame, arms: list[str], b: int, *,
                      sec: dict, binding_arm: str | None, r_dev: int = 20, n_conf_max: int = 100, top_m: int = 2,
                      search_frac: float = 1 / 3, alpha: float = 0.05, alpha1: float = 0.01, eps: float = 0.005,
                      hit_tol: float = 0.002, d_floor: float = 0.003, master_seed: int = 0,
                      method: str = "t", variants: dict | None = None) -> list[dict]:
    variants = FULLSET_VARIANTS if variants is None else variants
    K = len(arms)
    B = b * (2 + K)
    dev = block[:r_dev]
    conf = block[r_dev:r_dev + n_conf_max]
    comps_full = ["empty"] + arms
    theta_full = float(tr.loc[comps_full, "delta"].min())
    near = set(tr.loc[comps_full].index[tr.loc[comps_full, "delta"] <= theta_full + hit_tol])
    arg_true = tr.loc[comps_full, "delta"].idxmin()
    bind = binding_arm if (binding_arm in comps_full) else arg_true
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
            "est_error_target": float(theta_hat - th_t) if np.isfinite(theta_hat) else np.nan,
            "n_comparators": len(comps), **(extra or {})})

    def iut(idx_by_comp):
        D = _drop_nan({k: contrasts(P, idx, [k])[k] for k, idx in idx_by_comp.items()})
        c = iut_certificate(D, method, alpha, eps)
        return c, min(float(np.mean(v)) for v in D.values())

    # 1. PCGA-L ladder (its own estimand: the edge step real vs strat:block) -------------------
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

    # 2. exhaustive IUT, uniform allocation ----------------------------------------------------
    n_ex = min(len(conf), b)
    c_ex, th_ex = iut({k: conf[:n_ex] for k in comps_full})
    ex_counts = {"real": n_ex, **{k: n_ex for k in comps_full}}
    record("exhaustive_iut", "full", comps_full, c_ex.certified, c_ex.L_robust, th_ex, n_ex * (2 + K), n_ex,
           ex_counts, {"argmin": c_ex.argmin_L, "discovered": c_ex.argmin_L == bind})

    # 3-5. screen-then-confirm (selected-set) ----------------------------------------------------
    B_s = int(round(search_frac * B))
    for alg in ("uniform", "random", "successive_halving"):
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
                "discovered": bind in comps, "near_discovered": bool(set(comps) & near),
                "search_fits": res.fits_used})

    # 6. oracle selection --------------------------------------------------------------------
    comps = ["empty", arg_true] if arg_true != "empty" else ["empty"]
    n = min(len(conf), B // (1 + len(comps)))
    c, th = iut({k: conf[:n] for k in comps})
    record("oracle_select", "selected", comps, c.certified, c.L_robust, th, (1 + len(comps)) * n, n,
           {"real": n, **{k: n for k in comps}}, {"argmin": c.argmin_L, "discovered": True})

    # 7. full-set adaptive variants ----------------------------------------------------------
    R1 = stage1_size(b, K, r_dev, search_frac)
    d1 = dev[:R1]
    dev_cost = R1 * (2 + K)
    D_dev = _drop_nan(contrasts(P, d1, comps_full))
    sig = float(np.sqrt(np.mean([np.var(v, ddof=1) for v in D_dev.values() if len(v) > 1])))
    se = {k: float(np.std(v, ddof=1) / np.sqrt(len(v))) for k, v in D_dev.items()}
    w1 = float(np.sqrt(search_frac))  # fixed a priori = planned stage-1 budget share
    a1, a2 = alpha1, alpha - alpha1
    st1 = fullset_two_stage(D_dev, {}, a1, a2, eps, method)
    elim = {k for k, v in st1["stage"].items() if v == "dev"}
    rest = [k for k in comps_full if k not in elim]
    p1_bind = _t_p_s(_summ(D_dev.get(bind, [])), eps)
    for name, (n_min, fallback) in variants.items():
        feasible = fullset_feasible(K, B, R1, n_min)
        common = {"dev_instances": R1, "n_min": n_min, "feasible": feasible, "fallback": False}
        if not feasible:
            if fallback:  # a-priori rule: identical to exhaustive_iut with the whole budget
                record(name, "full", comps_full, c_ex.certified, c_ex.L_robust, th_ex, n_ex * (2 + K), n_ex,
                       ex_counts, {**common, "fallback": True, "argmin": c_ex.argmin_L,
                                   "discovered": c_ex.argmin_L == bind, "n_eliminated": 0})
            else:
                record(name, "full", comps_full, False, -np.inf, np.nan, 0, 0, {}, {**common, "infeasible": True})
            continue
        base_counts = {"real": R1, **{k: R1 for k in comps_full}}
        if not rest:
            record(name, "full", comps_full, st1["certified"], st1["L_robust"],
                   min(float(np.mean(v)) for v in D_dev.values()), dev_cost, R1, base_counts,
                   {**common, "argmin": st1["argmin"], "n_eliminated": st1["n_eliminated"], "discovered": np.nan,
                    "bind_stage": "dev", "bind_p1": p1_bind})
            continue
        alloc = optimal_allocation({k: float(np.mean(D_dev[k])) for k in rest}, sig, eps, B - dev_cost,
                                   se_hat=se, n_min=n_min, n_max=len(conf), d_floor=d_floor, alpha=a2)
        assert alloc is not None  # guaranteed by the a-priori feasibility check
        D_conf = _drop_nan({k: contrasts(P, conf[:alloc[k]], [k])[k] for k in rest})
        out = fullset_adaptive(D_dev, D_conf, w1, a1, a2, eps)
        means = {k: float(np.mean(np.concatenate([D_dev[k], D_conf.get(k, [])]))) for k in comps_full}
        top = max(alloc, key=lambda k: (alloc[k], k))
        counts = {"real": R1 + max(alloc.values()), **{k: R1 + alloc.get(k, 0) for k in comps_full}}
        bstage = out["stage"].get(bind)
        record(name, "full", comps_full, out["certified"], out["L_robust"], min(means.values()),
               dev_cost + allocation_cost(alloc), R1 + max(alloc.values()), counts,
               {**common, "argmin": out["argmin"], "n_eliminated": out["n_eliminated"], "discovered": top == bind,
                "binding_share": float(alloc.get(bind, 0) / max(1, sum(alloc.values()))),
                "bind_stage": bstage, "bind_p1": p1_bind,
                "bind_p2": _t_p_s(_summ(D_conf.get(bind, [])), eps) if bstage == "combined" else np.nan,
                "bind_pc": out["marginal"][bind].get("p", np.nan) if bind in out["marginal"] else np.nan,
                "bind_n2": int(alloc.get(bind, 0)), "infeasible": False})

    for r in rows:
        r.update({"scenario": P.scenario, "first_instance": int(block[0]), "K": K, "b": b, "eps": eps,
                  "alpha": alpha, "arg_true": arg_true, "binding_arm": bind, "n_near_binding": len(near)})
    return rows


def run_grid_2c(P: PoolArrays, tr: pd.DataFrame, sec: dict, configs: list[dict], eps_list, block_size: int,
                master_seed: int, binding_arm: str | None, **kw) -> pd.DataFrame:
    rows = []
    for cfg in configs:
        arms = arms_for(P, cfg["attrs"])
        for b in cfg["budgets"]:
            for eps in eps_list:
                for e in range(P.N // block_size):
                    blk = np.arange(e * block_size, (e + 1) * block_size)
                    rr = run_experiment_2c(P, blk, tr, arms, b, sec=sec, eps=eps, master_seed=master_seed,
                                           binding_arm=binding_arm, **kw)
                    for r in rr:
                        r["k_config"] = cfg["name"]
                    rows += rr
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ combination-test audit
def null_contrasts(P: PoolArrays, arm: str) -> np.ndarray:
    """Per-instance contrasts of an exact-null (A/A) arm, first valid draw, all instances."""
    d = contrasts(P, np.arange(P.N), [arm])[arm]
    return d[np.isfinite(d)]


def audit_marginal_t(d: np.ndarray, ns=(2, 3, 4, 5, 8, 12, 20), alphas=(0.01, 0.025, 0.04, 0.05, 0.10)) -> pd.DataFrame:
    """Size of the one-sided t-test (H0: mean <= 0) on disjoint groups of exact-null contrasts."""
    rows = []
    for n in ns:
        G = len(d) // n
        X = d[:G * n].reshape(G, n)
        p = np.array([_t_p_s(_summ(x), 0.0) for x in X])
        for a in alphas:
            k = int((p <= a).sum())
            rows.append({"n": n, "alpha": a, "groups": G, "rejections": k, "size": k / G})
    return pd.DataFrame(rows)


def _comb_p(x1, x2, w1):
    from ..inference.allocation import _combine
    return _combine(_t_p_s(_summ(x1), 0.0), _t_p_s(_summ(x2), 0.0), w1)


N2_RULES = {
    "fixed5": lambda p1: 5,
    "fixed20": lambda p1: 20,
    "promising_more": lambda p1: 30 if p1 < 0.3 else 3,   # extend when stage 1 looks significant
    "promising_less": lambda p1: 3 if p1 < 0.3 else 30,   # adversarial in the other direction
}


def audit_combination(d: np.ndarray, R1s=(2, 3, 4, 7), rules=None, w1: float = np.sqrt(1 / 3), alpha1: float = 0.01,
                      alpha2: float = 0.04, n_boot: int = 0, seed: int = 0) -> pd.DataFrame:
    """Type-I error of interim efficacy (alpha1) + inverse-normal combination (alpha2) for one exact-null
    arm under data-dependent stage-2 sizes.

    n_boot = 0: disjoint blocks of the observed exact-null contrasts (no resampling; exact
    population null). n_boot > 0: i.i.d. resampling from the *centred* empirical distribution
    (mean exactly 0, realistic non-normal shape), giving many more replicates.
    """
    rules = rules or N2_RULES
    rng = np.random.default_rng(seed)
    dc = d - d.mean()
    rows = []
    for R1 in R1s:
        for rname, rule in rules.items():
            n2max = max(rule(0.0), rule(1.0))
            if n_boot:
                reps = [(rng.choice(dc, R1), rng.choice(dc, n2max)) for _ in range(n_boot)]
            else:
                G = len(d) // (R1 + n2max)
                reps = [(d[g * (R1 + n2max): g * (R1 + n2max) + R1], d[g * (R1 + n2max) + R1:(g + 1) * (R1 + n2max)])
                        for g in range(G)]
            rej_int = rej_comb = 0
            pcs = []
            for x1, x2 in reps:
                p1 = _t_p_s(_summ(x1), 0.0)
                if p1 <= alpha1:
                    rej_int += 1
                    continue
                pc = _comb_p(x1, x2[:rule(p1)], w1)
                pcs.append(pc)
                rej_comb += pc <= alpha2
            G = len(reps)
            rows.append({"R1": R1, "rule": rname, "replicates": G,
                         "source": "bootstrap_centred" if n_boot else "disjoint_blocks",
                         "interim_rate": rej_int / G, "combination_rate": rej_comb / G,
                         "total_type1": (rej_int + rej_comb) / G, "nominal": alpha1 + alpha2})
    return pd.DataFrame(rows)
