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

Let h* be the antipodal cube edge, with endpoints u*,v*. Four other edges
incident with h*'s endpoints form F, partitioned into two pairs F_u* and
F_v*, each of size two. A pair in F shares a face label iff it selects
one spoke at EACH endpoint of h*, AND their remaining face label is
the same. Because a cube edge lies on exactly two faces, those same-face
cross-endpoint pairs occur in two choices? CAUTION: here the side-label
face shared between the two spokes may instead follow distinct endpoint
neighbors; verify against actual face labels before claiming a 4 count.

Authoritative rule: accept exactly F pairs with intersecting face-label
sets, `set(edge_a) & set(edge_b)`. Directly on the four spokes:
- same endpoint: two pairs; each contains no shared face label (adjacent
  faces at one endpoint may share a face, depending on the h* orientation);
- opposite endpoints: four pairs; shared face label may occur.
Use explicit fixed h labels to resolve. Do NOT infer without checking.

## Global 13 and 156 arithmetic

The original four geometric clauses are disjoint and produce
4 (N-N) + 4 (F-F) + 4 (F-h*) + 1 (P-P) = 13.
The 12 choices of original h give 12*13 = 156 labelled optimal layouts
under the existing uniqueness and positive-census assumptions.

This note distinguishes (a) easy cube-geometry incidence counts,
(b) B6 negative witness completeness, and (c) B6 positive injectivity.
