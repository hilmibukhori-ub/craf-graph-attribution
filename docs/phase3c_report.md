# RUSA Phase 3C — targeted real-world validation

Date: 2026-11-24. Status: **complete. Evidence-based decision: NO-GO for a full benchmark.**

The frozen Phase 3B NO-GO was respected and remains unchanged. Phase 3C ran only the
preregistered independent Cora calibration replication and one targeted CiteSeer pilot. It did
not launch the cross-domain benchmark, change delta, remove invalid results, or select a dataset
after observing model performance.

## Executive decision

| Frozen Phase 3C rule | Result | Verdict |
|---|---|---|
| C1 calibration | Cora GraphSAGE primary cell: 7/198 = 0.035; block-bootstrap 95% interval 0.015--0.061. t+Holm FWER: 1/18 = 0.056; Wilson lower limit 0.010. Neither is flagged | pass |
| C2 admissibility | all four singleton attributes and all 11 lattice elements pass; 100% valid samples | pass |
| C3 strong informativeness | no certified or possible frontier member, no gap set, no comparator frontier difference, and no certified non-monotonicity for either architecture | **fail** |
| C4 cost | confirmatory CRAF: 2.08 CPU-h (GCN), 3.42 CPU-h (SAGE), both below 12 CPU-h | pass |
| **Decision** | C3 is required and fails | **NO-GO** |

The most important negative result is substantive. A finer feature-assortativity control plus
local-clustering and two-hop controls moves the closest null much nearer to the real graph than in
Phase 3B, but the closest contrast remains about five times the fixed margin. CRAF again reduces
to a full-lattice specificity certificate instead of producing a frontier finding that standard
Holm testing or PCGA-L cannot report.

## 1. Frozen execution and preserved evidence

The protocol is `docs/phase3c_protocol.md`; its frozen copy and hash are in
`outputs/phase3c/phase3c_protocol.md` and `outputs/phase3c/PROTOCOL_SHA256.txt`.
`outputs/phase3c/FREEZE.json` hashes 82 files, including source, scripts, batch files, config,
protocol, and the CiteSeer archive. Verification succeeded before every job.

Phase 3B outputs were not modified. Phase 3C ran in `/scratch/hilmibukhori/rusa_3c`, separate from
`rusa_3b`. Hyperion jobs were: tests 8200735, label-free preparation 8200736, calibration array
8200739 (300 tasks), CiteSeer pool array 8200740 (80 tasks), and analysis 8200741. The frozen suite
passed 120/120 tests. The analysis job completed with exit code zero.

Raw preservation checks:

* calibration: 300 atomic CSV chunks, 1,500 clusters, 33,000 GraphSAGE fits, no incomplete cluster;
* targeted pool: 80 atomic chunks, 400 clusters, 20,400 fits across GCN, SAGE and MLP;
* all 11 null elements have valid rate 1.0 in both architectures;
* old and new empty frontiers are present in the reports and were not filtered.

## 2. Independent calibration rerun and inference audit

### Preregistered Cora replication

The rerun used 1,500 new clusters, a new master seed, the unchanged Phase 3B lattice, two new null
draws per element, and GraphSAGE only. The flagged Phase 3B cell was fixed in advance: `n=80`,
sufficiency direction, alpha 0.05. The primary interval resampled the 18 independent groups rather
than treating the 11 element tests within a group as independent.

| inference | rejections/tests | rate | 95% interval | flag |
|---|---:|---:|---:|---|
| one-sided t, primary | 7/198 | 0.035 | block bootstrap 0.015--0.061 | no |
| exact A/A sign-flip, diagnostic | 7/198 | 0.035 | block bootstrap 0.010--0.061 | no |
| t + Holm FWER at boundary | 1/18 groups | 0.056 | Wilson 0.010--0.258 | no |

The A/A distribution is well behaved: mean `4.24e-5`, SD 0.00752, skewness 0.016, excess
kurtosis 0.089, and mean cross-element correlation -0.0017. Thus the specific Phase 3B flag
(19/187 = 0.102) did not replicate. This does not revise the old decision: it shows that the old
cell is more consistent with a chance calibration excursion than a stable `n=80` sufficiency-side
failure.

The audit also identified a real weakness in the old reporting rule. Phase 3B's Wilson interval
pooled 11 tests sharing each split and training seed. Near-zero empirical correlations made the
numerical impact small there, but independence was not guaranteed. Phase 3C uses the independent
group as the resampling unit; future calibration reports should do the same.

### Secondary CiteSeer warning

The preregistered Cora cell passes, but calibration should not be generalized blindly. In the
300 CiteSeer reference clusters, the standard t+Holm audit flags GraphSAGE in the advantage
direction at `n=20` and `n=40` (FWER 3/15 and 3/7). A disclosed post-hoc exact A/A sign-flip audit
does not remove the pattern: marginal rejection is 15/165 with block-bootstrap interval
0.061--0.127 at `n=20`, and 8/77 with interval 0.052--0.169 at `n=40`; sign-flip Holm FWER is
2/15 and 3/7 groups. GCN is not block-bootstrap flagged.

This secondary result is based on few independent groups and was not the frozen C1 test. It is
therefore a warning, not a revised primary decision. It nevertheless argues against expanding the
benchmark until small-sample, dataset-specific calibration is replicated. Sign-flip is exact for
A/A draw exchangeability but cannot be substituted for real-vs-null mean inference, where the
real and null graph scores are not exchangeable. The diagnostic is preserved in
`outputs/phase3c/analysis/citeseer_signflip_diagnostic.csv`.

## 3. Structural lattice, admissibility, and leakage

The Phase 3C attributes are label-free: Louvain block, 16-cluster feature similarity (`fsim`),
local-clustering bins (`clust`), and exact-distance-two neighbourhood-volume bins (`hop2`). All
singletons and all order-two combinations pass the frozen audit.

| audit range over 11 elements | observed | frozen limit |
|---|---:|---:|
| valid-sample rate | 1.00 | at least 0.80 |
| overlap with original graph | 0.006--0.430 | at most 0.80 |
| mean pairwise overlap | 0.005--0.382 | at most 0.90 |
| hard violations | 0 | 0 |

Leakage tests verify that attribute and null APIs receive no labels, split, or scores; attributes
are invariant to label permutation; and null draws do not change when labels are permuted. Label
association was computed only after freezing. `fsim` and `block` each have NMI about 0.21 with
labels; this is expected association, not target leakage, because labels never define a stratum.

Scientific limitation: `clust` and `hop2` are fixed node contexts computed on `G0`. The swap null
preserves each node's neighbour counts across their bins; it does not preserve every triangle or
every two-hop path exactly. The results therefore concern these coarse, admissible proxies, not
exact triangle- or path-constrained graph ensembles.

## 4. Actual CiteSeer frontier results

Reference baselines over 300 clusters are:

| model | real score | no-graph score | real accuracy | no-graph accuracy |
|---|---:|---:|---:|---:|
| GCN | 0.7600 | 0.6901 | 0.689 | 0.559 |
| GraphSAGE | 0.7600 | 0.6905 | 0.675 | 0.560 |

Selected reference contrasts (`Delta_S`, real minus null) are:

| preserved property | GCN | GraphSAGE |
|---|---:|---:|
| degree only | 0.1510 | 0.1109 |
| local clustering | 0.1484 | 0.1069 |
| two-hop volume | 0.1374 | 0.1009 |
| community | 0.0904 | 0.0794 |
| feature similarity | 0.0447 | 0.0457 |
| community + feature similarity | 0.0269 | 0.0270 |
| feature similarity + two-hop volume (closest) | **0.0256** | **0.0245** |

Every simultaneous lower limit exceeds delta=0.005. The confirmatory block agrees with the
reference: for both architectures all 11 elements are certified advantage, none is sufficient or
inconclusive, and `cert_min = possible_min = {}`. The closest confirmatory simultaneous lower
limits are 0.0235 (GCN) and 0.0231 (GraphSAGE). Delta was not changed or supplemented.

The scientific pattern is coherent but does not rescue the frontier claim. Fine feature
assortativity explains the largest part of the real-vs-degree gap; community adds more; the
clustering proxy alone adds little; and two-hop volume adds modestly. Five of six GraphSAGE and
all six GCN pair interactions are Holm-significant, showing redundancy/synergy among properties.
No natural non-monotonicity is certified.

## 5. CRAF versus Holm and PCGA-L

On the same confirmatory data:

* CRAF, immediate-subset CRAF, unadjusted factorial testing, naive point estimates, and PCGA-L all
  report an empty frontier;
* Holm non-inferiority also reports no member, with all 11 elements unresolved;
* CRAF adds an affirmative certificate that all 11 declared combinations are insufficient;
* PCGA-L gives only its chain-level edge-specificity result;
* no certified-minimal element, possible-minimal element, or gap set appears.

So CRAF gives a broader certified negative than PCGA-L and a stronger status statement than
one-sided Holm non-inferiority alone. But the frozen C3 rule deliberately excludes specificity by
itself: it is the RUSA full-set claim, not evidence that frontier minimality or gap sets add value.
C3 therefore fails. Resampling comparisons are also uninformative: every method recovers the
empty reference frontier in all three available 100-cluster blocks.

Adaptive CRAF reaches the identical certificate with 556 versus 960 fits for GCN (42.1% fewer)
and 560 versus 960 for GraphSAGE (41.7% fewer). This is a cost result, not a power or novelty gain.

## 6. Computational cost

| item | actual cost |
|---|---:|
| independent calibration rerun | 68.74 CPU-h |
| targeted CiteSeer pool, all 400 clusters | 58.25 CPU-h |
| total Phase 3C pool compute | 126.99 CPU-h |
| confirmatory uniform CRAF, GCN | 2.08 CPU-h |
| confirmatory uniform CRAF, GraphSAGE | 3.42 CPU-h |
| null generation | 0.003--0.201 s/draw, negligible relative to fits |

The calibration-only runner used 33,000 fits instead of the 76,500 fits required by a full Phase
3B-shaped repeat, avoiding 43,500 irrelevant fits (56.9%) while retaining the same two null draws,
clusters, split/model pairing, and primary inference. Sparse input multiplication, shared null
graphs across architectures, atomic five-cluster checkpoints, and one CPU thread per task reduce
wall time without changing statistical guarantees. Parallel wall time was governed by the slowest
CiteSeer chunk (56.4 minutes); no statistical sample was dropped for runtime.

## 7. Dataset feasibility and separation

The fixed candidate universe remains CiteSeer, PubMed, Amazon Photo, Roman-empire, and
Minesweeper. CiteSeer was the sole confirmatory pilot because it met the pre-score cost and format
gate. Roman-empire and Minesweeper remain scientifically attractive heterophilous candidates;
they were not substituted after CiteSeer's empty frontier. PubMed and Amazon Photo require a
timing gate. Chameleon/Squirrel remain excluded because the published heterophily audit reports
duplicate-node leakage; Amazon Computers remains excluded by the measured Phase 3B cost; and
ogbn-arxiv still requires sparse directed time-respecting nulls.

These choices follow the archived gnn-benchmark dataset family and the heterophilous-graphs audit:

* https://github.com/shchur/gnn-benchmark
* https://arxiv.org/abs/2302.11640

No additional dataset may be promoted to confirmatory status using the Phase 3C results. A future
phase must freeze a mechanical selection/cost rule and keep exploratory development separate.

## 8. Updated novelty audit

`docs/novelty_audit.md` now includes Phase 3C. Feature/topology dependence, clustering, multi-hop
neighbourhood descriptors, community/feature rewiring, heterophilous datasets, Holm, sign-flip
randomization, and block bootstrap all have clear precedents and are not claimed as novel. Relevant
prior work includes Lee et al. on A-X dependence, localized topological features, community/feature
rewiring, and Platonov et al.'s heterophily audit:

* https://proceedings.mlr.press/v235/lee24m.html
* https://jmlr.org/papers/volume26/23-1424/23-1424.pdf
* https://proceedings.mlr.press/v325/rubio-madrigal26a.html
* https://arxiv.org/abs/2302.11640

The remaining contribution claim is narrow: the declared-lattice estimand and simultaneous
frontier sandwich. Phase 3C again fails to demonstrate that this formulation yields a distinctive
real-world frontier statement. It does demonstrate a reproducible broader specificity
certificate and substantial adaptive cost savings.

## 9. Final conclusion

The original GraphSAGE calibration flag did not replicate under a better block-aware audit, all
new nulls are admissible, and cost is manageable. Those are positive validation results. They are
not enough for GO: the targeted real-world lattice still produces no certified or possible
frontier member and no non-monotonicity, while the secondary CiteSeer calibration raises an
additional small-sample warning.

Following the frozen rule, the decision is **NO-GO for the full benchmark**. Recommended next work
is not to increase delta or add datasets opportunistically. It is to resolve small-sample
real-vs-null mean inference and, only under a new preregistration, test a mechanically selected
heterophilous dataset where structural sufficiency has a domain mechanism rather than merely a
hope of generating a non-empty frontier.
