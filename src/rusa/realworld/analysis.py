"""Phase 3B analyses on fixed-graph replicate-cluster pools (pre-specified in docs/phase3b_protocol.md).

Cluster roles (fixed before any score is seen):
* block 0 = clusters 0..block-1: the **confirmatory** run (the reported real-world frontier);
* clusters >= block: the **reference** set (high-precision estimates, calibration, resampling).

Contrasts D_{r,S} = S(real) − S(null_S) within cluster r. Confirmatory and resampling procedures use
the first audit-valid draw (one fit per element and cluster, as budgeted); reference estimates use
the mean over valid draws. A/A contrasts a_{r,S} = S(draw 0) − S(draw 1) have mean exactly 0 and a
symmetric law (the two draws are exchangeable given the cluster).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from ..craf.core import ADV, SUF, Lattice, certify, directional_p, frontier_sets, true_frontier
from ..craf.experiment import adaptive_pvalues, pcga_implied, run_block
from ..evaluation.methods import PoolArrays, contrasts, truth


def _fmt(s):
    return "|".join(sorted(s))


def _t_two_sided(d):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = len(d)
    m, se = d.mean(), d.std(ddof=1) / np.sqrt(n)
    return m, se, n, float(2 * stats.t.sf(abs(m) / max(se, 1e-15), n - 1))


def _holm_adj(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    adj = np.empty_like(p)
    run = 0.0
    for r, i in enumerate(o):
        run = max(run, min(1.0, (len(p) - r) * p[i]))
        adj[i] = run
    return adj


# ------------------------------------------------------------------ frontier certification on given data
def certify_frontier(L: Lattice, D: dict, delta: float, alpha: float) -> dict:
    pv = {n: directional_p(D[n], delta) for n in L.names}
    A, C = certify(pv, alpha, "holm")
    fs = frontier_sets(L, A, C)
    return {"pv": pv, **fs, "specificity": len(A) == len(L)}


def element_table(L: Lattice, D: dict, delta: float, alpha: float, res: dict) -> pd.DataFrame:
    """Per-element estimates, Bonferroni-simultaneous two-sided (1 − alpha) intervals and CRAF status."""
    m = len(L)
    rows = []
    for n in L.names:
        d = np.asarray(D[n], float)
        d = d[np.isfinite(d)]
        k = len(d)
        mu, se = d.mean(), d.std(ddof=1) / np.sqrt(k)
        q = stats.t.isf(alpha / (2 * m), k - 1)
        st = "advantage" if n in res["A"] else ("sufficient" if n in res["C"] else "inconclusive")
        rows.append({"element": n, "order": len(L.sets[n]), "n": k, "delta_hat": mu, "se": se,
                     "sim_lo": mu - q * se, "sim_hi": mu + q * se, "p_adv": res["pv"][n][ADV],
                     "p_suf": res["pv"][n][SUF], "status": st, "cert_min": n in res["cert_min"],
                     "possible_min": n in res["possible_min"], "min_among_cert": n in res["min_among_cert"],
                     "gap_set": _fmt(res["gaps"].get(n, []))})
    return pd.DataFrame(rows)


def reference(P: PoolArrays, L: Lattice, idx, delta, alpha):
    D = contrasts(P, idx, L.names, draws="mean")
    D = {k: v[np.isfinite(v)] for k, v in D.items()}
    res = certify_frontier(L, D, delta, alpha)
    return element_table(L, D, delta, alpha, res), res


def confirmatory(P: PoolArrays, L: Lattice, idx, b: int, delta, alpha, adaptive_kw):
    """The reported real-world run on block 0: uniform CRAF (primary) and adaptive CRAF (secondary)."""
    D = contrasts(P, idx, L.names)
    D = {k: v[np.isfinite(v)] for k, v in D.items()}
    Du = {k: v[:b] for k, v in D.items()}
    uni = certify_frontier(L, Du, delta, alpha)
    out = {"craf": (element_table(L, Du, delta, alpha, uni), uni)}
    ad = adaptive_pvalues(L, D, b, delta, alpha, **(adaptive_kw or {}))
    if ad is None:
        out["craf_adaptive"] = (out["craf"][0], {**uni, "fallback": True, "fits": b * (1 + len(L))})
    else:
        pva, fits, info = ad
        A, C = certify(pva, alpha, "holm")
        fs = frontier_sets(L, A, C)
        tab = pd.DataFrame([{"element": n, "p_adv": pva[n][ADV], "p_suf": pva[n][SUF], "mean": pva[n]["mean"],
                             "n": pva[n]["n"], "status": "advantage" if n in A else ("sufficient" if n in C else
                                                                                       "inconclusive"),
                             "cert_min": n in fs["cert_min"], "possible_min": n in fs["possible_min"],
                             "min_among_cert": n in fs["min_among_cert"], "gap_set": _fmt(fs["gaps"].get(n, []))}
                            for n in L.names])
        out["craf_adaptive"] = (tab, {**fs, "specificity": len(A) == len(L), "fallback": False, "fits": fits, **info})
    return out, D


def procedure_rows(P: PoolArrays, L: Lattice, idx, delta_true: dict, budgets, delta, alpha, adaptive_kw):
    D = contrasts(P, idx, L.names)
    D = {k: v[np.isfinite(v)] for k, v in D.items()}
    rows = []
    for b in budgets:
        pc = pcga_implied(P, idx[: max(2, b * (1 + len(L)) // 5)], alpha)
        rows += run_block(L, D, delta_true, b, delta=delta, alpha=alpha, pcga=pc, adaptive_kw=adaptive_kw)
    return rows


def resampling(P: PoolArrays, L: Lattice, ref_idx, block: int, budgets, delta, alpha, adaptive_kw):
    """Procedure comparison on disjoint reference blocks, scored against the leave-block-out reference."""
    rows = []
    nb = len(ref_idx) // block
    for e in range(nb):
        blk = ref_idx[e * block:(e + 1) * block]
        rest = np.setdiff1d(ref_idx, blk)
        tr = truth(P, rest)
        dt = {n: float(tr.loc[n, "delta"]) for n in L.names}
        se = {n: float(tr.loc[n, "mc_se"]) for n in L.names}
        near = [n for n in L.names if abs(dt[n] - delta) < 2 * se[n]]
        for r in procedure_rows(P, L, blk, dt, budgets, delta, alpha, adaptive_kw):
            r.update({"experiment": e, "n_near_margin_truth": len(near), "near_margin_truth": _fmt(near)})
            rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ calibration (fresh clusters only)
def aa_contrasts(P: PoolArrays, idx, names) -> dict:
    out = {}
    for k in names:
        T = P.cand_test[k][idx]
        out[k] = T[:, 0] - T[:, 1]
    return out


def calib_marginal(aa: dict, ns=(5, 10, 20, 40, 80), alphas=(0.05 / 22, 0.01, 0.05)) -> pd.DataFrame:
    """Size of one-sided t tests (both directions) on disjoint groups of exact A/A contrasts."""
    rows = []
    for n in ns:
        for direction in (ADV, SUF):
            ps = []
            for k, a in aa.items():
                a = a[np.isfinite(a)]
                G = len(a) // n
                for g in range(G):
                    ps.append(directional_p(a[g * n:(g + 1) * n], 0.0)[direction])
            ps = np.array(ps)
            for al in alphas:
                rows.append({"n": n, "direction": direction, "alpha": al, "tests": len(ps),
                             "rejections": int((ps <= al).sum()), "size": float((ps <= al).mean()) if len(ps) else np.nan})
    return pd.DataFrame(rows)


def _group_fwer(M: np.ndarray, names, L, n, delta, alpha, adaptive_kw=None, b=None):
    """M: (clusters, elements) boundary contrasts (mean delta for every element). Returns per-group outcomes."""
    out = []
    G = M.shape[0] // n
    for g in range(G):
        X = M[g * n:(g + 1) * n]
        D = {k: X[:, j][np.isfinite(X[:, j])] for j, k in enumerate(names)}
        if adaptive_kw is None:
            pv = {k: directional_p(D[k], delta) for k in names}
            fb = False
        else:
            ad = adaptive_pvalues(L, D, b, delta, alpha, **adaptive_kw)
            if ad is None:
                pv, fb = {k: directional_p(D[k][:b], delta) for k in names}, True
            else:
                pv, fb = ad[0], False
        A, C = certify(pv, alpha, "holm")
        out.append({"any_false": bool(A or C), "false_adv": bool(A), "false_suf": bool(C), "fallback": fb})
    return out


def calib_fwer(aa: dict, L: Lattice, delta, alpha, ns=(20, 40, 80), adaptive_bs=(20, 40, 80), block=100,
               adaptive_kw=None, n_boot=2000, seed=0, source="aa") -> pd.DataFrame:
    """Worst-case (all elements at the boundary Delta = delta) FWER of CRAF certifications.

    Primary: disjoint groups of fresh clusters (exact). Secondary: cluster bootstrap of whole rows
    (keeps cross-element dependence) from the centred empirical law, for adaptive CRAF which needs
    `block` clusters per experiment.
    """
    names = L.names
    M = np.column_stack([aa[k] for k in names])
    M = M - np.nanmean(M, 0) if source == "centred" else M
    M = M + delta
    rows = []
    for n in ns:
        res = _group_fwer(M, names, L, n, delta, alpha)
        rows.append({"procedure": "craf", "n_or_b": n, "scheme": "disjoint", "groups": len(res),
                     "fwer": np.mean([r["any_false"] for r in res]) if res else np.nan,
                     "false_adv": np.mean([r["false_adv"] for r in res]) if res else np.nan,
                     "false_suf": np.mean([r["false_suf"] for r in res]) if res else np.nan, "source": source})
    rng = np.random.default_rng(seed)
    ok = np.isfinite(M).all(1)
    Mf = M[ok]
    for b in adaptive_bs:
        res = _group_fwer(M, names, L, block, delta, alpha, adaptive_kw or {}, b)
        rows.append({"procedure": "craf_adaptive", "n_or_b": b, "scheme": "disjoint", "groups": len(res),
                     "fwer": np.mean([r["any_false"] for r in res]) if res else np.nan,
                     "false_adv": np.mean([r["false_adv"] for r in res]) if res else np.nan,
                     "false_suf": np.mean([r["false_suf"] for r in res]) if res else np.nan,
                     "fallback_rate": np.mean([r["fallback"] for r in res]) if res else np.nan, "source": source})
        if n_boot and len(Mf) >= block:
            Mc = Mf - Mf.mean(0) + delta            # exact boundary in the bootstrap law
            bres = []
            for _ in range(n_boot):
                bres += _group_fwer(Mc[rng.integers(0, len(Mc), block)], names, L, block, delta, alpha,
                                    adaptive_kw or {}, b)
            rows.append({"procedure": "craf_adaptive", "n_or_b": b, "scheme": "bootstrap", "groups": len(bres),
                         "fwer": np.mean([r["any_false"] for r in bres]),
                         "false_adv": np.mean([r["false_adv"] for r in bres]),
                         "false_suf": np.mean([r["false_suf"] for r in bres]),
                         "fallback_rate": np.mean([r["fallback"] for r in bres]), "source": source})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ structure of the real frontier
def nonmonotonicity(P: PoolArrays, L: Lattice, idx, delta, alpha) -> pd.DataFrame:
    """For every comparable pair S ⊊ T: Delta_T − Delta_S (> 0 = non-monotone). One-sided t, Holm over pairs."""
    D = contrasts(P, idx, L.names, draws="mean")
    rows = []
    for T in L.names:
        for S in L.proper_subsets(T):
            d = D[T] - D[S]
            d = d[np.isfinite(d)]
            m, se, n, _ = _t_two_sided(d)
            rows.append({"S": S, "T": T, "diff": m, "se": se, "n": n,
                         "p_nonmono": float(stats.t.sf(m / se, n - 1)),
                         "p_nonmono_delta": float(stats.t.sf((m - delta) / se, n - 1)),
                         "p_mono": float(stats.t.sf(-m / se, n - 1))})
    df = pd.DataFrame(rows)
    if len(df):
        for c in ("p_nonmono", "p_nonmono_delta", "p_mono"):
            df[c + "_holm"] = _holm_adj(df[c].to_numpy())
        df["certified_nonmono"] = df["p_nonmono_holm"] <= alpha
        df["certified_nonmono_delta"] = df["p_nonmono_delta_holm"] <= alpha
    return df


def interactions(P: PoolArrays, L: Lattice, idx, alpha) -> pd.DataFrame:
    """I_ab = Delta_{} − Delta_a − Delta_b + Delta_ab for every order-2 element; two-sided t, Holm over pairs.

    Negative I_ab: preserving a and b together removes more of the advantage than the two
    singletons separately (synergy / positive interaction of the preserved properties).
    """
    D = contrasts(P, idx, L.names, draws="mean")
    rows = []
    for n in L.names:
        S = L.sets[n]
        if len(S) != 2:
            continue
        a, b = sorted(S)
        na, nb = f"strat:{a}", f"strat:{b}"
        if na not in D or nb not in D:
            continue
        d = D["degree"] - D[na] - D[nb] + D[n]
        m, se, k, p = _t_two_sided(d)
        rows.append({"element": n, "interaction": m, "se": se, "n": k, "p": p})
    df = pd.DataFrame(rows)
    if len(df):
        df["p_holm"] = _holm_adj(df["p"].to_numpy())
        df["significant"] = df["p_holm"] <= alpha
    return df


def arch_differences(Pa: PoolArrays, Pb: PoolArrays, L: Lattice, idx, alpha) -> pd.DataFrame:
    """Paired (same clusters, same null graphs) Delta^a_S − Delta^b_S; two-sided t, Holm over elements."""
    assert np.array_equal(Pa.instances, Pb.instances)
    Da = contrasts(Pa, idx, ["empty"] + L.names, draws="mean")
    Db = contrasts(Pb, idx, ["empty"] + L.names, draws="mean")
    rows = []
    for n in ["empty"] + L.names:
        m, se, k, p = _t_two_sided(Da[n] - Db[n])
        rows.append({"element": n, "diff": m, "se": se, "n": k, "p": p})
    df = pd.DataFrame(rows)
    df["p_holm"] = _holm_adj(df["p"].to_numpy())
    df["significant"] = df["p_holm"] <= alpha
    return df


def baselines(df: pd.DataFrame, mlp: pd.DataFrame, idx) -> pd.DataFrame:
    rows = []
    for v, sub in list(df[df.variant.isin(["real", "empty"])].groupby("variant")) + [("mlp", mlp)]:
        s = sub[sub.instance.isin(idx)]
        for col in ("test_score", "test_acc"):
            x = s[col].dropna()
            rows.append({"variant": v, "metric": col, "mean": x.mean(), "se": x.std(ddof=1) / np.sqrt(len(x)),
                         "n": len(x)})
    return pd.DataFrame(rows)


def costs(df: pd.DataFrame, mlp: pd.DataFrame) -> pd.DataFrame:
    t = df.assign(gen=df.get("gen_seconds", 0).fillna(0))
    g = t.groupby("variant").agg(fit_seconds=("fit_seconds", "mean"), gen_seconds=("gen", "mean"),
                                 n_rows=("fit_seconds", "size"), valid_rate=("valid", "mean"))
    g.loc["mlp"] = [mlp["fit_seconds"].mean(), 0.0, len(mlp), 1.0]
    return g.reset_index()
