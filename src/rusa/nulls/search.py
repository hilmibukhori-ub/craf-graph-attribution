"""Budgeted search for the hardest admissible null on DEVELOPMENT data only.

Objective (to be minimised): the paired development contrast
    Delta_dev(Q) = E[S_dev(real) - S_dev(placebo ~ Q)],
i.e. we look for the null under which the placebo model performs closest to (or better
than) the real-graph model.  One "pull" of arm Q = one retrained placebo model evaluated on
development (validation) nodes.  The budget counts every model fit, including the real-graph
fits needed to pair the pulls.

Algorithms
* ``uniform``             equal pulls per arm (fixed-menu baseline at equal budget).
* ``successive_halving``  Karnin et al. (2013) / Jamieson & Talwalkar (2016): ceil(log2 K)
                          rounds with equal budget per round, keeping the best half.
Both return the full log of pulls, the ranking and the frozen selection.  Neither has a
global-optimality guarantee for the population ranking at a finite budget; misses are
measured empirically (``regret``), and certificates never extend to unselected arms.

Arms are accessed through a ``PullOracle`` so the same code runs on precomputed pools
(Monte Carlo studies) and on live fits.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Protocol

import numpy as np


class PullOracle(Protocol):
    def pull(self, arm: str, j: int) -> tuple[float, int]:
        """Return (paired dev contrast of the j-th pull of ``arm``, new fits consumed)."""

    def max_pulls(self, arm: str) -> int: ...


@dataclass
class SearchResult:
    algorithm: str
    budget: int
    fits_used: int
    selected: list[str]
    ranking: list[str]
    arm_stats: dict
    log: list = field(default_factory=list)

    def freeze(self, path: str | Path, extra: dict | None = None) -> str:
        """Serialise the selection *before* any confirmatory data are touched; return sha256."""
        import hashlib

        payload = {"search": asdict(self), **(extra or {})}
        text = json.dumps(payload, indent=1, sort_keys=True, default=float)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text)
        return hashlib.sha256(text.encode()).hexdigest()


def _stats(values: dict[str, list[float]]) -> dict:
    out = {}
    for k, v in values.items():
        a = np.asarray(v, dtype=float)
        a = a[np.isfinite(a)]
        out[k] = {"n": int(len(a)), "mean": float(a.mean()) if len(a) else float("nan"),
                  "se": float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")}
    return out


def _mean(v) -> float:
    a = np.asarray(v, dtype=float)
    a = a[np.isfinite(a)]
    return float(a.mean()) if len(a) else float("inf")


def _rank(values: dict[str, list[float]]) -> list[str]:
    # hardest first: smallest mean dev contrast; ties broken by name for determinism
    return sorted(values, key=lambda k: (_mean(values[k]), k))


def uniform_search(oracle: PullOracle, arms: list[str], budget: int, top_m: int = 2) -> SearchResult:
    """Round-robin equal allocation until the budget (or the pool) is exhausted."""
    vals = {a: [] for a in arms}
    log, used, j = [], 0, 0
    while True:
        progressed = False
        for a in arms:
            if j >= oracle.max_pulls(a):
                continue
            c = oracle.cost(a, j)
            if used + c > budget:
                continue
            v, c = oracle.pull(a, j)
            used += c
            vals[a].append(v)
            log.append({"round": j, "arm": a, "pull": j, "value": v, "fits": c})
            progressed = True
        j += 1
        if not progressed:
            break
    ranking = _rank(vals)
    return SearchResult("uniform", budget, used, ranking[:top_m], ranking, _stats(vals), log)


def successive_halving(oracle: PullOracle, arms: list[str], budget: int, top_m: int = 2) -> SearchResult:
    vals = {a: [] for a in arms}
    surv = list(arms)
    rounds = max(1, math.ceil(math.log2(max(len(arms), 2) / max(top_m, 1))))
    per_round = budget / rounds
    log, used = [], 0
    for r in range(rounds):
        n_r = max(1, int(per_round // max(len(surv), 1)))
        for a in surv:
            for _ in range(n_r):
                j = len(vals[a])
                if j >= oracle.max_pulls(a):
                    break
                c = oracle.cost(a, j)
                if used + c > budget:
                    break
                v, c = oracle.pull(a, j)
                used += c
                vals[a].append(v)
                log.append({"round": r, "arm": a, "pull": j, "value": v, "fits": c})
        ranked = sorted(surv, key=lambda k: (_mean(vals[k]), k))
        keep = max(top_m, math.ceil(len(surv) / 2))
        surv = ranked[:keep]
        if len(surv) <= top_m:
            break
    # final ranking: survivors first (by mean), then eliminated arms by mean
    elim = [a for a in _rank(vals) if a not in surv]
    surv_ranked = sorted(surv, key=lambda k: (_mean(vals[k]), k))
    ranking = surv_ranked + elim
    return SearchResult("successive_halving", budget, used, surv_ranked[:top_m], ranking, _stats(vals), log)


def random_search(oracle: PullOracle, arms: list[str], budget: int, top_m: int = 2,
                  rng: np.random.Generator | None = None, pulls_per_arm: int = 2) -> SearchResult:
    """Random-search baseline (as in hyperparameter optimisation): visit arms in a uniformly random
    order, give each ``pulls_per_arm`` pulls, stop when the budget is exhausted; select the top-m
    of the visited arms.  Unvisited arms can never be selected."""
    rng = rng if rng is not None else np.random.default_rng(0)
    order = [arms[i] for i in rng.permutation(len(arms))]
    vals = {a: [] for a in arms}
    log, used = [], 0
    for a in order:
        for j in range(pulls_per_arm):
            if j >= oracle.max_pulls(a):
                break
            c = oracle.cost(a, j)
            if used + c > budget:
                break
            v, c = oracle.pull(a, j)
            used += c
            vals[a].append(v)
            log.append({"round": 0, "arm": a, "pull": j, "value": v, "fits": c})
        if used >= budget:
            break
    visited = {a: v for a, v in vals.items() if v}
    ranking = _rank(visited) + [a for a in order if a not in visited]
    return SearchResult("random", budget, used, ranking[:top_m], ranking, _stats(vals), log)


ALGORITHMS = {"uniform": uniform_search, "successive_halving": successive_halving, "random": random_search}


class PoolOracle:
    """Pull oracle over a precomputed pool of *development* instances.

    Pull j of arm a uses dev instance (j mod R_dev) and draw (j // R_dev), so successive
    pulls spread over independent instances first.  The real-graph dev fit of an instance
    is charged once, the first time any arm uses that instance.
    """

    def __init__(self, real_val: np.ndarray, cand_val: dict[str, np.ndarray]):
        self.real_val = real_val                     # (R_dev,)
        self.cand_val = cand_val                     # arm -> (R_dev, b) with NaN for invalid
        self.R = len(real_val)
        self.b = next(iter(cand_val.values())).shape[1]
        self.paid = set()

    def max_pulls(self, arm):
        return self.R * self.b

    def _loc(self, j):
        return j % self.R, j // self.R

    def cost(self, arm, j):
        i, _ = self._loc(j)
        return 1 + (0 if i in self.paid else 1)

    def pull(self, arm, j):
        i, k = self._loc(j)
        c = self.cost(arm, j)
        self.paid.add(i)
        v = self.real_val[i] - self.cand_val[arm][i, k]
        return float(v), c
