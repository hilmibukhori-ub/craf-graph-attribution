#!/usr/bin/env python
"""Phase 2C tables (markdown + CSV) and figures, generated only from <out_dir>/analysis.

  python scripts/make_report_2c.py --config configs/phase2c.yaml

Every metric is reported against the estimand the procedure actually certifies:
  scope "full"     -> theta_full  (min over {empty} + all K candidates)
  scope "selected" -> theta_sel   (min over {empty} + the selected nulls)
  scope "L3"       -> Delta_{strat:block} (PCGA-L edge step)
plus, for information only, the full-set false-claim rate of every procedure.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.data.synthetic import PHASE2C_BINDING  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.reporting.report import md_table, rate_row  # noqa: E402

PROCS = ["pcga_l", "exhaustive_iut", "fullset_adaptive", "fullset_adaptive_fb", "fullset_adaptive_s",
         "screen_uniform", "screen_random", "screen_sh", "oracle_select"]
KEYS = ["scenario", "k_config", "b", "eps", "procedure"]


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for key, g in df.groupby(KEYS, sort=False):
        c = rate_row(g["claim"])
        r = dict(zip(KEYS, key))
        scope = g["scope"].iloc[0]
        r.update({"scope": scope, "n_exp": len(g), "budget": int(g["budget"].iloc[0]),
                  "theta_full": g["theta_full"].iloc[0], "theta_target_mean": g["theta_target"].mean(),
                  "claim_rate": c["rate"], "claim_lo": c["wilson_lo"], "claim_hi": c["wilson_hi"],
                  "false_vs_full": g["false_vs_full"].mean(), "false_vs_target": g["false_vs_target"].mean(),
                  "mean_fits": g["fits"].mean(), "mean_seconds": g["seconds"].mean(),
                  "mean_instances": g["n_instances"].mean()})
        for col in ("covered_full", "covered_target", "discovered"):
            if col in g and g[col].notna().any():
                rr = rate_row(g[col].dropna().astype(bool))
                r.update({col: rr["rate"], f"{col}_lo": rr["wilson_lo"], f"{col}_hi": rr["wilson_hi"]})
        # appropriate estimand: theta_full for full-set, own target otherwise
        own = "est_error" if scope == "full" else "est_error_target"
        r["coverage_own"] = r.get("covered_full" if scope == "full" else "covered_target", np.nan)
        for nm, col in (("own", own), ("vs_full", "est_error")):
            e = g[col].dropna()
            r[f"bias_{nm}"] = e.mean() if len(e) else np.nan
            r[f"rmse_{nm}"] = float(np.sqrt((e ** 2).mean())) if len(e) else np.nan
        for col in ("feasible", "fallback", "infeasible"):
            if col in g:
                r[f"rate_{col}"] = g[col].astype(float).mean()
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


def wide(s, value, eps, scen_prefix, procs=None):
    t = s[(s.eps == eps) & s.scenario.str.startswith(scen_prefix)]
    if procs:
        t = t[t.procedure.isin(procs)]
    w = t.pivot_table(index=["scenario", "k_config", "b"], columns="procedure", values=value, observed=True)
    w.columns = [str(c) for c in w.columns]
    return w.reset_index()


def truths(an, cfg):
    rows = []
    for f in sorted(an.glob("truth_*.csv")):
        t = pd.read_csv(f).set_index("comparator")
        sc = f.stem[len("truth_"):]
        for kc in cfg["analysis"]["k_configs"]:
            arms = [k for k in t.index if k != "empty" and (":" not in k or k.startswith("perm:")
                    or all(x in kc["attrs"] for x in k.split(":", 1)[1].split("+")))]
            d = t.loc[["empty"] + arms, "delta"].sort_values()
            th = d.iloc[0]
            rows.append({"scenario": sc, "k_config": kc["name"], "K": len(arms), "theta_full": th,
                         "argmin": d.index[0], "delta_binding": t.loc[PHASE2C_BINDING, "delta"],
                         "second": d.index[1], "delta_second": d.iloc[1], "gap": d.iloc[1] - th,
                         "delta_empty": t.loc["empty", "delta"], "delta_strat_block": t.loc["strat:block", "delta"],
                         "n_within_0.002": int((d <= th + 0.002).sum()), "n_within_0.005": int((d <= th + 0.005).sum()),
                         "sd_unit_binding": t.loc[PHASE2C_BINDING, "sd_unit"], "max_mc_se": t["mc_se"].max()})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase2c_smoke.yaml"))
    a = ap.parse_args()
    cfg = load_config(a.config)
    an = ROOT / cfg["out_dir"] / "analysis"
    rep = ROOT / cfg["out_dir"] / "report"
    rep.mkdir(parents=True, exist_ok=True)
    df = pd.concat([pd.read_csv(f) for f in sorted(an.glob("phase2c_*.csv.gz"))], ignore_index=True)
    md = [f"# {cfg['name']} report (generated from {an.relative_to(ROOT)}; model {cfg['model']})", ""]

    trs = truths(an, cfg)
    trs.to_csv(rep / "truth_summary.csv", index=False)
    md += ["## Monte Carlo truths (1 - Brier units; S7 binding arm exact 0 by A/A)", "", md_table(trs, ".4f"), ""]

    s = summarize(df)
    s.to_csv(rep / "summary.csv", index=False)
    full = ["exhaustive_iut", "fullset_adaptive", "fullset_adaptive_fb", "fullset_adaptive_s"]
    for eps in sorted(df.eps.unique(), reverse=True):
        md += [f"## eps = {eps}", ""]
        md += ["### Power: claim rate in positive scenarios (S8; theta_full > eps)", "",
               md_table(wide(s, "claim_rate", eps, "S8"), ".3f"), ""]
        md += ["### Full-set false-claim rate in negative controls (S7; theta_full <= 0). "
               "A guarantee (<= alpha) exists only for scope=full procedures", "",
               md_table(wide(s, "false_vs_full", eps, "S7"), ".3f"), ""]
        md += ["### S7: Wilson 95% upper limit of the full-set claim rate (full-set procedures)", "",
               md_table(wide(s, "claim_hi", eps, "S7", full), ".3f"), ""]
        md += ["### False claims against each procedure's OWN estimand (selected: theta_sel; PCGA-L: Delta_strat:block)", "",
               md_table(wide(s, "false_vs_target", eps, ""), ".3f"), ""]
        md += [f"### Binding-null discovery ({PHASE2C_BINDING} in the selected set; full-set: top-allocated arm)", "",
               md_table(wide(s, "discovered", eps, ""), ".3f"), ""]
        md += ["### Coverage of each procedure's own estimand by its lower bound", "",
               md_table(wide(s, "coverage_own", eps, ""), ".3f"), ""]
        md += ["### Coverage of theta_full (meaningful as a guarantee for full-set procedures only)", "",
               md_table(wide(s, "covered_full", eps, ""), ".3f"), ""]
        md += ["### Estimation bias against the procedure's own estimand", "", md_table(wide(s, "bias_own", eps, ""), ".4f"), ""]
        md += ["### Estimation RMSE against the procedure's own estimand", "", md_table(wide(s, "rmse_own", eps, ""), ".4f"), ""]
        md += ["### Estimation RMSE against theta_full", "", md_table(wide(s, "rmse_vs_full", eps, ""), ".4f"), ""]
        md += ["### Feasibility (fraction of experiments in which the adaptive branch ran)", "",
               md_table(wide(s, "rate_feasible", eps, "", full[1:]), ".2f"), ""]
        md += ["### Compute: mean fits used (budget = b (2 + K))", "", md_table(wide(s, "mean_fits", eps, ""), ".0f"), ""]
        md += ["### Compute: mean measured wall-clock seconds (fits + placebo generation)", "",
               md_table(wide(s, "mean_seconds", eps, ""), ".1f"), ""]

    pairs = [("fullset_adaptive_s", "exhaustive_iut", "claim"), ("fullset_adaptive_fb", "exhaustive_iut", "claim"),
             ("fullset_adaptive", "exhaustive_iut", "claim"), ("fullset_adaptive_s", "fullset_adaptive_fb", "claim"),
             ("screen_sh", "screen_uniform", "claim"), ("screen_sh", "screen_random", "claim"),
             ("screen_sh", "screen_uniform", "discovered"), ("screen_sh", "screen_random", "discovered"),
             ("screen_uniform", "screen_random", "discovered"),
             ("screen_uniform", "exhaustive_iut", "claim"), ("screen_uniform", "exhaustive_iut", "false_vs_full"),
             ("fullset_adaptive_s", "exhaustive_iut", "covered_full")]
    P = pd.concat([paired(df, x, y, c) for x, y, c in pairs], ignore_index=True)
    P.to_csv(rep / "paired_differences.csv", index=False)
    if len(P):
        md += ["## Paired differences (experiment-paired; 95% normal CI), eps = 0.005; full table in paired_differences.csv",
               "", md_table(P[np.isclose(P.eps, max(df.eps.unique()))], ".3f"), ""]

    # combination / marginal-test audit on the exact-null arm
    for kind, title in (("audit_t", "Size of the one-sided t-test on exact-null (A/A) contrasts, disjoint groups"),
                        ("audit_comb", "Interim (alpha1 = 0.01) + inverse-normal combination (alpha2 = 0.04), "
                                       "data-dependent stage-2 size, exact-null arm"),
                        ("nullarm_describe", "Exact-null contrast distribution")):
        fs = sorted(an.glob(f"{kind}_*.csv"))
        if not fs:
            continue
        A = pd.concat([pd.read_csv(f).assign(scenario=f.stem[len(kind) + 1:]) for f in fs], ignore_index=True)
        A.to_csv(rep / f"{kind}.csv", index=False)
        if kind == "audit_t":
            A = A.pivot_table(index=["scenario", "n", "groups"], columns="alpha", values="size").reset_index()
            A.columns = [str(c) for c in A.columns]
        md += [f"## {title}", "", md_table(A, ".4f"), ""]
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
    colors = dict(zip(PROCS, ["#7f7f7f", "#1f77b4", "#ff7f0e", "#8c564b", "#d62728", "#17becf", "#bcbd22",
                              "#9467bd", "#2ca02c"]))
    styles = {"screen_uniform": "--", "screen_random": "--", "screen_sh": "--", "oracle_select": ":"}
    for metric, ylab, fname in (("claim_rate", "claim rate", "claim_rate_vs_budget.png"),
                                ("discovered", "binding-null discovery", "discovery_vs_budget.png"),
                                ("covered_full", "coverage of theta_full", "coverage_vs_budget.png"),
                                ("false_vs_full", "full-set false-claim rate", "fullset_false_claims.png")):
        scen = sorted(t.scenario.unique()) if metric != "false_vs_full" else sorted(x for x in t.scenario.unique() if x.startswith("S7"))
        if not scen:
            continue
        kcs = sorted(t.k_config.unique())
        fig, axes = plt.subplots(len(kcs), len(scen), figsize=(3.0 * len(scen), 2.6 * len(kcs)), squeeze=False, sharey=True)
        for i, kc in enumerate(kcs):
            for j, sc in enumerate(scen):
                ax = axes[i, j]
                for p in PROCS:
                    u = t[(t.k_config == kc) & (t.scenario == sc) & (t.procedure == p)].sort_values("budget")
                    if metric in u and u[metric].notna().any():
                        ax.plot(u["b"], u[metric], marker="o", ms=3, label=p, color=colors[p], ls=styles.get(p, "-"))
                if metric in ("claim_rate", "false_vs_full"):
                    ax.axhline(0.05, ls=":", c="k", lw=0.7)
                if metric == "covered_full":
                    ax.axhline(0.95, ls=":", c="k", lw=0.7)
                ax.set_title(f"{sc} / {kc}", fontsize=8)
                ax.set_xlabel("budget b (fits = b(2+K))", fontsize=7)
                ax.tick_params(labelsize=7)
            axes[i, 0].set_ylabel(ylab, fontsize=8)
        axes[0, -1].legend(fontsize=5.5, loc="best")
        fig.tight_layout()
        fig.savefig(rep / fname, dpi=150)
        plt.close(fig)


if __name__ == "__main__":
    main()
