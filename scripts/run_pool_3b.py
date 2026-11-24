#!/usr/bin/env python
"""Phase 3B pool: one task = a chunk of replicate clusters of one dataset (all archs + MLP).

  python scripts/run_pool_3b.py --config configs/phase3b.yaml --task-id 0
  python scripts/run_pool_3b.py --config configs/phase3b.yaml --list      # number of tasks
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.realworld.data import load_npz_dataset  # noqa: E402
from rusa.realworld.pool import run_chunk_3b  # noqa: E402


def tasks(cfg):
    out = []
    for ds, d in cfg["datasets"].items():
        n, c = int(d["clusters"]), int(d["chunk"])
        out += [(ds, s, min(c, n - s)) for s in range(0, n, c)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--task-id", type=int, default=None)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    cfg = load_config(a.config)
    T = tasks(cfg)
    if a.list:
        print(len(T))
        return
    ds_name, start, count = T[a.task_id]
    d = cfg["datasets"][ds_name]
    ds = load_npz_dataset(ROOT / cfg["data_dir"] / d["file"], ds_name)
    z = np.load(ROOT / cfg["data_dir"] / "processed" / f"{ds_name}_attrs.npz", allow_pickle=False)
    attrs = {k: z[k] for k in z.files}
    paths = run_chunk_3b(ds, attrs, start, count, ROOT / cfg["out_dir"] / "pool", archs=cfg["archs"],
                         elements=cfg["elements"][ds_name], draws=int(cfg["draws"]),
                         master_seed=int(cfg["master_seed"]), swap_factor=float(cfg["swap_factor"]),
                         attempt_factor=float(cfg["attempt_factor"]), split_kw=cfg["split"])
    print(*paths, sep="\n")


if __name__ == "__main__":
    main()
