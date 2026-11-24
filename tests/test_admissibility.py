import numpy as np

from rusa.data.synthetic import generate_instance
from rusa.nulls.admissibility import (AdmissibilityPolicy, audit_sample, candidate_admissible,
                                      effective_diversity)
from rusa.nulls.generators import Graph, NullSpec
from rusa.utils.seeding import rng_for

INST = generate_instance("S3", 1, master_seed=11)


def _audit(gp, spec, info=None):
    return audit_sample(INST.graph, gp, spec, INST.node_attrs, info or {}, (0,))


def test_valid_sample_passes():
    spec = NullSpec("strat", ("block",))
    gp, info = spec.sample(INST.graph, INST.node_attrs, rng_for(1))
    r = _audit(gp, spec, info)
    assert r.valid and not r.violated_hard and not r.violated_soft
    assert 0 <= r.diagnostics["edge_overlap"] < 0.8


def test_self_loop_and_duplicates_rejected():
    e = INST.graph.edges.copy()
    e[0] = (5, 5)
    bad = Graph(INST.graph.n, e)  # bypass canonicalisation on purpose
    r = _audit(bad, NullSpec("er"))
    assert not r.valid and any(v.startswith("simple") for v in r.violated_hard)
    e = INST.graph.edges.copy()
    e[1] = e[0]
    r = _audit(Graph(INST.graph.n, e), NullSpec("er"))
    assert not r.valid and any("duplicate" in v for v in r.violated_hard)


def test_edge_count_and_degree_violations_detected():
    gp, info = NullSpec("er").sample(INST.graph, INST.node_attrs, rng_for(2))
    r = _audit(gp, NullSpec("degree"))  # ER graph claimed as degree-preserving
    assert "degree_sequence" in r.violated_hard
    fewer = Graph(INST.graph.n, INST.graph.edges[:-3])
    r = _audit(fewer, NullSpec("er"))
    assert "edge_count" in r.violated_hard


def test_stratum_violation_detected():
    gp, info = NullSpec("degree").sample(INST.graph, INST.node_attrs, rng_for(3))
    r = _audit(gp, NullSpec("strat", ("block",)))
    assert "neighbour_stratum_counts" in r.violated_hard


def test_near_identical_and_insufficient_mixing_rejected():
    spec = NullSpec("degree", swap_factor=0.02)
    gp, info = spec.sample(INST.graph, INST.node_attrs, rng_for(4))
    r = _audit(gp, spec, info)
    assert "near_identical" in r.violated_soft and not r.valid
    info2 = dict(info, achieved_swaps=1, target_swaps=100)
    r2 = _audit(gp, spec, info2)
    assert "insufficient_mixing" in r2.violated_soft


def test_candidate_level_verdict_and_diversity():
    spec = NullSpec("degree")
    samples, res = [], []
    for b in range(4):
        gp, info = spec.sample(INST.graph, INST.node_attrs, rng_for(5, b))
        samples.append(gp)
        res.append(_audit(gp, spec, info))
    v = candidate_admissible(res)
    assert v["admissible"] and v["acceptance"] == 1.0
    d = effective_diversity(samples)
    assert 0.5 < d["diversity"] <= 1.0
    bad = [_audit(Graph(INST.graph.n, INST.graph.edges[:-1]), spec)] * 4
    assert not candidate_admissible(bad)["admissible"]


def test_audit_row_serialisable():
    spec = NullSpec("perm", ("block",))
    gp, info = spec.sample(INST.graph, INST.node_attrs, rng_for(6))
    row = _audit(gp, spec, info).to_row()
    assert row["generator"] == "perm:block" and "diag_edge_overlap" in row
