# WORKING PAPER B — Exact Color Identification and Group-Equivariant Active Observation of the Rubik Cube

**Research draft D0.1 · 2026-11-06 · NOT SUBMISSION-READY.** Mathematical finite-case paper; no claims of human-cognitive mechanisms, RGB device accuracy or HTM motor-cost optimality. The original adaptive horizon is unresolved.

## Abstract

We consider zero-error identification of an arbitrary legal 3×3×3 Rubik configuration by two categorical sensors, each returning the color of one facelet: one edge and one corner. Between observation frames, a policy may execute a known finite sequence of legal face turns and use previous colors to select subsequent readings. Under an observation-frame objective that does not charge the intermediate turns, the exact minimum for a *preset* observation schedule is 21 frames, whereas the optimal unrestricted adaptive horizon is currently bounded between 18 and 21. We give precise finite verification dependencies for this result and for the adaptive decision trees arising after eight completely observed edge positions. We prove an exact full-cube group-equivariance reduction of the initial decision tree: all 576 paired initial spatial facelet queries are equivalent; all 36 ordered initial color responses are equivalent under legal independent original edge- and corner-label transformations; and the pointwise stabilizer of a fixed first queried facelet pair has exactly 12 orbits on the 576 possible second paired queries. An independent 48-sticker geometric engine checks the legality and covariance of the transformations. A parity-tracked matching dynamic program reproduces the full cube group cardinality and exactly enumerates the 36 possible second responses for the three representative first-color relation classes and twelve second-query stabilizer orbits. These reductions are exact but do not settle the adaptive 18–21 horizon. We identify the additional requirements for a sound global mixed-prefix decision-tree quotient and distinguish our case-specific finite computations from existing group-action and adaptive distinguishing-sequence theory.

**Keywords:** Rubik group; exact state identification; adaptive distinguishing experiment; categorical observation; group action; zero-error decision tree; parity-constrained matching.

## 1. Model and theorem targets

Let G be the legal 3×3×3 cube group with fixed centers. Every state x is a permutation of 48 individually identified moving facelets, partitioned into 24 edge and 24 corner facelets. Denote the solved color of original facelet a by c0(a) in the six-element face alphabet F={U,D,R,L,F,B}. The physical state maps original facelets to spatial positions. Consequently the sensor at spatial facelet i observes

    c_x(i) = c0(x^{-1}(i)).

A paired observation q=(i,j) with i an edge facelet and j a corner facelet gives O_q(x)=(c_x(i),c_x(j)). A policy chooses a legal turn word w_t based on its observation history; the observable facelets under the word are known, and the fixed physical probes therefore implement paired queries of initial spatial facelets. The induced two-sensor joint orbit of 576 pairs is transitive. We optimize **number of frames** rather than total face-turn count, action duration, motor constraints or entropy under a prior.

Define h_fixed as the smallest number of frames in a policy whose *query plan is independent of colors*. Define h_adaptive as the smallest worst-case number of frames in a deterministic color-feedback policy that reconstructs the entire original state, not merely its equivalence class. The underlying legal state count is

    |G| = (12! * 2^11) * (8! * 3^7) / 2
        = 43,252,003,274,489,856,000.

The inequality and proof dependencies established by the research archive are

    h_fixed = 21,                     18 <= h_adaptive <= 21.

**Evidence boundary:** the fixed lower bound uses physical collision certificates across all 10,626 relevant omission masks; it is not implied by the crude |G|<=36^h information inequality. The adaptive lower bound and fixed upper bound have different proof mechanisms. This manuscript must not extrapolate h_adaptive=21 from any restricted prefix obstruction.

## 2. Prior mathematics and case-specific contribution

The legal-cube characterization by matching edge/corner permutation parity, vanishing total edge flip modulo 2, and vanishing total corner twist modulo 3 is classical. Standard group action, posterior transport and Bellman decision-tree invariance are not new. Adaptive distinguishing sequences and identifying experiments for finite-state machines have established independent literatures (e.g. Lee and Yannakakis, 1994). A prior MIT two-RGB-sensor cube robot report demonstrates that the idea of scanning a cube through turns with limited hardware is not new. Our six-valued categorical probes, unbounded known legal routing and entire legal group are a specifically defined idealized mathematical model, not a replica of an error-prone physical RGB system.

The possible case-specific scientific contribution is: (i) a *complete exact* preset two-probe facelet-color observation horizon with separately replayable physical proof certificates; (ii) a precise parity-coupled local feedback advantage; and (iii) the physically valid stabilizer and source-label quotient geometry for full-cube active decision trees. Independent priority search for an equivalent full legal model remains a release condition.

## 3. Preset 21-frame theorem (previously obtained finite result)

**Theorem 1 — fixed-frame optimum, evidence dependent.** In the stated six-color paired-facelet model, h_fixed=21.

For the upper bound, the existing P48 construction reads 21 distinct initial spatial edge facelets and fourteen distinct initial corner facelets (two at each of seven corner positions, using corner chirality and the corner-twist constraint to infer the eighth). Every queried pair is reachable using a known legal turn word. The reconstruction uses actual observed colors and known legal turn actions, not ground-truth cubie labels. Total 21 frames; thirty-five *distinct* facelet positions are read, even though both sensors output 42 symbols across 21 frames.

For the lower bound, the existing physical P48 certificate enumerates all 10,626 four-edge-facelet omission patterns at the proposed critical 20-read boundary and provides legal state collisions. The released paper must attach the exact script, witnesses and fresh remote execution receipt. The present D0.1 points to the source lineage rather than reproducing that certificate here; therefore do not circulate this document as a standalone proof of the fixed minimum.

## 4. Conditional adaptive feedback and restricted lower bounds

After sixteen edge readings fully identify eight spatial edge cubies, the remaining four source labels form one of C(12,4)=495 sets. With corner parity and global flip parity known, each residual set induces exactly 96 legal oriented assignments. Exact conditional feedback trees give adaptive depths 3,4,5, with 72,369,54 label sets, respectively; nonadaptive depths differ on 216 label sets. The 54 five-read types comprise six four-stars and 48 triangle-with-pendant patterns in the K_{2,2,2} face-color graph.

An adversarial online completion leaves a hard set of four labels unread whenever the first 16 edge frames exactly complete eight spatial positions. Analogous hard residual games show impossibility of a 20-frame guarantee for policies whose first twelve reads complete six spatial edges, or first fourteen complete seven. These are **policy-class** impossibility theorems: an unrestricted policy can distribute partial edge color measurements over more positions, and none of the three arguments excludes that essential case.

## 5. Exact full-group initial decision-tree quotient

**Lemma 2 — free-slot query covariance.** For g in the legal cube group and hidden state x, put T_g(x)=g x. For every pair of spatial facelet locations q, define gq by applying g to both locations. Then O_{gq}(T_g x)=O_q(x), since (gx)^{-1}(gq)=x^{-1}q. Because the full prior is all of G and the physical paired-slot orbit has 576 elements, the first paired-query choice is arbitrary up to an exact zero-error decision-tree isomorphism.

**Lemma 3 — independent legal source-color relabeling.** For a proper rigid cube rotation r, let h_E(r) be its 48-sticker permutation restricted to the 24 *original edge* facelets, acting trivially on original corner facelets; define h_C(r) conversely. Exact legal cubie invariants show all 24 corner-restricted rotations h_C(r) are legal, and exactly twelve edge-restricted rotations h_E(r) are legal. The twelve edge restrictions and all 24 corner restrictions separately act transitively on the six face-color labels. Therefore 288 independent sector products h_E h_C are legal cube states, and each acts on the hidden original-source labeling by x -> x(h_E h_C)^{-1}.

Let phi_E and phi_C be the face-color permutations induced by the chosen edge and corner rotations. For all hidden legal states and all paired spatial queries,

    O_q(x(h_E h_C)^{-1})
        = (phi_E(O_q(x).edge), phi_C(O_q(x).corner)).

Thus all 36 possible ordered first-frame two-color results belong to **one** posterior decision-tree equivalence class. This is stronger than the 3-orbit classification under rotations of the entire cube: same, opposite, adjacent colored face pairs are not inequivalent once independent legal sector relabeling is admitted. A future policy transports through the source-label bijection and inverse color permutations. The entire zero-error Bellman recursion, not merely posterior cardinality, is preserved.

**Lemma 4 — second-query stabilizer orbits.** Fix the initial query q0=(i0,j0). Its legal group pointwise stabilizer H={g in G:g(i0)=i0, g(j0)=j0} preserves every first-result-conditioned belief. The edge-facelet H-orbits have sizes 1 (i0), 1 (its same-cubie mate), 22 (other edge facelets). The corner-facelet H-orbits have sizes 1 (j0), 1 and 1 (the two other stickers on its oriented corner), and 21 (other corner facelets). All twelve Cartesian products are single orbits, certified by thirty-two explicit legal generators acting transitively in each cell. The exact orbit-size histogram of all 576 possible second paired queries is {1:6,21:2,22:3,462:1}.

**Theorem 5 — exact initial quotient.** There exists a fixed canonical first paired query q0 and a fixed canonical first-color response y0=(U,U) such that the full adaptive problem has the exact form

    h_adaptive = 1 + D(B(q0,y0)),

with D the remaining worst-case paired-query Bellman depth. At the next decision node only twelve representatives of the H-orbits need be tested. Equivalently, the exact initial combinatorial choice structure reduces from 576 root queries, 36 first color outcomes, and 576 second query locations to one canonical root query, one representative first response, and twelve second query classes. **This does not solve D(B(q0,y0)).**

## 6. Two-frame posterior census and its limits

An independent 3D P48 facelet engine and exact parity-constrained matching DP compute all 36 possible second color branches for each of the 12 second-query orbits and three first response representatives from the weaker rigid-rotation relation classes (36 evaluated families). All branch counts sum to |G|/36=1,201,444,535,402,496,000. The minimax *immediate maximum posterior cardinality* among possible second paired queries is 41,608,468,758,528,000, attained by reading another edge position and another corner position. This measurement is not the minimal future decision depth, so no horizon claim follows. The full 36-row raw JSON census is preserved in Google Drive.

## 6A. R14-P5.4 — exact mixed-prefix stabilizer orbit formula (2026-11-06)

After reading one spatial facelet on each of `k` distinct original-spatial edge positions and `l` distinct corner positions, consider the LEGAL state-action subgroup fixing **every previously queried spatial facelet slot pointwise**. With `0<=k<=10, 0<=l<=6`, its orbit count on all 576 possible next paired-query locations is

    N(k,l)=(2k+1)(3l+1)   except   N(10,6)=400.

The exception is one extra orbit beyond `21*19=399`, caused by the matching edge/corner permutation-parity condition when each sector has exactly two untouched cubies. In a natural mixed two-frame prefix `k=l=2`, there are **35** third-query orbits, not 576; orbit sizes are `1:24, 18:4, 20:6, 360:1`. A P48 legal-generator and 576-pair BFS certifies **all 77** valid `(k,l)` profiles including the exceptional 400-orbit case. See [exact proof and declared P48 geometry dependency](../../docs/0.28/20261106_R14_P54_MIXED_PREFIX_STABILIZER_ORBITS.md). This orbit theorem is a safe subgroup action-pruning result, not a maximal color-observation belief quotient, not a minimax-depth calculation, and not a literature-first priority claim.

**Specific prior-art warning.** A public 2015 problem about minimal facelets needed to determine a scrambled cube already discusses sticker-color scanning and gives a 39-sticker *upper bound*, explicitly not an optimum; a 2016 correction observes that 14 selected corner stickers can determine the last corner. The original question and informal answers are not a peer-reviewed proof of our fixed paired-probe 21-frame theorem, but they establish that both sticker minimization and last-corner parity deduction have prior discussion. See https://puzzling.stackexchange.com/questions/22848/minimum-number-of-stickers-to-inspect-in-a-rubik-cube-to-define-a-scrambled-posi . In the manuscript, distinguish their sticker count (which includes center-color calibration) from our 21 **paired frames** and 35 distinct moving facelet slots with fixed known centers. Do not present the general idea of inferring an unread corner as new.

## 7. Verification contracts

P48 geometry is regenerated from 3D lattice positions and unit face normals with eighteen legal turns, not imported from an archived 54-facelet table. The computation checks 2,001 legal random turn-prefix states, the 576 joint orbit, 24 proper cube rotations, all twelve P5 small symmetry elements, and twelve exact second-query orbits. The independent source-label test enumerates 12x24 legal sector relabelings and 31,104 actual P48 color covariance checks. The matching DP counts posterior completions without enumerating 43 quintillion legal cube states. All independent source files and execution results are preserved as original bytes in Drive, with SHA-256 re-read verification.

A mathematical proof of h_adaptive<=20 must give an executable decision-tree policy with a decoder and proof that every legal state reaches a singleton within the allowed frames. A proof of h_adaptive>=21 must give a sound universal lower certificate over **all mixed-prefix adaptive policies**, not merely fully read edge-cubie prefixes. A failed search or unverified CI is not such a certificate.

## 8. Research priority and broader significance

The immediate task is to canonicalize partial facelet-color histories under both the left legal spatial-group action and right legal source-label automorphisms, then preserve all query successor sets with exact parity-coupled edge/corner matching constraints. The first two layers are now fully normalized; the gap is the general mixed-prefix Bellman decision tree. We will seek a cross-system theorem only when a nontrivial invariant or obstruction survives changes of finite group, observation alphabet or sensor partition; the elementary group-equivariance argument alone is not a newly discovered general theory.

## Provisional references and evidence

- The Fundamental Theorem of Cubology, SFU course note: https://www.sfu.ca/~jtmulhol/permutationpuzzles/puzzles-rc-cubology.html (standard legal-cube characterization).
- Lee, D., and Yannakakis, M. (1994). *Testing finite-state machines: State identification and verification*. IEEE Transactions on Computers 43, 306–320, DOI 10.1109/12.272431 (prior adaptive distinguishing-sequence theory).
- Hierons, R. M., Jourdan, G.-V., Ural, H., and Yenigun, H. (2008). *Using Adaptive Distinguishing Sequences in Checking Sequence Constructions*. ACM SAC, DOI 10.1145/1363686.1363850.
- MIT 6.111 (2017) *Rubik's Cube Solving Robot*, https://web.mit.edu/6.111/www/f2017/projects/jeswiezy_Project_Final_Report.pdf (two RGB sensor robot prior art; distinct error and hardware model).
- Project mathematical sources: 
  - https://github.com/WhoSia/CUBE-REV/blob/research/current/docs/0.28/20261106_R14_P53_ALL_ROOT_RESPONSES_EQUIVALENT.md
  - https://github.com/WhoSia/CUBE-REV/blob/research/current/scripts/cuberev-observation/audit_r14_p51_p48_group_lift.py
  - https://github.com/WhoSia/CUBE-REV/blob/research/current/scripts/cuberev-observation/audit_r14_p52_two_frame_p48_posteriors.py
  - https://github.com/WhoSia/CUBE-REV/blob/research/current/scripts/cuberev-observation/audit_r14_p53_source_label_automorphisms.py

**Release gate:** check novelty against original work on cube probing and automorphism quotients; independently verify CI and all positive/negative fixed-21 physical certificates; complete error bounds, executable figure/table generation, publication venue format and authorship/ethics declarations. Do not call this draft accepted, peer-reviewed or submission-ready.
