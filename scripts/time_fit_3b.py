#!/usr/bin/env python
"""Timing probe (dev seed 999): seconds and epochs per fit only; scores are not printed."""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import numpy as np  # noqa: E402

from rusa.realworld.data import load_npz_dataset, make_split  # noqa: E402
from rusa.realworld.models import fit_score, to_sparse_input  # noqa: E402

for ds_name, f in (("cora", "raw/cora.npz"), ("amazon_computers", "raw/amazon_electronics_computers.npz")):
    ds = load_npz_dataset(ROOT / "data" / f, ds_name)
    s = make_split(ds.y, np.random.default_rng(999))
    xs = to_sparse_input(ds.X)
    for arch in ("gcn", "sage", "mlp"):
        for mode, xt in (("sparse", xs),):
            t = time.time()
            r = fit_score(arch, ds.X, ds.y, ds.graph if arch != "mlp" else None, s, 999, x_t=xt)
            print(ds_name, arch, mode, f"{time.time() - t:.2f}s", "epochs", r["epochs_run"], flush=True)
