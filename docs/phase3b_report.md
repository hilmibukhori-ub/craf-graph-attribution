# RUSA Phase 3B — real-world pilot of CRAF (Cora)

Date: 2026-11-24. Status: **pilot complete.** The full benchmark was not started.

**Frozen decision rule: NO-GO for the full benchmark as designed.** Two things trigger it:
* R1 is not met: one marginal-calibration cell is flagged (§5).
* R3 is met only through the weak category (d), certified specificity (§6).

The CRAF guarantees themselves held on real contrasts. The worst-case FWER of certifications showed
no flag in any cell. However, on Cora no admissible property combination comes anywhere near
sufficiency, so the frontier part of CRAF, the part that differs from standard practice, was never
exercised. The recommendation for what to do next is in §8. The questions were not revised after
the results.

Documents:
* frozen protocol: `docs/phase3b_protocol.md` (a copy and its sha256 are in `outputs/phase3b/`);
* method (unchanged from Phase 3A): `docs/craf_math.md`;
* code: `src/rusa/realworld/` (data, label-free attributes, multi-class models, pool, analysis),
  plus `scripts/prepare_phase3b.py`, `run_pool_3b.py`, `run_phase3b.py`, `make_report_3b.py`;
* tests: `tests/test_phase3b.py` (11 tests); **116/116 pass on Hyperion** (job 8198866) on the frozen
  code;
* results: `outputs/phase3b/report/`. This holds `REPORT.md`, `frontiers.png`,
  `frontier_summary.csv`, `resampling_summary.csv`, `paired_differences.csv` and
  `decision_inputs.json`. `outputs/phase3b/analysis/` holds every per-analysis CSV, and
  `outputs/phase3b/admissibility/` holds the label-free audits.

## 1. What was done

| Task | Done |
|---|---|
| 1 Datasets | **Cora** run in full: GCN and GraphSAGE, 1,500 replicate clusters. **Amazon Computers**: label-free admissibility audit done (all 11 elements admissible), but not run, because the timing probe showed ~200–365 s per fit, i.e. ~4 CPU-h per cluster (protocol §0, §9). **ogbn-arxiv**: feasibility assessment only |
| 2 Models and baselines | GCN and SAGE (multi-class, hidden 64), each with a matched no-graph version, plus a feature-only MLP. GCN-no-graph equals the MLP exactly: same layers and initialisation, identity operator |
| 3 Admissible properties | label-free `deg`, `block` (Louvain), `feat` (feature clusters), `dlen` (document length). Lattice: orders ≤ 2, so `|L| = 11`. Pre-declared admissibility audit; leakage tests; class labels never used as strata. No temporal constraints apply to Cora |
| 4 Calibration | exact A/A contrasts from the second null draw on 1,400 fresh clusters (the confirmatory block is excluded), plus centred real contrasts |
| 5 Comparators | PCGA-L, exhaustive factorial (unadjusted), naive point estimates, Holm non-inferiority with naive minimality, immediate-subset certification; on the confirmatory block and on 14 resampling blocks |
| 6 Structure | non-monotonicity over all 32 comparable pairs, 6 pairwise interactions, GCN − SAGE paired differences |
| 7 Reporting | certified and possibly minimal frontiers, gap sets, inconclusive counts, simultaneous intervals, costs |
| 8 Adaptive allocation | `craf_adaptive` vs `craf`; `fullset_adaptive_fb` (frozen default) vs exhaustive IUT; matched budgets |
| 9 Informativeness audit | §6 |

**Execution and disclosures.**

| Item | Detail |
|---|---|
| Hyperion | `/scratch/hilmibukhori/rusa_3b`; earlier phase directories untouched |
| Jobs | label-free prep 8198276; tests 8198369/8198415/8198430 (test-code bugs fixed: a toy fixture and a DataFrame `.T` name clash), 8198431 (116 pass, before the model speed-up) and 8198866 (116 pass, frozen code); timing probe 8198683; pool 8198868 (300 tasks, all COMPLETED; 900 pool files with sha256 in `POOL_SHA256SUMS.txt`); analysis 8198869 |
| Pre-freeze changes (protocol §0) | `attempt_factor` 200 → 1000 after the label-free audit; sparse input layer after the first smoke was too slow; Amazon removed after the timing probe. No score was inspected before freezing |
| Change after freeze | only `scripts/make_report_3b.py`. matplotlib is not available on Hyperion, so figure generation was made optional; tables were produced on Hyperion (`REPORT_hyperion.md`) and figures locally from the same CSVs. The tables are identical. The analysis outputs come from the frozen code (freeze verified in the job log) |
| Post-hoc diagnostic | §5: the rejection pattern behind the flagged calibration cell. Exploratory, not part of any decision |

## 2. Baselines (reference clusters, n = 1,400; test 1 − Brier/2, accuracy)

| | GCN | SAGE |
|---|---|---|
| real graph | 0.838 (acc 0.801) | 0.836 (acc 0.784) |
| matched no-graph | 0.699 (acc 0.565) | 0.699 (acc 0.566) |
| feature-only MLP | 0.699 (acc 0.565) | 0.699 (acc 0.565) |

The accuracies are in the usual range for Cora with 20 labels per class on random splits
(Shchur et al. 2018).

## 3. Frontiers (Q2)

`Delta_S` is the real-graph score minus the score under null `N_S`. The intervals are the reference
estimates with Bonferroni-simultaneous 95% intervals (all half-widths ≤ 0.0007).

| N_S preserves (beyond degrees) | GCN `Delta_S` | SAGE `Delta_S` | status (reference and confirmatory) |
|---|---|---|---|
| nothing (degree null) | 0.249 | 0.178 | advantage |
| deg / dlen | 0.247 / 0.248 | 0.178 / 0.178 | advantage |
| feat | 0.187 | 0.146 | advantage |
| block | 0.122 | 0.098 | advantage |
| block+deg / block+dlen | 0.118 / 0.117 | 0.094 / 0.095 | advantage |
| deg+feat / dlen+feat | 0.162 / 0.160 | 0.132 / 0.131 | advantage |
| deg+dlen | 0.239 | 0.176 | advantage |
| **block+feat** | **0.081** | **0.071** | advantage |

* **Certified result, for both architectures.** The confirmatory run (block 0, b = 80, 960 fits)
  and the reference run agree:
  * all 11 elements are certified advantage;
  * `cert_min = possible_min = ∅`;
  * there are no gap sets and no inconclusive elements.

  So **relational specificity over L is certified**: no admissible combination of these label-free
  properties reproduces the real graph's performance within δ = 0.005. Adaptive CRAF reaches the
  same certificate with 520 instead of 960 fits.
* **Where the closest element sits.** Even block+feat leaves 0.081 (GCN) and 0.071 (SAGE), about
  15× the margin. Relative to the degree null, block+feat removes 67% (GCN) and 60% (SAGE) of the
  advantage.
* **Attribution pattern.**
  * Communities (`block`) carry the largest share.
  * Feature clusters add to it.
  * Degree mixing and document length add almost nothing. `dlen` was declared in advance as a
    control property and behaves as one.
* **Label association (post hoc, descriptive only).** `block` has NMI 0.38 with the labels and
  edge-level attribute homophily of 0.90 (label homophily is 0.81). `feat` has NMI 0.13.

`outputs/phase3b/report/frontiers.png` shows the lattice and the forest plot for each
architecture.

## 4. Comparators and adaptive allocation (Q4, Q5)

* **Confirmatory block.** Every procedure reports an empty frontier:
  * `ni_holm`, because it has no certified-sufficient element, so its 11 elements are reported as
    "not sufficient" without an insufficiency certificate;
  * `naive_point`, because no estimate is below δ;
  * `pcga_l`, because its edge step is supported, so no ladder level suffices.

  CRAF's output differs from the standard approach only in being **affirmative**: 11 certified
  insufficiencies, i.e. a specificity certificate. That is criterion (d).
* **Resampling (14 blocks × 3 budgets × 2 architectures).** Exact recovery is 1.00 for every
  procedure, and there are no false members and no class errors. With the truth this far from the
  margin, the frontier problem is trivial, and the comparison cannot discriminate between
  procedures. The Wilson upper bound with 14 experiments is 0.215.
* **Adaptive CRAF vs uniform.**
  * Exact recovery and inconclusiveness: no difference (both at the ceiling).
  * Cost: the same certificate for 520 vs 960 fits at b = 80, and 380 vs 480 at b = 40.
* **RUSA full-set claim.**
  * `exhaustive_iut` and `fullset_adaptive_fb` both claim in 14/14 experiments at every budget,
    with 0 false claims (θ_full = 0.081 GCN, 0.071 SAGE).
  * `fullset_adaptive_fb` uses 56 vs 168 fits at b = 12, and 112 vs 336 at b = 24. At b = 6 it
    falls back (a-priori rule) to exhaustive IUT.
  * The paired claim difference is 0. The adaptive gain shows up only as cost, not as power,
    because power is at its ceiling.

## 5. Calibration on fresh clusters (Q1)

**Primary FWER check (frozen R1, part 1): no flag in any cell.** Worst case: every element at the
boundary, exact A/A contrasts.

| | GCN | SAGE |
|---|---|---|
| craf, disjoint, n = 20 / 40 / 80 | 0.071 / 0.057 / 0.118 (70 / 35 / 17 groups) | 0.086 / 0.029 / 0.059 |
| craf_adaptive, cluster bootstrap (2,000), b = 20 / 40 / 80 | 0.053 / 0.046 / 0.054 | 0.048 / 0.042 / 0.046 |
| craf_adaptive, disjoint (14 blocks) | 0.071 / 0.071 / 0.071 | 0.071 / 0.143 / 0.143 |
| craf, centred real contrasts (secondary) | 0.029 / 0.029 / 0.059 | 0.043 / 0.029 / 0.000 |

* Wilson lower limits are all < 0.05.
* The disjoint-group FWER estimates are imprecise: there are only 17 groups at n = 80. The
  bootstrap estimates (2,000 replicates each) are close to the nominal 0.05.

**Marginal size (frozen R1, part 2): one flag.** At α = 0.05 there are 20 cells (2 architectures ×
5 group sizes × 2 directions). 19 are within tolerance; the size ranges over 0.029–0.059.
**SAGE, n = 80, sufficiency direction: size 0.102** (19 of 187 tests; Wilson 95% interval
0.066–0.153).

**Post-hoc diagnostic** (exploratory; not part of the decision):
* The 19 rejections are spread over 11 of the 17 groups and over elements. A/A contrasts are
  essentially uncorrelated across elements (mean correlation 0.004), so the 187 tests are close to
  independent, and the flag is not an artefact of pooled correlated tests.
* The same architecture at n = 80 in the advantage direction gives 0.059, and at n ≤ 40 in the
  sufficiency direction 0.048–0.052.
* For 20 cells, a binomial tail probability is 0.0028 per cell, about 0.056 after Bonferroni adjustment. So chance is
  plausible but not established.
* A/A contrasts are symmetric by construction, which makes a systematic one-directional failure
  of the t-test unlikely. It is not excluded.

**Under the frozen rule this is a calibration flag, and R1 fails.**

## 6. Natural structure and informativeness (Q3, task 9)

* **Non-monotonicity: none certified** (0 of 32 comparable pairs, with or without margin). Adding a
  constraint never increased `Delta_S` by more than 0.0001. This matches the synthetic phases:
  performance is empirically monotone in the constraint lattice. The Phase 3A advantage of CRAF
  over immediate-subset minimality (non-monotone settings) is therefore still validated only
  semi-synthetically.
* **Multiple sufficient combinations: none** (the frontier is empty).
* **Interactions: all 6 significant (Holm).** They are scientifically informative.
  * `block+feat` has a **positive** interaction: +0.022 for GCN and +0.005 for SAGE. Preserving
    communities and feature clusters together removes *less* than the sum of the two separately,
    i.e. the two properties partly encode the same information (redundancy).
  * `deg+feat` and `dlen+feat` have negative interactions (−0.023 / −0.026 for GCN): preserving
    feature clusters *jointly* with degree or length bins removes more than either alone.
* **Architecture differences: all 12 significant.** GCN's advantage over each null exceeds SAGE's.
  The gap is largest for the degree null (+0.071) and smallest for block+feat (+0.010). GCN depends
  more on the specific edges than SAGE, although their real-graph scores are nearly equal. SAGE's
  separate self-weight lets it rely less on neighbour information.
* **Informativeness (R3).**
  * (a) No certified-minimal element outside the PCGA-L ladder, because there is no certified
    frontier member at all.
  * (b) `ni_holm`'s reported frontier equals CRAF's (both ∅).
  * (c) No certified non-monotonicity.
  * (d) Certified specificity over L, for both architectures.

  **R3 holds only via (d).** What CRAF adds on Cora over PCGA-L is a *broader* certified negative.
  PCGA-L only certifies that G0 beats the block-preserving null. CRAF certifies that G0 beats
  every combination of order ≤ 2 of four label-free properties, and quantifies how far each one is
  from sufficiency, with interactions. This is meaningful, but it is a full-set specificity claim
  (RUSA Phases 2B–2C) with a lattice-shaped report, not a frontier finding.

## 7. Cost (Q6)

* **Cora.** One fit takes 3.3–5.8 s (GCN) or 6.6–7.8 s (SAGE). Null generation takes
  0.004–0.29 s, which is negligible.
* **Confirmatory CRAF at b = 80:** 1.2 CPU-h (GCN) and 1.9 CPU-h (SAGE). R4 is met.
* **The whole pilot** (1,500 clusters × 51 fits) took about 140 CPU-h, about 25 min of wall time
  on 300 cores.
* **Amazon Computers:** about 4 CPU-h per cluster. A pilot of the same shape (100 confirmatory +
  500 reference clusters) would cost about 2,400 CPU-h.
* **ogbn-arxiv** needs three engineering items before it is feasible:
  * a sparse swap kernel (the dense adjacency would take 28.7 GB);
  * time-respecting directed nulls;
  * the OGB temporal split instead of random clusters.

  Fit cost per cluster is expected to exceed Amazon's.

## 8. Recommendation for the full cross-domain benchmark

| Rule | Outcome |
|---|---|
| R1 calibration | **fails**: FWER check has no flag, but the marginal size has 1 flag of 20 cells (SAGE, n = 80, sufficiency direction, 0.102) |
| R2 admissibility | passes (all 11 elements admissible on Cora and on Amazon Computers) |
| R3 informativeness | only (d): certified specificity; no frontier finding, no non-monotonicity |
| R4 feasibility | passes on Cora (≤ 1.9 CPU-h); Amazon / arxiv need engineering (§7) |
| **Frozen decision** | **NO-GO** for the full benchmark as designed |

Assessment beyond the frozen rule:
1. **The calibration flag is probably, but not certainly, chance.** It is one cell of 20, in the
   less important marginal check. The procedure-level FWER, the quantity CRAF actually guarantees,
   was not flagged anywhere, and the bootstrap FWER is close to 0.05. However, the frozen rule
   treats it as a failure, and we do not override it. A cheap, pre-registered replication on fresh
   clusters would settle it: SAGE only, n = 80, about 1,500 new clusters, about 75 CPU-h.
2. **The more important finding is substantive.** On Cora, the standard label-free structural
   properties are an order of magnitude away from sufficiency. With such a lattice, CRAF's
   frontier reduces to the RUSA full-set specificity claim. Its distinctive outputs never appear:
   certified minimality vs "minimal among certified", gap sets, and robustness to
   non-monotonicity. Scaling the same design to more datasets would most likely repeat this
   pattern at a high cost.
3. **What would make a benchmark informative** must be specified and frozen *before* running,
   rather than tuned to this result. Options to review:
   * properties expected to approach sufficiency, e.g. finer communities, label-free
     feature-similarity strata at several resolutions, or joint block × feat at order 3;
   * a scientifically justified larger margin δ, fixed in advance and not chosen from these
     estimates;
   * datasets where structure is known to matter less, such as heterophilous or low-homophily
     graphs, so that sufficiency is plausible.

   Any of these is a new pre-registered phase, not a revision of this one.

**Summary.** CRAF behaved correctly on real data:
* no FWER flag;
* a coherent, reproducible certificate that is identical in the confirmatory and reference runs;
* adaptive savings of 40–67% of fits for the same certificate.

But the pilot gives no real-world evidence yet that the frontier formulation produces findings
that standard evaluation does not. Following the frozen rule, we do not recommend starting the full
benchmark. We recommend reviewing the options in point 3 and the calibration replication in point 1
first.

Sources (new in this phase; the rest are in `novelty_audit.md`):
* Shchur et al. 2018: https://arxiv.org/abs/1811.05868
* Ma et al. 2022: https://arxiv.org/abs/2106.06134
* Platonov et al. 2023: https://arxiv.org/abs/2209.06177
* Bechler-Speicher et al. 2024: https://proceedings.mlr.press/v235/bechler-speicher24a.html
