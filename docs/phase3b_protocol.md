# Phase 3B protocol: real-world pilot of CRAF (frozen before confirmatory execution)

Written 2026-11-24. `outputs/phase3b/FREEZE.json` hashes the config, all source files, scripts and
batch files. The run happens in a separate Hyperion directory, `/scratch/hilmibukhori/rusa_3b`.
Phases 2A–3A are preserved: their directories (`rusa`, `rusa_2b`, `rusa_2c`, `rusa_3a`) and local
outputs are not modified, and all Phase 3B code is new (`src/rusa/realworld/`) or additive.

**Frozen method.** CRAF exactly as in `docs/craf_math.md` (Phase 3A), with no change to the
estimands, the certification (Holm over 2|L| one-sided t tests), the frontier sets, or the adaptive
mode (`n_min = 5`, stage-1 share 1/3, `w1² = 1/3`, a-priori fallback). The RUSA full-set claim uses
`fullset_adaptive_fb`, the frozen default (selected after Phase 2C; disclosed there).

**Scope: a limited pilot.** Cora with GCN and GraphSAGE. Amazon Computers (label-free admissibility
audit done) and ogbn-arxiv receive a feasibility assessment only (§0, §9). The full cross-domain benchmark is **not** started before this
pilot has been reviewed.

## 0. Development observations (before freezing; not results)

| Observation | Consequence |
|---|---|
| Label-free admissibility audit at `attempt_factor = 200`: on Cora, `deg+feat` and `dlen+feat` reached only 33–38% of the target swaps (acceptance ≈ 0.2%), so they failed the pre-declared completion rule (≥ 0.95) | `attempt_factor` raised to 1000 before freezing. The audit was rerun, and every element passes on both datasets (`outputs/phase3b/admissibility/`; the af200 audit is kept in `admissibility_af200/`). This used no labels, scores or fits |
| A first smoke with a dense input layer did not finish one Cora cluster (51 fits) in 14 min | The input layer now uses a sparse-dense product with dropout on the stored entries. This is the same model and ~10× faster |
| Timing probe (dev seed 999, one fit per arch; only seconds and epochs were printed, scores were never printed): Cora 5.8 s (GCN), 7.2 s (SAGE), 2.9 s (MLP); Amazon Computers 200 s (GCN), 365 s (SAGE) | Cora: N = 1500 clusters (~140 CPU-h). **Amazon Computers would cost ~4 CPU-h per cluster (> 1,000 CPU-h for a minimal pilot), so it is moved to the post-review stage** with a cost projection (§9). Its label-free admissibility audit is kept: all 11 elements are admissible |

## 1. Fixed-graph estimand

The graph `G0`, features `X` and labels `y` are fixed. A **replicate cluster** `r` consists of:
* a fresh class-stratified split: 20 training and 30 validation nodes per class, the rest test;
* a fresh training seed `xi_r`, shared by every variant in the cluster;
* fresh, independent null draws for every lattice element (2 draws) and for ER (1 draw).

The draws are seeded by `(master, dataset, r, element, draw)`. They do not depend on the
architecture, so GCN and SAGE see the same null graphs.

```
Delta_S(G0) = E_{split, xi, G ~ N_S(G0)} [ S(G0; split, xi) − S(G; split, xi) ]
```

`S` is the test score `1 − Brier/2 ∈ [0, 1]` of the multi-class prediction. Clusters are i.i.d.
given `(G0, X, y)`, so the one-sided t-tests of CRAF apply. Their calibration is **measured** on
fresh clusters (§6). This is a conditional (fixed-graph) estimand. It says nothing about other
graphs from the same domain.

## 2. Datasets, models, clusters

| Dataset | Source (npz, `allow_pickle=False`) | n | m (undirected) | features | classes | clusters N | chunk |
|---|---|---|---|---|---|---|---|
| Cora | gnn-benchmark `cora.npz` (sha256 068e22d9…) | 2708 | 5278 | 1433 | 7 | 1500 | 10 |
| Amazon Computers (audit only) | gnn-benchmark `amazon_electronics_computers.npz` (sha256 736ba1d9…) | 13752 | 245861 (281 isolated nodes) | 767 | 10 | not run | – |

* The graph is symmetrised, without self-loops or duplicates. Features are L1 row-normalised.
* Models: GCN and GraphSAGE-mean (2 layers, hidden 64), plus their **matched no-graph** versions
  (same architecture with an identity / zero neighbour operator) and a **feature-only** MLP.
* Training is fixed a priori: Adam with lr 0.01 and weight decay 5e-4; dropout 0.5; at most 300
  epochs; early stopping on validation cross-entropy with patience 50; the best weights are
  restored.
* Test accuracy is a secondary, descriptive metric.

**Cluster roles (fixed):**
* block 0 (clusters 0–99) is the **confirmatory** run;
* clusters ≥ 100 are the **reference** set. They are used for high-precision estimates,
  calibration, resampling comparisons and structure analyses.

## 3. Admissible properties and null generators

The attributes are label-free (`src/rusa/realworld/attributes.py`). They are computed once from
`G0` and the raw features with seed 20261229 and frozen (`data/processed/<ds>_attrs.npz`, hashes in
`admissibility/<ds>_meta.json`). None of these functions receives labels, splits or scores
(`tests/test_phase3b.py::test_attributes_and_nulls_take_no_labels`,
`::test_pool_nulls_do_not_depend_on_labels`).

| attribute | definition | role |
|---|---|---|
| `deg` | degree quartile bin | degree–degree mixing |
| `block` | Louvain communities of G0 (resolution 1, fixed seed); the 7 largest kept, the rest merged | mesoscale structure; the PCGA-L "block" level |
| `feat` | spherical k-means (k = 8) on the top-32 SVD components of the L2-normalised raw features | feature homophily |
| `dlen` | quartile bin of the number of non-zero features | plausibly irrelevant (a control property) |

* **Lattice:** all subsets of order ≤ 2 of {deg, block, feat, dlen}, so `|L| = 11`.
* **Null `N_S`:** degree-preserving double-edge swaps that preserve each node's neighbour count in
  every joint stratum of `S`. The chain runs forward from G0 (`5m` target swaps, at most `1000 × 5m`
  attempts). ER (G(n, m)) is used only for the PCGA-L ladder.
* **Leakage:** class labels are never a stratification attribute. Preserving label–label mixing
  would hand the target to the null. `feat` and `block` are label-free but may be label-correlated.
  That is the scientific question, not leakage. Their association with labels is reported post
  hoc only.
* **Temporal constraints:** none apply to Cora or Amazon (no timestamps are used). For ogbn-arxiv
  see §9.
* **Admissibility rule** (pre-declared, label-free): an element is admissible if, over 20 audit
  samples, ≥ 80% are valid and the mean pairwise overlap of 10 samples is ≤ 0.90. A sample is
  valid if every hard constraint holds exactly, swap completion is ≥ 0.95 and edge overlap with
  G0 is ≤ 0.80.
* In the pool every sample is audited again. Invalid samples are not fitted, and contrasts use the
  first valid draw.

## 4. Procedures

On the same clusters and budget `B = b(1 + |L|)`:
* `craf` (primary) and `craf_adaptive`;
* `craf_children`: immediate-subset certification;
* `ni_holm`: Holm non-inferiority with naive minimality;
* `factorial_unadj`: exhaustive factorial, unadjusted;
* `naive_point`: point-estimate frontier;
* `pcga_l`: the ladder empty → ER → degree → block → real.

For the RUSA scalar full-set claim: `exhaustive_iut` vs `fullset_adaptive_fb` (`b ∈ {6, 12, 24}`,
20 dev clusters, `B = b(2 + K)`).

`delta = 0.005` and `alpha = 0.05`, as in Phases 2B–3A.

## 5. Analyses (per dataset × architecture)

1. **Confirmatory frontier.** On block 0 with `b_conf = 80`, uniform CRAF reports:
   * the certified advantage / sufficient / inconclusive elements;
   * `cert_min` and `possible_min`;
   * the gap sets and the specificity claim;
   * Bonferroni-simultaneous 95% intervals for every `Delta_S`.

   Adaptive CRAF is reported alongside it. Every comparator's report on the same data is tabulated.
2. **Reference frontier.** All clusters ≥ 100, with contrasts averaged over draws. This is CRAF at
   a large n, with the same outputs.
3. **Resampling comparison.** Disjoint blocks of 100 reference clusters at `b ∈ {20, 40, 80}`,
   scored against the **leave-block-out** reference point estimates (the proxy truth). Elements
   whose reference estimate lies within 2 SE of delta are flagged as near-margin, and that count
   is reported.
4. **Full-set claim.** Claim rates of `exhaustive_iut` and `fullset_adaptive_fb`, paired, plus the
   PCGA-L edge step.
5. **Structure.**
   * **Natural non-monotonicity:** every comparable pair `S ⊊ T` with one-sided `Delta_T − Delta_S > 0`
     (and `> delta`), Holm over pairs.
   * **Interactions:** `I_ab = Delta_∅ − Delta_a − Delta_b + Delta_ab`, two-sided, Holm.
   * **Multiple sufficient combinations:** `|cert_min|` or `|possible_min| > 1`.
   * **Architecture differences:** paired `Delta^GCN_S − Delta^SAGE_S` (same clusters and null
     graphs), Holm.
6. **Costs.** Seconds per fit and per null draw, and CPU-hours per procedure and budget.

## 6. Calibration (fresh clusters only, i.e. clusters ≥ 100; never block 0)

* **Exact A/A contrasts.** `a_{r,S} = S(draw 0) − S(draw 1)`. The two draws are exchangeable given
  the cluster, so the mean is exactly 0 and the law is symmetric.
  * (i) Size of the one-sided t-test in both directions, on disjoint groups with
    n ∈ {5, 10, 20, 40, 80}, at alpha ∈ {0.05/22, 0.01, 0.05}.
  * (ii) Worst-case FWER of CRAF certifications with every element at the boundary
    (`a + delta`), on disjoint groups with n ∈ {20, 40, 80}.
  * (iii) The same for adaptive CRAF on disjoint blocks of 100 (primary), plus a 2000-replicate
    cluster bootstrap (secondary).
* **Centred real contrasts** (secondary; captures the skewness of real-vs-null contrasts).
  `D − mean(D) + delta`, disjoint groups.
* **Flag:** the Wilson 95% lower limit exceeds the nominal level.

## 7. Pre-registered questions (no directional hypotheses)

* Q1. Is CRAF calibrated on real fixed-graph contrasts (§6)?
* Q2. Which label-free property combinations are certified sufficient, certified insufficient, or
  unresolved, for GCN and SAGE on each dataset? Is relational specificity over L certified?
* Q3. Does natural non-monotonicity occur? Do multiple minimal sufficient combinations or
  significant interactions occur? Do architectures differ?
* Q4. Do the comparators report different frontiers from CRAF on the same data? How do they
  perform against the reference?
* Q5. Does adaptive allocation improve exact recovery or inconclusiveness at a matched budget,
  without a calibration flag? Does `fullset_adaptive_fb` improve full-set claims over exhaustive
  IUT?
* Q6. What does certification cost, and is the full benchmark (including ogbn-arxiv) feasible?

## 8. Decision rules for recommending the full benchmark (fixed before results)

* **R1 Calibration.** No flag in the primary A/A FWER check (craf, disjoint groups) and no flag in
  the marginal size at alpha = 0.05.
* **R2 Admissibility.** In each audited dataset (Cora and Amazon Computers), all 4 singleton elements and at least 50% of all elements
  are admissible.
* **R3 Informativeness.** In at least one dataset × architecture, the confirmatory CRAF output
  contains a statement the standard approaches do not give:
  * (a) a certified-minimal element outside the PCGA-L ladder {∅, block}; or
  * (b) `ni_holm`'s reported frontier differs from CRAF's; or
  * (c) certified natural non-monotonicity in the reference analysis.

  Certified specificity over L **alone**, i.e. without (a)–(c), counts only as (d), the weaker
  category.
* **R4 Feasibility.** Confirmatory CRAF at b = 80 costs ≤ 24 CPU-hours per dataset × architecture
  on the pilot datasets.
* **Decision.**
  * **GO** for the full benchmark: R1, R2, R4, and R3 via (a), (b) or (c) for **both**
    architectures on Cora.
  * **CONDITIONAL GO:** R1 and R2 hold, but R3 holds for only one architecture or only via (d), or
    R4 fails. Because only one dataset is run, a GO still requires the full benchmark to begin with
    the cost-engineering items of §9.
  * **NO-GO:** R1 fails, or R2 fails on both datasets, or R3 fails entirely.

  Negative and inconclusive outcomes are reported as such. The questions are not revised after the
  results.

## 9. ogbn-arxiv: feasibility only

* ogbn-arxiv is a directed citation graph (169,343 nodes; 1,166,243 edges) with publication years
  and a temporal split.
* A temporally valid null must keep every citation pointing from a newer to an older (or
  same-year) paper. This needs a directed, time-respecting swap: stratify swap endpoints by year,
  or reject swaps that create forward-in-time citations. Nodes must also be split by year, as OGB
  does, rather than by random clusters.
* The current swap kernel stores a dense n×n adjacency, about 28.7 GB for arxiv, so a sparse
  (hash-set) kernel is needed.
* **Amazon Computers:** about 200 s (GCN) and 365 s (SAGE) per fit on one CPU thread, so one
  cluster (51 fits) costs about 4 CPU-h. A confirmatory block of 100 clusters plus 500 reference
  clusters would cost about 2,400 CPU-h. Options to review: multi-threaded or GPU fits, fewer
  reference clusters, one architecture.
* Neither of these is implemented in this pilot. The report gives a cost projection and the
  engineering items.
