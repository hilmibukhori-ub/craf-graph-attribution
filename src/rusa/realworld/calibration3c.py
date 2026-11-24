"""Independent Phase 3C GraphSAGE A/A calibration pool and inference audit."""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from ..craf.core import ADV, SUF, Lattice, certify, directional_p
from ..reporting.report import wilson
from ..utils.seeding import environment_info, int_seed_for, rng_for
from .data import make_split
from .models import fit_score, to_sparse_input
from .pool import audit_null, sample_null


def run_calibration_chunk(ds, node_attrs: dict, start: int, count: int, out_dir: str | Path, *, elements,
                          master_seed: int, swap_factor: float, attempt_factor: float,
                          split_kw: dict | None = None, hp: dict | None = None) -> Path:
    """Fit only the two GraphSAGE null draws needed by the preregistered A/A rerun."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ds.name}__sage_cal__{start:06d}_{start + count:06d}.csv.gz"
    meta = path.with_suffix("").with_suffix(".meta.json")
    if path.exists() and meta.exists():
        return path
    x_t = to_sparse_input(ds.X)
    rows, t_all = [], time.time()
    for r in range(start, start + count):
        split = make_split(ds.y, rng_for(master_seed, ds.name, r, "split"), **(split_kw or {}))
        mseed = int_seed_for(master_seed, ds.name, r, "model")
        for name in elements:
            for draw in (0, 1):
                key = (master_seed, ds.name, r, "null", name, draw)
                t0 = time.perf_counter()
                gp, info = sample_null(name, ds.graph, node_attrs, rng_for(*key), swap_factor, attempt_factor)
                gen_seconds = time.perf_counter() - t0
                au = audit_null(name, ds.graph, gp, node_attrs, info, key)
                base = {"scenario": ds.name, "instance": r, "variant": name, "draw": draw,
                        "valid": au.valid, "gen_seconds": gen_seconds,
                        "diag_edge_overlap": au.diagnostics.get("edge_overlap"),
                        "diag_swap_completion": au.diagnostics.get("swap_completion")}
                if not au.valid:
                    rows.append({**base, "test_score": np.nan, "fit_seconds": 0.0,
                                 "violated_hard": ";".join(au.violated_hard),
                                 "violated_soft": ";".join(au.violated_soft)})
                    continue
                t1 = time.perf_counter()
                score = fit_score("sage", ds.X, ds.y, gp, split, mseed, hp, x_t)
                rows.append({**base, **score, "fit_seconds": time.perf_counter() - t1,
                             "violated_hard": "", "violated_soft": ""})
    tmp = path.with_name(path.name + ".tmp")
    pd.DataFrame(rows).to_csv(tmp, index=False, compression="gzip")
    tmp.rename(path)
    meta.write_text(json.dumps({"dataset": ds.name, "start": start, "count": count,
                                "master_seed": master_seed, "elements": list(elements),
                                "seconds": time.time() - t_all, "env": environment_info()}, indent=1, default=str))
    return path


def aa_matrix(df: pd.DataFrame, names: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """Return sorted instance ids and draw-0 minus draw-1 matrix."""
    ids = np.sort(df.instance.unique())
    M = np.full((len(ids), len(names)), np.nan)
    loc = {int(v): i for i, v in enumerate(ids)}
    for j, name in enumerate(names):
        z = df[df.variant == name].pivot(index="instance", columns="draw", values="test_score")
        for r, row in z.iterrows():
            if 0 in row and 1 in row:
                M[loc[int(r)], j] = row[0] - row[1]
    return ids, M


def _block_rejections(M: np.ndarray, names: list[str], n: int, alpha: float, method: str = "t",
                      permutations: int = 9999, seed: int = 0) -> np.ndarray:
    """Boolean matrix (independent block, lattice element) for the sufficiency direction."""
    G = len(M) // n
    out = np.zeros((G, len(names)), dtype=bool)
    for g in range(G):
        for j, name in enumerate(names):
            x = M[g * n:(g + 1) * n, j]
            x = x[np.isfinite(x)]
            if method == "t":
                p = directional_p(x, 0.0)[SUF]
            elif method == "signflip":
                rng = rng_for(seed, "signflip", g, name)
                obs = x.mean()
                hits = 0
                left = permutations
                while left:
                    b = min(1000, left)
                    signs = rng.integers(0, 2, (b, len(x)), dtype=np.int8) * 2 - 1
                    hits += int(((signs @ x) / len(x) <= obs + 1e-15).sum())
                    left -= b
                p = (hits + 1) / (permutations + 1)
            else:
                raise ValueError(method)
            out[g, j] = p <= alpha
    return out


def _block_boot_ci(R: np.ndarray, seed: int, reps: int = 10000) -> tuple[float, float]:
    """Percentile CI resampling independent cluster blocks, preserving within-block dependence."""
    rng = np.random.default_rng(seed)
    vals = np.empty(reps)
    for b in range(reps):
        vals[b] = R[rng.integers(0, len(R), len(R))].mean()
    return tuple(map(float, np.quantile(vals, [0.025, 0.975])))


def analyze_calibration(df: pd.DataFrame, names: list[str], *, alpha: float = 0.05, n: int = 80,
                        bootstrap_reps: int = 10000, signflip_permutations: int = 9999,
                        seed: int = 3403) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    ids, M = aa_matrix(df, names)
    if not np.array_equal(ids, np.arange(len(ids))):
        raise ValueError("calibration clusters must be exactly 0..N-1")
    primary = []
    matrices = {}
    for method in ("t", "signflip"):
        R = _block_rejections(M, names, n, alpha, method, signflip_permutations, seed)
        matrices[method] = R
        k, total = int(R.sum()), int(R.size)
        lo, hi = wilson(k, total)
        blo, bhi = _block_boot_ci(R, seed + (0 if method == "t" else 1), bootstrap_reps)
        primary.append({"method": method, "n": n, "groups": R.shape[0], "elements": R.shape[1],
                        "rejections": k, "tests": total, "size": k / total,
                        "wilson_lo": lo, "wilson_hi": hi, "block_boot_lo": blo, "block_boot_hi": bhi,
                        "persistent_flag": bool(method == "t" and blo > alpha)})

    # Procedure-level FWER at the boundary; independent groups are the experimental units.
    L = Lattice.from_names(names)
    fw = []
    for g in range(len(M) // n):
        X = M[g * n:(g + 1) * n]
        pv = {name: directional_p(X[:, j] + 0.005, 0.005) for j, name in enumerate(names)}
        A, C = certify(pv, alpha, "holm")
        fw.append(bool(A or C))
    k = int(sum(fw))
    lo, hi = wilson(k, len(fw))
    fwer = pd.DataFrame([{"method": "t+Holm", "n": n, "groups": len(fw), "false_groups": k,
                          "fwer": np.mean(fw), "wilson_lo": lo, "wilson_hi": hi,
                          "persistent_flag": bool(lo > alpha)}])

    # Diagnostics do not alter the primary decision.
    flat = M[np.isfinite(M)]
    diag = {"clusters": len(M), "complete_clusters": int(np.isfinite(M).all(1).sum()),
            "mean": float(flat.mean()), "sd": float(flat.std(ddof=1)),
            "skew": float(stats.skew(flat)), "excess_kurtosis": float(stats.kurtosis(flat)),
            "q001": float(np.quantile(flat, .001)), "q999": float(np.quantile(flat, .999)),
            "mean_cross_element_correlation": float(np.nanmean((np.corrcoef(M, rowvar=False) - np.eye(len(names))))),
            "primary_cell": "GraphSAGE n=80 sufficiency direction alpha=0.05",
            "decision_uses": "block bootstrap lower bound; Wilson interval is descriptive"}
    return pd.DataFrame(primary), fwer, diag

