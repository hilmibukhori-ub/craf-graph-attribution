#!/usr/bin/env python
"""Build summary tables (markdown + CSV) and figures from <out_dir>/analysis.

  python scripts/make_report.py --config configs/pilot.yaml
Everything printed comes from the raw analysis CSVs; nothing is typed in by hand.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.evaluation.methods import MENU  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.reporting.report import (md_table, paired_procedure_difference, rate_row,  # noqa: E402
                                   summarize_calibration, summarize_comparison)

PROC_ORDER = ["pcga", "pcga_l", "single_degree", "menu_iut", "iut_all", "rusa_uniform", "rusa_sh"]


def _read_all(an: Path, prefix: str) -> pd.DataFrame:
    files = sorted(an.glob(f"{prefix}_*.csv*"))
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True) if files else pd.DataFrame()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/smoke.yaml"))
    a = ap.parse_args()
    cfg = load_config(a.config)
    an = ROOT / cfg["out_dir"] / "analysis"
    rep = ROOT / cfg["out_dir"] / "report"
    rep.mkdir(parents=True, exist_ok=True)
    md = [f"# {cfg['name']} report (generated from {an.relative_to(ROOT)})", ""]

    # ---- truth
    trs = []
    for f in sorted(an.glob("truth_*.csv")):
        t = pd.read_csv(f).set_index("comparator")
        sc = f.stem[len("truth_"):]
        arms = [k for k in t.index if k != "empty"]
        hardest = t.loc[arms, "delta"].idxmin()
        trs.append({"scenario": sc, "delta_empty": t.loc["empty", "delta"],
                    **{f"delta_{k}": t.loc[k, "delta"] for k in MENU},
                    "hardest_arm": hardest, "delta_hardest": t.loc[hardest, "delta"],
                    "theta_menu": t.loc[["empty"] + MENU, "delta"].min(),
                    "theta_full": t["delta"].min(), "max_mc_se": t["mc_se"].max(), "sd_unit_empty": t.loc["empty", "sd_unit"]})
    trs = pd.DataFrame(trs)
    trs.to_csv(rep / "truth_summary.csv", index=False)
    md += ["## Monte Carlo truths (population mean paired contrasts, 1 - Brier units)", "", md_table(trs, ".4f"), ""]

    # ---- audit
    aud = []
    for f in sorted(an.glob("audit_*.csv")):
        d = pd.read_csv(f)
        d.insert(0, "scenario", f.stem[len("audit_"):])
        aud.append(d)
    if aud:
        aud = pd.concat(aud)
        aud.to_csv(rep / "audit_summary.csv", index=False)
        g = aud.groupby("variant").agg(valid_rate_min=("valid_rate", "min"), overlap_mean=("mean_overlap", "mean"),
                                       overlap_max=("mean_overlap", "max"),
                                       swap_completion_min=("min_swap_completion", "min")).reset_index()
        md += ["## Admissibility audit (all scenarios)", "", md_table(g, ".3f"), ""]

    # ---- comparison
    cmp = _read_all(an, "comparison")
    if len(cmp):
        s = summarize_comparison(cmp)
        s["procedure"] = pd.Categorical(s["procedure"], PROC_ORDER, ordered=True)
        s = s.sort_values(["eps", "scenario", "procedure"])
        s.to_csv(rep / "comparison_summary.csv", index=False)
        for eps in sorted(cmp["eps"].unique(), reverse=True):
            t = s[s.eps == eps]
            wide = t.pivot(index="scenario", columns="procedure", values="claim_rate")
            wide.columns = [str(c) for c in wide.columns]
            wide = wide.reset_index().merge(trs[["scenario", "theta_menu", "theta_full"]], on="scenario", how="left")
            md += [f"## Claim rates at eps = {eps} (fraction of independent experiments; equal fit budget)", "",
                   md_table(wide, ".3f"), ""]
            fv = t.pivot(index="scenario", columns="procedure", values="false_vs_full_rate")
            fv.columns = [str(c) for c in fv.columns]
            md += [f"### False claims vs the full admissible set at eps = {eps} (rate of claim AND theta_full <= eps)", "",
                   md_table(fv.reset_index(), ".3f"), ""]
            cv = t.dropna(subset=["coverage"])[["scenario", "procedure", "coverage", "coverage_lo", "coverage_hi",
                                                "mean_L", "theta_target_mean", "mean_n_instances", "mean_fits", "budget"]]
            md += [f"### Robust lower-bound coverage of the procedure's own target, eps = {eps}", "", md_table(cv, ".4f"), ""]
            srch = t[t.procedure.astype(str).str.startswith("rusa")][["scenario", "procedure", "hit_rate", "hit_lo", "hit_hi",
                                                                       "hit_tol_rate", "hit_tol_lo", "hit_tol_hi",
                                                                       "mean_regret", "max_regret"]]
            md += [f"### Null-search quality (eps = {eps}; hit = true hardest admissible arm among the frozen top-m)", "",
                   md_table(srch, ".4f"), ""]
        diffs = pd.concat([paired_procedure_difference(cmp, x, y) for x, y in
                           [("rusa_sh", "iut_all"), ("rusa_uniform", "iut_all"), ("rusa_sh", "rusa_uniform"),
                            ("rusa_sh", "menu_iut")]], ignore_index=True)
        diffs.to_csv(rep / "paired_differences.csv", index=False)
        md += ["## Paired between-procedure differences in claim rate (experiment-paired, 95% normal CI)", "",
               md_table(diffs, ".3f"), ""]
        hd = pd.concat([paired_procedure_difference(cmp[cmp.procedure.str.startswith("rusa")], "rusa_sh", "rusa_uniform",
                                                    col=c) for c in ("hit_hardest", "hit_within_tol")])
        md += ["### Paired difference in hit rate (SH - uniform)", "", md_table(hd, ".3f"), ""]

    # ---- calibration
    cal = _read_all(an, "calibration")
    if len(cal):
        cs = summarize_calibration(cal)
        cs.to_csv(rep / "calibration_summary.csv", index=False)
        ex = cs[cs.exact_truth][["scenario", "R", "comparator", "method", "miscoverage", "mc_se", "lo", "hi", "n_subsets", "mean_width"]]
        md += ["## Exact A/A boundary: one-sided rejection rate of a TRUE null (nominal 0.05)", "", md_table(ex, ".4f"), ""]
        agg = cs[~cs.exact_truth].groupby(["R", "method"]).agg(
            cells=("miscoverage", "size"), mean_miscoverage=("miscoverage", "mean"),
            max_miscoverage=("miscoverage", "max"),
            cells_wilson_lo_above_005=("lo", lambda v: int((v > 0.05).sum())),
            mean_width=("mean_width", "mean")).reset_index()
        md += ["## Marginal miscoverage, all scenarios x comparators (cross-fitted MC truth)", "",
               "Cells with Wilson lower limit above 0.05 indicate over-rejection beyond MC error.", "",
               md_table(agg, ".4f"), ""]
        worst = cs[(~cs.exact_truth) & (cs.method == "t")].sort_values("miscoverage", ascending=False).head(10)
        md += ["### Ten worst t-test cells", "", md_table(worst[["scenario", "R", "comparator", "miscoverage", "lo", "hi", "n_subsets"]], ".4f"), ""]

    aa = _read_all(an, "aa_global")
    if len(aa):
        rows = []
        for (sc, R), g in aa.groupby(["scenario", "R"]):
            r1, r2 = rate_row(g["global_certified"]), rate_row(g["aa_marginal_reject"])
            rows.append({"scenario": sc, "R": R, "global_iut_reject": r1["rate"], "lo": r1["wilson_lo"], "hi": r1["wilson_hi"],
                         "aa_marginal_reject": r2["rate"], "n": r1["n"]})
        md += ["## Global IUT at the exact boundary (theta_full <= 0 because Delta_AA = 0)", "", md_table(pd.DataFrame(rows), ".4f"), ""]

    (rep / "REPORT.md").write_text("\n".join(md))
    _figures(cmp, rep)
    print(f"wrote {rep / 'REPORT.md'}")


def _figures(cmp: pd.DataFrame, rep: Path):
    if not len(cmp):
        return
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    s = summarize_comparison(cmp)
    eps = sorted(cmp["eps"].unique(), reverse=True)[0]
    s = s[s.eps == eps]
    scen = list(dict.fromkeys(s.scenario))
    procs = [p for p in PROC_ORDER if p in set(s.procedure)]
    fig, ax = plt.subplots(figsize=(max(8, 1.1 * len(scen)), 4))
    w = 0.8 / len(procs)
    for i, p in enumerate(procs):
        t = s[s.procedure == p].set_index("scenario").reindex(scen)
        x = np.arange(len(scen)) + i * w
        ax.bar(x, t.claim_rate, w, label=p)
        ax.errorbar(x, t.claim_rate, yerr=[t.claim_rate - t.claim_lo, t.claim_hi - t.claim_rate], fmt="none", ecolor="k", lw=0.6)
    ax.axhline(0.05, color="k", ls=":", lw=0.8)
    ax.set_xticks(np.arange(len(scen)) + 0.4 - w / 2)
    ax.set_xticklabels(scen, rotation=30)
    ax.set_ylabel(f"claim rate (eps={eps})")
    ax.legend(fontsize=7, ncol=4)
    fig.tight_layout()
    fig.savefig(rep / "claim_rates.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
