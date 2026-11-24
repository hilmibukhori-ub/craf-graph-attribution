"""Deterministic task lists (scenario x instance-chunk) for local or SLURM-array execution."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    cfg = yaml.safe_load(Path(path).read_text())
    cfg["_path"] = str(path)
    return cfg


def pool_tasks(cfg: dict) -> list[dict]:
    tasks = []
    for sc, n in cfg["scenarios"].items():
        for start in range(0, int(n), int(cfg["chunk"])):
            tasks.append({"scenario": sc, "start": start, "count": min(int(cfg["chunk"]), int(n) - start),
                          "model": cfg["model"], "draws": int(cfg["draws"]), "specs": None,
                          "out_dir": cfg["out_dir"] + "/pool"})
    return tasks


def gnn_tasks(cfg: dict) -> list[dict]:
    g = cfg["gnn_pilot"]
    tasks = []
    for model in g["models"]:
        for sc, n in g["scenarios"].items():
            for start in range(0, int(n), int(g["chunk"])):
                tasks.append({"scenario": sc, "start": start, "count": min(int(g["chunk"]), int(n) - start),
                              "model": model, "draws": int(g["draws"]), "specs": list(g["specs"]),
                              "out_dir": g["out_dir"] + "/pool"})
    return tasks


def run_task(task: dict, cfg: dict, root: str | Path = ".") -> str:
    from .runner import run_chunk

    p = run_chunk(task["scenario"], task["start"], task["count"], Path(root) / task["out_dir"],
                  model_name=task["model"], draws=task["draws"], master_seed=int(cfg["master_seed"]),
                  swap_factor=float(cfg["swap_factor"]), specs=task["specs"], attrs=cfg.get("attrs"))
    return str(p)
