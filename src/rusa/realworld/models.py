"""Multi-class GCN / GraphSAGE / MLP for the real-world pilot (plain PyTorch, CPU).

Matched controls (as in ``rusa.models.gnn``):
* ``graph=None`` with arch gcn/sage gives the matched **no-graph** model: same parameters,
  initialisation and training, identity (GCN) or zero (SAGE) neighbour operator;
* arch ``mlp`` is the **feature-only** baseline.

Inputs may be passed as a sparse COO tensor (``to_sparse_input``); the first layer then uses one
sparse-dense product and dropout acts on the stored entries. This is the same model (dropping a
zero entry changes nothing) and is ~10-50x faster on bag-of-words features.

Training protocol (fixed a priori; standard Kipf & Welling settings): full batch, Adam lr 0.01,
weight decay 5e-4, hidden 64, dropout 0.5 on input and hidden, at most 300 epochs, early stopping
on validation cross-entropy with patience 50, restore the best weights.

Score: S = 1 − Brier/2, where Brier = mean_i sum_k (p_ik − 1[y_i = k])^2, so S ∈ [0, 1] (higher is
better). Test accuracy is recorded as a secondary metric. Test labels are read only after the
restored model is frozen.
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from ..models.gnn import gcn_operator, mean_operator
from ..nulls.generators import Graph

HP = dict(hidden=64, lr=0.01, weight_decay=5e-4, dropout=0.5, max_epochs=300, patience=50)


def _drop(x, p, training):
    """Dropout that also works on a sparse COO input (drops stored entries; zeros stay zero)."""
    if not x.is_sparse:
        return nn.functional.dropout(x, p, training)
    if not training or p == 0:
        return x
    v = x._values()
    keep = (torch.rand_like(v) >= p).to(v.dtype) / (1 - p)
    return torch.sparse_coo_tensor(x._indices(), v * keep, x.shape)


def _lin(layer, x):
    """layer(x) for dense or sparse x (sparse: one sparse-dense product, same parameters)."""
    if not x.is_sparse:
        return layer(x)
    out = torch.sparse.mm(x, layer.weight.t())
    return out if layer.bias is None else out + layer.bias


def to_sparse_input(X: np.ndarray) -> torch.Tensor:
    import scipy.sparse as sp

    C = sp.coo_matrix(X)
    idx = torch.from_numpy(np.stack([C.row, C.col]).astype(np.int64))
    return torch.sparse_coo_tensor(idx, torch.from_numpy(C.data.astype(np.float32)), X.shape).coalesce()


class GCNc(nn.Module):
    def __init__(self, d_in, n_cls, hidden, dropout):
        super().__init__()
        self.l1, self.l2, self.p = nn.Linear(d_in, hidden), nn.Linear(hidden, n_cls), dropout

    def forward(self, x, op):
        x = _drop(x, self.p, self.training)
        h = torch.relu(torch.sparse.mm(op, _lin(self.l1, x)))
        h = nn.functional.dropout(h, self.p, self.training)
        return torch.sparse.mm(op, self.l2(h))


class SAGEc(nn.Module):
    def __init__(self, d_in, n_cls, hidden, dropout):
        super().__init__()
        self.s1, self.n1 = nn.Linear(d_in, hidden), nn.Linear(d_in, hidden, bias=False)
        self.s2, self.n2 = nn.Linear(hidden, n_cls), nn.Linear(hidden, n_cls, bias=False)
        self.p = dropout

    def forward(self, x, op):
        x = _drop(x, self.p, self.training)
        h = torch.relu(_lin(self.s1, x) + torch.sparse.mm(op, _lin(self.n1, x)))   # n1(op x) = op (x W_n)
        h = nn.functional.dropout(h, self.p, self.training)
        return self.s2(h) + self.n2(torch.sparse.mm(op, h))


class MLPc(nn.Module):
    def __init__(self, d_in, n_cls, hidden, dropout):
        super().__init__()
        self.l1, self.l2, self.p = nn.Linear(d_in, hidden), nn.Linear(hidden, n_cls), dropout

    def forward(self, x, op=None):
        x = _drop(x, self.p, self.training)
        h = nn.functional.dropout(torch.relu(_lin(self.l1, x)), self.p, self.training)
        return self.l2(h)


ARCHS = {"gcn": (GCNc, gcn_operator), "sage": (SAGEc, mean_operator), "mlp": (MLPc, None)}


def _scores(p: np.ndarray, y: np.ndarray, idx: np.ndarray) -> tuple[float, float]:
    P = p[idx]
    Y = np.zeros_like(P)
    Y[np.arange(len(idx)), y[idx]] = 1.0
    return 1.0 - 0.5 * float(np.mean(((P - Y) ** 2).sum(1))), float(np.mean(P.argmax(1) == y[idx]))


def fit_score(arch: str, X: np.ndarray, y: np.ndarray, g: Graph | None, split: dict, seed: int, hp: dict | None = None,
              x_t: torch.Tensor | None = None) -> dict:
    hp = {**HP, **(hp or {})}
    torch.set_num_threads(1)
    cls, op_fn = ARCHS[arch]
    x = torch.from_numpy(X) if x_t is None else x_t
    yt = torch.from_numpy(y)
    tr, va = (torch.from_numpy(split[k]).long() for k in ("train", "val"))
    op = op_fn(g, X.shape[0]) if op_fn else None
    torch.manual_seed(seed)
    model = cls(X.shape[1], int(y.max()) + 1, hp["hidden"], hp["dropout"])
    opt = torch.optim.Adam(model.parameters(), lr=hp["lr"], weight_decay=hp["weight_decay"])
    lossf = nn.CrossEntropyLoss()
    best, best_state, bad, best_epoch = np.inf, None, 0, -1
    for epoch in range(hp["max_epochs"]):
        model.train()
        opt.zero_grad()
        loss = lossf(model(x, op)[tr], yt[tr])
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
            if bad >= hp["patience"]:
                break
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        p = torch.softmax(model(x, op), 1).numpy().astype(np.float64)
    vs, vacc = _scores(p, y, split["val"])
    ts, tacc = _scores(p, y, split["test"])          # test labels read only here, after freezing
    return {"val_score": vs, "test_score": ts, "val_acc": vacc, "test_acc": tacc,
            "best_epoch": best_epoch, "epochs_run": epoch + 1}
