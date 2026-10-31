> **AUTHORITATIVE SUPERSESSION — 2026-10-31, B7 CLOSED.** The older claims below that b7 ∈ {17,18}, that at most 144 candidate 17-sensor layouts remain, and that 18 parallel-edge pairs lack B7 witnesses are HISTORICAL. Physical 14-HTM pure-outer words have now been verified for both opposite-parallel and same-face-parallel flipped edges; the latter were normalized from published middle-slice macros and physically cross-checked. Combined with the preexisting three 13-HTM words and both actual B7 midpoint transports, all **66/66 two-edge** supports occur in B7. Together with **28/28 two-corner** supports and typewise cube legality, the complete minimum obstruction clutter is **94 pure two-cubie pairs**. Therefore for ALL r>=7, **b_r=18, 96 optimal 18-tag layouts, four proper-rotation orbits of 24; b_r^(1)=20; b_r^(e>=2)=infeasible**. More strongly the entire static full-cubie-factor sensor-feasibility predicate on B7 equals that on the full legal cube group. Verified executable witness/evidence: [verify_b7_support_completion.py](../../scripts/cuberev-observation/verify_b7_support_completion.py), [verify_slice_to_htm.py](../../scripts/cuberev-observation/verify_slice_to_htm.py), [verify_b7_base_orbits.py](../../scripts/cuberev-observation/verify_b7_base_orbits.py). Formal canonical proof/semantics/audit are recorded directly in the dedicated 0.28 Notion page: https://app.notion.com/p/409ef561cf928193b3d1dc1165ad92ea . This does NOT solve adaptive binary/trit sensing costs or claim remote GitHub Actions CI success.

> **CORRECTION AND SHARPENING (2026-10-31, actual midpoint tag audit).** A solved-endpoint 13HTM word's *original cubie support* is not always the same pair of original tagged cubies that differ between the two B7 midpoint states. Directly computing BOTH physical midpoint states is essential. Three independently replayed 13HTM two-edge words, each cut after move 6 and move 7, give THREE distinct proper-rotation support orbits (sizes **24,12,12**), together exactly **all 48 pairs of NONPARALLEL physical cube edges**. They form the complete tripartite graph **K_(4,4,4)** on the three direction classes, each of four original edge tags. The 18 parallel edge pairs were NOT established or excluded by these three witnesses. Therefore any 17-tag B7 solution (7 corners+10 edges) must omit two PARALLEL edges, leaving at most **8×18=144 candidates**, tightening the earlier valid-but-weak 336 bound. One-erasure theorem b_r^(1)=20 (r≥7) is unchanged, but its correct proof should use verified **midpoint difference supports**, not just end-state supports. Source-grade independent checker: [verify_midpoint_transport.py](../../scripts/cuberev-observation/verify_midpoint_transport.py). This checked only the short words and orbit geometry, not full B7 injectivity.

# CUBE-REV 0.28 — Short-support phase diagram (2026-10-31)

## Model and evidence grades

Legal fixed-center 3×3×3 Rubik group, 18 outer face turns in HTM. Twenty original cubies are tagged (eight corners, twelve edges). Each tag contributes its COMPLETE position+orientation factor. This is distinct from instantaneous orientation-bit/trit sensing and adaptive-policy costs. B_r is the solved-state radius-r HTM ball. δ_r is the minimum number of differing cubie factors between distinct B_r states. b_r^(e) is the smallest selected tag set such that any e permanently erased selected tags still identify all B_r states.

### Physically verified short support witnesses (word existence is prior art)

- Face-diagonal corners, 12 HTM: U2 R' B D2 B' R U2 R' B D2 B' R. Changed originals: BLU, FRU; no edges.
- Body-diagonal corners, 12 HTM: U' B2 U L' F2 L U' B2 U L' F2 L. Changed originals: BDL, FRU; no edges.
- Adjacent corners, 14 HTM: R' D R F D F' U' F D' F' R' D' R U. Changed originals: FLU, FRU; no edges.
- Incident edges, 13 HTM: L F R' F' L' U2 R U R U' R2 U2 R. Changed originals: UF, UR; no corners.

Sources: https://puzzling.stackexchange.com/questions/117511/shortest-algorithm-to-rotate-2-corners-on-a-rubiks-cube and https://www.randelshofer.ch/rubik/patterns/U020.02.html . No claimed global shortest-word optimality. Two physically distinct implementations were used: old 54-facelet/20-factor model and a new standalone 48-movable-sticker tracker.

Proper 24 cube rotations of the corner words give size-12 face-diagonal, size-4 body-diagonal and size-12 adjacent-corner orbits. Hence all 28 corner pairs arise by radius7, of which at least 16 by radius6. The adjacent-edge witness yields 24 incident-edge pairs, touching all twelve edge tags, by radius7.

## Theorem 1 — Exact collapse radius δ6=2

Split a length-12 pure-two-corner word at its midpoint into a pair of states in B6. They differ in exactly two complete original cubie factors. No legal nonidentity cube element changes just one cubie (permutation parity and orientation invariants). Thus δ6=2 and δr=2 for r>=6. With inherited locally verified δ5=3, the first radius with distance2 is exactly six. Two permanent cubie-tag erasures cannot be tolerated from B6 onward even with all20 tags.

## Theorem 2 — Exact one-erasure threshold b_r^(1)=20, r>=7

A difference support exactly {a,b} forces BOTH a and b to be selected for one-erasure robustness. At radius6 rotated pure-two-corner words cover all corners; at radius7 rotated 13HTM pure-two-edge words cover all edges. Therefore all20 sensors are necessary from B7. They suffice because no legal nonidentity difference has cardinality one. This exact result does not rely on the full B5 census, only on certified physical words, symmetry and cube legality.

## Theorem 3 — B6 one-erasure dichotomy

Let L_EE be the shortest HTM word for an in-place two-edge flip fixing all corners/other edges. Existing δ5=3 yields L_EE>=11; the 13HTM word yields L_EE<=13.

Inherited B5 all C(12,3)=220 pure-three-edge supports mean B6 one-erasure robustness requires at least eleven edge tags. Radius6 pure-two-corner words force all eight corner tags. Hence 19<=b6^(1)<=20.

If L_EE>12, choose all 8 corners and any 11 edges. Every nontrivial support has at least two selected tags: the only potential two-support obstruction is a pure two-edge flip containing the one omitted edge, which is absent by assumption. Conversely, if L_EE<=12, rotate any pure-two-edge witness to touch any omitted edge, so all12 edges become compulsory. Thus b6^(1)=19 iff L_EE=13, otherwise20. Exact L_EE remains OPEN.

## Theorem 4 — B7 zero-erasure candidate pruning

By B7 every pair of two corners is a physical support, requiring >=7 corners to hit them all. Inherited B5 all pure three-edge supports require >=10 edges. Hence b7>=17. Any seven corners and eleven edges determine the entire legal cube state by missing-cubie parity and twist invariants, so b7<=18.

If a 17-tag B7 base exists, it consists of 7 corners+10 edges. Omitting one corner gives 8 choices. Of C(12,2)=66 omitted-edge pairs, 24 are adjacent (forbidden by the 13HTM edge collision orbit) and 42 are nonincident. Thus AT MOST 8×42=336 possible 17-tag bases remain under these necessary constraints; positive injectivity was NOT checked at B7.

At B6 any 16-tag candidate must be 6 corners+10 edges by inherited B5. Omitted corners cannot form a face/body diagonal, leaving 12 adjacent corner pairs and 66 edge pairs =792 preliminary candidates; inherited B5 mixed obstructions reduce those to at most 12×(66−18)=576. This is an upper bound on candidates, NOT 576 certified B6 solutions.

## General structure

Define the radius-r support-two graph with all original cubie tags as vertices and the physically realized exact two-cubie supports as edges. For zero-erasure identification, selected tags must be a vertex cover. For one-erasure identification, selected tags MUST contain every nonisolated graph vertex. This elementary graph principle plus short physical witness orbits proves the threshold above. Generic vertex-cover and cube legality are prior art.

## Reproducibility & status

- Independent executable 48-movable-sticker witness audit: scripts/cuberev-observation/verify_short_support_phase.py (four physical words and 24 proper rotations).
- Pure set-system test: scripts/cuberev-observation/verify_obstruction_phase.py (all corner pair orbit sizes and 336/792 candidate counts).
- Reference local note SHA256: 05a968d0d226d5783c87ee39b793efa23e6404eef44164d603695d596fbee210.
- Inherited but not rerun in this substage: full B5 positive layout census and 220 triple-edge supports. CI still NOT certified. No co-author bot, no 0.27 rewrite.

Notion canonical 0.28: https://app.notion.com/p/409ef561cf928193b3d1dc1165ad92ea
