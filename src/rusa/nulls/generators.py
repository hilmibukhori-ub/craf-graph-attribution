"""Graph null-model (placebo) generators.

Every generator is a *label-free* function ``(graph, node_attrs, rng) -> (graph, info)``.
Generators never receive labels, splits or scores, which is what makes them safe to apply
before confirmatory evaluation (see ``tests/test_no_leakage.py``).

Implemented families (all on simple graphs; undirected unless stated):

* ``er``            G(n, m): uniform simple graph with the observed node and edge count.
* ``degree``        double-edge-swap MCMC preserving every node's degree (Maslov--Sneppen).
* ``strat:<a,b>``   double-edge swaps that additionally preserve, for every node, the number
                    of neighbours in each stratum defined by node attributes ``a`` (x ``b``).
                    With ``strat:block`` this is the PCGA-L L3 control.
* ``perm:<a>``      node relabelling within strata of attribute ``a`` (PCGA's within-industry
                    permutation placebo).  Preserves the graph up to isomorphism.
* ``directed_degree`` directed double-edge swaps preserving in- and out-degree.

Swap chains can run in two modes:

* ``chain="forward"``: start each placebo at the observed graph G0 (what PCGA-L did).
  Placebos are then *descendants* of G0; G0 and the placebos are not exchangeable, so a
  rank test against them is not exact (it is approximately valid if the chain mixes).
* ``chain="besag_clifford"``: the parallel construction of Besag & Clifford (1989).  Run
  the (reversible) chain ``t`` steps from G0 to a hub G*, then draw every placebo ``t`` steps
  forward from G* independently.  If G0 is a draw from the chain's stationary law on its
  communicating class, then (G0, placebos) are exchangeable and the rank test is exact.

Swap targets are *verified*: ``info["achieved_swaps"]`` is reported and the admissibility
audit rejects samples that fall short, rather than silently returning a barely-mixed graph.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# ----------------------------------------------------------------------------- graph container
@dataclass(frozen=True)
class Graph:
    """Simple graph on nodes 0..n-1.  Undirected edges are stored once with i < j."""

    n: int
    edges: np.ndarray  # shape (m, 2), int64
    directed: bool = False

    def __post_init__(self):
        e = np.asarray(self.edges, dtype=np.int64).reshape(-1, 2)
        object.__setattr__(self, "edges", e)

    @property
    def m(self) -> int:
        return int(self.edges.shape[0])

    @staticmethod
    def from_edges(n: int, edges, directed: bool = False) -> "Graph":
        e = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
        if not directed:
            e = np.sort(e, axis=1)
        if len(e):
            e = np.unique(e, axis=0)
        return Graph(n=n, edges=e, directed=directed)

    def degrees(self) -> np.ndarray:
        if self.directed:
            raise ValueError("use in_degrees/out_degrees for directed graphs")
        return np.bincount(self.edges.ravel(), minlength=self.n)

    def out_degrees(self) -> np.ndarray:
        return np.bincount(self.edges[:, 0], minlength=self.n)

    def in_degrees(self) -> np.ndarray:
        return np.bincount(self.edges[:, 1], minlength=self.n)

    def edge_keys(self) -> np.ndarray:
        """Integer key per edge (i*n+j); undirected edges use canonical i<j."""
        e = self.edges if self.directed else np.sort(self.edges, axis=1)
        return e[:, 0] * self.n + e[:, 1]

    def adjacency_csr(self):
        import scipy.sparse as sp

        r, c = self.edges[:, 0], self.edges[:, 1]
        if not self.directed:
            r, c = np.concatenate([r, c]), np.concatenate([c, r])
        data = np.ones(len(r), dtype=np.float64)
        return sp.csr_matrix((data, (r, c)), shape=(self.n, self.n))

    def edge_index(self) -> np.ndarray:
        """PyG-style (2, E) array; undirected edges appear in both directions."""
        r, c = self.edges[:, 0], self.edges[:, 1]
        if not self.directed:
            r, c = np.concatenate([r, c]), np.concatenate([c, r])
        return np.stack([r, c])


def edge_overlap(g: Graph, h: Graph) -> float:
    """Fraction of g's edges also present in h (= Jaccard-type overlap at equal m)."""
    if g.m == 0:
        return 0.0
    return float(np.isin(g.edge_keys(), h.edge_keys()).sum() / g.m)


def stratum_codes(node_attrs: dict[str, np.ndarray], keys: tuple[str, ...], n: int) -> np.ndarray:
    """Joint stratum id per node for the attribute tuple ``keys`` (empty tuple -> all zeros)."""
    if not keys:
        return np.zeros(n, dtype=np.int64)
    code = np.zeros(n, dtype=np.int64)
    for k in keys:
        if k not in node_attrs:
            raise KeyError(f"node attribute {k!r} not available for stratification")
        a = np.asarray(node_attrs[k])
        _, inv = np.unique(a, return_inverse=True)
        code = code * (int(inv.max()) + 1) + inv
    _, code = np.unique(code, return_inverse=True)
    return code.astype(np.int64)


def neighbour_stratum_counts(g: Graph, strata: np.ndarray) -> np.ndarray:
    """(n, n_strata) matrix: number of neighbours of each node in each stratum."""
    k = int(strata.max()) + 1 if len(strata) else 1
    out = np.zeros((g.n, k), dtype=np.int64)
    a, b = g.edges[:, 0], g.edges[:, 1]
    np.add.at(out, (a, strata[b]), 1)
    if not g.directed:
        np.add.at(out, (b, strata[a]), 1)
    return out


# ----------------------------------------------------------------------------- generators
def erdos_renyi_gnm(g: Graph, rng: np.random.Generator) -> tuple[Graph, dict]:
    """Uniform simple undirected graph with the same n and m (no self-loops/duplicates)."""
    if g.directed:
        raise NotImplementedError("directed G(n,m) not implemented")
    n, m = g.n, g.m
    total = n * (n - 1) // 2
    if m > total:
        raise ValueError("edge count exceeds simple-graph capacity")
    idx = rng.choice(total, size=m, replace=False)
    # map linear index of the strict upper triangle to (i, j)
    i = (n - 2 - np.floor(np.sqrt(-8 * idx + 4 * n * (n - 1) - 7) / 2.0 - 0.5)).astype(np.int64)
    j = (idx + i + 1 - n * (n - 1) // 2 + (n - i) * ((n - i) - 1) // 2).astype(np.int64)
    return Graph.from_edges(n, np.stack([i, j], 1)), {"method": "gnm"}


def _swap_kernel_py(E, adj, strata, use_strata, picks, flips, n_swaps, done, max_attempts, attempts):
    """Process one chunk of pre-drawn proposals (pure Python reference implementation)."""
    for t in range(picks.shape[0]):
        if done >= n_swaps or attempts >= max_attempts:
            break
        attempts += 1
        e1 = picks[t, 0]
        e2 = picks[t, 1]
        if e1 == e2:
            continue
        a = E[e1, 0]
        b = E[e1, 1]
        c = E[e2, 0]
        d = E[e2, 1]
        if flips[t]:
            c, d = d, c
        if a == b or a == c or a == d or b == c or b == d or c == d:
            continue
        if use_strata and (strata[a] != strata[c] or strata[b] != strata[d]):
            continue
        if adj[a, d] or adj[c, b]:
            continue
        adj[a, b] = False
        adj[b, a] = False
        adj[c, d] = False
        adj[d, c] = False
        adj[a, d] = True
        adj[d, a] = True
        adj[c, b] = True
        adj[b, c] = True
        E[e1, 0] = a
        E[e1, 1] = d
        E[e2, 0] = c
        E[e2, 1] = b
        done += 1
    return done, attempts


try:  # optional acceleration; results are bit-identical to the Python reference
    import numba as _nb

    _swap_kernel_nb = _nb.njit(cache=True)(_swap_kernel_py)
    HAVE_NUMBA = True
except Exception:  # pragma: no cover
    _swap_kernel_nb = None
    HAVE_NUMBA = False

_USE_NUMBA = HAVE_NUMBA


def set_numba(enabled: bool) -> None:
    """Toggle the numba kernel (used by tests to verify identical outputs)."""
    global _USE_NUMBA
    _USE_NUMBA = bool(enabled) and HAVE_NUMBA


def _swap_chain(
    edges: np.ndarray,
    n: int,
    n_swaps: int,
    rng: np.random.Generator,
    strata: np.ndarray | None,
    max_attempts: int,
    chunk: int = 8192,
) -> tuple[np.ndarray, int, int]:
    """Undirected double-edge-swap chain with optional neighbour-stratum preservation.

    Proposal: choose an ordered pair of edge slots uniformly (i.i.d.) and an orientation
    coin; (a,b),(c,d) -> (a,d),(c,b).  The proposal is symmetric and every valid move is
    accepted, so the chain is reversible with uniform stationary law on its communicating
    class.  With ``strata`` a move is valid only if strata[a]==strata[c] and
    strata[b]==strata[d], which preserves every node's per-stratum neighbour counts.
    Random numbers are drawn in fixed-size chunks from ``rng`` so the result is a
    deterministic function of the rng state, whichever kernel is used.
    """
    E = np.array(edges, dtype=np.int64).reshape(-1, 2).copy()
    m = len(E)
    if m < 2 or n_swaps <= 0:
        return E, 0, 0
    adj = np.zeros((n, n), dtype=np.bool_)
    adj[E[:, 0], E[:, 1]] = True
    adj[E[:, 1], E[:, 0]] = True
    use_strata = strata is not None
    s = np.asarray(strata if use_strata else np.zeros(n), dtype=np.int64)
    kernel = _swap_kernel_nb if _USE_NUMBA else _swap_kernel_py
    done = attempts = 0
    while done < n_swaps and attempts < max_attempts:
        picks = rng.integers(0, m, size=(chunk, 2))
        flips = rng.random(chunk) < 0.5
        done, attempts = kernel(E, adj, s, use_strata, picks, flips, n_swaps, done, max_attempts, attempts)
    return E, int(done), int(attempts)


def _directed_swap_chain(edges, n, n_swaps, rng, max_attempts):
    """Directed swaps (a->b),(c->d) -> (a->d),(c->b): preserves in- and out-degrees."""
    E = [(int(a), int(b)) for a, b in edges]
    m = len(E)
    present = {a * n + b for a, b in E}
    done = attempts = 0
    while done < n_swaps and attempts < max_attempts and m >= 2:
        picks = rng.integers(0, m, size=(4096, 2))
        for e1, e2 in picks:
            if done >= n_swaps or attempts >= max_attempts:
                break
            attempts += 1
            if e1 == e2:
                continue
            a, b = E[e1]
            c, d = E[e2]
            if a == d or c == b or a == c or b == d:
                continue
            if (a * n + d) in present or (c * n + b) in present:
                continue
            present.discard(a * n + b)
            present.discard(c * n + d)
            present.add(a * n + d)
            present.add(c * n + b)
            E[e1] = (a, d)
            E[e2] = (c, b)
            done += 1
    return np.asarray(E, dtype=np.int64).reshape(-1, 2), done, attempts


def swap_null(
    g: Graph,
    rng: np.random.Generator,
    *,
    strata: np.ndarray | None = None,
    swap_factor: float = 5.0,
    attempt_factor: float = 60.0,
    chain: str = "forward",
    hub: Graph | None = None,
) -> tuple[Graph, dict]:
    """Degree-(and optionally stratum-)preserving swap placebo.

    ``chain='besag_clifford'`` with ``hub=None`` first runs the chain backwards from G0
    (the chain is reversible, so backwards == forwards in law) to create the hub; pass a
    precomputed ``hub`` to draw several exchangeable placebos from the same hub.
    """
    if g.directed:
        raise ValueError("use directed_degree_null for directed graphs")
    target = int(round(swap_factor * g.m))
    max_attempts = int(attempt_factor * max(target, 1))
    start = g
    hub_info = {}
    if chain == "besag_clifford":
        if hub is None:
            hub_edges, hd, ha = _swap_chain(g.edges, g.n, target, rng, strata, max_attempts)
            hub = Graph.from_edges(g.n, hub_edges)
            hub_info = {"hub_swaps": hd, "hub_attempts": ha}
        start = hub
    elif chain != "forward":
        raise ValueError(f"unknown chain mode {chain!r}")
    e, done, att = _swap_chain(start.edges, g.n, target, rng, strata, max_attempts)
    info = {
        "target_swaps": target,
        "achieved_swaps": done,
        "attempts": att,
        "acceptance_rate": done / att if att else 0.0,
        "chain": chain,
        **hub_info,
    }
    return Graph.from_edges(g.n, e), info


def directed_degree_null(g: Graph, rng, *, swap_factor=5.0, attempt_factor=60.0):
    if not g.directed:
        raise ValueError("graph is undirected")
    target = int(round(swap_factor * g.m))
    e, done, att = _directed_swap_chain(g.edges, g.n, target, rng, int(attempt_factor * max(target, 1)))
    return Graph.from_edges(g.n, e, directed=True), {
        "target_swaps": target, "achieved_swaps": done, "attempts": att,
        "acceptance_rate": done / att if att else 0.0,
    }


def within_stratum_permutation(g: Graph, strata: np.ndarray, rng) -> tuple[Graph, dict]:
    """Relabel nodes by a uniformly random permutation within each stratum.

    Node i of the placebo takes the role of node pi(i) in G0 (edges (u,v) -> (pi^{-1}u, pi^{-1}v)).
    The permutation group acts on graphs, so if G0's assignment is a uniform draw from its
    orbit, G0 and placebos are exactly exchangeable (the PCGA argument).
    """
    perm = np.arange(g.n)
    for s in np.unique(strata):
        idx = np.flatnonzero(strata == s)
        perm[idx] = rng.permutation(idx)
    # perm maps old position -> new label
    e = perm[g.edges]
    fixed = float(np.mean(perm == np.arange(g.n)))
    return Graph.from_edges(g.n, e, directed=g.directed), {"fixed_point_fraction": fixed}


# ----------------------------------------------------------------------------- specs
@dataclass(frozen=True)
class NullSpec:
    """Declarative description of a candidate null generator.

    ``family``: one of ``er``, ``degree``, ``strat``, ``perm``, ``directed_degree``.
    ``attrs``: node attributes the generator must preserve (strata), if any.
    The hard constraints implied by the family are what the admissibility audit verifies.
    """

    family: str
    attrs: tuple[str, ...] = ()
    swap_factor: float = 5.0
    chain: str = "forward"

    @property
    def name(self) -> str:
        if self.family in ("er", "degree", "directed_degree"):
            return self.family
        return f"{self.family}:{'+'.join(self.attrs)}"

    @staticmethod
    def parse(name: str, **kw) -> "NullSpec":
        if ":" in name:
            fam, rest = name.split(":", 1)
            return NullSpec(fam, tuple(rest.split("+")), **kw)
        return NullSpec(name, (), **kw)

    def hard_constraints(self) -> list[str]:
        base = ["node_count", "edge_count", "simple"]
        if self.family in ("degree", "strat"):
            base.append("degree_sequence")
        if self.family == "strat":
            base.append("neighbour_stratum_counts")
        if self.family == "directed_degree":
            base.append("in_out_degree_sequence")
        if self.family == "perm":
            base.append("stratum_preserving_isomorphism")
        return base

    def sample(self, g: Graph, node_attrs: dict, rng: np.random.Generator, hub: Graph | None = None):
        if self.family == "er":
            return erdos_renyi_gnm(g, rng)
        if self.family == "degree":
            return swap_null(g, rng, swap_factor=self.swap_factor, chain=self.chain, hub=hub)
        if self.family == "strat":
            strata = stratum_codes(node_attrs, self.attrs, g.n)
            return swap_null(g, rng, strata=strata, swap_factor=self.swap_factor, chain=self.chain, hub=hub)
        if self.family == "perm":
            strata = stratum_codes(node_attrs, self.attrs, g.n)
            return within_stratum_permutation(g, strata, rng)
        if self.family == "directed_degree":
            return directed_degree_null(g, rng, swap_factor=self.swap_factor)
        raise ValueError(f"unknown null family {self.family!r}")


def candidate_specs(attr_names: list[str], max_order: int = 2, include_perm: str | None = "block",
                    swap_factor: float = 5.0) -> list[NullSpec]:
    """The finite candidate set used in Phase 2A: er, degree, perm:<block>, strat over all
    attribute subsets of size 1..max_order.  Enumerated in a fixed, documented order."""
    from itertools import combinations

    specs = [NullSpec("er"), NullSpec("degree", swap_factor=swap_factor)]
    if include_perm:
        specs.append(NullSpec("perm", (include_perm,)))
    for k in range(1, max_order + 1):
        for combo in combinations(attr_names, k):
            specs.append(NullSpec("strat", tuple(combo), swap_factor=swap_factor))
    return specs
