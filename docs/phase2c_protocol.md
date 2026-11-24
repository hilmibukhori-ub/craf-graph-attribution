# Phase 2C protocol — frozen before the confirmatory Phase 2C pools

Written 2026-11-24, before any instance with master seed 20261215 existed. The code, configs and
Hyperion batch files are hashed in `outputs/phase2c/FREEZE.json` (SGC-ridge) and
`outputs/phase2c_sage/FREEZE.json` (GraphSAGE), and every SLURM task verifies its hash.

Earlier artefacts are preserved:
* Phase 2A: `outputs/pilot*`, `archive/phase2a_code_2026-11-24.tar.gz`.
* Phase 2B: `outputs/phase2b*` and `archive/phase2b_code_2026-11-24.tar.gz`. The latter is a
  snapshot of the frozen Hyperion copy `/scratch/hilmibukhori/rusa_2b`, sha256 `79e64e7a…`.
* Phase 2C runs in a separate Hyperion directory, `/scratch/hilmibukhori/rusa_2c`.

Phase 2A and 2B instance generation is unchanged:
* `tests/test_phase2b.py::test_phase2a_instances_unchanged`;
* `tests/test_phase2c.py::test_phase2b_instances_unchanged`. Its hashes were computed with the
  archived 2B code and cover graph, labels, features, split and model features.

## 0. Scope accepted from Phase 2B

RUSA is reframed as an **audited relational attribution and evaluation protocol extending PCGA-L**.
* Successive halving (SH) is **not** part of the framework. In Phase 2C it is run only as a
  secondary comparator. It re-enters only if a paired CI excludes 0 in its favour on **both**
  discovery and claim rate in a hard cell; otherwise it stays out.
* The full-set procedure is `fullset_adaptive`. It is standard adaptive-design methodology
  (interim efficacy plus the inverse-normal combination test), attributed as such.
* No new methodology is introduced. The only Phase 2C changes to procedures are:
  * the stage-2 minimum `n_min` (5 → 3) in one variant;
  * an a-priori, data-free feasibility fallback to `exhaustive_iut`.

## 1. Development phase (disclosed; not results)

| Step | Seed | Use |
|---|---|---|
| DGP calibration, 40 instances per setting, K48, SGC-ridge | 999 | choose `gamma_e`. The first try (1.25/1.75) gave S8_small a binding margin of only 0.002 over eps, so gamma_e was raised to 1.75/2.25 |
| neural calibration, 30 instances, K18, GraphSAGE and GCN | 999 | GCN does **not** pick up the edge-specific term (S8_large binding Delta ≈ 0), so GraphSAGE is the neural replication |
| smoke pools: 240 instances per scenario (SGC), 120 (SAGE) | 616161 | pipeline check. It also showed power ≈ 1 for every full-set procedure at every budget with gamma_e = 2.25 (a ceiling, uninformative), so before freezing gamma_e was lowered to **small = 1.5, large = 1.75**. Expected binding Delta ≈ 0.011 / 0.014 (SGC). No other change |

Dev calibration (seed 999; mean test contrasts, 1 − Brier units):

| setting | Delta_binding (strat:w1+w2) | strongest decoy | Delta_empty |
|---|---|---|---|
| S7_hard, SGC, K48 | 0.0006 (exact 0 by A/A) | strat:w3+w5 0.0067 | 0.0166 |
| S7_easy, SGC, K48 | 0.0009 | empty 0.0111 | 0.0111 |
| S8_hard, SGC, gamma_e 1.25 (first try) | 0.0068 | strat:w3+w5 0.0100 | 0.0209 |
| S8_hard, SGC, gamma_e 1.75 (= final "large") | 0.0138 | strat:w3+w5 0.0178 | 0.0280 |
| S8_hard, SGC, gamma_e 2.25 (dropped after smoke) | 0.0238 | strat:w3+w5 0.0278 | 0.0336 |
| S7_hard, SAGE, K18 | 0.0005 | strat:w2+w3 0.0147 | 0.0318 |
| S8_hard, SAGE, K18, gamma_e 2.25 | 0.0172 | strat:w2+w3 0.0224 | 0.0362 |
| S8_hard, GCN, K18, gamma_e 2.25 | −0.0003 (no edge effect learned) | — | 0.0209 |

## 2. Scenarios (fixed)

* **World.** n = 300 nodes, 3 blocks and binary metadata w1..w8. There is also an observed node
  covariate `u = w1 XOR w2`. It is a model feature but **not** stratification metadata.
  * Decoys: `w3, w5 = u XOR Bernoulli(q)`, with hard q = 0.10 and easy q = 0.5.
  * The graph is a DC-SBM, assortative in block (×3) and in u (×4).
  * Labels: `eta = 0.8(x0 − x1) + 3 z(u-composition of neighbours) [+ gamma_e z(mean nbr x2)]`.
* **Isolated binding null.** Because u is marginally independent of w1 and of w2,
  `strat:w1+w2` is the **unique** candidate that reproduces the u-composition term exactly
  (`tests/test_phase2c.py::test_binding_null_is_isolated`). Decoy strata on w3/w5 preserve it
  only partially and crowd just above the binding null. Discovery difficulty is set by q.
* **S7_{hard,easy} (negative control).** gamma_e = 0, and G0 is an exact A/A draw of
  `strat:w1+w2` from the DC-SBM hub. So `Delta_{strat:w1+w2} = 0` exactly and
  `theta_full <= 0 <= eps`. The full-set robust-advantage claim is false.
* **S8_{small,large}_{hard,easy} (positive).** G0 is the DC-SBM graph, with gamma_e = 1.5
  (small) or 1.75 (large). Then `theta_full = Delta_{strat:w1+w2} > eps = 0.005`.
* **Pool sizes, SGC-ridge.** S7: 14,400 instances each; S8: 7,200 each. 57,600 instances in all,
  K = 48 candidates × 2 draws.
* **Pool sizes, GraphSAGE.** S7_hard, S8_small_hard and S8_large_hard, 7,200 each, K = 18 × 2 draws.
  Same master seed, so the instances and placebo graphs are identical to the SGC pool (paired
  across models).

## 3. Factors analysed (fixed)

| Factor | Levels |
|---|---|
| candidate set | K18 (strata over {block, w1..w4}: binding + w3-decoy family) and K48 (all; adds w5 decoys and strat:w3+w5) |
| budget b (B = b (2 + K) fits) | K18: 6, 9, 12, 24; K48: 6, 12, 24 |
| binding difficulty | hard (q = 0.10) / easy (q = 0.5) |
| effect | S7 null / S8 small / S8 large |
| eps | 0.005 (primary), 0 (secondary) |
| model | SGC-ridge (all) / GraphSAGE (S7_hard, S8_*_hard; K18) |

Each experiment is a disjoint block of 120 instances (20 dev + 100 confirmatory). That gives 120
experiments per S7 cell and 60 per S8 cell (SGC), and 60 per cell for SAGE.

## 4. Procedures (same budget B; scope reported)

| Procedure | Scope | Role |
|---|---|---|
| `pcga_l` | L3 | PCGA-L ladder. Its estimand is Delta_{strat:block}; it is judged **only** against that. Its full-set false-claim rate is shown for context, not as a validity failure |
| `exhaustive_iut` | full | baseline full-set certificate |
| `fullset_adaptive` | full | Phase 2B rule (n_min = 5; infeasible → no claim) |
| `fullset_adaptive_fb` | full | n_min = 5; if infeasible a priori → exactly `exhaustive_iut` |
| `fullset_adaptive_s` | full | n_min = 3; if infeasible a priori → exactly `exhaustive_iut` |
| `screen_uniform` | selected | the framework's selected-set screen (uniform within B/3, top-2, confirm) |
| `screen_random` | selected | comparator |
| `screen_sh` | selected | secondary only (see §0) |
| `oracle_select` | selected | {empty, true argmin}; upper bound, not usable |

Settings:
* alpha = 0.05, alpha1 = 0.01 (interim), alpha2 = 0.04;
* w1 = sqrt(1/3), fixed;
* top-m = 2, kappa = 1, d_floor = 0.003;
* discovery = `strat:w1+w2` is in the selected set (screens), the top-allocated arm (adaptive), or
  the argmin of the lower bound (exhaustive).

**Feasibility rule (a priori).** Let `R1 = max(2, min(20, round(B/3)//(2+K)))`. The adaptive
branch runs iff `R1 (2+K) + n_min (K+2) <= B`. The rule depends on (b, K, n_min) only, never on
data.

## 5. Outcomes and decision rules (fixed before results)

Primary eps = 0.005; SGC-ridge is primary, SAGE is the replication.

1. **Validity (full-set).** For every scope=full procedure, the S7 claim rate is reported with a
   Wilson CI. A **flag** is raised if the Wilson lower limit > 0.05 in any cell.
2. **Selected-set behaviour.** Report the S7 full-set false-claim rate of screens together with
   their miss rate. Prop. 5 predicts `false ≈ (1 − discovery) × P(confirm decoys)`. Validity is
   judged against the screens' **own** estimand (θ_sel); a flag is raised if the Wilson lower limit
   of `false_vs_target` > 0.05.
3. **Power.** S8 claim rates. Paired differences with 95% CIs:
   * `fullset_adaptive_s − exhaustive_iut`;
   * `fullset_adaptive_fb − exhaustive_iut`;
   * `fullset_adaptive − exhaustive_iut`;
   * `screen_sh − screen_uniform`, `screen_sh − screen_random` (claim, discovery).
4. **Small budgets.** Feasibility rates. Size of the marginal t-test on exact-null contrasts at
   n = 2..20 (disjoint groups). The S7 claim rate of `fullset_adaptive_s` at b = 6, 9.
5. **Combination audit (exact-null arm of S7).**
   * Stagewise t size.
   * Interim + combination type I under four stage-2 size rules (fixed 5, fixed 20, and two
     adversarial data-dependent rules), on disjoint blocks and on a centred bootstrap.
   * Flag if the total exceeds 0.05 + 2 MC-SE.
6. **Estimation and cost.** Bias and RMSE against each procedure's own estimand and against
   theta_full; coverage of the own estimand and of theta_full; mean fits and measured seconds.

Decision for the real-world phase:
* **GO** if all of the following hold:
  * no full-set validity flag (SGC and SAGE);
  * no combination-audit flag;
  * the framework's full-set procedure (`fullset_adaptive_s` if its small-budget audit passes,
    otherwise `fullset_adaptive_fb`) is never significantly worse than `exhaustive_iut`, and is
    better in at least one S8 hard cell for SGC;
  * the S8 effect is detectable with SAGE at some budget.
* **CONDITIONAL GO** if validity holds but power gains are absent or confined, or the neural
  replication is weak. Real-world use then proceeds with `exhaustive_iut` or `fullset_adaptive`
  as stated and with the documented limitations.
* **NO-GO** if any full-set validity or combination-audit flag is raised.

## 6. Execution

Hyperion, bcam-exclusive, working directory `/scratch/hilmibukhori/rusa_2c`:
* `scripts/hyperion/pool2c.sbatch` (array; SGC and SAGE configs);
* `scripts/hyperion/analyze2c.sbatch` (dependent).

numba 0.58.1 is loaded from `/scratch/hilmibukhori/pylib_numba`.
