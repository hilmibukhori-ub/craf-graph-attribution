"""Closed-form matched models (fast; used for Monte Carlo calibration).

``SGCRidge``: Simplified Graph Convolution (Wu et al., 2019) features
[F, A_hat F, A_hat^2 F] with A_hat = D^{-1/2}(A + I)D^{-1/2}, followed by a ridge
linear-probability model.  Probabilities are clipped to [0, 1]; the score is
S = 1 - Brier, which is bounded in [0, 1] (needed for bounded-outcome certificates).

Matched no-relation control (as in PCGA): ``graph=None`` keeps the *same* column layout
with both propagated channels set to exactly zero, so the empty-graph model has identical
capacity and tuning protocol.

Tuning protocol A (fixed, fully specified): standardise columns on training nodes; select
ridge alpha from a fixed grid by validation Brier; report validation and test scores of the
selected fit.  Test labels are never read before the selected model is frozen.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from ..nulls.generators import Graph

ALPHA_GRID = (0.1, 1.0, 10.0, 100.0, 1000.0)


def normalized_adjacency(g: Graph):
    A = g.adjacency_csr() + sp.eye(g.n, format="csr")
    d = np.asarray(A.sum(1)).ravel()
    dinv = sp.diags(1.0 / np.sqrt(d))
    return (dinv @ A @ dinv).tocsr()


def sgc_features(F: np.ndarray, g: Graph | None, hops: int = 2) -> np.ndarray:
    if g is None:
        return np.concatenate([F] + [np.zeros_like(F)] * hops, 1)
    Ah = normalized_adjacency(g)
    out, cur = [F], F
    for _ in range(hops):
        cur = Ah @ cur
        out.append(cur)
    return np.concatenate(out, 1)


def brier_score(p: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((np.clip(p, 0.0, 1.0) - y) ** 2))


def ridge_path_fit(X: np.ndarray, y: np.ndarray, split: dict, alphas=ALPHA_GRID) -> dict:
    """Fit ridge for every alpha on train via one eigendecomposition; select by val Brier."""
    tr, va, te = split["train"], split["val"], split["test"]
    mu = X[tr].mean(0)
    sd = X[tr].std(0)
    sd[sd < 1e-10] = 1.0
    Z = (X - mu) / sd
    Z[:, X[tr].std(0) < 1e-10] = 0.0          # constant / zeroed channels carry no signal
    Ztr = Z[tr]
    ytr = y[tr].astype(float)
    ym = ytr.mean()
    evals, evecs = np.linalg.eigh(Ztr.T @ Ztr)
    proj = evecs.T @ (Ztr.T @ (ytr - ym))
    best = None
    for a in alphas:
        beta = evecs @ (proj / (evals + a))
        pv = Z[va] @ beta + ym
        bv = brier_score(pv, y[va])
        if best is None or bv < best[0] - 1e-15:
            best = (bv, a, beta)
    bv, a, beta = best
    p_te = Z[te] @ beta + ym                    # test predictions only after selection
    return {
        "alpha": a,
        "val_score": 1.0 - bv,
        "test_score": 1.0 - brier_score(p_te, y[te]),
        "n_params": int(Z.shape[1] + 1),
    }


class SGCRidge:
    name = "sgc_ridge"
    stochastic = False

    def __init__(self, hops: int = 2, alphas=ALPHA_GRID):
        self.hops = hops
        self.alphas = alphas

    def fit_score(self, F: np.ndarray, y: np.ndarray, g: Graph | None, split: dict, seed: int = 0) -> dict:
        X = sgc_features(F, g, self.hops)
        return ridge_path_fit(X, y, split, self.alphas)


class FeatureOnlyRidge:
    """Strong feature-only baseline (no graph channels at all)."""

    name = "feature_ridge"
    stochastic = False

    def __init__(self, alphas=ALPHA_GRID):
        self.alphas = alphas

    def fit_score(self, F, y, g, split, seed: int = 0) -> dict:
        return ridge_path_fit(F, y, split, self.alphas)
