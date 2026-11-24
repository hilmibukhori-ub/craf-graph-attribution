#!/usr/bin/env python
"""Analyze the frozen Phase 3C calibration rerun."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.realworld.calibration3c import analyze_calibration  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    a = ap.parse_args()
    cfg = load_config(a.config)
    out = ROOT / cfg["out_dir"]
    files = sorted((out / "calibration_pool").glob("*__sage_cal__*.csv.gz"))
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    if df.duplicated(["instance", "variant", "draw"]).any():
        raise ValueError("duplicate calibration rows")
    c, p = cfg["calibration"], cfg["calibration"]["primary"]
    primary, fwer, diag = analyze_calibration(
        df, c["elements"], alpha=float(p["alpha"]), n=int(p["n"]),
        bootstrap_reps=int(p["bootstrap_reps"]),
        signflip_permutations=int(c["signflip_permutations"]), seed=int(cfg["analysis"]["calib_seed"]))
    an = out / "analysis"
    an.mkdir(parents=True, exist_ok=True)
    primary.to_csv(an / "calibration_replication.csv", index=False)
    fwer.to_csv(an / "calibration_fwer.csv", index=False)
    (an / "calibration_diagnostics.json").write_text(json.dumps(diag, indent=1))
    print(primary.to_string(index=False))
    print(fwer.to_string(index=False))


if __name__ == "__main__":
    main()

