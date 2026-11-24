"""One-sided tests / lower confidence bounds for a mean paired contrast.

Input: ``d`` = paired differences D_r (real minus comparator), one per *independent
replicate unit* r (a new simulated graph instance for population inference, or an
independent training-seed bundle for conditional inference on a fixed graph/split).
Placebo draws within r must already be averaged into D_r.

Null H0: E[D] <= eps.  Every function returns a dict with the lower bound ``L`` at level
1 - alpha and a p-value ``p`` such that {p <= alpha} == {L > eps} (up to numerics), so that
marginal results can be combined by the intersection-union rule.

Methods and their validity conditions
-------------------------------------
* ``t``        one-sided Student t.  Exact under i.i.d. normal D; asymptotically valid
               otherwise.  PRIMARY method (justified by A/A calibration in the pilot).
* ``boot``     percentile bootstrap of the mean (sensitivity).  Asymptotic only; known to
               undercover for small n.
* ``signflip`` sign-flip randomisation test of mean(D - eps).  Exact if D - eps is
               symmetric about 0 under H0 (an *assumption*, not implied by H0).  p only.
* ``eb``       Maurer & Pontil (2009, Thm 4) empirical-Bernstein bound.  Finite-sample
               valid for i.i.d. D in a known interval [lo, hi].  Conservative.
* ``wsr``      Waudby-Smith & Ramdas (2024) betting bound with predictable plug-in bets.
               Finite-sample valid for i.i.d. (indeed martingale) D in [lo, hi].
* ``rank``     (separate function) Monte Carlo rank test of a single real score against K
               placebo scores; exact ONLY if real and placebo outcomes are exchangeable
               under H0 (e.g. group-orbit placebos, or Besag--Clifford swap chains under a
               uniform-on-class null).  Not a test of E[D] <= eps.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def _clean(d) -> np.ndarray:
    d = np.asarray(d, dtype=float).ravel()
    if not np.all(np.isfinite(d)):
        raise ValueError("paired differences must be finite")
    return d


def t_lower(d, alpha: float = 0.05, eps: float = 0.0) -> dict:
    d = _clean(d)
    n = len(d)
    if n < 2:
        return {"method": "t", "n": n, "mean": float(d.mean()) if n else np.nan, "L": -np.inf, "p": 1.0}
    mean, sd = float(d.mean()), float(d.std(ddof=1))
    se = sd / np.sqrt(n)
    q = stats.t.ppf(1 - alpha, n - 1)
    if se <= 1e-12 * max(1.0, abs(mean)):  # constant differences (round-off tolerant)
        p = 0.0 if mean > eps else 1.0
        L = mean
    else:
        p = float(stats.t.sf((mean - eps) / se, n - 1))
        L = mean - q * se
    return {"method": "t", "n": n, "mean": mean, "se": se, "L": float(L), "p": p}


def boot_lower(d, alpha: float = 0.05, eps: float = 0.0, n_boot: int = 4000, seed: int = 0) -> dict:
    d = _clean(d)
    n = len(d)
    rng = np.random.default_rng(seed)
    means = d[rng.integers(0, n, size=(n_boot, n))].mean(1)
    L = float(np.quantile(means, alpha))
    # percentile-interval inversion: p = smallest alpha' with L(alpha') > eps
    p = float((np.sum(means <= eps) + 1) / (n_boot + 1))
    return {"method": "boot", "n": n, "mean": float(d.mean()), "L": L, "p": min(1.0, p)}


def signflip_test(d, alpha: float = 0.05, eps: float = 0.0, n_flip: int = 4000, seed: int = 0) -> dict:
    d = _clean(d) - eps
    n = len(d)
    obs = d.mean()
    if n <= 14:
        signs = ((np.arange(2**n)[:, None] >> np.arange(n)) & 1) * 2 - 1
        null = (signs * np.abs(d)).mean(1)
        p = float(np.mean(null >= obs - 1e-15))
    else:
        rng = np.random.default_rng(seed)
        signs = rng.choice([-1.0, 1.0], size=(n_flip, n))
        null = (signs * np.abs(d)).mean(1)
        p = float((1 + np.sum(null >= obs - 1e-15)) / (n_flip + 1))
    return {"method": "signflip", "n": n, "mean": float(obs + eps), "L": np.nan, "p": p}


def eb_lower(d, alpha: float = 0.05, eps: float = 0.0, lo: float = -1.0, hi: float = 1.0) -> dict:
    """Maurer--Pontil empirical Bernstein lower bound for i.i.d. D in [lo, hi]."""
    d = _clean(d)
    n = len(d)
    if (d < lo - 1e-12).any() or (d > hi + 1e-12).any():
        raise ValueError("data outside the declared bounded range")
    z = (d - lo) / (hi - lo)
    v = z.var(ddof=1) if n > 1 else 0.25

    def L_of(a):
        if n < 2:
            return -np.inf
        lg = np.log(2.0 / a)
        lz = z.mean() - np.sqrt(2 * v * lg / n) - 7 * lg / (3 * (n - 1))
        return lo + (hi - lo) * lz

    L = float(L_of(alpha))
    # p-value: smallest a in (0,1] with L(a) > eps (L increasing in a); bisection on log scale
    if L_of(1.0) <= eps:
        p = 1.0
    else:
        a_lo, a_hi = 1e-12, 1.0
        if L_of(a_lo) > eps:
            p = a_lo
        else:
            for _ in range(80):
                mid = np.sqrt(a_lo * a_hi)
                if L_of(mid) > eps:
                    a_hi = mid
                else:
                    a_lo = mid
            p = a_hi
    return {"method": "eb", "n": n, "mean": float(d.mean()), "L": L, "p": float(p)}


def _wsr_logwealth_max(z: np.ndarray, m: float, alpha: float, c: float = 0.75) -> float:
    """max_t log K_t(m) for H0: E z <= m, z in [0,1], predictable plug-in bets (fixed-n tuning).

    Bets are truncated to [0, c] with c < 1 *independently of m*; since m <= 1 this keeps
    1 + lam (z - m) >= 1 - c > 0, and it makes log K_t(m) strictly decreasing in m, so the
    rejected set is an interval [0, L) and bisection returns a valid bound.
    """
    n = len(z)
    mu_hat, var_hat = 0.5, 0.25
    s1, s2 = 0.0, 0.0
    logk, best = 0.0, 0.0
    for t in range(n):
        lam = np.sqrt(2 * np.log(1 / alpha) / (n * var_hat))
        lam = min(max(lam, 0.0), c)
        logk += np.log1p(lam * (z[t] - m))
        best = max(best, logk)
        s1 += z[t]
        mu_hat = (0.5 + s1) / (t + 2)
        s2 += (z[t] - mu_hat) ** 2
        var_hat = (0.25 + s2) / (t + 2)
    return best


def wsr_lower(d, alpha: float = 0.05, eps: float = 0.0, lo: float = -1.0, hi: float = 1.0) -> dict:
    """Waudby-Smith--Ramdas betting lower bound (Ville's inequality); data order = given order."""
    d = _clean(d)
    if (d < lo - 1e-12).any() or (d > hi + 1e-12).any():
        raise ValueError("data outside the declared bounded range")
    z = (d - lo) / (hi - lo)
    thr = np.log(1 / alpha)
    # rejected set {m : max log K(m) >= thr} is [0, L_z); bisection on m in [0, 1]
    a, b = 0.0, 1.0
    if _wsr_logwealth_max(z, 1e-9, alpha) < thr:
        Lz = 0.0
    else:
        for _ in range(50):
            mid = 0.5 * (a + b)
            if _wsr_logwealth_max(z, mid, alpha) >= thr:
                a = mid
            else:
                b = mid
        Lz = a
    m0 = (eps - lo) / (hi - lo)
    p = float(min(1.0, np.exp(-_wsr_logwealth_max(z, m0, alpha))))
    return {"method": "wsr", "n": len(d), "mean": float(d.mean()), "L": lo + (hi - lo) * Lz, "p": p}


METHODS = {"t": t_lower, "boot": boot_lower, "signflip": signflip_test, "eb": eb_lower, "wsr": wsr_lower}


def lower_bound(d, method: str = "t", alpha: float = 0.05, eps: float = 0.0, **kw) -> dict:
    return METHODS[method](d, alpha=alpha, eps=eps, **kw)


def rank_test(real_score: float, placebo_scores, larger_is_better: bool = True) -> dict:
    """PCGA Monte Carlo rank p-value (1 + #{placebo >= real}) / (K + 1).

    Exact under exchangeability of (real, placebos) -- the caller must justify that.
    Ties count against the real graph (conservative).
    """
    s = np.asarray(placebo_scores, dtype=float)
    k = len(s)
    if not larger_is_better:
        s, real_score = -s, -real_score
    p = (1 + int(np.sum(s >= real_score))) / (k + 1)
    return {"method": "rank", "K": k, "rank": 1 + int(np.sum(s >= real_score)), "p": float(p)}


def wilcoxon_two_sided(d) -> float:
    d = _clean(d)
    if len(d) < 2 or np.all(d == 0):
        return 1.0
    return float(stats.wilcoxon(d, alternative="two-sided").pvalue)
