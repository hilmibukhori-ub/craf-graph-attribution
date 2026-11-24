"""CRAF core: property-subset lattice, three-way simultaneous certification, frontier sets.

Lattice. Each element is a set S of declared stratification attributes. Its null N_S is a
degree-preserving swap null that preserves, for every node, the neighbour counts in each joint
stratum of S (S = {} is the plain degree null). If S ⊂ T, then N_T preserves everything N_S
preserves, so the *constraints* are nested. The *performance* Delta_S is NOT assumed to be
monotone along the lattice, and nothing below uses monotonicity.

Estimands (margin delta > 0, fixed in advance):
  Delta_S = mu(G0) - mu(N_S)              relational advantage of G0 over N_S
  advantage(S)  :  Delta_S >  delta       G0 carries meaningful information beyond S
  sufficient(S) :  Delta_S <  delta       preserving S reproduces G0's performance within delta
  F = min_⊆ { S in L : sufficient(S) }    minimal sufficient property combinations (the frontier)
  relational specificity over L: min_S Delta_S > delta (no element of L is sufficient)

Certification. For each S there are two one-sided hypotheses:
  H_adv(S): Delta_S <= delta (rejecting it certifies advantage);
  H_suf(S): Delta_S >= delta (rejecting it certifies sufficiency).
All 2|L| hypotheses go through Holm's step-down at level alpha. Holm controls the FWER under
arbitrary dependence, so P(any false certification) <= alpha. Holm depends only on the multiset
of p-values, which makes the procedure order-independent: the result does not depend on the order
in which attributes or lattice elements are enumerated.

Frontier sets (computed from the certified sets A = advantage, C = sufficient):
  cert_min         = {S in C : every proper subset T in L is in A}
  min_among_cert   = {S in C : no proper subset T in L is in C}       (NOT a minimality guarantee)
  possible_min     = {S not in A : no proper subset T in L is in C}
On the event E that no false certification occurs (P(E) >= 1 - alpha):
  cert_min ⊆ F ⊆ possible_min, and every S in C contains at least one element of F.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import stats

ADV, SUF = "adv", "suf"


def element_of(name: str):
    """Lattice element (frozenset of attributes) for a pool variant name, or None if not a lattice null."""
    if name == "degree":
        return frozenset()
    if name.startswith("strat:"):
        return frozenset(name[len("strat:"):].split("+"))
    return None


def element_name(S) -> str:
    return "degree" if not S else "strat:" + "+".join(sorted(S))


@dataclass
class Lattice:
    sets: dict  # name -> frozenset

    @classmethod
    def from_names(cls, names, attrs=None, max_order: int | None = None) -> "Lattice":
        out = {}
        for n in names:
            S = element_of(n)
            if S is None:
                continue
            if attrs is not None and not S <= set(attrs):
                continue
            if max_order is not None and len(S) > max_order:
                continue
            out[n] = S
        return cls(out)

    @property
    def names(self) -> list[str]:
        return sorted(self.sets, key=lambda n: (len(self.sets[n]), sorted(self.sets[n])))

    def proper_subsets(self, n: str) -> list[str]:
        S = self.sets[n]
        return [m for m in self.names if self.sets[m] < S]

    def __len__(self):
        return len(self.sets)


# ------------------------------------------------------------------ marginal p-values
def _summ(d):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = len(d)
    if n < 2:
        return None
    m, sd = float(d.mean()), float(d.std(ddof=1))
    return m, max(sd / math.sqrt(n), 1e-12 * max(1.0, abs(m))), n - 1


def directional_p(d, delta: float) -> dict:
    """One-sided t p-values for H_adv: mean <= delta and H_suf: mean >= delta (p_adv + p_suf = 1)."""
    s = _summ(d)
    if s is None:
        return {ADV: 1.0, SUF: 1.0, "mean": np.nan, "se": np.nan, "n": 0}
    m, se, df = s
    p_adv = float(stats.t.sf((m - delta) / se, df))
    return {ADV: p_adv, SUF: 1.0 - p_adv, "mean": m, "se": se, "n": df + 1}


def _norm_p(z):
    return float(stats.norm.sf(z))


def combined_directional_p(d1, d2, delta: float, w1: float) -> dict:
    """Inverse-normal combination (fixed w1) of stage-wise one-sided t p-values, both directions.

    The two directions are exact mirror images: z_suf = -z_adv in each stage, so p_suf = 1 - p_adv.
    Valid for any stage-2 size chosen from stage-1 data, provided stage 2 is independent of stage 1.
    """
    a, b = directional_p(d1, delta), directional_p(d2, delta)
    if a["n"] < 2 or b["n"] < 2:
        raise ValueError("each stage needs >= 2 replicates")
    w2 = math.sqrt(1 - w1 * w1)
    z = w1 * stats.norm.isf(min(max(a[ADV], 1e-300), 1 - 1e-16)) + w2 * stats.norm.isf(min(max(b[ADV], 1e-300), 1 - 1e-16))
    allv = np.concatenate([np.asarray(d1, float), np.asarray(d2, float)])
    return {ADV: _norm_p(z), SUF: _norm_p(-z), "mean": float(np.nanmean(allv)), "n": a["n"] + b["n"]}


# ------------------------------------------------------------------ multiplicity
def holm(p: dict, alpha: float) -> set:
    """Holm step-down; returns the rejected keys. Ties are broken by key, which does not affect the result."""
    items = sorted(p.items(), key=lambda kv: (kv[1], str(kv[0])))
    m = len(items)
    rej = set()
    for i, (k, v) in enumerate(items):
        if v <= alpha / (m - i):
            rej.add(k)
        else:
            break
    return rej


def certify(pv: dict, alpha: float, method: str = "holm", directions=(ADV, SUF)) -> tuple[set, set]:
    """pv: name -> {adv: p, suf: p}. Returns (A, C) = certified advantage / certified sufficient names."""
    P = {(n, d): pv[n][d] for n in pv for d in directions}
    if method == "holm":
        rej = holm(P, alpha)
    elif method == "bonferroni":
        rej = {k for k, v in P.items() if v <= alpha / len(P)}
    elif method == "none":
        rej = {k for k, v in P.items() if v <= alpha}
    else:
        raise ValueError(method)
    return {n for n, d in rej if d == ADV}, {n for n, d in rej if d == SUF}


# ------------------------------------------------------------------ frontier
def frontier_sets(L: Lattice, A: set, C: set) -> dict:
    cert_min, min_cert, possible = set(), set(), set()
    gaps = {}
    for n in L.names:
        sub = L.proper_subsets(n)
        if n in C and all(t in A for t in sub):
            cert_min.add(n)
        if n in C and not any(t in C for t in sub):
            min_cert.add(n)
            unresolved = [t for t in sub if t not in A]
            if unresolved:
                gaps[n] = unresolved  # subsets that might still be sufficient
        if n not in A and not any(t in C for t in sub):
            possible.add(n)
    return {"cert_min": cert_min, "min_among_cert": min_cert, "possible_min": possible, "gaps": gaps,
            "A": set(A), "C": set(C), "inconclusive": set(L.names) - set(A) - set(C)}


def true_frontier(L: Lattice, delta_true: dict, delta: float) -> dict:
    suff = {n for n in L.names if delta_true[n] < delta}
    F = {n for n in suff if not any(t in suff for t in L.proper_subsets(n))}
    return {"F": F, "suff": suff, "ins": set(L.names) - suff}


def point_frontier(L: Lattice, means: dict, delta: float) -> set:
    """Naive point-estimate frontier: minimal elements of {S : mean_S < delta}."""
    return true_frontier(L, means, delta)["F"]
