#!/usr/bin/env python
"""Phase 2B tables (markdown + CSV) and figures, generated only from <out_dir>/analysis.

  python scripts/make_report_2b.py --config configs/phase2b.yaml
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.reporting.report import md_table, rate_row  # noqa: E402

PROCS = ["pcga_l", "exhaustive_iut", "screen_random", "screen_uniform", "screen_sh", "fullset_alloc",
         "fullset_elim", "fullset_adaptive", "oracle_select"]
KEYS = ["scenario", "k_config", "b", "eps", "procedure"]


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for key, g in df.groupby(KEYS, sort=False):
        c = rate_row(g["claim"])
        r = dict(zip(KEYS, key))
        r.update({"scope": g["scope"].iloc[0], "n_exp": len(g), "budget": int(g["budget"].iloc[0]),
                  "theta_full": g["theta_full"].iloc[0], "claim_rate": c["rate"], "claim_lo": c["wilson_lo"],
                  "claim_hi": c["wilson_hi"], "false_vs_full": g["false_vs_full"].mean(),
                  "false_vs_target": g["false_vs_target"].mean(), "mean_fits": g["fits"].mean(),
                  "mean_seconds": g["seconds"].mean(), "mean_instances": g["n_instances"].mean()})
        for col in ("covered_full", "covered_target", "discovered"):
            if col in g and g[col].notna().any():
                rr = rate_row(g[col])
                r.update({col: rr["rate"], f"{col}_lo": rr["wilson_lo"], f"{col}_hi": rr["wilson_hi"]})
        e = g["est_error"].dropna()
        r.update({"est_bias": e.mean(), "est_rmse": float(np.sqrt((e ** 2).mean())) if len(e) else np.nan})
        rows.append(r)
    s = pd.DataFrame(rows)
    s["procedure"] = pd.Categorical(s["procedure"], PROCS, ordered=True)
    return s.sort_values(["eps", "scenario", "k_config", "b", "procedure"], ascending=[False, True, True, True, True])


def paired(df, a, b, col):
    out = []
    for key, g in df.groupby(["scenario", "k_config", "b", "eps"], sort=False):
        ga = g[g.procedure == a].set_index("first_instance")[col].astype(float)
        gb = g[g.procedure == b].set_index("first_instance")[col].astype(float)
        d = (ga - gb).dropna()
        if len(d) < 2:
            continue
        se = d.std(ddof=1) / np.sqrt(len(d))
        out.append({**dict(zip(["scenario", "k_config", "b", "eps"], key)), "a": a, "b_proc": b, "metric": col,
                    "diff": d.mean(), "ci_lo": d.mean() - 1.96 * se, "ci_hi": d.mean() + 1.96 * se, "n_exp": len(d)})
    return pd.DataFrame(out)


def wide(s, value, eps, scen_prefix):
    t = s[(s.eps == eps) & s.scenario.str.startswith(scen_prefix)]
    w = t.pivot_table(index=["scenario", "k_config", "b"], columns="procedure", values=value, observed=True)
    w.columns = [str(c) for c in w.columns]
    return w.reset_index()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase2b_smoke.yaml"))
    a = ap.parse_args()
    cfg = load_config(a.config)
    an = ROOT / cfg["out_dir"] / "analysis"
    rep = ROOT / cfg["out_dir"] / "report"
    rep.mkdir(parents=True, exist_ok=True)
    df = pd.concat([pd.read_csv(f) for f in sorted(an.glob("phase2b_*.csv.gz"))], ignore_index=True)
    md = [f"# {cfg['name']} report (generated from {an.relative_to(ROOT)})", ""]

    # truths
    tr_rows = []
    for f in sorted(an.glob("truth_*.csv")):
        t = pd.read_csv(f).set_index("comparator")
        sc = f.stem[len("truth_"):]
        for kc in cfg["analysis"]["k_configs"]:
            arms = [k for k in t.index if k != "empty" and (":" not in k or k.startswith("perm:")
                    or all(x in kc["attrs"] for x in k.split(":", 1)[1].split("+")))]
            d = t.loc[arms, "delta"].sort_values()
            th = min(t.loc["empty", "delta"], d.iloc[0])
            non_w3 = d[[k for k in d.index if "w3" not in k]]
            tr_rows.append({"scenario": sc, "k_config": kc["name"], "K": len(arms), "delta_empty": t.loc["empty", "delta"],
                            "theta_full": th, "binding": d.index[0], "second": d.index[1], "delta_second": d.iloc[1],
                            "best_non_w3": non_w3.index[0], "delta_best_non_w3": non_w3.iloc[0],
                            "theta_menu": t.loc[["empty", "er", "degree", "perm:block", "strat:block"], "delta"].min(),
                            "n_within_tol": int((d <= th + cfg["analysis"]["hit_tol"]).sum()),
                            "max_mc_se": t["mc_se"].max()})
    trs = pd.DataFrame(tr_rows)
    trs.to_csv(rep / "truth_summary.csv", index=False)
    md += ["## Monte Carlo truths (1 - Brier units; N6 binding arm exact 0)", "", md_table(trs, ".4f"), ""]

    s = summarize(df)
    s.to_csv(rep / "summary.csv", index=False)
    for eps in sorted(df.eps.unique(), reverse=True):
        md += [f"## eps = {eps}", ""]
        md += ["### Power: claim rate in positive scenarios (S6; theta_full > eps)", "",
               md_table(wide(s, "claim_rate", eps, "S6"), ".3f"), ""]
        md += ["### Type I error vs the FULL candidate set: claim rate in negative controls (N6; theta_full <= 0)", "",
               md_table(wide(s, "false_vs_full", eps, "N6"), ".3f"), ""]
        md += ["### Binding-null discovery rate (selected set / top-allocated arm contains a binding arm)", "",
               md_table(wide(s, "discovered", eps, ""), ".3f"), ""]
        md += ["### Coverage of theta_full by the robust lower bound", "", md_table(wide(s, "covered_full", eps, ""), ".3f"), ""]
        md += ["### Robust-effect estimation: bias of theta_hat - theta_full", "", md_table(wide(s, "est_bias", eps, ""), ".4f"), ""]
        md += ["### Robust-effect estimation: RMSE", "", md_table(wide(s, "est_rmse", eps, ""), ".4f"), ""]
        md += ["### Compute: mean fits used (budget = b (2 + K))", "", md_table(wide(s, "mean_fits", eps, ""), ".0f"), ""]
        md += ["### Compute: mean measured wall-clock seconds (fits + placebo generation, Hyperion)", "",
               md_table(wide(s, "mean_seconds", eps, ""), ".1f"), ""]

    pairs = [("fullset_adaptive", "exhaustive_iut", "claim"), ("fullset_adaptive", "fullset_elim", "claim"),
             ("fullset_alloc", "exhaustive_iut", "claim"), ("fullset_elim", "exhaustive_iut", "claim"),
             ("fullset_alloc", "fullset_elim", "claim"), ("screen_sh", "screen_uniform", "claim"),
             ("screen_sh", "screen_random", "claim"), ("screen_sh", "screen_uniform", "discovered"),
             ("screen_sh", "screen_random", "discovered"), ("fullset_alloc", "screen_sh", "claim"),
             ("screen_sh", "exhaustive_iut", "claim")]
    P = pd.concat([paired(df, x, y, c) for x, y, c in pairs], ignore_index=True)
    P.to_csv(rep / "paired_differences.csv", index=False)
    md += ["## Paired differences (experiment-paired; 95% normal CI); full table in paired_differences.csv", "",
           md_table(P[P.eps == sorted(df.eps.unique())[-1]], ".3f"), ""]
    (rep / "REPORT.md").write_text("\n".join(md))
    figures(s, rep)
    print(f"wrote {rep / 'REPORT.md'}")


def figures(s, rep):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    eps = s.eps.max()
    t = s[s.eps == eps]
    colors = dict(zip(PROCS, ["#7f7f7f", "#1f77b4", "#bcbd22", "#17becf", "#9467bd", "#d62728", "#ff7f0e", "#8c564b", "#2ca02c"]))
    for metric, ylab, fname in (("claim_rate", "claim rate", "claim_rate_vs_budget.png"),
                                ("discovered", "binding-null discovery", "discovery_vs_budget.png"),
                                ("covered_full", "coverage of theta_full", "coverage_vs_budget.png")):
        scen = sorted(t.scenario.unique())
        kcs = sorted(t.k_config.unique())
        fig, axes = plt.subplots(len(kcs), len(scen), figsize=(3.0 * len(scen), 2.6 * len(kcs)), squeeze=False, sharey=True)
        for i, kc in enumerate(kcs):
            for j, sc in enumerate(scen):
                ax = axes[i, j]
                for p in PROCS:
                    u = t[(t.k_config == kc) & (t.scenario == sc) & (t.procedure == p)].sort_values("budget")
                    if metric in u and u[metric].notna().any():
                        ax.plot(u["budget"], u[metric], marker="o", ms=3, label=p, color=colors[p])
                if metric == "claim_rate":
                    ax.axhline(0.05, ls=":", c="k", lw=0.7)
                if metric == "covered_full":
                    ax.axhline(0.95, ls=":", c="k", lw=0.7)
                ax.set_title(f"{sc} / {kc}", fontsize=8)
                ax.set_xlabel("fit budget", fontsize=7)
                ax.tick_params(labelsize=7)
            axes[i, 0].set_ylabel(ylab, fontsize=8)
        axes[0, -1].legend(fontsize=6, loc="best")
        fig.tight_layout()
        fig.savefig(rep / fname, dpi=150)
        plt.close(fig)


if __name__ == "__main__":
    main()
