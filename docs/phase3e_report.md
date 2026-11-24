# Phase 3E report: preregistered heterophilous pilot (Roman-empire, Amazon-ratings)

Date: 2026-11-24. Protocol: `docs/phase3e_protocol.md` (frozen; `outputs/phase3e/FREEZE.json`, 89 files).
Hyperion directory: `/scratch/hilmibukhori/rusa_3e`. Generated report: `outputs/phase3e/report/REPORT.md`.
Phases 3B–3D are untouched.

## Decision (frozen rule §8)

| Rule | Result | Verdict |
|---|---|---|
| E1 calibration | Uniform t+Holm FWER on A/A contrasts: no flag in any cell. Adaptive CRAF, Roman-empire GCN, b = 80: 1 of 3 disjoint groups (Wilson 0.06–0.79). Marginal size flag: Roman-empire GCN, n = 80, sufficiency direction, 4/30 (0.13; Wilson 0.05–0.30). Few independent groups; reported, not dismissed | pass for the primary (uniform) procedure; adaptive flag disclosed |
| E2 non-trivial frontier | Graph relevance holds for Roman-empire SAGE and both Amazon-ratings cells; in all three `cert_min = ∅`. Roman-empire GCN has `cert_min = {degree}` but fails graph relevance (graph hurts), so it is labelled trivial | **fail** |
| E3 admissibility | Roman-empire 10/11, Amazon-ratings 9/11; all singletons admissible | pass |
| E4 cost | Confirmatory uniform CRAF (b = 80): 17.2 / 22.6 CPU-h (Roman GCN / SAGE), 18.4 / 23.1 CPU-h (Amazon GCN / SAGE); limit 60 | pass (the automated R4 = false is a NaN artefact from the unfitted inadmissible elements; recomputed from the pool) |
| **Decision** | E2 fails | **NO-GO for further real-world extension; no further dataset search** |

## Results

Reference clusters (300 per dataset), test score 1 − Brier/2 (accuracy):

| dataset | model | real | no graph | real − no graph |
|---|---|---|---|---|
| Roman-empire | GCN | 0.634 (0.433) | 0.760 (0.646) | −0.127 |
| Roman-empire | SAGE | 0.822 (0.747) | 0.760 (0.646) | +0.062 |
| Amazon-ratings | GCN | 0.656 (0.426) | 0.644 (0.389) | +0.012 |
| Amazon-ratings | SAGE | 0.662 (0.441) | 0.644 (0.389) | +0.018 |

CRAF (confirmatory and reference agree in every cell):

| cell | A / C / I | cert_min | possible_min | closest admissible element (Delta) |
|---|---|---|---|---|
| Roman GCN | 0 / 10 / 1 | {degree} | {degree} | all Delta in [−0.016, −0.011] |
| Roman SAGE | 10 / 0 / 1 | ∅ | {fsim+hop2} (inadmissible, unresolved) | clust+fsim 0.0229 |
| Amazon GCN | 9 / 0 / 2 | ∅ | {clust+fsim, fsim+hop2} (inadmissible) | block+fsim 0.0133 |
| Amazon SAGE | 9 / 0 / 2 | ∅ | {clust+fsim, fsim+hop2} (inadmissible) | block+fsim 0.0146 |

Interpretation:

1. **No admissible combination is sufficient wherever the graph helps.** Closest gaps are 2.7×
   (Amazon GCN), 2.9× (Amazon SAGE) and 4.6× (Roman SAGE) the margin.
2. **Specificity is not certified on the heterophilous graphs**, because inadmissible elements have no
   data and remain possibly minimal. This is the intended behaviour of CRAF: an untestable combination is
   reported as unresolved, not silently dropped.
3. **Roman-empire GCN.** The plain GCN is far worse with the graph than without it (−0.127). CRAF
   certifies the degree-only null as sufficient: degree-preserving random graphs reproduce the real
   graph's (harmful) performance within the margin, and every rewired graph is in fact slightly *less*
   harmful (Delta ≈ −0.013). The loss is generic to aggregating over this degree structure, not caused
   by specific edges. Under the frozen graph-relevance rule this frontier is "trivial" for E2.
4. **Roman-empire SAGE.** Only feature-similarity combinations recover part of the gain (Delta 0.023–0.028
   vs 0.061–0.064 for the others, ≈ the no-graph gap 0.062): degree, community, clustering and two-hop
   preservation explain nothing.
5. **Amazon-ratings GCN.** Every admissible null graph scores *below the no-graph model*
   (Delta_S 0.013–0.019 > real − no graph 0.012): randomised graphs with the same coarse structure hurt.
6. **Non-monotonicity.** 11 pairs with Delta_T > Delta_S (S ⊂ T) are Holm-certified, all in Roman GCN
   where every Delta is negative: nulls that preserve more structure move closer to the (worse) real
   graph. This is monotone in closeness to G0, and no pair crosses the margin, so no natural
   non-monotonicity relevant to sufficiency was found.
7. Interactions: mostly significant but tiny (|I| ≤ 0.004). GCN − SAGE differences all significant.
8. Comparators: on the confirmatory block every procedure reports the same frontier; ni_holm leaves all
   11 elements unresolved in the three graph-relevant cells, while CRAF certifies 9–10 as insufficient.
   Adaptive CRAF used the full 960 fits here (no saving: the stage-2 allocation did not saturate).

## Disclosures

* Pre-freeze (label-free, before scores): E4 threshold set from the timing probe; attempt budget not
  raised; split 50/25/25 per class; dense input path.
* Execution: 204 of 800 tasks failed instantly on two nodes (hyperion-187/188, "Illegal instruction",
  before any computation) and were re-run unchanged on other nodes (job 8209246). Pool: 800/800,
  2,400 files hashed in `outputs/phase3e/POOL_SHA256SUMS.txt`. Total pool cost ≈ 854 CPU-h.
* The automated report's R4 and cost table are affected by NaN fit times of inadmissible elements;
  costs above are recomputed from the pool.

## Post-hoc calibration audit (after the freeze; does not change any decision)

Scripts and outputs: `/scratch/hilmibukhori/rusa_posthoc/` (kept outside the frozen `rusa_3e` tree,
whose freeze still verifies), local copies in `outputs/posthoc/`. 5,000 random subsets of reference
clusters per cell and n ∈ {20, 40, 80}.

* Centred A/A contrasts (finite-sample mean removed): one-sided size 0.025–0.050 in every cell, so the
  t approximation itself is not anti-conservative.
* Mean-zero (exchangeability) check: smallest Bonferroni p per cell ≥ 0.12; pooled p ≥ 0.13.
* Uncentred FWER of uniform CRAF at n = 80: 0.020–0.050 on Cora, CiteSeer and Amazon-ratings;
  0.072 (GCN) and 0.085 (SAGE) on Roman-empire, with GCN advantage-direction size rising in n
  (0.067 / 0.075 / 0.088). Consistent with a chance mean deviation of the 300-cluster reference sample
  (max |t| = 2.5) amplified by subsampling; a small genuine miscalibration cannot be excluded.
* Every confirmatory real-graph certification has |T| ≥ 25.7 and p ≤ 2e-40 (Holm thresholds
  0.0023–0.0042), so no decision depends on fine calibration.
