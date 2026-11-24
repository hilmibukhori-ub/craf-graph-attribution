# Phase 3D exploratory mini-pilot report

## Decision

**STOP this lattice-expansion direction; do not launch the full benchmark.**

The missing order-three controls materially reduce the CiteSeer/GCN real-vs-null gap, but the best admissible control remains well outside the frozen sufficiency margin. The Phase 3B and Phase 3C NO-GO decisions remain unchanged. Delta remains 0.005.

This is an exploratory feasibility result, not a new confirmatory evaluation.

## Frozen design and integrity

The protocol was hash-frozen before model fitting. It reused CiteSeer cluster identifiers 0--23 from Phase 3C and fitted only the prespecified order-three/four controls with GCN. Existing Phase 3C order-zero through order-two scores were reused without modification.

The regenerated real and empty scores matched Phase 3C exactly (maximum absolute difference 0 for both), confirming identical splits and model seeds. Phase 3C's freeze verified before this run.

## Label-free admissibility

| New control | Order | Acceptance | Original overlap | Pairwise overlap | Verdict |
|---|---:|---:|---:|---:|---|
| block+clust+fsim | 3 | 1.00 | 0.532 | 0.524 | admissible |
| block+clust+hop2 | 3 | 1.00 | 0.290 | 0.237 | admissible |
| block+fsim+hop2 | 3 | 1.00 | 0.582 | 0.562 | admissible |
| clust+fsim+hop2 | 3 | 0.00 | 0.601 | 0.596 | rejected |
| block+clust+fsim+hop2 | 4 | 0.00 | 0.753 | 0.746 | rejected |

The rejected candidates were logged but not fitted. In particular, the only order-four candidate is not a scientifically usable route to a non-empty frontier under the current generator.

## Experimental result

All intervals below are ordinary exploratory cluster-level 95% t intervals; they are not confirmatory simultaneous intervals.

| Control | Order | Mean gap | SE | 95% interval |
|---|---:|---:|---:|---:|
| fsim+hop2 (best prior pair) | 2 | 0.02269 | 0.00116 | [0.02029, 0.02509] |
| block+clust+fsim | 3 | 0.02140 | 0.00122 | [0.01888, 0.02392] |
| block+clust+hop2 | 3 | 0.08021 | 0.00101 | [0.07811, 0.08231] |
| **block+fsim+hop2** | **3** | **0.01399** | **0.00100** | **[0.01192, 0.01606]** |

The best order-three control improves on the best pair by 0.00869 (paired 95% interval [0.00606, 0.01132]). Thus higher-order preservation genuinely explains additional performance; the reduction is not merely point-estimate noise in this mini-pilot.

However, the frozen delta = 0.005 is outside the best candidate's interval. Across the 14 admissible evaluated lattice elements, exploratory Holm CRAF classified all 14 as advantage, none as sufficient, and produced no certified or possible minimal frontier. The result is still specificity-only.

## Frozen feasibility gates

| Gate | Result |
|---|---|
| Best new element is admissible | PASS |
| Point estimate improves over best lower-order element | PASS |
| Frozen delta lies inside best new element's ordinary 95% interval | **FAIL** |

The conjunction therefore fails. No larger run is warranted for this particular higher-order CiteSeer lattice.

## Cost and execution deviation

The six four-cluster chunks completed in parallel; the slowest took 252 seconds. Total measured fit time was 0.322 CPU-hours for 144 GCN fits plus 0.054 CPU-hours for 24 MLP fits. Summed chunk time was 0.389 hours.

The generic pool runner automatically fitted one ER control and one MLP baseline per cluster. Those 48 fits were not needed for the frozen comparison and were excluded from the scientific analysis. This is a transparent execution overhead relative to the protocol's stated higher-order and real/empty fits, not a change in the tested hypothesis. Future mini-runners should disable these automatic baselines when they are already available from a frozen parent pool.

## Scientific interpretation

The pilot narrows the diagnosis:

1. the Phase 3C empty frontier was partly caused by truncating the lattice at order two;
2. adding `block` to `fsim+hop2` recovers a substantial portion of the remaining gap;
3. nevertheless, admissible higher-order preservation does not reach the preregistered equivalence margin;
4. pushing to all four properties makes the null generator fail admissibility rather than yielding credible sufficiency.

Therefore, simply extending the same lattice is unlikely to repair the real-world novelty evidence. A future investigation should focus on better-isolated conditional perturbations or a separately selected structural task, with a new frozen exploratory/confirmatory split. It should not increase delta or scale this CiteSeer experiment merely to seek a positive frontier.

## Artifacts

- Frozen protocol: `docs/phase3d_mini_protocol.md`
- Frozen configuration: `configs/phase3d_mini.yaml`
- Freeze manifest: `outputs/phase3d_mini/FREEZE.json`
- Label-free audit: `outputs/phase3d_mini/admissibility/citeseer_elements.csv`
- Raw mini-pool and logs: `outputs/phase3d_mini/pool/`, `outputs/phase3d_mini/logs/`
- Numeric summary: `outputs/phase3d_mini/analysis/summary.csv`
- Machine-readable decision: `outputs/phase3d_mini/analysis/decision.json`

