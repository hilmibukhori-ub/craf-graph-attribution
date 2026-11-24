# RUSA — consolidated mathematical specification (after Phases 2A–2C)

This document supersedes, for the final framework, `mathematical_spec.md` (Phase 2A, Props. 1–3)
and `phase2b_math.md` (Props. 4–6). Those files are kept unchanged as the frozen records of their
phases. **No statement here is new statistics.** The guarantees are standard results:
* intersection–union tests (Berger 1982);
* two-stage adaptive combination tests (Bauer & Köhne 1994; Lehmacher & Wassmer 1999;
  Brannath, Posch & Bauer 2002; reviewed in Bretz et al. 2009);

applied to a graph-null comparator set. What RUSA adds is the *protocol*: declared and audited
nulls, explicit scopes, and compute-matched execution (see `novelty_audit.md`).

## 1. Objects and estimands

| Symbol | Meaning |
|---|---|
| `D = (F, y, split)` | node features, labels, train/val/test split |
| `G0` | observed graph |
| `A(G; xi)` | fully specified train-and-select procedure, retrained on every graph variant |
| `S` | test score, higher is better (here `1 − Brier ∈ [0,1]`) |
| `Q_k` | label-free null generator `G0 → G`, from a declared family (ER, degree swap, stratified swap, within-stratum permutation, directed swap) |
| `J` | enumerated, admissibility-audited candidate set, `|J| = K`; `C = {empty} ∪ J` |

```
Delta_k = mu(G0) − E_{G~Q_k(G0,·)} mu(G)          Delta_empty = mu(G0) − mu(G_empty)
theta_full    = min_{j in C} Delta_j                 (full-set robust relational advantage)
theta_sel(S)  = min_{j in {empty} ∪ S} Delta_j       (selected-set advantage, S ⊂ J)
theta_PCGA-L  = Delta_{strat:block}                  (PCGA-L edge step, the L3 → L4 contrast)
```

There are two modes, each with its own estimand:
* **Population** (synthetic studies): instances are i.i.d. from a DGP, and `Delta^P = E_P[Delta]`.
* **Conditional** (one real graph): the expectation is over training seeds and placebo draws
  given `(D, G0)`.

These are different estimands. `theta^P = min_j E[Delta_j] >= E[min_j Delta_j]`.

**The three scopes are different hypotheses.** Each procedure is judged only against the
estimand it certifies:
* PCGA-L answers "does the edge assignment beat a block-preserving rewiring?" Its claims are not
  wrong when `theta_full <= eps`; they answer a different question.
* A selected-set claim is not a full-set claim.

## 2. Hypotheses and the intersection–union certificate

The hypotheses are `H0: theta <= eps` against `H1: theta > eps`, where the practical margin `eps`
is fixed in advance (primary 0.005, secondary 0). `H0 = ∪_j H0_j`, with `H0_j: Delta_j <= eps`.

**P1 (IUT; Berger 1982).** If each `p_j` is valid for `H0_j` and the comparator set is fixed
independently of the confirmatory data, then `p_IUT = max_j p_j` is a valid level-`alpha` test.

**P2 (robust bound).** If each `L_j` is a `(1−alpha)` lower bound for `Delta_j`, then
`min_j L_j` is a `(1−alpha)` lower bound for `min_j Delta_j`. Only the binding comparator
matters, so there is no multiplicity correction.

**P3 (nested radius).** Fixed-sequence testing along a declared nested ladder gives
`P(rho_hat > rho*) <= alpha` (Phase 2A).

## 3. Replication units and marginal tests

`D[r, k] = S[r, real] − S[r, k]` for replicate `r`. Replicates are independent instances
(population mode) or fresh seed bundles with fresh placebo draws (conditional mode). Placebo
draws within `r` are Monte Carlo averaging, not replicates.

The primary marginal test is the one-sided Student t. It is exact under normality (A2) and
otherwise asymptotic. Its calibration is **measured, not assumed**: Phase 2C reports its size on
exact-null A/A contrasts at n = 2..20 (`docs/phase2c_report.md` §6). Bounded alternatives
(empirical Bernstein, WSR betting) are valid without A2 but powerless at these effect sizes
(Phase 2A).

## 4. Selected-set versus full-set certification

Stage 1 (development, `X1`) and stage 2 (confirmation, `X2`) are independent: disjoint instances
or disjoint seed bundles.

**P4 (selected-set validity).** Given `X1`, the IUT over `{empty} ∪ S(X1)` on `X2` has level
`alpha` for `H0_sel: theta_sel(S(X1)) <= eps`.

**P5 (selected-set procedures do not control full-set error).** If a single comparator `j*`
has `Delta_{j*} <= eps` and every other comparator has `Delta_j > eps`, then as the stage-2 size
grows,

`P(claim) → P(j* ∉ S(X1)) · P(confirm | j* ∉ S)`.

This can be far above `alpha`. The excess equals the screen's miss rate times the power against
the decoys. Phase 2C (S7) measures both factors.

## 5. Full-set adaptive certification (the framework's full-set procedure)

**Steps.**
1. **Stage 1.** All comparators get `R1` replicates.
2. **Interim efficacy.** Comparator `j` is certified early if the stage-1 t p-value satisfies
   `p1j <= alpha1`.
3. **Allocation.** The remaining comparators get `n_j(X1)` stage-2 replicates from the
   minimax-power rule (§5.2).
4. **Combination test.** `pj = 1 − Phi(w1 Phi^{-1}(1 − p1j) + w2 Phi^{-1}(1 − p2j))`, with `w1`
   fixed a priori (`w1² = 1/3`, the planned stage-1 share) and `w2 = sqrt(1 − w1²)`.
5. **Claim.** Every comparator is certified, at stage 1 (`alpha1`) or by combination (`alpha2`).
   `alpha1 + alpha2 = alpha`.

**P6 (level).** Under `H0` with binding `j*`:

`P(claim) <= P(p1j* <= alpha1) + P(p1j* > alpha1, pj* <= alpha2) <= alpha1 + alpha2`,

provided conditions (C1)–(C4) below hold. The robust bound (inverted combination test, minimum
over comparators) has coverage `>= 1 − alpha1 − alpha2` by the same argument.

### 5.1 Conditions — the audit checklist (Phase 2C §6 verifies each one)

| | Condition | Why it is needed | How it is ensured / checked |
|---|---|---|---|
| C1 | `p1j` valid under `H0_j` | interim term `<= alpha1`; combination validity | t-test; size measured at `n = R1` on exact-null contrasts |
| C2 | `p2j` conditionally super-uniform given `X1` | combination validity with data-dependent `n_j` | `X2 ⟂ X1` by disjoint seed keys; `n_j` is a function of `X1` only; stage-2 replicates are taken in a fixed order (`conf[:n_j]`), never chosen by their values |
| C3 | weights fixed before data | otherwise the combined statistic is not N(0,1)-dominated | `w1 = sqrt(search_frac)` is a config constant. Mismatch with the realised information fraction `R1/(R1 + n_j)` costs power, not validity |
| C4 | stage-1 data used only through `(p1j, n_j)` | interim decision and allocation are `X1`-measurable | code path: `fullset_adaptive` receives `D1` and the allocation; the margin `eps` is fixed |
| C5 | full-set scope | every comparator in `C` is tested | `stage[j] in {dev, combined}` for all `j`. A comparator with fewer than 2 replicates is "untested" with `L = −inf`, which blocks the claim |
| C6 | the feasibility branch chosen a priori | otherwise the branch choice could depend on data | §5.3 |

Under (C1)–(C4), conditionally on `X1`, `Phi^{-1}(1 − p2j)` is stochastically no larger than
N(0,1) under `H0_j` whatever `n_j(X1)` is. With fixed weights, `w1 z1 + w2 z2` is therefore
dominated by N(0,1) given `z1`, and hence unconditionally. Because the t p-values are exact only
under normality, the procedure is exactly as approximate as the t-test itself, and no more.

### 5.2 Allocation (power heuristic; irrelevant for validity)

`pi_j(n) = Phi(sqrt(n) d_j / s − t_{1−alpha2, n−1})`, with the conservative plug-in
`d_j = max(delta_hat_j − kappa·se_j − eps, d_floor)`. The rule maximises `min_j pi_j` subject to
`max_j n_j + sum_j n_j <= C2` and `n_j >= n_min`. In the normal limit with no floors, this gives
`n_j ∝ s² / d_j²`.

### 5.3 Small-budget feasibility (Phase 2C)

The adaptive branch runs iff `R1 (2 + K) + n_min (K + 2) <= B`. Otherwise the procedure is
exactly `exhaustive_iut` with the whole budget.

**P7.** The rule depends on `(b, K, R1, n_min)` only. The executed branch is therefore fixed
before any data, and the procedure has the level of that branch: `alpha` for exhaustive, or
`alpha1 + alpha2` for adaptive.

Lowering `n_min` (5 → 3) changes only which budgets are feasible and the degrees of freedom of
the stage-2 t-tests. Validity at small `n` rests on C1/C2 at that `n`, which Phase 2C measures.

## 6. Placebo exchangeability, admissibility, scope of claims

These are unchanged from Phase 2A (`mathematical_spec.md` §§6, 8, 9).
* The admissibility audit verifies hard constraints exactly and applies label-free soft rules.
  Admissibility is a declared modelling assumption, not a verified truth.
* There is no guarantee beyond the enumerated, frozen candidate set, and no causal reading of
  edges.
* Absence of a certificate is not evidence of no relational value.
