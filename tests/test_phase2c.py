import hashlib

import numpy as np
import pandas as pd
import pytest

from rusa.data.synthetic import PHASE2C_BINDING, SCENARIOS, generate_instance, relational_term
from rusa.evaluation.methods import pool_arrays, truth
from rusa.evaluation.phase2c import (FULLSET_VARIANTS, audit_combination, audit_marginal_t, fullset_feasible,
                                     run_experiment_2c, stage1_size, variant_seconds)
from rusa.evaluation.runner import evaluate_instance
from rusa.inference.allocation import optimal_allocation
from rusa.models.baselines import SGCRidge
from rusa.nulls.generators import NullSpec
from rusa.utils.seeding import rng_for


# ------------------------------------------------------------------ regression: 2A and 2B worlds unchanged
@pytest.mark.parametrize("sc,h", [("S6_small_hard", "3c70eff369b55671"), ("N6_hard", "5fd33d1d44d8e14b"),
                                  ("S6_large_easy", "9143995393be0f34"), ("N6_easy", "b397e41654463913")])
def test_phase2b_instances_unchanged(sc, h):
    """Hashes computed with the archived frozen Phase 2B code (archive/phase2b_code_2026-11-24.tar.gz)."""
    i = generate_instance(sc, 3, 20261201)
    got = hashlib.sha256(i.graph.edges.tobytes() + i.y.tobytes() + i.x.tobytes() + i.split["test"].tobytes()
                         + i.model_features().tobytes()).hexdigest()
    assert got[:16] == h


# ------------------------------------------------------------------ S7 / S8 DGP
def test_s7_s8_structure():
    i = generate_instance("S8_small_hard", 0, 5)
    a = i.node_attrs
    assert np.array_equal(a["u"], a["w1"] ^ a["w2"])
    assert 0.03 < (a["w3"] != a["u"]).mean() < 0.2 and 0.03 < (a["w5"] != a["u"]).mean() < 0.2
    e = generate_instance("S8_small_easy", 0, 5)
    assert 0.35 < (e.node_attrs["w3"] != e.node_attrs["u"]).mean() < 0.65
    # u is a model feature (last column), not stratification metadata
    assert i.model_features().shape[1] == generate_instance("S6_small_hard", 0, 5).model_features().shape[1] + 1
    assert np.array_equal(i.model_features()[:, -1], a["u"])
    assert SCENARIOS["S7_hard"]["aa"] == PHASE2C_BINDING and SCENARIOS["S7_hard"]["gamma_e"] == 0.0
    assert SCENARIOS["S8_large_hard"]["gamma_e"] > SCENARIOS["S8_small_hard"]["gamma_e"] > 0
    # graph assortative in u
    ed = i.graph.edges
    assert (a["u"][ed[:, 0]] == a["u"][ed[:, 1]]).mean() > 0.65


def test_binding_null_is_isolated():
    """strat:w1+w2 reproduces the u-composition term exactly; single-attribute and decoy strata do not."""
    i = generate_instance("S8_large_hard", 1, 7)
    R0 = relational_term("u_comp", i.graph, i.node_attrs, i.x)
    err = {}
    for name in (PHASE2C_BINDING, "strat:w1", "strat:w2", "strat:w3", "strat:w3+w5", "strat:block", "degree"):
        g, _ = NullSpec.parse(name).sample(i.graph, i.node_attrs, rng_for(7, "iso", name))
        err[name] = float(np.abs(relational_term("u_comp", g, i.node_attrs, i.x) - R0).mean())
    assert err[PHASE2C_BINDING] < 1e-12
    for k in ("strat:w1", "strat:w2", "strat:block", "degree"):
        assert err[k] > 0.3, (k, err[k])
    assert 1e-3 < err["strat:w3+w5"] < err["strat:w3"] < err["strat:w1"]  # decoys: partial preservation


def test_s7_exact_aa_hub():
    i = generate_instance("S7_hard", 2, 11)
    assert i.hub is not None
    # G0 and a placebo from the hub share the hub's joint (w1,w2) neighbour counts -> same R
    g, _ = NullSpec.parse(PHASE2C_BINDING).sample(i.hub, i.node_attrs, rng_for(1, "p"))
    assert np.allclose(relational_term("u_comp", g, i.node_attrs, i.x),
                       relational_term("u_comp", i.graph, i.node_attrs, i.x))


# ------------------------------------------------------------------ feasibility rule
@pytest.mark.parametrize("K", [18, 48])
@pytest.mark.parametrize("b", [4, 6, 9, 12, 24])
@pytest.mark.parametrize("n_min", [3, 5])
def test_apriori_feasibility_implies_allocation(K, b, n_min):
    R1 = stage1_size(b, K, 20, 1 / 3)
    B = b * (2 + K)
    feas = fullset_feasible(K, B, R1, n_min)
    rng = np.random.default_rng(K * b)
    dh = {f"c{j}": float(rng.uniform(-0.01, 0.05)) for j in range(K + 1)}
    alloc = optimal_allocation(dh, 0.015, 0.005, B - R1 * (2 + K), n_min=n_min, n_max=100)
    assert (alloc is not None) == feas
    if alloc is not None:  # any subset after elimination is also feasible
        sub = dict(list(dh.items())[: max(1, K // 2)])
        assert optimal_allocation(sub, 0.015, 0.005, B - R1 * (2 + K), n_min=n_min, n_max=100) is not None


def test_small_budget_variant_is_feasible_where_n5_is_not():
    assert not fullset_feasible(18, 6 * 20, stage1_size(6, 18, 20, 1 / 3), 5)
    assert fullset_feasible(18, 6 * 20, stage1_size(6, 18, 20, 1 / 3), 3)
    assert FULLSET_VARIANTS["fullset_adaptive_s"] == (3, True)


# ------------------------------------------------------------------ engine
@pytest.fixture(scope="module")
def s7_pool():
    specs = [NullSpec.parse(s) for s in ("er", "degree", "perm:block", "strat:block", "strat:w1", "strat:w2",
                                         "strat:w3", PHASE2C_BINDING, "strat:block+w3")]
    rows = []
    for i in range(40):
        rows += evaluate_instance(generate_instance("S7_hard", i, 13), specs, SGCRidge(), 2, 13)
    return pd.DataFrame(rows)


def test_run_experiment_2c(s7_pool):
    P = pool_arrays(s7_pool)
    tr = truth(P)
    tr.loc[PHASE2C_BINDING, "delta"] = 0.0
    from rusa.evaluation.phase2c import arms_for
    arms = arms_for(P, ["block", "w1", "w2", "w3"])
    assert PHASE2C_BINDING in arms
    sec = variant_seconds(s7_pool)
    for b in (2, 6):
        rows = run_experiment_2c(P, np.arange(40), tr, arms, b, sec=sec, binding_arm=PHASE2C_BINDING,
                                 r_dev=10, n_conf_max=30)
        by = {r["procedure"]: r for r in rows}
        assert set(by) == {"pcga_l", "exhaustive_iut", "screen_uniform", "screen_random", "screen_sh",
                           "oracle_select", "fullset_adaptive", "fullset_adaptive_fb", "fullset_adaptive_s"}
        for r in rows:
            assert r["fits"] <= r["budget"], (b, r["procedure"])
            assert r["binding_arm"] == PHASE2C_BINDING and r["theta_full"] <= 0
        assert by["pcga_l"]["scope"] == "L3" and by["screen_uniform"]["scope"] == "selected"
        if not by["fullset_adaptive_fb"]["feasible"]:  # fallback reproduces exhaustive_iut exactly
            assert by["fullset_adaptive_fb"]["fallback"]
            for k in ("claim", "L", "fits", "theta_hat"):
                assert by["fullset_adaptive_fb"][k] == by["exhaustive_iut"][k]
            assert by["fullset_adaptive"]["infeasible"]
        # screen discovery is defined by the known binding arm
        assert by["screen_uniform"]["discovered"] == (PHASE2C_BINDING in by["screen_uniform"]["selected"].split("|"))


# ------------------------------------------------------------------ combination audit helpers
def test_audit_marginal_t_normal_is_calibrated():
    d = np.random.default_rng(0).normal(0, 1, 60000)
    a = audit_marginal_t(d, ns=(3, 8), alphas=(0.05,))
    assert np.all(np.abs(a["size"] - 0.05) < 0.012)


def test_audit_combination_controls_level_under_adaptive_n2():
    d = np.random.default_rng(1).normal(0, 1, 50000)
    a = audit_combination(d, R1s=(2, 4), n_boot=6000, seed=3)
    assert np.all(a["total_type1"] <= a["nominal"] + 0.012)
    assert set(a["rule"]) == {"fixed5", "fixed20", "promising_more", "promising_less"}
