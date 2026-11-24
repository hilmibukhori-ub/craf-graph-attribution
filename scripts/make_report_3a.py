#!/usr/bin/env python
"""Phase 3A tables and figures from <out_dir>/analysis.  python scripts/make_report_3a.py --config configs/phase3a.yaml"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.craf.core import Lattice, true_frontier  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.reporting.report import md_table, rate_row  # noqa: E402

PROCS = ["craf", "craf_adaptive", "craf_children", "ni_holm", "factorial_unadj", "naive_point", "pcga_l"]
KEYS = ["scenario", "model", "role", "b", "procedure"]


def summarize(df):
    rows = []
    for key, g in df.groupby(KEYS, sort=False):
        r = dict(zip(KEYS, key))
        r.update({"n_exp": len(g), "F_true": g["F_true"].iloc[0], "budget": int(g["budget"].iloc[0]),
                  "mean_fits": g["fits"].mean()})
        for col in ("exact", "false_member", "class_error", "false_adv", "false_suf", "covered", "specificity_claim",
                    "min_cert_false"):
            if col in g and g[col].notna().any():
                rr = rate_row(g[col].dropna().astype(bool))
                r.update({col: rr["rate"], f"{col}_hi": rr["wilson_hi"], f"{col}_lo": rr["wilson_lo"]})
        for col in ("n_missed", "n_reported", "n_inconclusive", "unc_size", "min_cert_not_certmin", "n_A", "n_C"):
            if col in g and g[col].notna().any():
                r[col] = g[col].mean()
        r["modal_report"] = g["reported"].fillna("").replace("", "∅").value_counts().index[0]
        rows.append(r)
    s = pd.DataFrame(rows)
    s["procedure"] = pd.Categorical(s["procedure"], PROCS, ordered=True)
    return s.sort_values(["role", "scenario", "model", "b", "procedure"])


def paired(df, a, b, col):
    out = []
    for key, g in df.groupby(["scenario", "model", "b"], sort=False):
        ga = g[g.procedure == a].set_index("experiment")[col].astype(float)
        gb = g[g.procedure == b].set_index("experiment")[col].astype(float)
        d = (ga - gb).dropna()
        if len(d) < 2:
            continue
        se = d.std(ddof=1) / np.sqrt(len(d))
        out.append({"scenario": key[0], "model": key[1], "b": key[2], "a": a, "b_proc": b, "metric": col,
                    "diff": d.mean(), "ci_lo": d.mean() - 1.96 * se, "ci_hi": d.mean() + 1.96 * se, "n_exp": len(d)})
    return pd.DataFrame(out)


def wide(s, value, procs=PROCS):
    t = s[s.procedure.isin(procs)]
    w = t.pivot_table(index=["role", "scenario", "model", "b"], columns="procedure", values=value, observed=True)
    w.columns = [str(c) for c in w.columns]
    return w.reset_index()


def truths(an, delta):
    rows = []
    for f in sorted(an.glob("truth_*.csv")):
        tag = f.stem[len("truth_"):]
        t = pd.read_csv(f, index_col=0)
        col = "delta" if "delta" in t.columns else t.columns[0]
        L = Lattice.from_names(t.index, attrs=None)
        if tag.endswith("semisynthetic"):
            L = Lattice({n: (frozenset() if n == "degree" else frozenset(n[6:].split("+"))) for n in t.index})
        else:
            L = Lattice.from_names(t.index, attrs=["block", "w1", "w2", "w3", "w4"])
        dt = {n: float(t.loc[n, col]) for n in L.names}
        tf = true_frontier(L, dt, delta)
        near = sorted(dt.items(), key=lambda kv: abs(kv[1] - delta))[:3]
        nonmono = [(a, b) for a in L.names for b in L.names if L.sets[a] < L.sets[b] and a in tf["suff"] and b in tf["ins"]]
        rows.append({"pool": tag, "|L|": len(L), "F_true": "|".join(sorted(tf["F"])) or "∅ (none sufficient)",
                     "n_sufficient": len(tf["suff"]), "min_delta": min(dt.values()),
                     "closest_to_margin": "; ".join(f"{n}={v:.4f}" for n, v in near),
                     "nonmonotone_pairs": len(nonmono)})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase3a.yaml"))
    a = ap.parse_args()
    cfg = load_config(a.config)
    an = ROOT / cfg["out_dir"] / "analysis"
    rep = ROOT / cfg["out_dir"] / "report"
    rep.mkdir(parents=True, exist_ok=True)
    df = pd.concat([pd.read_csv(f) for f in sorted(an.glob("craf_*.csv.gz"))], ignore_index=True)
    delta = cfg["analysis"]["delta"]
    md = [f"# {cfg['name']} report (generated from {an.relative_to(ROOT)})", ""]
    tr = truths(an, delta)
    tr.to_csv(rep / "truth_frontiers.csv", index=False)
    md += ["## True frontiers (Monte Carlo truths; A/A elements exact 0)", "", md_table(tr, ".4f"), ""]
    s = summarize(df)
    s.to_csv(rep / "summary.csv", index=False)
    for v, title in (("exact", "Exact frontier recovery: reported frontier == true frontier"),
                     ("false_member", "False frontier member: some reported element is not truly minimal sufficient"),
                     ("class_error", "FWER of certifications (any false advantage or false sufficiency)"),
                     ("covered", "Uncertainty-set coverage: true frontier ⊆ possible_min (CRAF)"),
                     ("unc_size", "Size of the uncertainty region |possible_min − cert_min| (CRAF)"),
                     ("n_inconclusive", "Mean number of inconclusive lattice elements"),
                     ("min_cert_not_certmin", "Elements minimal among certified-sufficient but NOT certified minimal (mean count)"),
                     ("specificity_claim", "Certified relational specificity over L (all elements certified advantage)"),
                     ("mean_fits", "Mean fits used (budget B = b (1 + |L|))")):
        if v in s:
            fmt = ".3f"
            md += [f"## {title}", "", md_table(wide(s, v), fmt), ""]
    mr = s.pivot_table(index=["role", "scenario", "model", "b"], columns="procedure", values="modal_report",
                       aggfunc="first", observed=True)
    mr.columns = [str(c) for c in mr.columns]
    md += ["## Most frequent reported frontier", "", md_table(mr.reset_index(), ".3f"), ""]
    pairs = [("craf_adaptive", "craf", "exact"), ("craf", "ni_holm", "exact"), ("craf", "naive_point", "exact"),
             ("craf", "factorial_unadj", "exact"), ("craf", "pcga_l", "exact"),
             ("craf_adaptive", "craf", "n_inconclusive"), ("craf", "ni_holm", "false_member"),
             ("craf", "naive_point", "false_member"), ("craf", "craf_children", "false_member")]
    P = pd.concat([paired(df, x, y, c) for x, y, c in pairs], ignore_index=True)
    P.to_csv(rep / "paired_differences.csv", index=False)
    md += ["## Paired differences (experiment-paired; 95% normal CI)", "", md_table(P, ".3f"), ""]
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
    cols = dict(zip(PROCS, ["#d62728", "#ff7f0e", "#9467bd", "#1f77b4", "#8c564b", "#7f7f7f", "#2ca02c"]))
    for metric, fname in (("exact", "exact_recovery.png"), ("false_member", "false_member.png"),
                          ("class_error", "fwer.png")):
        cells = s[["scenario", "model"]].drop_duplicates().values.tolist()
        fig, axes = plt.subplots(1, len(cells), figsize=(2.6 * len(cells), 2.6), squeeze=False, sharey=True)
        for j, (sc, mo) in enumerate(cells):
            ax = axes[0, j]
            for p in PROCS:
                u = s[(s.scenario == sc) & (s.model == mo) & (s.procedure == p)].sort_values("b")
                if metric in u and u[metric].notna().any():
                    ax.plot(u["b"], u[metric], marker="o", ms=3, color=cols[p], label=p)
            if metric != "exact":
                ax.axhline(0.05, ls=":", c="k", lw=0.7)
            ax.set_title(f"{sc}\n{mo}", fontsize=7)
            ax.set_xlabel("b", fontsize=7)
            ax.tick_params(labelsize=6)
        axes[0, 0].set_ylabel(metric, fontsize=8)
        axes[0, -1].legend(fontsize=5)
        fig.tight_layout()
        fig.savefig(rep / fname, dpi=150)
        plt.close(fig)


if __name__ == "__main__":
    main()
