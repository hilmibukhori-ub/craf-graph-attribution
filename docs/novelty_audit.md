# Novelty audit — RUSA vs PCGA/PCGA-L and related methods

Status: Phase 2A audit (2026-11-24). This is a targeted primary-source check, **not** a
systematic review. Each source is marked:
* **[V]** bibliographic details confirmed online on 2026-11-24;
* **[V-abs]** abstract or secondary description checked, full text not read;
* **[U]** cited from background knowledge, not verified in this audit.

Nothing below assigns novelty to an established statistical tool.

## 1. Component-by-component comparison

| Component | Where it already exists | RUSA status |
|---|---|---|
| Matched no-graph control, retrained | PCGA (this group, `METHOD_PROPOSAL_PCGA.md`); graph-necessity studies, e.g. Bechler-Speicher et al. ICML 2024 [V-abs, via PCGA audit] | **existing** |
| Retrained placebo graphs (node permutation within strata) | PCGA; QAP / network permutation tests (Krackhardt 1988) [U] | **existing** |
| Structural ladder ER → degree → block → real | PCGA-L (this group) | **existing** |
| Degree-preserving double-edge swaps | Maslov & Sneppen 2002 [U, cited in the PCGA paper]; configuration-model space choice: Fosdick, Larremore, Nishimura & Ugander, *SIAM Review* 60(2):315–355, 2018 [V] | **existing** |
| Degree/ER rewiring as a control in GNN studies | e.g. "On the impact of communities on semi-supervised classification using GNNs", arXiv:2010.16245 [V-abs]; a diagnostic protocol for GNNs in load forecasting with degree-preserving swap controls, arXiv:2610.35074 [V-abs] | **existing** (adjacent prior art; must be cited) |
| Stratum-preserving swaps (per-node neighbour counts by attribute) | generalisation of PCGA-L L3 (block → arbitrary attribute subsets); joint-degree / dK-series null models in network science [U] | **existing idea**; the attribute-subset *enumeration* is an engineering choice |
| Intersection–union test, `max p` | Berger, *Technometrics* 24(4):295–300, 1982 [V]; Gleser 1973 [U] | **existing** |
| `min_j L_j` robust lower bound | direct corollary of the IUT | **existing** |
| Nested radius by fixed-sequence logic | closed testing / fixed-sequence (Marcus, Peritz & Gabriel 1976) [U] | **existing** |
| Exact MCMC rank tests via parallel construction | Besag & Clifford, *Biometrika* 76:633–642, 1989 [V-abs, secondary] | **existing**; using it to correct the PCGA-L L3 exactness claim is a *correction*, not a contribution |
| Empirical-Bernstein bounds | Maurer & Pontil, COLT 2009 (arXiv:0907.3740) [V] | **existing** |
| Betting confidence bounds | Waudby-Smith & Ramdas, *JRSSB* 86(1), 2024 (arXiv:2010.09686) [V] | **existing** |
| Successive halving / best-arm identification at fixed budget | Karnin, Koren & Somekh, ICML 2013, PMLR 28:1238–1246 [V]; Jamieson & Talwalkar, AISTATS 2016 [U] | **existing** |
| Data splitting: select on one part, infer on the other | Cox, *Biometrika* 62:441–444, 1975 [V-abs, secondary]; selective inference, Fithian, Sun & Taylor, arXiv:1410.2597 [V-abs] (data-splitting tests often inadmissible) | **existing**; RUSA's dev/confirm split *is* data splitting |
| Robustness across a family of defensible analysis choices + joint test | multiverse analysis, Steegen et al. 2016 *Perspect. Psychol. Sci.* 11:702–712 [V-abs]; specification curve, Simonsohn, Simmons & Nelson 2020 *Nat. Hum. Behav.* 4:1208–1214 [V] | **existing concept**: RUSA is a specification-robustness analysis whose "specifications" are graph nulls |
| Worst case over an ambiguity set | distributionally robust optimisation (e.g. Ben-Tal et al.; Duchi & Namkoong) [U] | **existing concept** |
| Searching for the *hardest* admissible null at a fixed fit budget, on dev data, then freezing | not found in this targeted check | **candidate contribution** (see §2) |

## 2. What could be new, stated narrowly

The only element not found in the targeted check is the **combination**:

> a declared, auditable family of graph nulls (with exact constraint verification), a
> development-data-only budgeted search for the most competitive admissible null, and a frozen
> confirmatory IUT certificate whose scope is explicit.

Each ingredient is standard. Under the spec's own criterion (§0.10), the combination is a
contribution only if it gives an **independent algorithmic or empirical advantage** over
(a) PCGA-L plus a standard IUT and (b) a fixed multi-null IUT over the same candidates at
equal compute. That is an empirical question, addressed by the Phase 2A pilot and decided in
`phase2a_report.md`.

Some *a priori* reasons to doubt the novelty claim follow; they are recorded before the
results were seen:
1. The dev/confirm two-stage design is ordinary data splitting. With a uniform screen it is
   "screen then confirm", which needs no new theory.
2. Successive halving is an off-the-shelf bandit routine. Any advantage over a uniform screen
   is a property of SH, not of RUSA.
3. The confirmatory certificate covers only the selected nulls. A fixed IUT over all
   candidates covers the whole enumerated set, i.e. it answers a *stronger* question. RUSA's
   efficiency gain (if any) is bought with a weaker guarantee whose gap equals the search
   miss rate.

## 3. Gaps not closed by this audit

* No systematic search (databases, snowballing) was run for "hardest null" / "adversarial
  placebo" / "least-favourable null" in graph ML or network science. The PCGA systematic search
  covered stock-GNN relation claims only.
* Primary texts of Besag & Clifford (1989), Cox (1975) and Gleser (1973) were not read in full.
* The adjacent arXiv preprints found here (2010.16245, 2610.35074) were seen only at abstract
  level. They must be read before any manuscript claim.
* Exponential random graph / maximum-entropy null models with attribute constraints (e.g.
  dK-series, stochastic block configuration models) likely already cover the "stratified swap"
  family conceptually. Not verified.

**Gate D status:** passes only for the narrow combination claim, and only if Gate C shows an
empirical advantage. Otherwise RUSA should be presented as a benchmark / PCGA extension
without a method-novelty claim.

## Sources consulted online (2026-11-24)
- Besag & Clifford 1989, secondary descriptions: https://arxiv.org/pdf/2204.13581 , https://arxiv.org/abs/2310.04924
- Berger 1982: https://portal.mardi4nfdi.de/wiki/Item:Q3962385 , https://arxiv.org/pdf/2202.12540
- Waudby-Smith & Ramdas 2024: https://arxiv.org/abs/2010.09686
- Fosdick et al. 2018: https://arxiv.org/abs/1608.00607
- Karnin, Koren & Somekh 2013: https://proceedings.mlr.press/v28/karnin13.html
- Maurer & Pontil 2009: https://arxiv.org/abs/0907.3740
- Fithian, Sun & Taylor: https://arxiv.org/abs/1410.2597 ; Cox 1975 via https://arxiv.org/pdf/2102.02159
- Simonsohn, Simmons & Nelson 2020: https://doi.org/10.1038/s41562-020-0912-z
- Adjacent GNN controls: https://arxiv.org/pdf/2010.16245 , https://arxiv.org/pdf/2610.35074

---

# Phase 2B update (2026-11-24): targeted review of the closest prior work

Labels as above. **[V-full]** means the full text was read (via fetch), with the stated limits.

## A. Graph rewiring / null-graph controls for GNNs (closest applied prior art)

| Work | Controls | Retrained? | Inference | Multiple nulls / selection | Relation to RUSA |
|---|---|---|---|---|---|
| Hussain, Duricic, Lex, Kern & Helic, "On the impact of communities on semi-supervised classification using GNNs", Complex Networks IX, 2020 (arXiv:2010.16245) [V-full] | SBM rebuilt from communities; configuration model ("each node keeps its degree"); Erdős–Rényi; feature-only logistic regression | yes (10 graphs × 50 splits × 10 inits) | Mann–Whitney U, Bonferroni, GNN vs feature baseline; no test on the ablations was seen | three fixed null families; **no search or selection** | a fixed multi-null ladder very close to PCGA-L's L1/L2/L3 idea; predates PCGA-L |
| Campagne et al., "A diagnostic protocol for GNNs in electricity load forecasting: separating parameter sharing from neighborhood access", arXiv:2610.35074 (Oct 2026) [V-abs + partial full text] | empty graph, identity graph, **degree-preserving rewiring** ("tests whether neighbor identity matters"), per-node / shared MLPs | yes, under common training rules (from summary) | bootstrap percentile intervals and permutation z-scores (summary); benchmark ranks "without testing for significance" | fixed menu; graph chosen on validation | **the closest contemporaneous work**: the same separation of "neighbourhood access" vs "neighbour identity" as PCGA's utility/specificity axes. No admissible-family search, no IUT certificate |
| Bechler-Speicher et al., "Graph neural networks use graphs when they shouldn't", ICML 2024 [V-abs] | regular graphs / overfitting to structure (abstract only) | n/a from abstract | n/a | n/a | motivates graph-utility controls; the full PDF still needs reading |
| Platonov et al., "A critical look at the evaluation of GNNs under heterophily", ICLR 2023 (arXiv:2302.11640) [V-abs] | dataset duplicates, baselines, adjusted homophily | — | — | — | evaluation-critique context; no null-graph certification |
| Orsini et al., "Quantifying randomness in real networks", *Nat. Commun.* 6:8627, 2015 [V-abs] | dk-series: a nested sequence of null ensembles preserving progressively more structure | — | descriptive | **nested null hierarchy**; argues that degree-only nulls are arbitrary | the conceptual ancestor of PCGA-L's ladder and of RUSA's "admissible family"; RUSA's stratified nulls are attribute-conditioned dk-like ensembles |
| Fosdick et al., *SIAM Rev.* 2018 [V] | configuration-model space choices | — | — | — | the null-space specification matters (supports "admissibility is declared") |

**Conclusion A.** Retrained rewiring controls, a fixed multi-null ladder, and nested null
hierarchies all exist. No work found here **searches** an admissible null family, or gives a
**full-set inferential certificate** over a family of graph nulls at a fixed compute budget.
This was a targeted, not systematic, search.

## B. Adaptive screening / selection

| Work | Relevance |
|---|---|
| Karnin, Koren & Somekh, ICML 2013 [V]; Jamieson & Talwalkar, AISTATS 2016 [U] | sequential halving / best-arm identification at fixed budget (RUSA `screen_sh`) |
| Li, Jamieson, DeSalvo, Rostamizadeh & Talwalkar, "Hyperband", *JMLR* 18(185), 2018 [V] | random search + adaptive resource allocation + early stopping; the standard ML baseline for "search at a budget" |
| Sampson & Sill, "Drop-the-losers design: normal case", *Biometrical J.* 47(3):257–268, 2005 [V-abs, secondary] | two-stage select-then-test with data combined across stages; the clinical-trial analogue of screen-then-confirm |
| Bretz, Schmidli, König, Racine & Maurer, "Confirmatory seamless phase II/III clinical trials with hypotheses selection at interim", *Biometrical J.* 48, 2006 [V-abs; page numbers inconsistent across sources] | closed testing + combination tests after interim selection; **the established way** to select at interim and still control error |
| Bauer & Köhne, *Biometrics* 1994 [V-abs, secondary]; Lehmacher & Wassmer 1999 [V-abs, secondary]; Bauer et al., "Twenty-five years of confirmatory adaptive designs", 2016 (PMC6680191) [V-abs] | combination tests valid under data-dependent stage-2 sample sizes; **RUSA `fullset_adaptive` is a direct application** |
| Cox 1975; Fithian, Sun & Taylor (arXiv:1410.2597) [V-abs] | data splitting / selective inference; `screen_*` are data-splitting procedures |

**Conclusion B.** Every Phase 2B screening or allocation mechanism is an instance of established
methodology:
* SH and random search come from bandits / HPO;
* screen-then-confirm is drop-the-losers / data splitting;
* full-set adaptive allocation is an adaptive-design combination test;
* the minimax-power allocation is the classical optimal allocation for a minimum of means.

The only possibly new element is applying these to *graph-null families* with an explicit
selected-set vs full-set scope.

## C. Robust inference across multiple nulls / specifications

| Work | Relevance |
|---|---|
| Berger 1982 IUT [V] | the global "beats every comparator" test |
| Benjamini & Heller, "Screening for partial conjunction hypotheses", *Biometrics* 64(4):1215–1222, 2008 [V] | generalises "all nulls false" to "at least u of n false". A partial-conjunction RUSA ("beats at least u of K admissible nulls") is a natural, already-solved generalisation |
| Simonsohn, Simmons & Nelson 2020 [V]; Steegen et al. 2016 [V-abs] | specification-curve / multiverse robustness with joint tests; RUSA is a specification-robustness analysis over graph nulls |

## D. Phase 2B novelty verdict

The verdict is filled in from results in `phase2b_report.md` §7. Before results, the maximum
defensible claim is:

> An audited protocol that (i) declares an admissible family of graph nulls, (ii) uses established
> screening / adaptive-allocation designs to concentrate retraining budget, and (iii) reports
> certificates with explicit scope (selected-set vs full-set).

It makes **no** claim to a new statistical test, a new search algorithm or a new allocation theory.

### D (filled in after Phase 2B results; see phase2b_report.md §8–9)

* **Hardest-null search (successive halving): no demonstrated value** over uniform or random
  screening at equal budget.
  * Claim rates: no positive difference in any cell.
  * Discovery: +0.067 in one scenario only.
  * No novelty claim.
* **Full-set adaptive certification:** valid (0 type-I in N6) and more powerful than exhaustive
  multi-null IUT at b ≥ 12, by +0.15 to +0.27 (eps = 0.005) and up to +0.30 (eps = 0). It is a
  direct application of adaptive-design combination tests and classical optimal allocation, so it
  carries **no methodological novelty claim**; the claim is limited to its use and evaluation for
  graph-null certification.
* **Gate D verdict:** the only defensible novelty is a *protocol / empirical* contribution:
  * an audited admissible-null protocol extending PCGA-L;
  * explicit selected-set vs full-set certificate scope;
  * the demonstration that fixed null menus (PCGA-L) certify non-existent robust effects (100% of
    N6 experiments).

## E. Phase 2C — final novelty audit and contribution statement

The evidence is in `docs/phase2c_report.md`.

**Correction to D (Phase 2B wording).** The last bullet of D says that PCGA-L "certifies
non-existent robust effects". That phrasing is wrong and is withdrawn. PCGA-L tests the edge step
against `strat:block`. In both N6 and S7 that contrast is truly positive (0.026–0.04), so PCGA-L's
claims are **correct for its own hypothesis**: Phase 2C false-vs-own-target rate = 0 in every
cell. The accurate statement is narrower. PCGA-L does not test, and was not designed to test,
robustness against the whole admissible null family. Its edge-step claim therefore must not be
read as a full-set claim.

| Element | Status after 2C | Novelty claim |
|---|---|---|
| Successive halving / hardest-null search | removed from the framework. It gains discovery in hard K48 cells (+0.15 to +0.21) but no full-set power | none |
| `fullset_adaptive` (interim efficacy + minimax-power allocation + inverse-normal combination) | kept as an optional execution mode (`_fb` variant). It is valid in every audit, and +0.08 to +0.52 more powerful than exhaustive at b ≥ 12 (SGC), +0.15 to +0.42 (SAGE) | none. It applies Bauer & Köhne 1994, Lehmacher & Wassmer 1999 and Brannath et al. 2002 |
| A-priori feasibility fallback | kept | none (a trivial design rule) |
| Exhaustive IUT certificate over the declared family | kept; the primary claim | none (Berger 1982) |
| Admissibility audit and declared null family | kept | protocol-level |
| Selected-set vs full-set scoping, with the empirical demonstration (S7: screens up to 0.21–0.24 full-set false claims vs 0 for full-set procedures) | kept, mandatory | protocol-level / empirical |

**Contribution statement.** RUSA is an audited relational attribution and evaluation protocol
that extends PCGA-L. It certifies, at a prespecified margin and for a stated model, that the
observed edge assignment improves prediction over **every** member of a declared,
admissibility-audited family of graph nulls. It reports each claim with its scope: full-set,
selected-set, or PCGA-L edge step. Its statistical machinery is standard, and it is attributed as
such. The contribution is:
1. the protocol (declaration, audit, scope and compute accounting);
2. its validation under matched compute on synthetic worlds with known isolated binding nulls,
   including the demonstration that screen-then-confirm certificates do not transfer to the full
   family.

No algorithmic or statistical novelty is claimed.

## F. Phase 3A — CRAF (Certified Relational Attribution Frontier)

The evidence is in `docs/phase3a_report.md`. References were verified by search; [V] = bibliographic record and
abstract checked, not the full text.

| Area | Reference | Relation to CRAF | Novelty consequence |
|---|---|---|---|
| Own prior work | PCGA / PCGA-L | ordered ladder (a chain in the lattice); order-dependent step attribution; no sufficiency certificate | CRAF generalises the chain to a lattice |
| Null-model hierarchies | Orsini et al. 2015, Nat. Commun. 6:8627 [V]; dk-series (Mahadevan et al. 2006) | nested constraint hierarchy; finds the d needed to reproduce *structural* properties | closest precedent for "minimal sufficient constraints". CRAF differs by being a lattice with a performance estimand and a statistical certificate |
| Null-model choice | Fosdick et al. 2018, SIAM Rev. 60:315 [V] | which configuration space to use | background only |
| Factorial / generator-based studies | Palowitch et al. 2022, GraphWorld (KDD) [V] | property–performance relations across generated worlds; descriptive | none |
| Minimal sufficient explanations | Shih, Choi & Darwiche 2018 (IJCAI; prime implicants) [V]; Carter et al. 2019 (AISTATS; sufficient input subsets) [V] | minimal sufficient subsets for decisions; deterministic, instance-wise | the *concept* of minimal sufficient subsets is not new |
| Multiple testing | Holm 1979; closed testing; Logan & Tamhane 2008 (superiority/non-inferiority as closed testing) [V-secondary] | Holm-adjusted non-inferiority = CRAF's sufficiency half | standard |
| Directional / set inference | Finner & Strassburger 2002, Ann. Stat. 30:1194 (partitioning principle) [V]; Hsu 1996 (MCB); Mogstad, Romano, Shaikh & Wilhelm 2024, REStud 91:476 (confidence sets for ranks) [V] | simultaneous inference on set-valued functions of parameters | **the frontier sandwich is an instance of this standard logic; no novelty claim** |
| Adaptive designs | Bauer & Köhne 1994; Lehmacher & Wassmer 1999; Brannath et al. 2002 [V] | combination test for adaptive allocation | standard |

**Phase 3A contribution statement.** CRAF defines graph-relational attribution as the frontier of
minimal δ-sufficient combinations of declared graph-null constraints. The definition is
order-independent and makes no monotonicity assumption. CRAF reports this frontier with a
simultaneous (1 − alpha) sandwich `cert_min ⊆ F ⊆ possible_min` built from standard
Holm-controlled directional certification, together with gap sets that quantify unresolved
minimality.

Empirically, the usual reporting rules give wrong frontier members at substantial rates while
CRAF does not:
* minimal-among-certified after non-inferiority testing: 0.19–0.38;
* children-only minimality under non-monotonicity: up to 0.88;
* point estimates: up to 0.99 at the margin.

No novelty is claimed for the tests, Holm, the combination test, the lattice, or the sandwich
logic. The contribution is the estimand, the certified reporting framework, and its validation
for graph pipelines.

## G. Phase 3B — real-world pilot (Cora): updated audit

Web-verified on 2026-11-24 [V].

| Closest real-data practice | What it does | Relation to CRAF on real graphs |
|---|---|---|
| Random-split, multi-seed GNN evaluation (Shchur et al. 2018, arXiv:1811.05868) [V] | resamples splits and initialisations, because single splits reshuffle model rankings | CRAF's replicate cluster (fresh split + seed + null draws) uses the same protocol. **Standard; no novelty** |
| Homophily / label-informativeness diagnostics (Ma et al. 2022, ICLR, arXiv:2106.06134 [V]; Platonov et al. 2023, NeurIPS, arXiv:2209.06177 [V]) | scalar dataset statistics that predict or explain when GNNs help | descriptive and label-based. CRAF asks a different question: whether label-free structural properties, *preserved jointly by a null*, reproduce the trained model's performance, with simultaneous certification |
| "GNNs use graphs when they shouldn't" (Bechler-Speicher et al. 2024, ICML, arXiv:2309.04332) [V] | shows that GNNs overfit graph structure; graph-editing remedies | compatible: CRAF can certify that some graph properties are insufficient or sufficient for a model, but it does not explain *why* |
| Rewired / randomised-graph controls (§A above) | single null, or an ordered ladder (PCGA-L) | CRAF replaces the single null or ladder with a lattice, and reports a certified frontier |

**Verdict after the pilot.** The real-world pilot adds no new methodological component, and none is
claimed. The question for Phase 3B is whether the formulation-level contribution of §F produces
**scientifically meaningful statements on real data** that the standard approaches do not give.
That is answered empirically in `docs/phase3b_report.md` §§4–6 (decision rule R3), not by
argument. **Result (Cora):** only category (d). CRAF certified specificity over the whole lattice
(a broader certified negative than PCGA-L's single edge step), but it found no frontier member and
no non-monotonicity. So on real data the distinctive frontier statements are not yet demonstrated. The label-free attribute construction (Louvain communities, feature clusters, degree
and length bins) is standard and is not claimed as a contribution.

Sources:
* https://arxiv.org/abs/1811.05868
* https://arxiv.org/abs/2106.06134
* https://arxiv.org/abs/2209.06177
* https://proceedings.mlr.press/v235/bechler-speicher24a.html

## H. Phase 3C — targeted structural validation: updated audit

Web-verified on 2026-11-24. Phase 3C does not expand the methodological novelty claim.

| Phase 3C component | Closest prior work | Consequence |
|---|---|---|
| feature-assortativity / A-X strata | Lee et al., ICML 2024, explicitly measure and randomize dependence between topology and node features | established scientific target; the `fsim` discretization is an implementation choice, not novelty |
| local clustering and multi-hop neighbourhood strata | localized topological-feature work encodes triangles, clustering coefficients, shortest paths, and j-hop neighbourhoods; subgraph-GNN literature likewise uses k-hop ego structure | established graph descriptors; no novelty |
| community plus feature-similarity rewiring | Rubio-Madrigal, Jamadandi & Burkholz, ICLR 2025 / PMLR 2026 study community- and feature-guided rewiring | reinforces that these are scientifically motivated controls, not a new idea |
| heterophilous candidate datasets | Platonov et al. 2023 introduce Roman-empire, Amazon-ratings, Minesweeper, Tolokers, and Questions and document duplicate-node leakage in Chameleon/Squirrel | dataset choice and exclusions follow prior audit; no novelty |
| block-aware calibration replication | standard independent replication and cluster/block bootstrap | diagnostic protocol only; no statistical novelty |

The only contribution still under evaluation is the Phase 3A formulation: whether a declared
property lattice plus simultaneous frontier sandwich gives an informative real-world statement
beyond a fixed PCGA-L chain and ordinary Holm non-inferiority. A non-empty frontier would be
evidence for usefulness, not evidence that feature, clustering, multi-hop descriptors, Holm, or
the bootstrap are new. An empty frontier is retained as a negative result.

Additional sources:

* https://proceedings.mlr.press/v235/lee24m.html
* https://jmlr.org/papers/volume26/23-1424/23-1424.pdf
* https://proceedings.mlr.press/v325/rubio-madrigal26a.html
* https://arxiv.org/abs/2302.11640

## I. Phase 3D mini-pilot — higher-order lattice check

The exploratory CiteSeer/GCN mini-pilot adds no methodological novelty. Higher-order
intersections of standard label-free constraints are a direct extension of the already declared
lattice.

The result refines, but does not reverse, the real-world evidence audit. Preserving
`block+fsim+hop2` reduced the estimated real-vs-null gap from 0.02269 for the best pair to
0.01399 (paired reduction 0.00869, ordinary 95% interval [0.00606, 0.01132]). However, the
best candidate's interval [0.01192, 0.01606] remained above the frozen delta = 0.005. The only
order-four candidate failed the label-free admissibility audit. Thus the experiment remains
specificity-only: it provides evidence that the order-two truncation omitted meaningful joint
structure, but it still does not demonstrate an informative certified or possible minimal
frontier beyond standard Holm testing or PCGA-L.

Consequently, the safe novelty statement remains unchanged: CRAF contributes the frontier
estimand and certified reporting formulation, with strong synthetic validation, while its
distinctive frontier usefulness on real-world graphs has not yet been demonstrated.
