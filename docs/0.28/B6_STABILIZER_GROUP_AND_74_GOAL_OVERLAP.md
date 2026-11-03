# P0.28 — From eight 12-state stabilizers to exactly 74 distinct physical-coordinate goals

**Date:** 2026-11-03. **Status:** proved by elementary legal-cubie
algebra and independently exhaustive coordinate checking. No 54-facelet
archive is needed for the overlap count. This does NOT certify a single
HTM lower bound and does NOT independently reproduce the 41-class
spatial symmetry quotient.

## Previously reported B6 census, and the exact remaining question

The existing B6 positive family contains eight representative
two-corner/two-edge omitted-tag layouts under proper cube rotations.
Each layout has 12 legal stabilizer states, of which 11 are nonidentity.
The original archived facelet goal generator produced 8*11=88 target
entries but only 74 different full physical states. Previously this
was established empirically by matching 54-facelet encodings.

The present note derives the 74 **without facelet search or hashing**.

## Theorem (shared C3 and union of stabilizer goals)

Fix any pair C of omitted original corner tags. Let E_1,...,E_m be
pairwise DISTINCT two-element subsets of original edge tags.
Define H_i=H(C,E_i), the legal oriented-cubie pointwise stabilizer
fixing every original cubie outside C union E_i, including orientation.

Then:

1. Each H_i has exactly 12 states.
2. For any i != j, H_i intersect H_j = K_C, where K_C is the order-3
   subgroup of pure corner twists on the fixed omitted corner pair.
3. For the union over all m subgroups,

       |union_i H_i| = 3 + 9m,
       |union_i (H_i minus {identity})| = 2 + 9m.

*Proof.* Standard 3x3 legality restricts the two missing corners and
two missing edges to a linked even/odd permutation choice (two
possibilities), three compensated corner-twist choices and two equal
edge-flip choices, yielding 2*3*2=12 configurations.

Precisely three of these leave all edges individually fixed in both
position and orientation: the identity and two opposite compensated
corner twists. They form K_C, isomorphic to C3.

Every remaining state of H_i changes both original edge tags in E_i.
Indeed, a parity-linked simultaneous swap changes both; otherwise
the paired nonzero flip affects both. If a legal state lies in both
H_i and H_j with E_i != E_j, then its changed edge-tag support is
contained in E_i intersect E_j, a set of size at most one; this is
impossible for an edge-changing state in a two-edge stabilizer. Hence
the pairwise intersection is exactly K_C. Further, each
H_i minus K_C consists of nine states with edge support exactly E_i;
these sets are mutually disjoint. Therefore the union has 3+9m
states and 2+9m nonidentity states. QED.

**Corollary for the eight historical B6 representatives.** They share
the same missing corner pair, but have eight distinct omitted-edge
pairs. Thus 88 nonidentity entries reduce to

       2 + 9*8 = 74 unique nonidentity states.

The duplicate count is 88-74=14, explained entirely by repeatedly
including the same two pure corner-twist states eight times.

**Crucial:** a group element being unique as a cubie state is NOT
the same as a word-metric class. Quotienting these 74 distinct states
to 41 HTM-distance classes additionally requires the certified
facelet symmetry and inverse covariance from
B6_41_STABILIZER_DISTANCE_GATE.md.

## A second classical-algebra check: subgroup type

For fixed missing corner and edge pairs, write each element as
(s,t,f), with s in C2 a simultaneous pair-swap, t in C3 a
compensated corner twist, and f in C2 a paired edge flip.
In the cubie-coordinate composition convention of the current source,
for left element (s,t,f) composed with right element (u,v,h),

       (s,t,f)*(u,v,h) =
       (s XOR u, (-1)^u*t+v mod 3, f XOR h).

The RIGHT permutation determines the sign on the LEFT twist. Changing
it to (-1)^s*v without changing the coordinate convention is
incorrect. The semidirect factor is S3=C3 semidirect C2, so

       H(C,E) is isomorphic to S3 x C2.

It has center C2 (identity and pure edge flip), commutator subgroup
C3 (pure corner twists) and element-order histogram

       order 1: 1; order 2: 7; order 3: 2; order 6: 2.

These are standard finite-group consequences, not new group theory.
They provide independent corruption checks on the physical goal
generator, while **not** determining 18-HTM shortest lengths.

## Reproduction and trust boundary

- scripts/cuberev-observation/verify_stabilizer_support_spectrum.py:
  closed combinatorial order/support count; standalone code test.
- scripts/cuberev-observation/verify_b6_stabilizer_group_structure.py:
  all 144 products checked against legal 8-corner/12-edge coordinate
  multiplication, all 1728 associativity triples, inverses, group
  order histogram, center and commutators.
- scripts/cuberev-observation/verify_b6_goal_union_count.py:
  all C(12,2)=66 omitted-edge pairs and C(66,2)=2145 distinct
  pairwise intersections checked, plus exact 3+9m union formula.
- test_stabilizer_support_spectrum.py,
  test_b6_stabilizer_group_structure.py, and
  test_b6_goal_union_count.py: discovery-compatible unittest tests.
- Verified previous target SHA and 41 geometric distance classes
  belong to the separately recorded archived 54-facelet provenance;
  the new files do not reconstruct or supersede those results.

## Reading and research reflection

Seress (2003) §4.1 explicitly separates base/stabilizer chain, strong
generating set and actual group-element representation.
Cameron (1999) §4.13 separates minimal vs irredundant base.
Godsil & Royle (2001) §3.7 separates group automorphisms and Cayley
graph symmetries. These distinctions explain why the algebraic
74-target census is a useful preprocessing audit but neither the
41-class physical-symmetry reduction nor the independent
HTM>=13 geodesic nonexistence proof.

A promising next task is to augment the historical 41-goal manifest
with a support-type and group-element-order column and verify those
attributes by a SECOND independent physical state decoder. If this
fails at any entry, withhold its geodesic claims rather than silently
trusting previously recorded target digests.
