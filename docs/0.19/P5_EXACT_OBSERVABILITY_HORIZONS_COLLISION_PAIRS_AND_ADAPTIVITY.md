# CUBE-REV 0.19 — P5: Exact Observation-Horizon Profile, Collision-Pair Geometry, and Adaptive Separation

**Scope:** Physical 3x3 Rubik cube's sticker-derived 18 HTM edge actions; tracked UR edge starts with intrinsic flip zero in any of twelve edge slots. A fixed word of length L emits its orientation bit after every move; a source requirement A is distinguished if the L-bit history is injective on A. The **frozen** source family R has 1192 subsets: all 220 triples, 492 four-sets intersecting at least two of the three edge-position groups, and 480 admitted five-sets. Unit dictionary cost M*(L) counts selected *experiments*, not physical turns. Different known A may select different words in a dictionary.

## Exact profile, including clearly unfinished cases

| L | Dictionary M*(L) | Status |
|---|---|---|
| 0,1,2,3 | infinite | Analytic physical F/B confinement theorem (P1) |
| 4 | 34 | 0.18 independent physical DRUP-certified optimum |
| 5 | integer 6..8 | Exact physical rational LP 16/3; physical 8 upper; k7 still open |
| 6 | integer 3..4 | Three-word lower from L7 monotonicity; physical four-word upper |
| 7 | **3** | Physical full rank <=10 by 114852864-word residual enumeration + two-word collision theorem; physically replayed three-word cover |
| 8 | **2** | Hamming/four-cut + F/B confinement + 179830784-word residual enumeration rule out rank12; physically replayed two-word cover |
| 9 and every later L | **1** | One physically replayed nine-HTM universal observation word; prefix-memory monotonicity |

This is an exact profile **except L5 and L6**, and is explicitly only for this frozen observation and source-family ontology. At 9 turns a *single predetermined word* identifies all 12 starts. Do not confuse this with human speedsolving, FMC or full cube-state determination.

## General analytic fixed-word geometry

Each physical HTM map decomposes as (p,b) -> (sigma_a(p), b XOR f_a(p)), with p one of 12 edge slots and b intrinsic edge orientation. Incremental observations d_i = observed_bit_i XOR observed_bit_(i-1) induce exactly the same initial-state partition as complete cumulative histories. Each nonzero physical f_a is an indicator of precisely four edge positions (the F or B face edge slots), and only F,F',B,B' may change the bit.

**Four-cut Hamming-mass bound.** If a length-L word contains q flip-capable quarter turns, its q-bit increment signatures across the 12 starting slots contain exactly 4q ones in total, because preceding physical slot permutations transport each four-slot cut bijectively. For q<=3 there are fewer than twelve possible signatures. For q=4, the twelve smallest weights of distinct 4-bit strings sum to 19, exceeding 4q=16. Thus q<=4 can NEVER distinguish all twelve starts, for any word length. This is sharper than the naive 2^q code-count bound.

**F/B-only confinement.** Words consisting solely of front/back face actions preserve F={1,5,8,9}, B={3,7,10,11}, N={0,2,4,6} as three position sets; flip events within each of these sets are identical across its initial states. They produce <=3 distinct histories for any word length. A word with only one other action has <=3x3=9 distinct initial histories: before that exceptional action, output depends only on the original F/B/N group, and afterward only on the transported F/B/N group. In particular length 8 words with q>=7 flip-capable actions cannot be fully injective.

**Residual exhaustive length-8 lower bound.** The only unresolved q cases are 5 and 6. A self-contained C++ exact physical enumerator checks exactly C(8,5)*4^5*14^3 + C(8,6)*4^6*14^2 = 179830784 distinct length-8 words, preserving all 12 oriented starting states, and the maximum observation rank is **11**, not 12. Histogram: rank2 1336832; rank3 25153024; rank4 7447040; rank5 64338688; rank6 25562624; rank7 38629120; rank8 9906688; rank9 6694912; rank10 636928; rank11 124928. The only inputs are 18 physically sticker-derived 24-state move bijections. Therefore no fixed word with L<=8 distinguishes all 12.

**Length-9 positive witness (fixed, not adaptive):**

```text
F B U R2 F B' U F B
```

Its twelve independent zero-flip starting slots produce distinct 9-bit codes (least-significant bit is first observation): `[112,287,224,30,384,15,0,398,399,255,286,510]`. Prefix ranks `[2,3,3,3,6,9,9,11,12]`. Consequently the first possible *single-word full 12-state identification* horizon is EXACTLY L_full=9.

Because the source family includes **all 220 triples**, every pair of initial slots co-occurs in at least one admitted requirement; hence a **single** word covers all requirements if and only if it distinguishes all twelve slots. This proves M*(L)>1 for L<9 and M*(L)=1 for all L>=9.

## Exact two-word criterion for this particular source family

For a word w let B(w) be the set of unordered pairs {i,j} of initially possible slots with the same observation history. A source set A is covered by w exactly if A contains no pair in B(w).

Suppose two words w,v jointly cover the full frozen R, and neither is already a universally distinguishing word. For every collided pair e in B(w) and f in B(v), their union cannot be an admitted source subset (or contained in one), because both words would fail that source. If e and f share a state, |e∪f|<=3, and every three-set is admitted: contradiction. If they are disjoint, |e∪f|=4 and every nonhomogeneous four-set is admitted. Thus the union must be EXACTLY one of the three excluded homogeneous quartets F, B, N.

Fix any f. The homogeneous quartet containing f is unique, so every e in B(w) must be its complementary pair. Therefore B(w) contains exactly ONE pair. Symmetrically B(v) contains exactly one, and the two disjoint collision pairs partition one of F,B,N. Conversely if two words have just those complementary pairs in one of F,B,N, then they cover all source requirements because none of the 1192 sources contains the entire homogeneous quartet.

**Two-word dictionary iff:** (a) one word already fully distinguishes 12, OR (b) each word has exactly one collided pair and the two pairs partition an excluded homogeneous F/B/N quartet. In case (b) both words have exactly 11 distinct observation histories. This is a mathematical combinatorial characterization, not a numerical SAT claim.

## General collision-hypergraph characterization for arbitrary dictionary size

Let B(w) denote the graph of all distinct initial slot pairs that produce **identical complete observation transcripts** under a physical word w. A source A is distinguished by w if and only if A is an independent vertex subset of B(w). Therefore a dictionary D succeeds on the fixed source family R if and only if there **does not exist** an admitted source A and one chosen collided pair e_w from every w in D such that the union of all chosen pairs is a subset of A. Formally:

`D valid <=> NOT EXISTS A in R, (e_w in B(w))_(w in D): (UNION_(w in D) e_w) SUBSET A.`

This is an exact equivalence for any L and any dictionary size and does not rely on an integer-program encoding. The preceding two-word criterion is its first nontrivial closed-form case, obtained from the source family's all-triples and three excluded homogeneous quartets. For k=3, a prospective three-word obstruction is a collision-edge triple with a union contained in an admitted source set of at most five elements. This points to a **constraint-preserving collision-hypergraph attack** on the remaining M*(6)=3-versus-4 and M*(5)=6/7/8 problems; it does not resolve either yet. Crucially, unlike column-orbit aggregation, the collision graphs retain which exact initial-state pairs overlap.

## M*(8)=2 constructive upper

```text
F U2 F B U2 D F B     # only ambiguous pair {0,2}
F U2 F B U D2 F B     # only ambiguous pair {4,6}
```

These pair unions constitute N={0,2,4,6}, excluded from every admitted source subset. Independent frozen 1192-source replay confirms the union of the two word cover sets covers all 1192 rows (each alone covers 1066). Length-8 exhaustive lower excludes one word. Thus M*(8)=2 exactly.

## M*(7)=3 constructive upper and exact lower

```text
F' B L D2 B U2 F      # output rank10; collision pairs {0,4}, {1,8}
F' B R D2 B' U2 F     # output rank10; collision pairs {2,6}, {5,8}
F B R F U' F B        # output rank9; collision pairs {3,10}, {7,11}, {8,9}
```

These words cover respectively 967, 967 and 884 admitted requirements; their combined union covers all **1192**. For lower: q<=2 yields at most four observation types; q>=6 in a seven-move word yields at most nine by at most-one-exception F/B confinement. The remaining 114852864 physical seven-move words with q=3,4,5 were exhaustively enumerated; maximum ranks are respectively 8, 10, 9. Thus EVERY seven-move word has rank <=10, so no word has just one collision pair. The two-word collision criterion proves 2 words impossible. Hence M*(7)=3 exactly.

## M*(6) bounds

Physical 6-turn greedy cover (independently replayed across all 1192 original requirements) uses four real HTM words:

```text
F B U2 L F B
F' B' U L2 F B
F B U2 D F B
F B' U2 R F B
```

Each of these has nine distinct starting-slot output histories; union covers all 1192. Therefore M*(6)<=4. Because fixed-word full-history dictionaries have M*(6)>=M*(7)=3 by prefix refinement and extensibility, the current **honest range** is 3<=M*(6)<=4. No three-word UNSAT proof yet.

## Adaptive versus preset observability

Let belief B consist of possible **current** states among 24 oriented edge states. Define worst-depth boolean success F(B,d) recursively: F(B,d)=true if |B|<=1; false when d=0 and |B|>1, or |B|>2^d; otherwise true iff there exists a legal action a such that for both possible next flip outputs b in {0,1}, its successor belief B_(a,b) satisfies F(B_(a,b),d-1). This is a standard finite automata adaptive distinguishing-policy recurrence; it is an exact policy existence decision when all histories are perfectly retained and all actions accurately known.

Independent local Python DP on the real 18x24 move maps reports **no policy at worst depth6** (442 memoized explored belief-horizon states), and **a physically replayed policy at depth7** (556 total explored). Replay against all 12 initial slots reaches singleton leaves. Its leaf depths have distribution {3:1,4:1,5:2,6:2,7:6}; uniform-prior average 71/12 moves for THIS policy (not an expected-value optimum). Thus the exact adaptive minimax identification length is **7**, compared with fixed full 12-state identification length **9**. This is NOT the same optimization criterion as M*(7)=3 and not a measurement of human cognition.

## Status and proof lineage

This P5 record reports local independent deterministic physical enumeration, replay, and a finite-belief recurrence. A fresh GitHub Actions workflow `.github/workflows/cuberev-019-horizon-theorems.yml` was authored to reconstruct the sticker-derived move maps, verify the 9-step witness and 7-step policy, and rerun the 179830784-word L8 physical obstruction. **A GitHub Actions completed-run receipt is NOT yet independently confirmed.** Do not claim that external formal verification or academic peer review has already occurred. The existing 0.18 M*(4)=34 theorem has separately passed independent DRUP verification: https://github.com/WhoSia/CUBE-REV/actions/runs/37958523951

Separately, the L5 integer k7 exact court remains open: 6<=M*(5)<=8; the ordinary fractional cover optimum is exactly 16/3. Its 16-symmetry SAT branch program and independent integer dual cuts are stored in P3/P4. This P5 result does not settle that k7 problem.

**New research questions:** Can M*(6) be shown 3 or 4 by a collision-hypergraph obstruction? Can M*(5) be narrowed by symmetry-aware integer SAT/DRUP? What physical transition invariants determine the observed 34 to 3 to 2 to 1 collapse? What does a resettable known-source experiment dictionary explain—and NOT explain—about attention, memory, adaptive feedback and human cube solving?
