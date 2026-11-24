#!/usr/bin/env python
"""Phase 2B analysis: run every procedure x K-config x budget x eps on each scenario pool.

  python scripts/run_phase2b.py --config configs/phase2b.yaml [--workers 6] [--scenarios N6_hard]

Writes <out_dir>/analysis/{truth,phase2b,seconds}_<scenario>.csv(.gz) and analysis_meta.json.
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
from rusa.evaluation.methods import pool_arrays, truth  # noqa: E402
from rusa.evaluation.phase2b import run_grid_2b, variant_seconds  # noqa: E402
from rusa.evaluation.runner import load_pool  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.utils.seeding import environment_info, sha256_file  # noqa: E402


def analyse(args):
    sc, cfg = args
    an = cfg["analysis"]
    out = ROOT / cfg["out_dir"] / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    df = load_pool(ROOT / cfg["out_dir"] / "pool", sc, cfg["model"])
    n_inst = df["instance"].nunique()
    if n_inst != int(cfg["scenarios"][sc]):
        return f"{sc}: SKIPPED incomplete pool ({n_inst})"
    P = pool_arrays(df)
    tr = truth(P)
    aa = SCENARIOS[sc].get("aa")
    if aa:
        tr.loc[aa, "delta"] = 0.0  # exact by construction
    tr.to_csv(out / f"truth_{sc}.csv")
    sec = variant_seconds(df)
    pd.Series(sec, name="seconds").to_csv(out / f"seconds_{sc}.csv")
    aud = df[~df.variant.isin(["real", "empty"])].agg(valid_rate=("valid", "mean"))
    res = run_grid_2b(P, tr, sec, an["k_configs"], an["eps"], an["block"], int(cfg["master_seed"]),
                      r_dev=an["r_dev"], n_conf_max=an["n_conf_max"], top_m=an["top_m"],
                      search_frac=an["search_frac"], alpha=an["alpha"], alpha1=an["alpha1"],
                      hit_tol=an["hit_tol"], n_min=an["n_min"], d_floor=an["d_floor"])
    res.to_csv(out / f"phase2b_{sc}.csv.gz", index=False, compression="gzip")
    return f"{sc}: {len(res)} rows in {time.time() - t0:.0f}s; audit valid rate {float(aud.iloc[0, 0]):.4f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(ROOT / "configs/phase2b_smoke.yaml"))
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--scenarios", nargs="*")
    a = ap.parse_args()
    cfg = load_config(a.config)
    jobs = [(s, cfg) for s in (a.scenarios or list(cfg["scenarios"]))]
    if a.workers > 1:
        with ProcessPoolExecutor(a.workers) as ex:
            msgs = list(ex.map(analyse, jobs))
    else:
        msgs = [analyse(j) for j in jobs]
    print(*msgs, sep="\n")
    (ROOT / cfg["out_dir"] / "analysis" / "analysis_meta.json").write_text(json.dumps(
        {"config": a.config, "config_sha256": sha256_file(a.config), "env": environment_info(), "log": msgs}, indent=1))


if __name__ == "__main__":
    main()
