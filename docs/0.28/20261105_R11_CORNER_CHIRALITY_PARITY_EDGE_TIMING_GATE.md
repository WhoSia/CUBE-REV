# CUBE-REV 0.28 R11 — Corner Chirality, Edge Parity Timing and Joint Identification

Date: 2026-11-05. Status: constructive mathematical arguments, independent local P48 reimplementation, multiple GitHub source and CI gates; remote Actions runs were QUEUED at the final verification snapshot. Do not promote remote R11 to PASS before a completed run receipt.

## Central hard problem

Full Rubik legal 18-HTM group, one exact 6-color edge and one exact 6-color corner facelet per frame, known actions. Current confirmed global optimum bounds are 18 <= h_adaptive <= 21, with exact fixed nonadaptive h=21. All R11 results below preserve this OPEN global adaptive problem. The original CUBE-REV human reconstruction goal remains distinct from a hypothetical physical color-probe information theorem.

## Lemma A: exact ordered-corner chirality

P48 physical corner facelet cycles are right-handed. For each of eight original corner types and each of three physically legal twists, the pair of colors seen at two distinct prescribed ORDERED spatial corner facelets is unique. All eight times three = 24 possible type-and-orientation configurations are in bijection with 24 ordered adjacent color pairs. An independent 3D normal-vector enumerator confirms these 24 mutually different ordered results. Unordered color pairs would NOT work.

## Theorem B: full corner subsystem from 14 corner-color readings, no edge oracle

Observe two ordered facelet colors at seven spatial corner positions, 14 readings total. Lemma A individually determines the seven source labels and twists. The last label is the sole remaining corner type; its orientation is forced by the legal twist sum modulo 3. This works for EVERY legal cube with no edge parity information. It is a constructive SUFFICIENCY result, not the exact corner-only optimum.

Source: scripts/cuberev-observation/audit_r11_corner14_chirality.py. Independent local 3D P48 reimplementation generated 2,501 legal cube states and exactly recovered corners from only these 14 colors. Independent source is available as /mnt/data/r11_independent_geometry_audit.py in this conversation environment. Remote CI still awaits confirmation.

## Lemma C: 13 corner colors given one true edge parity bit

Two ordered facelet colors at six corner positions identify their six types and twists (12 reads). The two remaining original corner labels can be assigned to the final two spatial positions using equality of edge and corner permutation parity. One extra color at the seventh position identifies its twist; corner-twist sum determines the last. Thus 13 fixed corner color reads suffice PROVIDED the actual true edge permutation parity bit is already known. Never introduce this bit before a real policy has obtained it.

Source: scripts/cuberev-observation/audit_r11_corner13_with_parity.py. Independently checked on 2,501 legal random P48 states.

The earlier constructed R11 19-corner (parity-known) and 20-corner (parity-unknown) methods are less efficient and are superseded by 13 and 14. Neither 13 nor 14 is asserted globally minimal.

## Theorem D: upgrade the existing full-cube fixed 21-frame construction

Pair the original R2 21 distinct edge-facelet slots (10 complete spatial edge positions plus one facelet at an eleventh) with the 14 distinct corner-facelet slots of Lemma B, repeating seven already seen corner slots in frames 15–21. All 21 joint probe slot pairs are real legal P48 addressable pairs among the known 576 reachable pairs. The complete corners and their permutation parity are recovered after 14 frames. The final two missing original edge labels are separated at frame 21 using corner/edge permutation parity, the partial edge color fixes its flip and the even total edge-flip parity fixes the last flip.

Consequently every legal full cube state is reconstructed using 21 actual simultaneous frames, 21 DISTINCT initial spatial edge sticker colors, and only 14 DISTINCT initial spatial corner sticker colors: 35 ESSENTIAL initial sticker positions, even though sensors physically emit 42 color symbols. A real no-reset 18-HTM route is constructed. This does not improve the temporal optimum (still 21 for nonadaptive policies).

Source: scripts/cuberev-observation/audit_r11_full21_with_corner14.py. Independent second P48 decoder (separate source and randomly generated legal cubes) recovered 2,400 legal scrambles correctly; source /mnt/data/r11_full21_independent_audit.py.

## Theorem E: unknown edge parity makes the Hall 18-read bound decisive for edge-only sensing

Without any corner observations or parity oracle, the observer must distinguish 12! times 2^11 = 980,995,276,800 legal edge states (both edge permutation parity classes); every edge arrangement extends to some legal full cube. The R7 Hall-constrained universal ADAPTIVE color-tree capacity at 18 edge reads is 947,446,315,200, strictly smaller. Hence an edge-only observer with no corner parity information needs at least 19 adaptive reads even with free access to arbitrary spatial initial edge facelet slots. The ordinary full two-probe cube remains lower-bounded by 18, NOT 19: the corner sensor may reveal information about edge parity.

Source: scripts/cuberev-observation/audit_r11_edge_unknown_parity_hall.cpp. Independently reimplemented and compiled in /mnt/data/r11_hall_unknown_parity_independent.cpp: exact answer 947446315200, 2,245,866 visited Bellman signatures. This shows how one bit changes the COUNTING lower-bound barrier; it does not establish an exact one-frame difference in optimal adaptive policies.

## Negative theorem F: a natural staged 14+6 edge policy is insufficient

If the first 14 edge color reads fully determine seven predetermined spatial edge positions, then five unknown edges remain. Once 14 corner colors have identified the true corners, the residual edge permutation and flip parity conditions are known, but there are 5!/2 times 2^4 = 960 compatible residual edge configurations per remaining label set and parity combination.

Exhaustive exact adaptive minimax search over all ten available spatial facelets gives the following two checked example label sets:
- UR, UF, UL, UB, DR: adaptive 6-read continuation exists, 5 reads fail.
- UR, UF, UL, UB, FR: a 6-read continuation is IMPOSSIBLE, while 7 predetermined reads suffice.

Both statements hold across all four permutation/flip parity conditions. The separate local Python implementation fully evaluated the failing six-read tree (9,517 memoized nodes in one parity case). GitHub source: scripts/cuberev-observation/audit_r11_five_edge_20frame_gate.py. This disproves only the specified FIXED seven-complete-edge-prefix 14+6 family; it does not eliminate genuinely mixed or interleaved 20-frame policies.

## R12 research decision — no escape

The core next gate is a 20-frame ZERO-ERROR full-cube decision tree whose first 14 corner slots recover corners, while edge query selection before parity is learned cannot illegally depend on the true parity. Candidate adaptive edge policies must be tested against all legal states and both parity classes. Alternative target: prove a stronger full-group all-policy adversary by retaining the correlation between edge and corner observations. Legal no-reset routing has been demonstrated by R10's 576-pair reachability and actual P48 action replay, but no complete 20-frame algorithm has been found.

Human action timing, visual memory and cognitive strategy remain empirical, and the 0.21 strict cross-reconstructor state-history comparison has zero overlap. Never present an HTM count or a mathematical oracle as a measured cognitive cost.

## Evidence custody and limitations

GitHub source code and formal explanation are public on WhoSia/CUBE-REV, research/current; commit author/committer must remain WhoSia and CI is read-only. The independent local 3D and Hall verifiers are available for explicit reuse. P7 allowlist registers all R11 executable sources. Remote GitHub Actions currently QUEUED in this session; report this precisely, and only mark SUCCESS after completed run plus log readback. Notion is the semantic head and must be separately updated/verified. No newly published participant data.
