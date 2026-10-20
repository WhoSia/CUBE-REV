# CUBE-REV 0.27 — P20: Heterogeneous Split Composition and a New Disjoint Physical Source Court

**2026-10-20 | Research classification:** mathematical composition lemma + real but **bounded** new physical exclusion + adversarial structural checks. **The global independent theorem `d18(s)=18` is not established.**

## 1. Fixed problem and why mixing proof branches is legitimate

The fixed source is the WCA original 20-turn scramble `R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2`. HTM uses the 18 face rotations, each cost one. The exact original labeled 54-sticker representation and independent known 18-move physical witnesses are frozen. The complete set of canonical 17-move words is divided into exactly 243 disjoint **word-prefix** cylinders by the first two canonical turns. The partition is of words, not cube positions; different words may reach the same cube.

**Conditional heterogeneous composition theorem.** Assume: (i) an independently sound bound `d(s,e)>=17`, ruling out all shorter solutions; (ii) an endpoint-preserving, length-nonincreasing HTM normal form that removes adjacent same-face turns and fixes the ordering of commuting opposite-face turns; (iii) for every canonical two-turn prefix `p` there is a chosen split `a(p)+b(p)=17`, `2<=a(p)<=17`, and an independently sound certificate ruling out every exact-length `a(p)` canonical extension beginning with `p` whose physical endpoint lies within true solved `B_{b(p)}(e)`; (iv) an independently physically replayed length-18 solution. Then `d(s,e)=18`.

**Derivation:** If `d(s,e)<18`, hypothesis (i) makes an optimal solution exactly 17. Apply normalization. It cannot become shorter without contradicting (i), hence it is a canonical 17-word. Its unique legal two-action prefix is `p`. Take its first `a(p)` turns; the remaining `b(p)` turns solve it. Therefore the middle physical state belongs to the true goal ball `B_{b(p)}`. This contradicts the sector-specific certificate (iii). Thus no length17 solution exists, and the length18 witness from (iv) supplies the matching upper bound. QED.

A **one-sided** goal superset `F_p` can replace the exact `B_{b(p)}` condition in (iii), provided the verifier proves `B_{b(p)} \subseteq F_p` in the same physical-state encoding. Hash collisions create false positives only. Different sector proofs may use different data structures, generators, and search algorithms, but each must carry the prerequisites of its own negative result. Missing or wrong source physical-frame equivalence, invalid prefix normalization, incorrect pruning, or forged zero-hit logs are fatal. The theorem itself does not validate those premises.

Without hypothesis (i), a more self-contained approach is to exhaust **all source words through depth `a(p)`** in every two-prefix cylinder, check all length-zero/one ancestors separately, and use the inclusion of `B_{b(p)}`; this may exclude all length<=17 simultaneously when split lengths and ancestor coverage are handled correctly. The P14/19 `10+B7` formulation is an example of this stronger local variant.

## 2. Old results cannot be silently made unconditional

The genuine P19 full `(1,4)` second-prefix court used PDB-free physical source-depth10 + independently goal-inclusive `B7`, and completed 15/15 third actions, `1,212,049,276` grammar nodes with zero goal filter hits. P8 original `(14,1)` and P9 `(14,2)` second-prefix courts instead completed source-depth11 + solved-B6 via the C8/E6 branch pruners. Their original logs are real, but **their independent mathematical admissibility certification is still incomplete**. A mixed plan may account for **3/243** second-prefix labels as *conditional computational negatives*, while only **1/243** is a completed full two-prefix court without those large projection assumptions. It must not count a P20 third-prefix result as a fourth complete parent.

The historical earlier external physical Go source10+B6 proof of the lower bound17, and the independent external RubikOptimal 1.1.0 18-step result with a conservative no-equal-axis rerun, are **separate** evidence with explicitly conditional assumptions; they are not secretly promoted to a formally checked global lower-18 proof by this composition. This is a ledger of proof dependencies, not a new mathematical compression that closes 240 unvisited labels.

## 3. New physical execution: original prefix `(1,5,0)`

P20 actually searched **all fifteen** legal fourth-action subtrees of the *new* canonical three-turn prefix `(1,5,0)`, using the authentic 54 labeled sticker move geometry and the fully previously checked 109,043,123-entry one-sided `B7` fingerprint filter. A timed attempted single large run stopped after four fourth-action reports: correctly classified **INCOMPLETE** and not included as one completed report. It was replaced with fifteen distinct native C++ executions, each with its own output and genuine terminal `P17_FOURTH_SECTOR_ONLY_NEGATIVE_RECEIPT` marker. Their union was independently checked by a fresh Python program that derives the canonical grammar, and validates exact labels, per-sector word counts, leaves, parent sum and absence of reported filter hits.

| Actual P20 source-three result | Count |
|:--|--:|
| Independent completed fourth actions | 15/15 (`3` through `17`) |
| Sum of all canonical nodes, including the three-turn parent | **90,800,620** |
| Source-depth10 final leaves | **83,998,296** |
| Reported B7 physical fingerprint intersections | **0** |
| Sum of actual per-fourth DFS traversal seconds (excluding per-job loading) | **108.65 seconds** |
| Independent checked malicious report alterations | **7/7 REJECTED** |
| Parent `(1,5)` fully complete? | **NO — 1/15 third actions** |

This new prefix is disjoint from P19 `(1,4)` and from old `(14,1)/(14,2)` source courts. A separate **explicit-queue breadth-first** C++ implementation was adapted from the P19 BFS physical witness checker and recomputed the exact fourth subtree `(1,5,0,3)` without importing the P17 DFS: **6,802,324** nodes, **6,292,728** depth-ten leaves, **zero** B7 hits, matching the DFS. BFS and DFS still share the 54-site move table and goal fingerprint specification; they are not fully independent physical models.

The new Python grammar checker was itself attacked by removal, duplication, forged positive hit, corrupt B7 size, wrong source prefix, incorrect subtree count, and missing completion marker; all seven were rejected. During test setup two bookkeeping errors were identified (a mutation targeting the wrong size class and a JSON dict with tuple keys) and repaired *before* the final audit. These errors did not change any C++ physical search result. None of these receipt checks alone proves the original C++ code actually computed the reported zero intersections. The stronger evidence is the complete re-executable native traversal and the bounded independently implemented BFS replay, with the B7 inclusion theorem as a separately recorded premise.

## 4. Rewind into an independently checkable theorem: what remains

A complete proof-carrying `d18(s)=18` result can follow either (A) the PDB-free complete `10+B7` original source word-tree scan for all 243 second prefixes plus empty/one-turn ancestors, or (B) a heterogeneous family of source-depth10/goal-B7 and source-depth11/goal-B6 certificates **after** independently proving each chosen projection's admissibility and a global lower17 premise. The first route has a smaller mathematical trust base but high runtime; the second potentially reuses large computation but inherits a more intricate PDB verification obligation.

A genuine compact *semantic* induction would need a finite-state abstraction with a checked physical commuting square, a goal superset, and an actual invariant family closed under every remaining legal move. The recurrence on the word tree is an exact statement but not a speedup by itself, and the 64-bit goal filter does not automatically yield a compact reachable-set invariant. A Merkle root or checksum can authenticate delivered bytes but cannot certify a false `hits=0` as a physical fact.

**Immediate next work:** close additional third-prefix children under `(1,5)` with separately sealed fourth-court runs; build a two-mode complete second-prefix checker with a machine-readable dependency ledger and adversarial missing-ancestor checks; parallelize source certification without trusting only producer counters. Compare any proposed stronger certified projection to the strict threshold `17-k` before new giant searches. Continue Paper 2 writing in Research OS WRITING 3.0, keeping the mixed-radius theorem and demonstrated limitations in the main text without false novelty claims.
