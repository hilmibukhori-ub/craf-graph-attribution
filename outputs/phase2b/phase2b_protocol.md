# Phase 2B protocol — frozen before the confirmatory Phase 2B pool

Written 2026-11-24, before any instance with master seed 20261201 existed. The code, configs and
Hyperion batch files are hashed in `outputs/phase2b/FREEZE.json`, and every SLURM task verifies
that hash. Phase 2A outputs (`outputs/pilot*`) are untouched:
* the Phase 2A code is archived in `archive/phase2a_code_2026-11-24.tar.gz` (sha256 in `.sha256`);
* on Hyperion it is snapshotted as `/scratch/hilmibukhori/rusa_phase2a_code_snapshot.tar.gz`;
* Phase 2B runs from a separate copy, `/scratch/hilmibukhori/rusa_2b`.

Phase 2A instance generation is unchanged. Regression hashes are enforced by
`tests/test_phase2b.py::test_phase2a_instances_unchanged`.

## 1. Development phase (disclosed; not results)

| Step | Seed | Use |
|---|---|---|
| DGP calibration, 40–60 instances per setting, 12 nulls | 999 | choose `gamma_e`, `q` (`dev2b.py` output below) |
| smoke pool, 240 instances per scenario | 515151 | pipeline check; revealed that full-set allocation with `n_min = 3` and discarded stage-1 data is almost powerless. This led to the minimax-power rule (`n_min = 5`) and the `fullset_adaptive` procedure, before any frozen-seed data |

Dev calibration (seed 999; mean test contrasts):

| setting | Δ_empty | Δ_strat:w3 (binding) | Δ_strat:w4+w5 (near decoy) | Δ_strat:w4 |
|---|---|---|---|---|
| S6, q = 0.10, gamma_e = 1.25 | 0.020 | 0.008 | 0.010 | 0.020 |
| S6, q = 0.10, gamma_e = 1.75 | 0.027 | 0.015 | 0.019 | 0.027 |
| S6, q = 0.5, gamma_e = 1.25 | 0.020 | 0.011 | 0.036 | 0.034 |
| N6, q = 0.10 | 0.013 | ≈ 0 (exact 0 by A/A) | 0.007 | 0.013 |

## 2. Scenarios (fixed)

* **World.** n = 300, 3 blocks, metadata w1..w8, with decoys `w4, w5 = w3 XOR Bernoulli(q)`.
  The graph is a DC-SBM assortative in block (×3) and w3 (×4).
* **S6_{small,large}_{hard,easy}.** `eta = 0.8(x0 - x1) + gamma_e z(mean nbr x2) + 3 z(w3 comp)`.
  * gamma_e: small = 1.25, large = 1.75.
  * q: hard = 0.10, easy = 0.5.
  * Truth: `theta_full > eps = 0.005`, attained by a w3-preserving placebo (a hidden binding null).
* **N6_{hard,easy}.** gamma_e = 0, and G0 is an exact A/A draw of `strat:w3` from the DC-SBM hub,
  so Δ_strat:w3 = 0 exactly and `theta_full <= 0`. Nulls that miss w3 composition are beaten
  (Δ ≈ 0.01–0.03).
* **Pool sizes.** 7,200 instances per S6 scenario; 14,400 per N6 scenario.
* **Pool contents.** Each instance fits the real graph, the empty graph and 48 candidates × 2 draws
  with SGC-ridge: K = 48 = er, degree, perm:block, and strat over all 1- and 2-subsets of
  {block, w1..w8}.

## 3. Factors analysed (fixed)

| Factor | Levels |
|---|---|
| candidate set | K18 (strata over {block, w1..w4}; includes w3 and decoy w4) and K48 (all) |
| budget b (B = b (2 + K) fits per experiment) | K18: 6, 12, 24; K48: 6, 12 |
| binding difficulty | hard (q = 0.10) / easy (q = 0.5) |
| effect size | small / large (S6); null (N6) |
| eps | 0.005 (primary), 0 (secondary) |

Each experiment is a disjoint block of 120 instances: 20 development + 100 confirmatory. This
gives 60 independent experiments per S6 cell and 120 per N6 cell.

## 4. Procedures (all at the same budget B; scope reported)

| Procedure | Scope | Description |
|---|---|---|
| `pcga_l` | L3 | PCGA-L ladder; claim = edge step supported (PCGA verdict rule) |
| `exhaustive_iut` | full | b confirmatory instances × all comparators; IUT (t) |
| `screen_random` | selected | random visiting order, 2 pulls per arm within B/3; top-2; confirm `{empty} + top-2` |
| `screen_uniform` | selected | uniform screening within B/3; top-2; confirm |
| `screen_sh` | selected | successive halving within B/3; top-2; confirm |
| `oracle_select` | selected (oracle) | confirm `{empty, true argmin arm}` with B; an upper bound, not a usable procedure |
| `fullset_alloc` | full | stage 1 exhaustive on `R1 = B/3/(2+K)` dev instances (used only for allocation); minimax-power stage-2 allocation; t at alpha |
| `fullset_elim` | full | as alloc + stage-1 certification at alpha1 = 0.01; stage 2 at 0.04 |
| `fullset_adaptive` | full | as elim + stage-2 test = inverse-normal combination with stage 1 (w1² = 1/3) |

Settings: alpha = 0.05; top-m = 2; n_min = 5; d_floor = 0.003; kappa = 1; hit_tol = 0.002;
confirmatory cap 100 instances.

## 5. Outcomes and decision rules (fixed before results)

Primary (eps = 0.005):
1. **Validity.** For full-set procedures, the N6 claim rate (type I vs the full set) must be
   ≤ 0.05 within MC error (Wilson upper limit ≥ observed; flag if the Wilson lower limit > 0.05).
   For selected-set procedures the N6 claim rate is reported as the "full-set false-claim rate";
   no guarantee applies to it.
2. **Power** in S6 at equal budget, and paired differences with 95% CIs:
   * fullset_adaptive − exhaustive_iut;
   * fullset_alloc − exhaustive_iut;
   * screen_sh − screen_uniform;
   * screen_sh − screen_random.
3. **Discovery rate, estimation error (bias, RMSE of `theta_hat - theta_full`), coverage of
   `theta_full`, fits and measured seconds.**

Decision:
* **GO (methodological contribution)** requires:
  * a full-set procedure with paired power gain over `exhaustive_iut` whose CI excludes 0 in at
    least the hard-binding S6 cells at some budget;
  * no N6 type-I flag;
  * and, separately, an SH advantage counts only if its paired CI excludes 0.
* **CONDITIONAL GO:** gains exist but are confined to narrow regimes or are explained by standard
  adaptive-design components alone.
* **NO-GO for novelty:** no full-set procedure beats exhaustive, and SH does not beat
  uniform/random. Then RUSA is reframed as an audited evaluation protocol extending PCGA-L.

## 6. Execution

Hyperion, bcam-exclusive:
* `scripts/hyperion/pool2b.sbatch` (array over 480 chunks of 120 instances);
* `scripts/hyperion/analyze2b.sbatch` (dependent).

numba 0.58.1 is loaded from `/scratch/hilmibukhori/pylib_numba` (kernel bit-identical to the
reference Python implementation, enforced by test).
