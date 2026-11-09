# CUBE-REV 0.28 — R14-P8.3: True physical belief aliases and an exact three-edge 20-frame strategy obstruction

**Date:** 2026-11-09. **Research axis:** complete-state correctness of belief compression and structural elimination of unsuccessful 20-frame policies. **Distinct from:** proving the unrestricted Rubik dual-color sensor horizon. Existing bound remains \(18\le h_{\rm adaptive}\le21\), open.

## Research cycle 1 — Deliberately try to falsify naive belief canonicalization

### Negative control in the fully observed 10E/6C twelve-state suffix

The physically oriented parity-matched suffix (two remaining edges, two remaining corners) has exactly twelve legal states and ten unread facelet positions. Exhausting every subset of those ten facelet queries on all twelve true states yields **43 distinct realizable posterior masks**. Under equal cardinality and common-parity stratum sizes, no pair in this finite suffix has distinct multisets of all 576 paired-action outcome-size partitions. This is a *negative finite result*, not evidence that cardinality counts are a sound general quotient.

### Positive physical counterexample in the 9E/5C 648-state suffix

Fully reading nine edge and five corner positions in the 3D-derived P5.1 physical lattice leaves exactly 648 legal states, with three cubies unobserved in each sector. A deterministic counterexample search checked **32,768** candidate subsets of the fifteen remaining facelets for a reference true state, plus **160 deterministic pseudorandom subset masks for each of the other 647** target states. The resulting pool contained **12,500 distinct realizable posterior sets**. This was a deterministic **sample of histories**, not exhaustive enumeration of all possible histories for all 648 true states.

Two realized histories have exactly the same posterior cardinality **six** and even/odd **sector** completion counts

\[
(E_0,E_1,C_0,C_1)=(1,1,3,3).
\]

Indexing *locally* within the 24 edge and 24 corner moving spatial stickers, with \(E\) and \(C\) identifying sectors:

- \(H_A:\;(E,19,R),(E,20,F),(C,15,D)\).
- \(H_B:\;(E,19,R),(E,20,F),(C,16,R),(C,19,R)\).

Both extend the **same** nine-edge/five-corner full observation prefix. The 576 possible paired spatial next queries have the following invariant **multiset of nonempty outcome population partitions**:

| Sorted nonzero partition | \(H_A\): number of query actions | \(H_B\): number of query actions |
|---|---:|---:|
| (1,1,1,1,1,1) | 12 | 12 |
| (2,2,1,1) | 132 | 0 |
| (2,2,2) | 0 | 132 |
| (3,3) | 36 | 36 |
| (6) | 396 | 396 |

No bijection on the full set of 576 queries, even with arbitrary rearrangement of color-response labels for each action, can transform these *full one-step partition structures*: the multiplicity of partition (2,2,1,1) is different. In particular the four parity counts and total size are **not a sound full observation-game isomorphism key**. This does **not** imply that the exact remaining minimax depths differ: both equal **one** in this example.

An independent verifier imports the previously vetted **P5.1 geometry only**, constructs all 648 oriented state words by a separate method, filters the two literal observation histories, and checks all 576 actions and exact partition frequencies. It does **not** use the original searcher's state masks, matching DP, or branch partition computation.

## Research cycle 2 — Exact physical 648-state Bellman court

The same physically ordered **9E/5C full-read suffix**, with 54 informative paired queries (6 remaining edge facelets ×9 corner facelets), admits an exact zero-error minimax calculation:

\[
\boxed{\operatorname{Win}(B,3)=\mathrm{false},\qquad \operatorname{Win}(B,4)=\mathrm{true}.}
\]

An explicit extracted four-deep policy correctly decodes **all 648 original states**: 24 targets finish in three reads and 624 in four. **Every one of the 54 potential root queries** has a concrete color response leaving a belief that cannot be solved in two further paired queries; these are fully enumerated AND–OR lower certificates, not merely state count bounds.

This matches the earlier 3E/3C miniature's depth numerically, but the new source uses *actual physical P5.1 edge and corner label words*. It is not a proof that the full 20-frame root is impossible or possible.

## Research cycle 3 — Try to finish the 648 suffix in two pairs after extra corner-only observations

The model permits additional readings of the nine unread corner facelets **without** new edge information, followed by at most two paired edge/corner readings. Exact AND–OR reports **false** for zero, one, two, three and four preliminary corner-only reads. This explicitly rules out that restricted finishing plan for this fixed remaining source-piece triple; it is a conditional statement, not a theorem about arbitrary interleaved 20-frame strategies.

The stronger reason is in the edge sector alone. With a *free oracle revealing the remaining edge permutation sign*, the three remaining edge pieces in this physical prefix still require three informative edge single-facelet observations. That question was then classified for **all 220** three-edge source-type sets.

## Research cycle 4 — Complete three-edge structural obstruction and adversarial proof

For any three distinct source edge color types, suppose their residual permutation sign and their total edge flip parity are fixed (the reference code uses the even-flip sector). Exactly **12** legal oriented assignments remain in each fixed permutation-sign stratum. The allowed next query is any one of their **six moving edge facelet positions**. An independent direct-frozenset exhaustive AND–OR solver finds:

\[
\boxed{D_{E,3}(L,\text{known parity})=3\iff
L\text{ forms a 3-edge star or a triangle in }K_{2,2,2}.}
\]

There are **24 star triples** (choose one central color among 6 and three of its 4 adjacent colors) and **8 color triangles** (one color from each of the three opposite-color pairs). Thus **32 of 220** remaining source-type triples require three edge readings **under each of the two known permutation signs**. The other **188** require exactly two.

An explicit machine-verifiable *online adversary* ledger enumerates **32 source triples × two known parities × six possible first spatial queries = 384** certificates. Each cert selects a feasible adversarial first color outcome and lists, for **every one of six possible second spatial queries**, two distinct legal assignments that still produce identical observation colors. Therefore each hard triple has no valid two-read adaptive exact decoding policy. This generates **2,304** literal second-query collision pairs, which can be independently rechecked.

### Sound implication for 20-frame policy research

If, after 18 frames, a branch of a candidate complete dual-probe policy has **fully observed exactly nine edge cubie positions** and has **not observed any sticker at the other three edge positions**, AND the remaining possible edge source types form a star or triangle, then the next two frames cannot distinguish the edge sector **even if the true permutation parity and the entire corner sector are revealed for free**. This branch cannot be part of a universally correct 20-frame policy.

**Important qualification:** the edge source types remaining and the nine fully read positions can themselves depend on observed colors. The structural obstruction above does **not** prove every 18-frame policy must reach a bad branch, nor establish the unrestricted global 21-frame lower bound. The result is a *sound adversarial branch-pruning lemma* that may be integrated into a future complete proof search.

## Verification / research falsifiability

1. `audit_r14_p83_suffix_equivalence.py` exhausts the restricted 12-state suffix (negative result).
2. `audit_r14_p83_648_prefix_invariant.py` searches actual 648-state reachable histories and produces the exact four-count alias.
3. `verify_r14_p83_independent_physical_counterexample.py` independently reconstructs the two six-state histories and every P48 query partition.
4. `audit_r14_p83_physical_648_exact_andor.py` proves depth four with an extracted policy and 54 distinct lower obstructions.
5. `audit_r14_p83_cornertime_tradeoff.py` tests restricted preliminary corner-only budgets 0..4.
6. `audit_r14_p83_all_220_three_edge_barriers.py` exhausts both known permutation signs for every triple.
7. `verify_r14_p83_all_220_independent_frozenset.py` independently reproves the exact 32/188 classification and star/triangle graph criterion.
8. `audit_r14_p83_384_adversarial_edge_witnesses.py` materializes query-by-query adversarial collisions.

No `python-chess` or other unrelated dependencies required. Sources use Python standard library. The P5.1 geometry dependency is explicit where used, and clean repository checkout reproducibility must be verified before claiming remote CI green.

**Release gate:** only local independent tests completed at preparation. GitHub CI remote completion, full-cube 20-frame feasibility, published priority over existing cubology/decision tree results, and unrestricted physical-query Bellman quotient remain **OPEN**. The guiding rule is **research questions first, code and commits only to establish or falsify them**.
