"""Phase 3E: heterophilous npz loader, fractional split, label-free attributes on dense features."""
import numpy as np

from rusa.realworld.data import load_npz_dataset, make_split
from rusa.realworld.phase3c import compute_attributes_3c
from rusa.realworld.pool import run_chunk_3b


def _toy_npz(tmp_path, n=60, d=6, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d)).astype(np.float32)
    y = rng.integers(0, 3, n)
    e = np.array([(i, (i + 1) % n) for i in range(n)] + [(i, (i + 7) % n) for i in range(0, n, 2)]
                 + [(3, 3), (5, 4)], dtype=np.int64)          # self-loop and reversed duplicate
    p = tmp_path / "toy_het.npz"
    np.savez(p, node_features=X, node_labels=y, edges=e,
             train_masks=np.zeros((1, n), bool), val_masks=np.zeros((1, n), bool), test_masks=np.zeros((1, n), bool))
    return p, X, y


def test_platonov_loader_symmetrises_and_keeps_signed_features(tmp_path):
    p, X, y = _toy_npz(tmp_path)
    ds = load_npz_dataset(p)
    assert ds.n == 60 and ds.n_classes == int(y.max()) + 1
    np.testing.assert_array_equal(ds.X, X)                       # used as provided, signed
    np.testing.assert_array_equal(ds.X_raw.toarray(), X.astype(np.float64))
    E = ds.graph.edges
    assert (E[:, 0] < E[:, 1]).all() and len({tuple(r) for r in E.tolist()}) == len(E)
    assert not (E[:, 0] == E[:, 1]).any()
    assert ds.graph.m == 60 + 30                                 # self-loop dropped, (5,4) duplicate of (4,5)


def test_fractional_split_is_stratified_disjoint_and_covering():
    rng = np.random.default_rng(1)
    y = np.repeat(np.arange(5), [400, 40, 9, 3, 1000])
    s = make_split(y, rng, train_frac=0.5, val_frac=0.25)
    tr, va, te = s["train"], s["val"], s["test"]
    assert len(np.intersect1d(tr, va)) == 0 and len(np.intersect1d(tr, te)) == 0 and len(np.intersect1d(va, te)) == 0
    assert len(tr) + len(va) + len(te) == len(y)
    for c, k in zip(range(5), [400, 40, 9, 3, 1000]):
        assert abs((y[tr] == c).sum() - 0.5 * k) <= 1
        if k >= 3:
            assert (y[tr] == c).sum() >= 1 and (y[va] == c).sum() >= 1 and (y[te] == c).sum() >= 1
    # default per-class mode is unchanged
    s0 = make_split(y, np.random.default_rng(1))
    assert all((y[s0["train"]] == c).sum() == min(20, k // 3) for c, k in zip(range(5), [400, 40, 9, 3, 1000]))


def test_attributes_on_dense_features_are_label_free(tmp_path):
    p, X, y = _toy_npz(tmp_path, n=80, d=8)
    ds = load_npz_dataset(p)
    a1 = compute_attributes_3c(ds.graph, ds.X_raw, 7)
    a2 = compute_attributes_3c(ds.graph, ds.X_raw, 7)
    for k in ("block", "fsim", "clust", "hop2"):
        assert len(a1[k]) == ds.n and (a1[k] == a2[k]).all()


def test_dense_pool_chunk_runs(tmp_path):
    p, X, y = _toy_npz(tmp_path, n=60)
    ds = load_npz_dataset(p)
    attrs = compute_attributes_3c(ds.graph, ds.X_raw, 3)
    paths = run_chunk_3b(ds, attrs, 0, 1, tmp_path / "pool", archs=["gcn", "sage"], elements=["degree", "strat:block"],
                         draws=1, master_seed=5, swap_factor=2.0, attempt_factor=50.0,
                         split_kw={"train_frac": 0.5, "val_frac": 0.25}, hp={"max_epochs": 5, "patience": 3})
    assert len(paths) == 3 and all(q.exists() for q in paths)
