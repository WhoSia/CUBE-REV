# CUBE-REV 0.25 P0-R6I-P12-P4 — Unordered Relative Permutations, the Cube-Graph Conjugacy Action, and Four Weighted Geometric Orbits

**Initial status 2026-10-16: proposed finite orbit theorem, external Go CI PENDING.**

## 2026-10-16 verified original finite four-orbit theorem, metric profile, conditional Lean

The initial 'PENDING' state at top of this report is intentionally preserved as history. The stage is **ACTUAL VERIFIED SOURCE/GO ORIGINAL B6 FINITE CLASSIFICATION PASS**, not a complete algebraic explanation of fiber equality.

[External P12-P4 Actions #38852970561](https://github.com/WhoSia/CUBE-REV/actions/runs/38852970561) full native actual B6 CP/CO/EP/EO solved6 regenerated and 576 complete exact-fiber pair ledger audited (original domain-separated SHA 82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979); independent Go built all 48 Aut(Q3) from original native 288-byte actual 18HTM face-turn table, then verified the **102** inversion-normalized relative CP maps form exactly **four** Q3 conjugacy orbits with constant observed pair weights.

| relative cycle type | orbit cardinality | actual identical-fiber corner pairs per label | orbit aggregate | stabilizer cardinality | intrinsic physical Q3 metric displacement histogram D0,D1,D2,D3 |
| :-- | --: | --: | --: | --: | :-- |
| (2)(2) | 6 | 32 | 192 | 8 | (4,0,4,0) |
| (2)(2) | 24 | 8 | 192 | 2 | (4,2,0,2) |
| (4)(2) | 24 | 4 | 96 | 2 | (2,4,2,0) |
| (4)(2) | 48 | 2 | 96 | 1 | (2,1,4,1) |

The independent [metric-profile action run #38853254299](https://github.com/WhoSia/CUBE-REV/actions/runs/38853254299) confirmed four distinct observed metric displacement profiles and exact 576 total. Here D_k(delta) is the number of cube corner positions v with graph-distance d(v,delta(v))=k. A Q3 graph isometry sends delta to g delta g^{-1}; by vertex relabeling the D_k are the same. Reversing the unordered corner pair sends delta to delta^{-1} and preserves the D_k by symmetric graph distance and changing variables v↦delta(v). Hence this metric is INTRINSIC to both conjugacy and inverse class. These four metric profiles distinguish the four observed Q3 orbits. This property does NOT claim that all 8! possible S8 elements with one of these histograms belong to the observed set: there are other S8 permutations with these spectra.

**Observed new weight-stabilizer identity:** for EACH of the 102 observed unordered relative labels, denoting observed actual pairs per label by μ([δ]), the permutation order (2 or4) by o, and graph conjugacy stabilizer size by h, the finite census satisfies **μ·o=8h**. Therefore each orbit's mass times o is |G|·8=384, and 576=48×(4+4+2+2). The factor8 is the number of corner graph vertices, which is suggestive but NOT yet derived by a bijection of actual fiber pair objects; no proof that the physical 576 pair objects carry a free 48-element action. Four raw orbit totals are direct empirical proof, not a radius-universal statement.

**Lean kernel proof grades:** New pure lemmas in [RelativeCornerCycleConstraints.lean](../../formal/025/RelativeCornerCycleConstraints.lean) establish universal pointwise graph distance preservation under invertible isometries and inverse reindexing, plus conditional orbit-mass arithmetic given the weight premise and orbit-stabilizer premise. First [Lean run #38853488125](https://github.com/WhoSia/CUBE-REV/actions/runs/38853488125) FAILED with tactic 'No goals to be solved' after an arithmetic rewrite already solved the final goal. Fixed by [human commit 3d8e7d96](https://github.com/WhoSia/CUBE-REV/commit/3d8e7d96c4aab78a8aaa5ceab1d6bd2ce3d53591), then entire [Lean workflow #38853787948](https://github.com/WhoSia/CUBE-REV/actions/runs/38853787948) SUCCESS; no sorry, no math-axiom injection. This certifies the abstract conditional facts, **NOT** full native B6 original geometry, true Aut(Q3) state action, or the counted μ.
 
**Actual corruption control:** Deliberately corrupted original source pair receipt fails the independent Go test, and original source goal corruption fails the upstream P12-P3 stage. CI read-only and human WhoSia author/committer only. 0.16-P11 finite cover obstruction, 0.19--0.24 exact physical/human provenance lineage, P11 proof boundaries and P12-P3 wrong face-support hypothesis preserved intact.

### Open structural mechanism: a genuine lift, not more coincidental numerology

Construct a solved-goal-preserving action of physical cube symmetries on the ENTIRE CP/CO/EP/EO group, with correct corner twist and edge flip coordinate transformations; check whether the involutive unordered corner pair relation E={c≠d:F6(c)=F6(d)≠∅} transports equivariantly. Only then can one derive μ invariance from group action. If that holds, the new identity μ·ord=8|Stab| suggests 4,4,2,2 induced pair orbits of full 48, but this free-action explanation remains **HYPOTHESIS**. If mirror symmetries are not actual allowed whole goal automorphisms, restrict to justified proper rotations before drawing consequences. Fixed original WCA scramble/18HTM-DFA certificate transport needs additional source-fixing proofs. Current original distance **16≤d18(s)≤18**. No lower17, no measured solver speedup.

## Problem and exact predecessor
P12-P3 original solved ball B6 yielded 576 corners pairs c≠d with exactly equal literal edge fibers. Their relative CP permutations delta = inverse(CP_c) composed with CP_d have 108 *ordered* raw maps in the canonical P12 pair orientation. But the original pair is **unordered**, so switching endpoints replaces delta by delta^(-1). Thus the correct unordered label is [delta]={delta,delta^-1}. The P12-P3 original 576 row record is preserved in exact read-only source workflow. The full 8,240,087 CP/CO/EP/EO B6 original SHA is 82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979.

## Proposed finite classification to check from the original pair ledger
Let Q3 be the cube's physical eight-corner POSITION graph recovered exclusively from original P9 288-byte 18HTM corner turn table. Enumerate all 8! bijections of the eight corner positions, retain those preserving adjacency (48 = |Aut(Q3)|). The *position graph* acts on unordered relative permutation labels by conjugation [delta] -> [g delta g^-1]. This is a mathematically meaningful action on permutations, but it is **NOT YET** verified to act on actual corner orientation + edge-state compatible fibers.

Preliminary postprocessing of previously verified P12-P3 full-run relative permutation histogram predicts:
| cycle | position-conjugacy orbit size | pairs per undirected label | total pairs | stabilizer size in graph group |
| --- | ---: | ---: | ---: | ---: |
| (2)(2) | 6 | 32 | 192 | 8 |
| (2)(2) | 24 | 8 | 192 | 2 |
| (4)(2) | 24 | 4 | 96 | 2 |
| (4)(2) | 48 | 2 | 96 | 1 |
| **TOTAL** | **102** | | **576** | |

The raw 108 oriented relative maps are expected to coalesce into 102 inversion-normalized maps. In all four predicted orbits, the number of original fiber-equal pairs per label is numerically CONSTANT across all graph-conjugates. If an independent external court certifies this, the structure is a **four-orbit finite theorem** at the label-count level, not yet a whole physical group automorphism proof. It refines P12-P3's 12,24,6 moved SUPPORT families, and explains how relative permutation labels refine the 12 six-support, 24 path and 6 antipodal-edge support families.

## Negative tests and proof boundaries
New Go checker re-parses all 576 original packed corner pairs and verifies each cycle, 8-bit CP/CO masks, signed twists and fiber count. It builds the six physical corner-face support masks, 12 graph edges, and all 48 graph automorphisms without trusting a predetermined table of 48 mappings. It then checks closure and weight invariance in EVERY orbit and rejects a deliberately modified pair ledger. This is separate from and downstream of full B6 C++ original SHA and previous P12-P3 exact fiber census.

No actual action h on whole CP/CO/EP/EO states has been built/verified here. Consequently **do not infer** F6(h_C c)=h_E F6(c), true physical symmetry of the observed fiber-equal pair set, 24-or-48 transformation on the fixed original WCA scramble, or canonical DFA-language certificate reuse. The original distance is still 16≤d18(s)≤18 with 14 first generator source B10 sectors unproved. Full scientific history 0.16-P11 integrality finite vs pure explanation and P12-P3 false face-support hypothesis and parser two failures remains recorded.

## Next genuine mathematical mechanism
If the four weighted orbit types are independently certified, seek an actual solved-ball-preserving complete CP/CO/EP/EO action lifting G=Aut(Q3), and relate the 32/8/4/2 multiplicities to stabilizer-fixed fibers or twisted cocycles rather than mere group invariance. Under an *actual* equivariant bijection of corner pair objects, equal fiber-object counts within each orbit follow as a theorem; constructing that action is a substantive open proof obligation. Do not claim the existence of any such lift from orbit-uniformity alone.
