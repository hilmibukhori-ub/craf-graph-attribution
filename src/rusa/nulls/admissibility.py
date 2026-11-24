"""Admissibility audit for graph null samples and candidate generators.

Hard constraints are verified *exactly* on every sample; a violation makes the sample
invalid.  Soft diagnostics are measured and compared with pre-declared, label-free
thresholds (``AdmissibilityPolicy``); a soft failure rejects the sample as degenerate or
near-identical.  Neither step uses labels, splits or model scores, so the audit can run
before any confirmatory evaluation.

Admissibility is a modelling assumption declared by the analyst (which properties a
"no relation-specific information" world would preserve).  Passing the audit establishes
that a sample satisfies the declared constraints; it does NOT establish exchangeability
of G0 with the null or the scientific credibility of the declaration.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np

from .generators import Graph, NullSpec, edge_overlap, neighbour_stratum_counts, stratum_codes


@dataclass(frozen=True)
class AdmissibilityPolicy:
    """Pre-declared, label-free rejection thresholds (soft constraints)."""

    max_edge_overlap: float = 0.80        # near-identical placebo if more edges are retained
    min_swap_completion: float = 0.95     # achieved / target swaps for MCMC nulls
    min_candidate_acceptance: float = 0.80  # fraction of valid samples for a candidate
    max_pairwise_overlap: float = 0.90    # effective diversity floor among placebo draws


@dataclass
class AdmissibilityResult:
    valid: bool
    generator: str
    seed_key: tuple
    violated_hard: list[str] = field(default_factory=list)
    violated_soft: list[str] = field(default_factory=list)
    diagnostics: dict = field(default_factory=dict)
    settings: dict = field(default_factory=dict)

    def to_row(self) -> dict:
        d = asdict(self)
        d["violated_hard"] = ";".join(self.violated_hard)
        d["violated_soft"] = ";".join(self.violated_soft)
        d["seed_key"] = "-".join(map(str, self.seed_key))
        diag = d.pop("diagnostics")
        sett = d.pop("settings")
        d.update({f"diag_{k}": v for k, v in diag.items()})
        d.update({f"set_{k}": v for k, v in sett.items()})
        return d


def _is_simple(g: Graph) -> tuple[bool, str]:
    e = g.edges
    if len(e) == 0:
        return True, ""
    if (e < 0).any() or (e >= g.n).any():
        return False, "node_index_out_of_range"
    if (e[:, 0] == e[:, 1]).any():
        return False, "self_loop"
    keys = g.edge_keys()
    if len(np.unique(keys)) != len(keys):
        return False, "duplicate_edge"
    if not g.directed and (e[:, 0] >= e[:, 1]).any():
        return False, "non_canonical_undirected_edge"
    return True, ""


def degree_assortativity(g: Graph) -> float:
    if g.m == 0 or g.directed:
        return float("nan")
    d = g.degrees().astype(float)
    x = np.concatenate([d[g.edges[:, 0]], d[g.edges[:, 1]]])
    y = np.concatenate([d[g.edges[:, 1]], d[g.edges[:, 0]]])
    if x.std() == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def mixing_matrix(g: Graph, strata: np.ndarray) -> np.ndarray:
    k = int(strata.max()) + 1
    M = np.zeros((k, k))
    a, b = strata[g.edges[:, 0]], strata[g.edges[:, 1]]
    np.add.at(M, (a, b), 1)
    if not g.directed:
        np.add.at(M, (b, a), 1)
    return M / max(M.sum(), 1)


def audit_sample(
    g0: Graph,
    gp: Graph,
    spec: NullSpec,
    node_attrs: dict,
    gen_info: dict,
    seed_key: tuple,
    policy: AdmissibilityPolicy = AdmissibilityPolicy(),
    report_attrs: tuple[str, ...] = ("block",),
) -> AdmissibilityResult:
    """Exact hard-constraint checks plus soft diagnostics for one placebo sample."""
    hard, soft = [], []
    ok, why = _is_simple(gp)
    if not ok:
        hard.append(f"simple:{why}")
    if gp.n != g0.n:
        hard.append("node_count")
    if gp.m != g0.m:
        hard.append("edge_count")
    if gp.directed != g0.directed:
        hard.append("directedness")
    cons = spec.hard_constraints()
    if "degree_sequence" in cons and not g0.directed:
        if not np.array_equal(gp.degrees(), g0.degrees()):
            hard.append("degree_sequence")
    if "in_out_degree_sequence" in cons:
        if not (np.array_equal(gp.in_degrees(), g0.in_degrees())
                and np.array_equal(gp.out_degrees(), g0.out_degrees())):
            hard.append("in_out_degree_sequence")
    if "neighbour_stratum_counts" in cons:
        s = stratum_codes(node_attrs, spec.attrs, g0.n)
        if not np.array_equal(neighbour_stratum_counts(gp, s), neighbour_stratum_counts(g0, s)):
            hard.append("neighbour_stratum_counts")
    if "stratum_preserving_isomorphism" in cons:
        # verified via invariants: sorted degree multiset per stratum and stratum mixing matrix
        s = stratum_codes(node_attrs, spec.attrs, g0.n)
        for st in np.unique(s):
            if not np.array_equal(np.sort(gp.degrees()[s == st]), np.sort(g0.degrees()[s == st])):
                hard.append("stratum_degree_multiset")
                break
        if not np.allclose(mixing_matrix(gp, s), mixing_matrix(g0, s)):
            hard.append("stratum_mixing_matrix")

    overlap = edge_overlap(g0, gp)
    diag = {
        "edge_overlap": overlap,
        "degree_assortativity_g0": degree_assortativity(g0),
        "degree_assortativity_null": degree_assortativity(gp),
    }
    for a in report_attrs:
        if a in node_attrs and not g0.directed:
            s = stratum_codes(node_attrs, (a,), g0.n)
            diag[f"mixing_l1_{a}"] = float(np.abs(mixing_matrix(gp, s) - mixing_matrix(g0, s)).sum())
    if "achieved_swaps" in gen_info:
        comp = gen_info["achieved_swaps"] / max(gen_info["target_swaps"], 1)
        diag["swap_completion"] = comp
        diag["swap_acceptance_rate"] = gen_info.get("acceptance_rate", np.nan)
        if comp < policy.min_swap_completion:
            soft.append("insufficient_mixing")
    if "fixed_point_fraction" in gen_info:
        diag["fixed_point_fraction"] = gen_info["fixed_point_fraction"]
    if overlap > policy.max_edge_overlap:
        soft.append("near_identical")
    return AdmissibilityResult(
        valid=not hard and not soft,
        generator=spec.name,
        seed_key=tuple(seed_key),
        violated_hard=hard,
        violated_soft=soft,
        diagnostics=diag,
        settings={"family": spec.family, "attrs": "+".join(spec.attrs),
                  "swap_factor": spec.swap_factor, "chain": spec.chain},
    )


def effective_diversity(samples: list[Graph]) -> dict:
    """Mean pairwise edge overlap among placebo draws and 1 - that (diversity)."""
    if len(samples) < 2:
        return {"mean_pairwise_overlap": float("nan"), "diversity": float("nan")}
    ov = [edge_overlap(samples[i], samples[j]) for i in range(len(samples)) for j in range(i + 1, len(samples))]
    mo = float(np.mean(ov))
    return {"mean_pairwise_overlap": mo, "diversity": 1.0 - mo}


def candidate_admissible(results: list[AdmissibilityResult], policy: AdmissibilityPolicy = AdmissibilityPolicy()) -> dict:
    """Candidate-level verdict from its sample audits (label-free; frozen before confirmation)."""
    n = len(results)
    acc = float(np.mean([r.valid for r in results])) if n else 0.0
    hard_any = any(r.violated_hard for r in results)
    return {
        "n_samples": n,
        "acceptance": acc,
        "any_hard_violation": hard_any,
        "admissible": (not hard_any) and acc >= policy.min_candidate_acceptance,
        "mean_overlap": float(np.mean([r.diagnostics["edge_overlap"] for r in results])) if n else np.nan,
    }
