# Phase 2A experiment protocol

## 1. Timeline and freezing

| Step | Date (UTC) | Seeds | Artefact |
|---|---|---|---|
| Development: code, unit tests, smoke runs | 2026-11-23 | 7, 11, 424242 (tests/smoke) | `tests/`, `outputs/smoke` (local, regenerable) |
| DGP effect-size calibration (40 instances per setting, 7 nulls) | 2026-11-23 | **999** (dev only) | values written into `data/synthetic.py: SCENARIOS` |
| Pilot plan freeze: config + all `src/` + `scripts/` hashed | 2026-11-24, before any pilot instance existed | — | `outputs/pilot/FREEZE.json`; every SLURM task verifies it |
| Pilot execution (Hyperion, DIPC) | 2026-11-24 | **20261123** | `outputs/pilot*` |
| Confirmatory study | not run | 20270101 (reserved) | `configs/confirmatory.yaml` (template) |

The freeze-time protocol is `configs/pilot.yaml` plus the code. This document describes it and was
written after the freeze but before any pilot output was read.

## 2. Development-phase DGP calibration (disclosed)

Effect sizes `gamma` were chosen on dev seed 999 so that each scenario tests what it is designed
to test:
* S5/S4: the real graph beats the empty graph by a clear margin, while the hidden null is
  competitive;
* S1: the relational signal is detectable.

Observed dev means (40 instances, test 1 − Brier contrasts; development numbers, **not results**):
* S5 at gamma=2: Δ_empty ≈ +0.005 (too close to eps), so gamma=3 was chosen (Δ_empty ≈ +0.009).
* S1 at gamma=1: Δ_empty ≈ +0.009.
* At gamma=1, S5 had Δ_empty < 0. The empty graph beating the real graph would make every search
  irrelevant, so gamma was increased.

No pilot-seed output was used for these choices.

## 3. Design (population inference)

* **Replication unit.** An independently simulated instance (graph, attributes, labels, split),
  n = 300 nodes, average degree 8, 3 blocks, 4 binary metadata attributes, 4 continuous features.
* **Model.** SGC-ridge (closed form). Matched empty graph = zeroed propagation channels.
* **Candidates (K = 18).** er, degree, perm:block, strat:{block, w1..w4}, and strat over all 10
  pairs of {block, w1..w4}. Each is drawn twice per instance with 5 swaps/edge and audited.
* **Scenarios and instance counts.** S0 4800; S1 gamma ∈ {0.5, 1.0, 1.5, 2.0} (4800 for 1.0,
  2400 otherwise); S1_hetero 2400; S2, S3, S4, S5 4800 each; A/A degree and A/A block 4800 each.
* **Monte Carlo experiments.** Disjoint blocks of 60 instances, i.e. 80 independent experiments
  for a 4800 pool and 40 for a 2400 pool. Within a block, instances 0–9 are development data
  (search only, validation scores only) and 10–59 are confirmatory.
* **Budget.** `B = r_base (2 + K) = 12 × 20 = 240` model fits per experiment for every procedure.
  A procedure that needs fewer fits per instance uses more confirmatory instances, capped at 50.
* **Procedures.** pcga, pcga_l, single_degree, menu_iut (RUSA without search), iut_all (critical
  baseline), rusa_uniform, rusa_sh (search budget B/3, top-m = 2, confirm {empty} ∪ top-2).
* **Inference.** alpha = 0.05 one-sided. Primary eps = 0.005; secondary eps = 0. Primary
  marginal test: one-sided t. PCGA/PCGA-L use their own verdict rule (Holm over two-sided
  Wilcoxon + mean sign + 95% t interval) and have no eps.
* **Truth.** Monte Carlo mean contrasts over the full pool (all valid draws). A/A families use the
  exact value 0. The calibration study uses cross-fitted truths (the other half of the pool).
* **Calibration study.** For every scenario × comparator, disjoint subsets of R ∈ {12, 40}
  instances; methods t, bootstrap, sign-flip, empirical Bernstein, WSR betting. The metric is
  the one-sided miscoverage rate `P(L > Δ_true)` with Wilson intervals. Global IUT type I is
  measured at the exact A/A boundary.

## 4. Outcomes

* **Gate B:** A/A rejection ≈ 0.05 (Wilson interval contains 0.05 or lies below it); marginal
  miscoverage ≤ 0.05 up to MC error across scenarios; global IUT rejection ≤ 0.05 at the boundary.
* **Gate C:** at equal budget, compared with iut_all and menu_iut:
  * rusa_sh/rusa_uniform have higher claim rates when `theta_full > eps` (power), **and**
  * their false claims vs the full candidate set are not higher when `theta_full <= eps`.
  * Separately: does SH beat uniform screening (paired hit rate)?
* Secondary outcomes: search hit / regret, coverage of each procedure's own target, fits used,
  audit statistics.

## 5. Small pilots (estimation only)

* **GNN population pilot.** GCN and SAGE (plain torch); S1_g150, S3, S4, S5; 48 instances each;
  comparators empty, er, degree, perm:block, strat:block, strat:w3, strat:block+w3. One dataset
  per cell, so these give estimates and certificates, **not calibration**.
* **Conditional demo.** One fixed instance (index 0) of S1_g150 and S3; GCN; 30 independent
  seed bundles. Swap nulls use the Besag–Clifford chain. Reports conditional t bounds and the
  PCGA rank test.

## 6. Exact commands (as executed)

```bash
python scripts/freeze_plan.py --config configs/pilot.yaml                       # local, before runs
rsync -az --exclude __pycache__ ./ hyperion:/scratch/hilmibukhori/rusa/
# on hyperion, from a clean shell:
sbatch --array=0-479 scripts/hyperion/pool.sbatch configs/pilot.yaml sgc        # job 8188012
sbatch --array=0-31  scripts/hyperion/pool.sbatch configs/pilot.yaml gnn        # job 8188013
sbatch --array=0-1   scripts/hyperion/conditional.sbatch configs/pilot.yaml     # job 8188014
sbatch --dependency=afterok:8188012:8188013 scripts/hyperion/analyze.sbatch configs/pilot.yaml  # 8188015
```
