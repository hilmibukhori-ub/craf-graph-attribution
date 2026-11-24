"""Real-world node-classification datasets (fixed graph) and per-cluster random splits.

Datasets are read from the npz files of Shchur et al. (2018, gnn-benchmark) with
``allow_pickle=False``; only numeric arrays are touched (object arrays such as node names are
never loaded). The graph is symmetrised, self-loops and duplicate edges are removed, and the
features are L1 row-normalised (label-free, per node).

Fixed-graph estimand: G0, X and y are fixed. A *replicate cluster* r draws a fresh
class-stratified split (``n_train`` / ``n_val`` per class, rest test), a fresh training seed and
fresh null draws. Clusters are i.i.d. given (G0, X, y).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy.sparse as sp

from ..nulls.generators import Graph


@dataclass
class RealDataset:
    name: str
    graph: Graph
    X: np.ndarray          # float32, L1 row-normalised features (model input)
    X_raw: sp.csr_matrix   # raw (binary / count) features, used only for label-free attributes
    y: np.ndarray          # int64 class labels
    n_classes: int

    @property
    def n(self) -> int:
        return self.graph.n


def _csr(z, prefix):
    return sp.csr_matrix((z[f"{prefix}_data"], z[f"{prefix}_indices"], z[f"{prefix}_indptr"]),
                         shape=tuple(z[f"{prefix}_shape"]))


def load_npz_dataset(path: str | Path, name: str | None = None) -> RealDataset:
    z = np.load(path, allow_pickle=False)
    if "node_features" in z.files:
        return _load_platonov(z, name or Path(path).stem)
    A = _csr(z, "adj").tocoo()
    n = A.shape[0]
    e = np.stack([A.row, A.col], 1).astype(np.int64)
    e = e[e[:, 0] != e[:, 1]]
    g = Graph.from_edges(n, e)                     # symmetrise (i<j) and deduplicate
    Xr = _csr(z, "attr").astype(np.float64)
    Xr.sum_duplicates()
    rs = np.asarray(Xr.sum(1)).ravel()
    rs[rs == 0] = 1.0
    X = (sp.diags(1.0 / rs) @ Xr).toarray().astype(np.float32)
    y = np.asarray(z["labels"]).astype(np.int64)
    return RealDataset(name or Path(path).stem, g, X, Xr.tocsr(), y, int(y.max()) + 1)


def _load_platonov(z, name: str) -> RealDataset:
    """Heterophilous benchmark npz of Platonov et al. (2023): dense ``node_features``, ``edges``,
    ``node_labels``. The provided fixed split masks are ignored (each replicate cluster draws its
    own split). Features are dense real-valued embeddings and are used as provided (no L1
    normalisation, which is undefined for signed features); edges are symmetrised and deduplicated.
    """
    Xd = np.asarray(z["node_features"], dtype=np.float32)
    n = Xd.shape[0]
    e = np.asarray(z["edges"], dtype=np.int64)
    e = e[e[:, 0] != e[:, 1]]
    g = Graph.from_edges(n, e)
    y = np.asarray(z["node_labels"]).astype(np.int64)
    return RealDataset(name, g, Xd, sp.csr_matrix(Xd.astype(np.float64)), y, int(y.max()) + 1)


def make_split(y: np.ndarray, rng: np.random.Generator, n_train: int = 20, n_val: int = 30,
               train_frac: float | None = None, val_frac: float | None = None) -> dict:
    """Class-stratified random split, every node not in train/val is test.

    Default: ``n_train`` and ``n_val`` nodes per class. If ``train_frac``/``val_frac`` are given,
    each class contributes ``round(frac * class size)`` nodes instead (Phase 3E, 50/25/25).
    """
    tr, va = [], []
    for c in np.unique(y):
        idx = rng.permutation(np.flatnonzero(y == c))
        if train_frac is not None:
            k_tr = int(round(train_frac * len(idx)))
            k_va = int(round(val_frac * len(idx)))
            if len(idx) >= 3:                     # keep >= 1 node of the class in each part
                k_tr = min(max(k_tr, 1), len(idx) - 2)
                k_va = min(max(k_va, 1), len(idx) - k_tr - 1)
            tr.append(idx[:k_tr])
            va.append(idx[k_tr:k_tr + k_va])
            continue
        k_tr = min(n_train, len(idx) // 3)
        k_va = min(n_val, (len(idx) - k_tr) // 2)
        tr.append(idx[:k_tr])
        va.append(idx[k_tr:k_tr + k_va])
    tr, va = np.sort(np.concatenate(tr)), np.sort(np.concatenate(va))
    te = np.setdiff1d(np.arange(len(y)), np.concatenate([tr, va]))
    return {"train": tr, "val": va, "test": te}
