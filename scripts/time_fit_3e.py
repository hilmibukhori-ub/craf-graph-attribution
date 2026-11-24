#!/usr/bin/env python
"""Phase 3E timing probe (dev seed 999, not a replicate cluster): seconds/epochs per fit only.
No score or accuracy is printed or saved."""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import numpy as np  # noqa: E402

from rusa.realworld.data import load_npz_dataset, make_split  # noqa: E402
from rusa.realworld.models import fit_score  # noqa: E402

for ds_name in ("roman_empire", "amazon_ratings"):
    ds = load_npz_dataset(ROOT / "data" / "raw" / f"{ds_name}.npz", ds_name)
    print(ds_name, "n", ds.n, "m", ds.graph.m, "d", ds.X.shape[1], "classes", ds.n_classes, flush=True)
    s = make_split(ds.y, np.random.default_rng(999), train_frac=0.5, val_frac=0.25)
    for arch in ("gcn", "sage", "mlp"):
        t = time.time()
        r = fit_score(arch, ds.X, ds.y, ds.graph if arch != "mlp" else None, s, 999)
        print(ds_name, arch, f"{time.time() - t:.2f}s", "epochs", r["epochs_run"], flush=True)
