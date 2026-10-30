# CUBE-REV 0.28 — Two-corner threshold for one-erasure cubie bases

Status: conditional mathematical theorem, not a new full-cube census. Date: 2026-10-31.

Let B_r be the radius-r ball of the 3x3 physical cube with 18 HTM face turns. Each sensor observes the full hidden position/orientation factor of one original tagged cubie (not a single instantaneous orientation bit/trit). A selected set S tolerates one permanently deleted sensor iff every physical difference support D(x,y) for distinct states in B_r contains at least two elements of S.

Define L_CC as the minimum HTM length of a nonidentity legal cube element whose full cubie support consists of exactly two CORNERS and no edges.

**Theorem (conditional on the physically checked 13-HTM adjacent-two-edge witness).** For every r >= 7,

    b_r^(1) = 19 if 2r < L_CC; otherwise b_r^(1) = 20.

**Proof.**
1. The 24 proper cube rotations of a physical adjacent-two-edge-only 13 HTM witness realize all 24 pairs of edges meeting at a cube vertex. Each corresponding state pair lies in B_7 by word midpoint factorization. To survive one erasure, both edges of each difference pair must be sensed. Thus all twelve edges must be installed.
2. Earlier B_4 physical witnesses realize all 56 three-corner-only supports, so at least seven corners must be installed to survive one erasure. All 20 cubies always suffice: no legal nonidentity state changes only one original cubie. Hence 19 <= b_r^(1) <= 20.
3. Each 19-sensor candidate installs all edges and omits exactly one corner c. As every nonidentity difference support has size >= 2, the selected support has size <= 1 iff the full difference support is exactly {c,c'} with c' another corner.
4. Proper rotations are transitive on the eight corners and preserve B_r. Existence of ANY pure two-corner difference support therefore makes EVERY 19-sensor layout fail; absence makes all eight layouts work.
5. For symmetric HTM word metric, B_r^(-1) B_r = B_(2r), by midpoint splitting. Under the consistent original-cubie permutation convention, D(x,y) is the support of the relative group element. Thus a pure-two-corner difference occurs in B_r iff L_CC <= 2r. QED.

**Consequences.** Whether b_7^(1)=19 or 20 is equivalent to whether a pure-two-corner group element has length <=14. Either all eight 19-tag candidates work or none do. Once 20 is required, it stays required for larger radii. L_CC is NOT the same as L_2: the existing 13-HTM two-EDGE witness does not settle it.

**Independent structural cross-check.** Cube graph Q3 has eight vertices, twelve edges. Its line graph L(Q3) has twelve vertices, 24 adjacent-edge pairs, degree four. A maximum matching in Q3 has size four, so alpha(L(Q3))=4 and vertex cover number eight. This graph theorem alone does not verify the physical 13-HTM witness; physical source replay is an explicit prerequisite.

**Evidence boundary.** Previous exact local physical witnesses and B4 support census are inherited. No fresh B5/B7 census, no independent shortest word solver, no remote CI pass. Generic group-base and hitting-set principles are prior art.

**Next proof duties.** Find/certify shortest pure-two-corner HTM support; independently certify B5 positive 16-tag layouts; verify active orientation-bit/trit observation costs separately.

Notion canonical 0.28: https://app.notion.com/p/409ef561cf928193b3d1dc1165ad92ea

GitHub author requirement: do not impersonate the human researcher or add automated co-author trailers.