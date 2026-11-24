"""Phase 3C label-free structural attributes and calibration helpers.

The structural attributes are fixed functions of the observed graph and raw node
features.  They never receive labels, data splits, model scores, or fitted model
objects.  They are deliberately coarse: a stratum-preserving swap must retain
enough freedom to create genuinely perturbed graphs.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import svds

from .attributes import _kmeans, louvain_blocks, quantile_bins


ATTR_NAMES_3C = ("block", "fsim", "clust", "hop2")


def local_clustering_bins(g, q: int = 4) -> np.ndarray:
    """Quantile bins of the undirected local clustering coefficient."""
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(range(g.n))
    G.add_edges_from(map(tuple, g.edges.tolist()))
    cm = nx.clustering(G)
    c = np.fromiter((cm[i] for i in range(g.n)), dtype=float, count=g.n)
    return quantile_bins(c, q)


def two_hop_bins(g, q: int = 4) -> np.ndarray:
    """Quantile bins of the number of distinct nodes at graph distance exactly two."""
    nbr = [set() for _ in range(g.n)]
    for i, j in g.edges:
        nbr[int(i)].add(int(j))
        nbr[int(j)].add(int(i))
    out = np.empty(g.n, dtype=np.int64)
    for i in range(g.n):
        reach = set()
        for j in nbr[i]:
            reach.update(nbr[j])
        reach.discard(i)
        reach.difference_update(nbr[i])
        out[i] = len(reach)
    return quantile_bins(out, q)


def compute_attributes_3c(g, X_raw: sp.csr_matrix, seed: int) -> dict[str, np.ndarray]:
    """Phase 3C lattice attributes: community, feature, triangle, and two-hop structure."""
    return {
        "block": louvain_blocks(g, seed),
        # k=16 is preregistered as a finer A-X/feature-assortativity control than Phase 3B's k=8.
        "fsim": sparse_feature_clusters(X_raw, seed + 1, k=16, dim=32, restarts=10),
        "clust": local_clustering_bins(g),
        "hop2": two_hop_bins(g),
    }


def sparse_feature_clusters(X_raw: sp.csr_matrix, seed: int, k: int = 16, dim: int = 32,
                            restarts: int = 10) -> np.ndarray:
    """Spherical k-means on a deterministic sparse truncated-SVD feature embedding."""
    X = X_raw.tocsr().astype(np.float64)
    nr = np.sqrt(np.asarray(X.multiply(X).sum(1)).ravel())
    nr[nr == 0] = 1.0
    X = sp.diags(1.0 / nr) @ X
    d = min(dim, min(X.shape) - 1)
    v0 = np.random.default_rng(seed).standard_normal(min(X.shape))
    U, s, _ = svds(X, k=d, which="LM", v0=v0)
    order = np.argsort(s)[::-1]
    Z = U[:, order] * s[order]
    Z /= np.maximum(np.linalg.norm(Z, axis=1, keepdims=True), 1e-12)
    rng, best = np.random.default_rng(seed), None
    for _ in range(restarts):
        lab, inertia = _kmeans(Z, k, rng)
        if best is None or inertia < best[1] - 1e-12:
            best = (lab, inertia)
    _, lab = np.unique(best[0], return_inverse=True)
    return lab.astype(np.int64)


def feature_cosine_on_edges(g, X_raw: sp.csr_matrix) -> float:
    """Mean cosine similarity on edges; descriptive perturbation audit only."""
    X = X_raw.tocsr().astype(float)
    nr = np.sqrt(np.asarray(X.multiply(X).sum(1)).ravel())
    nr[nr == 0] = 1.0
    X = sp.diags(1.0 / nr) @ X
    a, b = g.edges[:, 0], g.edges[:, 1]
    return float(np.asarray(X[a].multiply(X[b]).sum(1)).ravel().mean()) if g.m else float("nan")
