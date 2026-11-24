# Phase 2B — mathematical justification of the screening and allocation procedures

This extends `mathematical_spec.md` (Props. 1–3). The notation is the same, with these additions:
* `J` is the enumerated admissible candidate set (K nulls);
* `C = {empty} ∪ J` is the comparator set;
* `theta_full = min_{j in C} Delta_j`;
* `H0: theta_full <= eps`.

**Replication units.** There are two independent sets of instances (or seed bundles): stage 1
("development", `R1` units) and stage 2 ("confirmation"). They come from disjoint seed keys, so
stage-1 data `X1` and stage-2 data `X2` are independent.

## 1. Two kinds of certificate

| Kind | Certified statement | Procedures |
|---|---|---|
| **selected-set** | `theta_sel = min_{j in {empty} ∪ S(X1)} Delta_j > eps`, where `S(X1) ⊂ J` is a set selected from stage-1 data | `screen_random`, `screen_uniform`, `screen_sh`, `oracle_select` (with `S` = true argmin) |
| **full-set** | `theta_full > eps` | `exhaustive_iut`, `fullset_alloc`, `fullset_elim`, `fullset_adaptive` |

**Proposition 4 (selected-set validity, conditional).** Given `X1`, the confirmatory IUT over
`{empty} ∪ S(X1)` has level `alpha` for `H0_sel: theta_sel <= eps`. *Proof.* `S(X1)` is fixed
given `X1`, and `X2` is independent of `X1`; apply Prop. 1 conditionally. ∎

**Proposition 5 (selected-set procedures do not control full-set error).** There exist
configurations with `theta_full <= eps` and `P(claim) -> P(S(X1) ∌ j*) · 1 > alpha` as the
stage-2 size grows. Here `j*` is the binding arm and every other comparator has
`Delta_j > eps`.
*Proof.* If `j* ∉ S`, every confirmed comparator has `Delta > eps` and the IUT rejects with
probability tending to 1. ∎

This is the formal reason that a screened certificate may only be reported as selected-set. It is
illustrated in `tests/test_phase2b.py::test_selected_set_screening_is_not_fullset_valid`. The size
of the gap is exactly the miss probability of the screen, which Phase 2B measures ("discovery").

## 2. Full-set procedures

All three full-set procedures test **every** comparator in `C`. Stage 1 only decides (a) whether a
comparator is certified early, and (b) how many stage-2 replicates `n_j(X1)` it gets.

### 2.1 Allocation only (`fullset_alloc`, `alpha1 = 0`)

`n_j = n_j(X1)`; stage-2 marginal one-sided t-tests at level `alpha`; IUT over `C`.

**Proposition 6a.** `P(claim | H0) <= alpha` for any allocation rule that is a function of `X1`
(and external randomness) only.
*Proof.* Condition on `X1`. The `n_j` are fixed and `X2` is independent. Under `H0` the binding
`j*` has `Delta_{j*} <= eps` and its stage-2 test is a valid level-`alpha` test with `n_{j*}`
replicates. Prop. 1 applies conditionally; integrate over `X1`. ∎

Mis-allocation, such as giving `j*` few replicates because its stage-1 estimate looked large,
reduces power only.
`tests/test_phase2b.py::test_fullset_valid_under_adversarial_allocation` deliberately gives the
binding arm the *largest* stage-1 estimate and checks the level by Monte Carlo.

### 2.2 Stage-1 elimination (`fullset_elim`, `alpha1 > 0`)

Comparator `j` is "eliminated", i.e. certified at stage 1, if its stage-1 one-sided t bound at
level `alpha1` exceeds `eps`. The remaining comparators are tested on stage 2 at level
`alpha2 = alpha - alpha1`.

**Proposition 6b.** `P(claim | H0) <= alpha1 + alpha2`.
*Proof.* A claim requires `j*` to be certified at one of the two stages:
* `P(stage-1 rejects j*) <= alpha1`;
* conditionally on not being eliminated (an `X1`-event), the stage-2 test of `j*` has level
  `alpha2`.

Hence `P(claim) <= alpha1 + (1 - P(elim)) alpha2 <= alpha1 + alpha2`. ∎

The robust lower bound `min_j L_j`, with each `L_j` taken from the stage at which `j` was
certified, has coverage `>= 1 - alpha1 - alpha2` for `theta_full`, by the same union argument.

### 2.3 Adaptive combination (`fullset_adaptive`)

Stage-1 data are *reused*. Each non-eliminated comparator is tested with the inverse-normal
combination `p_j = 1 - Phi(w1 z1j + w2 z2j)`, where:
* `zij = Phi^{-1}(1 - p_ij)`;
* `p_ij` is the one-sided t p-value of stage `i`;
* the weights `w1 = sqrt(1/3)` (the prespecified stage-1 budget share) and `w2 = sqrt(1 - w1^2)` are
  fixed before any data.

**Proposition 6c (Bauer & Köhne 1994; Lehmacher & Wassmer 1999).** Under `H0_j`, if `p_1j` is
valid and `p_2j` is conditionally valid given `X1` (true here: the stage-2 sample is independent
and its size `n_j(X1)` is fixed given `X1`), then `p_j` is valid **for any data-dependent choice of
`n_j(X1)`**. With interim efficacy at `alpha1`, the procedure has level `<= alpha1 + alpha2`
(union bound as in 6b).
*Proof sketch.* `z2j | X1` is (stochastically smaller than) N(0,1) under `H0_j` with the boundary
`Delta_j = eps`. The combination statistic with fixed weights is therefore N(0,1)-dominated
conditionally on `z1j`, and hence unconditionally. ∎

Two caveats:
* The t-based `p_ij` are exact only under normality (assumption A2 of Phase 2A). The procedure
  inherits the approximate validity of the t-test; there is no new approximation.
* The robust bound for `fullset_adaptive` inverts the combination test over the margin. The
  combined p-value is increasing in the margin, so the inversion is a valid level-`alpha2`
  lower bound for each `Delta_j`.

### 2.4 Allocation rule (minimax power)

The approximate power of the one-sided t-test of `j` with `n` stage-2 replicates is

```
pi_j(n) = Phi( sqrt(n) d_j / s - t_{1-a, n-1} ),     d_j = Delta_j - eps.
```

For an IUT, `P(all j reject) >= 1 - sum_j (1 - pi_j(n_j))`. Under budget
`max_j n_j + sum_j n_j <= C2` (one real-graph fit per stage-2 unit plus one fit per comparator
replicate), the allocation maximises the smallest `pi_j`:

```
n_j(q) = min{ n >= n_min : pi_j(n) >= q },   q* = max{ q : cost(n(q)) <= C2 },
```

with leftover budget spent on the currently least-powered comparator. This is a minimax
(equalised-power) rule. In the normal limit with no floors it reduces to
`n_j ∝ s^2 / d_j^2`, the classical optimal allocation for a minimum of independent means.

Plug-in values are deliberately **conservative**:
* `d_j = max(delta_hat_j - kappa·se_j - eps, d_floor)`, with `kappa = 1`;
* `d_floor = 0.003`;
* `n_min = 5` (≥ 4 degrees of freedom for every comparator).

The rule is a heuristic for power. Validity never depends on it (Props. 6a–c).

**When can allocation beat exhaustive uniform allocation at equal budget?** Let `F` be the
"binding family", the comparators with `d_j` near the minimum `d*`, and let `m = |C|`.
* Uniform allocation gives each comparator `N/m` replicates.
* Allocation gives the binding family about `(N - (m - |F|) n_easy) / |F|`.

The gain needs both `|F| << m` and `n_easy << N/m`. It is offset by the stage-1 cost, which is
wasted in `fullset_alloc` and partly recovered in `fullset_adaptive` at the price of an
`alpha1/alpha2` split and a weight mismatch. The pilot DGPs have `|F| ≈ 5` (K = 18) and
`|F| ≈ 9` (K = 48) near-binding w3-containing comparators. So the attainable gain is bounded by
roughly `m/|F|` ≈ 4–5 in replicates for the binding family, before the stage-1 cost and the floors
for easy comparators are paid. Phase 2B measures whether any of it survives.

## 3. Search procedures for selected-set screening

Uniform, successive halving and random search are as defined in Phase 2A / `nulls/search.py`.
Development pulls in Phase 2B use test-node scores on **development instances**. This is valid
because development and confirmatory instances are independent (Prop. 4 needs only `X1 ⟂ X2`).
In conditional (single-graph) use, development replicates must be fresh seed bundles.

## 4. Estimation target and metrics

| Metric | Definition |
|---|---|
| `theta_hat` | min over the procedure's comparators of their estimated mean contrasts. A plug-in of a minimum, so biased downward by noise and **upward** when the binding comparator is not confirmed. |
| `est_error` | `theta_hat - theta_full` |
| `covered_full` | `L_robust <= theta_full` (meaningful as a guarantee only for full-set procedures) |
| `discovered` | the selected set (screens) or the top-allocated comparator (full-set) is within `hit_tol = 0.002` of `theta_full` |

## 5. What would count as methodological value (decided before results)

1. A **full-set** procedure (`fullset_*`) with higher power than `exhaustive_iut` at equal
   budget, with type-I error ≤ alpha up to MC error in N6. This would be a genuine computational
   allocation contribution, though built from standard adaptive-design components.
2. `screen_sh` beating `screen_uniform` / `screen_random` in discovery and in N6 false-claim
   rate at equal budget. This would be value of the search algorithm, for selected-set use.
3. Otherwise: no algorithmic value; reframe as an audited evaluation protocol extending PCGA-L.
