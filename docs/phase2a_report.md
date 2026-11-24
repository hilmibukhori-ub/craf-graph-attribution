# RUSA Phase 2A — decision report

Date: 2026-11-24. Every number below comes from generated files:
* `outputs/pilot/report/REPORT.md` (+ CSVs in `outputs/pilot/analysis/`);
* `outputs/pilot_gnn/REPORT.md`;
* `outputs/pilot_conditional/*_summary.json`.

The pilot is a **synthetic pilot**, not a confirmatory study.

## 1. What was executed

| Item | Status |
|---|---|
| Code: generators, audit, search, models, inference, certificates, runner, reporting | done (`src/rusa`) |
| Tests | 51 tests: 51 pass locally (macOS, py3.12); 50 pass + 1 skipped (numba absent) on Hyperion (py3.10) |
| Pilot freeze | `outputs/pilot/FREEZE.json` (34 files hashed); verified by every SLURM task and again after the run |
| SGC-ridge pilot pool | 48,000 independent instances × (real + empty + 18 nulls × 2 draws) ≈ 1.82 M model fits; Hyperion jobs 8188012 (480 tasks, all COMPLETED) |
| Analysis | job 8188015: 12 scenarios × 2 eps × 7 procedures over 800 independent experiments (zcat check: 0 invalid placebo rows in the raw pool); calibration on 226 scenario × comparator cells × 5 methods × R ∈ {12, 40} |
| GCN/SAGE population pilot | 8 cells × 48 instances, 7 comparators (job 8188013) |
| Conditional demo | GCN, one fixed graph per scenario (S1_g150, S3), 30 seed bundles, Besag–Clifford swap nulls (job 8188014) |
| Raw pools | kept on Hyperion `/scratch/hilmibukhori/rusa/outputs/pilot/pool` (105 MB; sha256 in `outputs/pilot/POOL_SHA256SUMS.txt`); local copy holds per-chunk metadata only (laptop disk ≈ 1 GB free) |

**Not executed:**
* the confirmatory study (`configs/confirmatory.yaml` is a template);
* neural-model calibration (too expensive at the needed Monte Carlo scale; only estimates);
* real-graph experiments (out of Phase 2A scope);
* a systematic literature search.

## 2. Monte Carlo truths (design check)

The pilot pools confirm the intended scenario structure (1 − Brier units, MC SE ≤ 0.0005):

| scenario | Δ_empty | Δ_degree | Δ_strat:block | hardest admissible arm (Δ) | θ_menu | θ_full |
|---|---|---|---|---|---|---|
| S0 (null) | −0.0107 | 0.0007 | −0.0001 | perm:block (−0.0002) | −0.0107 | −0.0107 |
| S1, γ = 1.0 | +0.0086 | 0.0185 | 0.0182 | strat:block+w3 (0.0180) | 0.0086 | 0.0086 |
| S1, γ = 1.5 | +0.0247 | 0.0334 | 0.0330 | 0.0327 | 0.0247 | 0.0247 |
| S2 (degree) | +0.0638 | −0.0002 | −0.0000 | strat:w3 (−0.0005) | −0.0002 | −0.0005 |
| S3 (block composition) | +0.0210 | 0.0324 | 0.0002 | strat:block+w1 (0.0002) | 0.0002 | 0.0002 |
| S4 (block × w3) | +0.0136 | 0.0272 | 0.0103 | strat:block+w3 (0.0002) | **0.0103** | 0.0002 |
| S5 (hidden w3) | +0.0124 | 0.0243 | 0.0234 | strat:block+w3 (0.0002) | **0.0124** | 0.0002 |
| AA_degree / AA_block | — | 0 exactly / — | — / 0 exactly | — | ≈ 0 | ≈ 0 |

S2 empirically confirms "generic structure": degree-preserving nulls match the real graph while ER/perm
nulls do not. In S4/S5 the fixed PCGA-L menu misses the null that explains the signal
(θ_menu ≈ 0.010–0.012 > eps = 0.005 > θ_full ≈ 0). In all S1 settings the **binding comparator is the
empty graph**, not a placebo. This matters for interpreting the power results (§4).

The admissibility audit:
* every one of the ≈ 1.73 M placebo samples passed the hard constraints;
* swap completion was 1.00 throughout;
* mean edge overlap with G0 was 0.03–0.13, with no near-identical rejections;
* the joint strata (block × w) had move acceptance ≈ 3%, but 5 swaps/edge was always reached.

## 3. Gate B — statistical calibration

**Exact A/A boundary** (Δ = 0 by construction). One-sided rejection of a true null at nominal 0.05:

| family | R | t | bootstrap | sign-flip | emp. Bernstein | WSR betting |
|---|---|---|---|---|---|---|
| AA_degree | 12 (400 subsets) | 0.038 [0.023, 0.061] | 0.053 | 0.040 | 0.000 | 0.000 |
| AA_degree | 40 (120) | 0.050 [0.023, 0.105] | 0.050 | 0.042 | 0.000 | 0.000 |
| AA_block | 12 (400) | 0.048 [0.031, 0.073] | 0.070 [0.049, 0.099] | 0.045 | 0.000 | 0.000 |
| AA_block | 40 (120) | 0.067 [0.034, 0.126] | 0.067 | 0.067 | 0.000 | 0.000 |

**Global IUT at the boundary** (all 19 comparators, θ ≤ 0):
* AA_degree: 0.000 (R = 12) and 0.000 (R = 40);
* AA_block: 0.0025 and 0.0083.

That is ≤ alpha, and strongly conservative because the other comparators sit far above zero.

**Marginal coverage across all scenarios × comparators** (226 cells per R; cross-fitted MC truth):

| method | R = 12 mean / max miscoverage | cells with Wilson lower limit > 0.05 | R = 40 mean / max | cells > 0.05 |
|---|---|---|---|---|
| t (primary) | 0.048 / 0.075 | 2 | 0.053 / 0.150 | 8 |
| sign-flip | 0.049 / 0.078 | 1 | 0.053 / 0.133 | 9 |
| bootstrap | 0.073 / 0.100 | **100** | 0.060 / 0.150 | 17 |
| empirical Bernstein | 0.000 | 0 | 0.000 | 0 |
| WSR betting | 0.000 | 0 | 0.000 | 0 |

How to read this:
* **The t-procedure is calibrated on average.** At R = 40, 8 cells are flagged, all in
  S1_hetero (3), S0 (2) and S4 (3). With 226 correlated cells and one-sided 97.5% Wilson limits, about 6
  spurious flags are expected. Cross-fitted truths also carry error of about 0.1–0.15 SE at
  R = 40, which inflates measured miscoverage. The flagged cells are not proof of miscalibration,
  but the worst cell (S1_hetero/strat:w2, 0.15 [0.08, 0.26], 60 subsets) should be re-examined
  in the confirmatory study.
* **The percentile bootstrap undercovers at R = 12** (100/226 cells flagged), as known for small n.
  It must not be used as the primary method.
* **The bounded finite-sample methods are valid but useless here.** Mean bound widths are 1.58
  (EB) and 0.76 (WSR) at R = 12, and 0.45 / 0.21 at R = 40, against effects of about 0.01–0.03.
  This is because the a priori range of a Brier difference is [−1, 1]. A useful bounded
  certificate would need a much tighter, justified range or far more replicates.
* Own-target coverage of the robust lower bound per procedure (80 or 40 experiments per cell)
  ranges from 0.90 to 1.00. The lowest cells are S1_g100 menu_iut/RUSA at 0.90 [0.81, 0.95] and
  S1_g200 at 0.90 [0.77, 0.96]. They are consistent with nominal 0.95 at this MC precision but
  should be monitored.

**Gate B: PASS (pilot level),** with the caveats above: t only; bootstrap excluded; the Monte
Carlo precision is pilot-grade.

## 4. Gate C — methodological value at equal compute

Budget: 240 fits per experiment for every IUT/RUSA procedure. Claim rates at the primary eps = 0.005,
with 80 independent experiments (40 for the 2400-instance scenarios):

| scenario (truth) | PCGA | PCGA-L | single degree | menu IUT (RUSA w/o search) | **IUT over all 18** | RUSA uniform | RUSA SH |
|---|---|---|---|---|---|---|---|
| S1 γ = 0.5 (θ_full < 0) | 0.375 | 0.475 | 0.125 | 0.000 | 0.000 | 0.000 | 0.000 |
| S1 γ = 1.0 (θ_full = 0.009 > eps) | 1.000 | 1.000 | 1.000 | 0.338 | **0.175** | 0.338 | 0.338 |
| S1 γ = 1.5 | 1.000 | 1.000 | 1.000 | 1.000 | 0.925 | 1.000 | 1.000 |
| S1 hetero | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 |
| S2 (generic degree) | 1.000 | 0.013 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S3 (block composition) | 1.000 | 0.025 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| **S4** (hidden joint null) | 1.000 | 0.963 | 1.000 | **0.650** | 0.000 | 0.025 | 0.013 |
| **S5** (hidden w3 null) | 1.000 | 1.000 | 1.000 | **0.950** | 0.000 | 0.000 | 0.000 |
| AA_degree / AA_block | 1.000 / 1.000 | 0 / 0 | 0 / 1.000 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

In S2–S5 and the A/A scenarios θ_full ≤ eps, so every claim there is false with respect to the
full admissible candidate set. PCGA and single-null claims are, however, correct for *their own*
narrower nulls: PCGA's perm placebo really is beaten. That is exactly the point. A single or
small fixed null answers a weaker question than "beyond all declared generic structure".

Paired experiment-level differences (95% CI), eps = 0.005:
* **RUSA (SH or uniform) − IUT-all, power:**
  * S1 γ = 1.0: +0.163 [+0.055, +0.270];
  * S1 hetero: +0.100 [+0.006, +0.194];
  * S1 γ = 1.5: +0.075 [−0.008, +0.158].
  At eps = 0, S1 γ = 1.0 gives +0.425 [+0.316, +0.534].
* **RUSA − IUT-all, false claims (θ_full ≤ eps):**
  * S4: +0.013 [−0.012, +0.037] (SH) and +0.025 [−0.009, +0.059] (uniform);
  * 0 elsewhere.
* **RUSA SH − menu IUT, false claims:** S4 −0.637 [−0.744, −0.531]; S5 −0.950 [−0.998, −0.902].
  Power in S1 is identical (difference 0).
* **SH − uniform:**
  * claim rates: no difference in any scenario (all CIs include 0);
  * near-tie hit rate (selected set within 0.002 of the hardest arm): ≥ 0.91 for both everywhere;
    S4 SH 0.963 vs uniform 0.925, difference +0.037 [−0.027, +0.102];
  * exact-argmin hit rate: mixed (SH better in S1_hetero +0.15, worse in S3 −0.14).

Search diagnostics: development contrasts of the selected null are biased downwards (winner's
curse). In S5 the mean dev estimate is −0.0026 (SH) / −0.0050 (uniform) against a truth of
+0.0002. This is why the confirmatory stage must use fresh instances.

**Interpretation, honestly attributed:**
1. *Where the gain comes from.* The two-stage RUSA design is "screen candidates on development
   data, confirm {empty} + top-2 on fresh data". At equal fit budget it **dominates both critical
   baselines** in this pilot:
   * it keeps IUT-all's protection against hidden nulls (S4/S5: ≤ 0.025 vs menu IUT 0.65–0.95);
   * it matches the power of the cheaper fixed menu (S1: 0.338 vs IUT-all 0.175 at γ = 1).
2. *Where it does not come from.*
   * **The power gain is not produced by the search.** In every S1 setting the binding comparator
     is the empty graph. RUSA wins because it confirms 3 comparators on 40 instances, whereas
     IUT-all must spread the same budget over 19 comparators on 12 instances. A uniform screen
     does exactly as well as successive halving.
   * **The search's only demonstrated role is safety:** finding the hidden null in S4/S5 at
     92–100% near-tie hit rates.
   * The pilot has **no scenario in which a hidden placebo is the binding comparator and
     θ_full > eps.** That is the one case where search quality would drive power, so the
     efficiency claim for the search itself is untested.
3. *Novelty.* "Screen on a split, confirm on the rest" is classical data splitting (Cox 1975).
   Successive halving adds nothing measurable over uniform screening here. Together with the
   novelty audit, the defensible contribution is a **design/protocol**:
   * an audited, declared null family;
   * dev-only screening with a freeze;
   * a confirmatory IUT with explicit certificate scope;
   * empirical evidence that fixed PCGA/PCGA-L menus mis-attribute under plausible hidden
     structure.
   It is not a new search algorithm or a new statistical test.

**Gate C: PARTIAL PASS.** There is measurable value over PCGA-L and over fixed multi-null IUT at
equal compute (power and protection). It comes from the two-stage screen-and-confirm design
(standard) and from the admissible family; it does not come from the adaptive search algorithm.

## 5. Neural-model and conditional pilots (estimates only)

* **GCN/SAGE, 48 instances per cell** (`outputs/pilot_gnn/REPORT.md`):
  * The menu IUT certifies in S4 and S5 for both GCN and SAGE (L_robust 0.010–0.024). Extending
    the menu with strat:w3 and strat:block+w3 removes every one of these certificates (Δ ≈ −0.002
    to +0.001). This qualitatively reproduces the SGC finding with neural models.
  * In S3 the block-stratified null removes the apparent relation effect for both architectures.
  * SAGE certifies S1 γ = 1.5 (L = 0.024).
  * **Plain GCN in S1 is worse than its matched empty graph** (Δ_empty = −0.011). Self-loop
    normalisation without a separate self-weight dilutes the own-feature signal. This is a model
    artefact that RUSA correctly reports as "no certified relational value". It is not a
    statement about the DGP.
* **Conditional demo (one fixed graph, GCN, 30 seed bundles):**
  * In S3 the PCGA rank test rejects for the degree and perm placebos (rank 1/30, p = 0.033).
    Against the Besag–Clifford block-stratified null the real graph is not better (rank 17/30,
    p = 0.57; Δ = −0.0055). A PCGA-style single-placebo analysis would claim relation specificity
    on this graph; RUSA abstains.
  * In S1_g150 this particular graph/split is worse than empty under GCN. That is conditional on
    one instance and consistent with the GCN artefact above.

## 6. Acceptance gates

| Gate | Verdict | Basis |
|---|---|---|
| A — correctness | **PASS** | 51/51 tests local, 50 + 1 skipped on Hyperion; exact hard-constraint checks on ≈ 1.73 M placebos with no violation; no-leakage tests; freeze verified |
| B — calibration | **PASS (pilot)** | t-procedure A/A and cross-fitted coverage consistent with 0.05; global IUT ≤ alpha; bootstrap excluded; bounded methods valid but powerless |
| C — methodological value | **PARTIAL** | equal-compute dominance over menu IUT and IUT-all, attributable to two-stage design + admissible family; the adaptive search adds nothing over uniform screening |
| D — honest novelty | **PASS only for a narrow design claim** | no statistical component is new; see `novelty_audit.md`; adjacent GNN-control preprints must still be read |

## 7. Decision: **CONDITIONAL GO**, with reframing

Option (c) from the brief: reframe as a benchmark / PCGA extension, combined with a narrowly
scoped (b).
* Do **not** present RUSA as a new hardest-null search algorithm or new inference method.
  Present it as an *admissibility-audited, screen-then-confirm robust attribution protocol* that
  extends PCGA-L. Its empirical message: fixed null menus (PCGA, PCGA-L, single nulls)
  systematically over-attribute when label-relevant generic structure lies outside the menu, and
  an audited screen-and-confirm IUT fixes this at no power cost in the tested settings.
* Before any Phase 2B real-data work, run the targeted confirmatory study (§8). Proceed only if:
  * it reproduces Gate B at confirmatory precision (MC SE ≤ 0.005); and
  * it tests the missing case (hidden binding null with θ_full > eps).
  If SH still shows no advantage there, drop SH and keep a uniform screen.

## 8. Recommended next runs (not executed)

1. **Add S6, "hidden binding null with positive effect".** Exact-edge signal plus w3-composition
   signal, so the w3-aware null binds with θ_full ≈ 0.01 > eps. This is the only setting where
   search quality affects power; compare uniform vs SH vs IUT-all.
2. **Larger candidate sets** (K ≈ 50–100, e.g. triple strata, feature-quantile strata), where a
   uniform screen becomes thin and SH could plausibly matter.
3. **Confirmatory calibration** with `configs/confirmatory.yaml` (fresh seed 20270101, about 2000
   experiments per scenario), including the flagged S1_hetero cells.
4. **Neural calibration at reduced scale** (SAGE, e.g. 400 subsets of R = 12 for A/A) to check that
   seed variance does not break the t-procedure.
5. Read the adjacent GNN-control preprints in full and run a systematic search on "adversarial /
   hardest null models" before writing any novelty sentence.

Commands (after adding S6 to `SCENARIOS` and `configs/confirmatory.yaml`, then a new freeze):
```bash
python scripts/freeze_plan.py --config configs/confirmatory.yaml
rsync -az --exclude __pycache__ --exclude outputs ./ hyperion:/scratch/hilmibukhori/rusa/
# on hyperion (clean shell):
N=$(python3 -c "import yaml;c=yaml.safe_load(open('configs/confirmatory.yaml'));print(sum(-(-v//c['chunk']) for v in c['scenarios'].values())-1)")
sbatch --array=0-$N%400 scripts/hyperion/pool.sbatch configs/confirmatory.yaml sgc
sbatch --dependency=afterok:<jobid> scripts/hyperion/analyze.sbatch configs/confirmatory.yaml
```

## 9. Risks and limitations

* One synthetic DGP family; SGC-ridge carries the calibration study; n = 300 graphs.
* Monte Carlo precision is pilot-grade: 40–80 experiments per scenario for procedure comparisons.
* Truths are Monte Carlo estimates. Only the A/A families have an exact zero.
* PCGA and single-null procedures used fewer fits than the budget (capped at 50 instances); this
  only favours them.
* Admissibility is a declared assumption. A null preserving neighbour *feature* composition would
  also absorb S1's signal; whether such a null is admissible is a scientific choice.
* No result here licenses causal or semantic interpretation of edges. Non-certification is not
  evidence of no relational value.
