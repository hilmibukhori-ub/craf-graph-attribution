"""Matched message-passing models in plain PyTorch (no PyTorch Geometric dependency).

PyG is unavailable on the target cluster, so the two standard layers are written out:

* GCN (Kipf & Welling, 2017):  H' = A_hat H W,  A_hat = D^{-1/2}(A+I)D^{-1/2}
* GraphSAGE-mean (Hamilton et al., 2017):  H' = H W_self + mean_{N(i)}(H) W_nbr

Matched no-relation control: ``graph=None`` gives A_hat = I (GCN) / a zero neighbour
operator (SAGE) with the *same* parameters, initialisation and minibatch order, so the
empty-graph model differs only in the graph.  ``MLP`` is the feature-only baseline.

Training protocol A (fixed): full-batch Adam, lr 0.01, weight decay 5e-4, dropout 0.5,
hidden 32, max 300 epochs, early stopping on validation BCE (patience 30), restore best
weights; score = 1 - Brier on val/test of the restored model.  Seeds are paired across
graph variants by the caller.  CPU execution with ``torch.use_deterministic_algorithms``;
residual nondeterminism in sparse matmul across platforms is at round-off level.
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from ..nulls.generators import Graph


def _sparse(indices: np.ndarray, values: np.ndarray, n: int) -> torch.Tensor:
    return torch.sparse_coo_tensor(
        torch.from_numpy(indices).long(), torch.from_numpy(values).float(), (n, n)
    ).coalesce()


def gcn_operator(g: Graph | None, n: int) -> torch.Tensor:
    if g is None:
        idx = np.stack([np.arange(n), np.arange(n)])
        return _sparse(idx, np.ones(n), n)
    ei = g.edge_index()
    loops = np.stack([np.arange(n), np.arange(n)])
    ei = np.concatenate([ei, loops], 1)
    deg = np.bincount(ei[0], minlength=n).astype(float)
    w = 1.0 / np.sqrt(deg[ei[0]] * deg[ei[1]])
    return _sparse(ei, w, n)


def mean_operator(g: Graph | None, n: int) -> torch.Tensor:
    if g is None or g.m == 0:
        return _sparse(np.zeros((2, 0), dtype=np.int64), np.zeros(0), n)
    ei = g.edge_index()
    deg = np.bincount(ei[0], minlength=n).astype(float)
    return _sparse(ei, 1.0 / deg[ei[0]], n)


class GCN(nn.Module):
    def __init__(self, d_in, hidden=32, dropout=0.5):
        super().__init__()
        self.l1 = nn.Linear(d_in, hidden)
        self.l2 = nn.Linear(hidden, 1)
        self.dropout = dropout

    def forward(self, x, op):
        h = torch.relu(torch.sparse.mm(op, self.l1(x)))
        h = nn.functional.dropout(h, self.dropout, self.training)
        return torch.sparse.mm(op, self.l2(h)).squeeze(-1)


class SAGE(nn.Module):
    def __init__(self, d_in, hidden=32, dropout=0.5):
        super().__init__()
        self.s1, self.n1 = nn.Linear(d_in, hidden), nn.Linear(d_in, hidden, bias=False)
        self.s2, self.n2 = nn.Linear(hidden, 1), nn.Linear(hidden, 1, bias=False)
        self.dropout = dropout

    def forward(self, x, op):
        h = torch.relu(self.s1(x) + self.n1(torch.sparse.mm(op, x)))
        h = nn.functional.dropout(h, self.dropout, self.training)
        return (self.s2(h) + self.n2(torch.sparse.mm(op, h))).squeeze(-1)


class MLP(nn.Module):
    def __init__(self, d_in, hidden=32, dropout=0.5):
        super().__init__()
        self.l1, self.l2 = nn.Linear(d_in, hidden), nn.Linear(hidden, 1)
        self.dropout = dropout

    def forward(self, x, op=None):
        h = nn.functional.dropout(torch.relu(self.l1(x)), self.dropout, self.training)
        return self.l2(h).squeeze(-1)


ARCH = {"gcn": (GCN, gcn_operator), "sage": (SAGE, mean_operator), "mlp": (MLP, None)}


class TorchNodeModel:
    stochastic = True

    def __init__(self, arch="gcn", hidden=32, lr=0.01, weight_decay=5e-4, dropout=0.5,
                 max_epochs=300, patience=30):
        if arch not in ARCH:
            raise ValueError(arch)
        self.arch, self.name = arch, arch
        self.hp = dict(hidden=hidden, lr=lr, weight_decay=weight_decay, dropout=dropout,
                       max_epochs=max_epochs, patience=patience)

    def fit_score(self, F: np.ndarray, y: np.ndarray, g: Graph | None, split: dict, seed: int = 0) -> dict:
        torch.set_num_threads(1)
        cls, op_fn = ARCH[self.arch]
        tr, va, te = (torch.from_numpy(split[k]).long() for k in ("train", "val", "test"))
        mu, sd = F[split["train"]].mean(0), F[split["train"]].std(0)
        sd[sd < 1e-10] = 1.0
        x = torch.from_numpy((F - mu) / sd).float()
        yt = torch.from_numpy(y).float()
        op = op_fn(g, F.shape[0]) if op_fn else None
        torch.manual_seed(seed)
        model = cls(F.shape[1], self.hp["hidden"], self.hp["dropout"])
        opt = torch.optim.Adam(model.parameters(), lr=self.hp["lr"], weight_decay=self.hp["weight_decay"])
        lossf = nn.BCEWithLogitsLoss()
        best, best_state, bad, best_epoch = np.inf, None, 0, -1
        for epoch in range(self.hp["max_epochs"]):
            model.train()
            opt.zero_grad()
            out = model(x, op)
            loss = lossf(out[tr], yt[tr])
            loss.backward()
            opt.step()
            model.eval()
            with torch.no_grad():
                vl = float(lossf(model(x, op)[va], yt[va]))
            if vl < best - 1e-6:
                best, bad, best_epoch = vl, 0, epoch
                best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
            else:
                bad += 1
                if bad >= self.hp["patience"]:
                    break
        model.load_state_dict(best_state)
        model.eval()
        with torch.no_grad():
            p = torch.sigmoid(model(x, op)).numpy()
        return {
            "val_score": 1.0 - float(np.mean((p[split["val"]] - y[split["val"]]) ** 2)),
            "test_score": 1.0 - float(np.mean((p[split["test"]] - y[split["test"]]) ** 2)),
            "best_epoch": best_epoch,
            "epochs_run": epoch + 1,
            "n_params": int(sum(p_.numel() for p_ in model.parameters())),
        }


def make_model(name: str):
    from .baselines import FeatureOnlyRidge, SGCRidge

    if name == "sgc_ridge":
        return SGCRidge()
    if name == "feature_ridge":
        return FeatureOnlyRidge()
    if name in ARCH:
        return TorchNodeModel(name)
    raise ValueError(f"unknown model {name!r}")
