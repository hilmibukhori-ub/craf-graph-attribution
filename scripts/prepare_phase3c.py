#!/usr/bin/env python
"""Label-free Phase 3C attributes and admissibility audit; never fits a model."""

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.nulls.admissibility import AdmissibilityPolicy, candidate_admissible, effective_diversity  # noqa: E402
from rusa.nulls.generators import stratum_codes  # noqa: E402
from rusa.realworld.attributes import compute_attributes  # noqa: E402
from rusa.realworld.data import load_npz_dataset  # noqa: E402
from rusa.realworld.phase3c import compute_attributes_3c  # noqa: E402
from rusa.realworld.pool import audit_null, lattice_names, sample_null  # noqa: E402
from rusa.utils.seeding import environment_info, rng_for, sha256_file  # noqa: E402


def audit_dataset(cfg, ds_name, dcfg):
    policy = AdmissibilityPolicy()
    out = ROOT / cfg["out_dir"] / "admissibility"
    out.mkdir(parents=True, exist_ok=True)
    raw = ROOT / cfg["data_dir"] / dcfg["file"]
    if dcfg.get("sha256") and sha256_file(raw) != dcfg["sha256"]:
        raise ValueError(f"raw hash mismatch: {ds_name}")
    ds = load_npz_dataset(raw, ds_name)
    t0 = time.time()
    attrs = compute_attributes_3c(ds.graph, ds.X_raw, int(cfg["attr_seed"]))
    apath = ROOT / cfg["data_dir"] / "processed" / f"{ds_name}_attrs.npz"
    apath.parent.mkdir(parents=True, exist_ok=True)
    np.savez(apath, **attrs)
    arows = []
    for k, v in attrs.items():
        cnt = np.bincount(v)
        arows.append({"attribute": k, "n_strata": len(cnt), "min_size": int(cnt.min()),
                      "max_size": int(cnt.max()), "sizes": " ".join(map(str, cnt))})
    pd.DataFrame(arows).to_csv(out / f"{ds_name}_attributes.csv", index=False)

    rows, verdicts = [], []
    names = lattice_names(cfg["lattice_attrs"], int(cfg["max_order"])) + ["er"]
    for name in names:
        res, samples, secs = [], [], []
        for s in range(int(cfg["admissibility"]["n_samples"])):
            key = (int(cfg["master_seed"]), ds_name, "admissibility", name, s)
            t1 = time.perf_counter()
            gp, info = sample_null(name, ds.graph, attrs, rng_for(*key), cfg["swap_factor"], cfg["attempt_factor"])
            secs.append(time.perf_counter() - t1)
            r = audit_null(name, ds.graph, gp, attrs, info, key, policy)
            res.append(r)
            samples.append(gp)
            rows.append({"element": name, "sample": s, "gen_seconds": secs[-1], **r.to_row()})
        v = candidate_admissible(res, policy)
        div = effective_diversity(samples[:int(cfg["admissibility"]["n_diversity"])])
        S = name[6:].split("+") if name.startswith("strat:") else []
        k = int(stratum_codes(attrs, tuple(sorted(S)), ds.n).max()) + 1 if S else 1
        ok = v["admissible"] and div["mean_pairwise_overlap"] <= policy.max_pairwise_overlap
        verdicts.append({"element": name, "order": len(S), "n_joint_strata": k, **v, **div,
                         "mean_gen_seconds": float(np.mean(secs)), "admissible_final": bool(ok)})
        print(ds_name, name, "admissible" if ok else "REJECTED", flush=True)
    pd.DataFrame(rows).to_csv(out / f"{ds_name}_samples.csv", index=False)
    pd.DataFrame(verdicts).to_csv(out / f"{ds_name}_elements.csv", index=False)
    (out / f"{ds_name}_meta.json").write_text(json.dumps({
        "dataset": ds_name, "raw_sha256": sha256_file(raw), "attrs_sha256": sha256_file(apath),
        "n": ds.n, "m": ds.graph.m, "n_features": ds.X.shape[1], "n_classes": ds.n_classes,
        "isolated_nodes": int((ds.graph.degrees() == 0).sum()), "seconds": time.time() - t0,
        "env": environment_info()}, indent=1, default=str))


def prepare_calibration_attrs(cfg):
    c = cfg["calibration"]
    raw = ROOT / cfg["data_dir"] / c["file"]
    ds = load_npz_dataset(raw, c["dataset"])
    attrs = compute_attributes(ds.graph, ds.X_raw, int(cfg["attr_seed"]))
    p = ROOT / cfg["data_dir"] / "processed" / f"{c['dataset']}_attrs.npz"
    p.parent.mkdir(parents=True, exist_ok=True)
    np.savez(p, **attrs)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase3c.yaml"))
    ap.add_argument("--dataset")
    ap.add_argument("--calibration-only", action="store_true")
    a = ap.parse_args()
    cfg = load_config(a.config)
    if a.calibration_only:
        print(prepare_calibration_attrs(cfg))
        return
    for name, dcfg in cfg["datasets"].items():
        if a.dataset is None or a.dataset == name:
            audit_dataset(cfg, name, dcfg)


if __name__ == "__main__":
    main()

