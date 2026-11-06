# CUBE-REV 0.28 R14-P5.5 — A Two-Sector Parity-Coupled Cyclic-Cubie Orbit Theorem

**2026-11-06 · Status: mathematical proof with 42 source-independent finite orbit checks · Prior-literature originality NOT established.** This is a theoretical generalization of R14-P5.4 that does **not** by itself decide the original h_adaptive=20 question.

## Abstract family and observation game

Fix integers `n,m,r,s >= 2`. Sector A consists of `n` labeled cubies, each carrying `r` cyclically ordered facelet positions; sector B has `m` labeled cubies each with `s` cyclic facelets. The within-sector allowed coordinate group is the wreath product `C_r wr S_n` (respectively `C_s wr S_m`). Restrict the pair to the kernel of the two total-orientation-sum homomorphisms and the matched-sign subgroup of sector permutations:

    G = { (p,o; q,t):
           p in S_n, q in S_m,
           sgn(p)=sgn(q),
           sum(o_i)=0 mod r,
           sum(t_j)=0 mod s }.

A paired query reads a single ordered facelet of sector A and one of B. The *spatial query domain* has `nr * ms` positions.

For `0 <= k <= n-2` and `0 <= l <= m-2`, fix exactly one distinguished spatial facelet coordinate in each of `k` distinct A cubie positions and `l` distinct B cubie positions; define `H_{k,l}` as its pointwise stabilizer inside `G`.

## Exact orbit theorem

The number of orbits under `H_{k,l}` on the Cartesian paired-query position domain is

    N(n,m,r,s;k,l) = (r*k+1)*(s*l+1) + I(n-k=2 AND m-l=2).

Here `I` is the indicator of the joint two-untouched-cubie boundary. This is a group-action orbit theorem, **not** the number of distinct observation-conditioned minimax-depth states, and not a claim that the formula was absent in existing group theory.

## Proof

A legal action fixing any single facelet of a *visited spatial cubie* must fix that cubie's spatial position and cyclic orientation entirely. Thus the `r*k` A-facelets belonging to visited A cubies are singleton orbits, and the `s*l` B-facelets belonging to visited B cubies are singleton orbits. Each sector's untouched cubies form a transitive family under permutations with parity compensated in the other sector, and cyclic orientations of untouched cubies can be freely varied one at a time provided an opposite orientation change is assigned to another untouched cubie. In particular, each sector's individual untouched facelets form exactly one orbit when both sectors have at least two untouched cubies.

The evident `r*k+1` by `s*l+1` Cartesian blocks are invariant under `H_{k,l}`. Any block touching a fixed visited-cubie facelet is transitive: if moving an untouched cubie in the other sector requires an odd permutation, the first sector can compensate by swapping its two untouched cubies without moving the fixed visited facelet. The same applies with sectors exchanged.

For an untouched×untouched pair of target facelets, if at least one sector has three or more untouched cubies, any required sign compensation can be performed by swapping **two cubies other than the target cubie** in that sector. Then both target cubie positions and their local facelet orientation can be routed independently, so the entire untouched×untouched block is one orbit.

Only when exactly two cubies remain untouched in EACH sector does this argument fail. The two possible position permutations of two cubies have opposite signs, and the two sectors must use **the same sign**. There are then two orbits on the untouched×untouched block, corresponding to whether the matching of the two selected cubie indices has the same or opposite pairing relative to the two two-element sector position sets. Within either orbit, cancelling local orientation changes on the other untouched cubie makes all `r*s` local facelet choices reachable. Each exceptional orbit therefore has size `2*r*s`, and the former single `2r * 2s` block splits into exactly two. Thus the formula acquires exactly one extra orbit, as stated.

A mechanical finite proof also directly exhibits generators achieving every listed orbit without relying on an unpublished cube-specific search. QED.

## Independent executable checks

The standalone Python checker imports **no** Rubik or CUBE-REV geometry. It builds the two wreath-product sector coordinate permutations directly, checks the parity and orientation-sum legality of all generators, then performs a full query-domain breadth-first search of the pointwise-stabilizer group action for every admissible `(k,l)` in five family instances:

- `(n,m,r,s)=(4,4,2,3)` : 9 profile cases.
- `(5,4,3,4)` : 12 profile cases.
- `(3,3,2,2)` : 4 profile cases.
- `(5,5,4,2)` : 16 profile cases.
- `(2,2,2,3)` : 1 profile case.

**42/42 cases PASS**, including five examples where exactly two cubies remain untouched in both sectors. The original full Rubik cube corresponds to `n=12,m=8,r=2,s=3`, independently checked in R14-P5.4 across its 77 admissible profile pairs. Its special case `(k,l)=(10,6)` has `400` instead of `399` paired-query orbits. These checks are proof *corroboration*, not a claim of unprecedented general wreath-product theory.

## Scientific value and strict boundary

A small result concerning a specific Rubik cube symmetry has become a closed symbolic statement applying to an infinite class of finite parity-coupled sensor systems. Its value for the central research programme is to supply **safe action pruning** for mixed spatial sensor-prefix patterns and to mark the exact boundary where a naive product quotient becomes unsound. Novelty relative to existing permutation-group, wreath-product and stabilizer-orbit literature is **OPEN**; group orbit-stabilizer machinery is classical.

It does **not** show that each subset of same-size posterior states is equivalent, and it cannot replace actual color-conditioned belief set constraints in the 20-frame minimax search. Paper A's finite radius-6 classification and Paper B's hard adaptive horizon retain priority.

## Evidence custody

- Independent executable finite family audit: `scripts/cuberev-observation/audit_r14_p55_parity_coupled_wreath_orbits.py`.
- Local receipt: 42 passed profile counts with five boundary examples, no third-party imports.
- New remote CI and Drive raw-byte verification: separate completion gates.
