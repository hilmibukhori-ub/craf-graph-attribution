#!/usr/bin/env python
"""Generate instance pools (fit real / empty / every placebo) -- one task or all tasks.

Examples
  python scripts/run_pool.py --config configs/pilot.yaml --list
  python scripts/run_pool.py --config configs/pilot.yaml --task-id 17          # one SLURM array task
  python scripts/run_pool.py --config configs/smoke.yaml --all --workers 6     # everything locally
  python scripts/run_pool.py --config configs/pilot.yaml --kind gnn --task-id 3
Completed chunks are skipped (checkpointing), so re-running fills gaps only.
"""

import argparse
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rusa.evaluation.tasks import gnn_tasks, load_config, pool_tasks, run_task  # noqa: E402


def _one(args):
    task, cfg = args
    t0 = time.time()
    p = run_task(task, cfg, ROOT)
    return f"{task['scenario']} {task['model']} {task['start']}+{task['count']} -> {p} ({time.time() - t0:.1f}s)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(ROOT / "configs/smoke.yaml"))
    ap.add_argument("--kind", choices=["sgc", "gnn"], default="sgc")
    ap.add_argument("--task-id", type=int, default=None, help="index into the task list (SLURM_ARRAY_TASK_ID)")
    ap.add_argument("--stride", type=int, default=1, help="run task-id, task-id+stride, ... (pack tasks per job)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    cfg = load_config(a.config)
    tasks = pool_tasks(cfg) if a.kind == "sgc" else gnn_tasks(cfg)
    if a.list:
        print(len(tasks))
        return
    if a.task_id is not None:
        sel = list(range(a.task_id, len(tasks), a.stride)) if a.stride > 1 else [a.task_id]
        sel = [i for i in sel if i < len(tasks)]
        if not sel:
            print(f"task-id {a.task_id} out of range ({len(tasks)} tasks)")
            return
    elif a.all:
        sel = list(range(len(tasks)))
    else:
        ap.error("give --task-id, --all or --list")
    jobs = [(tasks[i], cfg) for i in sel]
    if a.workers > 1:
        with ProcessPoolExecutor(a.workers) as ex:
            for msg in ex.map(_one, jobs):
                print(msg, flush=True)
    else:
        for j in jobs:
            print(_one(j), flush=True)


if __name__ == "__main__":
    main()
