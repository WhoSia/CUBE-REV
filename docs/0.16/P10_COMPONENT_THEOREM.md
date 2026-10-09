# CUBE-REV 0.16 — exact split of the small universal-word covering obstruction

**Internal P10; formal version CUBE-REV 0.16 stays OPEN.** This document is a mathematical theorem about the reduced P9 50×116 finite covering instance, not a solution of the original 1,192-basis universal dictionary minimum.

## Provenance and model boundary

Earlier P5–P9 work constructs 1,192 original 3/4/5-source separating-basis requirements for a tracked Rubik-edge, under 18 legal HTM tokens and exactly four turns. Let M* denote the minimum number of four-turn words separating every original basis. A physically checked 34-word list proves M*≤34. A 60-positive-dual-weight certificate proves that if a catalogue of 24 words existed it would use only 168 near-tight original output partitions, and ten different candidate words must be spent on ten weight-20 singleton bases, leaving 50 reduced positive-weight bases for at most fourteen other words. The exact P9 reduced instance is now PUBLIC and math-only at [P10_50_BY_116.json](P10_50_BY_116.json). It is an *abstract mathematical necessary subproblem*, not an unrestricted replacement for the original physical state transitions.

## Theorem (componentwise optimum)

Let `U` consist of the fifty basis indices with nonnegative integer weights given in the JSON, total weight276. Let each of the 116 candidate masks cover the indicated basis indices. Every candidate has weight either16 (six masks) or20 (110 masks), and no candidate has weight>20. Build the bipartite incidence graph of targets and masks; target connected components induce **exactly** two disjoint subproblems.

- **Component A:** 22 targets, weight180, 36 candidate masks. An eight-mask family covers weight≤8·20=160<180. Nine explicit masks in the associated public Python test cover all22 bases. Hence **minimum=9**.
- **Component B:** 28 targets, weight96, 80 candidate masks; 74 masks of individual mass20 and six of mass16. Suppose five masks covered all28 targets. If one mask has mass16, then total mass≤16+4·20=96, so necessarily all five cover pairwise-disjoint target sets, with four of the mass20 variety. If all five have mass20, their summed mass100 is only four more than the needed union weight96. Because every nonempty pairwise intersection has weight at least four, only one pair could overlap, in a target weight exactly four, with no triple overlap. Dropping one member of this pair leaves **four pairwise-disjoint mass20 masks**; the fifth mass20 mask overlaps their union in total weight exactly four. This is necessary; no assumption of equivalence is made.

The 74 mass20 masks contain exactly **7,004 unordered, pairwise-disjoint four-mask families**. Independently compiled C++20 and Python direct enumeration show **zero** extensions of these families by a disjoint mass16 mask, and **zero** extensions by any other mass20 mask of overlap-weight four. Thus **no five-mask cover of B exists**. Six explicit candidate masks cover all28 targets; hence **minimum=6**.

Since every candidate is fully contained in exactly one of the two components, a cover of all fifty has minimum **9+6=15** masks. Adding the ten forced weight20 singleton words gives a **25-word covering of the SIXTY POSITIVE-WEIGHT DUAL bases**, using original physically derived near-tight HTM candidate words. This is a model-specific finite exact theorem, not a human cognition observation.

## Why this does not decide M*

There are **1,192** original required source bases, of which only **60** carry positive dual weights. The new 25-word witness covers those sixty but may fail on the other **1,132 bases**. Hence it proves the *present particular positive-support argument* is saturated at 25; it does **NOT** show M*=25.

The currently certified original universal-word dictionary bound is still

`25 ≤ M* ≤ 34`

and the precise integer M* remains OPEN. A new ≥26 lower bound would have to use at least some of the 1,132 remaining targets or a different valid weighted certificate/cut family. A new upper≤33 requires an explicit word list checked against all1,192 original targets; a MILP timeout proves neither.

## Compact finite proof receipt and Lean plan

The portable Python-standard-library checker [test-p10-small-core.py](../../scripts/cuberev-016/test-p10-small-core.py) loads the precise published 50×116 data, confirms the graph decomposition, checks all7,004 quadruples with zero possible fifth extension, and checks concrete 9+6 covers. A separately compiled strict C++20 certificate and original P7/P9 24-state physical action oracle are included in the private math-only bundle and linked via SHA256 manifest.

**Lean kernel status** remains PENDING, not PASS. A natural staged formalization is (i) formalize the generic weighted-cover inequality for a family of finite subsets; (ii) prove the disjoint 22+28 component additivity lemma; (iii) import 74+6 finite 28-target masks and check the 7,004/zero-extension statement by a Lean reduction or proof-carrying LRAT refutation; (iv) link the 50×116 data back to the physical Rubik-edge 18-HTM orbit model. These are separate obligations. A Lean check of an abstract mask table without proving the physical semantic bridge is not a complete cube theorem.

**Paper value:** the decomposition and four-disjoint obstruction are inspectable finite combinatorics, but the set-cover phenomenon itself is classical. This is most promising as the exact-catalogue section of a broader cube-constrained experiment-design manuscript, or as a standalone problem only after exact M* or a structural generalization is proven.
