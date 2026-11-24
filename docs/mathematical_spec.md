# RUSA — mathematical specification (Phase 2A)

Status: specification of what the code in `src/rusa` computes and of the guarantees it
claims. Every guarantee below is conditional on stated assumptions. None of them is new
statistics; see `novelty_audit.md`.

## 1. Objects

| Symbol | Meaning | Code |
|---|---|---|
| `D` | node features `F`, labels `y`, split (train/val/test) | `data/synthetic.py: Instance` |
| `G0` | observed graph (simple, undirected unless stated) | `nulls/generators.py: Graph` |
| `A(G; xi)` | full training-and-selection procedure on graph `G` with randomness `xi` | `models/*.py: fit_score` |
| `S` | score on test nodes, **higher is better**; Phase 2A uses `S = 1 - Brier`, bounded in `[0,1]` | `models/baselines.py` |
| `Q_k` | null (placebo) generator: a label-free Markov kernel `G0 -> G` | `NullSpec.sample` |
| `G_empty` | matched no-relation control: same architecture, graph channels/operators zero (SGC) or identity (GCN) | `sgc_features(F, None)`, `gcn_operator(None)` |

`A` is fully specified (protocol A): SGC-ridge standardises on train nodes, selects the ridge
penalty from a fixed grid by validation Brier, and only then computes test predictions. GCN and
SAGE use full-batch Adam with fixed hyperparameters, early stopping on validation BCE (patience
30), and restore the best weights. Every graph variant is **retrained**.

## 2. Estimands

Conditional on a fixed `(D, G0)`:

```
mu(G)      = E_xi[ S(A(G; xi)) ]
mu_k       = E_{G ~ Q_k(G0, .)} E_xi[ S(A(G; xi)) ]
Delta_k    = mu(G0) - mu_k                 (k = 1..K)
Delta_empty= mu(G0) - mu(G_empty)
theta_RUSA = min(Delta_empty, Delta_1, ..., Delta_K)
```

`Delta_empty` is PCGA's graph utility `U`. `Delta_k` with `k` = perm-within-block is PCGA's
relation specificity `S`.

**Population version** (synthetic studies). Instances `(D_r, G0_r)` are i.i.d. draws from a
data-generating process `P`. Define `Delta_k^P = E_P[Delta_k(D, G0)]` and `theta^P = min_j Delta_j^P`.
This is the estimand of the pilot in `outputs/pilot`. It is **not** the same as the
conditional estimand for any particular graph. Note that
`theta^P = min_j E[Delta_j] >= E[min_j Delta_j]`: the population minimum of means is not the
mean of per-instance minima. RUSA certifies the former.

## 3. Hypotheses and the intersection–union test

`H0: theta <= eps` vs `H1: theta > eps`, where `eps >= 0` is a practical margin fixed in
advance. In Phase 2A the primary value is `eps = 0.005` (1 − Brier units) and `eps = 0` is
secondary; both were fixed before the pilot.

`H0 = union_j H0_j` with `H0_j: Delta_j <= eps`. Given marginal tests with
`P(p_j <= a) <= a` under `H0_j`, the IUT rejects `H0` when `p_IUT = max_j p_j <= alpha`.

**Proposition 1 (IUT; Berger 1982).** If every `p_j` is valid for `H0_j` and the comparator set
`J` is fixed independently of the confirmatory data, then `P(p_IUT <= alpha) <= alpha` under `H0`.
*Proof.* Under `H0` some `j*` has `Delta_{j*} <= eps`, and
`{max_j p_j <= alpha} ⊆ {p_{j*} <= alpha}`. ∎

**Proposition 2 (robust lower bound).** If `P(L_j <= Delta_j) >= 1 - alpha` for every `j`, then
`P(min_j L_j <= theta) >= 1 - alpha`. *Proof.* Let `j*` attain the minimum of `Delta_j`. Then
`min_j L_j <= L_{j*}`, and `L_{j*} <= Delta_{j*} = theta` with probability `>= 1 - alpha`. ∎

No multiplicity correction is needed for the *single global claim*. These statements do not
certify the individual `Delta_j > eps`; that requires simultaneous inference (Bonferroni,
`inference/certificates.py: bonferroni_bounds`).

**Counterexample (selection on confirmatory data).** Let `J` be chosen as the `m` comparators
with the *largest* observed `D`-means on the confirmatory data, and then apply the IUT. Under
`H0` with one comparator at `Delta = eps` and the rest far above, the null comparator is dropped
whenever its noisy mean falls low. The rejection probability then exceeds `alpha`. This is why
the search uses development data only and its output is serialised before confirmation
(`SearchResult.freeze`). The code-level guard is `tests/test_no_leakage.py::test_search_and_freeze_are_invariant_to_test_scores`.

**Counterexample (certificate scope).** If the search freezes `J_sel ⊂ J_cand` and the IUT
certifies `min_{j in J_sel} Delta_j > eps`, nothing follows for `min_{j in J_cand} Delta_j`. A miss
by the search (a harder arm left unselected) yields a valid certificate for the *wrong* question.
Phase 2A measures how often this happens ("false vs full" rates).

## 4. Nested robustness radius

Take nested comparator sets `Q_1 ⊂ Q_2 ⊂ ... ⊂ Q_Lambda`, prespecified and frozen. Define
`theta(lam) = min_{j in Q_lam} Delta_j`, which is non-increasing in `lam`, and
`rho* = max{lam : theta(lam) > eps}` (0 if the set is empty). The estimator is
`rho_hat = max{lam : min_{j in Q_lam} L_j > eps}`, where each `L_j` is a **marginal** level-`alpha`
bound.

**Proposition 3.** `P(rho_hat > rho*) <= alpha`.
*Proof.* `L(lam) := min_{j in Q_lam} L_j` is non-increasing in `lam`. So `rho_hat > rho*` implies
`L(rho*+1) > eps`, which means every `L_j > eps` for `j in Q_{rho*+1}`. In particular this holds
for `j*` attaining `theta(rho*+1) <= eps`, so `L_{j*} > eps >= Delta_{j*}`. That is a miscoverage
event of a single marginal bound and has probability `<= alpha`. ∎

This is the fixed-sequence / closed-testing logic applied to nested IUTs. It covers the claim
"the radius is not overstated". Reporting the whole *curve* `lam -> lower bound on theta(lam)` with
joint coverage needs simultaneous bounds; the code reports Bonferroni bounds for this. Proposition 3
requires the levels to be nested and fixed in advance. An adaptively chosen ordering voids it.

## 5. Replication units and marginal tests

For replicate `r` (an independent instance in population mode, an independent seed bundle in
conditional mode):

```
D[r, k]     = S[r, real] - mean_b S[r, k, b]        (b: placebo draws within r)
D[r, empty] = S[r, real] - S[r, empty]
```

Placebo draws within `r` are Monte Carlo averaging and do not add replicates. The rows
`D[r, ·]` must be i.i.d. across `r`.
* Population mode: i.i.d. holds by construction, because instances are generated from disjoint
  seed keys.
* Conditional mode: i.i.d. holds given `(D, G0)` (and the Besag–Clifford hub when used),
  provided seeds and placebo draws are fresh per `r`.

Marginal methods (`inference/tests.py`):

| Method | Validity | Role |
|---|---|---|
| one-sided Student t | exact if `D` normal; asymptotic otherwise | primary; calibrated by A/A |
| percentile bootstrap | asymptotic; known small-`n` undercoverage | sensitivity |
| sign-flip | exact if `D - eps` symmetric under `H0` (assumption) | sensitivity |
| Maurer–Pontil empirical Bernstein | finite-sample, i.i.d., `D in [-1, 1]` | conservative bounded option |
| Waudby-Smith–Ramdas betting (predictable plug-in, bets truncated to `[0, 0.75]`) | finite-sample by Ville's inequality, `D in [-1, 1]` | conservative bounded option |

The bounded methods use the a priori range `[-1, 1]` of a difference of two `[0,1]` scores. This
is valid but very wide relative to Phase 2A effect sizes (about 0.01), so they are expected to be
powerless at `n <= 40`. The pilot measures this instead of assuming it. For unbounded metrics
(log-loss, MSE) these two methods must **not** be used without a proven bound.

**WSR monotonicity.** Bets are truncated at `c = 0.75`, independently of the tested mean `m`.
Since `m <= 1` this keeps every wealth factor `>= 0.25`. It also makes `log K_t(m)` strictly
decreasing in `m`, so the rejected set is an interval and bisection gives a valid bound. An
`m`-dependent cap `c/m` would break this monotonicity.

## 6. Placebo exchangeability and the PCGA rank test

The PCGA rank p-value `(1 + #{k: S_k >= S_0}) / (K + 1)` is exact if `(S_0, S_1, ..., S_K)` is
exchangeable under `H0`. Two cases:

* **Group-orbit placebos** (node permutation within strata). If `H0` states that `G0`'s labelling
  is a uniform draw from its orbit, then `G0` and i.i.d. uniform orbit draws are exchangeable
  (PCGA's argument; correct).
* **Swap-chain placebos** (PCGA-L L2/L3; RUSA `degree`, `strat:*`). Each placebo is the endpoint
  of an MCMC chain **started at `G0`**. Even if `G0` is uniform on its class, `G0` and its
  descendants are not exchangeable for a finite chain, so the rank test is not exact. It is
  approximately valid only if the chain mixes. **Correction:** the Besag & Clifford (1989)
  parallel construction. Run the reversible chain `t` steps from `G0` to a hub `G*`, then draw
  each placebo `t` forward steps from `G*` independently. Under "`G0` ~ stationary law on its
  communicating class", `(G0, placebos)` are exchangeable. The swap chain here has a symmetric
  proposal (ordered pair of edge slots drawn uniformly, fair orientation coin) and accepts every
  valid move, so it is reversible with uniform stationary law on its communicating class.
  Implemented as `chain="besag_clifford"`.
* Even with exact exchangeability, the rank test addresses a **sharp randomisation null** about
  `G0`, not `H0: Delta <= eps`. A real graph drawn from an SBM is *not* uniform on its
  degree-sequence class, so rejecting this null says nothing about relation specificity unless
  the null family is scientifically admissible (scenario S3).

## 7. Search (Module B)

The objective uses development data only: `Delta_dev(Q) = E[S_val(real) - S_val(placebo~Q)]`
over development instances (population mode) or seed bundles (conditional mode). Uniform
allocation and successive halving (`ceil(log2(K/m))` rounds) operate at a fixed model-fit
budget that counts the real-graph pairing fits. The selection `J_sel` (top-`m`) is frozen
before the confirmatory instances are touched. There is **no** guarantee that `J_sel` contains
the population argmin. Misses are measured as `hit` / `regret` against Monte Carlo truths.

Because the confirmatory data are independent of the development data, Propositions 1–2 hold
for `theta_sel = min_{j in {empty} ∪ J_sel} Delta_j` **conditionally on `J_sel`**, and hence
unconditionally for the random target `theta_sel`. They do not hold for
`theta_full = min_{j in {empty} ∪ J_cand} Delta_j`.

## 8. Admissibility (Module A)

The hard constraints are verified exactly on every sample:
* node count, edge count, simplicity (no self-loops, duplicates or non-canonical edges);
* degree sequence (swap families) and in/out-degree (directed);
* per-node neighbour counts in each stratum (`strat:*`);
* stratum degree multisets and the mixing matrix (`perm:*`).

The soft rejection rules are label-free and prespecified:
* edge overlap with `G0 > 0.80` (near-identical);
* swap completion `< 0.95` (insufficient mixing);
* candidate acceptance `< 0.80` on development instances (inadmissible candidate).

Admissibility is a **declared modelling assumption**: it says which properties a
"no relation-specific information" world should preserve. The audit verifies that samples obey
the declaration. It cannot verify that the declaration is scientifically right, nor that `G0` is
exchangeable with the null.

## 9. What is *not* claimed

* No optimality of the search; no guarantee beyond enumerated, frozen comparator sets.
* No causal or semantic meaning of edges.
* No population claim from conditional (single-graph) analyses.
* Absence of a certificate is not evidence of no relational value.
