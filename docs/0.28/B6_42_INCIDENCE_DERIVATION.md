# B6 4:2 incidence split: a hand-verifiable proof (existing rule, not new discovery)

## Status and exact source

This is a derivation of the EXISTING `admissible` predicate in
`scripts/cuberev-observation/verify_b6_geometric_rule.py`, not a
new B6 theorem. The original coordinate-free criterion and its
physical replay comparator predate this note.
- `verify_b6_geometric_rule.py` defines admissibility using cube incidence.
- `verify_b6_geometric_bridge.py` matches the rule to 19 physically replayed
  B6 negative-witness orbits and previously archived B5-positive candidates.
- The positive injectivity assertion for 156 layouts requires the separately
  archived full B6 state census. It does NOT follow from the negative witnesses.

## Why N-N has 4 successes and 2 failures

Let h have endpoints u,v. There are four edges incident with exactly one
endpoint of h, other than h itself. Partition them as N_u and N_v, each of
size two. They are disjoint: the cube's one-skeleton is triangle-free.

An unordered pair of two N edges has `C(4,2)=6` possibilities. The existing
criterion accepts precisely one edge from EACH of N_u and N_v. Therefore

    #accepted = |N_u|*|N_v| = 2*2 = 4,
    #rejected = C(2,2)+C(2,2) = 2.

This is a purely local cube-incidence count. It explains the 4:2 split
without any fresh enumeration of B6 states.

## Why F-F has 4 successes and 2 failures

Let h* be the antipodal cube edge, with endpoints u*,v*. Its four
other incident edge-spokes form F. There are precisely four pairs of F
spokes sharing one of the four relevant faces: for h=DL, F is
{UB, UF, RB, RF}, and the pairs are

    {UB,UF} (shared U face)
    {UB,RB} (shared B face)
    {UF,RF} (shared F face)
    {RB,RF} (shared R face).

The two non-face-sharing pairs are {UB,RF} and {UF,RB}.
Thus the "share a face" relation on F is a cycle C4,
with exactly four accepted edges and two rejected diagonals.
The intrinsic proof for arbitrary h follows by transporting this
incidence statement under cube rotations (every cube edge is in the
same orbit). Here the labels are original edge tags, so the
face-name intersection is exactly the existing admissibility test.

## Global 13 and 156 arithmetic

The original four geometric clauses are disjoint and produce
4 (N-N) + 4 (F-F) + 4 (F-h*) + 1 (P-P) = 13.
The 12 choices of original h give 12*13 = 156 labelled optimal layouts
under the existing uniqueness and positive-census assumptions.

This note distinguishes (a) easy cube-geometry incidence counts,
(b) B6 negative witness completeness, and (c) B6 positive injectivity.
