# WORKING PAPER B — Exact Color Identification and Group-Equivariant Active Observation of the Rubik Cube

**Research draft D0.7 · 2026-11-09 · NOT SUBMISSION-READY.** Mathematical finite-case paper; no claims of human-cognitive mechanisms, RGB device accuracy or HTM motor-cost optimality. The original adaptive horizon is unresolved.

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

For the lower bound, the existing physical P48 certificate enumerates all 10,626 four-edge-facelet omission patterns at the proposed critical 20-read boundary and provides legal state collisions. The released paper must attach the exact script, witnesses and fresh remote execution receipt. The present D0.7 points to the source lineage rather than reproducing that certificate here; therefore do not circulate this document as a standalone proof of the fixed minimum.

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

## 6B. R14-P6.2 — an exact belief quotient preserving policies, not just populations (2026-11-09)

The parity-matched miniature model with three oriented edges and three oriented corners has 648 legal states and 54 freely routable paired-facelet queries. In this deliberately smaller model, all 648 legal *spatial* cubie transformations act on full hidden states, on all paired queries, and on literal two-color observations with exact covariance

    g(B_(q,y)) = (gB)_(gq,y).

Therefore the minimum 648-bit transformed belief is a **sound** canonical representative when accompanied by a transporting group element; any winning query for the representative is carried back to the original state by the inverse transformation. An independent finite checker reconstructed the full 963-node optimal depth-four policy without external certificate dependencies, verified every one of the 648 decoder leaves, checked 153,090 complete successor partition transports, and confirmed both exact Bellman values and inversely transported winning policies for 315 nonterminal beliefs. It inspected 2,007 distinct beliefs and enumerated 49 associated exact group orbits. These are finite proof-audit results in an **abstract miniature**, not numerical progress from the full 20-frame search.

A prior caution is sharpened. P6's two realized 108-candidate belief sets give different child-count partitions at a *fixed* next query, but P6.2 shows they **are related by a legal spatial query permutation**. They therefore do **not** demonstrate different global decision-tree classes. The newer auditable negative control consists of two reachable **36-candidate** beliefs. Across all 54 possible next queries, their multisets of sorted nonempty color-branch cardinalities differ. As this multiset must be invariant under any exact query-permutation/output-relabeling observation isomorphism, these two beliefs are genuinely nonisomorphic. Their optimal depths are not claimed to differ.

See [P6.2 proof, scope and falsification ledger](../../docs/0.28/20261109_R14_P62_FULL_COVARIANT_BELIEF_QUOTIENT.md) and [standalone exact decision-tree covariance court](../../scripts/cuberev-observation/audit_r14_p62_exact_belief_covariance.py). A general sound full-P48 canonical constraint signature and a universal depth-20 or depth-21 certificate remain **OPEN**. The usual generic group-action argument is established prior mathematics, not a standalone originality claim here.

## 6C. R14-P7 / P7.1 — Certificate discovery versus worst-case adaptive decision depth (2026-11-09)

For any known legal state `x`, a separating certificate is a fixed set of paired sensor queries whose observed outputs on `x` exclude every different legal state. This state-dependent object must not be confused with a universally executable online policy. A simple full physical Rubik construction gives **a 20-frame separating certificate for every specified `x`**: read two facelets on eight spatial edge positions, and the non-U facelet on each of the four spatial edge positions occupied by the four U-incident original edge types; use the parallel corner probe to read both ordered facelets from seven spatial corner positions. With advance knowledge of the hidden state, these chosen spatial slots are known. The four remaining edge types are UR/UF/UL/UB and are distinguished by the observed R/F/L/B non-U facelets. This proves only `max_x C_G(x) <= 20` (not equality) and does **not** constitute a 20-frame online strategy.

A fresh independent **3-edge/3-corner** complete model has 648 legal states. For **every** one of these states, the minimum individualized certificate length is **two** paired queries, while the previously proven unrestricted adaptive minimax worst depth is **four**. Per-state minimality was checked by all 54 possible one-query choices and a complete two-query signature census. In the physically motivated *edge-only, known-parity* hard residual models of 4/5/6 distinct types (96/960/11,520 oriented legal states), exhaustive certificate minima for every target are **3/4/6**, versus **previously established** exact adaptive worst depths **5/7/9** (gaps 2/3/3). A complete alternative-state collision ledger proves the certificate lower bounds for all 28+120+792=940 too-short read subsets. A greedy, not minimum, set cover distills those 940 witnesses to reusable alternate-state obstruction cores of 7/12/41. Witnesses store even permutation, even edge flip and all observed color equalities; some six-edge witnesses are alternating matching 3-cycles, double swaps and five-cycles. These are **static**, not online-adversarial, certificates. See [P7 mathematical report](../../docs/0.28/20261109_R14_P7_CERTIFICATE_GAP_AND_MATCHING_CYCLES.md).

**A new complete computational distinction between one- and two-step future awareness:** For all `C(12,4)=495` sets of four remaining edge types, each with 96 known-parity legal states and eight possible color queries, independently evaluate the exact AND–OR adaptive depth and two deterministic online policies. The one-step greedy policy minimizes the maximum immediate child cardinality (with squared-cell and query-index tie-breakers). The **two-step** lookahead minimizes the largest cardinality reachable after a further optimally chosen single probe from each first color branch, with the same tie-breakers. Their complete classification is:

| Worst depth | Full AND–OR optimum | One-step cardinality greedy | Two-step cardinality lookahead |
|---|---:|---:|---:|
| 3 | 72 | 72 | **72** |
| 4 | 369 | 249 | **369** |
| 5 | 54 | 174 | **54** |

Thus the one-step rule wastes a query on **120/495** label sets, and two-step lookahead attains the exact optimum on **495/495**. A concrete one-step counterexample is `{UR,UF,UL,DR}`: 5 versus an exact depth 4. An independent non-bitset, direct-frozenset implementation recomputed all 495 exact minimax values, both policy depths, and replayed the two-step online policy to the exact hidden state on **47,520/47,520** starting states. Selected 960- and 11,520-state difficult five/six-edge residual cases also attain their previously established depths 7/9 under the two-step rule, but these are **two examples, not an all-size generalization**. See [P7.1 complete all-495 certificate](../../docs/0.28/20261109_R14_P71_TWO_STEP_LOOKAHEAD_ALL_495.md).

**Scientific boundary:** This is a finite verified algorithmic property of the **edge-only, parity-conditioned residual game**, not an assertion that two-step greedy remains optimal for the original full 12-edge/8-corner P48 game or all other residual type sets. The general distinction between certificate complexity and deterministic decision-tree complexity is classical; cf. Buhrman and de Wolf (2002), *Complexity Measures and Decision Tree Complexity: A Survey*, DOI 10.1016/S0304-3975(01)00144-X. A global online depth-20 policy or unrestricted depth-21 obstruction remains OPEN.

## 6D. R14-P7.2 — a sharp T-graph failure condition and a necessary scientific correction (2026-11-09)

The 495-item four-edge complete finite census has now been structurally classified under the **48 automorphisms of the original edge-type color graph** `K_{2,2,2}`. The 495 four-label subsets comprise **18** graph-automorphism orbits. For the *specified* original one-step policy that lexicographically minimizes `(maximum immediate child population, sum of squared child populations, spatial query index)`, the exact one-query regret occurs **if and only if** the four source-edge colors form a **T-shaped tree**, namely a four-edge graph with nonzero vertex-degree sequence `(3,2,1,1,1)`. Exactly **three complete orbits**, of sizes **24, 48, 48**, satisfy this criterion. The **120** cases also have a direct independent combinatorial count: six degree-three centers × four choices of the three star edges × five legal pendant extensions. The 18-orbit classification is a consequence of explicit finite color-graph permutations; it must not be confused with a full physical corner chirality or Rubik move-group quotient.

The precise mechanism is exhibited by a **12-state reachable partial belief** for each of the three orbit representatives. In `L={BL,BR,DB,DF}`, after color readings `(slot 0,B)` and `(slot 2,B)`, immediate minimax population ties at four candidates. The old tie-break favors a five-color partition of sizes `(3,4,3,1,1)` with squared total **36**; however the four-state child reached after color `D` cannot be fully distinguished by any one next facelet query, and hence this action has *true remaining depth three*. An alternative query yields the coarser `(4,4,4)` partition with squared total **48**, but each four-state child is separable by a single next sticker; its *true remaining depth is two*. This complete local certificate is supplied as four literal legal oriented-cubie words, with all next sticker colors checked. The new finite structural criterion thereby identifies what is wrong with the old deterministic tie-break, not a global hardness property of T graphs.

**Correction to the prior inference:** Two-step anticipation is **NOT necessary** for this finite family. A fresh full 495-case court for the simpler *one-step* policy that lexicographically minimizes `(maximum immediate child population, number of nonempty color outcomes, sum of squared child populations, query index)` returns the exact AND–OR optimal depths **72/369/54**, with **zero regret across all 495**. The reversed outcome-count tie-break returns the original inferior **72/249/174**. An independent, direct-`frozenset` implementation replays all **47,520** complete initial states for the simpler one-step policy without a single decoding error, establishing the finite result independently of the bitset producer. This observation supersedes any reading of section 6C as claiming a two-level lookahead is required; section 6C's factual two-step zero-regret finding remains correct. The simpler rule achieves known exact depths seven/nine in two specifically identified hard five-/six-edge examples, *not* a complete classification of those larger families.

See [R14-P7.2 finite theorem, failure certificates and correction](../../docs/0.28/20261109_R14_P72_T_TREE_FAILURE_AND_TIEBREAK_REPAIR.md). All minimax claims remain conditional on the **known sector parity, 96-state four-edge residual**, and the previously independently verified exact-AND–OR enumeration. This has no demonstrated implication for a universal physical 20-frame dual-probe Rubik policy, and the overall adaptive 18–21 interval remains **OPEN**. The general color-graph group action and decision-tree theory are established mathematical methods; literature priority for this specialized classification is not asserted.

## 6E. R14-P7.3 — the complete five-edge residual minimax classification (2026-11-09)

The same known-parity single-edge-facelet residual identification problem now has a **complete exact five-piece classification**. For each of all `C(12,5)=792` sets of five distinct original edge types, enumerate the `5!/2 × 2^4 = 960` even-parity/even-flip oriented assignments. Independently of our heuristic conjectures, calculate the exact AND–OR feasibility `Win(X_L,k)` at `k=D_policy(L)-1`, where `D_policy` is the explicit worst-case depth achieved by the simple one-step rule from section 6D. **Every one** of the 792 shorter-budget feasibility calculations returns false; every actual one-step policy returns the right exact singleton across all `792×960=760,320` starting state replays. Thus this is an exact **upper plus matching lower bound** classification, rather than merely two policies agreeing. The resulting worst depths are

| Exact 5-edge residual worst depth | Number of source-type sets |
|---|---:|
| 5 | **12** |
| 6 | **672** |
| 7 | **108** |
| Total | **792** |

Both the simple one-step `(M,K,S,q)` rule and P7.1's two-step max-leaf rule attain those exact minima for **every** five-type set. A second **independent frozenset representation** repeats full exact AND–OR lower and one-step policy upper calculations for each of the **24** symmetry-orbit representatives under the 48 abstract face-color graph automorphisms. These orbits cover all 792 source-type sets; the independent verifier decodes 24×960=23,040 explicit starting states. The complete 792-case primary computation does not rely on the physical validity of all 48 graph automorphisms as full corner-sector transformations. The three independent receipts are [R14-P7.3 proof and executable-court audit](../../docs/0.28/20261109_R14_P73_EXACT_ALL_792_FIVE_EDGE_MINIMAX.md), covering the full 792-row online-policy upper results, complete 792-row exact AND–OR lower result, and the 24-orbit separate checker.

**Boundary:** These are *known-parity conditional residual edge-only* results, not a theorem that the simple one-step rule works for six remaining pieces, all arbitrary partial edge histories, or the original simultaneous **edge+corner** P48 problem. The full cube's adaptive horizon stays `18<=h_adaptive<=21`. The ordinary mathematical tools are prior art; priority of the explicit finite classification still requires a precise independent literature comparison.

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


## 6F. R14-P7.5 — Full exact conditional six-edge residual minimax through signed color transport

The prior P7.4 six-edge experiment classified all 924 source-type six-subsets into 30 source-color graph orbits, replayed all 11,520 states for each representative one-step policy, but had verified exact lower bounds for only twelve representatives. The completed P7.5 court adds full AND–OR `Win(X_L,D-1)=false` negative proofs for the **other eighteen** representatives, including the nine-read instance that initially timed out. Exact Bellman feasibility is now established for **all thirty** representatives. The complete result is

\[

\#\{L:D^*(L)=7\}=20,\quad\#\{L:D^*(L)=8\}=832,\quad\#\{L:D^*(L)=9\}=72.

\]

Here exactness for every one of the 924 distinct label subsets depends crucially on an observation-game isomorphism, not only a graph-orbit list. For a 48-element `K_(2,2,2)` color automorphism `c`, let `tau` permute the **ordered source type indices**, let `epsilon` record each color-relabeling induced reversal of a source type's two-letter order, choose a spatial slot permutation `sigma` of the same parity as `tau`, and a spatial per-slot facelet flip `delta` with `sum(delta)=sum(epsilon) mod 2`. Then an old legal assignment `(p,f)` is mapped to

\[
p'_i=\tau(p_{\sigma(i)}),\qquad f'_i=f_{\sigma(i)}\oplus\epsilon_{p_{\sigma(i)}}\oplus\delta_i.
\]

The new permutation and total flip remain even, and a new spatial slot/facelet query `(i,s)` is related to old `(sigma(i),s xor delta_i)` by observation-color covariance `O_new=c(O_old)`. This transports exact adaptive policies and all outcome children; it is not an assertion that the *literal index-tiebroken one-step greedy* is equivariant. A new standalone checker independently regenerated all **924×11,520=10,644,480** states and verified exact state-set equality under those explicit transformations; a separate transport producer checked all 48 mappings of an entire representative 11,520-state set and 177,408 additional legal samples.

This is a **conditional edge-only residual theorem with known permutation and flip parity**. It does not settle the original coupled full physical 48-sticker dual-sensor adaptive horizon `18<=h_adaptive<=21`, nor imply those 48 abstract face-color automorphisms constitute legal full-cube corner-sector symmetries. The novelty priority of the 924-set exact classification remains to be independently audited against prior literature. Detailed R14-P7.5 theorem and replayable sources are in `docs/0.28/20261109_R14_P75_COMPLETE_SIX_EDGE_924_EXACT_MINIMAX.md`.
