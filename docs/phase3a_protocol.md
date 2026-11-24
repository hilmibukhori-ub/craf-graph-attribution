# Phase 3A protocol (CRAF proof of concept): frozen before execution

Written 2026-11-24. `outputs/phase3a/FREEZE.json` hashes the code, the config and the batch files.
The run happens in a separate Hyperion directory, `/scratch/hilmibukhori/rusa_3a`.

Earlier phases are preserved:
* Phase 2A–2C directories and outputs are read-only. Reused pools are loaded from
  `/scratch/hilmibukhori/rusa_2b` and `/scratch/hilmibukhori/rusa_2c` and are never written.
* `fullset_adaptive_fb` remains the RUSA default. It was selected **after** the Phase 2C results
  (`docs/phase2c_report.md` §9), and CRAF's adaptive mode inherits its settings: `n_min = 5`,
  stage-1 share 1/3, `w1² = 1/3`, and an a-priori feasibility fallback.

## 0. Development observations (before freezing; not results)

| Observation | Consequence |
|---|---|
| A scan of all existing Phase 2A–2C Monte Carlo truths (SGC, SAGE) found **no** pair S ⊂ T with Delta_T meaningfully > Delta_S (threshold max(4 MC-SE, 0.002)) | Within these DGPs and models, performance is empirically monotone in the constraint lattice. Non-monotonicity is therefore tested on **semi-synthetic Delta tables** with realistic noise, not on a contrived graph world. A natural non-monotone graph mechanism, such as harmful heterophily for GCN, was considered but not built: it is fragile, and GCN did not learn the edge term in Phase 2C |
| First test run on Hyperion: 1 failure. The test assumed b = 6 is infeasible, which is true only with `n_min = 5` | The adaptive default `n_min` was set to 5, matching `fullset_adaptive_fb`. No procedure logic changed |

## 1. Questions

1. Does CRAF control the FWER of its certifications (advantage, sufficiency) and give a valid
   frontier statement (`cert_min ⊆ F ⊆ possible_min`) on real pipeline contrasts and in
   non-monotone, interaction and multiple-minimum settings?
2. How often does it recover the true frontier exactly, compared with the baselines below?
3. Does adaptive allocation improve exact recovery or reduce inconclusiveness at matched budget,
   without losing validity?

## 2. Settings (fixed)

* delta = 0.005 (equal to eps in Phases 2B/2C), alpha = 0.05, one-sided t marginal tests.
* Lattice: all subsets of order 0–2 of {block, w1, w2, w3, w4}, so |L| = 16. Element `{}` is the
  degree null.
* Budget B = b (1 + |L|), with b ∈ {20, 40, 80}. One experiment is a block of 100 independent
  instances.
* Adaptive mode: R1 = round(b/3), minimax-power allocation at level alpha/(2|L|), `n_min = 5`,
  relevance screening (supersets of an element with stage-1 `mean + 2 se < delta` get `n_min`),
  and the inverse-normal combination.
* Truth: Monte Carlo Delta from the full pool; A/A elements are exactly 0. `F` is the set of
  minimal elements of {S : Delta_S < delta}.

| Pool | Source | Role | Experiments |
|---|---|---|---|
| S7_hard (SGC) | 2C, reused | interaction: F = {w1+w2}, singletons insufficient, hard decoys | 144 |
| S7_easy (SGC) | 2C, reused | interaction, easy | 144 |
| S8_small_hard (SGC) | 2C, reused | no sufficient element: certified relational specificity | 72 |
| N6_hard (SGC) | 2B, reused | many sufficient elements (every element containing w3), one minimal: F = {w3} | 144 |
| S7_hard (SAGE) | 2C, reused | neural replication of the interaction | 72 |
| **P3_multi (SGC)** | **new**, seed 20261222, 7,200 instances | two minimal combinations: F = {w3} and {w1+w2} (w3 = u exactly) | 72 |
| SS_boundary | semi-synthetic, 7-element lattice over {a, b, c} | all Delta = delta: worst-case FWER | 2000 |
| SS_nonmono_A | semi-synthetic | F = {∅}, while {a} is insufficient and {a, b} sufficient again | 2000 |
| SS_nonmono_B | semi-synthetic | F = {a, b+c}, with {a, b} ⊃ {a} insufficient | 2000 |
| SS_near | semi-synthetic | elements near the margin (0.002, 0.008) | 2000 |

Semi-synthetic noise: t-distributed with 5 df, scaled to sd 0.012 (close to the pool contrast
sd), independent across elements.

## 3. Procedures (same data and budget)

`craf`, `craf_adaptive`, `craf_children` (ablation: minimality checked against immediate subsets
only, which implicitly assumes monotonicity), `ni_holm` (standard Holm-adjusted non-inferiority,
reporting minimal-among-certified), `factorial_unadj` (exhaustive factorial with unadjusted
per-element tests), `naive_point` (point-estimate frontier), and `pcga_l` (ladder-implied level;
pool mode only).

## 4. Outcomes and decision rules (fixed before results)

* **Validity (primary).** For `craf` and `craf_adaptive`:
  * The class-error rate (any false advantage or sufficiency certification) is ≤ 0.05; flag if
    the Wilson lower limit > 0.05.
  * The false-frontier-member rate is ≤ 0.05; same flag.
  * The coverage `F ⊆ possible_min` is ≥ 0.95.
* **Comparators.** Report their false-member and exact-recovery rates. PCGA-L is judged only on
  whether its ladder-implied level is truly sufficient. Its ladder cannot express {w1+w2} or
  {w3}, which is a statement about scope, not validity.
* **Adaptive.** Paired `craf_adaptive − craf` on exact recovery and on the number of inconclusive
  elements.
* **Decision.**
  * **GO** (a methodological contribution worth developing) requires all of:
    * no validity flag;
    * CRAF's frontier statement differs materially from what the standard approach (`ni_holm`
      plus "minimal among certified") gives. Specifically, `ni_holm`'s false-member rate exceeds
      0.05 in at least one setting where CRAF's does not, or CRAF provides certified minimality
      that the standard approach cannot;
    * reasonable exact recovery (≥ 0.5) at the largest budget in the pipeline PoCs.
  * **CONDITIONAL GO** if validity holds but the advantage over the standard approach is confined
    to particular regimes, or recovery needs impractical budgets.
  * **NO-GO** if there is a validity flag, or CRAF adds nothing beyond `ni_holm` plus a
    post-processing rule that is standard in set identification.
