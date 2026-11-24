"""Compute-matched comparison of attribution procedures on precomputed instance pools.

Population-inference setting: the replication unit is an independently simulated graph
instance.  A Monte Carlo *experiment* consumes a disjoint block of ``block`` consecutive
instances; different experiments never share instances, so experiment-level outcomes are
independent and binomial Monte Carlo standard errors are valid.

Within an experiment every procedure receives the same total model-fit budget ``B``
(anchored at the critical baseline: fixed multi-null IUT over all candidates with
``r_base`` instances).  Procedures that need fewer fits per instance use more instances, up
to the block size (budget then under-used; recorded).

Procedures (``claim`` = "real graph beats every comparator in the procedure's set by > eps"):
  pcga          PCGA endpoints (empty + perm:block), PCGA's verdict rule (Holm over two-sided
                Wilcoxon, mean sign and t-CI).  Claim = specificity supported.
  pcga_l        PCGA-L ladder L0..L4 = empty, er, degree, strat:block, real; Holm over the four
                steps with the PCGA verdict rule.  Claim = edge step (L3->L4) supported.
  single_degree single prespecified null (degree swap), one-sided t bound.
  menu_iut      RUSA without search: audited fixed menu {empty, er, degree, perm:block,
                strat:block} + IUT (t).
  iut_all       critical baseline: audited full candidate set + empty + IUT (t).
  rusa_uniform  dev-only uniform screening -> freeze top-m -> confirm {empty + top-m} (IUT, t).
  rusa_sh       dev-only successive halving -> freeze top-m -> confirm (IUT, t).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..inference.certificates import iut_certificate
from ..inference.tests import lower_bound, t_lower, wilcoxon_two_sided
from ..nulls.search import ALGORITHMS, PoolOracle

MENU = ["er", "degree", "perm:block", "strat:block"]
LADDER = ["empty", "er", "degree", "strat:block"]  # L0..L3; L4 = real


@dataclass
class PoolArrays:
    scenario: str
    instances: np.ndarray
    real_val: np.ndarray
    real_test: np.ndarray
    empty_val: np.ndarray
    empty_test: np.ndarray
    cand_val: dict      # name -> (N, b), NaN where the placebo failed the audit
    cand_test: dict
    cand_valid: dict    # name -> (N, b) bool

    @property
    def names(self):
        return list(self.cand_val)

    @property
    def N(self):
        return len(self.instances)


def pool_arrays(df: pd.DataFrame) -> PoolArrays:
    sc = df["scenario"].iloc[0]
    inst = np.sort(df["instance"].unique())
    pos = {v: i for i, v in enumerate(inst)}
    N = len(inst)

    def one(variant, col):
        d = df[df.variant == variant].set_index("instance")[col]
        return d.reindex(inst).to_numpy(dtype=float)

    names = [v for v in df["variant"].unique() if v not in ("real", "empty")]
    b = int(df["draw"].max()) + 1
    cv, ct, ok = {}, {}, {}
    for k in names:
        sub = df[df.variant == k]
        V = np.full((N, b), np.nan)
        T = np.full((N, b), np.nan)
        A = np.zeros((N, b), dtype=bool)
        ii = sub["instance"].map(pos).to_numpy()
        dd = sub["draw"].to_numpy()
        val = sub["valid"].astype(bool).to_numpy()
        A[ii, dd] = val
        V[ii, dd] = np.where(val, sub["val_score"].to_numpy(), np.nan)
        T[ii, dd] = np.where(val, sub["test_score"].to_numpy(), np.nan)
        cv[k], ct[k], ok[k] = V, T, A
    return PoolArrays(sc, inst, one("real", "val_score"), one("real", "test_score"),
                      one("empty", "val_score"), one("empty", "test_score"), cv, ct, ok)


def contrasts(P: PoolArrays, idx: np.ndarray, names: list[str], draws: str = "first_valid") -> dict:
    """Paired test contrasts D_r for the instances ``idx``.

    ``first_valid``: one placebo fit per instance (first audit-valid draw; regenerating an
    invalid placebo costs no fit).  ``mean``: Monte Carlo mean over all valid draws.
    """
    out = {}
    for k in names:
        if k == "empty":
            out[k] = P.real_test[idx] - P.empty_test[idx]
            continue
        T = P.cand_test[k][idx]
        if draws == "mean":
            with np.errstate(all="ignore"):
                s = np.nanmean(T, 1)
        else:
            s = np.full(len(idx), np.nan)
            for j in range(T.shape[1] - 1, -1, -1):
                s = np.where(np.isfinite(T[:, j]), T[:, j], s)
        out[k] = P.real_test[idx] - s
    return out


def truth(P: PoolArrays, idx: np.ndarray | None = None) -> pd.DataFrame:
    """Monte Carlo estimate of Delta_k (population mean over instances, all valid draws)."""
    idx = np.arange(P.N) if idx is None else idx
    D = contrasts(P, idx, ["empty"] + P.names, draws="mean")
    rows = []
    for k, d in D.items():
        d = d[np.isfinite(d)]
        rows.append({"comparator": k, "delta": d.mean(), "mc_se": d.std(ddof=1) / np.sqrt(len(d)),
                     "sd_unit": d.std(ddof=1), "n": len(d)})
    return pd.DataFrame(rows).set_index("comparator")


def admissible_arms(P: PoolArrays, idx: np.ndarray, min_acceptance: float = 0.8) -> list[str]:
    """Candidate-level admissibility from label-free audit flags on the given instances."""
    return [k for k in P.names if P.cand_valid[k][idx].mean() >= min_acceptance]


def _drop_nan(D: dict) -> dict:
    return {k: v[np.isfinite(v)] for k, v in D.items()}


def _pcga_verdict(d: np.ndarray, p_adj: float, alpha: float) -> str:
    t = t_lower(d, alpha=0.025)  # lower end of the two-sided 95% t interval
    if p_adj < alpha and d.mean() > 0 and t["L"] > 0:
        return "supported"
    return "not supported"


def _holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(p) - r) * p[i]))
        adj[i] = run
    return adj


def run_experiment(P: PoolArrays, block_idx: np.ndarray, truth_df: pd.DataFrame, *, r_base: int = 12,
                   r_dev: int = 10, top_m: int = 2, search_frac: float = 1 / 3, alpha: float = 0.05,
                   eps: float = 0.0, method: str = "t", hit_tol: float = 0.002) -> list[dict]:
    dev = block_idx[:r_dev]
    conf_pool = block_idx[r_dev:]
    arms = admissible_arms(P, dev)
    K = len(P.names)
    B = r_base * (2 + K)
    theta_full = float(truth_df.loc[["empty"] + arms, "delta"].min())
    hardest = truth_df.loc[arms, "delta"].idxmin()
    rows = []

    def record(proc, comps, claim, fits, n_inst, L=np.nan, extra=None):
        th_t = float(truth_df.loc[comps, "delta"].min())
        rows.append({
            "procedure": proc, "claim": bool(claim), "fits": int(fits), "budget": B, "n_instances": int(n_inst),
            "theta_target": th_t, "theta_full": theta_full, "L": L,
            "covered": bool(L <= th_t) if np.isfinite(L) else np.nan,
            "false_vs_target": bool(claim and th_t <= eps), "false_vs_full": bool(claim and theta_full <= eps),
            "comparators": "|".join(comps), **(extra or {}),
        })

    # --- critical baseline: fixed multi-null IUT over all admissible candidates
    idx = conf_pool[:r_base]
    comps = ["empty"] + arms
    cert = iut_certificate(_drop_nan(contrasts(P, idx, comps)), method, alpha, eps)
    record("iut_all", comps, cert.certified, len(idx) * (2 + len(arms)), len(idx), cert.L_robust,
           {"argmin": cert.argmin_L})

    # --- RUSA without search = audited fixed menu + IUT
    comps = ["empty"] + [k for k in MENU if k in arms]
    n = min(len(conf_pool), B // (1 + len(comps)))
    idx = conf_pool[:n]
    cert = iut_certificate(_drop_nan(contrasts(P, idx, comps)), method, alpha, eps)
    record("menu_iut", comps, cert.certified, n * (1 + len(comps)), n, cert.L_robust, {"argmin": cert.argmin_L})

    # --- single prespecified null
    n = min(len(conf_pool), B // 2)
    idx = conf_pool[:n]
    r = lower_bound(_drop_nan(contrasts(P, idx, ["degree"]))["degree"], method, alpha, eps)
    record("single_degree", ["degree"], r["L"] > eps, n * 2, n, r["L"])

    # --- PCGA (endpoints, PCGA verdict rule)
    n = min(len(conf_pool), B // 3)
    idx = conf_pool[:n]
    D = _drop_nan(contrasts(P, idx, ["empty", "perm:block"]))
    padj = _holm([wilcoxon_two_sided(D["empty"]), wilcoxon_two_sided(D["perm:block"])])
    util = _pcga_verdict(D["empty"], padj[0], alpha)
    spec = _pcga_verdict(D["perm:block"], padj[1], alpha)
    record("pcga", ["perm:block"], spec == "supported", n * 3, n, np.nan,
           {"pcga_utility": util, "pcga_relation_value": util == spec == "supported"})

    # --- PCGA-L (ladder, Holm over four steps, PCGA verdict rule); claim = edge step
    n = min(len(conf_pool), B // 5)
    idx = conf_pool[:n]
    S = {"L0": P.empty_test[idx], "L4": P.real_test[idx]}
    Dl = contrasts(P, idx, ["er", "degree", "strat:block"])
    S["L1"], S["L2"], S["L3"] = (P.real_test[idx] - Dl[k] for k in ("er", "degree", "strat:block"))
    steps = {"density": S["L1"] - S["L0"], "degree": S["L2"] - S["L1"], "block": S["L3"] - S["L2"],
             "edge": S["L4"] - S["L3"]}
    ok = np.all([np.isfinite(v) for v in steps.values()], 0)
    steps = {k: v[ok] for k, v in steps.items()}
    padj = _holm([wilcoxon_two_sided(v) for v in steps.values()])
    verd = {k: _pcga_verdict(v, pa, alpha) for (k, v), pa in zip(steps.items(), padj)}
    tel = float(np.max(np.abs((S["L4"] - S["L0"])[ok] - sum(steps.values()))))
    record("pcga_l", ["strat:block"], verd["edge"] == "supported", n * 5, n, np.nan,
           {**{f"step_{k}": v for k, v in verd.items()}, "telescoping_err": tel})

    # --- full RUSA: dev-only search -> freeze -> confirm
    B_s = int(round(search_frac * B))
    for alg in ("uniform", "successive_halving"):
        oracle = PoolOracle(P.real_val[dev], {a: P.cand_val[a][dev] for a in arms})
        res = ALGORITHMS[alg](oracle, arms, B_s, top_m=top_m)
        sel = res.selected
        comps = ["empty"] + sel
        n = min(len(conf_pool), (B - res.fits_used) // (1 + len(comps)))
        idx = conf_pool[:n]
        cert = iut_certificate(_drop_nan(contrasts(P, idx, comps)), method, alpha, eps)
        sel_true = truth_df.loc[sel, "delta"]
        record("rusa_" + ("sh" if alg == "successive_halving" else "uniform"), comps, cert.certified,
               res.fits_used + n * (1 + len(comps)), n, cert.L_robust,
               {"argmin": cert.argmin_L, "selected": "|".join(sel), "hit_hardest": hardest in sel,
                "regret": float(sel_true.min() - truth_df.loc[arms, "delta"].min()),
                "hit_within_tol": bool(sel_true.min() - truth_df.loc[arms, "delta"].min() <= hit_tol),
                "search_fits": res.fits_used, "dev_best_estimate": res.arm_stats[sel[0]]["mean"]})
    for r in rows:
        r.update({"scenario": P.scenario, "first_instance": int(block_idx[0]), "eps": eps, "alpha": alpha,
                  "test_method": method, "hardest_arm": hardest, "n_arms": len(arms)})
    return rows


def run_comparison(P: PoolArrays, block: int = 60, eps: float = 0.0, method: str = "t",
                   exact_zero: str | None = None, **kw) -> pd.DataFrame:
    """All independent experiments of a pool.  ``exact_zero``: A/A family whose Delta is 0 by
    construction; its Monte Carlo estimate is replaced by the exact value."""
    tr = truth(P)
    if exact_zero is not None:
        tr.loc[exact_zero, "delta"] = 0.0
    rows = []
    for e in range(P.N // block):
        rows += run_experiment(P, np.arange(e * block, (e + 1) * block), tr, eps=eps, method=method, **kw)
    return pd.DataFrame(rows)


def calibration(P: PoolArrays, R_list=(12, 40), methods=("t", "boot", "signflip", "eb", "wsr"),
                alpha: float = 0.05, exact_zero: str | None = None, max_subsets: int | None = None) -> pd.DataFrame:
    """Marginal coverage of one-sided lower bounds for every comparator, with cross-fitted truth.

    Subsets in the first half of the pool are scored against truth estimated on the second
    half, and vice versa, so truth estimates are independent of the evaluated subset.  For the
    A/A family (``exact_zero``) the truth is exactly 0 and no estimate is used.
    """
    N = P.N
    halves = [np.arange(0, N // 2), np.arange(N // 2, N)]
    tr = [truth(P, halves[1]), truth(P, halves[0])]
    comps = ["empty"] + P.names
    rows = []
    for R in R_list:
        for h in (0, 1):
            ids = halves[h]
            nsub = len(ids) // R
            if max_subsets:
                nsub = min(nsub, max_subsets // 2)
            for s in range(nsub):
                idx = ids[s * R:(s + 1) * R]
                D = contrasts(P, idx, comps)
                for k in comps:
                    d = D[k][np.isfinite(D[k])]
                    true = 0.0 if k == exact_zero else float(tr[h].loc[k, "delta"])
                    for mth in methods:
                        r = lower_bound(d, mth, alpha, eps=true)
                        rows.append({"scenario": P.scenario, "R": R, "comparator": k, "method": mth,
                                     "truth": true, "exact_truth": k == exact_zero, "L": r["L"], "p": r["p"],
                                     "reject_true_null": bool(r["p"] <= alpha), "mean": r["mean"]})
    return pd.DataFrame(rows)


def aa_global_iut(P: PoolArrays, aa_family: str, R: int = 12, method: str = "t", alpha: float = 0.05) -> pd.DataFrame:
    """Global IUT type-I at the exact boundary theta <= 0 (A/A family has Delta = 0 exactly)."""
    comps = ["empty"] + P.names
    rows = []
    for s in range(P.N // R):
        idx = np.arange(s * R, (s + 1) * R)
        cert = iut_certificate(_drop_nan(contrasts(P, idx, comps)), method, alpha, 0.0)
        aa = lower_bound(_drop_nan(contrasts(P, idx, [aa_family]))[aa_family], method, alpha, 0.0)
        rows.append({"scenario": P.scenario, "R": R, "method": method, "global_certified": cert.certified,
                     "aa_marginal_reject": aa["p"] <= alpha, "argmin": cert.argmin_L})
    return pd.DataFrame(rows)
