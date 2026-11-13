# CUBE-REV 0.28 R14-P8.34 — The entire static identifying-family saturates at B7

Date: 2026-11-13. Model: **persistent original-cubie sensors**, each measuring full original corner/edge position and orientation. Not the paired 6-color spatial facelet scheme of the full adaptive experiment.

## Statement

Let \(G\) be the fixed-center legal Rubik cube group, let \(B_r\) be the closed radius-r symmetric 18-HTM ball, let \(C,E\) be the eight original corners and twelve original edges, and define
\[
\mathcal I(X)=\{S\subseteq C\sqcup E:\pi_S|_X \text{ is injective}\}.
\]
Then
\[
\boxed{
\mathcal I(B_7)=\mathcal I(G)=
\{S:\lvert S\cap C\rvert\ge7 \ \text{and}\ \lvert S\cap E\rvert\ge11\}.
}
\]
In particular, for every \(r\ge7\), \(\mathcal I(B_r)=\mathcal I(G)\), which is stronger than \(b_r=b_G=18\).

**Proof.** The P8.30 physically verified two-B7-state witnesses realize **every** one of the 28 two-corner supports and 66 two-edge supports. Thus if a set \(S\) omits any two corners or any two edges, it fails to identify even \(B_7\). This forces \(S\) to retain at least seven corners and eleven edges. Conversely, a legal cube is uniquely determined by the pose of all but at most one corner and one edge: the remaining original locations are fixed by bijective corner/edge permutations and remaining orientations by the sum-zero corner twist mod three and edge flip mod two. Therefore every such \(S\) identifies all of \(G\). The inclusion \(\mathcal I(G)\subseteq\mathcal I(B_7)\) follows from \(B_7\subseteq G\). QED.

The total number of identifying sets at and beyond B7 is
\[
\binom{8}{7}\binom{12}{11}+\binom{8}{8}\binom{12}{11}
+\binom{8}{7}\binom{12}{12}+\binom{8}{8}\binom{12}{12}
=96+12+8+1=117.
\]
This includes 96 sets of size18, 20 sets of size19, and the full20 set.

## Complete quantitative comparison B6 vs B7

The earlier P48 physically certified B6 full family, supported by **fresh 41-target P8.33 MITM** positive-side re-execution and 872 negative physically witnessed support masks, has exactly:
- 156 size16, 672 size17, 174 size18, 20 size19, 1 size20 identifying sets: **1,023 total**.
- B7 has 96 size18, 20 size19, 1 size20: **117 total**.
- Lost between B6 and B7: 156 size16 + 672 size17 + 78 size18 = **906 designs**.
- All 156 sixteen-tag B6-optimal families first fail at B7. So do all 276 inclusion-wise minimal seventeen-tag B6 designs; their B7 failure is already implied by their total tag cardinality. The 19/20 tag families survive.

The quantitative assertion is an application of existing exact group observation constraints, not a novel abstract group theorem. Relevance: the **entire zero-error sensor-design feasibility family** becomes globally saturated by radius seven, before the cube's physically reachable-state set reaches the full group.

## Executable proof and provenance

[R14-P8.34 self-contained census](../../scripts/cuberev-observation/audit_r14_p834_exact_static_family_saturation.py) replays P48 physical B6 negative supports via \`verify_b6_complete_4845_p48.py\` and all P8.30 physically derived pair-collision supports via its independent 48-sticker coordinates, then exhaustively evaluates every 20-bit subset. It tests 872 masks for B6, 94 masks for B7, and uses a deterministic upward-closure transform to check all **1,048,576** candidate sensor families. For every subset, B7 support avoidance equals the whole-group elementary \((\#C_{\mathrm{selected}}\ge7)\land(\#E_{\mathrm{selected}}\ge11)\) criterion.

**Actually verified GitHub Actions run:** [R14-P8.34 43350675032](https://github.com/WhoSia/CUBE-REV/actions/runs/43350675032), complete SUCCESS, with exact expected-count assertions and artifact upload. [P8.34 receipt ZIP](https://drive.google.com/file/d/1LzA07XNgexLT7nYJmCowjd3hB5-2Ei1Y/view), SHA-256 \`26e9f46fc442adae57ba5914cd65d4c213a2682c5b540c72d9a2282236797256\`, 728 bytes, two files; after complete Drive upload, actual re-download has byte-for-byte identical ZIP SHA and \`cmp\` PASS. JSON receipt SHA-256 \`4c8c1d077754b0de769ba2bb34a49311c87e08a7ebbda8c6f244a21199999ec4\`.

**Dependencies and limits:** The negative B6 support masks are genuinely recomputed from physical P48 word witnesses; the assumption that all 872-mask-free B6 layouts are positive depends on the separately [executed P8.33 41-target radius12 exclusion](https://github.com/WhoSia/CUBE-REV/actions/runs/43349579675) and the explicit 156-layout to 41-target symmetry quotient from its P48 generator. P8.34 does not run C++ MITM itself, nor a full B7 state-space BFS, nor a 19-frame adaptive categorical-color search. The latter is still OPEN. The entire family saturation conclusion is a combinatorial corollary of physically certified pair supports and the legal group constraints, not a general statement for all reversible group actions.

## Editorial decision

Version [C0.3 integrated single-paper candidate](../../papers/0.28/ONE_PAPER_EXACT_RUBIK_IDENTIFICATION_CONSOLIDATION_C03.md) elevates the complete family saturation and the 906-design collapse to a central theorem, while preserving the **different observation protocol** in the second color-feedback result \((h_{\rm fixed}=21,\,18\le h_{\rm adaptive}\le20)\). It does not compare numeric sensor count with observation frames; A D0.5, B D0.8, C0.1 and C0.2 source manuscripts remain preserved.

**Next high-value original research:** the unrestricted 19-frame posterior minimax decision, exact prior-art screening for model-equivalent finite cube sensor results, and a reviewer-readable compact physical proof-certificate appendix. The 2026-10-30 historical B5 source ZIP is still missing, but the modern archive-independent P48 physical proof line was rebuilt and executed in P8.33.
