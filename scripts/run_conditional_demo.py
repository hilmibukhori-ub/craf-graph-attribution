#!/usr/bin/env python
"""Conditional-inference demo on ONE fixed graph/split (no population claim).

Replication unit: an independent training-seed bundle r.  In bundle r every variant (real,
empty, one placebo per family) is trained with seed r, and each placebo is a fresh draw.
Swap families use the Besag--Clifford construction (hub drawn once from G0), so that under
the uniform-on-class null the real graph and the placebos are exchangeable.

Outputs per scenario:
  * conditional t lower bounds on Delta_k = E_xi[S(real)] - E_{G,xi}[S(placebo)] (given D, G0, hub);
  * the PCGA rank test: real (bundle 0) vs placebos of bundles 1..R-1 (i.i.d. seeds), exact
    under exchangeability -- reported alongside, because it tests a different (sharp) null.

  python scripts/run_conditional_demo.py --config configs/pilot.yaml [--replicates 30]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.data.synthetic import generate_instance  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.inference.certificates import iut_certificate  # noqa: E402
from rusa.inference.tests import rank_test, t_lower  # noqa: E402
from rusa.models.gnn import make_model  # noqa: E402
from rusa.nulls.admissibility import audit_sample  # noqa: E402
from rusa.nulls.generators import NullSpec, stratum_codes, swap_null  # noqa: E402
from rusa.utils.seeding import environment_info, int_seed_for, rng_for  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/pilot.yaml"))
    ap.add_argument("--replicates", type=int, default=None)
    ap.add_argument("--scenario", default=None)
    a = ap.parse_args()
    cfg = load_config(a.config)
    c = cfg["conditional_demo"]
    R = a.replicates or int(c["replicates"])
    ms = int(cfg["master_seed"])
    alpha, eps = cfg["analysis"]["alpha"], cfg["analysis"]["eps"][0]
    out = ROOT / c["out_dir"]
    out.mkdir(parents=True, exist_ok=True)
    model = make_model(c["model"])
    for sc in ([a.scenario] if a.scenario else c["scenarios"]):
        path = out / f"{sc}_scores.csv"
        inst = generate_instance(sc, int(c["instance"]), ms)
        F = inst.model_features()
        specs = [NullSpec.parse(s, chain="besag_clifford") for s in c["specs"]]
        hubs = {}
        for s in specs:
            if s.family in ("degree", "strat"):
                strata = stratum_codes(inst.node_attrs, s.attrs, inst.graph.n) if s.family == "strat" else None
                hub, _ = swap_null(inst.graph, rng_for(ms, sc, "hub", s.name), strata=strata,
                                   swap_factor=s.swap_factor, chain="forward")
                hubs[s.name] = hub
        done = pd.read_csv(path) if path.exists() else pd.DataFrame()
        rows = done.to_dict("records")
        have = set(done["replicate"]) if len(done) else set()
        for r in range(R):
            if r in have:
                continue  # checkpoint
            seed = int_seed_for(ms, sc, "cond", r)
            rec = {"replicate": r, "real": model.fit_score(F, inst.y, inst.graph, inst.split, seed)["test_score"],
                   "empty": model.fit_score(F, inst.y, None, inst.split, seed)["test_score"]}
            for s in specs:
                gp, info = s.sample(inst.graph, inst.node_attrs, rng_for(ms, sc, "cond_null", s.name, r),
                                    hub=hubs.get(s.name))
                au = audit_sample(inst.graph, gp, s, inst.node_attrs, info, (ms, r))
                rec[s.name] = model.fit_score(F, inst.y, gp, inst.split, seed)["test_score"] if au.valid else np.nan
                rec[f"valid[{s.name}]"] = au.valid
            rows.append(rec)
            pd.DataFrame(rows).to_csv(path, index=False)
        df = pd.DataFrame(rows).sort_values("replicate")
        comps = ["empty"] + [s.name for s in specs]
        D = {k: (df["real"] - df[k]).dropna().to_numpy() for k in comps}
        summ = {"scenario": sc, "instance": int(c["instance"]), "R": R, "model": c["model"], "eps": eps,
                "marginal": {k: t_lower(v, alpha, eps) for k, v in D.items()},
                "iut": iut_certificate(D, "t", alpha, eps).as_row(),
                "rank_tests": {s.name: rank_test(df["real"].iloc[0], df[s.name].iloc[1:].dropna())
                               for s in specs},
                "note": "conditional on this graph, split, hub; not population inference",
                "env": environment_info()}
        (out / f"{sc}_summary.json").write_text(json.dumps(summ, indent=1, default=float))
        print(sc, json.dumps({k: round(v["mean"], 4) for k, v in summ["marginal"].items()}),
              "IUT certified:", summ["iut"]["certified"],
              "rank p:", {k: v["p"] for k, v in summ["rank_tests"].items()})


if __name__ == "__main__":
    main()
