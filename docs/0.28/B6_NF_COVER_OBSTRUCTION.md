# 0.28 B6: one local obstruction is a complete bipartite hitting-set problem

## Source provenance and exact scope

The archived physical witness replay in
`scripts/cuberev-observation/verify_b6_nf_four_seeds.py`
certifies, up to the tested cube symmetries, **six-HTM vs six-HTM**
pairs of distinct B6 cube states with differences confined to:
- the two original corner tags at the endpoints of original edge DL; and
- one original edge from `N = {DB, DF, LB, LF}` and one from
  `F = {UB, UF, RB, RF}`.

There are 16 original edge-support pairs `{n,f}`, with `n∈N,f∈F`.
The physical evidence is in the pre-existing replay script, **not**
in the present combinatorial verifier, which only consumes the
already-established 16-support proposition.

## Proposition — complete bipartite obstruction

Let `S` be any collection of original cubie-tag sensors. Suppose
the two original corner tags at the endpoints of DL are **not** in
`S`. To distinguish all sixteen exhibited B6 witness pairs, the
observed edge tags must contain **all of N or all of F**.

### Proof

Fix `n∈N,f∈F`. The physical witness for this pair differs only
in the two unobserved original DL endpoint corner tags and the two
edge tags `n,f`. If neither `n` nor `f` is observed, these
two distinct B6 states collide under `S`. Thus `S` must meet each
of the sixteen 2-element sets `{n,f}`. They are the edges of
`K_{4,4}` with sides `N,F`. Every vertex cover of this complete
bipartite graph contains all of `N` or all of `F`: otherwise
choose an unobserved vertex on each side, and their edge is uncovered.
Conversely either whole side meets all sixteen supports. QED.

The conclusion is *necessary to avoid the exhibited collisions*,
NOT sufficient to separate all B6 states.

## Cheap arithmetic consequence

When the two DL endpoint corners are omitted and **exactly two
original edge tags** are omitted, the omitted edges cannot consist
of one N edge and one F edge. This rules out precisely `4×4=16`
of the `binom(12,2)=66` possible two-edge omissions at fixed
DL corners, before any additional witness or SAT analysis. Fifty
candidate omissions remain, some still excluded by other collision
supports. Therefore do **NOT** infer all 50 are valid; the prior
complete B6 classification has 13 successful two-edge patterns.

This is a local hand proof derived from previous physical witnesses,
not a new general Test Cover or NP-completeness theorem.

## Independent check

Run:
`python scripts/cuberev-observation/verify_b6_nf_cover_duality.py`

The verifier enumerates all 256 choices of the eight N/F original
edge tags and asserts that the sixteen collision supports are met
iff the choice contains all four N tags or all four F tags. It also
enumerates exactly two inclusion-minimal hitting sets.

## Research method

Use known physical witness support hypergraphs and cheap exact
combinatorics before launching new cube-state enumeration. Promote
an obstruction to a global theorem only after proving sufficiency
separately. Preserve physical semantics by linking every support
claim to archived executable replay evidence.
