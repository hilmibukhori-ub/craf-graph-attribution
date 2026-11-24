# Phase 3D exploratory mini-pilot protocol

Status: exploratory, frozen before model fitting. This pilot cannot alter the Phase 3B or Phase 3C NO-GO decisions and cannot support a confirmatory real-world claim.

## Question

Phase 3C evaluated the four label-free properties `block`, `fsim`, `clust`, and `hop2` only through order two. The best pair remained about 0.025 below the real-graph score, versus the unchanged sufficiency margin delta = 0.005. This mini-pilot asks whether the missing order-three or order-four controls materially close that gap while retaining nontrivial perturbation.

## Frozen scope

- Dataset: CiteSeer only; its raw file and hash are unchanged from Phase 3C.
- Architecture: GCN only.
- Replication units: Phase 3C cluster identifiers 0--23, with exactly the same split and model seeds.
- New fits: only the four order-three controls and one order-four control, one null draw each. Real and empty fits produced by the generic runner are consistency checks and are not needed for the merged analysis.
- Existing order-zero through order-two observations are reused from the frozen Phase 3C pool. They are not regenerated or modified.
- Total planned new candidate fits: 24 x 5 = 120; the generic runner additionally produces 48 real/empty consistency fits.
- No other dataset, architecture, property, seed, margin, or tuning choice may be added after scores are observed.

## Label-free admissibility gate

Before model fitting, all candidates are audited using 10 fresh graph draws. A candidate must satisfy the existing hard constraints and Phase 3C overlap/diversity policy. If every new candidate fails, model fitting stops. Invalid candidate draws are never fitted.

The audit also checks the lower-order elements because `max_order=4`, but only the five prespecified higher-order elements are fitted.

## Analysis

For every element, define the paired cluster contrast

`D[r,S] = score(real,r) - score(null_S,r)`.

The primary output is descriptive: mean contrast, cluster standard error, and ordinary two-sided 95% t interval. Holm-based CRAF statuses at alpha = 0.05 are reported only as unstable exploratory diagnostics because n = 24 is not powered as a confirmatory run.

The best new higher-order element is compared with the best order-at-most-two element using paired cluster differences. The pilot is considered promising for a separately preregistered follow-up only if:

1. the best new element is admissible;
2. its point estimate is smaller than the best lower-order point estimate; and
3. its ordinary 95% interval contains the frozen delta = 0.005.

These gates are feasibility criteria, not evidence of certified sufficiency. Failure of any gate means stop this lattice-expansion direction. Delta is not changed under any outcome.

## Interpretation constraints

- Empty frontiers and rejected candidates must be reported.
- The best element may be named only after all five candidates are evaluated.
- This pilot cannot be used to select a favorable dataset because no dataset search is performed.
- No full benchmark follows automatically. Any follow-up requires review and a new frozen protocol.

