#!/usr/bin/env python
"""Phase 3B preparation (LABEL-FREE): processed graphs, lattice attributes, admissibility audit.

Nothing here reads labels or fits a model. Labels stay in the raw npz and are loaded only by the
pool runner. Outputs:
  data/processed/<ds>_attrs.npz                      frozen attributes (deg, block, feat, dlen)
  <out_dir>/admissibility/<ds>_attributes.csv        stratum counts and sizes per attribute
  <out_dir>/admissibility/<ds>_samples.csv           per-sample audit rows
  <out_dir>/admissibility/<ds>_elements.csv          element-level verdicts (pre-declared rule)

  python scripts/prepare_phase3b.py --config configs/phase3b.yaml [--dataset cora]
"""

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
from rusa.realworld.pool import audit_null, lattice_names, sample_null  # noqa: E402
from rusa.utils.seeding import environment_info, rng_for, sha256_file  # noqa: E402


def load_attrs(cfg, ds_name):
    z = np.load(ROOT / cfg["data_dir"] / "processed" / f"{ds_name}_attrs.npz", allow_pickle=False)
    return {k: z[k] for k in z.files}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase3b.yaml"))
    ap.add_argument("--dataset", default=None)
    a = ap.parse_args()
    cfg = load_config(a.config)
    adm = cfg["admissibility"]
    policy = AdmissibilityPolicy()
    out = ROOT / cfg["out_dir"] / "admissibility"
    out.mkdir(parents=True, exist_ok=True)
    (ROOT / cfg["data_dir"] / "processed").mkdir(parents=True, exist_ok=True)
    for ds_name, dcfg in cfg["datasets"].items():
        if a.dataset and ds_name != a.dataset:
            continue
        t0 = time.time()
        raw = ROOT / cfg["data_dir"] / dcfg["file"]
        ds = load_npz_dataset(raw, ds_name)
        attrs = compute_attributes(ds.graph, ds.X_raw, int(cfg["attr_seed"]))   # no labels passed
        ap_ = ROOT / cfg["data_dir"] / "processed" / f"{ds_name}_attrs.npz"
        np.savez(ap_, **attrs)
        arow = []
        for k, v in attrs.items():
            cnt = np.bincount(v)
            arow.append({"attribute": k, "n_strata": len(cnt), "min_size": int(cnt.min()), "max_size": int(cnt.max()),
                         "sizes": " ".join(map(str, cnt))})
        pd.DataFrame(arow).to_csv(out / f"{ds_name}_attributes.csv", index=False)
        rows, verdicts = [], []
        for name in lattice_names(cfg["lattice_attrs"], int(cfg["max_order"])) + ["er"]:
            res, samples, secs = [], [], []
            for s in range(int(adm["n_samples"])):
                key = (int(cfg["master_seed"]), ds_name, "admissibility", name, s)
                t1 = time.perf_counter()
                gp, info = sample_null(name, ds.graph, attrs, rng_for(*key), cfg["swap_factor"], cfg["attempt_factor"])
                secs.append(time.perf_counter() - t1)
                r = audit_null(name, ds.graph, gp, attrs, info, key, policy)
                res.append(r)
                samples.append(gp)
                rows.append({"element": name, "sample": s, "gen_seconds": secs[-1], **r.to_row()})
            v = candidate_admissible(res, policy)
            div = effective_diversity(samples[: int(adm["n_diversity"])])
            S = name[6:].split("+") if name.startswith("strat:") else []
            n_strata = int(stratum_codes(attrs, tuple(sorted(S)), ds.n).max()) + 1 if S else 1
            ok = v["admissible"] and div["mean_pairwise_overlap"] <= policy.max_pairwise_overlap
            verdicts.append({"element": name, "order": len(S), "n_joint_strata": n_strata, **v, **div,
                             "mean_gen_seconds": float(np.mean(secs)), "admissible_final": bool(ok)})
            print(ds_name, name, "admissible" if ok else "REJECTED", f"acc={v['acceptance']:.2f}",
                  f"overlap={v['mean_overlap']:.3f}", f"pairwise={div['mean_pairwise_overlap']:.3f}", flush=True)
        pd.DataFrame(rows).to_csv(out / f"{ds_name}_samples.csv", index=False)
        pd.DataFrame(verdicts).to_csv(out / f"{ds_name}_elements.csv", index=False)
        (out / f"{ds_name}_meta.json").write_text(json.dumps({
            "dataset": ds_name, "raw_sha256": sha256_file(raw), "attrs_sha256": sha256_file(ap_),
            "n": ds.n, "m": ds.graph.m, "n_features": int(ds.X.shape[1]), "n_classes": ds.n_classes,
            "isolated_nodes": int((ds.graph.degrees() == 0).sum()), "seconds": time.time() - t0,
            "env": environment_info()}, indent=1))


if __name__ == "__main__":
    main()
