"""CRAF procedures under matched budgets, on pool contrasts or semi-synthetic contrasts.

One experiment uses a block of independent replicates (instances). For each block, ``D[name]`` is
the per-replicate contrast real − null(name) for every lattice element. The budget is
B = b (1 + |L|) model fits: one real fit per replicate plus one fit per (element, replicate).

| procedure        | data / certification                                | reported frontier |
|------------------|-----------------------------------------------------|-------------------|
| craf             | b replicates for all; Holm over 2|L| one-sided tests | cert_min (plus possible_min as the uncertainty set) |
| craf_adaptive    | stage 1 R1 = round(b/3) for all; minimax-power stage-2 allocation; inverse-normal combination; Holm over 2|L| | cert_min |
| craf_children    | as craf, but minimality checked only against immediate subsets (|T| = |S| − 1), i.e. it implicitly assumes monotonicity (ablation) | cert_min_children |
| ni_holm          | standard multiplicity-controlled non-inferiority: Holm over the |L| sufficiency hypotheses only | minimal among certified sufficient |
| factorial_unadj  | exhaustive factorial evaluation, per-element tests at alpha (no multiplicity) | cert_min |
| naive_point      | point estimates (mean < delta)                       | minimal elements |
| pcga_l           | PCGA-L ladder (empty, ER, degree, block, real), n = B/5, Holm–Wilcoxon steps | ladder-implied lowest sufficient level (pool mode only) |
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..inference.allocation import allocation_cost, optimal_allocation
from .core import (ADV, SUF, Lattice, certify, combined_directional_p, directional_p, frontier_sets, point_frontier,
                   true_frontier)


def _fmt(s):
    return "|".join(sorted(s))


def _children_cert_min(L: Lattice, A: set, C: set) -> set:
    out = set()
    for n in L.names:
        kids = [t for t in L.proper_subsets(n) if len(L.sets[t]) == len(L.sets[n]) - 1]
        if n in C and all(t in A for t in kids):
            out.add(n)
    return out


def adaptive_pvalues(L: Lattice, D: dict, b: int, delta: float, alpha: float, *, search_frac: float = 1 / 3,
                     n_min: int = 5, d_floor: float = 0.003, kappa: float = 1.0, relevance: bool = True):
    """Two-stage p-values. Returns (pv, fits, info), or None when infeasible a priori.

    Infeasibility depends only on (b, |L|, n_min), so the caller's fallback is decided before data.
    """
    m = len(L)
    B = b * (1 + m)
    R1 = max(2, int(round(search_frac * b)))
    N = min(len(v) for v in D.values())
    budget2 = B - R1 * (1 + m)
    if budget2 < allocation_cost({n: n_min for n in L.names}) or R1 + n_min > N:
        return None
    st1 = {n: directional_p(D[n][:R1], delta) for n in L.names}
    sig = float(np.sqrt(np.mean([np.var(D[n][:R1], ddof=1) for n in L.names])))
    dominated = set()
    if relevance:  # supersets of an element that already looks clearly sufficient cannot be frontier members
        for n in L.names:
            if any(st1[t]["mean"] + 2 * st1[t]["se"] < delta for t in L.proper_subsets(n)):
                dominated.add(n)
    live = [n for n in L.names if n not in dominated]
    alloc = {n: n_min for n in dominated}
    if live:
        a = optimal_allocation({n: delta + abs(st1[n]["mean"] - delta) for n in live}, sig, delta,
                               budget2 - n_min * len(dominated),
                               se_hat={n: st1[n]["se"] for n in live}, kappa=kappa, n_min=n_min,
                               n_max=N - R1, d_floor=d_floor, alpha=alpha / (2 * m))
        if a is None:
            return None
        alloc.update(a)
    w1 = float(np.sqrt(search_frac))
    pv = {n: combined_directional_p(D[n][:R1], D[n][R1:R1 + alloc[n]], delta, w1) for n in L.names}
    fits = R1 * (1 + m) + allocation_cost(alloc)
    return pv, fits, {"R1": R1, "n_dominated": len(dominated), "alloc_max": max(alloc.values()),
                      "alloc_min": min(alloc.values())}


def run_block(L: Lattice, D: dict, delta_true: dict, b: int, *, delta: float = 0.005, alpha: float = 0.05,
              pcga: dict | None = None, adaptive_kw: dict | None = None) -> list[dict]:
    m = len(L)
    B = b * (1 + m)
    truth = true_frontier(L, delta_true, delta)
    F = truth["F"]
    rows = []

    def rec(proc, reported, fits, A=None, C=None, fs=None, extra=None):
        r = {"procedure": proc, "b": b, "budget": B, "fits": int(fits), "reported": _fmt(reported), "F_true": _fmt(F),
             "exact": set(reported) == F, "false_member": bool(set(reported) - F),
             "n_missed": len(F - set(reported)), "n_reported": len(reported)}
        if A is not None:
            not_adv = {n for n in L.names if delta_true[n] <= delta}
            not_suf = {n for n in L.names if delta_true[n] >= delta}
            r.update({"class_error": bool((A & not_adv) | (C & not_suf)),
                      "false_adv": bool(A & not_adv), "false_suf": bool(C & not_suf),
                      "n_A": len(A), "n_C": len(C), "n_inconclusive": m - len(A) - len(C),
                      "specificity_claim": len(A) == m})
        if fs is not None:
            r.update({"covered": F <= fs["possible_min"], "unc_size": len(fs["possible_min"] - fs["cert_min"]),
                      "possible_min": _fmt(fs["possible_min"]), "min_among_cert": _fmt(fs["min_among_cert"]),
                      "min_cert_not_certmin": len(fs["min_among_cert"] - fs["cert_min"]),
                      "min_cert_false": bool(fs["min_among_cert"] - F)})
        r.update(extra or {})
        rows.append(r)

    # uniform data: b replicates for every element
    pv = {n: directional_p(D[n][:b], delta) for n in L.names}
    means = {n: pv[n]["mean"] for n in L.names}
    A, C = certify(pv, alpha, "holm")
    fs = frontier_sets(L, A, C)
    rec("craf", fs["cert_min"], B, A, C, fs)
    rec("craf_children", _children_cert_min(L, A, C), B, A, C)
    Au, Cu = certify(pv, alpha, "none")
    rec("factorial_unadj", frontier_sets(L, Au, Cu)["cert_min"], B, Au, Cu)
    _, Cn = certify(pv, alpha, "holm", directions=(SUF,))
    rec("ni_holm", frontier_sets(L, set(), Cn)["min_among_cert"], B, set(), Cn)
    rec("naive_point", point_frontier(L, means, delta), B)

    # adaptive (a-priori fallback to craf when infeasible)
    ad = adaptive_pvalues(L, D, b, delta, alpha, **(adaptive_kw or {}))
    if ad is None:
        rec("craf_adaptive", fs["cert_min"], B, A, C, fs, {"fallback": True})
    else:
        pva, fits, info = ad
        Aa, Ca = certify(pva, alpha, "holm")
        fa = frontier_sets(L, Aa, Ca)
        rec("craf_adaptive", fa["cert_min"], fits, Aa, Ca, fa, {"fallback": False, **info})

    if pcga is not None:
        rec("pcga_l", pcga["implied"], pcga["fits"], extra={"pcga_edge_supported": pcga["edge"]})
    for r in rows:
        r.update({"lattice_size": m, "delta": delta, "alpha": alpha})
    return rows


# ------------------------------------------------------------------ pool mode
def pcga_implied(P, idx, alpha: float = 0.05) -> dict:
    """PCGA-L ladder verdicts on instances idx -> lowest ladder lattice element not beaten by a later step."""
    from ..evaluation.methods import _holm, _pcga_verdict, contrasts
    from ..inference.tests import wilcoxon_two_sided

    Dl = contrasts(P, idx, ["er", "degree", "strat:block"])
    S = {"L0": P.empty_test[idx], "L4": P.real_test[idx]}
    S["L1"], S["L2"], S["L3"] = (P.real_test[idx] - Dl[k] for k in ("er", "degree", "strat:block"))
    steps = {"density": S["L1"] - S["L0"], "degree": S["L2"] - S["L1"], "block": S["L3"] - S["L2"],
             "edge": S["L4"] - S["L3"]}
    padj = _holm([wilcoxon_two_sided(v) for v in steps.values()])
    sup = {k: _pcga_verdict(v, pa, alpha) == "supported" for (k, v), pa in zip(steps.items(), padj)}
    if sup["edge"]:
        implied = set()  # no ladder level reproduces the real graph
    elif sup["block"]:
        implied = {"strat:block"}
    else:
        implied = {"degree"}
    return {"implied": implied, "edge": sup["edge"], "fits": 5 * len(idx)}


def run_pool_grid(P, tr: pd.DataFrame, L: Lattice, budgets, block_size: int, *, delta: float, alpha: float,
                  adaptive_kw=None) -> pd.DataFrame:
    from ..evaluation.methods import contrasts

    delta_true = {n: float(tr.loc[n, "delta"]) for n in L.names}
    rows = []
    for e in range(P.N // block_size):
        blk = np.arange(e * block_size, (e + 1) * block_size)
        D = contrasts(P, blk, L.names)
        D = {k: v[np.isfinite(v)] for k, v in D.items()}
        for b in budgets:
            pc = pcga_implied(P, blk[: max(2, b * (1 + len(L)) // 5)], alpha)
            for r in run_block(L, D, delta_true, b, delta=delta, alpha=alpha, pcga=pc, adaptive_kw=adaptive_kw):
                r.update({"scenario": P.scenario, "experiment": e})
                rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ semi-synthetic mode
def semisynthetic_grid(name: str, delta_true: dict, attrs, budgets, n_exp: int, block_size: int, *, sd: float,
                       df_t: float, delta: float, alpha: float, seed: int, adaptive_kw=None) -> pd.DataFrame:
    """Contrasts = Delta_S + sd * t_df / sd(t_df), i.i.d. across replicates and elements."""
    L = Lattice({n: s for n, s in ((k, frozenset() if k == "degree" else frozenset(k[6:].split("+")))
                                   for k in delta_true)})
    rng = np.random.default_rng(seed)
    scale = sd / np.sqrt(df_t / (df_t - 2))
    rows = []
    for e in range(n_exp):
        D = {n: delta_true[n] + scale * rng.standard_t(df_t, block_size) for n in L.names}
        for b in budgets:
            for r in run_block(L, D, delta_true, b, delta=delta, alpha=alpha, adaptive_kw=adaptive_kw):
                r.update({"scenario": name, "experiment": e})
                rows.append(r)
    return pd.DataFrame(rows)
