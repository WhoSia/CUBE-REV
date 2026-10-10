# CUBE-REV 0.22 P8-R4 — Full DR/HTR Schreier Geometry and All-18-HTM Source-Conditioned Completion Dominance

**Stage:** CUBE-REV 0.22, P8-R4. This is an extension of P8, not a new 0.23 release.

**Formal program title retained:** *Source-Relative FMC Continuation Geometry & Candidate Dominance Tests: Multi-Axis DR–HTR Reachability, Exact Endpoint-Cost Comparisons, Non-Dominated Search Branches & Retrospective Process Constraints.*

**Independent evidence verdict (2026-10-11 KST):** **PASS** (i) complete 29,400-vertex authentic DR/HTR left-coset Schreier transition census, (ii) exact HTR contact distance **10** from Riabov Other #3 under its declared conditional normal-side source parse, and (iii) exact general 18-HTM whole-cube minimal post-prefix completions of **9 vs 12** for the two source-authored Miao same-EO DR branches, yielding **19 vs 23 raw HTM actions** including fixed authored prefixes. NOT a global FMC optimum or observation of human mental path.

## 1 — Origin and evidence typing

Original source: P7 actual FMC World 2026 authored retrospective attempt-one candidate records, as preserved in `data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json`. The six written EO+DR candidate pairs give five complete physical endpoints under their explicitly chosen parses; five satisfy a real phase-axis DR definition and correspond to four distinct DR physical states. Miao and Riabov main written DR variants commute to the same physical FB DR endpoint. Riabov Other #1/#3 need the **ASSUMED_CONTIGUOUS_NORMAL_SIDE_FOR_TEST_ONLY** input-type assumption; Other #2 remains CONTEXT/PARSE HOLD. The authored 10-turn Miao main DR word is NOT a contiguous prefix of the original 19-turn submitted human FMC final word.

R3 independently proved bounded HTR noncontact for Riabov Other #3 through eight turns (`d_H≥9`), and exact ten-DR-action completion costs `9/9/12/13/13`; its step-by-step optimal completion path visited HTR only at step 13 for Other #3. R4 directly addresses the remaining HTR first-contact uncertainty and the robustness of the same-EO Miao branch comparison when all 18 real face turns are allowed after the fixed written DR prefixes.

## 2 — Exact HTR Schreier action

Let `G=<U,U2,U',D,D2,D',R2,L2,F2,B2>` be the orientation-zero, phase-axis-canonical actual 3×3 DR subgroup; its permutation states have cardinality

`|G| = (8! × 8! × 4!)/2 = 19,508,428,800.`

Let `H=<U2,D2,R2,L2,F2,B2>`, the physically exhaustively enumerated half-turn subgroup with **663,552** full cubie states. The index is `[G:H]=29,400`. For LEFT cosets `Hg`, the right move action `(Hg)a=H(ga)` is well-defined, whereas the quotient does not preserve distance to the solved identity.

**Exact operational representation.** The six half-turn generators act on corner positions with physical orbits **[0,2,5,7]** and **[1,3,4,6]**, and edge positions **[0,2,4,6]**, **[1,3,5,7]**, and **[8,9,10,11]**. The two selected 4-of-8 orbit occupancy masks identify **70×70 = 4,900** bins. To distinguish the residual cosets within each bin, compare arbitrary physical representatives g and r by explicitly constructing the left ratio `h = g r^{-1}` and checking its complete 8-corner + 12-edge permutation against the independently BFS-enumerated H set. Exactly **six** residual H-cosets per occupancy bin are found.

An actual right-generator BFS constructs **29,400** physical representatives and **294,000** labeled generator edges, with exactly **4,900** bins containing six cosets each. All 294,000 edges pass the inverse-generator return property and one-step distance Lipschitz check. Another **500** sample h-left-multiplied representatives independently verify that different physical representatives of the same left coset yield the same right-action edge target.

**Actual complete Schreier distance distribution**, distance 0 through 13 respectively:

`[1, 2, 9, 36, 124, 530, 1806, 3732, 5158, 7070, 7218, 3202, 488, 24]`.

The sum is **29,400**, and the full Schreier Cayley-target diameter is **13 HTM**. This is about HTR group contact, NOT the full 3×3 Rubik group's God’s number or solved-state distance.

### Physical authored-candidate results

| Authored candidate | Fixed verified DR axis | Schreier exact d(g,H) HTM | Authority |
| --- | --- | ---: | --- |
| Miao main | FB | **5** | actual source linear prefix |
| Riabov main | FB | **5** | actual source linear prefix, identical physical endpoint |
| Miao same-EO alternate | FB | **7** | actual source linear prefix |
| Riabov Other #1 | LR | **7** | conditional source parse |
| Riabov Other #3 | LR | **10** | conditional source parse |

For Riabov Other #3, one physical shortest actual-face suffix is:

`U2 R2 F2 R B2 L B2 L' F2 L'`

The original scramble + literal source DR prefix + this ten-turn suffix is independently replayed by the source full 54-sticker physical oracle and ends in the genuine HTR subgroup in the verified LR phase axis. Exhaustiveness of all **29,400** coset shortest-distance BFS removes the possibility of any nine-turn-or-shorter HTR contact for this source-conditioned physical state. **R3 [9,13] interval is now EXACTLY 10**, without retroactively changing R3's historical conclusion.

**Read-only independent CI SUCCESS #38079623253:** https://github.com/WhoSia/CUBE-REV/actions/runs/38079623253

**Original group/Schreier full JSON certificate #11680026198:** https://github.com/WhoSia/CUBE-REV/actions/runs/38079623253/artifacts/11680026198

ZIP SHA-256 `5f14542e272ce7f160369a951e9a8ac2ab98b4d318a3d267b86c52a698650045`.

Source code: `scripts/cuberev-022/verify-p8-r4-schreier-29400-left-cosets.mjs`, workflow: `.github/workflows/cuberev-022-P8-R4-Schreier-29400.yml`.

## 3 — All 18 true HTM moves after actual source DR prefixes

**Changed experiment:** The physical state after each literal source EO+DR prefix is frozen, but the continuation is now allowed ANY of the 18 legal outer-face HTM quarter/half turns. Thus the continuation is **not restricted to remain DR** and need not enter HTR before completion. No human-submitted NISS-insertion grammar or alternative authored prefix is inferred.

Use the actual sticker-derived full cubie representation with corner and edge permutations **and orientation**. Bidirectional BFS from the real solved state through depth **5**, with exact layer counts **[1, 18, 243, 3,240, 43,239, 574,908]**; distinct source state BFS through depths 4 and 5; prune only adjacent same-face moves (mergeable in HTM) and reversed adjacent opposite-face commuting moves (canonically reorderable without changing length). These pruning rules preserve at least one representative of any shortest solution.

For any path of length ≤9, a midpoint occurs within 4 source moves and 5 goal moves. For ≤10, use 5 and 5. For any path of length **exactly 11**, enumerate actual legal goal-side turns from the full goal depth-five frontier and test physical membership in the source depth-five set, **without materializing the ~7.6-million-state depth-six layer**. The independent expanded CI checked **10,348,344** directed goal depth-five extensions for each of the three non-main source DR endpoints and found **no ≤11-turn solution** for any of them. The source's entire original legal physical state is used, not the 29,400 HTR coset quotient (which would discard necessary information to solve the cube).

### Completion cost results

| Authored DR candidate | Authored literal prefix | Exact 10-generator DR continuation | General 18-HTM continuation | Fixed-prefix raw completion cost |
| --- | ---: | ---: | --- | --- |
| Miao main | 10 | 9 | **9 exactly** | **19 exactly** |
| Riabov main | 10 | 9 | **9 exactly** | **19 exactly** |
| Miao same-EO alternate | 11 | 12 | **12 exactly** | **23 exactly** |
| Riabov Other #1 | 9 | 13 | **12–13** | **21–22**, conditional source parse |
| Riabov Other #3 | 10 | 13 | **12–13** | **22–23**, conditional source parse |

**How the Miao alternative exact 12 is proved:** The all-18-HTM meet-in-middle search excludes every completion in ≤11, giving `d_18 ≥12`. The independent R3 ten-action DR-preserving shortest 12-turn suffix is itself a valid sequence of general 18 HTM face turns. The R4 combined verifier physically replays this precise authored-prefix-specific earlier witness, giving `d_18 ≤12`. Hence `d_18=12`.

For Miao main, an independently physical-solved 18-HTM 9-turn suffix is present, and complete bidirectional BFS certifies no shorter completion. The two candidate prefixes share one genuine written four-turn EO prefix but diverge at their authored DR extensions. Thus:

`(11+12) - (10+9) = 4 HTM`.

**Exact result:** If and ONLY if the two human-authored literal EO+DR candidate prefixes are frozen and any subsequent legal 18 outer-face moves are allowed, the main Miao prefix is **exactly four HTM actions cheaper** at physical completion than the alternate prefix. The result is robust to leaving DR entirely after the fixed stage prefix. The full original 54-sticker oracle independently validates both complete words. Their normalized examples preserve the authored literal stage prefix.

This is a concrete restricted scientific counterfactual about **physical endpoints and admissible continuation costs**, not a proof that the human deliberately compared these two distances, not general superiority of an algorithm or of HTR-first choice, not evidence of an unobserved mental state, and not an unconstrained FMC optimum allowing NISS, insertions or changes to the prior prefix.

For the Riabov Other cases no general-18 exact 12/13 selection is certified yet; report **[12,13]**, not a fabricated scalar. Riabov Other #1's original DR-restricted raw 22-turn concatenation has the boundary `F F2` and compresses to 21 physical HTM turns only by changing the literal authored stage segmentation. Do not silently equate raw physically staged action totals with irreducible FMC normalized solution lengths.

### Reproduction and independent proof receipts

- All-18 code and explicit witness/normalization checks: `scripts/cuberev-022/verify-p8-r4-general-18-htm-mitm.mjs`.
- Read-only Actions: `.github/workflows/cuberev-022-P8-R4-general-18-HTM-MITM.yml`.
- Initial radius 5+5 PASS: https://github.com/WhoSia/CUBE-REV/actions/runs/38079780445, artifact #11679791880.
- Exhaustive depth-11 streamed absence PASS: https://github.com/WhoSia/CUBE-REV/actions/runs/38079862936, artifact #11680555160.
- **Source-upper + unrestricted-lower joined exact source-prefix PASS: https://github.com/WhoSia/CUBE-REV/actions/runs/38079967359**, artifact https://github.com/WhoSia/CUBE-REV/actions/runs/38079967359/artifacts/11680381293 ; ZIP SHA-256 `32052627c2e158ff992b70fa9b220f2b64ceaf9939ed7a3560f7034216829f9c`.
- R3's original authorized phase-two exact witness ledger: `data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json`. Its lower-bound authority is prior independent R3 PDB/IDA exhaustive 10-generator proof; the R4 CI explicitly replays its original source full-cube upper witness, not an imagined human step.

## 4 — Remaining scientific and governance boundaries

- **R4 physical subgroup/coset contact problem CLOSED** for the current four certified physical DR source endpoints, subject to stated conditional source interpretations.
- **R4 original-source Miao same-EO 18-HTM fixed-prefix cost comparison CLOSED** at exactly 19 versus 23.
- **Riabov Other #1/#3 all-18 continuations:** only exact interval [12,13] for suffix, not settled shortest distance; source words remain conditional.
- **Riabov Other #2:** original mixed-side/NISS/notation context HOLD, not author error.
- **Cognitive mechanism:** recorded textual candidate identities and physical possibilities, not observed moment-by-moment human search; stay in actual cube physics.
- **Unconstrained full FMC:** prefix may be altered, NISS/insertions and global shortest solution not evaluated.
- Preserve all P7/P8-R2/R3 source and CI failures, and read-only Actions custody. Current default is `research/current`; use human `WhoSia` author/committer only, no Actions writeback. The persistent legacy P7 active-set audit failures and historical nondefault `main` bot-authored deployment commit are separate debts; no repository-wide green claim.

**Next discriminating step:** resolve the two Riabov Other general-18 intervals [12,13] with an exact depth-twelve test if scientifically worthwhile, while guarding conditional source interpretation. More importantly, seek real candidate-selection chronology or genuinely richer source grammar before attributing any cognitive search mechanism. Do not promote 0.23 solely because the subgroup benchmark is completed.


## P8-R5 certified successor (2026-10-11)

The R4 [12,13] all-18-HTM completion intervals for conditional Riabov Other #1 and #3 were the correct bounded R4 status. They were independently closed in [P8-R5](P8_R5_ALL18_RIABOV_EXACT_AND_MIAO_JOINT_CONSTRAINT_BRANCH.md): both have **EXACT 13** shortest post-DR legal 18-HTM physical continuations, from a verified exhaustive middle-two depth-twelve non-intersection of **186,270,192** queries plus independently physically replayed previously certified 13-turn upper witnesses. New [physical evidence CI #38081458813](https://github.com/WhoSia/CUBE-REV/actions/runs/38081458813) and [certificate #11680219208](https://github.com/WhoSia/CUBE-REV/actions/runs/38081458813/artifacts/11680219208) close these intervals without changing the conditional source-side interpretation.

P8-R5 also separately cross-examined Miao's two actual same-EO branches and found the corner+E and UD-edge+E exact PDB lower bounds **both reversed the final cost ranking**: main projected max=8, exact DR completion=9; alternative projected max=6, exact completion=12. This reveals a concrete whole-cubie coupling/abstraction loss counterexample; it is not a uniquely identified causal mediator or proof of the author's actual decision chronology. [Independent PDB physical contrast #38081607848](https://github.com/WhoSia/CUBE-REV/actions/runs/38081607848). Preserve R4's historical proof and all group verification records, now superseded only on these former HOLD subquestions.
