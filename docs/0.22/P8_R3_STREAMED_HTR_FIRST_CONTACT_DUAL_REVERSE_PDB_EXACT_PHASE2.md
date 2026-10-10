# CUBE-REV 0.22 P8-R3 — Streamed HTR First-Contact Search & Dual Reverse-Projection Exact Phase-Two Completion

**Stage:** CUBE-REV 0.22 P8-R3, not 0.23. Keep the existing formal P8 title and all P6–P8-R2 verdicts.

**Final scope:** Original FMC World 2026 sourced written candidate fragments, original 54-sticker full-cube transitions, axis-conjugated actual physical DR groups, ten legal phase-two HTM moves, source conditionality maintained. P7 still counts 6 written candidates, 5 physical endpoints under selected parses, 5 DR-valid paths and 4 distinct DR endpoints. Riabov Other #2 parse HOLD. Riabov Other #1/#3 remain conditional on consecutive normal-side interpretation; the source does not prove human temporal search order.

## R3.1 — Exact eighth-turn HTR exclusion

The LR-axis Riabov Other #3 full DR cube passed independent 0..7 exhaustive frontiers with unique whole-cubie counts 1, 10, 74, 524, 3589, 23508, 146571, 883454 and zero HTR endpoints. For last-move h belonging to the six-generator square subgroup H, g*h is in H iff g is in H. Therefore the first entrance to H cannot end in a half turn. Inspecting exactly four possible terminal quarter turns (U, U-prime, D, D-prime) from each depth-7 physical state is exhaustive for the 8-turn first arrival. The R3 verifier computed 3,533,816 eighth-edge original physical HTR membership checks: **ZERO HTR contacts**; no eighth frontier materialized.

**New exact lower bound: d_H(Riabov Other #3) >= 9**, in the fixed ten-action LR DR-preserving grammar under the source parsing assumption.

Source program: https://github.com/WhoSia/CUBE-REV/blob/research/current/scripts/cuberev-022/verify-p8-r3-streamed-first-htr-depth8.mjs
External independent CI **SUCCESS #38077503684**: https://github.com/WhoSia/CUBE-REV/actions/runs/38077503684
Artifact #11678612250: https://github.com/WhoSia/CUBE-REV/actions/runs/38077503684/artifacts/11678612250
Artifact ZIP SHA-256 4f46b09324283f71e2fd29a35ef4f85e8e5535c08c39188ba625af08a411bb1d.

## R3.2 — Reverse PDB to exact complete physical DR-phase solutions

Unlike forced HTR-first decomposition, the new test minimizes moves all the way to solved within the entire **ten-action DR-preserving phase-two grammar**. From physically solved, reverse BFS builds TWO exact pattern databases for (8 corner permutations x 4 E-slice edge permutations) and (8 UD-edge permutations x 4 E-slice edge permutations), **967,680 states each**, projected diameters **14 and 12**. Their maximum defines an admissible lower bound on real full-cube distance to solved. Forward depth-limited IDA exhausts lengths in increasing order; same-face adjacent turns and reverse-order adjacent opposite-face commute pairs may be pruned because each forbidden pair has an equally short or shorter normalized representative. Search has 20,000,000 visits per unique physical endpoint as hard cap; NO solved witness or lower-bound proof was capped. Every complete word was independently replayed against the actual full 54-sticker original competition scramble.

| Authored DR path | Axis | Literal stage HTM | Exact ten-action DR-to-solved distance | Raw authored-prefix-plus-continuation actions |
| --- | --- | ---: | ---: | ---: |
| Qijun Miao main | FB | 10 | **9** | **19** |
| Yurii Riabov main | FB | 10 | **9** | **19** |
| Miao alternate from same four-turn EO | FB | 11 | **12** | **23** |
| Riabov Other #1 (conditional parse) | LR | 9 | **13** | **22** |
| Riabov Other #3 (conditional parse) | LR | 10 | **13** | **23** |

The two different main written DR words correspond to the same **physical** DR endpoint, so their optimal continuation distances agree. The first CI reused the previous source's literal prefix in the cached representative witness; repaired verifier independently reconstructs and original-sticker-replays **each actual author's own** original source prefix. Never conflate reused endpoint distance with source text identity.

**Critical count caveat:** the source literal Riabov Other #1 prefix ends in F and its newly computed suffix begins in F2; the written joint 22-turn sequence can be reduced by the group identity F F2 = F-prime, producing a physically equivalent 21-turn normalized final word. This changes the literal source-prefix boundary; 22 is the exact *raw prefix-preserving action budget*, NOT a claim of globally minimal normalized FMC word length. For the other four cases the reported literal stage and appended solution do not share this immediate same-face join.

**New real 19-turn physical solution continuing Miao's actual DR state:**

    L2 F' L D L2 F2 B L B2 L
    R2 B' R2 U2 B U2 L2 B F

This whole sequence was physically solved against the genuine scramble. Its nine-turn suffix was independently proved shortest inside the ten-action DR grammar, not among all 18 outer face moves. The author's original submitted 19-turn word is DIFFERENT and is not itself a literal suffix continuation of this DR prefix. This resolves the previous apparent conflict without inventing human workflow history.

The former physically valid P8-R2 21-turn compulsory HTR-completion witness was **not** the shortest unconstrained-within-DR completion: its 5+6-stage construction cost 11 after DR, while the new 9-turn direct DR solution shows the cost of compulsory HTR-halfturn decomposition. Preserve the R2 achievement as an exact constrained stage geometry and valid upper bound, not an incorrect result.

**Restricted exact dominance:** Two Miao DR candidates share the exact same real four-turn EO prefix. Under the fixed literal candidate prefixes and ten DR-preserving completion turns, their **optimal raw total costs are 19 and 23**. The main candidate is strictly four actions cheaper in that precisely specified model. No proof of global FMC dominance, cognized participant consideration, insertion/NISS equivalence, or preference is implied.

Source code: https://github.com/WhoSia/CUBE-REV/blob/research/current/scripts/cuberev-022/verify-p8-r3-reverse-pdb-exact-phase2-ida.mjs
Independent read-only CI **SUCCESS #38077785735**: https://github.com/WhoSia/CUBE-REV/actions/runs/38077785735
Corrected full authored-prefix proof artifact #11678697387: https://github.com/WhoSia/CUBE-REV/actions/runs/38077785735/artifacts/11678697387
ZIP SHA-256 cc8665e9bd70dae7db619baaa41f2d3823eaa768cff9cd85f1e212b3d337df98. Prior CI #38077689105 is retained as initial exact-distance grade, not promoted as its cached Riabov word was not authored-prefix-specific.

Since solved belongs to H and Other #3 has a real 13-turn direct DR-preserving completion, the combined rigorous remaining HTR-contact interval is **9 <= d_H(Riabov Other #3) <= 13**. Exact contact value inside this interval remains OPEN; solved-distance is already EXACT 13.

## R3.3 — Legitimate coset quotient versus invalid full-solve quotient

The DR subgroup G has all zero orientations, freely chosen 8-corner, 8 UD-edge and 4 E-slice permutations with one parity condition. It has cardinality (8!)^2 * 4!/2 = **19,508,428,800**. H has the physically enumerated **663,552** states. Therefore its index [G:H] = **29,400**. The right-move action on LEFT cosets H*g is well-defined, and distance from g to H depends only on that left coset. A complete 29,400-vertex Schreier quotient is a mathematically legitimate future way to compute all HTR-contact distances; **R3 has not yet constructed the Schreier graph**.

The quotient does NOT preserve distance to the solved identity: solved and U2 lie in the SAME H coset but need zero and one move to solve, respectively. Thus applying the 29,400-node HTR quotient to a shortest complete solution is UNSOUND. R3 instead used backward physically derived PDB projections and forward exact IDA.

## Governance and follow-on

All code and workflows remain on actual default branch research/current under human WhoSia authorship; Actions has contents: read with no GitHub writeback. The historic active-set CI failure remains unrelated. The historical nondefault main branch has one bot-authored deployment commit; preserve for separately authorized custody-safe repair. Retain older P7 and P8 run failures and artifacts. No video/VFMC acquisition, no new human recruitment, no speculative human attention or knowledge scalar.

**Next precise question:** materialize/independently validate full 29,400-coset Schreier graph and decide whether Other #3 first reaches H at 9, 10, 11, 12 or 13. Separately test 18-move post-DR unrestricted minima against the present fixed-10 grammar, keeping source-side and user consent boundaries.
