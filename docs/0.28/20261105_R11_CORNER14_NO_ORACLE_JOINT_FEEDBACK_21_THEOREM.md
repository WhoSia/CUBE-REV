# CUBE-REV 0.28 — R11: Fourteen Corner-Color Reads, Oracle Elimination, and a Genuine Joint 21-Frame Adaptive Policy

**Date:** 2026-11-05. **Research director's verdict:** A rigorous construction and lower-bound collision proof for a separate corner-only channel, combined with R9's exact residual edge decision tree to give a full-cube zero-error adaptive procedure with at most 21 joint two-color observation frames. This **does not reduce** the previously known global worst-case bound 18–21. CI must be explicitly checked; do not label pending queued GitHub Actions as PASS. No human cognition result has been obtained.

## Why this attacks rather than evades the original problem

R9 and R10 proved physically meaningful color-feedback gains but assumed the entire true corner state was given for free. The hard R11 task is to remove that oracle *without adding extra observation frames*, retaining actual legal turn words and correct full 48-sticker reconstruction. Instead of polishing a convenient earlier paper, we derive an exact corner information theorem and insert it into the full adaptive physical policy.

## Lemma 1 — two corner facelet colors are exactly an oriented-cubie identifier

Fix any one of the eight spatial corner positions of a standard fixed-centre, legally oriented 3×3×3 Rubik group, and any two distinct facelet slots at that position. Each of the 8 original corner labels has 3 cyclicly admissible orientations. The 24 combinations give **24 distinct ordered pairs of six face colors** at the chosen two slots. This is a geometric chirality restriction: the cyclic corner orientation excludes the reflected alternative which would otherwise conflate the two endpoints of a color edge. The 3D P48 geometry checks this bijection for all 8 destinations and all 3 choices of the omitted facelet slot, 24 bijections in total.

Therefore two readings at a known corner *spatial position* determine both its original cubie identity and its actual orientation, without access to any edge or corner identity sensor.

## Theorem 2 — exact nonadaptive corner-only universal minimum 14

**Upper bound.** Query two spatial facelets on each of seven distinct corner positions: 14 single six-color observations. Lemma 1 identifies the source label and cyclic orientation in each of the seven positions. The eighth original corner label is the only unused label; its orientation is fixed by the legal **corner twist sum = 0 mod 3**. Thus all 24 corner sticker destinations are uniquely reconstructed, independent of any edge observations or edge permutation parity.

**Lower bound against every fixed 13-read corner-only schedule.** Any selection of at most 13 spatial corner facelet slots leaves at least two corner positions A and B with at most one observed slot each; otherwise seven positions would require 14 reads. Take two *distinct* original corner labels X and Y sharing an original color c (for example any two containing U). Put X,Y at A,B, and orient each so that, if a facelet is observed at that destination, it shows c. Swapping X and Y can preserve those selected colors. When both weak positions show c, the sum of their physical corner twists is unchanged on swapping because if the index of c in original label X is q_X and its chosen slot at A is k_A, then the required cyclic shift is t_A(X)=k_A-q_X mod 3. The sum t_A(X)+t_B(Y) equals t_A(Y)+t_B(X) mod 3. If one position is unobserved, its cyclic shift can be adjusted freely to match the same total. Adjust an identical unchanged third corner's orientation to make total twist 0 in both states. The two full corner states differ by the transposition X↔Y and therefore have opposite corner-permutation parity, but **both extend to legal full cube states** by choosing the edge permutation parity accordingly (edge flip sum 0 can be retained). Since this lower bound concerns corner colors ONLY, edges are not exposed.

This yields the **exact fixed/nonadaptive corner-only observation minimum of 14** under freely addressable spatial corner facelet slots:

\`h_corner_nonadaptive = 14.\`

Do **not** infer an adaptive-corner lower bound of 14 or a dual-sensor full-cube lower bound: edge sensor observations could distinguish the two full-state witnesses, and feedback could alter corner query positions.

**Executable probes:** [R11 14-read joint-probe decoder](../../scripts/cuberev-observation/audit_r11_corner14_no_oracle.py) enumerates the 24 orientation signatures for every two-slot selection, independently reconstructs the true corner sticker mapping from the 14 measured colors, and physically replays 262 B2 states plus longer sequences through legal no-reset turn words. [R11 13-read adversary](../../scripts/cuberev-observation/audit_r11_corner13_collision_witness.py) builds physically legal indistinguishable pairs for reproducibly sampled schedules and checks corner/edge permutation parity as well as corner twist and edge flip constraints. The mathematical argument covers **all** ≤13 fixed schedules; the randomized smoke confirms only the sampled witness implementation.

## Theorem 3 — complete corner-oracle elimination for the R9 staged adaptive policy

The R2 geometric joint-probe orbit includes all \`24 × 24 = 576\` edge-facelet/corner-facelet target pairs. Therefore the two stationary six-color sensors can simultaneously read **any selected initial spatial edge facelet and any selected corner facelet** through known legal 18-HTM turns, with no additional observation frame and no free reset between frames.

**Constructive full legal cube algorithm:**
1. During the **first 14 joint frames**, fully read seven spatial edge cubies (14 edge colors) while querying two spatial facelets in each of seven corner positions (14 corner colors). By Lemma 1 and the corner twist sum, the full corner state is known **at frame 14**, without an oracle.
2. During frames **15 and 16**, read the two facelets of an eighth edge position, while the corner sensor can read any convenient legal corner slot.
3. At frame 16, eight original edge labels and their flips are identified by their pairs of colors. Four source labels remain but are not yet assigned to the four unobserved edge positions. The **actual decoded corner permutation parity** and the eight observed edge assignments determine the required remaining four-label permutation parity. The known prefix edge flips and global flip-sum parity determine the remaining four-flip parity. No true-state oracle is used.
4. Use the exact R8/R9 minimax decision tree for this four-label set and parity pair: there are 96 admissible completions. Choose each later edge slot from the observed colors, pairing it with any convenient corner slot; every pair is reachable with known legal 18-HTM actions. At most five further frames identify the unique residual edge configuration.
5. Combine the independently recovered 24 original corner sticker positions with all 24 original edge sticker positions to return the exact full P48 permutation. The final truth comparison, when used by tests, is *after* the decoder, not an input to it.

**Consequences:** The policy is fully adaptive (edge continuation depends on colors) and reconstructs **every legal full Rubik state** within \`16 + 5 = 21\` simultaneous two-probe color observation frames **without a free corner oracle**. A previously verified 21-frame nonadaptive full-cube policy already exists, so this theorem does NOT improve the guaranteed worst-case upper bound. It does, however, lift a *feedback-dependent variable-length plan* from the free-corner model into the true physically coupled two-color sensor model. For 72 possible remaining four-label sets the guaranteed residual budget is 3, for 369 it is 4, and for 54 it is 5; these counts are independent of the correctly inferred parity pair. Some branches may terminate even earlier.

The accompanying [R11 full joint decoder](../../scripts/cuberev-observation/audit_r11_full_cube_joint_feedback_21.py) actually reads both categorical probes after each legal relative P48 turn, reconstructs corners after 14 reads, obtains the eight known edge labels/flips from the first 16 edge reads, computes both required parity bits, runs the R9 adaptive decision tree and reconstructs the **complete** sticker permutation using only measured colors. It checks B2 (262 states), long-turn controls and legal residual edge states. This is a constructive algorithmic proof by the independent lemmas and exact finite R9 certificates; all paper claims must retain an independent CI and mathematical audit requirement.

## An additional solved-reference corner/parity census

The independent 3D-P48 ordered corner-color model exhausts these **state-dependent** missing-facelet masks, initially for solved corners:

| Reads | Omitted slots | Masks | Singleton given no edge parity | Singleton given correct edge parity |
|---:|---:|---:|---:|---:|
| 20 | 4 | 10,626 | 10,590 | 10,626 |
| 19 | 5 | 42,504 | 41,784 | 42,504 |
| 18 | 6 | 134,596 | 127,796 | 134,528 |

Every ambiguous result is an alternate corner arrangement satisfying the twist sum; the 'given edge parity' column restricts permutations to the correct parity class. These are solved-reference **local certificates** and cannot be interpreted as every arbitrary fixed readout schedule globally identifying corners. In particular the 14-frame construction uses a *specific two-facelets-at-seven-positions pattern* whose universal correctness follows from the bijective individual corner signatures.

The 20-read missing-four no-parity ambiguity occurs only when the missing mask spans exactly two positions with two omitted facelets each and compatible original-corner colors. 19 reads require not all arrangements unless edge parity is known. These facts specify how the shared edge–corner permutation parity can compensate for corner-only ambiguous measurements, but the 14-frame route shows that corner reconstruction can avoid this coupling entirely in the staged policy.

## R11 remaining hard limits

- Exact full-group adaptive two-probe horizon remains \`18 ≤ h_adaptive ≤ 21\`. The R11 full-cube 21 upper construction does **not** close this gap.
- An adaptive **20-or-fewer** guaranteed construction would have to do better than the initial-16-full-edge staged policy in its worst-case 54 residual graph classes, or exploit additional joint structure earlier. Simply selecting corner readouts more cleverly cannot reduce the 54-class *edge-only* lower bound when the corner state is already granted to the adversary.
- The full 17-read Hall bound and 18-read stronger adversarial routes require further work on edge permutation/flip constraints and the global feedback tree.
- Real human working memory, response times, motor execution and the causal effect of history have not been measured; all observation/readout costs here are precise mathematical proxy quantities.

## Research custody

GitHub sources are authored/committed through the authenticated human \`WhoSia\`, no GitHub Actions bot writeback. Read-only CI must print PASS before marking remote results verified. P7 exact active-set manifest must include every newly added source/report. Notion holds semantic claims and limitations, Drive holds irreplaceable raw data rather than generated verification code. Do not assume private naturalistic reconstructions provide matched human behavioral comparisons: the previous 0.21 strict matched-state/stage/prior-action support count was zero.
