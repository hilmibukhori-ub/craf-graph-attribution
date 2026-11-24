#!/usr/bin/env python
"""Phase 3B analysis (CRAF on real graphs). Pre-specified in docs/phase3b_protocol.md.

  python scripts/run_phase3b.py --config configs/phase3b.yaml --workers 8
"""

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.craf.core import Lattice  # noqa: E402
from rusa.evaluation.methods import contrasts, pool_arrays, truth  # noqa: E402
from rusa.evaluation.phase2b import arms_for, variant_seconds  # noqa: E402
from rusa.evaluation.phase2c import run_experiment_2c  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.realworld import analysis as an  # noqa: E402
from rusa.utils.seeding import environment_info, sha256_file  # noqa: E402


def load(cfg, ds, arch):
    files = sorted((ROOT / cfg["out_dir"] / "pool").glob(f"{ds}__{arch}__*.csv.gz"))
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    if df.duplicated(["instance", "variant", "draw"]).any():
        raise ValueError(f"duplicate rows {ds}/{arch}")
    return df


def cell_job(args):
    ds, arch, cfg = args
    A = cfg["analysis"]
    out = ROOT / cfg["out_dir"] / "analysis"
    t0 = time.time()
    tag = f"{ds}__{arch}"
    df = load(cfg, ds, arch)
    mlp = load(cfg, ds, "mlp")
    P = pool_arrays(df)
    if not np.array_equal(P.instances, np.arange(P.N)):
        raise ValueError(f"missing clusters in {tag}")
    L = Lattice.from_names(cfg["elements"][ds])
    delta, alpha, blk = A["delta"], A["alpha"], A["block"]
    conf_idx = np.arange(blk)
    ref_idx = np.arange(blk, P.N)
    log = {}

    # 1. reference (high precision; clusters >= block)
    ref_tab, ref = an.reference(P, L, ref_idx, delta, alpha)
    ref_tab.to_csv(out / f"reference_{tag}.csv", index=False)
    tr_all = truth(P, ref_idx)
    tr_all.to_csv(out / f"truth_{tag}.csv")
    log["reference"] = {"cert_min": sorted(ref["cert_min"]), "possible_min": sorted(ref["possible_min"]),
                        "A": sorted(ref["A"]), "C": sorted(ref["C"]), "specificity": ref["specificity"]}

    # 2. confirmatory run (block 0)
    conf, _ = an.confirmatory(P, L, conf_idx, A["b_conf"], delta, alpha, A["adaptive"])
    for proc, (tab, res) in conf.items():
        tab.to_csv(out / f"confirm_{proc}_{tag}.csv", index=False)
        log[f"confirm_{proc}"] = {k: (sorted(v) if isinstance(v, set) else v) for k, v in res.items()
                                  if k not in ("pv",)}
    dt = {n: float(tr_all.loc[n, "delta"]) for n in L.names}
    cr = pd.DataFrame(an.procedure_rows(P, L, conf_idx, dt, [A["b_conf"]], delta, alpha, A["adaptive"]))
    cr.to_csv(out / f"confirm_procedures_{tag}.csv", index=False)

    # 3. resampling comparison on reference blocks (leave-block-out truth)
    rs = an.resampling(P, L, ref_idx, blk, A["budgets"], delta, alpha, A["adaptive"])
    rs["dataset"], rs["model"] = ds, arch
    rs.to_csv(out / f"resampling_{tag}.csv.gz", index=False, compression="gzip")

    # 4. RUSA full-set claim: exhaustive IUT vs fullset_adaptive_fb (frozen default), PCGA-L, on the same blocks
    arms = arms_for(P, cfg["lattice_attrs"])
    sec = variant_seconds(df)
    fs_rows = []
    for e in range(P.N // blk):
        b_idx = np.arange(e * blk, (e + 1) * blk)
        tr_e = truth(P, np.setdiff1d(ref_idx, b_idx))
        for b in A["fullset_budgets"]:
            for r in run_experiment_2c(P, b_idx, tr_e, arms, b, sec=sec, binding_arm=None, r_dev=A["fullset_r_dev"],
                                       n_conf_max=blk - A["fullset_r_dev"], eps=delta, alpha=alpha,
                                       master_seed=int(cfg["master_seed"]),
                                       variants={"fullset_adaptive_fb": (5, True)}):
                r.update({"experiment": e, "role": "confirmatory" if e == 0 else "resampling"})
                fs_rows.append(r)
    pd.DataFrame(fs_rows).to_csv(out / f"fullset_{tag}.csv.gz", index=False, compression="gzip")

    # 5. calibration on fresh clusters (>= block) only
    aa = an.aa_contrasts(P, ref_idx, L.names)
    an.calib_marginal(aa).to_csv(out / f"calib_marginal_{tag}.csv", index=False)
    cal = [an.calib_fwer(aa, L, delta, alpha, adaptive_kw=A["adaptive"], n_boot=A["calib_boot"],
                         seed=int(A["calib_seed"]), source="aa")]
    Dref = contrasts(P, ref_idx, L.names)
    cal.append(an.calib_fwer(Dref, L, delta, alpha, adaptive_kw=A["adaptive"], n_boot=0, source="centred"))
    pd.concat(cal).to_csv(out / f"calib_fwer_{tag}.csv", index=False)

    # 6. structure: non-monotonicity, interactions; baselines; costs
    an.nonmonotonicity(P, L, ref_idx, delta, alpha).to_csv(out / f"nonmono_{tag}.csv", index=False)
    an.interactions(P, L, ref_idx, alpha).to_csv(out / f"interactions_{tag}.csv", index=False)
    an.baselines(df, mlp, ref_idx).to_csv(out / f"baselines_{tag}.csv", index=False)
    an.costs(df, mlp).to_csv(out / f"costs_{tag}.csv", index=False)
    (out / f"log_{tag}.json").write_text(json.dumps(log, indent=1, default=str))
    return f"{tag}: N={P.N}, |L|={len(L)}, {time.time() - t0:.0f}s"


def ds_job(args):
    ds, cfg = args
    out = ROOT / cfg["out_dir"] / "analysis"
    A = cfg["analysis"]
    a, b = cfg["archs"][:2]
    Pa, Pb = pool_arrays(load(cfg, ds, a)), pool_arrays(load(cfg, ds, b))
    L = Lattice.from_names(cfg["elements"][ds])
    an.arch_differences(Pa, Pb, L, np.arange(A["block"], Pa.N), A["alpha"]).to_csv(
        out / f"archdiff_{ds}__{a}_minus_{b}.csv", index=False)
    # descriptive, post hoc: association of the label-free attributes with the labels (never used upstream)
    from rusa.realworld.data import load_npz_dataset
    d = load_npz_dataset(ROOT / cfg["data_dir"] / cfg["datasets"][ds]["file"], ds)
    z = np.load(ROOT / cfg["data_dir"] / "processed" / f"{ds}_attrs.npz", allow_pickle=False)
    rows = []
    for k in z.files:
        rows.append({"attribute": k, "nmi_with_labels": _nmi(z[k], d.y),
                     "edge_homophily_attr": float(np.mean(z[k][d.graph.edges[:, 0]] == z[k][d.graph.edges[:, 1]]))})
    rows.append({"attribute": "LABEL (reference)", "nmi_with_labels": 1.0,
                 "edge_homophily_attr": float(np.mean(d.y[d.graph.edges[:, 0]] == d.y[d.graph.edges[:, 1]]))})
    pd.DataFrame(rows).to_csv(out / f"attributes_vs_labels_{ds}.csv", index=False)
    return f"{ds}: arch differences and attribute descriptives"


def _nmi(a, b):
    from collections import Counter
    n = len(a)
    ca, cb, cab = Counter(a.tolist()), Counter(b.tolist()), Counter(zip(a.tolist(), b.tolist()))
    H = lambda c: -sum(v / n * np.log(v / n) for v in c.values())  # noqa: E731
    I = sum(v / n * np.log(v * n / (ca[x] * cb[y])) for (x, y), v in cab.items())  # noqa: E741
    return float(I / np.sqrt(H(ca) * H(cb))) if H(ca) > 0 and H(cb) > 0 else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase3b.yaml"))
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    cfg = load_config(a.config)
    (ROOT / cfg["out_dir"] / "analysis").mkdir(parents=True, exist_ok=True)
    jobs = [(cell_job, (ds, arch, cfg)) for ds in cfg["datasets"] for arch in cfg["archs"]]
    jobs += [(ds_job, (ds, cfg)) for ds in cfg["datasets"]]
    with ProcessPoolExecutor(a.workers) as ex:
        futs = [ex.submit(f, x) for f, x in jobs]
        msgs = [f.result() for f in futs]
    print(*msgs, sep="\n")
    (ROOT / cfg["out_dir"] / "analysis" / "analysis_meta.json").write_text(json.dumps(
        {"config": a.config, "config_sha256": sha256_file(a.config), "env": environment_info(), "log": msgs}, indent=1))


if __name__ == "__main__":
    main()
