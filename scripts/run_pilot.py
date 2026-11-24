#!/usr/bin/env python
"""Analyse completed pools: compute-matched procedure comparison, calibration, A/A checks.

  python scripts/run_pilot.py --config configs/pilot.yaml [--workers 8] [--scenarios S4 S5]

Reads <out_dir>/pool, writes raw per-experiment CSVs to <out_dir>/analysis.  Analysis
choices are read from the config (frozen before the pool was generated).
"""

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from rusa.data.synthetic import SCENARIOS  # noqa: E402
from rusa.evaluation.methods import (aa_global_iut, calibration, pool_arrays, run_comparison,  # noqa: E402
                                     truth)
from rusa.evaluation.runner import load_pool  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.utils.seeding import environment_info, sha256_file  # noqa: E402


def analyse(args):
    sc, cfg = args
    an = cfg["analysis"]
    pool_dir = ROOT / cfg["out_dir"] / "pool"
    out = ROOT / cfg["out_dir"] / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    df = load_pool(pool_dir, sc, cfg["model"])
    expected = int(cfg["scenarios"][sc])
    n_inst = df["instance"].nunique()
    if n_inst != expected:
        return f"{sc}: SKIPPED, pool incomplete ({n_inst}/{expected} instances)"
    P = pool_arrays(df)
    tr = truth(P)
    tr.to_csv(out / f"truth_{sc}.csv")
    audit = df[df.variant.isin(P.names)].groupby("variant").agg(
        valid_rate=("valid", "mean"), mean_overlap=("diag_edge_overlap", "mean"),
        min_swap_completion=("diag_swap_completion", "min"), mean_gen_s=("gen_seconds", "mean"))
    audit.to_csv(out / f"audit_{sc}.csv")
    aa = SCENARIOS[sc].get("aa")
    cmp = pd.concat([run_comparison(P, block=an["block"], eps=e, r_base=an["r_base"], r_dev=an["r_dev"],
                                    top_m=an["top_m"], search_frac=an["search_frac"], alpha=an["alpha"],
                                    exact_zero=aa, hit_tol=an.get("hit_tol", 0.002))
                     for e in an["eps"]], ignore_index=True)
    cmp.to_csv(out / f"comparison_{sc}.csv.gz", index=False, compression="gzip")
    cal = calibration(P, R_list=an["calibration_R"], methods=an["calibration_methods"], alpha=an["alpha"],
                      exact_zero=aa)
    cal.to_csv(out / f"calibration_{sc}.csv.gz", index=False, compression="gzip")
    if aa:
        g = pd.concat([aa_global_iut(P, aa, R=R, alpha=an["alpha"]) for R in an["calibration_R"]])
        g.to_csv(out / f"aa_global_{sc}.csv", index=False)
    return f"{sc}: done in {time.time() - t0:.0f}s ({n_inst} instances)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(ROOT / "configs/smoke.yaml"))
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--scenarios", nargs="*")
    a = ap.parse_args()
    cfg = load_config(a.config)
    scs = a.scenarios or list(cfg["scenarios"])
    jobs = [(s, cfg) for s in scs]
    if a.workers > 1:
        with ProcessPoolExecutor(a.workers) as ex:
            msgs = list(ex.map(analyse, jobs))
    else:
        msgs = [analyse(j) for j in jobs]
    for m in msgs:
        print(m)
    meta = {"config": a.config, "config_sha256": sha256_file(a.config), "env": environment_info(), "log": msgs}
    (ROOT / cfg["out_dir"] / "analysis" / "analysis_meta.json").write_text(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
