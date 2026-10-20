# P21 — Ancestor-Complete Mixed-Radius Exclusion (2026-10-20)

The source-fixed global exact-18 theorem is **NOT YET independently certified**. This mathematical result is a proposed sufficient certificate structure, not a completed full physical search.

## Theorem
Set radius R=17 and choose a length-nonincreasing normal form of every HTM solution. Partition all canonical words of length ≥2 by their first two legal moves p. Choose **independently for each p** a depth k(p), 2≤k(p)≤17, and a physically sound one-sided goal superset F_p satisfying B_(17-k(p))(e) ⊆ F_p. For every two-move prefix p, completely check **all** its legal continuations from length 2 through length k(p), not only its terminal depth, and prove that no reached *physical state* belongs to F_p. In addition check that no solution of length 0 or 1 exists. Then d(s,e)>17.

**Proof:** A hypothetical ≤17 word can be normalized without increasing length. A normalized 0/1 word is directly excluded. A normalized word w of length m≥2 has exactly one canonical first-two prefix p. If m<k(p), w itself is included among the checked ancestors and its endpoint e belongs to F_p. If m≥k(p), its first k(p) steps reach x while its suffix length m-k(p)≤17-k(p) solves x, giving x∈B_(17-k(p))(e)⊆F_p. Both contradict the hypothesized exhaustive negative physical check. QED.

This proof needs **no separate previously established lower-17 premise**, unlike the earlier exact-length17-only mixing construction. Conversely, checking only the terminal k(p) frontier and omitting its ancestors is unsound.

## Finite independent falsification test
Executed standalone `p21_mixed_split_toy_checker.py` on the seven-element cyclic group with inverse-closed generators ±1: all 385 choices of source, R=1..5 and two first-move split depths agreed with direct shortest-path distance. A deliberately unsound *terminal-frontier-only* algorithm has the explicit nonzero-source counterexample **R=2, source=1, optimal distance=1, k(+1)=1, k(−1)=2**; it falsely claims no solution. This is a mathematical counterexample to a checker design, **not** an independent Rubik's Cube proof.

## Current original WCA evidence boundaries
- P19 completed source prefix (1,4) under one-sided source10+B7 with full 15 third children. It is the only PDB-free completed two-prefix court currently in the ledger.
- P20 independently completed *third*-prefix (1,5,0), with 15/15 fourth actions and an additional BFS single fourth replay. This is **not** completion of (1,5).
- P8 (14,1) and P9 (14,2) are actual C8/E6-pruned source11+B6 computational results but their large projection pruning admissibility is not independently certified; at most a conditional mixed ledger 3/243; independently PDB-free 1/243.
- Existing verified physical 18-step solutions and third-party optimum18 do not prove a new full checker-certified no17 claim.

## Certificate application prerequisites
For every sector independently verify its source word-tree coverage, its ancestors up to k(p), its actual physical state endpoint calculations, any algorithmic pruning, its goal-ball inclusion and physical frame. Reject any missing sector, any missing short root, or any unsigned claim of zero physical intersections. Do **not** confuse immutable bytes/receipt totals with semantic proof.

## Research OS writing decision
Promote the mixed-radius ancestor-complete theorem as a **proved method statement** in Paper2; keep the original WCA exact18 theorem explicitly open until the remaining sectors and semantics are independently certified. BRM Paper1 and Humantech prior submitted drafts remain separate historical lineages.
