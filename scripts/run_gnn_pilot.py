#!/usr/bin/env python
"""Analyse the GCN / GraphSAGE population pilot (pools from run_pool.py --kind gnn).

  python scripts/run_pool.py --config configs/pilot.yaml --kind gnn --all --workers 8
  python scripts/run_gnn_pilot.py --config configs/pilot.yaml

One dataset of independent instances per (model, scenario): per-comparator mean contrasts
with one-sided t bounds, and IUT certificates over (a) the PCGA-L-style fixed menu and
(b) the menu extended by the w3-aware nulls.  These are single-dataset estimates, NOT
calibration evidence.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.evaluation.methods import contrasts, pool_arrays  # noqa: E402
from rusa.evaluation.runner import load_pool  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.inference.certificates import iut_certificate  # noqa: E402
from rusa.inference.tests import t_lower  # noqa: E402
from rusa.reporting.report import md_table  # noqa: E402

MENU = ["empty", "er", "degree", "perm:block", "strat:block"]
EXT = MENU + ["strat:w3", "strat:block+w3"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/pilot.yaml"))
    a = ap.parse_args()
    cfg = load_config(a.config)
    g = cfg["gnn_pilot"]
    eps = cfg["analysis"]["eps"][0]
    alpha = cfg["analysis"]["alpha"]
    out = ROOT / g["out_dir"]
    rows, certs = [], []
    for model in g["models"]:
        for sc in g["scenarios"]:
            try:
                df = load_pool(out / "pool", sc, model)
            except FileNotFoundError:
                print(f"missing pool {model}/{sc}")
                continue
            P = pool_arrays(df)
            idx = np.arange(P.N)
            D = contrasts(P, idx, ["empty"] + P.names)
            for k, d in D.items():
                d = d[np.isfinite(d)]
                r = t_lower(d, alpha, eps)
                r2 = t_lower(d, 0.025, 0.0)
                rows.append({"model": model, "scenario": sc, "comparator": k, "n": r["n"], "mean": r["mean"],
                             "ci95_lo": r2["L"], "ci95_hi": 2 * r["mean"] - r2["L"], "L_one_sided": r["L"]})
            for name, comps in (("menu", MENU), ("menu+w3", EXT)):
                c = iut_certificate({k: D[k][np.isfinite(D[k])] for k in comps}, "t", alpha, eps)
                certs.append({"model": model, "scenario": sc, "set": name, "theta_hat": c.theta_hat,
                              "L_robust": c.L_robust, "p_iut": c.p_iut, "argmin": c.argmin_L,
                              "certified": c.certified, "n": P.N})
    est, cer = pd.DataFrame(rows), pd.DataFrame(certs)
    est.to_csv(out / "gnn_estimates.csv", index=False)
    cer.to_csv(out / "gnn_certificates.csv", index=False)
    wide = est.pivot_table(index=["model", "scenario"], columns="comparator", values="mean").reset_index()
    md = ["# GNN population pilot (single dataset per cell; estimates, not calibration)", "",
          f"eps = {eps}, alpha = {alpha}.  Mean paired test contrasts (1 - Brier).", "", md_table(wide, ".4f"), "",
          "## IUT certificates", "", md_table(cer, ".4f"), "", "## Per-comparator estimates", "", md_table(est, ".4f")]
    (out / "REPORT.md").write_text("\n".join(md))
    print(f"wrote {out / 'REPORT.md'}")


if __name__ == "__main__":
    main()
