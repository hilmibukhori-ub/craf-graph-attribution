"""Label-free node attributes that define the CRAF property lattice on real graphs.

Every function here takes only the observed graph G0 and/or the raw features; none receives
labels, splits or scores (checked by ``tests/test_phase3b.py``). They are computed once per
dataset with fixed seeds and frozen before any model is fitted.

| attribute | definition | null N_{attr} preserves (on top of degrees) |
|-----------|------------|---------------------------------------------|
| deg   | degree quartile bin (4 bins, ties kept together) | each node's neighbour counts per degree bin (degree-degree mixing) |
| block | Louvain communities of G0 (networkx, resolution 1, fixed seed); the 7 largest kept, the rest merged into one 'other' stratum | each node's neighbour counts per community (mesoscale / SBM-like structure); plays the role of PCGA-L's 'block' |
| feat  | spherical k-means (k = 8, 10 restarts, fixed seed) on the top-32 SVD components of the L2-normalised raw features | each node's neighbour counts per feature cluster (feature homophily) |
| dlen  | quartile bin of the number of non-zero raw features (document length) | each node's neighbour counts per length bin (a plausibly irrelevant property) |

Attributes are label-free but may be label-*correlated* (feature clusters and communities usually
are). That is intended: the scientific question is whether preserving such label-free structure
reproduces the real graph's performance.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from ..nulls.generators import Graph

ATTR_NAMES = ("deg", "block", "feat", "dlen")


def quantile_bins(v: np.ndarray, q: int = 4) -> np.ndarray:
    v = np.asarray(v, float)
    cuts = np.unique(np.quantile(v, np.linspace(0, 1, q + 1)[1:-1]))
    b = np.digitize(v, cuts, right=True)
    _, b = np.unique(b, return_inverse=True)
    return b.astype(np.int64)


def degree_bins(g: Graph, q: int = 4) -> np.ndarray:
    return quantile_bins(g.degrees(), q)


def doc_length_bins(X_raw: sp.csr_matrix, q: int = 4) -> np.ndarray:
    return quantile_bins(np.diff(X_raw.tocsr().indptr), q)


def louvain_blocks(g: Graph, seed: int, keep: int = 7, resolution: float = 1.0) -> np.ndarray:
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(range(g.n))
    G.add_edges_from(map(tuple, g.edges.tolist()))
    comms = nx.community.louvain_communities(G, resolution=resolution, seed=seed)
    comms = sorted((sorted(c) for c in comms), key=lambda c: (-len(c), c[0]))
    lab = np.full(g.n, keep, dtype=np.int64)
    for i, c in enumerate(comms[:keep]):
        lab[c] = i
    _, lab = np.unique(lab, return_inverse=True)
    return lab.astype(np.int64)


def _kmeans(Z: np.ndarray, k: int, rng: np.random.Generator, iters: int = 100) -> tuple[np.ndarray, float]:
    n = len(Z)
    cent = [Z[rng.integers(n)]]
    d2 = ((Z - cent[0]) ** 2).sum(1)
    for _ in range(1, k):                       # k-means++ initialisation
        p = d2 / d2.sum() if d2.sum() > 0 else np.full(n, 1 / n)
        cent.append(Z[rng.choice(n, p=p)])
        d2 = np.minimum(d2, ((Z - cent[-1]) ** 2).sum(1))
    C = np.array(cent)
    lab = np.zeros(n, dtype=np.int64)
    for _ in range(iters):
        D = (Z ** 2).sum(1)[:, None] - 2 * Z @ C.T + (C ** 2).sum(1)[None]
        new = D.argmin(1)
        if _ > 0 and np.array_equal(new, lab):
            break
        lab = new
        for j in range(k):
            if (lab == j).any():
                C[j] = Z[lab == j].mean(0)
    D = (Z ** 2).sum(1)[:, None] - 2 * Z @ C.T + (C ** 2).sum(1)[None]
    return lab, float(D[np.arange(n), lab].sum())


def feature_clusters(X_raw: sp.csr_matrix, seed: int, k: int = 8, dim: int = 32, restarts: int = 10) -> np.ndarray:
    Xd = X_raw.toarray().astype(np.float64)
    nr = np.linalg.norm(Xd, axis=1)
    nr[nr == 0] = 1.0
    Xd /= nr[:, None]
    U, s, _ = np.linalg.svd(Xd - Xd.mean(0), full_matrices=False)
    Z = U[:, :dim] * s[:dim]
    Z /= np.maximum(np.linalg.norm(Z, axis=1, keepdims=True), 1e-12)   # spherical
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(restarts):
        lab, inertia = _kmeans(Z, k, rng)
        if best is None or inertia < best[1] - 1e-12:
            best = (lab, inertia)
    _, lab = np.unique(best[0], return_inverse=True)
    return lab.astype(np.int64)


def compute_attributes(g: Graph, X_raw: sp.csr_matrix, seed: int) -> dict:
    """All lattice attributes. Inputs are G0 and raw features only (label-free by construction)."""
    return {"deg": degree_bins(g), "block": louvain_blocks(g, seed), "feat": feature_clusters(X_raw, seed),
            "dlen": doc_length_bins(X_raw)}
