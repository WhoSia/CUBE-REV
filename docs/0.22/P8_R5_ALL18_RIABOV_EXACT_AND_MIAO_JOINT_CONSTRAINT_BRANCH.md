# CUBE-REV 0.22 P8-R5 — Exact All-18-HTM Closure of Riabov Alternatives & Same-EO Coupled-Constraint Falsification

**Formal stage:** CUBE-REV 0.22 P8-R5. Retain P8 formal title and all prior P6/P7/P8-R2/R3/R4 historical verdicts. Do not promote 0.23.

**Verdict (2026-10-11 KST):** Source-conditioned Riabov Other #1 and #3 full-18 HTM post-DR completion minima are **EXACTLY 13 and 13**, not [12,13]. The five P7 DR-valid authored source paths thus have exact 18-HTM continuation costs **9, 9, 12, 13, 13**, with Miao same-EO literal-prefix-preserving all-18-HTM solution costs **19 vs 23**. Further independent physical projection test identifies an actual reversal between two independent projected search lower bounds and whole-cube shortest completion order. Scientific grade: exact finite physical search + source-typed branch observations PASS; uniquely identified human decision mechanism HOLD.

## 1. Source and authority

Source records:
- [Qijun Miao, FMC World 2026 attempt 1 authored reconstruction](https://333.fm/wca/reconstruction/FMCWorld2026/2014MIAO02), lines 29–53. The author gives common four-turn EO `L2 F' L D`, a six-turn main DR extension, and an explicitly labeled alternative extension *from the EO* in line 45. This is documented retrospective evidence of an authored alternative; not a continuous chronological record of all considered candidates or their full-continuation costs. The author's surrounding comments about 4-move EO coverage and practical search strategy are retrospective self-report.
- [Yurii Riabov, FMC World 2026 attempt 1 authored reconstruction](https://333.fm/wca/reconstruction/FMCWorld2026/2018RIAB01), lines 29–56. The public text reports approximate EO search count and discovery timing and lists three other DR-like fragments. Other #1 and Other #3 are physically reconstructed **only under the declared contiguous normal-side grammar assumption**. Other #2 remains context/notation HOLD; no claim of author error.

Authentic frozen P7 source ledger: `data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json`. Independent R3 full-54-sticker physically solved conditional upper-bound fixture: `data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json`. P8-R4 complete 29,400-coset exact HTR contact certificate is prior mathematical authority, not substituted for exact solved distance.

## 2. Exact all-18-HTM Riabov completion decision: 12 versus 13

For each genuine source-conditional Riabov Other #1 and Other #3 DR endpoint, reconstruct the original 3×3 physical cube after the author's two source lines, keep the source-grade assumption attached, then permit **all 18 original legal outer-face HTM moves**, with no DR preservation or compulsory HTR contact.

Let B5(e) be all states within five legal outer-face turns from solved and B5(s) all states within five turns from the source endpoint. Both spheres have exactly **619,649** full cubie states including levels 0–5; the exact depth-5 layer contains **574,908** states. These are full corner+edge positions and orientations, not a projection.

- 0–10 turns: test direct B5(e) and B5(s) state intersection.
- 11 turns: test all 18 legal one-edge extensions of exact goal-depth-5 states for membership in B5(s): **10,348,344** tests per source.
- 12 turns: test all **18×18** legal ordered two-edge extensions from each exact goal-depth-5 state against B5(s), without allocating huge depth-6 physical-state maps. Both source candidates required exhaustive enumeration of **574,908×324 = 186,270,192** two-edge probes. Zero joins for either candidate. Previous 0–11 tests are independently repeated in this same program.

Any path of length <=12 can be split at depths <=5 from both ends with at most two middle legal moves; all are exhaustively represented by these tests. Hence no physical complete word of length <=12 exists for either endpoint. Independent original-sticker replay of the previously certified exact 13-action DR-preserving continuation provides a legal upper bound (the 10-action alphabet is a subset of the full 18-action alphabet). Thus for both, mathematically **d_18(sourceDR,solved)=13**.

**Physical source-path verdicts**

| Authored source DR | Conditional source grade | Prefix raw actions | Exactly shortest all-18 suffix | Raw total actions |
| --- | --- | ---: | ---: | ---: |
| Miao main FB | written linear prefix | 10 | **9** | 19 |
| Riabov main FB | written linear prefix, physically identical to Miao main | 10 | **9** | 19 |
| Miao alternative FB from same four-turn EO | written linear prefix | 11 | **12** | 23 |
| Riabov Other #1 LR | contiguous normal-side source reconstruction hypothesis | 9 | **13** | 22 |
| Riabov Other #3 LR | contiguous normal-side source reconstruction hypothesis | 10 | **13** | 23 |

Riabov Other #1 literal authored prefix ends F and the computed optimal suffix begins F2. The concatenation has **22 raw stage-preserving actions**, but merging F F2=F-prime gives a physically equivalent **21-HTM normalized word** which no longer literally preserves the source prefix as a separate contiguous segment. The proof therefore deliberately labels both counts; it does not assert a global FMC optimum.

**Independent CI:** [P8-R5 Riabov 18-HTM exact 12/13 decision SUCCESS #38081458813](https://github.com/WhoSia/CUBE-REV/actions/runs/38081458813); [complete JSON certificate #11680219208](https://github.com/WhoSia/CUBE-REV/actions/runs/38081458813/artifacts/11680219208), ZIP SHA-256 `04d38264b5cd5ecb7d909265cda8ce6bf5185c5e30060007e507f6379053329e`. Source verifier: `scripts/cuberev-022/verify-p8-r5-riabov-general18-middle-two.mjs`. Its workflow uses repository `contents: read` only.

## 3. The same-EO physical branch and why projected search cost can reverse whole-state ranking

**Actually authored fork:** Both Qijun Miao attempt-one DR paths share the first six legal turns **L2 F' L D L2 F2** (the first four are the author's source EO, the next two are shared DR extension). The first divergence is at legal move **7**, main B versus alternate L-prime. Both complete stages physically satisfy FB-axis DR, and independent full-cube physical hashes differ.

At these two real DR endpoints, full-cubie physical comparison finds **six distinct corner permutation slots and six distinct edge permutation slots**. Within the half-turn group's verified orbit partition, the source-endpoint UD-edge occupancy mask remains identical at integer 114, while the corner occupancy mask differs: 46 main versus 204 alternate. This is a *specific observable structural contrast*, **not** proof that a single corner orbit mask uniquely causes the four-move effect.

### Dual exact reverse-projection lower bounds versus exact whole-cube cost

R3 independently built exact backward BFS databases for (eight corner permutations, four E-slice edge permutations) and (eight UD-edge permutations, four E-slice permutations), each 8!×4!=967,680 projected states. Since any actual full DR-preserving path projects to a legal path in either database, their maximum is an admissible lower bound. P8-R5 independently replayed the two actual source states and the physical moves to remeasure their projected lower bounds:

| Physical endpoint | Corner+E-slice projected lower | UD-edge+E-slice projected lower | max admissible h | Exact whole-cube DR-preserving d | Gap d−h |
| --- | ---: | ---: | ---: | ---: | ---: |
| Miao main | 6 | 8 | **8** | **9** | **1** |
| Miao alternate | 4 | 6 | **6** | **12** | **6** |

**Counterexample:** Every displayed independent partial-distance lower bound is numerically smaller for the Miao alternative, yet its whole-cube shortest completion is **three actions larger**. Thus independent projected difficulty rankings cannot be elevated to actual whole-state candidate rankings. The residual is a model-specific whole-state coupling / abstraction loss, not an identified unique physical factor. In particular the equality `d_Alt−d_Main = (h_Alt−h_Main)+[(d−h)_Alt−(d−h)_Main] = −2+5 =3` is an **exact descriptive decomposition**, not a causal mediation estimate.

The extra one DR source turn gives `(11−10)+3=4` total exact fixed-prefix HTM disadvantage. R4 already proved this **same 19-vs-23 comparison using all 18 legal post-prefix turns**, independent of whether either solution maintains DR. R5 provides a sharper structural falsification of naive independent subproblem search, not a rebranding of R4 as a new global Rubik optimum.

Earlier physical Schreier HTR contact costs are 5 main and 7 alternative. That also distinguishes their endpoints, but the 29,400-state left-coset distance cannot by itself recover the shortest solved-state distance. Only the full physical cube exact proof settles 9 vs 12. Do not propose informational or epistemic scalars in place of physical cubie constraints.

**Independent CI:** [P8-R5 same-EO cubie/PDB contrast SUCCESS #38081607848](https://github.com/WhoSia/CUBE-REV/actions/runs/38081607848); [physical projection/branch certificate #11680512339](https://github.com/WhoSia/CUBE-REV/actions/runs/38081607848/artifacts/11680512339), ZIP SHA-256 `36504d337de733eee567c56117406f09d64c3ba28da5cd9975657a9c8351030c`. Source code: `scripts/cuberev-022/verify-p8-r5-Miao-sameEO-physical-projection-contrast.mjs`.

## 4. What is demonstrably human and what is not

There are now three distinct evidential levels:

- **Retrospective authored observation:** Qijun Miao documented both a main attempt-one DR and a second extension from the same EO; Riabov documented other fragments and coarse EO search count/timing. This supports actual *written* alternative candidates, not only artificial computer alternatives.
- **Exact physical counterfactual:** If the written prefix is kept fixed and the solver thereafter receives unrestricted 18 outer-face moves, exact minimum physical completion cost differs (Miao main 19, alternative 23); full source-conditional Riabov 13-turn suffix results also verified. This provides a physically meaningful feasible-opportunity difference.
- **Human decision mechanism:** No source documents a complete timestamped set of alternatives, exact search operations, cognitive state trajectories, or explicit 19-vs-23 comparison at time of choice. Do not claim an effect on the actual competitor's preference or an identified cognitive strategy. The source author's remarks on search coverage are author retrospective testimony, not experimental mediator data.

The physical fork and endpoint cost are suitable **inputs to a falsifiable future human-process hypothesis**, but not already evidence of a cognitive mechanism. A prospectively predeclared task with timestamped candidate selection and source-side reconstruction would be required to adjudicate that causal question; no new VFMC/video collection or human recruitment is authorized here.

## 5. Custody, release and remaining work

- Default research branch `research/current`, author/committer `WhoSia` only; Actions `contents: read` and no writeback. Historical P7 active-set audit failures and nondefault main branch historic bot deploy commit remain separately reported. Do not sanitize existing fail logs.
- Prior P7/R2/R3/R4 versions, independent source-to-cubie provenance, source parsing HOLD, and physical solution receipts all preserved. P8-R5 is a substage within version 0.22; not permission to promote 0.23.
- Riabov Other #2 original notation parse remains **HOLD**; Other #1/#3 new 13-turn results are *conditional on P7 source grammar*.
- Unrestricted *entire FMC* optimum (where historical EO/DR prefixes, insertion, NISS and cross-side operations can change) remains **NOT PROVEN**.
- A stronger structural explanation than one PDB-order counterexample requires controlled neighboring physical states or demonstrable counterfactual interventions on cubie constraints, with matched initial conditions and exact state-to-state search. This should be designed within the current physical cube research and must not be relabeled human cognition without direct evidence.

**Next exact physical attack:** source-adjacent perturbations from the common EO branching state, explicit neighboring DR endpoints and exact geodesic costs, followed by cross-candidate robustness / falsification. Prioritize mechanical reproducibility and source-side constraints over generic philosophy of information.
