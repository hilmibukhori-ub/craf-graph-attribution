import itertools

import numpy as np
import pytest

from rusa.data.synthetic import generate_instance
from rusa.nulls import generators as G
from rusa.nulls.generators import Graph, NullSpec, neighbour_stratum_counts, stratum_codes
from rusa.utils.seeding import rng_for


@pytest.fixture(scope="module")
def inst():
    return generate_instance("S4", 0, master_seed=7)


def _simple(g: Graph):
    e = g.edges
    assert (e[:, 0] < e[:, 1]).all()
    assert len(np.unique(g.edge_keys())) == g.m


def test_er_exact_counts_and_simple(inst):
    gp, _ = G.erdos_renyi_gnm(inst.graph, rng_for(1))
    assert gp.n == inst.graph.n and gp.m == inst.graph.m
    _simple(gp)


def test_er_index_mapping_is_bijective():
    n = 9
    total = n * (n - 1) // 2
    g = Graph.from_edges(n, [(0, 1)])
    # sample every index once by setting m = total
    full = Graph.from_edges(n, list(itertools.combinations(range(n), 2)))
    gp, _ = G.erdos_renyi_gnm(full, rng_for(2))
    assert gp.m == total
    assert set(map(tuple, gp.edges)) == set(itertools.combinations(range(n), 2))


def test_degree_swap_preserves_degrees(inst):
    gp, info = NullSpec("degree").sample(inst.graph, inst.node_attrs, rng_for(3))
    assert np.array_equal(gp.degrees(), inst.graph.degrees())
    assert info["achieved_swaps"] == info["target_swaps"]
    _simple(gp)
    assert G.edge_overlap(inst.graph, gp) < 0.5


@pytest.mark.parametrize("attrs", [("block",), ("w3",), ("block", "w3"), ("w1", "w2")])
def test_stratified_swap_preserves_neighbour_strata(inst, attrs):
    spec = NullSpec("strat", attrs)
    gp, info = spec.sample(inst.graph, inst.node_attrs, rng_for(4, *attrs))
    s = stratum_codes(inst.node_attrs, attrs, inst.graph.n)
    assert np.array_equal(neighbour_stratum_counts(gp, s), neighbour_stratum_counts(inst.graph, s))
    assert np.array_equal(gp.degrees(), inst.graph.degrees())
    _simple(gp)


def test_besag_clifford_mode_preserves_constraints(inst):
    spec = NullSpec("strat", ("block",), chain="besag_clifford")
    gp, info = spec.sample(inst.graph, inst.node_attrs, rng_for(5))
    s = stratum_codes(inst.node_attrs, ("block",), inst.graph.n)
    assert "hub_swaps" in info
    assert np.array_equal(neighbour_stratum_counts(gp, s), neighbour_stratum_counts(inst.graph, s))


def test_within_block_permutation_invariants(inst):
    gp, info = NullSpec("perm", ("block",)).sample(inst.graph, inst.node_attrs, rng_for(6))
    b = inst.node_attrs["block"]
    for k in np.unique(b):
        assert np.array_equal(np.sort(gp.degrees()[b == k]), np.sort(inst.graph.degrees()[b == k]))
    assert gp.m == inst.graph.m
    _simple(gp)


def test_directed_swap_preserves_in_out_degree():
    rng = np.random.default_rng(0)
    n = 60
    E = {(int(a), int(b)) for a, b in rng.integers(0, n, size=(400, 2)) if a != b}
    g = Graph.from_edges(n, sorted(E), directed=True)
    gp, info = G.directed_degree_null(g, rng_for(7))
    assert np.array_equal(gp.in_degrees(), g.in_degrees())
    assert np.array_equal(gp.out_degrees(), g.out_degrees())
    assert not (gp.edges[:, 0] == gp.edges[:, 1]).any()
    assert len(np.unique(gp.edge_keys())) == gp.m


@pytest.mark.skipif(not G.HAVE_NUMBA, reason="numba not installed")
def test_numba_and_python_kernels_identical(inst):
    spec = NullSpec("strat", ("block", "w3"))
    try:
        G.set_numba(True)
        a, ia = spec.sample(inst.graph, inst.node_attrs, rng_for(8))
        G.set_numba(False)
        b, ib = spec.sample(inst.graph, inst.node_attrs, rng_for(8))
    finally:
        G.set_numba(True)
    assert np.array_equal(a.edges, b.edges)
    assert ia == ib


def test_generator_is_deterministic_given_seed(inst):
    spec = NullSpec("degree")
    a, _ = spec.sample(inst.graph, inst.node_attrs, rng_for(9))
    b, _ = spec.sample(inst.graph, inst.node_attrs, rng_for(9))
    c, _ = spec.sample(inst.graph, inst.node_attrs, rng_for(10))
    assert np.array_equal(a.edges, b.edges)
    assert not np.array_equal(a.edges, c.edges)


def test_candidate_set_is_fixed_and_documented():
    names = [s.name for s in G.candidate_specs(["block", "w1", "w2", "w3", "w4"])]
    assert names[:4] == ["er", "degree", "perm:block", "strat:block"]
    assert len(names) == 18 and len(set(names)) == 18
