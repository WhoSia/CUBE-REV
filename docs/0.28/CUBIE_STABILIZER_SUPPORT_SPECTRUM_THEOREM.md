# P0.28 — Exact cubie-stabilizer order and support spectrum (classical algebra)

**Date:** 2026-11-03. **Status:** exact combinatorial theorem; finite independent
coordinate check. NOT a new HTM geodesic lower-bound certificate or a
new universal observability theorem.

## Model and definitions

Let G be the standard legal fixed-centre 3x3 cube group. Every original
corner/edge tag has a fully observed position AND orientation (3-state
corner twist, 2-state edge flip). Choose subsets C and E of original cubie
tags to leave unobserved, with |C|=c (0<=c<=8) and |E|=e (0<=e<=12).
All original tags outside C union E are fixed in BOTH coordinates. Write
H(C,E) for the pointwise stabilizer. The count below is independent of
which physically located tags are chosen, since legality depends only on
permutation parity and orientation sums, not word length.

Use delta(n)=1 for n=0 or 1, and 0 otherwise. Define

    P(c,e) = (c! e! + delta(c)delta(e))/2,
    O(c,e) = 3^max(c-1,0) 2^max(e-1,0).

**Theorem 1 (legal oriented-cubie stabilizer census).**

    |H(C,E)| = A(c,e) := P(c,e) O(c,e).

*Proof.* Every permutation of the omitted c corners and e edges fixes
every other original position tag. The whole 3x3 cube requires equal
corner/edge permutation parity. For n>=2, exactly n!/2 permutations
have each parity; for n=0 or 1, the unique permutation is even. Hence
the number of matching-parity permutation pairs is

    ((c!+delta(c))(e!+delta(e))
     +(c!-delta(c))(e!-delta(e)))/4
    = (c!e!+delta(c)delta(e))/2.

The global corner twist sum must vanish mod 3. This leaves 3^(c-1)
choices if c>=1, otherwise one; analogously edge flips contribute
2^(e-1) if e>=1, otherwise one. These choices are independent for
legal whole-cube oriented coordinates. Multiply. QED.

**Theorem 2 (exact physical tag-support spectrum).** Let N(c,e) count
legal states whose original oriented-cubie support is precisely a
SPECIFIED set of c corners and e edges (all those tags change, no
others). Then

    A(c,e) = sum_{i=0}^c sum_{j=0}^e C(c,i) C(e,j) N(i,j)

and binomial inversion gives

    N(c,e) = sum_{i=0}^c sum_{j=0}^e
             (-1)^(c-i+e-j) C(c,i) C(e,j) A(i,j).

*Proof.* Partition H(C,E) by its exact support; symmetry of the standard
legal cubie-coordinate constraints implies N(i,j) depends only on
support counts. Every specified omission set contains C(c,i)C(e,j)
potential exact supports of those sizes. Two-variable Möbius inversion
on the Boolean product lattice gives the displayed expression. QED.

## Regression values and their meaning

| c omitted corners | e omitted edges | A(c,e) stabilizer states | N(c,e) exact full support |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 1 | 1 (identity) |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 3 | 2 |
| 0 | 2 | 2 | 1 |
| 1 | 2 | 2 | 0 |
| 2 | 1 | 3 | 0 |
| 2 | 2 | 12 | 8 |
| 3 | 0 | 27 | 20 |
| 0 | 3 | 12 | 8 |
| 8 | 12 | 43,252,003,274,489,856,000 | (compute programmatically if needed) |

For (2,2), H contains exactly: the identity (1), two pure paired
corner twists (2), one pure paired edge flip (1), and eight states
whose support includes all four omitted original tags (8). Therefore
there are 11 nonidentity targets, divided 2+1+8. The classification is
independent of which two corner and two edge tags are omitted. Their
18-HTM geodesic distance is not independent of those positions.

No legal state has a nonempty support containing exactly ONE corner,
or exactly ONE edge: N(1,e)=N(c,1)=0 for all valid c,e. This is an
algebraic statement and does not locate the shortest physical word
realizing any positive N(c,e).

## Checks, code and falsification scope

Code: scripts/cuberev-observation/verify_stabilizer_support_spectrum.py.
Implements A, N, and histogram by exact-support counts using only the
Python standard library. Independent direct cubie legality enumeration
over 16 small (c,e) values 0..3 and (4,4) checks parity, corner twists,
edge flips and original tag-support masks without trusting the formula.
An additional full-group-order regression and (2,2) decomposition
check are included. This is a second enumeration of ABSTRACT legal
cubie coordinates, not an independent 54-facelet transition
implementation.

Do not infer a radius-B6 lower bound from these counts. In particular:

1. Classical base means H_S={1} globally; a radius-r base requires
   H_S intersect B_(2r)={1} and is strictly weaker.
2. A stabilizer generating set, its group order, and support profile
   do not certify shortest paths in the original 18-HTM alphabet.
3. Cube rotations preserve HTM distance only after checking their
   induced automorphism maps the face-turn generating set to itself.
4. A group-legal cubie configuration does not provide a short turn
   witness, and an absent short witness requires independent proof.
5. This counting theorem is an elementary consequence of standard
   3x3 cube legality plus binomial inversion: no novelty claim for
   the general count or inversion is made.

## Reading provenance / next questions

Seress (2003), Permutation Group Algorithms §§4.1–4.2, 5.1.1, 8.2:
stabilizer chains, Schreier–Sims, pointwise stabilizers and exact SGS
verification. Cameron (1999), Permutation Groups §§1.13, 4.13:
minimal and irredundant bases. Godsil & Royle (2001),
Algebraic Graph Theory §§2.2, 3.7: orbit-stabilizer and Cayley
graphs. These are background and delimitations, not citations
claiming they prove this exact cube support-count theorem.

For CUBE-REV 0.28, the useful next objective is an independently
replayable physical transition proof of minimum HTM length >=13
for each symmetry-reduced target of the B6-positive layouts.
The support profile gives simple fail-closed completeness/counting
checks for that goal generator, but contributes no HTM lower bound.

Current baseline docs: B6_EXACT_16_TWO_CERTIFICATE_CLOSURE.md,
B6_41_STABILIZER_DISTANCE_GATE.md and
B6_RADIUS_DOUBLING_STABILIZER.md. Preserve their actual verified
physical replay and independence limitations.
