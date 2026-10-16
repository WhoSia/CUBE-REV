# CUBE-REV 0.25 P0-R6I-P12-P4 — Unordered Relative Permutations, the Cube-Graph Conjugacy Action, and Four Weighted Geometric Orbits

**Initial status 2026-10-16: proposed finite orbit theorem, external Go CI PENDING.**

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
