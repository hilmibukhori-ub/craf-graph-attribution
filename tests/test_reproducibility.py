import hashlib

import numpy as np
import pandas as pd

from rusa.data.synthetic import generate_instance
from rusa.evaluation.methods import pool_arrays, run_experiment, truth
from rusa.evaluation.runner import load_pool, run_chunk
from rusa.models.gnn import TorchNodeModel
from rusa.nulls.search import PoolOracle, successive_halving, uniform_search
from rusa.utils.seeding import rng_for, seed_key

SPECS = ["er", "degree", "perm:block", "strat:block", "strat:w3"]


def _hash_df(df):
    cols = [c for c in df.columns if not c.endswith("seconds")]
    return hashlib.sha256(df[cols].to_csv(index=False).encode()).hexdigest()


def test_instance_generation_deterministic():
    a, b = generate_instance("S4", 3, 5), generate_instance("S4", 3, 5)
    assert np.array_equal(a.graph.edges, b.graph.edges) and np.array_equal(a.y, b.y)
    c = generate_instance("S4", 4, 5)
    assert not np.array_equal(a.y, c.y)


def test_seed_keys_stable_and_distinct():
    assert seed_key("S1", 3) == seed_key("S1", 3)
    x = rng_for(1, "S1", 0, "null").random(3)
    y = rng_for(1, "S1", 1, "null").random(3)
    assert not np.allclose(x, y)


def test_run_chunk_bitwise_reproducible_and_checkpointed(tmp_path):
    p1 = run_chunk("S3", 0, 3, tmp_path / "a", draws=1, specs=SPECS)
    p2 = run_chunk("S3", 0, 3, tmp_path / "b", draws=1, specs=SPECS)
    assert _hash_df(pd.read_csv(p1)) == _hash_df(pd.read_csv(p2))
    mtime = p1.stat().st_mtime
    assert run_chunk("S3", 0, 3, tmp_path / "a", draws=1, specs=SPECS) == p1
    assert p1.stat().st_mtime == mtime  # completed chunk is skipped
    df = load_pool(tmp_path / "a", "S3")
    assert set(df.variant) == {"real", "empty", *SPECS}


def test_torch_model_seed_reproducible():
    inst = generate_instance("S1_g100", 0, 5)
    m = TorchNodeModel("gcn", max_epochs=40, patience=10)
    F = inst.model_features()
    r1 = m.fit_score(F, inst.y, inst.graph, inst.split, seed=11)
    r2 = m.fit_score(F, inst.y, inst.graph, inst.split, seed=11)
    assert r1 == r2
    e = m.fit_score(F, inst.y, None, inst.split, seed=11)
    assert e["n_params"] == r1["n_params"]  # matched architecture for the empty graph


def test_search_budget_respected_and_deterministic():
    rng = np.random.default_rng(0)
    R, b = 10, 2
    real = rng.normal(0.8, 0.01, R)
    cand = {f"a{i}": real[:, None] - (0.01 * i + rng.normal(0, 0.005, (R, b))) for i in range(8)}
    for alg in (uniform_search, successive_halving):
        res = alg(PoolOracle(real, cand), list(cand), budget=50, top_m=2)
        assert res.fits_used <= 50
        res2 = alg(PoolOracle(real, cand), list(cand), budget=50, top_m=2)
        assert res.selected == res2.selected and res.log == res2.log
        assert "a0" in res.selected


def test_freeze_hash(tmp_path):
    real = np.array([0.8, 0.8])
    res = uniform_search(PoolOracle(real, {"x": np.full((2, 1), 0.7)}), ["x"], 10, 1)
    h1 = res.freeze(tmp_path / "f.json", {"note": "dev only"})
    h2 = res.freeze(tmp_path / "g.json", {"note": "dev only"})
    assert h1 == h2 and len(h1) == 64


def test_experiment_budget_and_ladder_telescoping(tmp_path):
    run_chunk("S2", 0, 30, tmp_path, draws=2, specs=SPECS)
    P = pool_arrays(load_pool(tmp_path, "S2"))
    rows = run_experiment(P, np.arange(30), truth(P), r_base=4, r_dev=6)
    for r in rows:
        assert r["fits"] <= r["budget"], r["procedure"]
    lad = [r for r in rows if r["procedure"] == "pcga_l"][0]
    assert lad["telescoping_err"] < 1e-12
