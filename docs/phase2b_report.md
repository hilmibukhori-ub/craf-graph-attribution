# RUSA Phase 2B — targeted novelty validation: report and decision

Date: 2026-11-24. All numbers come from generated files:
* `outputs/phase2b/report/REPORT.md` (tables), `summary.csv`, `paired_differences.csv`,
  `truth_summary.csv`, and figures `claim_rate_vs_budget.png`, `discovery_vs_budget.png`,
  `coverage_vs_budget.png`;
* raw per-experiment rows in `outputs/phase2b/analysis/phase2b_<scenario>.csv.gz`.

The protocol was frozen before execution (`docs/phase2b_protocol.md`, `docs/phase2b_math.md`,
`outputs/phase2b/FREEZE.json`). Phase 2A outputs are untouched.

## 1. What was executed

| Item | Status |
|---|---|
| New code | `inference/allocation.py` (minimax-power allocation, two-stage and adaptive full-set certificates), `evaluation/phase2b.py` (9 procedures), random search in `nulls/search.py`, S6/N6 DGPs in `data/synthetic.py`, `scripts/run_phase2b.py`, `scripts/make_report_2b.py`, Hyperion batch files |
| Tests | 64 pass locally; 64 pass on Hyperion with numba, so the numba ≡ Python swap-kernel test ran; Phase 2A instance regression hashes unchanged |
| Freeze | 41 files hashed; verified by all 480 pool tasks and by the analysis job |
| Pool (Hyperion job 8188699) | 57,600 independent instances (4 × 7,200 S6 + 2 × 14,400 N6) × (real + empty + 48 nulls × 2 draws) ≈ 5.6 M model fits; 0 audit failures; median 85 s per 120-instance task with numba |
| Analysis (job 8188700) | 6 scenarios × 5 (K, budget) settings × 2 eps × 9 procedures; 60 (S6) or 120 (N6) independent experiments per cell |
| Raw pool | on Hyperion `/scratch/hilmibukhori/rusa_2b/outputs/phase2b/pool` (322 MB; sha256 in `outputs/phase2b/POOL_SHA256SUMS.txt`) |

Not executed: neural models in Phase 2B (SGC-ridge only), real data (outside the scope of this phase), and a
systematic literature search (targeted review only).

**Disclosed pre-freeze design change.** The development smoke run (seed 515151) showed that a
full-set allocation that discards stage-1 data, with `n_min = 3`, is almost powerless. Before the
freeze we replaced it with the minimax-power rule (`n_min = 5`) and added `fullset_adaptive`. The
ablations `fullset_alloc` and `fullset_elim` were kept. No frozen-seed data were seen before this
change.

## 2. Scenario truths (S6 and N6 behave as designed)

| scenario | θ_full | Δ_empty | binding null | nearest non-w3 decoy (K18 / K48) | θ_menu (PCGA-L menu) |
|---|---|---|---|---|---|
| S6_large_hard | 0.0149 | 0.0275 | strat:block+w3 (5 w3-arms within 0.002 for K18; 9 for K48) | 0.0241 / 0.0186 | 0.0275 |
| S6_large_easy | 0.0161 | 0.0260 | strat:block+w3 | 0.0403 / 0.0402 | 0.0260 |
| S6_small_hard | 0.0075 | 0.0211 | strat:block+w3 | 0.0174 / 0.0116 | 0.0211 |
| S6_small_easy | 0.0084 | 0.0187 | strat:block+w3 | 0.0331 / 0.0331 | 0.0187 |
| N6_hard | 0 (exact A/A on strat:w3) | 0.0143 | strat:w3 family | 0.0111 / 0.0045 | 0.0143 |
| N6_easy | 0 (exact) | 0.0108 | strat:w3 family | 0.0254 / 0.0254 | 0.0108 |

In every S6 scenario:
* the binding comparator is a **hidden placebo**, not the empty graph;
* `θ_full > eps = 0.005`;
* the PCGA-L menu overstates the robust effect by 0.010–0.013.

In N6, θ_full = 0 while every null outside the w3 family is beaten.

**Design limitation found.** The "binding null" is a *family*: every w3-containing stratification
(5 arms in K18, 9 in K48) lies within 0.002 of θ_full. Hitting any of them counts as discovery, so
screening was easy even in the "hard" (q = 0.10) conditions (§4).

## 3. Validity (type I error vs the full candidate set; N6, θ_full ≤ 0)

| procedure | scope | max N6 claim rate over all 10 cells, eps = 0.005 | same, eps = 0 (exact boundary) |
|---|---|---|---|
| exhaustive_iut, fullset_alloc, fullset_elim, fullset_adaptive | full | **0.000** (0/120 per cell; Wilson upper ≤ 0.031) | **0.000** |
| screen_random | selected | 0.008 | 0.033 |
| screen_uniform | selected | 0.000 | 0.033 |
| screen_sh | selected | 0.008 | 0.033 |
| oracle_select | selected (oracle) | 0.000 | 0.075 (a selected-set test exactly at its boundary; consistent with alpha, 120 exps) |
| **pcga_l** | L3 only | **1.000** | **1.000** |

* **PCGA-L certifies a non-existent robust effect in every N6 experiment.** Its menu lacks the
  w3-preserving null. This replicates and sharpens the Phase 2A S4/S5 finding.
* **All full-set procedures control type I error**, and are conservative at the exact boundary.
* **Selected-set screens did not over-claim here** (≤ 0.033 even at eps = 0), because discovery was
  ≥ 0.98 in N6 (§4). With the observed discovery rates this negative control did **not** stress
  the screens. A harder N6, with a single, isolated binding null, is required (§7).

## 4. Discovery of the binding null (selected set / top-allocated comparator within 0.002 of θ_full)

* Screens:
  * N6: ≥ 0.983 in every cell;
  * S6: 0.933–1.000;
  * SH vs random: +0.067 [0.003, 0.130] in S6_small_hard K48 (b = 6 and 12); all other cells
    have CIs containing 0;
  * SH vs uniform: +0.067 [0.003, 0.130] in S6_small_hard K48 b = 6 only.
* Full-set allocation (top-allocated comparator): 0.37–1.00. These procedures do **not** need
  discovery for validity; misallocation only costs power.

## 5. Power at equal fit budget (S6, θ_full > eps)

eps = 0.005 (primary). Claim rates (60 experiments per cell):

| scenario / K / b (budget) | exhaustive | fullset_alloc | fullset_elim | **fullset_adaptive** | screen_sh (selected) | oracle_select |
|---|---|---|---|---|---|---|
| large_hard K18 b12 (240) | 0.450 | 0.183 | 0.250 | 0.517 | 0.967 | 1.000 |
| large_hard K18 b24 (480) | 0.733 | 0.417 | 0.783 | **0.900** | 1.000 | 1.000 |
| large_hard K48 b12 (600) | 0.333 | 0.117 | 0.133 | **0.483** | 1.000 | 1.000 |
| large_easy K18 b12 | 0.550 | 0.400 | 0.433 | **0.717** | 1.000 | 1.000 |
| large_easy K18 b24 | 0.850 | 0.617 | 0.917 | **1.000** | 1.000 | 1.000 |
| large_easy K48 b12 | 0.467 | 0.233 | 0.333 | **0.733** | 1.000 | 1.000 |
| small_hard K18 b24 | 0.067 | 0.017 | 0.050 | 0.083 | 0.350 | 0.583 |
| small_easy K18 b24 | 0.117 | 0.133 | 0.217 | **0.317** | 0.617 | 0.850 |
| any scenario, b = 6 | 0.000–0.183 | 0 (infeasible) | 0 (infeasible) | 0 (infeasible) | 0.117–1.000 | 0.267–1.000 |

**Paired difference fullset_adaptive − exhaustive_iut** (95% CI), eps = 0.005:
* large_easy:
  * K18 b12: +0.167 [0.042, 0.291];
  * K18 b24: +0.150 [0.059, 0.241];
  * K48 b12: +0.267 [0.145, 0.389].
* large_hard:
  * K18 b24: +0.167 [0.072, 0.262];
  * K48 b12: +0.150 [0.012, 0.288];
  * K18 b12: +0.067 [−0.055, 0.189].
* small_easy K18 b24: +0.200 [0.070, 0.330].
* small_hard: no detectable difference (all CIs contain 0).
* At **b = 6: −0.03 to −0.18**, worse, because the `n_min = 5` floor makes full-set allocation
  infeasible for 19–49 comparators.

At eps = 0 the gains are larger and broader: +0.10 to +0.30 at b ≥ 12. Examples:
* small_hard K18 b24: +0.300 [0.183, 0.417];
* small_hard K48 b12: +0.183 [0.032, 0.334].

**Ablation (what produces the gain).**
* `fullset_alloc` (stage 1 used only for allocation) is *worse* than exhaustive in every
  large-effect cell, by −0.15 to −0.32.
* `fullset_elim` is roughly equal to exhaustive.
* `fullset_adaptive` − `fullset_elim`: +0.27 to +0.40 at b = 12 and +0.08 to +0.12 at b = 24.

The gain therefore comes from **reusing stage-1 data via the inverse-normal combination test,
together with power-equalising allocation**. Allocation alone is not enough.

**Search algorithm.** `screen_sh` − `screen_uniform` and `screen_sh` − `screen_random` claim rates:
* no positive difference in any cell;
* in small_hard, SH is *lower* than random by 0.12–0.22, with CIs excluding 0. Random search
  misses the binding family more often and then confirms against a weaker null. That inflates its
  selected-set claim rate; it is not real power.

## 6. Estimation and coverage of θ_full

| procedure | bias of θ̂ − θ_full (range over cells, eps = 0.005) | RMSE range | coverage of θ_full |
|---|---|---|---|
| exhaustive_iut | −0.0014 … −0.0057 (min of many noisy means) | 0.0028 – 0.0084 | 0.983 – 1.000 |
| fullset_adaptive | −0.0008 … −0.0097 | 0.0021 – 0.0097 | 0.992 – 1.000 |
| screen_sh / uniform / random | −0.0011 … +0.0003 | 0.0011 – 0.0043 | 0.900 – 1.000 (random lowest; no full-set guarantee) |
| oracle_select | −0.0001 … +0.0005 | 0.0012 – 0.0028 | 0.917 – 0.967 |
| pcga_l (edge step) | +0.024 … +0.027 | 0.024 – 0.028 | — |

* Screen-then-confirm gives the most accurate *point* estimate of θ_full, because it averages
  over few comparators.
* Full-set procedures are conservative but downward-biased (winner's-curse-type min bias).
* PCGA-L overstates the robust effect by about 0.025, its menu gap.

## 7. Compute

* Every procedure used ≤ its budget B = b(2 + K) fits per experiment (`mean_fits` table).
* Measured Hyperion time per experiment was 0.2–3.5 s. It scales with fits; per-fit costs are
  nearly identical across procedures, and placebo generation with numba is negligible.
* The procedures therefore differ in *statistical* efficiency at equal fits, not in wall-clock
  cost per fit.
* Rough budget-equivalence from the claim-rate curves (`claim_rate_vs_budget.png`):
  * `fullset_adaptive` at B = 240 (K18) matches or exceeds `exhaustive_iut` at B = 240 and
    approaches its B = 480 power in the large-effect cells;
  * at K48 B = 600 it reaches 0.73 / 0.48 (easy / hard) against exhaustive 0.47 / 0.33.
  * This is not an exact sample-size ratio: only 2–3 budget levels were run.

## 8. Gate assessment (rules frozen in `phase2b_protocol.md` §5)

| Criterion | Result |
|---|---|
| Full-set procedure with paired power gain over exhaustive, CI excluding 0, in a hard-binding S6 cell | **met**: `fullset_adaptive`, S6_large_hard K18 b24 (+0.167 [0.072, 0.262]) and K48 b12 (+0.150 [0.012, 0.288]) |
| No N6 type-I flag for full-set procedures | **met**: 0/120 in every cell, both eps |
| SH advantage over uniform/random with CI excluding 0 | **not met** for claims; marginal discovery gain (+0.067) in one scenario only |
| Gains confined / explained by standard components? | **yes** — the gain needs b ≥ 12, vanishes for small hard effects at eps = 0.005, and reverses at b = 6. It is produced entirely by an inverse-normal adaptive combination test (Bauer & Köhne 1994; Lehmacher & Wassmer 1999) plus the classical minimax / optimal allocation for a minimum of means |

## 9. Decision: **CONDITIONAL GO — reframe; no algorithmic-novelty claim for the hardest-null search**

1. **Hardest-null search: NO-GO as a contribution.**
   * Successive halving gave no claim-rate advantage over uniform or random screening in any cell.
   * Its discovery advantage is marginal and confined to one scenario.
   * Selected-set screening is only valid for the selected nulls (Prop. 5). It was not shown to
     fail here, only because the binding family was easy to hit.
   * Drop "hardest-null search" from any novelty claim.
2. **Full-set adaptive certification: useful, but borrowed.**
   * `fullset_adaptive` is the only procedure that certifies over the *entire* admissible
     candidate set and beats exhaustive multi-null IUT at equal compute (+0.15 to +0.27 in power
     at b ≥ 12 for large effects; up to +0.30 at eps = 0) with zero observed type-I error.
   * It is a direct application of confirmatory adaptive-design methodology, not a new test or
     allocation theory.
   * It should be presented as the **recommended certification module** of the protocol, with
     correct attribution.
3. **Reframe RUSA** as an *audited evaluation protocol extending PCGA-L*. Its parts:
   * declared admissible null families with exact constraint audits;
   * explicit certificate scope (selected-set vs full-set);
   * a full-set adaptive two-stage certificate as the default;
   * empirical evidence that fixed menus (PCGA-L) certify spurious robust effects — 100% false
     claims in N6, and a θ overstatement of about 0.025 in S6.

   The defensible novelty is at the level of **protocol and empirical diagnosis for graph-null
   attribution**, not statistical methodology.
4. **Before real data (Phase 2C), if this reframing is accepted:**
   * (a) a negative control with a **single isolated binding null**, for example a triple-stratum
     or feature-quantile null with no near-equivalent arms, so that screening genuinely fails and
     the selected-set vs full-set gap becomes measurable;
   * (b) reduce `n_min`, or use a bounded-outcome or pooled-variance stage-2 test, so that full-set
     certification stays feasible at small budgets;
   * (c) one neural-model check of `fullset_adaptive` validity at the exact boundary (SAGE,
     A/A strat:w3).

   These are refinements; none is required to accept the reframing.

## 10. Risks and limitations

* One synthetic DGP family; SGC-ridge only in Phase 2B; t-based marginal tests (approximate).
* The binding *family* made discovery easy. The negative control therefore did not stress
  selected-set screens, and "hard" vs "easy" changed power less than intended.
* Monte Carlo precision is 60 experiments per S6 cell (SE ≈ 0.06 at 50% rates) and 120 per N6 cell.
* `fullset_*` are infeasible at b = 6 by construction (`n_min` floor); the reported power there is
  a design choice, not a property of adaptive designs in general.
* Selected-set and oracle claim rates in S6 are *not* comparable to full-set power: they certify a
  weaker statement.
