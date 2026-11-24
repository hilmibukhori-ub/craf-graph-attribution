# RUSA — final proposed framework (after Phase 2C)

**RUSA is an audited relational attribution and evaluation protocol that extends PCGA-L.**
It asks a question that PCGA-L does not ask: does the *specific edge assignment* of a graph
improve a fixed predictive model beyond **every** member of a declared, audited family of graph
nulls, by more than a practical margin `eps`?

RUSA does not replace PCGA-L. The PCGA-L ladder (empty → ER → degree → block → real) is kept
as the descriptive, attribution part of the protocol, and its edge step keeps its own meaning
and validity. RUSA adds:
* a declared candidate family;
* an admissibility audit;
* explicitly scoped certificates;
* compute-matched execution.

Mathematical details: `docs/rusa_mathematical_spec.md`. Evidence: `docs/phase2a_report.md`,
`docs/phase2b_report.md` and `docs/phase2c_report.md`.

## Components

| # | Component | Status | Origin / attribution |
|---|---|---|---|
| 1 | **Declared null family and candidate enumeration**: ER, degree swap, stratified swaps over declared metadata (orders 1–2), within-stratum permutation, directed swaps; Besag–Clifford chains for exchangeable placebos | kept | standard network null models (Maslov–Sneppen-type swaps; Fosdick et al. 2018; Orsini et al. 2015); Besag & Clifford 1989 |
| 2 | **Admissibility audit**: exact hard constraints on every sample, prespecified label-free soft rules, logged and frozen | kept | protocol contribution |
| 3 | **PCGA-L ladder** (attribution) | kept unchanged | PCGA / PCGA-L |
| 4 | **Full-set certificate**: IUT over `{empty} ∪ J` with a robust lower bound on `theta_full` | kept; the primary claim | Berger 1982 |
| 5 | **Full-set adaptive execution**: interim efficacy + minimax-power allocation + inverse-normal combination, with an a-priori feasibility fallback to exhaustive IUT | kept as an optional compute-saving execution mode. Variant and defaults are in the "Defaults" section below | Bauer & Köhne 1994; Lehmacher & Wassmer 1999; Brannath et al. 2002; Bretz et al. 2009 |
| 6 | **Selected-set screening** (uniform screen → confirm `{empty} + top-m`) | kept **only** as an exploratory or selected-set report, always labelled with its scope | standard data splitting / screen-then-confirm |
| 7 | Successive halving / hardest-null search | **removed** (no evidence of value in 2B or 2C) | Jamieson & Talwalkar 2016; Li et al. 2018 |
| 8 | Nested robustness radius | kept (descriptive, fixed-sequence) | fixed-sequence testing |

## Steps for a real-world analysis

1. **Declare.** Fix the model `A`, the metric and the split protocol; the metadata available for
   stratification; the candidate family `J`; `eps`; `alpha`; the budget; and the replication
   mode. In conditional single-graph mode, replicates are fresh seed bundles with fresh placebo
   draws. Freeze all of this (hash) before any confirmatory fit.
2. **Audit.** Generate placebo samples on development seeds and drop inadmissible candidates by
   the prespecified rules. The audited `J` is then frozen.
3. **Attribute (PCGA-L).** Report the ladder steps with their own tests. They are descriptive of
   *where* the gain enters, and they are not full-set claims.
4. **Certify (full set).** Use `exhaustive_iut` over `{empty} ∪ J`, or the adaptive mode under
   the defaults below. Report `L_robust`, the binding comparator and the claim at `eps`.
5. **Report scope explicitly.** The labels are "full-set (K = …)", "selected-set (S = …)" or
   "PCGA-L edge step". A selected-set result must never be reported as a full-set result
   (Prop. P5; Phase 2C S7 gives the empirical demonstration).
6. **Report cost.** Give fits and wall-clock time for each component.

## Defaults

The defaults come from the Phase 2C results (`docs/phase2c_report.md` §9). The adaptive-mode
default was chosen **after** seeing the results, and is disclosed as such.

| Setting | Default |
|---|---|
| alpha / eps | 0.05 / declared per application (0.005 in the synthetic studies) |
| marginal test | one-sided t. Its size must be checked on an A/A construction with the application's own nulls before confirmation |
| full-set certificate | `exhaustive_iut` |
| optional compute-saving mode | `fullset_adaptive_fb`: stage-1 share 1/3, interim alpha1 = 0.01, combination alpha2 = 0.04, `w1² = 1/3`, minimax-power allocation with `n_min = 5`, `kappa = 1`, `d_floor = 0.003`. If `R1(2+K) + 5(K+2) > B`, run `exhaustive_iut` instead (decided before data) |
| not recommended | `n_min = 3`. It is valid, but no more powerful, and once significantly less powerful, at b = 6 |
| selected-set screen (exploratory only) | uniform screening of B/3, top-2, confirm `{empty} + top-2` |
| replication units | population mode: independent instances. Conditional mode: fresh seed bundles with fresh placebo draws, disjoint between stages |
| models | report at least one model shown to use edge-level information. A null result with one architecture is not a statement about the graph |
