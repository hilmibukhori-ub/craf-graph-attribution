# RUSA Phase 3A — Certified Relational Attribution Frontier (CRAF): development and proof of concept

Date: 2026-11-24. Status: **complete.** No real-world experiment had been started at this stage.

**Recommendation: CONDITIONAL GO.** The pre-specified protocol rule gives GO, because all three
criteria are met. We recommend CONDITIONAL GO because the novelty audit (§2) shows the inferential
construction is a standard simultaneous-inference / set-identification construction. The
defensible contribution is the **estimand and its certified, monotonicity-free frontier
statement for graph-property attribution**, not a new statistical method. See §8.

Documents:
* formulation, guarantees and pseudocode: `docs/craf_math.md`;
* protocol (frozen before execution): `docs/phase3a_protocol.md`;
* code: `src/rusa/craf/`; tests: `tests/test_craf.py` (12 tests; **105/105 pass on Hyperion**);
* results: `outputs/phase3a/report/` (REPORT.md, summary.csv, paired_differences.csv,
  truth_frontiers.csv, and three figures).

## 1. What was done

| Task | Done |
|---|---|
| 1 Novelty audit | §2, and `docs/novelty_audit.md` §F (references verified by search) |
| 2 Property-subset lattice, no monotonicity assumed | `craf_math.md` §1; `Lattice`; minimality is always checked against **all** proper subsets |
| 3 Estimands | `Delta_S`; advantage `Delta_S > delta`; sufficiency `Delta_S < delta`; frontier `F = min_⊆ Suff`; relational specificity `Suff = ∅` |
| 4 Simultaneous three-way certification | Holm over 2|L| one-sided hypotheses → certified advantage / certified sufficiency / inconclusive; FWER ≤ alpha (Prop. C1) |
| 5 Frontier: certified minimal vs minimal among certified; uncertainty | `cert_min ⊆ F ⊆ possible_min` with probability ≥ 1 − alpha (Prop. C2); gap sets; Prop. C3 shows why "minimal among certified" and "children-only" minimality are not guarantees |
| 6 Adaptive allocation | two-stage minimax-power allocation + relevance screening + inverse-normal combination, with the `fullset_adaptive_fb` defaults (`n_min = 5`, a-priori fallback); valid by Prop. C5 |
| 7 Comparators | PCGA-L, exhaustive factorial (unadjusted), naive point-estimate frontier, standard Holm non-inferiority (`ni_holm`), plus a monotonicity-assuming ablation (`craf_children`) |
| 8 Pool reuse and targeted PoCs | 5 reused pools (2B N6_hard; 2C S7_hard, S7_easy, S8_small_hard; 2C SAGE S7_hard); 1 new pool (P3_multi, 7,200 instances); 4 semi-synthetic Delta tables for non-monotonicity and worst-case error |

**Execution and disclosures.**

| Item | Detail |
|---|---|
| Hyperion working directory | `/scratch/hilmibukhori/rusa_3a`. Reused pools were read-only from `rusa_2b`/`rusa_2c`; Phase 2A–2C artefacts are unchanged |
| Jobs | tests 8195917 (1 failure: a wrong test assumption, see protocol §0) and 8195932 (105 pass); pool 8195958 (60 tasks); analysis 8195959 |
| Change after freeze | only `scripts/make_report_3a.py`, which pivoted a text column that newer pandas rejects. The analysis outputs were produced by the frozen code |
| fullset_adaptive_fb | adopted as the RUSA default, documented as selected *after* Phase 2C results (`rusa_framework.md`, protocol header) |

## 2. Novelty audit (summary; detail in `novelty_audit.md` §F)

| Closest work | What it does | Difference from CRAF | Consequence for novelty |
|---|---|---|---|
| PCGA-L (own prior work) | one ordered ladder empty→ER→degree→block→real; step attributions | a chain, so attribution depends on order; it cannot express joint combinations ({w1,w2}) or alternative routes ({w3} vs {w1,w2}); no sufficiency claims | CRAF generalises the ladder to a lattice. That is a formulation contribution |
| dk-series / null-model hierarchies (Orsini et al. 2015; Mahadevan et al. 2006) | nested hierarchy of constraints (d = 0, 1, 2, 2.5, 3); find the d at which dk-random graphs reproduce *network properties* | a chain, not a lattice; the target is reproduction of structural statistics, not predictive performance; no simultaneous certification | closest conceptual precedent for "minimal sufficient constraints". CRAF's novelty is restricted to the lattice + performance estimand + certificate |
| Factorial ablation / GraphWorld (Palowitch et al. 2022) | vary generator parameters; study property–performance relations | descriptive, with no inferential certificate of sufficiency or minimality | none from factorial designs themselves |
| Minimal sufficient explanations (prime implicants: Shih, Choi & Darwiche 2018; sufficient input subsets: Carter et al. 2019) | minimal feature subsets sufficient for a model's *decision*, instance-wise, deterministic | CRAF's units are graph-null constraints, the target is population/conditional *performance*, and sufficiency is statistical with a margin | the concept of minimal sufficient subsets is not new. Its certified statistical version for graph constraints appears not to be in the literature reviewed |
| Non-inferiority / equivalence with multiplicity (Holm 1979; closed testing; Logan & Tamhane 2008) | Holm-adjusted non-inferiority over many hypotheses | gives certified-sufficient sets; no insufficiency certificates, so no minimality guarantee (Prop. C3a, and the 0.19–0.38 false-member rates below) | standard; CRAF uses it as one half |
| Partitioning principle / directional decisions (Finner & Strassburger 2002); MCB (Hsu 1996); inference for ranks (Mogstad et al. 2024) | simultaneous confidence statements about set-valued or ordinal functions of parameters | CRAF's frontier sandwich is an instance of the same logic: simultaneous sign identification of `Delta_S − delta`, then a deterministic set function | **the inferential construction is standard.** No novelty claim for it |

**Verdict.** No novelty is claimed for the tests, Holm, combination tests, the lattice, or the
sandwich logic. A contribution can be claimed for:
1. defining relational attribution as a *frontier of minimal δ-sufficient graph-constraint
   combinations* over a declared lattice, which is order-independent and needs no monotonicity;
2. showing, on graph pipelines, that the standard reporting practices (non-inferiority +
   "minimal among certified", children-only minimality, point estimates, single ladders) give
   wrong frontier members at substantial rates, while the certified sandwich does not.

This is a modest, formulation-level contribution.

## 3. Proof-of-concept worlds (Monte Carlo truths; delta = 0.005; |L| = 16 for pools, 7 for semi-synthetic)

| Pool / table | True frontier F | # sufficient | Property demonstrated |
|---|---|---|---|
| S7_hard (SGC; SAGE) | {w1+w2} | 1 | **interaction**: neither w1 nor w2 alone suffices (Delta ≥ 0.026); decoys at 0.011 |
| S7_easy (SGC) | {w1+w2} | 1 | interaction, easy |
| N6_hard (SGC, 2B pool) | {w3} | 5 | many sufficient combinations ({w3} and every pair containing it), one minimal |
| **P3_multi (SGC, new)** | **{w3}, {w1+w2}** | 6 | **two distinct minimal combinations** of different size |
| S8_small_hard (SGC) | ∅ (min Delta 0.0106) | 0 | no combination suffices → relational specificity |
| SS_nonmono_A | {degree} | 2 | **non-monotone**: {} sufficient, {a} insufficient, {a,b} sufficient again (5 non-monotone pairs) |
| SS_nonmono_B | {a}, {b+c} | 3 | **non-monotone**: {a} sufficient, {a,b} insufficient |
| SS_near | {c}, {a+b} | 4 | near-margin elements (0.002, 0.008) |
| SS_boundary | ∅ (all Delta = delta) | 0 | worst case for the FWER: every certification is false |

**Scope.** Non-monotonicity was **not** found in any existing Phase 2A–2C pool truth (protocol
§0), so it is validated only on semi-synthetic Delta tables. Their noise is t5 with sd 0.012,
matched to pool contrasts. This is a limitation, and a natural graph-pipeline instance remains
open.

## 4. Validity

| Metric | CRAF (uniform) | CRAF (adaptive) | Requirement |
|---|---|---|---|
| FWER of certifications, worst case (SS_boundary; 2000 experiments) | 0.040 / 0.046 / 0.051 (b = 20/40/80); Wilson lower limit ≤ 0.042 | 0.040 / 0.043 / 0.048 | ≤ 0.05, no flag ✔ |
| FWER of certifications, all other settings | 0.000 | 0.000 | ✔ |
| False frontier member (some reported element is not truly minimal sufficient) | ≤ 0.004 everywhere | ≤ 0.004 | ✔ |
| Coverage `F ⊆ possible_min` | 1.000 in every cell | 1.000 | ≥ 0.95 ✔ |

**Comparators: false frontier members.** These are wrong claims of the form "S is a minimal
sufficient combination".

| Setting | ni_holm (standard NI + minimal among certified) | craf_children (assumes monotonicity) | naive_point | factorial_unadj | CRAF |
|---|---|---|---|---|---|
| N6_hard b20/40/80 | **0.31 / 0.38 / 0.19** | 0 | 0.09 / 0.03 / 0 | 0 | 0 |
| P3_multi b20/40/80 | **0.26 / 0.33 / 0.06** | 0 | 0.04 / 0 / 0 | 0 | 0 |
| SS_near b20/40/80 | **0.15 / 0.28 / 0.37** | 0 | 0.24 / 0.10 / 0.02 | 0.00 | 0 |
| SS_nonmono_A b20/40/80 | 0.21 / 0.24 / 0.09 | **0.25 / 0.54 / 0.88** | 0.02 / 0.01 / 0 | 0 | 0 |
| SS_nonmono_B b20/40/80 | 0.20 / 0.23 / 0.08 | 0 | 0.03 / 0 / 0 | 0 | 0 |
| SS_boundary | 0.04–0.05 | 0.00 | **0.99** | 0.06 | ≤ 0.004 |
| S7 / S8 pools | 0 | 0 | ≤ 0.10 | 0 | 0 |

The unadjusted factorial's certification FWER is **0.52–0.54** at the boundary.

* **`ni_holm`.** It reports a sufficient superset as "minimal" whenever the true minimal subset
  is not yet certified. This is Prop. C3a in action. Note that its false-member rate **rises**
  with budget in SS_near: more sufficient supersets get certified while the near-margin minimal
  element stays inconclusive.
* **`craf_children`.** It fails exactly where monotonicity fails, with up to 88% wrong claims in
  SS_nonmono_A.
* **PCGA-L.** Its modal report is "edge step supported; no ladder level sufficient" in every
  pool. That is correct within its scope: degree and block are truly insufficient in S7, N6 and
  P3_multi, and nothing is sufficient in S8. It has 0 false members. But it **cannot** recover
  {w1+w2} or {w3}, so its exact recovery is 0 except in S8, where the truth is "none". This is
  a scope limitation, not invalidity.

## 5. Exact frontier recovery (reported frontier == F)

| Setting | b | CRAF | CRAF-adaptive | ni_holm | naive_point | factorial_unadj |
|---|---|---|---|---|---|---|
| S7_hard SGC | 20 / 40 / 80 | 0.10 / 0.38 / 0.79 | 0.17 / **0.66** / **0.92** | 0.13 / 0.41 / 0.79 | 0.86 / 0.99 / 1.00 | 0.54 / 0.81 / 0.99 |
| S7_hard SAGE | 20 / 40 / 80 | 0.25 / 0.61 / 0.81 | 0.46 / **0.86** / **0.96** | 0.29 / 0.63 / 0.81 | 0.96 / 1 / 1 | 0.61 / 0.85 / 0.99 |
| N6_hard | 20 / 40 / 80 | 0.12 / 0.39 / 0.74 | 0.17 / 0.54 / 0.90 | 0.17 / 0.41 / 0.81 | 0.91 / 0.97 / 1 | 0.61 / 0.79 / 0.98 |
| P3_multi | 20 / 40 / 80 | 0.13 / 0.29 / 0.88 | 0.11 / **0.78** / 0.94 | 0.17 / 0.42 / 0.90 | 0.94 / 1 / 1 | 0.56 / 0.78 / 1 |
| S8_small_hard | all | 1.00 | 1.00 | 1.00 | 0.96–1 | 1.00 |
| SS_nonmono_A | 20 / 40 / 80 | 0.23 / 0.53 / 0.88 | 0.40 / 0.83 / 0.94 | 0.27 / 0.57 / 0.90 | 0.98 / 0.99 / 1 | 0.58 / 0.84 / 0.98 |
| SS_near | 20 / 40 / 80 | 0.00 / 0.01 / 0.13 | 0.00 / 0.03 / 0.20 | 0.03 / 0.12 / 0.41 | 0.73 / 0.90 / 0.98 | 0.05 / 0.20 / 0.50 |

Read this table honestly:
* When the sufficient and insufficient elements are well separated, which is the case in every
  pipeline PoC, the **point estimate recovers the frontier most often**. It has no guarantee: at
  the boundary it is wrong 99% of the time, and in SS_near up to 24%.
* CRAF trades exact recovery for certified correctness of every claim it makes. Exact recovery
  needs every subset of a frontier element certified insufficient and the element certified
  sufficient at Holm-adjusted levels, which costs budget.
* With near-margin elements (SS_near), certified exact recovery stays low even at b = 80.
  CRAF's honest output there is the uncertainty set: 2.7–4.8 possibly-minimal elements, always
  covering F.

**Certified relational specificity (S8, nothing sufficient).** CRAF certifies it in 0.07 / 0.33 /
0.69 of experiments at b = 20 / 40 / 80. CRAF-adaptive does so in 0.26 / 0.83 / 0.88.

## 6. Adaptive allocation (task 6)

Paired CRAF-adaptive − CRAF, exact recovery, 95% CI:
* **S7_hard SGC**: +0.069 [0.013, 0.126], **+0.285 [0.191, 0.379]**, +0.132 [0.067, 0.197].
* **S7_easy**: +0.13, **+0.40 [0.31, 0.48]**, +0.15.
* **S7_hard SAGE**: +0.21 [0.08, 0.34], +0.25 [0.13, 0.37], +0.15 [0.07, 0.24].
* **N6_hard**: +0.05 (n.s.), +0.15 [0.07, 0.22], +0.16 [0.10, 0.22].
* **P3_multi**: −0.01 (n.s.), **+0.49 [0.37, 0.60]**, +0.07 (n.s.).
* **SS_nonmono_A/B**: +0.04 to +0.30, all significant. **SS_near**: 0 to +0.07.
* **Never significantly negative.** Validity is unchanged (§4). Fits used are ≤ B.

The number of inconclusive elements is not uniformly lower. Relevance screening deliberately
leaves dominated supersets at `n_min`, where they often stay inconclusive, but that cannot change
the frontier. So adaptive allocation **helps frontier recovery at matched budget while preserving
validity**. The gain comes from standard adaptive-design machinery plus a frontier-relevance
heuristic, which is the only CRAF-specific design element, and it is a heuristic.

## 7. Cost

* Each replicate costs `1 + |L|` fits; |L| = 16 here (5 attributes, order ≤ 2).
* At b = 80 that is 1,360 SGC fits per experiment (≈ 6 s on Hyperion). For SAGE it is about 10×.
* |L| grows combinatorially, so CRAF is meant for small declared attribute sets (≤ 6–8, order
  ≤ 2–3).
* For conditional single-graph use, b = 40–80 seed bundles × 17 fits is feasible for SGC and
  SAGE on graphs of moderate size.

## 8. Decision

| Pre-specified criterion | Result |
|---|---|
| no validity flag | ✔ (worst-case FWER ≤ 0.051, Wilson lower limit 0.042; coverage 1.0) |
| CRAF differs materially from the standard approach | ✔ (`ni_holm` false members 0.19–0.38 in N6, P3_multi and SS_near; CRAF 0. CRAF also gives certified minimality, which `ni_holm` cannot) |
| exact recovery ≥ 0.5 at the largest budget, pipeline PoCs | ✔ (CRAF 0.74–0.88; adaptive 0.90–0.96) |

**Protocol rule → GO.** **Recommendation → CONDITIONAL GO**, because:
1. **Novelty is formulation-level.** The certification is Holm over directional hypotheses, and
   the frontier sandwich is standard set-identification logic (§2). CRAF should be presented as
   a certified *estimand and reporting framework* for graph-property attribution, with all
   inferential components attributed.
2. **Non-monotonicity has only been validated semi-synthetically.** The graph pipelines studied
   are empirically monotone. Before claiming practical relevance of the monotonicity-free design,
   a real-data or realistic-generator instance of non-monotonicity should be sought. If real
   graphs turn out to be monotone, CRAF still adds the multiplicity-correct frontier, and its
   advantage over `craf_children` disappears.
3. **Certified exact recovery needs b ≈ 40–80 replicates per element**, and fails gracefully
   (large uncertainty sets) near the margin. Real-world use must report `possible_min` and the
   gap sets, not only `cert_min`.
4. **Lattice size.** The number of lattice elements grows combinatorially; the declared attribute
   set must be small, and the lattice frozen before data.

Conditions for the real-world phase:
* use CRAF-adaptive with the `fullset_adaptive_fb` defaults;
* in conditional mode, use fresh seed bundles with fresh placebo draws per stage;
* run an A/A calibration of the t-test on the real graph's own lattice nulls;
* report every scope: certified advantage, certified sufficiency, inconclusive, `cert_min`,
  `possible_min` and gap sets;
* keep the PCGA-L ladder alongside as the descriptive attribution.

**Do not start large-scale real-world experiments until this methodological contribution has
been reviewed.**

## 9. Limitations

* Semi-synthetic non-monotonicity only (see above).
* delta = eps = 0.005 was inherited from Phases 2B/2C, not re-derived.
* The truths of near-margin elements (|Delta − delta| < 0.002) are Monte Carlo estimates
  (MC-SE ≤ 0.0002). No pipeline PoC element lies that close, but SS_near does by design.
* Holm ignores the logical structure that `H^adv_S` and `H^suf_S` cannot both be true unless
  `Delta_S = delta`. A partitioning-principle refinement could be more powerful. Not pursued,
  and it would carry no novelty.
* Only SGC-ridge and GraphSAGE were used; one metric (1 − Brier); n = 300 nodes.
