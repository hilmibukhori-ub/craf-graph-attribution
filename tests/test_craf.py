import numpy as np
import pytest

from rusa.craf.core import (ADV, SUF, Lattice, certify, combined_directional_p, directional_p, element_name,
                            frontier_sets, holm, true_frontier)
from rusa.craf.experiment import _children_cert_min, adaptive_pvalues, run_block, semisynthetic_grid
from rusa.data.synthetic import generate_instance, relational_term
from rusa.nulls.generators import NullSpec, candidate_specs
from rusa.utils.seeding import rng_for

K18 = [s.name for s in candidate_specs(["block", "w1", "w2", "w3", "w4"], 2)]


def lat(names):
    return Lattice.from_names(names)


def test_lattice_from_k18():
    L = Lattice.from_names(K18 + ["er", "perm:block", "empty"])
    assert len(L) == 16  # {} + 5 singles + 10 pairs
    assert set(L.proper_subsets("strat:w1+w2")) == {"degree", "strat:w1", "strat:w2"}
    assert L.proper_subsets("degree") == []
    assert element_name(frozenset({"w2", "w1"})) == "strat:w1+w2"


def test_holm():
    assert holm({"a": 0.01, "b": 0.02, "c": 0.5}, 0.05) == {"a", "b"}
    assert holm({"a": 0.02, "b": 0.02}, 0.03) == set()


def test_directional_and_combined_mirror():
    rng = np.random.default_rng(0)
    d1, d2 = rng.normal(0.01, 0.01, 5), rng.normal(0.01, 0.01, 9)
    p = directional_p(d1, 0.005)
    assert abs(p[ADV] + p[SUF] - 1) < 1e-12
    c = combined_directional_p(d1, d2, 0.005, np.sqrt(1 / 3))
    assert abs(c[ADV] + c[SUF] - 1) < 1e-9


# ------------------------------------------------------------------ frontier logic
NAMES3 = ["degree", "strat:a", "strat:b", "strat:c", "strat:a+b", "strat:a+c", "strat:b+c"]


def test_frontier_interaction_and_multiple():
    L = lat(NAMES3)
    d = {"degree": .02, "strat:a": .02, "strat:b": .02, "strat:c": 0.0, "strat:a+b": 0.0, "strat:a+c": 0.0,
         "strat:b+c": 0.0}
    tf = true_frontier(L, d, 0.005)
    assert tf["F"] == {"strat:c", "strat:a+b"}  # interaction pair + a single property
    # with perfect certification, cert_min = F = possible_min
    fs = frontier_sets(L, tf["ins"], tf["suff"])
    assert fs["cert_min"] == tf["F"] == fs["possible_min"]


def test_minimal_among_certified_is_not_certified_minimal():
    L = lat(NAMES3)
    A = {"degree", "strat:a", "strat:c"}          # strat:b inconclusive
    C = {"strat:a+b"}
    fs = frontier_sets(L, A, C)
    assert "strat:a+b" in fs["min_among_cert"] and "strat:a+b" not in fs["cert_min"]
    assert fs["gaps"]["strat:a+b"] == ["strat:b"]
    assert "strat:b" in fs["possible_min"]        # the true frontier could be {b}


def test_non_monotone_children_rule_fails_full_rule_does_not():
    L = lat(NAMES3)
    d = {"degree": 0.0, "strat:a": .02, "strat:b": .02, "strat:c": .02, "strat:a+b": 0.0, "strat:a+c": .02,
         "strat:b+c": .02}
    tf = true_frontier(L, d, 0.005)
    assert tf["F"] == {"degree"}                  # non-monotone: {} sufficient, {a} not, {a,b} again sufficient
    A, C = tf["ins"], tf["suff"]
    assert _children_cert_min(L, A, C) == {"degree", "strat:a+b"}  # wrongly calls {a,b} minimal
    assert frontier_sets(L, A, C)["cert_min"] == {"degree"}


def test_order_independence_under_relabelling():
    rng = np.random.default_rng(3)
    L = lat(NAMES3)
    d = {n: rng.normal(0.004, 0.012, 40) for n in L.names}
    pv = {n: directional_p(v, 0.005) for n, v in d.items()}
    A, C = certify(pv, 0.05)
    fs = frontier_sets(L, A, C)
    perm = {"a": "c", "b": "a", "c": "b"}
    ren = lambda n: element_name(frozenset(perm[x] for x in L.sets[n]))  # noqa: E731
    L2 = lat([ren(n) for n in reversed(L.names)])
    pv2 = {ren(n): pv[n] for n in reversed(L.names)}
    A2, C2 = certify(pv2, 0.05)
    fs2 = frontier_sets(L2, A2, C2)
    for k in ("cert_min", "possible_min", "min_among_cert", "A", "C"):
        assert fs2[k] == {ren(n) for n in fs[k]}


# ------------------------------------------------------------------ validity by Monte Carlo
def test_fwer_at_worst_case_boundary():
    """All Delta = delta exactly: every certification is false; CRAF (both modes) must stay <= alpha."""
    d = {n: 0.005 for n in NAMES3}
    df = semisynthetic_grid("bound", d, None, [20, 40], n_exp=400, block_size=100, sd=0.012, df_t=5,
                            delta=0.005, alpha=0.05, seed=1)
    g = df.groupby("procedure")["class_error"].mean()
    assert g["craf"] <= 0.05 + 0.025 and g["craf_adaptive"] <= 0.05 + 0.025
    assert g["factorial_unadj"] > 0.2  # unadjusted factorial inflates


def test_adaptive_budget_and_fallback():
    rng = np.random.default_rng(5)
    L = lat(NAMES3)
    D = {n: rng.normal(0.01, 0.01, 100) for n in L.names}
    out = adaptive_pvalues(L, D, 30, 0.005, 0.05)
    assert out is not None and out[1] <= 30 * (1 + len(L))
    assert adaptive_pvalues(L, D, 6, 0.005, 0.05) is None  # infeasible a priori -> caller falls back
    rows = run_block(L, D, {n: 0.01 for n in L.names}, 6)
    ad = [r for r in rows if r["procedure"] == "craf_adaptive"][0]
    assert ad["fallback"] and ad["fits"] == 6 * (1 + len(L))


# ------------------------------------------------------------------ P3_multi world
def test_p3_multi_two_minimal_routes():
    i = generate_instance("P3_multi", 0, 9)
    a = i.node_attrs
    assert np.array_equal(a["w3"], a["u"]) and i.hub is not None
    R0 = relational_term("u_comp", i.graph, a, i.x)
    for name, exact in (("strat:w3", True), ("strat:w1+w2", True), ("strat:w1", False), ("degree", False)):
        g, _ = NullSpec.parse(name).sample(i.graph, a, rng_for(9, name))
        err = np.abs(relational_term("u_comp", g, a, i.x) - R0).mean()
        assert (err < 1e-12) == exact, name
