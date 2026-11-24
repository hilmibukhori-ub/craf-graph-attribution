# Phase 3E protocol: preregistered heterophilous real-world pilot (frozen before model scores)

Date: 2026-11-24. Phase 3E is one targeted follow-up. It does not revise Phase 3B, 3C or 3D: the
Phase 3B and 3C **NO-GO** decisions and the Phase 3D stop remain in force. No earlier file is
overwritten; Phase 3E runs in its own directory (`/scratch/hilmibukhori/rusa_3e`) and output tree
(`outputs/phase3e`).

## 1. Question and why these datasets

Phases 3B–3D found, on homophilous citation graphs (Cora, CiteSeer), that no combination of the
label-free properties studied is sufficient: every CRAF frontier was empty and only full-lattice
specificity was certified. The distinctive part of CRAF (certified minimal sufficient sets,
possible-minimal sandwich, non-monotonicity) has therefore never been exercised on real data.

Phase 3E asks the same question on two heterophilous graphs from Platonov et al. (2023), chosen
**before any Phase 3E score** and both reported regardless of outcome:

| dataset | why | source / SHA256 |
|---|---|---|
| Roman-empire | sparse, heterophilous, large graph gain for GNNs over MLP in the original benchmark | `yandex-research/heterophilous-graphs` `data/roman_empire.npz`, `a58ba741…d428` |
| Amazon-ratings | heterophilous, small but nonzero graph gain; more room for coarse properties to be sufficient | same repository, `amazon_ratings.npz`, `4c3a3e3b…c7dd` |

These were the two heterophilous candidates already named as future targets in the Phase 3C
dataset universe (Roman-empire explicitly; Amazon-ratings from the same benchmark family). No other
dataset is added after scores are observed, and neither is dropped because of its result.
Minesweeper, Tolokers and Questions remain out of scope (cost / binary-label design differences).

## 2. Frozen estimand, method and margin (unchanged)

Fixed-graph estimand, replicate-cluster construction, score `1 - Brier/2`, GCN and GraphSAGE
architectures, matched no-graph and MLP controls, training rule (hidden 64, Adam lr 0.01, weight
decay 5e-4, dropout 0.5, at most 300 epochs, patience 50 on validation loss), CRAF certificate,
Holm over `2|L|` directional hypotheses, adaptive rule, `ni_holm`, naive, factorial,
immediate-subset and PCGA-L comparisons are exactly those of Phase 3B/3C
(`docs/phase3b_protocol.md`, `docs/phase3c_protocol.md`, `docs/craf_math.md`).

`delta = 0.005`, `alpha = 0.05`. **Delta is not changed under any outcome.**

## 3. Dataset-specific adaptations (fixed before scores)

1. **Loader.** These files store dense signed 300-d text embeddings, an edge list and labels.
   Edges are symmetrised, deduplicated and self-loops removed (as for Cora/CiteSeer). Features are
   used as provided: L1 row normalisation (Phase 3B) is undefined for signed features. The fixed
   split masks in the files are ignored.
2. **Split.** Each replicate cluster draws a fresh class-stratified random split with 50% train,
   25% validation and 25% test per class (the proportions of the original benchmark). The
   Phase 3B/3C 20/30-per-class split would leave Amazon-ratings with 100 training nodes, far from
   the regime in which these graphs are known to help. This is a design choice, not a tuning result.
3. **Dense input path.** Inputs with density at least 0.5 are passed to the first layer as a dense
   tensor (the Phase 3B sparse path is an exact reimplementation intended for bag-of-words input;
   the model is identical).
4. **Lattice.** Unchanged from Phase 3C: attributes `block` (7 largest Louvain communities + other),
   `fsim` (spherical k-means k=16 on 32 truncated-SVD feature components), `clust` (quartile bins of
   local clustering), `hop2` (quartile bins of distinct 2-hop neighbours); all subsets of order
   ≤ 2 (11 elements including degree-only). Attributes take `G0` and raw features only. On graphs
   with many tied values (e.g. clustering coefficient 0) `quantile_bins` merges tied bins; the
   resulting number of strata is reported, not altered.

Hyperparameters are deliberately **not** retuned for heterophily: the question is about the
fixed, standard GCN/SAGE used throughout Phases 3B–3D.

## 4. Label-free admissibility (run before the freeze)

Unchanged policy: 20 audit samples per element; no hard violation; ≥ 80% valid; swap completion
≥ 0.95; edge overlap with `G0` ≤ 0.80; mean pairwise overlap of 10 draws ≤ 0.90. The audit outputs
and their hashes are recorded in §9 before any model is fitted. An inadmissible element stays in
the lattice: its draws are marked invalid and not fitted, and CRAF reports it as unresolved.

## 5. Replication design and cost

400 fresh replicate clusters per dataset (master seed 20270301; no cluster, split, seed or null draw
shared with any earlier phase). Clusters 0–99 are confirmatory (`b = 80`); clusters 100–399 are
reference/exploratory and give the calibration (A/A) checks. Two null draws per element, one ER
draw, GCN and SAGE on identical null graphs, one MLP per cluster. The timing probe (dev seed 999,
prints no score) is recorded in §9.

## 6. Analyses

As in Phase 3C §6: certified advantage / sufficient / inconclusive sets, `cert_min`,
`possible_min`, `min_among_cert`, gap sets, specificity, simultaneous intervals; matched-budget
comparison with `ni_holm`, naive, factorial, immediate-subset, adaptive CRAF and PCGA-L; natural
non-monotonicity, pair interactions and GCN−SAGE differences; A/A calibration on reference
clusters; costs. Attribute–label association (NMI) is computed only after the freeze, descriptively.

## 7. Graph-relevance precondition

A frontier is only meaningful if the observed graph itself helps. For each dataset × architecture,
**graph relevance** holds if the reference-cluster 95% interval of `S(real) − S(empty)` lies
entirely above `delta`. If it fails, every "sufficient" claim for that cell is reported but labeled
*trivial* (the graph does not matter) and does not count toward E2 below.

## 8. Frozen decision rule

Phase 3E recommends extending the real-world evaluation in the paper (**GO**) only if all hold:

* E1 (calibration): no persistent flag for t+Holm FWER on the reference clusters of any cell.
* E2 (non-trivial frontier): for at least one dataset × architecture with graph relevance, the
  confirmatory CRAF `cert_min` is non-empty (at least one certified-minimal sufficient element).
* E3 (admissibility): on each dataset all four singleton attributes and at least half of the 11
  elements are admissible.
* E4 (cost): confirmatory CRAF costs at most 60 CPU-hours per dataset × architecture. (The Phase 3C
  limit of 12 CPU-hours was set at Cora/CiteSeer scale; the label-free timing probe in §9 shows that a
  single fit here takes 60–106 s, so the threshold was set from the probe, before any score.)

Secondary (reported, not part of GO): Phase 3C strong-informativeness criteria 1–3, i.e. a
certified-minimal element outside the PCGA-L chain, a CRAF sandwich strictly more informative than
`ni_holm`/PCGA-L, or Holm-certified natural non-monotonicity.

If E2 fails on both datasets, the real-world conclusion of the paper is the negative one from
Phases 3B–3E (certified specificity; no sufficient coarse label-free summary), and **no further
dataset search is performed**. There is no conditional GO. All empty frontiers, invalid
candidates and failed gates are reported.

## 9. Pre-freeze label-free records

**Tests:** 124/124 pass on Hyperion (job 8205176), including `tests/test_phase3e.py`.

**Timing probe** (job 8204936, dev seed 999, no score printed; seconds per fit, all 300 epochs):

| dataset | n | m (undirected) | classes | GCN | SAGE | MLP |
|---|---|---|---|---|---|---|
| Roman-empire | 22,662 | 32,927 | 18 | 60 s | 73 s | 51 s |
| Amazon-ratings | 24,492 | 93,050 | 5 | 80 s | 106 s | 55 s |

Projected pool: ~51 fits per cluster, about 1.0 / 1.3 CPU-h per cluster, ~900 CPU-h in total for
400 clusters per dataset. Chunk size 1 (one cluster per array task).

**Attribute strata** (label-free): Roman-empire block 8 (7 Louvain communities of 170–184 nodes,
'other' 21,436 nodes), fsim 16, clust 4, hop2 4; Amazon-ratings block 8 (7 of 478–769, 'other'
20,062), fsim 16, clust 4, hop2 4. The Louvain attribute is therefore coarse on both graphs (most
nodes in 'other'); the frozen definition is kept and this is reported.

**Admissibility** (jobs 8204934, 8204935; attempt_factor 1000 unchanged):

| dataset | rejected | reason (mean swap completion, threshold 0.95) | admissible |
|---|---|---|---|
| Roman-empire | fsim+hop2 | 0.908 | 10/11 |
| Amazon-ratings | clust+fsim, fsim+hop2 | 0.731, 0.856 | 9/11 |

No hard-constraint violation anywhere; all admissible elements have mean edge overlap ≤ 0.17.
The attempt budget is **not** raised (unlike Phase 3B), to avoid an extra degree of freedom:
rejected elements stay in the lattice, their draws are marked invalid and not fitted, and CRAF
reports them as unresolved. E3 is met on both datasets.

Audit file SHA256 (outputs/phase3e/admissibility, data/processed):
`roman_empire_elements.csv a0b4f4d6…7d`, `roman_empire_samples.csv 062285e4…b3`,
`amazon_ratings_elements.csv 08df6964…d0`, `amazon_ratings_samples.csv b0dcc73d…c5`,
`roman_empire_attrs.npz 65032b0d…30`, `amazon_ratings_attrs.npz 0594460c…41`.
