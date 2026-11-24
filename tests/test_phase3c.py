"""Phase 3C structural, leakage, and calibration tests."""

import inspect

import numpy as np
import pandas as pd

from rusa.realworld.calibration3c import aa_matrix, analyze_calibration
from rusa.realworld.phase3c import compute_attributes_3c, local_clustering_bins, two_hop_bins
from rusa.realworld.pool import audit_null, sample_null
from rusa.utils.seeding import rng_for

from test_phase3b import _toy


def test_phase3c_attributes_are_label_free_and_deterministic():
    assert not (set(inspect.signature(compute_attributes_3c).parameters) & {"y", "labels", "split", "score"})
    d = _toy(n=90, seed=31)
    a = compute_attributes_3c(d.graph, d.X_raw, 12)
    b = compute_attributes_3c(d.graph, d.X_raw, 12)
    assert set(a) == {"block", "fsim", "clust", "hop2"}
    assert all(np.array_equal(a[k], b[k]) for k in a)
    d.y[:] = np.random.default_rng(4).permutation(d.y)
    c = compute_attributes_3c(d.graph, d.X_raw, 12)
    assert all(np.array_equal(a[k], c[k]) for k in a)


def test_local_and_twohop_bins_are_valid_node_partitions():
    d = _toy(n=90, seed=32)
    for x in (local_clustering_bins(d.graph), two_hop_bins(d.graph)):
        assert x.shape == (d.n,)
        assert x.dtype == np.int64
        assert x.min() == 0 and x.max() < 4


def test_phase3c_nulls_preserve_declared_joint_strata():
    d = _toy(n=90, seed=33)
    attrs = compute_attributes_3c(d.graph, d.X_raw, 14)
    for name in ("strat:clust", "strat:fsim+hop2"):
        gp, info = sample_null(name, d.graph, attrs, rng_for(3, name), 2.0, 1000.0)
        r = audit_null(name, d.graph, gp, attrs, info, (3, name))
        assert not r.violated_hard


def _cal_frame(N=160, names=("degree", "strat:a"), seed=2):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(N):
        for name in names:
            z = rng.normal(size=2)
            for draw in (0, 1):
                rows.append({"instance": i, "variant": name, "draw": draw, "test_score": z[draw]})
    return pd.DataFrame(rows), list(names)


def test_calibration_analysis_preserves_block_unit():
    df, names = _cal_frame()
    ids, M = aa_matrix(df, names)
    assert np.array_equal(ids, np.arange(160)) and M.shape == (160, 2)
    p, f, d = analyze_calibration(df, names, n=80, bootstrap_reps=100, signflip_permutations=99)
    assert set(p.method) == {"t", "signflip"}
    assert (p.groups == 2).all() and (p.elements == 2).all()
    assert f.groups.item() == 2 and d["clusters"] == 160

