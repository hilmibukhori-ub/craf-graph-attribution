"""Summaries with Monte Carlo uncertainty (Wilson intervals, paired experiment-level differences)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def wilson(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    if n == 0:
        return (np.nan, np.nan)
    z = stats.norm.ppf(0.5 + conf / 2)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def rate_row(x: pd.Series) -> dict:
    x = x.dropna().astype(bool)
    k, n = int(x.sum()), int(len(x))
    lo, hi = wilson(k, n)
    return {"rate": k / n if n else np.nan, "k": k, "n": n, "mc_se": np.sqrt((k / n) * (1 - k / n) / n) if n else np.nan,
            "wilson_lo": lo, "wilson_hi": hi}


def summarize_comparison(cmp: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (sc, eps, proc), g in cmp.groupby(["scenario", "eps", "procedure"], sort=False):
        claim = rate_row(g["claim"])
        row = {"scenario": sc, "eps": eps, "procedure": proc, "n_exp": len(g),
               "claim_rate": claim["rate"], "claim_lo": claim["wilson_lo"], "claim_hi": claim["wilson_hi"],
               "theta_full": g["theta_full"].iloc[0], "theta_target_mean": g["theta_target"].mean(),
               "target_null_true_frac": float((g["theta_target"] <= eps).mean()),
               "false_vs_full_rate": g["false_vs_full"].mean(),
               "false_vs_target_rate": g["false_vs_target"].mean(),
               "mean_fits": g["fits"].mean(), "budget": g["budget"].iloc[0], "mean_n_instances": g["n_instances"].mean()}
        cov = g["covered"].dropna()
        if len(cov):
            c = rate_row(cov)
            row.update({"coverage": c["rate"], "coverage_lo": c["wilson_lo"], "coverage_hi": c["wilson_hi"]})
            row["mean_L"] = g["L"].mean()
        if "hit_hardest" in g and g["hit_hardest"].notna().any():
            h = rate_row(g["hit_hardest"])
            ht = rate_row(g["hit_within_tol"])
            row.update({"hit_rate": h["rate"], "hit_lo": h["wilson_lo"], "hit_hi": h["wilson_hi"],
                        "hit_tol_rate": ht["rate"], "hit_tol_lo": ht["wilson_lo"], "hit_tol_hi": ht["wilson_hi"],
                        "mean_regret": g["regret"].mean(), "max_regret": g["regret"].max()})
        rows.append(row)
    return pd.DataFrame(rows)


def paired_procedure_difference(cmp: pd.DataFrame, a: str, b: str, col: str = "claim") -> pd.DataFrame:
    """Experiment-paired difference in rates (a - b) with a normal-approximation 95% CI."""
    rows = []
    for (sc, eps), g in cmp.groupby(["scenario", "eps"], sort=False):
        ga = g[g.procedure == a].set_index("first_instance")[col].astype(float)
        gb = g[g.procedure == b].set_index("first_instance")[col].astype(float)
        d = (ga - gb).dropna()
        if len(d) < 2:
            continue
        se = d.std(ddof=1) / np.sqrt(len(d))
        rows.append({"scenario": sc, "eps": eps, "a": a, "b": b, "metric": col, "diff": d.mean(),
                     "ci_lo": d.mean() - 1.96 * se, "ci_hi": d.mean() + 1.96 * se, "n_exp": len(d)})
    return pd.DataFrame(rows)


def summarize_calibration(cal: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (sc, R, comp, m), g in cal.groupby(["scenario", "R", "comparator", "method"], sort=False):
        r = rate_row(g["reject_true_null"])
        rows.append({"scenario": sc, "R": R, "comparator": comp, "method": m, "exact_truth": bool(g["exact_truth"].iloc[0]),
                     "miscoverage": r["rate"], "mc_se": r["mc_se"], "lo": r["wilson_lo"], "hi": r["wilson_hi"],
                     "n_subsets": r["n"], "mean_width": float((g["mean"] - g["L"]).mean()) if g["L"].notna().any() else np.nan})
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame, floatfmt: str = ".4f") -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)):
                cells.append("" if np.isnan(v) else format(v, floatfmt))
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)
