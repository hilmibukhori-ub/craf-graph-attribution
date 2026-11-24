#!/usr/bin/env python
"""Calibration only: marginal one-sided bound coverage + global IUT at the exact A/A boundary.

  python scripts/run_calibration.py --config configs/pilot.yaml --scenarios AA_degree AA_block
Prints a compact summary; raw rows go to <out_dir>/analysis/calibration_<scenario>.csv.gz.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from rusa.data.synthetic import SCENARIOS  # noqa: E402
from rusa.evaluation.methods import aa_global_iut, calibration, pool_arrays  # noqa: E402
from rusa.evaluation.runner import load_pool  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.reporting.report import summarize_calibration  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/smoke.yaml"))
    ap.add_argument("--scenarios", nargs="*")
    a = ap.parse_args()
    cfg = load_config(a.config)
    an = cfg["analysis"]
    out = ROOT / cfg["out_dir"] / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    for sc in a.scenarios or [s for s in cfg["scenarios"] if s.startswith("AA")]:
        P = pool_arrays(load_pool(ROOT / cfg["out_dir"] / "pool", sc, cfg["model"]))
        aa = SCENARIOS[sc].get("aa")
        cal = calibration(P, an["calibration_R"], an["calibration_methods"], an["alpha"], exact_zero=aa)
        cal.to_csv(out / f"calibration_{sc}.csv.gz", index=False, compression="gzip")
        s = summarize_calibration(cal)
        print(s[s.exact_truth].to_string(index=False) if aa else s.groupby(["R", "method"]).miscoverage.agg(["mean", "max"]))
        if aa:
            g = pd.concat([aa_global_iut(P, aa, R=R, alpha=an["alpha"]) for R in an["calibration_R"]])
            g.to_csv(out / f"aa_global_{sc}.csv", index=False)
            print(g.groupby("R")[["global_certified", "aa_marginal_reject"]].mean())


if __name__ == "__main__":
    main()
