# CUBE-REV 0.28 — R14-P7: Individual Identification Certificates vs Adaptive Decision Trees

**Research date:** 2026-11-09. **Status:** Independent exact finite calculation and independently replayed lower-collision certificates; the 4-/5-/6-edge *adaptive minimax* values are imported as **previously established**, not recomputed in this court. The original full-cube adaptive horizon remains **18 ≤ h_adaptive ≤ 21**. The general concept of certificate vs decision-tree complexity is established prior literature.

## 1. Target invariant and why it matters

Let a finite full-state identification experiment consist of a set of legal states `X` and a set of categorical queries `Q`. For any **known** true state `x`, define an individualized identification certificate

    C_X(x) = min{|S| : S subset Q and for all z in X\{x},
                    there exists q in S with O_q(z) != O_q(x)}.

Let `C(X) = max_x C_X(x)` and `D(X)` be the minimum worst-case adaptive zero-error number of queries. Every valid leaf transcript contains a certificate of its true state, so

    C(X) <= D(X).

The reverse inequality need not hold: the certificate can depend on the initially *unknown* state. In the paired-query cube model, a certificate of `k` frames can read **k edge facelets and k corner facelets**, paired arbitrarily; if an edge or corner slot is repeated, it contributes no extra information. Our finite certificate checker enumerates all distinct subsets of the two sectors of the same cardinality.

## 2. Complete 648-state miniature court: exact 2 vs 4 gap

Independently construct all 3-edge/3-corner signed permutation states with matched permutation parity, flip sum even and twist sum zero modulo 3. There are exactly 648 legal states and 54 possible paired facelet queries (six edge facelets times nine corner facelets).

For each of the **648** target states, enumerate all (edge 2-slot subset, corner 2-slot subset) pairs, and verify at least one chosen pair of two-frame facelet reads uniquely identifies the target against all other **647** legal states. There are 15*36=540 such slot pairings per target; pairing the two selected edge and corner slots in either order is physically permitted in the free-known-turn model. One frame is insufficient for *every* target: the producer checks all 648 targets and all 54 possible one-frame paired queries, while the independent verifier repeats the one-frame test by outcome-bucket census and finds **no singleton bucket** for any query. In particular, the weaker pigeonhole inequality `648>36` alone would not suffice to establish this target-wise claim. The original 648-state exhaustive court gives `D(X)=4` and a complete 963-node optimal decision tree, independently proven in R14-P6.1.

A separate new finite producer counts `C_X(x)=2` for all 648; its independent verifier checks 2-slot certificates exhaustively and should be enhanced to check target-wise k=1 before final proof promotion. This is an **exact-model certificate/decision-depth gap of two** once the per-target k=1 rejection is replayed.

## 3. Real edge residual courts with known sector parity

Consider the established hard residual edge-type sets below with **known permutation parity zero and flip parity zero**. A state has an ordered assignment of each of n distinct edge types into the n spatial cubie locations, together with each local edge orientation. The number of legal states is n!/2 * 2^(n-1). Reading one spatial sticker returns one of six actual colors. Every parity-zero residual state is related to the chosen solved-reference assignment by a legal even spatial permutation plus even flip map (within this conditional sector model); therefore the *individual certificate length* is the same for every target. It suffices to solve exactly for the solved-reference target, not for all 11,520 states separately.

| Remaining labeled edges | Type set | Legal states | Exact target certificate C | Previously established adaptive minimax D | Gap D-C |
|---|---|---:|---:|---:|---:|
| 4 | UR UF UL UB | 96 | **3** | **5** | **2** |
| 5 | UR UF UL UB FR | 960 | **4** | **7** | **3** |
| 6 | UR UF UL UB FR FL | 11,520 | **6** | **9** | **3** |

The standalone Python producer enumerates every orientation-valid even permutation state and every spatial sticker subset of size k (for k=1..2n until it finds a unique certificate). It explicitly reports the first valid **k**-sticker subset, and for **every** (k−1)-sticker subset generates an orientation- and parity-valid alternative state whose observed facelet colors are IDENTICAL to the target. In the 4/5/6 residual courts the counts of such comprehensive negative witnesses are **28**, **120**, **792**, totaling **940** collision certificates. They verify that each listed k really is minimal for the reference state.

## 4. Alternating matching cycles and tiny obstruction nuclei

For each target-alternative state pair, let p be the alternative's assignment of source cubies to spatial positions, and o its flip vector. The relative permutation p is decomposed into disjoint nontrivial cycles. Each p-cycle is an alternating cycle of the two perfect matchings (target assignment versus alternative assignment) in the position/type bipartite graph. The candidate alternative is a **legal** facelet-color collision only if:

- its permutation p is even, so it preserves the known parity;
- its flip sum is even;
- every observed sticker color on the candidate alternative equals the target's color.

The full witness ledger records p, o, the facelet word, the chosen read subset and nontrivial cycles, so these conditions can be checked independently.

On the six-edge court, the lexicographically first valid witnesses for the **792** impossible five-sticker reading subsets have the following concrete cycle characterization: **600 orientation-only**, **65 with permutation cycle lengths (2,2)**, **125 with a 3-cycle**, and **2 with a 5-cycle**. These are witness statistics from the deterministic enumerator, **not intrinsic counts of obstacle types**; choosing different collision witnesses would change the histogram. In the 4- and 5-edge courts the enumerator's first witnesses are all orientation-only.

A greedy (NOT minimum) set-cover distillation compresses the 940 subset-specific witnesses into reusable alternative-state *cores*:

- 4-edge: **7** alternative states cover all 28 impossible two-read subsets;
- 5-edge: **12** alternative states cover all 120 impossible three-read subsets;
- 6-edge: **41** alternative states cover all 792 impossible five-read subsets.

Each selected alternative supplies a set of read patterns for which it collides with the reference; an **independent verifier** exhaustively checks that the union covers every short read subset and that each alternative is a legal parity-/orientation-compatible cubie configuration. These are **compact static certificate lower-bound cores**, not universal adaptive adversary sets. In particular, a single alternative matching one short subset does not imply that a policy can be defeated after adaptive branches without an online invariant; the chosen target itself also depends on the allowed initial prior/oracle.

## 5. The global-cube six-star 20-frame certificate (structural upper bound only)

For any *specified* fully legal cube state x, choose a center face color U and the spatial positions containing the four incident source-edge types UR, UF, UL, UB. Read the **non-U** sticker on each of those four spatial cubies (the visible colors R,F,L,B are unique), and read **both** stickers at each of the other eight spatial edge cubies: 4+16=20 edge facelet readings. All eight fully observed cubies are identified with orientation. The remaining four labels must be precisely UR, UF, UL, UB; their four distinctive non-U observed colors identify and orient each one. The simultaneously available corner probe reads two ordered stickers at each of seven distinct corner cubies (14 reads, padded/repeated to 20 frames). The eighth corner type and orientation follow from remaining type and total twist residue; edge-corner permutation parity is already legal. Therefore the entire full cube is uniquely identified by **20 paired frames**, but **only if the query locations are chosen with advance knowledge of x**:

    forall x in G  exists an x-dependent separating paired-query set S_x with |S_x| <=20.

This is *not* a 20-frame online adaptive strategy. It rules out any attempted universal 21 lower bound from a claim that *some individual x requires more than 20 observations even with x-dependent targeting*. It supplies no tight full-cube certificate minimum (20 is only a general upper bound).

## 6. Next exact research gate

The next falsifiable step should be an **online certificate-discovery** study, not one more symmetry-orbit census:

1. Given an arbitrary **partial legal P48 edge belief**, maintain the set of possible star-center colors and the feasible type-to-position bipartite matching constraints. Design actions optimizing *guaranteed feasible future certificate completions* rather than one-step candidate counts. Include strategy-switch cost when a center becomes implausible.
2. Independently build adversarial matching-cycle witnesses for choices proposed by the policy. A sufficient lower-bound certificate must prove a collision remains along every adaptive path, not merely for every fixed subset.
3. Replay algorithms on the full 648-state court (exact D=4, C=2), then on 96/960/11,520 residual courts. In the latter, compare to previously established exact D=5/7/9 without treating certificate gap as a new adaptive-depth proof.
4. For a full-P48 global claim, preserve both sectors' matched permutation parity and corner twist; the edge-only oracle residual game may be used for sound **lower bounds**, but its policies are not directly global full-cube constructions.

**Novelty caution:** Buhrman & de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288 (2002), 21–43, DOI 10.1016/S0304-3975(01)00144-X, establishes the general conceptual terrain. Here the possibly manuscript-useful contribution is a fully certified **domain-specific quantitative gap** and the state-dependent six-star configuration. It requires additional literature and full physical proof audit before claiming research priority.

## 7. Evidence and executable artifacts

Primary producer: `scripts/cuberev-observation/audit_r14_p7_certificates.py`.
Independent replay: `scripts/cuberev-observation/verify_r14_p7_certificates.py`.
Raw outputs: summary JSON, 940-witness full static collision JSON, and greedy obstruction nucleus JSON, preserved in Drive. GitHub read-only CI should independently replay the JSONs and verify the parent data with a fresh generator execution. The original 20-frame global adaptive problem is **OPEN**.
