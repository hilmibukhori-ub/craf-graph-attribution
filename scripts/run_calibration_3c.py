#!/usr/bin/env python
"""Run one chunk of the preregistered 1,500-cluster GraphSAGE calibration rerun."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.realworld.calibration3c import run_calibration_chunk  # noqa: E402
from rusa.realworld.data import load_npz_dataset  # noqa: E402


def tasks(cfg):
    c = cfg["calibration"]
    return [(s, min(int(c["chunk"]), int(c["clusters"]) - s))
            for s in range(0, int(c["clusters"]), int(c["chunk"]))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--task-id", type=int)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    cfg = load_config(a.config)
    T = tasks(cfg)
    if a.list:
        print(len(T))
        return
    c = cfg["calibration"]
    start, count = T[a.task_id]
    ds = load_npz_dataset(ROOT / cfg["data_dir"] / c["file"], c["dataset"])
    z = np.load(ROOT / cfg["data_dir"] / "processed" / f"{c['dataset']}_attrs.npz", allow_pickle=False)
    attrs = {k: z[k] for k in z.files}
    p = run_calibration_chunk(ds, attrs, start, count, ROOT / cfg["out_dir"] / "calibration_pool",
                              elements=c["elements"], master_seed=int(c["master_seed"]),
                              swap_factor=float(cfg["swap_factor"]), attempt_factor=float(cfg["attempt_factor"]),
                              split_kw=cfg["split"])
    print(p)


if __name__ == "__main__":
    main()

