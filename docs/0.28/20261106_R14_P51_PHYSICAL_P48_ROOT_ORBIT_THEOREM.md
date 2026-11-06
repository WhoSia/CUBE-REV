# CUBE-REV 0.28 R14-P5.1 — Physical P48 Root Orbit Theorem

Date: 2026-11-06. Model: all legal fixed-centre 3x3 Rubik configurations, 48 mobile stickers, one edge and one corner six-color probe per observation frame, known legal turns without an HTM cost bound. **Local independent P48 computation passed.** This is not a solved 20-frame adaptive horizon.

## Exact physical group action

Let G be the legal Rubik group acting on original-to-spatial sticker permutations x. Let c(i) be the solved sticker face color. Define the output at spatial sticker slot i as c(x^{-1}(i)). The output of a paired edge/corner query q=(i,j) is the ordered pair of such colors.

For any g in G, left multiplication T_g(x)=g*x and the paired-query transformation rho_g(q)=(g(i),g(j)) satisfy EXACTLY O_{rho_g(q)}(T_g(x))=O_q(x). The full prior G is invariant under T_g. An independently constructed BFS using all 18 physical face turns verifies transitivity of the paired-sticker action on all 24*24=576 edge/corner query pairs. Therefore **the first query location can be chosen arbitrarily without affecting the optimal zero-error horizon**.

The legal group is characterized by matched edge/corner permutation parity, zero edge flip sum mod 2 and zero corner twist sum mod 3. These are established facts of cubology, not new theorems. A fresh source-independent P48 geometric implementation generates the 48 slots and legal turns from three-dimensional positions and unit face normals. It reconstructs the earlier 12-element P5 group as three *legal physical* slot permutations: simultaneous odd swaps of two edge and two corner positions; even paired edge flips; opposing corner twists. A lone odd edge-position swap is illegal.

## Full-group reduction of first feedback: 36 -> 3

The 24 proper rigid rotations of the cube induce color permutations on six face colors and preserve the cube group under conjugation. Their orbits on ordered two-color readings are exactly:

- same colors: 6;
- opposite colors: 6;
- adjacent distinct colors: 24.

For any rigid rotation r and the fixed first paired query q0, the joint 576-pair reachability produces a legal h with h(q0)=r(q0). The legal-state bijection T(x)=h^{-1}*r*x*r^{-1} fixes the query location q0 and replaces the observed two colors by their images under the color permutation induced by r. This transports the **entire future paired-query decision tree** and its zero-error terminal predicate. Hence the 36 possible first-response posterior problems have exactly three symmetry orbits (not necessarily identical depths across the three classes).

The initial legal group size is 43,252,003,274,489,856,000. Each of the 36 first-output cells contains exactly 1,201,444,535,402,496,000 states. The equal sizes alone are not used to establish the three equivalences; the entire decision-tree transport supplies the proof.

With D(B) the exact remaining minimax number of paired color queries, the original unknown global optimum satisfies

    h_adaptive = 1 + max(D(B_same), D(B_opposite), D(B_adjacent))

where the three beliefs are representatives of the three paired-color relations after any fixed q0.

## Exact second-query reduction: 576 -> 12

Let H be the subgroup of legal G fixing both initial query facelet slots q0 pointwise. Left action by H preserves each first-output belief, for every possible first color pair. H has exactly three orbits on possible edge facelet positions: the observed sticker (1), its cubie mate (1), other edge stickers (22). H has exactly four orbits on possible corner facelet positions: the observed sticker (1), each of the two other ordered stickers on that corner (1 each), and all remaining corner stickers (21).

The Cartesian products of these edge and corner classes are H-invariant. A set of **32 explicitly constructed legal H generators**, involving matched odd swaps among the previously unobserved cubies, even paired flips, and zero-total-twist rotations, is transitive in each of the 12 product cells. Exhaustive BFS on all 576 query pairs yields exactly 12 orbits, with size histogram:

    {1:6, 21:2, 22:3, 462:1}.

The total is 576. Since orbit cells cannot mix their edge/corner within-cubie distinctions, this is also the full H orbit classification. Thus **at most 12 exact symmetry representatives** suffice for testing possible second query locations after *any* first color response; do not conflate this with optimal full-game termination.

## Proof obligations and limits

This establishes an exact, original-model, first-two-layer state-observation symmetry reduction:

    first paired query locations: 576 -> 1;
    first paired color outcomes: 36 -> 3 equivalence classes;
    second paired query locations after a fixed first read: 576 -> 12.

This is a full legal-cube mathematical structural reduction, not a 20-frame policy construction or impossibility proof. The 12 second query orbits include repeats of observed positions; a later strictly information-increasing action filter may reduce usable options further but is not claimed here. Full cube group action and cubology legality are standard prior art; novelty of the specific orbit census must be assessed against existing literature before a priority claim.

The independent 3D P48 source tests 2,001 deterministic legal turn-prefix states, all three P5 generators, the 12-element group, all 576 paired sensor locations, 24 proper spatial rotations, full-root color relation orbits, and the 32-element generating family for H (32 generators, not a 32-element group). Algebraic proof uses the sticker mapping identities and exact subgroup-orbit classification, not sampling alone.

The project next must use exact partial-color matching-parity completion counts to populate all three root response classes and 12 second-query representatives; then preserve whole successor belief sets through a sound canonicalization and seek a global h<=20 strategy or universal h>=21 obstruction. **Global h_adaptive remains between 18 and 21.**

## Custody

- Independent runnable source: `scripts/cuberev-observation/audit_r14_p51_p48_group_lift.py`.
- Drive Python original: https://drive.google.com/file/d/1cu-k8TX87Yj20vaDEgDD1n4Tg44Ec_Gt/view
- Drive JSON result: https://drive.google.com/file/d/16fA5u5gfZmXEYnqPVSDkNbhJ3KiAASfm/view
- Source SHA256: 44f3d43b3c8c637d889c262700e490306112eb2627d37ec39cde30f199a19bce
- JSON SHA256: e1c5f2936b811c7f2eea17d7f2aa9da3f3bbd67f5ee96bcfcec42277168fa53e
- Read-only remote CI verification is a separate gate.
- Fundamental theorem of cubology, prior-art reference: https://www.sfu.ca/~jtmulhol/permutationpuzzles/puzzles-rc-cubology.html
