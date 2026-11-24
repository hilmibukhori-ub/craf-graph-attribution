#!/usr/bin/env python
"""Phase 3B tables, decision-rule evaluation and frontier figures from <out_dir>/analysis.

  python scripts/make_report_3b.py --config configs/phase3b.yaml
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from rusa.craf.core import Lattice  # noqa: E402
from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.reporting.report import md_table, rate_row, wilson  # noqa: E402

PROCS = ["craf", "craf_adaptive", "craf_children", "ni_holm", "factorial_unadj", "naive_point", "pcga_l"]


def short(n):
    return "∅(degree)" if n == "degree" else n.replace("strat:", "")


def fset(s):
    s = "" if (s is None or (isinstance(s, float) and np.isnan(s))) else str(s)
    return "{" + ", ".join(short(x) for x in s.split("|") if x) + "}"


def summarize(rs):
    rows = []
    for (ds, mo, b, p), g in rs.groupby(["dataset", "model", "b", "procedure"], sort=False):
        r = {"dataset": ds, "model": mo, "b": b, "procedure": p, "n_exp": len(g), "mean_fits": g["fits"].mean()}
        for c in ("exact", "false_member", "class_error", "covered"):
            if c in g and g[c].notna().any():
                rr = rate_row(g[c].dropna().astype(bool))
                r.update({c: rr["rate"], f"{c}_hi": rr["wilson_hi"]})
        for c in ("n_inconclusive", "unc_size", "min_cert_not_certmin"):
            if c in g and g[c].notna().any():
                r[c] = g[c].mean()
        r["modal_report"] = fset(g["reported"].fillna("").value_counts().index[0])
        rows.append(r)
    s = pd.DataFrame(rows)
    s["procedure"] = pd.Categorical(s["procedure"], PROCS, ordered=True)
    return s.sort_values(["dataset", "model", "b", "procedure"])


def paired(df, a, b, col, keys=("dataset", "model", "b")):
    out = []
    for key, g in df.groupby(list(keys), sort=False):
        ga = g[g.procedure == a].set_index("experiment")[col].astype(float)
        gb = g[g.procedure == b].set_index("experiment")[col].astype(float)
        d = (ga - gb).dropna()
        if len(d) < 2:
            continue
        se = d.std(ddof=1) / np.sqrt(len(d))
        out.append({**dict(zip(keys, key)), "a": a, "b_proc": b, "metric": col, "diff": d.mean(),
                    "ci_lo": d.mean() - 1.96 * se, "ci_hi": d.mean() + 1.96 * se, "n_exp": len(d)})
    return pd.DataFrame(out)


def hasse(ax, L, tab, title, delta):
    """Frontier figure: lattice by order; colour = status, ring = certified minimal, dashed = possibly minimal."""
    col = {"advantage": "#c0392b", "sufficient": "#2471a3", "inconclusive": "#b3b3b3"}
    names = L.names
    lev = {}
    for n in names:
        lev.setdefault(len(L.sets[n]), []).append(n)
    pos = {}
    for k, ns in lev.items():
        for i, n in enumerate(ns):
            pos[n] = ((i + 1) / (len(ns) + 1), k)
    for n in names:
        for t in L.proper_subsets(n):
            if len(L.sets[t]) == len(L.sets[n]) - 1:
                ax.plot([pos[n][0], pos[t][0]], [pos[n][1], pos[t][1]], c="#999", lw=0.6, zorder=1)
    T = tab.set_index("element")
    for n in names:
        r = T.loc[n]
        x, y = pos[n]
        ax.scatter([x], [y], s=380, c=col[r["status"]], zorder=2,
                   edgecolors="k" if r["cert_min"] else ("#2471a3" if r["possible_min"] else "none"),
                   linewidths=2.2 if r["cert_min"] else 1.2, linestyle="-" if r["cert_min"] else "--")
        val = r.get("delta_hat", r.get("mean", np.nan))
        ax.text(x, y + 0.2, short(n), ha="center", va="bottom", fontsize=6)
        ax.text(x, y - 0.22, f"{val:.3f}", ha="center", va="top", fontsize=5.5)
    ax.set_ylim(-0.6, max(lev) + 0.6)
    ax.set_xlim(0, 1)
    ax.set_yticks(sorted(lev))
    ax.set_yticklabels([f"|S|={k}" for k in sorted(lev)], fontsize=6)
    ax.set_xticks([])
    ax.set_title(title, fontsize=7)


def forest(ax, tab, delta, title):
    t = tab.reset_index(drop=True)
    y = np.arange(len(t))[::-1]
    c = t["status"].map({"advantage": "#c0392b", "sufficient": "#2471a3", "inconclusive": "#7f7f7f"})
    ax.hlines(y, t["sim_lo"], t["sim_hi"], colors=c, lw=1.5)
    ax.scatter(t["delta_hat"], y, c=c, s=12, zorder=3)
    ax.axvline(delta, ls="--", c="k", lw=0.7)
    ax.axvline(0, ls=":", c="k", lw=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels([short(n) for n in t["element"]], fontsize=6)
    ax.tick_params(axis="x", labelsize=6)
    ax.set_title(title, fontsize=7)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/phase3b.yaml"))
    a = ap.parse_args()
    cfg = load_config(a.config)
    A = cfg["analysis"]
    delta, alpha = A["delta"], A["alpha"]
    out = ROOT / cfg["out_dir"]
    an, rep = out / "analysis", out / "report"
    rep.mkdir(parents=True, exist_ok=True)
    cells = [(ds, m) for ds in cfg["datasets"] for m in cfg["archs"]]
    md = [f"# {cfg['name']} report (generated from {an.relative_to(ROOT)})", "",
          f"delta = {delta}, alpha = {alpha}, confirmatory b = {A['b_conf']} (block 0); reference = clusters >= {A['block']}.", ""]
    dec = {}

    # admissibility
    md += ["## 1. Admissibility (label-free, before any fit)", ""]
    for ds in cfg["datasets"]:
        f = out / "admissibility" / f"{ds}_elements.csv"
        if f.exists():
            t = pd.read_csv(f)[["element", "n_joint_strata", "acceptance", "mean_overlap", "mean_pairwise_overlap",
                                "mean_gen_seconds", "admissible_final"]]
            md += [f"### {ds}", "", md_table(t, ".3f"), ""]
            dec.setdefault("R2", {})[ds] = bool(t.loc[t.element != "er", "admissible_final"].mean() >= 0.5
                                                and t.loc[t.element.str.count(r"\+") == 0, "admissible_final"].sum() >= 4)

    # baselines
    md += ["## 2. Matched baselines (reference clusters; test 1 − Brier/2 and accuracy)", ""]
    B = []
    for ds, m in cells:
        b = pd.read_csv(an / f"baselines_{ds}__{m}.csv")
        b.insert(0, "model", m)
        b.insert(0, "dataset", ds)
        B.append(b)
    md += [md_table(pd.concat(B), ".4f"), ""]

    # reference + confirmatory frontiers
    md += ["## 3. Frontiers", "",
           "Reference = all clusters >= block (mean over draws), Holm at alpha; simultaneous (Bonferroni) 95% intervals. "
           "Confirmatory = block 0, uniform CRAF at b_conf (primary) and adaptive CRAF (secondary).", ""]
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:  # Hyperion's module has no matplotlib: tables only, figures made elsewhere
        plt = None
    if plt is not None:
        fig, axes = plt.subplots(len(cells), 3, figsize=(11, 3.1 * len(cells)), squeeze=False)
    fsum = []
    for i, (ds, m) in enumerate(cells):
        tag = f"{ds}__{m}"
        L = Lattice.from_names(cfg["elements"][ds])
        ref = pd.read_csv(an / f"reference_{tag}.csv")
        cu = pd.read_csv(an / f"confirm_craf_{tag}.csv")
        ca = pd.read_csv(an / f"confirm_craf_adaptive_{tag}.csv")
        log = json.loads((an / f"log_{tag}.json").read_text())
        md += [f"### {ds} / {m}", "", "Reference:", "",
               md_table(ref[["element", "n", "delta_hat", "se", "sim_lo", "sim_hi", "status", "cert_min", "possible_min",
                             "gap_set"]], ".4f"), "",
               "Confirmatory (uniform CRAF, b = %d):" % A["b_conf"], "",
               md_table(cu[["element", "delta_hat", "sim_lo", "sim_hi", "p_adv", "p_suf", "status", "cert_min",
                            "possible_min", "min_among_cert", "gap_set"]], ".4f"), ""]
        for nm, lg in (("reference", log["reference"]), ("confirm craf", log["confirm_craf"]),
                       ("confirm craf_adaptive", log["confirm_craf_adaptive"])):
            fsum.append({"dataset": ds, "model": m, "run": nm, "cert_min": fset("|".join(lg["cert_min"])),
                         "possible_min": fset("|".join(lg["possible_min"])),
                         "n_advantage": len(lg["A"]), "n_sufficient": len(lg["C"]),
                         "n_inconclusive": len(L) - len(lg["A"]) - len(lg["C"]),
                         "specificity_over_L": lg["specificity"],
                         "min_among_cert": fset("|".join(lg.get("min_among_cert", []))),
                         "gaps": "; ".join(f"{short(k)}: {fset('|'.join(v))}" for k, v in lg.get("gaps", {}).items())})
        if plt is not None:
            hasse(axes[i, 0], L, ref, f"{ds}/{m}: reference", delta)
            hasse(axes[i, 1], L, cu, f"{ds}/{m}: confirmatory CRAF b={A['b_conf']}", delta)
            forest(axes[i, 2], ref, delta, f"{ds}/{m}: Δ_S, simultaneous 95% (ref.)")
    if plt is not None:
        fig.tight_layout()
        fig.savefig(rep / "frontiers.png", dpi=160)
        plt.close(fig)
    fsum = pd.DataFrame(fsum)
    fsum.to_csv(rep / "frontier_summary.csv", index=False)
    md += ["### Frontier summary", "", md_table(fsum, ".3f"), "", "![frontiers](frontiers.png)", ""]

    # confirmatory procedure comparison
    CP = pd.concat([pd.read_csv(an / f"confirm_procedures_{ds}__{m}.csv").assign(dataset=ds, model=m) for ds, m in cells])
    CP["reported"] = CP["reported"].map(fset)
    md += ["## 4. Confirmatory block: what each procedure reports (same data, same budget)", "",
           md_table(CP[["dataset", "model", "procedure", "reported", "fits", "n_A", "n_C", "n_inconclusive"]], ".0f"), ""]

    # resampling
    rs = pd.concat([pd.read_csv(an / f"resampling_{ds}__{m}.csv.gz") for ds, m in cells], ignore_index=True)
    s = summarize(rs)
    s.to_csv(rep / "resampling_summary.csv", index=False)
    cols = ["dataset", "model", "b", "procedure", "n_exp", "exact", "false_member", "false_member_hi", "class_error",
            "class_error_hi", "covered", "n_inconclusive", "unc_size", "mean_fits", "modal_report"]
    md += ["## 5. Resampling comparison (disjoint reference blocks; leave-block-out reference truth)", "",
           md_table(s[[c for c in cols if c in s]], ".3f"), ""]
    pairs = [("craf_adaptive", "craf", "exact"), ("craf_adaptive", "craf", "n_inconclusive"),
             ("craf", "ni_holm", "false_member"), ("craf", "craf_children", "false_member"),
             ("craf", "naive_point", "false_member"), ("craf", "naive_point", "exact")]
    PD = pd.concat([paired(rs, *p) for p in pairs], ignore_index=True)
    PD.to_csv(rep / "paired_differences.csv", index=False)
    md += ["Paired differences (experiment-paired; normal 95% CI):", "", md_table(PD, ".3f"), ""]

    # full-set claim
    fs = pd.concat([pd.read_csv(an / f"fullset_{ds}__{m}.csv.gz").assign(dataset=ds, model=m) for ds, m in cells])
    fs = fs[fs.procedure.isin(["exhaustive_iut", "fullset_adaptive_fb", "pcga_l"])]
    g = fs[fs.role == "resampling"].groupby(["dataset", "model", "b", "procedure"]).agg(
        n_exp=("claim", "size"), claim=("claim", "mean"), false_vs_full=("false_vs_full", "mean"),
        theta_full=("theta_full", "mean"), fits=("fits", "mean"), fallback=("fallback", "mean")).reset_index()
    md += ["## 6. RUSA full-set claim (exhaustive IUT vs fullset_adaptive_fb; PCGA-L edge step for reference)", "",
           md_table(g, ".3f"), ""]
    fsc = fs[fs.role == "confirmatory"][["dataset", "model", "b", "procedure", "claim", "L", "theta_hat", "fits"]]
    md += ["Confirmatory block:", "", md_table(fsc, ".4f"), ""]
    fs2 = fs[fs.role == "resampling"].rename(columns={"first_instance": "fi"})
    pdf = []
    for (ds, m, b), gg in fs2.groupby(["dataset", "model", "b"]):
        x = gg[gg.procedure == "fullset_adaptive_fb"].set_index("experiment")["claim"].astype(float)
        y = gg[gg.procedure == "exhaustive_iut"].set_index("experiment")["claim"].astype(float)
        d = (x - y).dropna()
        if len(d) > 1:
            se = d.std(ddof=1) / np.sqrt(len(d))
            pdf.append({"dataset": ds, "model": m, "b": b, "diff_claim(fb − exhaustive)": d.mean(),
                        "ci_lo": d.mean() - 1.96 * se, "ci_hi": d.mean() + 1.96 * se, "n_exp": len(d)})
    if pdf:
        md += [md_table(pd.DataFrame(pdf), ".3f"), ""]

    # calibration
    md += ["## 7. Calibration on fresh clusters (exact A/A contrasts; centred real contrasts secondary)", ""]
    CM = pd.concat([pd.read_csv(an / f"calib_marginal_{ds}__{m}.csv").assign(dataset=ds, model=m) for ds, m in cells])
    CM["wilson_lo"] = [wilson(r, t)[0] for r, t in zip(CM.rejections, CM.tests)]
    CM["wilson_hi"] = [wilson(r, t)[1] for r, t in zip(CM.rejections, CM.tests)]
    CM["flag"] = CM["wilson_lo"] > CM["alpha"]
    md += ["Marginal one-sided t size (pooled over elements):", "",
           md_table(CM[["dataset", "model", "n", "direction", "alpha", "tests", "size", "wilson_lo", "wilson_hi", "flag"]],
                    ".4f"), ""]
    CF = pd.concat([pd.read_csv(an / f"calib_fwer_{ds}__{m}.csv").assign(dataset=ds, model=m) for ds, m in cells])
    k = (CF["fwer"] * CF["groups"]).round().astype(int)
    CF["wilson_lo"] = [wilson(a_, b_)[0] for a_, b_ in zip(k, CF.groups)]
    CF["wilson_hi"] = [wilson(a_, b_)[1] for a_, b_ in zip(k, CF.groups)]
    CF["flag"] = CF["wilson_lo"] > alpha
    md += ["Worst-case FWER of certifications (all elements at Delta = delta):", "",
           md_table(CF[["dataset", "model", "procedure", "n_or_b", "scheme", "source", "groups", "fwer", "false_adv",
                        "false_suf", "wilson_lo", "wilson_hi", "flag"]], ".3f"), ""]
    prim = CF[(CF.source == "aa") & (CF.scheme == "disjoint")]
    dec["R1"] = {"no_fwer_flag_primary": bool(not prim["flag"].any()),
                 "no_marginal_flag_alpha05": bool(not CM[CM.alpha == 0.05]["flag"].any())}

    # structure
    md += ["## 8. Natural structure (reference clusters)", ""]
    NM, IT = [], []
    for ds, m in cells:
        nm = pd.read_csv(an / f"nonmono_{ds}__{m}.csv").assign(dataset=ds, model=m)
        NM.append(nm)
        IT.append(pd.read_csv(an / f"interactions_{ds}__{m}.csv").assign(dataset=ds, model=m))
    NM, IT = pd.concat(NM), pd.concat(IT)
    nmc = NM[NM.certified_nonmono]
    md += [f"Certified non-monotone pairs (Delta_T > Delta_S for S ⊊ T; Holm over pairs): {len(nmc)}; "
           f"with margin delta: {int(NM.certified_nonmono_delta.sum())}.", ""]
    if len(nmc):
        md += [md_table(nmc[["dataset", "model", "S", "T", "diff", "se", "p_nonmono_holm", "certified_nonmono_delta"]],
                        ".4f"), ""]
    md += ["Largest estimated violations of monotonicity per cell:", "",
           md_table(NM.sort_values("diff", ascending=False).groupby(["dataset", "model"]).head(3)[
               ["dataset", "model", "S", "T", "diff", "se", "p_nonmono_holm"]], ".4f"), ""]
    md += ["Pairwise interactions I_ab = Delta_∅ − Delta_a − Delta_b + Delta_ab (two-sided, Holm):", "",
           md_table(IT[["dataset", "model", "element", "interaction", "se", "p_holm", "significant"]], ".4f"), ""]
    AD = []
    for ds in cfg["datasets"]:
        f = an / f"archdiff_{ds}__{cfg['archs'][0]}_minus_{cfg['archs'][1]}.csv"
        if f.exists():
            AD.append(pd.read_csv(f).assign(dataset=ds))
    if AD:
        AD = pd.concat(AD)
        md += [f"Architecture differences Delta^{cfg['archs'][0]} − Delta^{cfg['archs'][1]} (paired; Holm):", "",
               md_table(AD[["dataset", "element", "diff", "se", "p_holm", "significant"]], ".4f"), ""]
    for ds in cfg["datasets"]:
        f = an / f"attributes_vs_labels_{ds}.csv"
        if f.exists():
            md += [f"Attribute–label association, {ds} (descriptive, post hoc; never used upstream):", "",
                   md_table(pd.read_csv(f), ".3f"), ""]

    # costs
    C = pd.concat([pd.read_csv(an / f"costs_{ds}__{m}.csv").assign(dataset=ds, model=m) for ds, m in cells])
    md += ["## 9. Computational cost (CPU seconds per fit / per null draw, single thread)", "", md_table(C, ".3f"), ""]
    cost = []
    for (ds, m), g in C.groupby(["dataset", "model"]):
        g = g.set_index("variant")
        el = [n for n in cfg["elements"][ds] if n in g.index]
        per_rep = g.loc["real", "fit_seconds"] + sum(g.loc[n, "fit_seconds"] + g.loc[n, "gen_seconds"] for n in el)
        cost.append({"dataset": ds, "model": m, "cpu_s_per_replicate(real+|L| nulls)": per_rep,
                     "craf_b80_cpu_hours": 80 * per_rep / 3600, "craf_b20_cpu_hours": 20 * per_rep / 3600})
    cost = pd.DataFrame(cost)
    md += [md_table(cost, ".3f"), ""]
    dec["R4"] = {r.dataset + "/" + r.model: bool(r.craf_b80_cpu_hours <= 24) for r in cost.itertuples()}

    # decision inputs (R3 per protocol)
    r3 = {}
    for (ds, m), g in CP.groupby(["dataset", "model"]):
        g = g.set_index("procedure")
        lg = json.loads((an / f"log_{ds}__{m}.json").read_text())["confirm_craf"]
        cm = set(lg["cert_min"])
        outside_ladder = bool(cm - {"degree", "strat:block"})
        ni_diff = g.loc["ni_holm", "reported"] != g.loc["craf", "reported"]
        r3[f"{ds}/{m}"] = {"certified_member_outside_pcga_ladder": outside_ladder,
                           "ni_holm_differs_from_craf": bool(ni_diff),
                           "certified_specificity_over_L": bool(lg["specificity"])}
    dec["R3"] = r3
    dec["natural_nonmonotonicity_certified"] = bool(len(nmc) > 0)
    (rep / "decision_inputs.json").write_text(json.dumps(dec, indent=1))
    md += ["## 10. Decision inputs (rules R1–R4 of the protocol)", "", "```", json.dumps(dec, indent=1), "```", ""]
    (rep / "REPORT.md").write_text("\n".join(md))
    print(f"wrote {rep / 'REPORT.md'}")


if __name__ == "__main__":
    main()
