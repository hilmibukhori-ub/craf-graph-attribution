#!/usr/bin/env python
"""Phase 3A (CRAF) analysis: frontier certification on reused / new pools and semi-synthetic tables.

  python scripts/run_phase3a.py --config configs/phase3a.yaml --workers 8
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

from rusa.craf.core import Lattice  # noqa: E402
from rusa.craf.experiment import run_pool_grid, semisynthetic_grid  # noqa: E402
from rusa.evaluation.methods import pool_arrays, truth  # noqa: E402
from rusa.evaluation.runner import load_pool  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.utils.seeding import environment_info, sha256_file  # noqa: E402


def pool_job(args):
    spec, cfg = args
    an = cfg["analysis"]
    out = ROOT / cfg["out_dir"] / "analysis"
    t0 = time.time()
    d = Path(spec["dir"]) if Path(spec["dir"]).is_absolute() else ROOT / spec["dir"]
    df = load_pool(d, spec["scenario"], spec["model"])
    P = pool_arrays(df)
    tr = truth(P)
    if spec.get("aa"):
        tr.loc[spec["aa"], "delta"] = 0.0
    tag = f"{spec['scenario']}__{spec['model']}"
    tr.to_csv(out / f"truth_{tag}.csv")
    L = Lattice.from_names(P.names, attrs=an["lattice_attrs"])
    res = run_pool_grid(P, tr, L, an["budgets"], an["block"], delta=an["delta"], alpha=an["alpha"],
                        adaptive_kw=an["adaptive"])
    res["model"] = spec["model"]
    res["role"] = spec["role"]
    res.to_csv(out / f"craf_{tag}.csv.gz", index=False, compression="gzip")
    return f"{tag}: {len(res)} rows, {P.N} instances, |L| = {len(L)}, {time.time() - t0:.0f}s"


def ss_job(args):
    name, tab, cfg = args
    an, ss = cfg["analysis"], cfg["analysis"]["semisynthetic"]
    t0 = time.time()
    res = semisynthetic_grid(name, tab, None, an["budgets"], ss["n_exp"], an["block"], sd=ss["sd"], df_t=ss["df_t"],
                             delta=an["delta"], alpha=an["alpha"], seed=int(ss["seed"]) + sum(map(ord, name)),
                             adaptive_kw=an["adaptive"])
    res["model"] = "semisynthetic"
    res["role"] = ss["roles"].get(name, "semisynthetic")
    res.to_csv(ROOT / cfg["out_dir"] / "analysis" / f"craf_{name}__semisynthetic.csv.gz", index=False, compression="gzip")
    pd.Series(tab).to_csv(ROOT / cfg["out_dir"] / "analysis" / f"truth_{name}__semisynthetic.csv")
    return f"{name}: {len(res)} rows, {time.time() - t0:.0f}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase3a.yaml"))
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    cfg = load_config(a.config)
    (ROOT / cfg["out_dir"] / "analysis").mkdir(parents=True, exist_ok=True)
    jobs = [(pool_job, (s, cfg)) for s in cfg["analysis"]["pools"]]
    jobs += [(ss_job, (n, t, cfg)) for n, t in cfg["analysis"]["semisynthetic"]["tables"].items()]
    with ProcessPoolExecutor(a.workers) as ex:
        futs = [ex.submit(f, x) for f, x in jobs]
        msgs = [f.result() for f in futs]
    print(*msgs, sep="\n")
    (ROOT / cfg["out_dir"] / "analysis" / "analysis_meta.json").write_text(json.dumps(
        {"config": a.config, "config_sha256": sha256_file(a.config), "env": environment_info(), "log": msgs}, indent=1))


if __name__ == "__main__":
    main()
