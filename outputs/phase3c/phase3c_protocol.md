# Phase 3C protocol: targeted real-world validation (frozen before model scores)

Date: 2026-11-24. This phase is a targeted follow-up, not a revision of Phase 3B and not a full
benchmark. The frozen Phase 3B **NO-GO remains in force**. No Phase 3B file is overwritten.

## 1. Scope and separation

Phase 3C has two independent streams:

1. **Cora calibration replication:** GraphSAGE only, 1,500 fresh replicate clusters and the exact
   Phase 3B lattice. It tests the single flagged Phase 3B cell without reusing any cluster, split,
   model seed, or null draw.
2. **Targeted structural pilot:** CiteSeer, GCN and GraphSAGE, 400 fresh clusters. The first 100 are
   confirmatory and clusters 100--399 are reference/exploratory. The dataset and lattice are fixed
   here before any Phase 3C model score is computed.

Development is limited to unit tests, label-free admissibility, runtime probes that print no score,
and existing Phase 3B evidence. Confirmatory CiteSeer scores may not be used to change attributes,
the lattice, delta, budgets, models, or decision rules. The raw pool and all empty frontiers are
retained. A full multi-dataset benchmark is prohibited before review of this phase.

## 2. Frozen estimand, method, and margin

The fixed-graph estimand, cluster construction, score `1 - Brier/2`, models, training rule, CRAF
certificate, Holm correction over `2|L|` directional hypotheses, adaptive rule, and PCGA-L
comparison are unchanged from Phase 3B (`docs/phase3b_protocol.md`, `docs/craf_math.md`).

`delta = 0.005` and `alpha = 0.05`. **Delta will not be increased to make a frontier non-empty.**
No alternative margin is analyzed in Phase 3C. Any later margin requires a scientific utility
argument and a new preregistration before scores are inspected.

## 3. Independent GraphSAGE calibration replication

Dataset and model are Cora and the frozen GraphSAGE-mean implementation. The 11 Phase 3B lattice
elements, two independent null draws, split sizes, training rule, `swap_factor=5`, and
`attempt_factor=1000` are identical. Only the 22 null fits needed for A/A contrasts are run; real,
empty, ER, GCN, and MLP fits are omitted because they contain no information for this question.
The new master seed is 20270201.

For each element, `a_r = score(draw 0) - score(draw 1)`. Exchangeability of the two independently
drawn nulls implies a distribution symmetric around zero. The primary cell is fixed to the one
flagged previously: one-sided t-test, sufficiency direction, `n=80`, alpha 0.05. The 1,500 clusters
give 18 disjoint groups and 198 element-group tests; the final 60 clusters are retained but not
used in this cell.

Because 11 tests in the same group share splits and training seeds, the primary 95% interval for
the pooled rejection rate is a 10,000-replicate **block bootstrap over the 18 independent groups**.
The ordinary Wilson interval is descriptive only. A persistent flag is declared only when the
block-bootstrap lower limit exceeds 0.05. Procedure-level t+Holm FWER at the all-boundary
configuration is separately flagged when its Wilson lower limit across groups exceeds 0.05.

Conditional investigation if the marginal flag persists:

* report skewness, kurtosis, tails, invalid draws, block/element rejection patterns and
  cross-element dependence;
* run a 9,999-draw paired sign-flip randomization audit. This is exact for A/A exchangeability and
  is diagnostic; it is **not** substituted for real-vs-null inference, where exchangeability does
  not hold;
* retain the NO-GO and treat t-based real-data certification as requiring further robust-inference
  work if both the block-aware t audit and procedure-level FWER fail. No post-hoc test is promoted
  to primary.

## 4. Scientifically motivated Phase 3C lattice

All attributes are computed from `G0` and raw features only:

| attribute | frozen definition | scientific target |
|---|---|---|
| `block` | seven largest Louvain communities plus other, as in Phase 3B | PCGA-L anchor / mesoscale structure |
| `fsim` | spherical k-means, k=16, on 32 sparse truncated-SVD feature components | finer feature assortativity / A-X dependence than Phase 3B k=8 |
| `clust` | quantile bins of node local clustering coefficient | triangle and ego-network structure |
| `hop2` | quantile bins of distinct nodes at distance exactly two | multi-hop neighbourhood volume |

The lattice contains all subsets of order at most two (11 elements including degree-only). The
null preserves the degree sequence and, for every node, neighbour counts in each joint stratum.
The property labels are fixed from `G0`; they are not recomputed after rewiring. This tests whether
coarse mixing with scientifically motivated node contexts is sufficient, not exact preservation of
every triangle or two-hop path. That limitation must be stated in the report.

Admissibility is label-free and unchanged: 20 audit samples; no hard violation; at least 80% valid;
swap completion at least 0.95; overlap with `G0` at most 0.80; mean pairwise overlap of 10 draws at
most 0.90. Edge overlap, pairwise overlap, acceptance, and mixing-matrix deviations are reported.
Passing proves the declared constraints and perturbation strength, not scientific correctness.

Leakage audit: attribute and null APIs must have no `y`, label, split, or score argument; attributes
must be invariant to label permutation; null graphs must be identical after label permutation.
Label association is computed only after freezing and is descriptive. CiteSeer's known isolated
nodes remain in the fixed graph and splits; they are not silently removed.

## 5. Dataset universe and fixed choice

The candidate universe was defined from public benchmark families before Phase 3C scores:

| dataset | role / reason | status |
|---|---|---|
| CiteSeer | small citation graph, same file format as Cora, feasible matched replication | **one confirmatory pilot selected** |
| PubMed | larger homophilous citation graph | future; cost gate first |
| Amazon Photo | product co-purchase structure distinct from citations | future; cost gate first |
| Roman-empire | sparse heterophilous graph without the Chameleon/Squirrel duplicate-node problem | future targeted candidate |
| Minesweeper | small-feature heterophilous graph with explicitly local relational mechanism | future targeted candidate |

Chameleon and Squirrel are excluded because published audits identify duplicate-node leakage.
Amazon Computers is not rerun because Phase 3B measured about four CPU-hours per cluster.
ogbn-arxiv is excluded until a sparse, directed, time-respecting null exists. Tolokers and Questions
exceed the initial edge/node cost screen. These exclusions are reported, not replaced after seeing
results.

CiteSeer source: the archived `shchur/gnn-benchmark` npz, SHA256
`280278b21b434c047922e8389518861416fb3ad39389c27865ff0e6bbb0aaab7`; 3,312 nodes,
4,536 undirected edges, 3,703 features, six classes, and 48 isolated nodes.

## 6. Targeted pilot analyses

Confirmatory CRAF uses clusters 0--99 and `b=80`; reference analyses use clusters 100--399 and the
mean of both valid draws. Report certified advantage, sufficient and inconclusive sets;
`cert_min`, `possible_min`, `min_among_cert`, gap sets, specificity, and simultaneous intervals.
Compare on the same clusters and matched fit budgets with `ni_holm`, naive point frontier,
unadjusted factorial testing, immediate-subset CRAF, adaptive CRAF, and PCGA-L. Report natural
non-monotonicity and pair interactions without changing the primary decision.

CRAF is "strongly informative beyond standard Holm/PCGA-L" only if at least one architecture has:

1. a confirmatory certified-minimal element outside the PCGA-L chain; or
2. a confirmatory CRAF frontier sandwich/gap set that is strictly more informative than the
   `ni_holm` reported frontier and PCGA-L result; or
3. Holm-certified natural non-monotonicity in the reference analysis.

Specificity over the full lattice is a useful negative result but is not a distinctive frontier
finding. Empty frontiers are displayed and counted, never suppressed.

## 7. Cost control without weaker guarantees

The calibration stream omits 29 irrelevant fits per cluster (real, empty, ER, GCN and MLP), saving
43,500 fits relative to repeating the Phase 3B pool. Graphs are shared across architectures in the
targeted pilot, inputs use the exact sparse first-layer implementation, jobs are chunked/checkpointed,
and BLAS/PyTorch each use one thread. None changes the estimand, model, draws, tests, alpha, or Holm
family. Confirmatory cost must be at most 12 CPU-hours per dataset-architecture; all measured and
projected costs are reported.

## 8. Frozen GO/NO-GO rule

The Phase 3B decision remains NO-GO regardless of this outcome. Phase 3C recommends a later full
benchmark (**GO**) only if all hold:

* C1: neither the primary block-aware calibration cell nor t+Holm FWER has a persistent flag;
* C2: all four singleton attributes and at least half of the 11 lattice elements are admissible;
* C3: strong informativeness criterion 1, 2, or 3 above holds for at least one architecture;
* C4: confirmatory CRAF costs at most 12 CPU-hours for each architecture.

Otherwise the evidence-based decision is **NO-GO**. There is no conditional-GO category and no
exception for an empty frontier. Failures, invalid candidates, and negative findings remain in the
frozen outputs.
