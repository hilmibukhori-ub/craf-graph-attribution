"""Robust certificates over a *frozen, finite* comparator set.

Given paired-difference arrays D[:, j] for comparators j (empty graph and each frozen null
family), with independent replicate units in rows:

* intersection--union (IUT): p_RUSA = max_j p_j;   L_robust = min_j L_j.
  Valid for H0: theta = min_j Delta_j <= eps whenever every marginal test is valid and
  the comparator set was fixed independently of the confirmatory data.
* simultaneous bounds (Bonferroni): each L_j at level alpha/J; covers all Delta_j jointly.
* nested robustness radius over levels Q_1 subset Q_2 subset ...: with marginal level-alpha
  bounds, rho_hat = max{lam : min_{j in Q_lam} L_j > eps} satisfies
  P(rho_hat > rho*) <= alpha (proof in docs/mathematical_spec.md, Prop. 3).  The reported
  *curve* of lower bounds theta(lam) needs simultaneous bounds and uses Bonferroni.

Guarantees never extend beyond the enumerated, frozen comparator sets.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .tests import lower_bound


@dataclass
class Certificate:
    comparators: list[str]
    method: str
    alpha: float
    eps: float
    marginal: dict = field(default_factory=dict)  # name -> dict(L, p, mean, ...)
    theta_hat: float = np.nan
    L_robust: float = np.nan
    p_iut: float = np.nan
    argmin_L: str = ""
    certified: bool = False

    def as_row(self) -> dict:
        row = {
            "method": self.method, "alpha": self.alpha, "eps": self.eps,
            "comparators": "|".join(self.comparators), "theta_hat": self.theta_hat,
            "L_robust": self.L_robust, "p_iut": self.p_iut, "argmin_L": self.argmin_L,
            "certified": self.certified,
        }
        for k, v in self.marginal.items():
            row[f"mean[{k}]"] = v.get("mean")
            row[f"L[{k}]"] = v.get("L")
            row[f"p[{k}]"] = v.get("p")
        return row


def iut_certificate(D: dict[str, np.ndarray], method: str = "t", alpha: float = 0.05,
                    eps: float = 0.0, **kw) -> Certificate:
    if not D:
        raise ValueError("empty comparator set")
    names = list(D)
    marg = {k: lower_bound(D[k], method=method, alpha=alpha, eps=eps, **kw) for k in names}
    Ls = {k: marg[k]["L"] for k in names}
    ps = {k: marg[k]["p"] for k in names}
    means = {k: marg[k]["mean"] for k in names}
    p_iut = max(ps.values())
    has_L = all(np.isfinite(v) or v == -np.inf for v in Ls.values())
    if has_L:
        argmin = min(names, key=lambda k: Ls[k])
        L_rob = Ls[argmin]
        certified = bool(L_rob > eps)
    else:  # p-value-only method (sign-flip): decision from the IUT p-value
        argmin = max(names, key=lambda k: ps[k])
        L_rob = np.nan
        certified = bool(p_iut <= alpha)
    return Certificate(names, method, alpha, eps, marg, float(min(means.values())), float(L_rob),
                       float(p_iut), argmin, certified)


def bonferroni_bounds(D: dict[str, np.ndarray], method="t", alpha=0.05, eps=0.0, **kw) -> dict:
    J = len(D)
    return {k: lower_bound(v, method=method, alpha=alpha / J, eps=eps, **kw) for k, v in D.items()}


def nested_radius(D: dict[str, np.ndarray], levels: list[list[str]], method="t", alpha=0.05,
                  eps=0.0, **kw) -> dict:
    """Certified robustness radius over nested comparator sets (levels[i] subset levels[i+1])."""
    for a, b in zip(levels[:-1], levels[1:]):
        if not set(a) <= set(b):
            raise ValueError("comparator levels must be nested")
    marg = {k: lower_bound(D[k], method=method, alpha=alpha, eps=eps, **kw) for k in levels[-1]}
    simul = bonferroni_bounds({k: D[k] for k in levels[-1]}, method, alpha, eps, **kw)
    rho, curve = 0, []
    for lam, Q in enumerate(levels, start=1):
        Lm = min(marg[k]["L"] for k in Q)
        Ls = min(simul[k]["L"] for k in Q)
        th = min(marg[k]["mean"] for k in Q)
        curve.append({"level": lam, "theta_hat": th, "L_marginal_min": Lm, "L_simultaneous_min": Ls,
                      "set": "|".join(Q)})
        if Lm > eps and rho == lam - 1:
            rho = lam
    return {"rho_hat": rho, "curve": curve}
