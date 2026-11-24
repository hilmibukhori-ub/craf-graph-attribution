# Assumptions ledger and limitations (Phase 2A)

Each row states the assumption, what depends on it, how it is checked, and its status.
"Verified" means a test or a pilot measurement checks it. "Assumed" means nothing in Phase 2A
can check it.

## A. Statistical assumptions

| # | Assumption | Used by | Check | Status |
|---|---|---|---|---|
| A1 | Replicate rows `D[r,·]` are i.i.d. | all marginal tests, IUT | population: disjoint seed keys per instance; conditional: fresh seed + placebo per bundle | verified by construction (`utils/seeding.py`) |
| A2 | t-test approximately valid at `R = 12..40` for these contrasts | primary inference | A/A exact boundary + cross-fitted coverage (pilot) | **measured in pilot** |
| A3 | Comparator set fixed independently of confirmatory data | Prop. 1–3 | dev/confirm instance split; freeze; leakage test | verified (code + `test_no_leakage.py`) |
| A4 | `S in [0,1]` | EB / WSR bounds | metric definition (1 − Brier, clipped probabilities) | verified |
| A5 | Symmetry of `D − eps` under `H0` | sign-flip test | not checkable in general | assumed; sensitivity only |
| A6 | Nested levels prespecified | radius (Prop. 3) | API rejects non-nested levels | verified; ordering choice is assumed |
| A7 | MC truths accurate enough to score coverage | calibration study | cross-fitted truth on the other half of the pool; MC SE reported | partially: truth error inflates measured miscoverage slightly (about 0.1–0.15 of the subset SE at `R=40`) |
| A8 | `G0` uniform on its swap class (for an exact rank test) | PCGA/PCGA-L rank test with BC chains | not checkable from one graph; false for SBM-type graphs | **assumed / generally false**; rank test reported only as a sharp-null test |

## B. Null-model assumptions

| # | Assumption | Check | Status |
|---|---|---|---|
| B1 | Swap chain reversible with uniform law on its communicating class | symmetric proposal by construction (`_swap_kernel_py`); not tested numerically | argued, not tested |
| B2 | 5 swaps/edge mixes adequately | edge overlap with `G0` and among draws (audit) | proxy only; no formal mixing diagnostic |
| B3 | Declared admissible properties (degree, block / metadata composition) are scientifically right for the "no relation-specific information" world | none | **assumed** — the central modelling choice |
| B4 | Candidate set (18 generators) contains a competitive null | none in applications; known in synthetic DGPs | synthetic only |
| B5 | Strat swaps can reach a diverse sample in highly constrained strata | acceptance, overlap, completion (audit) | measured; joint strata have about 3% move acceptance |

## C. Synthetic-design assumptions

| # | Assumption | Status |
|---|---|---|
| C1 | DGP features/graph/split independent of labels except through the stated mechanism | verified (`test_no_leakage.py::test_dgp_graph_features_split_do_not_depend_on_label_mechanism`) |
| C2 | "Known generative fact" (e.g. S3: only block composition matters) implies Δ ≈ 0 under the matching null | **not implied exactly**: structural differences between `G0` and placebos can change model variance. Measured as MC truth, not assumed. Only the A/A families have Δ = 0 exactly. |
| C3 | Effect sizes were chosen on dev seed 999 before the pilot | recorded in `synthetic.py` and the protocol |
| C4 | SGC-ridge behaves like a GNN for the questions studied | partially checked by the GCN/SAGE pilot (estimates only) |

## D. Limitations (known before results)

1. **Scope of certificates.** Full RUSA certifies only `{empty} ∪ selected nulls`. When the search
   misses the hardest admissible null, it can claim superiority that the full candidate set would
   refute. The pilot reports this as "false vs full".
2. **Single synthetic family.** One DGP family (DC-SBM, n = 300, binary labels). Results may not
   transfer to other graph sizes, heterophily regimes, metrics or real graphs.
3. **Closed-form workhorse.** Calibration Monte Carlo uses SGC-ridge (deterministic given data).
   Training-seed variance of neural models is absent from the calibration study. Neural models
   appear only in small estimation pilots.
4. **Small-n asymptotics.** The primary t-procedure relies on approximate normality of `D` at
   `R = 12–40`.
5. **No real data.** Phase 2A intentionally has no real-graph experiments.
6. **Literature audit is targeted, not systematic** (`novelty_audit.md` §3).
7. **Admissibility is declared, not discovered.** The hardest *admissible* null depends on the
   declaration. A harder null outside the declared family (e.g. preserving neighbour *feature*
   composition) would remove relation signal in S1 too. That would be a scientific question,
   not a statistical one.

## E. Corrections to the Phase 1 (PCGA / PCGA-L) formulation

1. **L3 edge-step exactness.** The PCGA manuscript states that the edge step uses an "exact rank
   test against retrained L3 placebos, whose exactness rests on the exchangeability argument".
   That argument holds for the within-industry *node permutation* orbit. It does not hold for L3
   placebos produced by a swap chain started at `G0`. **Correction:** use the Besag–Clifford
   parallel construction (`chain="besag_clifford"`), or call the L3 rank test approximate. Even
   then, exactness concerns a sharp null on `G0`'s placement in its class, not `H0: Δ ≤ eps`.
2. **Unverified swap counts.** `dapilot/ladder.py::double_edge_swap` stops after
   `50 * n_swaps` attempts and silently returns fewer swaps than requested. RUSA reports
   `achieved_swaps` and rejects samples with completion below 0.95.
3. **Population vs conditional.** The PCGA-L construct-recovery study correctly uses independent
   DGP seeds as units. The empirical re-tests use one graph and per-seed or rank inference. Their
   conclusions are conditional on that graph/split and must not be read as population statements.
   (The manuscript largely says this already; no change is needed beyond keeping the wording.)
