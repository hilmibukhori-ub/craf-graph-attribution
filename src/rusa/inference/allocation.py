"""Full-set certification with screening: allocation, two-stage elimination, adaptive combination.

Selected-set procedures (screen -> confirm top-m) certify only theta_sel. Every procedure here
certifies the whole enumerated candidate set J (plus the empty graph), because **every**
comparator is tested at some stage. Development (stage-1) data decide how much stage-2 budget
each comparator receives, and optionally certify comparators early.

Validity (docs/phase2b_math.md, Props. 4-6):
* ``fullset_two_stage`` (alloc / elim): comparator j is certified either on stage-1 data at level
  alpha1 or on independent stage-2 data at level alpha2. For the binding comparator j* under H0,
  P(claim) <= alpha1 + alpha2. The allocation is a function of stage-1 data only, so stage-2
  tests are valid conditionally on it. Mis-allocation costs power, never validity.
* ``combination_test`` (adaptive): inverse-normal combination of independent stage-wise
  one-sided p-values with weights fixed in advance (Bauer & Koehne 1994; Lehmacher & Wassmer
  1999). Under H0_j the stage-2 p-value is (super-)uniform conditionally on stage 1, whatever
  sample size stage 1 chose, so the combined p-value is valid. Interim efficacy at alpha1 plus a
  combination test at alpha2 gives level alpha1 + alpha2 by the union bound.

Allocation rule (minimax power): the one-sided t-test of comparator j with n_j replicates and
margin d_j = Delta_j - eps has approximate power
  pi_j(n) = Phi( sqrt(n) d_j / s - t_{1-a, n-1} ).
For an IUT, P(all reject) >= 1 - sum_j (1 - pi_j), so we maximise the smallest per-comparator
power: choose the largest common target q with n_j(q) = min{n >= n_min : pi_j(n) >= q} affordable.
Plug-in d_j is the conservative stage-1 estimate max(delta_hat_j - kappa * se_j - eps, d_floor).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from .tests import lower_bound


def allocation_cost(n: dict[str, int]) -> int:
    """One real-graph fit per stage-2 instance (max n_j) plus one fit per comparator-instance."""
    return (max(n.values()) if n else 0) + int(sum(n.values()))


from functools import lru_cache


@lru_cache(maxsize=64)
def _tcrit(a: float, n_max: int) -> np.ndarray:
    """t_{1-a, n-1} for n = 0..n_max (inf for n < 2)."""
    out = np.full(n_max + 1, np.inf)
    n = np.arange(2, n_max + 1)
    out[2:] = stats.t.ppf(1 - a, n - 1)
    return out


def _power_curve(d: float, s: float, a: float, n_max: int) -> np.ndarray:
    n = np.arange(n_max + 1)
    return stats.norm.cdf(np.sqrt(n) * d / s - _tcrit(a, n_max))


def optimal_allocation(delta_hat: dict[str, float], sigma_hat: float, eps: float, budget: int, *,
                       se_hat: dict[str, float] | None = None, kappa: float = 1.0, n_min: int = 5,
                       n_max: int = 100, d_floor: float = 0.003, alpha: float = 0.05) -> dict[str, int] | None:
    """Minimax-power integer allocation within ``budget`` (cost = allocation_cost). None if infeasible."""
    names = list(delta_hat)
    if not names:
        raise ValueError("no comparators")
    se_hat = se_hat or {k: 0.0 for k in names}
    d = {k: max(delta_hat[k] - kappa * se_hat.get(k, 0.0) - eps, d_floor) for k in names}
    s = max(float(sigma_hat), 1e-9)
    # power curve per comparator, tabulated once
    curves = {k: _power_curve(d[k], s, alpha, n_max) for k in names}

    def need(q):
        out = {}
        for k in names:
            ok = np.flatnonzero(curves[k][n_min:] >= q)
            out[k] = n_min + int(ok[0]) if len(ok) else n_max
        return out

    if allocation_cost({k: n_min for k in names}) > budget:
        return None
    lo, hi = 0.0, 1.0 - 1e-12
    if allocation_cost(need(hi)) <= budget:
        best = need(hi)
    else:
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if allocation_cost(need(mid)) <= budget:
                lo = mid
            else:
                hi = mid
        best = need(lo)
    # spend leftover budget on the comparators with the lowest power, one replicate at a time
    left = budget - allocation_cost(best)
    while left > 0:
        k = min(names, key=lambda k: (curves[k][min(best[k], n_max)], k))
        if best[k] >= n_max:
            break
        extra = 2 if best[k] + 1 > max(best.values()) else 1
        if extra > left:
            break
        best[k] += 1
        left -= extra
    return best


def uniform_allocation(names: list[str], budget: int, n_max: int = 100) -> dict[str, int]:
    n = min(n_max, budget // (1 + len(names)))
    return {k: n for k in names}


def fullset_two_stage(D_dev: dict[str, np.ndarray] | None, D_conf: dict[str, np.ndarray], alpha1: float,
                      alpha2: float, eps: float = 0.0, method: str = "t") -> dict:
    """Two-stage full-set IUT: stage-1 certification at alpha1 (alpha1 = 0 disables it), otherwise
    stage-2 certification at alpha2. Robust lower bound valid at level alpha1 + alpha2."""
    names = list(D_conf) if D_dev is None else list(D_dev)
    stage, res = {}, {}
    for k in names:
        if D_dev is not None and alpha1 > 0 and len(D_dev[k]) >= 2:
            r1 = lower_bound(D_dev[k], method, alpha1, eps)
            if r1["L"] > eps:
                stage[k], res[k] = "dev", r1
                continue
        if k not in D_conf or len(D_conf[k]) < 2:
            stage[k], res[k] = "untested", {"L": -np.inf, "p": 1.0, "mean": np.nan, "n": 0}
            continue
        stage[k], res[k] = "conf", lower_bound(D_conf[k], method, alpha2, eps)
    L = min(r["L"] for r in res.values())
    return {"certified": bool(L > eps), "L_robust": float(L), "stage": stage, "marginal": res,
            "n_eliminated": sum(v == "dev" for v in stage.values()),
            "argmin": min(res, key=lambda k: res[k]["L"]), "level": alpha1 + alpha2}


def _summ(d):
    d = np.asarray(d, float)
    n = len(d)
    if n < 2:
        return None
    m, sd = float(d.mean()), float(d.std(ddof=1))
    return m, max(sd / math.sqrt(n), 1e-12 * max(1.0, abs(m))), n - 1


def _t_p_s(sm, eps):
    if sm is None:
        return 1.0
    m, se, df = sm
    return float(stats.t.sf((m - eps) / se, df))


def _combine(p1, p2, w1):
    w2 = math.sqrt(1 - w1 * w1)
    z1 = stats.norm.isf(min(max(p1, 1e-300), 1 - 1e-16))
    z2 = stats.norm.isf(min(max(p2, 1e-300), 1 - 1e-16))
    return float(stats.norm.sf(w1 * z1 + w2 * z2))


def combination_p(d1, d2, w1: float, eps: float) -> float:
    """Inverse-normal combination p-value of stage-wise one-sided t p-values (weights fixed a priori)."""
    return _combine(_t_p_s(_summ(d1), eps), _t_p_s(_summ(d2), eps), w1)


def combination_test(d1, d2, w1: float, alpha: float, eps: float = 0.0) -> dict:
    """Combination test and its inverted lower confidence bound (p is increasing in the margin)."""
    s1, s2 = _summ(d1), _summ(d2)

    def pf(e):
        return _combine(_t_p_s(s1, e), _t_p_s(s2, e), w1)

    p = pf(eps)
    lo, hi = -1.0, 1.0
    if pf(lo) > alpha:
        L = -np.inf
    else:
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if pf(mid) <= alpha:
                lo = mid
            else:
                hi = mid
        L = lo
    allv = np.concatenate([np.asarray(d1, float), np.asarray(d2, float)])
    return {"p": p, "L": float(L), "mean": float(allv.mean()) if len(allv) else np.nan}


def fullset_adaptive(D1: dict[str, np.ndarray], D2: dict[str, np.ndarray], w1: float, alpha1: float,
                     alpha2: float, eps: float = 0.0) -> dict:
    """Adaptive two-stage full-set IUT: interim certification at alpha1 on stage 1; otherwise an
    inverse-normal combination test of stage 1 and stage 2 at alpha2."""
    stage, res = {}, {}
    for k in D1:
        if alpha1 > 0 and len(D1[k]) >= 2:
            r1 = lower_bound(D1[k], "t", alpha1, eps)
            if r1["L"] > eps:
                stage[k], res[k] = "dev", r1
                continue
        if k not in D2 or len(D2[k]) < 2:
            stage[k], res[k] = "untested", {"L": -np.inf, "p": 1.0, "mean": np.nan}
            continue
        stage[k], res[k] = "combined", combination_test(D1[k], D2[k], w1, alpha2, eps)
    L = min(r["L"] for r in res.values())
    return {"certified": bool(L > eps), "L_robust": float(L), "stage": stage, "marginal": res,
            "n_eliminated": sum(v == "dev" for v in stage.values()),
            "argmin": min(res, key=lambda k: res[k]["L"]), "level": alpha1 + alpha2}
