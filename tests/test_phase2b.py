import hashlib

import numpy as np
import pandas as pd
import pytest

from rusa.data.synthetic import SCENARIOS, generate_instance
from rusa.evaluation.methods import pool_arrays, truth
from rusa.evaluation.phase2b import arms_for, run_experiment_2b, variant_seconds
from rusa.evaluation.runner import evaluate_instance
from rusa.inference.allocation import allocation_cost, fullset_two_stage, optimal_allocation
from rusa.models.baselines import SGCRidge
from rusa.nulls.generators import NullSpec
from rusa.nulls.search import PoolOracle, random_search


# ------------------------------------------------------------------ Phase 2A regression
@pytest.mark.parametrize("sc,h", [("S5", "12e993c39837180f"), ("AA_degree", "9afdebb9b692c3da"),
                                  ("S1_g100", "9e79bbe17cceb122")])
def test_phase2a_instances_unchanged(sc, h):
    i = generate_instance(sc, 3, 20261123)
    got = hashlib.sha256(i.graph.edges.tobytes() + i.y.tobytes() + i.x.tobytes() + i.split["test"].tobytes()).hexdigest()
    assert got[:16] == h


# ------------------------------------------------------------------ DGP
def test_phase2b_decoys_and_exact_aa():
    i = generate_instance("S6_small_hard", 0, 5)
    assert {f"w{k}" for k in range(1, 9)} <= set(i.node_attrs)
    flip = (i.node_attrs["w4"] != i.node_attrs["w3"]).mean()
    assert 0.03 < flip < 0.2  # q = 0.10
    e = generate_instance("S6_small_easy", 0, 5)
    assert 0.35 < (e.node_attrs["w4"] != e.node_attrs["w3"]).mean() < 0.65
    n = generate_instance("N6_hard", 0, 5)
    assert n.hub is not None and SCENARIOS["N6_hard"]["aa"] == "strat:w3"
    assert SCENARIOS["N6_hard"]["gamma_e"] == 0.0 and SCENARIOS["S6_large_hard"]["gamma_e"] > 0


# ------------------------------------------------------------------ allocation
def test_allocation_properties():
    dh = {"hard": 0.006, "mid": 0.02, "easy": 0.05, "empty": 0.03}
    a = optimal_allocation(dh, 0.015, 0.005, budget=200, n_min=5, n_max=100)
    assert allocation_cost(a) <= 200
    assert a["hard"] >= a["mid"] >= a["easy"] >= 5
    assert optimal_allocation(dh, 0.015, 0.005, budget=10, n_min=5) is None
    big = optimal_allocation(dh, 0.015, 0.005, budget=10_000, n_min=5, n_max=50)
    assert allocation_cost(big) <= 10_000 and big["hard"] == 50


def _sim(rng, delta, n, sd=1.0):
    return rng.normal(delta, sd, n)


@pytest.mark.parametrize("alpha1", [0.0, 0.01])
def test_fullset_valid_under_adversarial_allocation(alpha1):
    """Hidden binding comparator at the boundary; dev estimates are made MISLEADING on purpose
    (the binding arm looks easy) -- the full-set certificate must still keep level alpha."""
    rng = np.random.default_rng(0)
    true = {"bind": 0.0, **{f"d{i}": 0.6 for i in range(8)}, "empty": 1.0}
    rej, reps = 0, 3000
    for _ in range(reps):
        D_dev = {k: _sim(rng, v, 4) for k, v in true.items()}
        dh = {k: float(np.mean(v)) for k, v in D_dev.items()}
        dh["bind"] = 2.0  # adversarial: binding arm looks easiest
        st_elim = set()
        if alpha1 > 0:
            st = fullset_two_stage(D_dev, {}, alpha1, 0.05 - alpha1)
            st_elim = {k for k, v in st["stage"].items() if v == "dev"}
        rest = [k for k in true if k not in st_elim]
        a = optimal_allocation({k: dh[k] for k in rest}, 1.0, 0.0, budget=150, n_min=3, n_max=60, d_floor=0.05)
        if a is None:
            continue
        D_conf = {k: _sim(rng, true[k], a[k]) for k in rest}
        out = fullset_two_stage(D_dev if alpha1 > 0 else {k: np.array([]) for k in true}, D_conf, alpha1, 0.05 - alpha1)
        rej += out["certified"]
    assert rej / reps <= 0.05 + 3 * np.sqrt(0.05 * 0.95 / reps)


def test_selected_set_screening_is_not_fullset_valid():
    """Counterexample (documents Prop. 6): screening that drops the binding arm certifies falsely."""
    rng = np.random.default_rng(1)
    rej, reps = 0, 1000
    for _ in range(reps):
        dev = {"bind": _sim(rng, 0.0, 2), "decoy": _sim(rng, 0.25, 2), "e": _sim(rng, 1.0, 2)}
        sel = min(["bind", "decoy"], key=lambda k: dev[k].mean())
        conf = {"e": _sim(rng, 1.0, 40), sel: _sim(rng, 0.0 if sel == "bind" else 0.25, 40)}
        out = fullset_two_stage(None, conf, 0.0, 0.05)
        rej += out["certified"]
    assert rej / reps > 0.10  # far above alpha w.r.t. the full set


# ------------------------------------------------------------------ random search
def test_random_search_budget_and_determinism():
    rng = np.random.default_rng(0)
    real = rng.normal(0.8, 0.01, 10)
    cand = {f"a{i}": real[:, None] - (0.01 * i + rng.normal(0, 0.003, (10, 2))) for i in range(12)}
    r1 = random_search(PoolOracle(real, cand), list(cand), 16, 2, rng=np.random.default_rng(3))
    r2 = random_search(PoolOracle(real, cand), list(cand), 16, 2, rng=np.random.default_rng(3))
    assert r1.fits_used <= 16 and r1.selected == r2.selected
    assert len({e["arm"] for e in r1.log}) < 12  # budget does not reach every arm


# ------------------------------------------------------------------ procedure engine
@pytest.fixture(scope="module")
def tiny_pool():
    specs = [NullSpec.parse(s) for s in ("er", "degree", "perm:block", "strat:block", "strat:w3", "strat:w4",
                                         "strat:w4+w5", "strat:block+w3")]
    rows = []
    for i in range(36):
        rows += evaluate_instance(generate_instance("N6_hard", i, 9), specs, SGCRidge(), 2, 9)
    return pd.DataFrame(rows)


def test_run_experiment_2b_budgets_scopes(tiny_pool):
    P = pool_arrays(tiny_pool)
    tr = truth(P)
    tr.loc["strat:w3", "delta"] = 0.0
    arms = arms_for(P, ["block", "w3", "w4", "w5"])
    assert "strat:w4+w5" in arms
    rows = run_experiment_2b(P, np.arange(36), tr, arms, b=4, sec=variant_seconds(tiny_pool), r_dev=8, n_conf_max=28)
    by = {r["procedure"]: r for r in rows}
    assert set(by) == {"pcga_l", "exhaustive_iut", "screen_random", "screen_uniform", "screen_sh", "oracle_select",
                       "fullset_alloc", "fullset_elim", "fullset_adaptive"}
    for r in rows:
        assert r["fits"] <= r["budget"], r["procedure"]
    assert by["exhaustive_iut"]["scope"] == "full" and by["fullset_adaptive"]["scope"] == "full"
    assert by["screen_sh"]["scope"] == "selected"
    assert by["oracle_select"]["discovered"]
    assert rows[0]["theta_full"] <= 0.0


def test_fullset_elim_all_eliminated_certifies_from_stage1():
    rng = np.random.default_rng(2)
    D_dev = {k: rng.normal(1.0, 0.01, 6) for k in ("a", "b", "empty")}
    out = fullset_two_stage(D_dev, {}, 0.01, 0.04, 0.0)
    assert out["n_eliminated"] == 3 and out["certified"]


def test_adaptive_combination_valid_with_data_dependent_stage2_size():
    """Prop. 6: stage-2 size chosen from stage 1 (adversarially) must not break level alpha."""
    from rusa.inference.allocation import fullset_adaptive
    rng = np.random.default_rng(3)
    rej, reps = 0, 3000
    for _ in range(reps):
        D1 = {"bind": rng.normal(0, 1, 4), "e": rng.normal(2.0, 1, 4)}
        # adversarial sizing: bigger stage 2 when stage 1 looked favourable for the binding arm
        n2 = 40 if D1["bind"].mean() > 0 else 3
        D2 = {"bind": rng.normal(0, 1, n2), "e": rng.normal(2.0, 1, 20)}
        rej += fullset_adaptive(D1, D2, np.sqrt(1 / 3), 0.01, 0.04, 0.0)["certified"]
    assert rej / reps <= 0.05 + 3 * np.sqrt(0.05 * 0.95 / reps)


def test_combination_bound_consistent_with_p():
    from rusa.inference.allocation import combination_test
    rng = np.random.default_rng(4)
    for _ in range(20):
        d1, d2 = rng.normal(0.3, 1, 6), rng.normal(0.3, 1, 30)
        r = combination_test(d1, d2, np.sqrt(1 / 3), 0.05, 0.0)
        assert (r["L"] > 0) == (r["p"] <= 0.05 + 1e-9)
