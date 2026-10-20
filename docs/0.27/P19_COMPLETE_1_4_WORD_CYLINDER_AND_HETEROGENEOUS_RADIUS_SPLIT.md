# CUBE-REV 0.27 — P19: An Entire Source Two-Move Cylinder, Direct Short-Ancestor Replay, and Heterogeneous Radius-Split Certification

**Research date:** 2026-10-20. **Fixed source:** WCA scramble `R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2`. **Metric:** HTM. **Exact global 18 theorem:** NOT independently established.

## 1. The actual computational result: one complete radius-10 source cylinder

The two-action canonical prefix `(1,4)` has fifteen legal third moves

`{0,1,2,6,7,8,9,10,11,12,13,14,15,16,17}`.

P17 and P18 had already executed the three third-child courts `0`, `7`, `8`; P18 gave the entire `1,4,0` court a corrected BFS/DFS comparison. In P19 the twelve missing third-child courts `{1,2,6,9,10,11,12,13,14,15,16,17}` were **actually executed to depth ten**, each using the original fixed 54-sticker permutation representation and the complete one-sided solved-radius-seven fingerprint filter (B7). These P19 runs were split across 3 concurrent native C++ processes; each completed independently with a genuine zero-hit report and a terminal completion marker, not a partial log.

The exact grammar masses, including each third-prefix root, are:

| Third move class | Number of children | Nodes per completed third-prefix court | Depth-10 leaves per court |
|---|---:|---:|---:|
| `{0,1,2,6,7,8}` | 6 | 90,800,620 | 83,998,296 |
| `{9,10,11,12,13,14,15,16,17}` | 9 | 74,138,395 | 68,584,320 |
| **Complete two-prefix court** | **15** | **1,212,049,276 including the two-prefix root** | **1,121,248,656** |

The exact arithmetic identity is

\[
1 + 6(90,800,620) + 9(74,138,395) = 1,212,049,276.
\]

P19 newly executed `3(90,800,620) + 9(74,138,395) = 939,647,415` word-tree nodes. The previously completed three third children contributed `272,401,860`. Every third-child and its legal fourth children are identified by their original prefix, without double counting. The original goal filter recorded **zero matches in all 15 third-child subtrees**. The separate independent Python grammar checker determined all fifteen names and counts from HTM normalization, rejected four deliberately corrupted/missing/duplicated reports, and **refused** to equate perfect structural counts with an independent verification of zero-hit semantics.

### Short ancestors: no dependency on P13 for this parent

A new C++ program independently replayed all canonical source words of lengths zero, one, two, and three, measuring `1+18+243+3240=3502` original 54-sticker states/words. Each had **no match with B7**. A deliberately changed source equal to the solved state was a **positive control**: its 3,502 short paths were all in B7 and were detected. This directly establishes the missing two-prefix root and all lower-length parent obligations of this decomposition, without importing the separate P13 lower-11 theorem.

The B6 checkpoint independently passed a renewed 8,240,087-state physical-layer BFS audit (11,189,682 neighbor tests). The 64 B7 filter shards independently passed renewed inclusion checks for all `8,240,087 × 19 = 156,561,653` solved-radius-six self-or-successor fingerprints. This is a *one-sided inclusion proof*: collisions and extra false positives cannot manufacture a false negative result.

### Cross-method semantic confirmation, not complete model independence

To challenge the DFS implementation, P19 introduced a separate explicit-queue breadth-first traversal of the canonical physical word tree. It independently traversed every one of the **twelve fourth-action subtrees** below the newly completed third prefix `1,4,9`, totaling **74,138,395** canonical nodes and **68,584,320** depth-ten leaves including the third-prefix root accounted by the original DFS; reported goal hits remained zero. The cross-method comparator required identical move labels, counts and zero-hit values and rejected four tampered/partial BFS collections. An additional one-sector BFS replay `(1,4,1,3)` agreed with the DFS. Earlier P18 performed a fully corrected BFS replay on all fifteen `1,4,0` fourth-action sectors. **Only two of the fifteen third-prefix courts (0 and 9) have whole-court BFS/DFS dual replay**; this is not an assertion of two independent 54-sticker geometries or an independently machine-checked whole 1.2-billion-node trace.

### Precise evidence class

This result provides a **complete physically executed conditional negative source-cylinder computation**, independently audited at the level of word-tree coverage and complete one-sided goal-image inclusion, with bounded cross-method physical replay. The receipt parser alone cannot verify an adversarially fabricated zero-hit claim; verification at that adversarial standard requires actually rerunning the native source explorer for the court or obtaining a compact independently checked semantic invariant. The large B7 fingerprint shards themselves remain scratch T0, not yet separately whole-byte sealed in Drive. The small code/log/receipt capsule is portable and may be independently rerun with the exact original physical model and regenerated goal shards.

## 2. Exact recursive semantic invariant

Let `last(p)` be the last face turn in a canonical word `p`, `L(last)` its legal HTM successors, `T_a` the physical state permutation, `H` the deterministic 54-sticker fingerprint, and `F` a one-sided filter containing the fingerprints of every state in the solved B7. Define

\[
I(p,r) := [H(s\cdot p)\notin F]\ \land\
\bigwedge_{a\in L(\mathrm{last}(p))} I(pa,r-1),\quad r>0,
\]

with `I(p,0) := [H(s·p) not in F]`. Induction on `r` shows that `I(p,r)` is equivalent to absence of any canonical extension of `p` of length at most `r` whose physical endpoint belongs to the filter. **This is an exact semantic induction, not merely a sum-of-nodes identity.** To prove it with a small certificate rather than a full traversal, one must exhibit a new invariant over physical or abstract states whose accepting set excludes F and whose transition relation is checked for all legal face turns. P19 does not invent such a compact compression: the induction is discharged by complete physical enumeration in one particular cylinder.

The parent proof is the actual P19 check of `H(s·(1,4)) not in F`, plus the conjunction of the 15 negative third-child checks with remaining radius seven. Its grammar mass includes its root exactly once. **It does not prove d(s·(1,4),e) ≥ 16**, since canonicalizing an arbitrary solution starting at that intermediate state can change its left prefix. The legitimate conclusion is only *no original-source canonical short word whose first two moves are (1,4) meets B7 at depth ≤10*.

## 3. Heterogeneous split theorem: the stronger rewound architecture

Suppose an independent lower bound already excludes every solution with fewer than 17 HTM moves (the previous external source10+B6 whole-root lower-17 certificate is one such conditional premise). The remaining potential counterexamples to optimal distance eighteen are **exactly length-17 canonical solving words**.

Partition all canonical length-17 words by their first two actions `p`. For each 2-prefix `p`, choose any integer split `(a_p,b_p)` with `a_p + b_p = 17`, `2 ≤ a_p ≤ 17`, `b_p ≥ 0`, potentially *different for different prefix sectors*. If a physically sound certificate proves that **no exact-depth `a_p` canonical word starting with `p` ends inside the solved `B_{b_p}(e)`**, then there can be no length-17 canonical solving word beginning with `p`.

**Proof:** If such a length-17 solution existed, its first `a_p` moves would form a canonical prefix still beginning with `p`. The remaining `b_p` solving moves put its depth-`a_p` endpoint in `B_{b_p}(e)`, contradicting the certificate. With a sound complete collection for all 243 canonical second prefixes, no canonical length-17 solution exists; the assumed independently certified absence of shorter solutions and a separately verified 18-step witness imply `d(s,e)=18`. Because prefix cylinders partition full words rather than physical states, different certificates need not use the same goal-ball radius or the same search algorithm.

This **heterogeneous-radius proof composition** allows reusing sound negative `11+B6` prefix sectors from P8 (`14,1`) and P9 (`14,2`) with the new full-depth `10+B7` P19 sector (`1,4`), under clearly different correctness assumptions. The P8/P9 local C8/E6-pruning proofs presently depend on the independent admissibility of those projections, which is not yet certified; so the combined three-sector proof remains **conditional** and cannot be promoted to an independent global result. Do not conflate *three completed local computational cylinders by heterogeneous methods* with *three full PDB-free one-sided certificates*. If the intended final claim rests on the standalone B7 checker only, use new B7-based certificates for those sectors too.

The advantage of the theorem is practical and mathematical: when an independently certified lower-17 theorem is available, final optimality requires ruling out exactly length17—not redoing a separate `≤16` proof in every 2-prefix—and different certified local solvers may be composed. The price is explicit dependence on the global lower-17 premise and the respective local search/pruning verification for each chosen split.

## 4. Next test, constraints, and writing status

To improve beyond exhaustive enumeration, a compact abstract-state certificate needs a total abstraction `α(x)`, an independently checked commutation `α(T_a x)=\bar T_a(α(x))`, a superset of goal fingerprints in the abstract domain, and finite inductive safe sets `K_r` closed under all relevant transitions. Without such an actual closed invariant and its verified transition table, **the word-tree recursion itself is not an algorithmic shortcut**. Searching for a small one is valuable, but claims of a new independent exact-distance theorem cannot precede that construction.

The entire `1,4` cylinder now has a completed negative physical run. Only **one of the 243 canonical second-prefix courts** is complete under this specific `10+B7` approach. Its 12 new third-child logs plus earlier 3 prior child logs, grammar audit, P18 prior cross-method receipts, P19 B6/B7 audit replays, short-ancestor positive/negative controls and one entirely cross-replayed third child are retained. This is a substantial **bounded local theorem**, not a complete standalone lower-18 theorem and not a universal optimality result. Research OS WRITING 3.0: preserve the failed early P18 BFS attempt, the distinct source trust issue, and the absence of global closure in the manuscript rather than inflate the proven scope. Do not spend resources treating file digests as mathematical proof.
