"""Phase 3B (real-world CRAF pilot): data handling, label-freeness of attributes and nulls, models,
analysis helpers. Uses small synthetic stand-ins; the real datasets are not needed."""

import inspect

import numpy as np
import pandas as pd
import scipy.sparse as sp

from rusa.craf.core import Lattice
from rusa.evaluation.methods import pool_arrays
from rusa.nulls.generators import Graph, neighbour_stratum_counts, stratum_codes
from rusa.realworld import analysis as an
from rusa.realworld.attributes import compute_attributes, quantile_bins
from rusa.realworld.data import RealDataset, load_npz_dataset, make_split
from rusa.realworld.models import fit_score
from rusa.realworld.pool import audit_null, lattice_names, run_chunk_3b, sample_null


def _toy(n=90, k=3, seed=0):
    rng = np.random.default_rng(seed)
    y = np.repeat(np.arange(k), n // k)
    edges = set()
    while len(edges) < 3 * n:
        i, j = rng.integers(0, n, 2)
        if i != j and (y[i] == y[j] or rng.random() < 0.2):
            edges.add((min(i, j), max(i, j)))
    g = Graph.from_edges(n, np.array(sorted(edges)))
    Xr = sp.csr_matrix((rng.random((n, 20)) < 0.2).astype(float) + np.eye(n, 20))
    rs = np.asarray(Xr.sum(1)).ravel()
    X = (sp.diags(1 / rs) @ Xr).toarray().astype(np.float32)
    return RealDataset("toy", g, X, Xr, y.astype(np.int64), k)


def test_npz_loader_symmetrises_and_normalises(tmp_path):
    A = sp.csr_matrix(np.array([[1, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=np.float32))  # self-loop, directed
    F = sp.csr_matrix(np.array([[1, 1, 0], [0, 2, 0], [0, 0, 0]], dtype=np.float32))
    np.savez(tmp_path / "d.npz", adj_data=A.data, adj_indices=A.indices, adj_indptr=A.indptr, adj_shape=A.shape,
             attr_data=F.data, attr_indices=F.indices, attr_indptr=F.indptr, attr_shape=F.shape,
             labels=np.array([0, 1, 1]))
    d = load_npz_dataset(tmp_path / "d.npz")
    assert d.graph.m == 3 and set(map(tuple, d.graph.edges.tolist())) == {(0, 1), (1, 2), (0, 2)}
    assert np.allclose(d.X[0], [0.5, 0.5, 0]) and np.allclose(d.X[2], 0)
    assert d.n_classes == 2


def test_split_is_stratified_disjoint_and_complete():
    y = np.repeat(np.arange(4), 50)
    s = make_split(y, np.random.default_rng(1), n_train=5, n_val=7)
    allidx = np.concatenate([s["train"], s["val"], s["test"]])
    assert len(np.unique(allidx)) == len(y) == len(allidx)
    assert all((y[s["train"]] == c).sum() == 5 for c in range(4))
    assert all((y[s["val"]] == c).sum() == 7 for c in range(4))


def test_attributes_and_nulls_take_no_labels():
    for f in (compute_attributes, sample_null):
        params = set(inspect.signature(f).parameters)
        assert not params & {"y", "labels", "split", "score"}, f.__name__


def test_quantile_bins_keep_ties_together():
    b = quantile_bins(np.array([1, 1, 1, 1, 2, 3, 4, 5, 6, 7]))
    assert len(set(b[:4])) == 1


def test_attributes_deterministic_and_nulls_preserve_strata():
    d = _toy()
    a1 = compute_attributes(d.graph, d.X_raw, 7)
    a2 = compute_attributes(d.graph, d.X_raw, 7)
    assert all(np.array_equal(a1[k], a2[k]) for k in a1)
    for name in lattice_names(["deg", "block", "feat"], 2):
        gp, info = sample_null(name, d.graph, a1, np.random.default_rng(3), 5.0, 1000.0)
        assert np.array_equal(gp.degrees(), d.graph.degrees())
        if name != "degree":
            s = stratum_codes(a1, tuple(sorted(name[6:].split("+"))), d.n)
            assert np.array_equal(neighbour_stratum_counts(gp, s), neighbour_stratum_counts(d.graph, s))
        assert not audit_null(name, d.graph, gp, a1, info, (0,)).violated_hard


def test_pool_nulls_do_not_depend_on_labels(tmp_path):
    d = _toy()
    attrs = compute_attributes(d.graph, d.X_raw, 7)
    kw = dict(archs=["gcn"], elements=["degree", "strat:block"], draws=2, master_seed=5, swap_factor=2.0,
              attempt_factor=200.0, split_kw={"n_train": 5, "n_val": 5}, hp={"max_epochs": 3, "patience": 2})
    p1 = run_chunk_3b(d, attrs, 0, 2, tmp_path / "a", **kw)
    d2 = RealDataset("toy", d.graph, d.X, d.X_raw, np.random.default_rng(9).permutation(d.y), d.n_classes)
    p2 = run_chunk_3b(d2, attrs, 0, 2, tmp_path / "b", **kw)
    a, b = pd.read_csv(p1[0]), pd.read_csv(p2[0])
    nul = a.variant.isin(["degree", "strat:block", "er"])
    assert np.allclose(a.loc[nul, "diag_edge_overlap"].to_numpy(), b.loc[nul, "diag_edge_overlap"].to_numpy())
    assert set(a.variant) == {"real", "empty", "er", "degree", "strat:block"}
    P = pool_arrays(a)
    assert P.N == 2 and P.cand_test["degree"].shape == (2, 2)


def test_models_score_in_unit_interval_and_deterministic():
    d = _toy()
    s = make_split(d.y, np.random.default_rng(0), 5, 5)
    for arch in ("gcn", "sage", "mlp"):
        for g in (d.graph, None):
            r1 = fit_score(arch, d.X, d.y, g, s, 11, {"max_epochs": 20})
            r2 = fit_score(arch, d.X, d.y, g, s, 11, {"max_epochs": 20})
            assert 0 <= r1["test_score"] <= 1 and abs(r1["test_score"] - r2["test_score"]) < 1e-6


def _lat():
    return Lattice({"degree": frozenset(), "strat:a": frozenset("a"), "strat:b": frozenset("b"),
                    "strat:a+b": frozenset("ab")})


def test_certify_frontier_and_tables():
    L = _lat()
    rng = np.random.default_rng(0)
    D = {"degree": 0.05 + 0.01 * rng.standard_normal(400), "strat:a": 0.05 + 0.01 * rng.standard_normal(400),
         "strat:b": 0.05 + 0.01 * rng.standard_normal(400), "strat:a+b": 0.0 + 0.01 * rng.standard_normal(400)}
    res = an.certify_frontier(L, D, 0.005, 0.05)
    assert res["cert_min"] == {"strat:a+b"} and res["possible_min"] == {"strat:a+b"}
    t = an.element_table(L, D, 0.005, 0.05, res)
    assert (t.sim_lo <= t.delta_hat).all() and t.loc[t.element == "strat:a+b", "status"].item() == "sufficient"


def _pool_from(D_draws, real=None):
    """Build a PoolArrays-compatible frame: D_draws[name] = (N, 2) null test scores."""
    N = next(iter(D_draws.values())).shape[0]
    real = np.full(N, 0.8) if real is None else real
    rows = [{"scenario": "t", "instance": i, "variant": v, "draw": 0, "val_score": 0, "test_score": s, "valid": True}
            for i in range(N) for v, s in (("real", real[i]), ("empty", 0.5))]
    for k, M in D_draws.items():
        rows += [{"scenario": "t", "instance": i, "variant": k, "draw": j, "val_score": 0, "test_score": M[i, j],
                  "valid": True} for i in range(N) for j in range(2)]
    return pool_arrays(pd.DataFrame(rows))


def test_nonmonotonicity_and_interaction_detected():
    rng = np.random.default_rng(1)
    N = 300
    mu = {"degree": 0.80, "strat:a": 0.77, "strat:b": 0.79, "strat:a+b": 0.80}   # a hurts; a+b recovers
    P = _pool_from({k: m + 0.005 * rng.standard_normal((N, 2)) for k, m in mu.items()})
    nm = an.nonmonotonicity(P, _lat(), np.arange(N), 0.005, 0.05)
    hit = nm[nm.certified_nonmono]
    assert ("degree", "strat:a") in set(zip(hit["S"], hit["T"]))
    assert not nm[(nm["S"] == "strat:a") & (nm["T"] == "strat:a+b")].certified_nonmono.item()
    it = an.interactions(P, _lat(), np.arange(N), 0.05)
    assert it.significant.item() and it.interaction.item() < 0


def test_aa_calibration_is_null():
    rng = np.random.default_rng(2)
    N = 2000
    P = _pool_from({k: 0.7 + 0.01 * rng.standard_t(4, (N, 2)) for k in _lat().names})
    aa = an.aa_contrasts(P, np.arange(N), _lat().names)
    cm = an.calib_marginal(aa, ns=(10,), alphas=(0.05,))
    assert (cm["size"] < 0.08).all()
    cf = an.calib_fwer(aa, _lat(), 0.005, 0.05, ns=(20,), adaptive_bs=(20,), block=100, n_boot=20,
                       adaptive_kw={"n_min": 5})
    assert (cf.fwer <= 0.2).all() and set(cf.procedure) == {"craf", "craf_adaptive"}


def test_analysis_pipeline_end_to_end(tmp_path):
    """run_phase3b.cell_job / ds_job on a synthetic pool (plumbing only)."""
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("run_phase3b", root / "scripts" / "run_phase3b.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["run_phase3b"] = mod
    spec.loader.exec_module(mod)
    rng = np.random.default_rng(4)
    N = 300
    names = ["degree", "strat:block", "strat:b", "strat:b+block"]   # PCGA-L needs a 'block' attribute
    mu = {"degree": 0.03, "strat:block": 0.02, "strat:b": 0.03, "strat:b+block": 0.0, "er": 0.05}
    pool = tmp_path / "out" / "pool"
    pool.mkdir(parents=True)
    for arch in ("gcn", "sage"):
        rows = []
        for i in range(N):
            real = 0.8 + 0.01 * rng.standard_normal()
            base = {"scenario": "toy", "instance": i, "val_score": 0.0, "fit_seconds": 0.1, "valid": True}
            rows += [{**base, "variant": "real", "draw": 0, "test_score": real, "test_acc": 0.8},
                     {**base, "variant": "empty", "draw": 0, "test_score": 0.6, "test_acc": 0.6}]
            for k, m in mu.items():
                for j in range(1 if k == "er" else 2):
                    rows.append({**base, "variant": k, "draw": j, "gen_seconds": 0.01,
                                 "test_score": real - m + 0.008 * rng.standard_normal()})
        pd.DataFrame(rows).to_csv(pool / f"toy__{arch}__000000_000300.csv.gz", index=False)
    pd.DataFrame([{"scenario": "toy", "instance": i, "variant": "mlp", "draw": 0, "test_score": 0.55,
                   "test_acc": 0.5, "fit_seconds": 0.1, "valid": True} for i in range(N)]).to_csv(
        pool / "toy__mlp__000000_000300.csv.gz", index=False)
    cfg = {"out_dir": str(tmp_path / "out"), "master_seed": 1, "archs": ["gcn", "sage"], "lattice_attrs": ["block", "b"],
           "elements": {"toy": names},
           "analysis": {"delta": 0.005, "alpha": 0.05, "block": 100, "b_conf": 40, "budgets": [20, 40],
                        "fullset_budgets": [6], "fullset_r_dev": 20, "calib_boot": 5, "calib_seed": 0,
                        "adaptive": {"search_frac": 1 / 3, "n_min": 5, "d_floor": 0.003, "kappa": 1.0}}}
    (tmp_path / "out" / "analysis").mkdir()
    msg = mod.cell_job(("toy", "gcn", cfg))
    assert "N=300" in msg
    an_dir = tmp_path / "out" / "analysis"
    ref = pd.read_csv(an_dir / "reference_toy__gcn.csv")
    assert ref.loc[ref.element == "strat:b+block", "cert_min"].item()
    rs = pd.read_csv(an_dir / "resampling_toy__gcn.csv.gz")
    assert set(rs.procedure) >= {"craf", "craf_adaptive", "ni_holm", "craf_children", "naive_point", "pcga_l"}
    fs = pd.read_csv(an_dir / "fullset_toy__gcn.csv.gz")
    assert {"exhaustive_iut", "fullset_adaptive_fb", "pcga_l"} <= set(fs.procedure)
    assert len(pd.read_csv(an_dir / "calib_fwer_toy__gcn.csv"))
