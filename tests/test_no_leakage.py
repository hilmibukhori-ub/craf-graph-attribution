"""No-leakage checks: generators are label-free, tuning/selection never read test labels,
and the null search only consumes validation scores of development instances."""

import inspect

import numpy as np
import pandas as pd

from rusa.data import synthetic as S
from rusa.evaluation.methods import pool_arrays, run_experiment, truth
from rusa.evaluation.runner import evaluate_instance
from rusa.models.baselines import SGCRidge
from rusa.nulls.generators import NullSpec
from rusa.nulls.search import PoolOracle, successive_halving
from rusa.utils.seeding import rng_for


def test_generator_signatures_have_no_label_access():
    params = set(inspect.signature(NullSpec.sample).parameters)
    assert params == {"self", "g", "node_attrs", "rng", "hub"}
    inst = S.generate_instance("S1_g100", 0, 3)
    assert "y" not in inst.node_attrs and "label" not in inst.node_attrs


def test_placebos_identical_when_labels_change():
    inst = S.generate_instance("S5", 2, 3)
    spec = NullSpec("strat", ("w3",))
    a, _ = spec.sample(inst.graph, inst.node_attrs, rng_for(1))
    inst.y = 1 - inst.y  # flip every label
    b, _ = spec.sample(inst.graph, inst.node_attrs, rng_for(1))
    assert np.array_equal(a.edges, b.edges)


def test_dgp_graph_features_split_do_not_depend_on_label_mechanism():
    old = dict(S.SCENARIOS["S3"])
    a = S.generate_instance("S3", 4, 3)
    try:
        S.SCENARIOS["S3"]["gamma"] = 0.0
        b = S.generate_instance("S3", 4, 3)
    finally:
        S.SCENARIOS["S3"].clear()
        S.SCENARIOS["S3"].update(old)
    assert np.array_equal(a.graph.edges, b.graph.edges)
    assert np.array_equal(a.x, b.x)
    for k in ("train", "val", "test"):
        assert np.array_equal(a.split[k], b.split[k])
    assert not np.array_equal(a.y, b.y)


def test_split_is_a_partition():
    inst = S.generate_instance("S0", 1, 3)
    allidx = np.concatenate([inst.split[k] for k in ("train", "val", "test")])
    assert len(allidx) == inst.graph.n and len(np.unique(allidx)) == inst.graph.n


def test_model_selection_ignores_test_labels():
    inst = S.generate_instance("S1_g100", 5, 3)
    F = inst.model_features()
    m = SGCRidge()
    r1 = m.fit_score(F, inst.y, inst.graph, inst.split)
    y2 = inst.y.copy()
    y2[inst.split["test"]] = 1 - y2[inst.split["test"]]
    r2 = m.fit_score(F, y2, inst.graph, inst.split)
    assert r1["alpha"] == r2["alpha"] and r1["val_score"] == r2["val_score"]
    assert r1["test_score"] != r2["test_score"]


def _tiny_pool(n=24):
    specs = [NullSpec.parse(s) for s in ("er", "degree", "perm:block", "strat:block", "strat:w3")]
    rows = []
    for i in range(n):
        rows += evaluate_instance(S.generate_instance("S5", i, 3), specs, SGCRidge(), 2, 3)
    return pd.DataFrame(rows)


def test_search_and_freeze_are_invariant_to_test_scores():
    df = _tiny_pool()
    P = pool_arrays(df)
    tr = truth(P)
    rows_a = run_experiment(P, np.arange(24), tr, r_base=4, r_dev=8)
    # scramble every test score: selection must not change
    df2 = df.copy()
    df2["test_score"] = np.random.default_rng(0).permutation(df2["test_score"].to_numpy())
    P2 = pool_arrays(df2)
    rows_b = run_experiment(P2, np.arange(24), truth(P2), r_base=4, r_dev=8)
    sel_a = {r["procedure"]: r.get("selected") for r in rows_a if r["procedure"].startswith("rusa")}
    sel_b = {r["procedure"]: r.get("selected") for r in rows_b if r["procedure"].startswith("rusa")}
    assert sel_a == sel_b


def test_pool_oracle_reads_validation_only():
    real_val = np.array([0.8, 0.7])
    cand = {"a": np.array([[0.6, 0.65], [0.5, 0.55]]), "b": np.array([[0.79, 0.8], [0.7, 0.69]])}
    o = PoolOracle(real_val, cand)
    res = successive_halving(o, ["a", "b"], budget=20, top_m=1)
    assert res.selected == ["b"]
