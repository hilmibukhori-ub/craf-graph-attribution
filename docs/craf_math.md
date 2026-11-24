# CRAF — Certified Relational Attribution Frontier: formulation, guarantees, algorithm

This builds on `rusa_mathematical_spec.md` and uses its notation. Implementation:
`src/rusa/craf/core.py` and `src/rusa/craf/experiment.py`. Tests: `tests/test_craf.py`.

**Nothing here is a new statistical test.** The ingredients are standard:
* one-sided t-tests;
* the inverse-normal combination test;
* Holm's step-down procedure;
* simultaneous-confidence reasoning about sets, which is standard in set identification and in
  multiple comparisons with the best.

What is formulated here is an *estimand* (minimal δ-sufficient combinations of graph-null
constraints) and a *frontier statement* with a simultaneous guarantee that does not assume
monotonicity.

## 1. Property-subset lattice

`M` is the declared set of stratification attributes (metadata). For `S ⊆ M`:
* `N_S` is the degree-preserving swap null that preserves every node's neighbour counts in each
  joint stratum of `S`. `N_∅` is the degree null.
* `L ⊆ 2^M` is the declared, admissibility-audited lattice. Here it is all subsets of order ≤ 2.

If `S ⊂ T`, the **constraints** are nested: every statistic preserved by `N_S` is preserved by
`N_T`. This holds because joint-stratum counts for `T` determine those for `S`.

**The performance of `N_S` is not assumed monotone in `S`.** It is not implied by nesting:
* `mu(N_T)` averages over a smaller set of graphs than `mu(N_S)`;
* that subset can perform worse than the larger set, for example if the extra preserved
  statistics are harmful to the model and the real graph's benefit comes from edge-specific
  structure that no null preserves.

No result below uses monotonicity. Minimality is always checked against **all** proper subsets in
`L`, not only immediate children.

## 2. Estimands

Margin `delta > 0` is fixed in advance (here `delta = eps = 0.005`).

| Estimand | Definition | Reading |
|---|---|---|
| relational advantage over S | `Delta_S = mu(G0) − mu(N_S)` | what G0's edges give beyond preserving S |
| meaningful advantage | `Delta_S > delta` | S is *insufficient* |
| structural sufficiency | `Delta_S < delta` | preserving S alone reproduces G0's performance up to delta |
| sufficient family | `Suff = {S in L : Delta_S < delta}` | |
| **frontier** (minimal sufficient combinations) | `F = {S in Suff : no T ⊊ S, T in L, is in Suff}` | the order-independent answer to "which property combinations suffice?" |
| relational specificity over L | `Suff = ∅`, i.e. `min_S Delta_S ≥ delta` | no admissible combination suffices; the specific edges matter (RUSA's full-set claim restricted to L) |

* `F` can contain several elements (several routes to sufficiency), of different sizes.
* `F` is empty iff no element is sufficient.
* When `Delta_S = delta` exactly, `S` is neither sufficient nor meaningfully advantaged. Both
  directional claims are then false, and the error accounting treats them so.

PCGA-L corresponds to one chain `∅ ⊂ {block}` inside `L` (plus ER and empty below the lattice).
Its step attributions depend on the order of that chain. `F` does not depend on any order.

## 3. Simultaneous three-way certification

For each `S` there are two one-sided hypotheses:
* `H^adv_S: Delta_S <= delta`; rejecting it certifies **advantage** (insufficiency).
* `H^suf_S: Delta_S >= delta`; rejecting it certifies **sufficiency**.

Their p-values come from one-sided t-tests on i.i.d. replicate contrasts, so
`p^adv_S + p^suf_S = 1`. All `2|L|` hypotheses go through **Holm's step-down at level alpha**.
`A` is the set of certified-advantage elements and `C` the set of certified-sufficient elements.
Every other element is **inconclusive**. Since `p^adv + p^suf = 1`, `A ∩ C = ∅` whenever
`alpha <= 1/2`.

**Proposition C1 (FWER; Holm 1979).** If each p-value is valid for its hypothesis, then
`P(E^c) <= alpha`. Here `E` is the event that there is no false certification:
`A ⊆ {Delta > delta}` and `C ⊆ {Delta < delta}`. This holds under arbitrary dependence between
the tests; the elements share replicates and the real-graph fit.

**Proposition C2 (frontier sandwich).** Define
* `cert_min = {S in C : every T ⊊ S in L is in A}`;
* `possible_min = {S not in A : no T ⊊ S in L is in C}`.

On `E`:
* (i) `cert_min ⊆ F ⊆ possible_min`;
* (ii) every `S in C` contains some `T in F`, and every such `T` lies in `possible_min`.

Hence `P(cert_min ⊆ F ⊆ possible_min) >= 1 − alpha`, **without any monotonicity assumption**.

*Proof.*
* (i, left) Take `S in cert_min`. On `E`, `S in C ⊆ Suff`. Every proper subset `T` is in
  `A ⊆ {Delta > delta}`, so `T ∉ Suff`. Hence `S` is minimal in `Suff`.
* (i, right) Take `S in F`. Then `Delta_S < delta`, so `S ∉ A` on `E`. Every proper subset `T`
  has `T ∉ Suff`, so `T ∉ C ⊆ Suff`. Hence `S in possible_min`.
* (ii) `S in C ⊆ Suff`, and the finite set `Suff ∩ ↓S` has minimal elements. Such a minimal
  element is in `F`, and by (i) it is in `possible_min`. ∎

**Proposition C3 (two weaker reports carry no minimality guarantee).**
* (a) **Minimal among certified sufficient**, `min_among_cert = min_⊆ C`, satisfies
  `min_among_cert ⊆ F` only if every non-certified subset is truly insufficient. Counterexample:
  `T ⊊ S` with `Delta_T = delta − tau` (sufficient but hard to certify) and `Delta_S = 0`.
  * `S` is certified sufficient with probability → 1.
  * `T` is certified sufficient with probability ≈ alpha-level when `tau` is small.
  * So `S` is reported "minimal among certified" with probability → 1, yet `S ∉ F`.

  Standard multiplicity-adjusted non-inferiority testing (`ni_holm`) reports exactly this set.
* (b) **Immediate-children minimality** (`craf_children`) declares `S` minimal when its
  `|S| − 1` subsets are certified insufficient. Under non-monotonicity this is wrong even when
  every certification is correct. Example: `Delta_∅ = 0`, `Delta_{a} = Delta_{b} = 0.02`,
  `Delta_{a,b} = 0`; then `{a,b}` is reported minimal but `F = {∅}`
  (`tests/test_craf.py::test_non_monotone_children_rule_fails_full_rule_does_not`).

**Uncertainty quantification.** When minimality cannot be certified, CRAF reports:
* `possible_min \ cert_min`: the frontier elements not ruled out (a 1−alpha confidence superset
  of the uncertain part of `F`);
* for every `S in min_among_cert \ cert_min`, its **gap set**: the proper subsets of `S` that
  are inconclusive. The true frontier element below `S` is either `S` itself or lies among
  those subsets (C2(ii));
* the number of inconclusive elements.

**Proposition C4 (order independence).** The decisions are equivariant under:
* any permutation of the enumeration order of `L` and of the hypotheses (Holm depends only on
  the multiset of p-values; ties do not change the rejection set);
* any relabelling of attributes (the frontier sets are defined by set inclusion).

The PCGA-L ladder, by contrast, attributes gains to steps in a fixed order
(`tests/test_craf.py::test_order_independence_under_relabelling`).

## 4. Adaptive allocation (optional; validity unaffected)

**Stage 1.** Every element gets `R1 = round(b/3)` replicates.

**Stage 2.** Element `S` gets `n_S(X1) >= n_min` replicates, chosen by:
* **minimax power** for the direction suggested by stage 1: margin `|mean_S − delta|` with the
  conservative plug-in of Phase 2B §2.4, at level `alpha/(2|L|)`, the first Holm threshold;
* **relevance screening**: if some proper subset `T` looks clearly sufficient at stage 1
  (`mean_T + 2 se_T < delta`), then `S` cannot be a frontier member and gets only `n_min`.

**Test.** Each directional p-value is the inverse-normal combination of the stage-wise one-sided
t p-values, with `w1 = sqrt(1/3)` fixed. Holm is applied to the `2|L|` combined p-values.

**Proposition C5.** Under conditions C1–C4 of `rusa_mathematical_spec.md` §5.1, each combined
p-value is valid for any data-dependent `n_S(X1)`. Holm then controls the FWER at alpha, and C2
holds.

**Feasibility.** If `R1(1+|L|) + n_min(|L|+1) > B`, the procedure is exactly uniform CRAF. The
decision depends only on `(b, |L|, n_min)`.

## 5. Algorithm

```
CRAF(L, data source, b, delta, alpha, mode)
  B = b (1 + |L|)
  if mode == uniform or not feasible(b, |L|, n_min):
      for S in L: D_S = contrasts on replicates 1..b;   p_S = one-sided-t(D_S, delta)  (both directions)
  else:  # adaptive
      for S in L: D1_S = contrasts on replicates 1..R1
      dominated = {S : exists T ⊊ S with mean(D1_T) + 2 se(D1_T) < delta}
      n = minimax_power_allocation({|mean(D1_S) - delta|}, budget B - R1(1+|L|), n_min, level alpha/(2|L|));
          dominated elements get n_min
      for S in L: D2_S = contrasts on fresh replicates R1+1..R1+n_S
                  p_S = inverse_normal(p_t(D1_S), p_t(D2_S); w1)   (both directions)
  A, C = Holm({p^adv_S, p^suf_S : S in L}, alpha)
  cert_min     = {S in C : all T ⊊ S in L are in A}
  possible_min = {S ∉ A : no T ⊊ S in L is in C}
  gaps(S)      = {T ⊊ S : T ∉ A}   for S in min_⊆(C) \ cert_min
  specificity  = (A == L)
  return A, C, inconclusive = L \ (A ∪ C), cert_min, possible_min, gaps, specificity
```

Cost: `|L|` lattice nulls plus the real graph per replicate. `|L| = sum_{k<=r} C(|M|, k)`, which
grows quickly. The method is intended for small declared `M` (≤ 6–8 attributes) and orders
`r <= 2–3`.
