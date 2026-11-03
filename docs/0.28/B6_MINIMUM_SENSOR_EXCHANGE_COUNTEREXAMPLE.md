# P0.28 — Explicit B6 minimum-sensor basis-exchange obstruction

**Date:** 2026-11-03. **Status:** exact exchange-axiom counterexample
relative to the PREVIOUSLY certified 0.28 physical B6 positive and negative
layout results. New incidence-only finite verification PASS; no fresh
54-facelet or independent 18-HTM search is claimed.

## Why the classical literature matters

Cameron (1999), *Permutation Groups*, section 4.14, explicitly warns
that irredundant bases for permutation-group actions need not behave
like vector-space bases. In particular, basis-exchange axioms should
not be silently assumed. For CUBE-REV the issue is even sharper:
a radius-six sensor set is a restricted-radius identifying set,
which is weaker than a global permutation-group base.

The actual testable question is whether all minimum, radius-six,
16-tag physical sensor sets happen to form bases of a matroid on the
20 original fully oriented cubie tags.

## Geometric setup

Fix h=DL as the cube edge whose TWO endpoint corner tags are omitted.
The previously certified intrinsic B6 criterion admits exactly 13
pairs of omitted edge tags, split into geometric classes:

    N-N (4), F-F (4), F-h* (4), P-P (1).

Every admissible pair defines a 16-tag sensor set by observing the
remaining six corner tags and ten edge tags.

Let

    A = all 20 tags minus {DL endpoint corners, FR, UR};
    B = all 20 tags minus {DL endpoint corners, DR, UL}.

Here A's missing edge pair {FR,UR} is valid F-h*; B's missing edge
pair {DR,UL} is valid P-P. Thus they are two B6-injective 16-tag
sensor sets according to the previously sealed 41-goal positive
certificate (not re-executed here).

## Concrete violation

The sensor x=DR belongs to A minus B. The potential exchange
sensors y in B minus A are precisely FR and UR. There are only two
ways to form a putative matroid-exchange basis A-x+y:

    A - {DR} + {FR} : omitted edges {DR,UR} -> class P-h*, B6 FAIL;
    A - {DR} + {UR} : omitted edges {DR,FR} -> class P-F, B6 FAIL.

Both failures are covered by the earlier physical 19 negative-witness
orbits and the 576-candidate geometric bridge; they are NOT merely
missed from the geometric-positive list by convention.

There is therefore no y in B minus A such that A-x+y remains a
radius-six 16-sensor basis. This directly contradicts matroid
basis exchange for the actual B6 sensor family (assuming the
pre-existing physical positive/negative certificates, as above).

This counterexample does NOT require claiming that every conceivable
16-tag candidate was newly enumerated. It requires only the TWO
named actual positives and the TWO named physical negatives.

## Full light finite audit

Code: scripts/cuberev-observation/verify_b6_basis_exchange_failure.py

For every fixed omitted-corner edge h, the 13 admissible omitted-edge
pairs define the same finite basis-exchange problem up to physical
cube rotations. There are exactly 176 violating ordered
(A_omissions, B_omissions, x_observed) triples per h, hence

    12 * 176 = 2,112

over all 12 choices of h, counting labelled core edges (not quotient
orbits). A negative control with the complete 66-pair uniform family
has ZERO violations. The code distinguishes observed sensor exchange
from omitted pair exchange: if x is observed in A but absent in B,
then x is in E_B minus E_A and exchange with y in E_A minus E_B
changes omissions E_A to (E_A minus y) union x.

The graph of allowed omitted edge pairs for any h is the earlier
W5 disjoint union C4 disjoint union K2 disjoint union K1.
The disconnected positive-edge graph provides conceptual intuition
for why rank-two matroid exchange fails, but the explicit four-tag
counterexample above is the actual proof.

## Scientific status and limitations

- This is a new specific elementary mathematical consequence of
  earlier B6 finite certificates, NOT the discovery that permutation
  group bases in general can violate exchange (classical prior art).
- The criterion's equivalence to actual B6 positive/negative
  physical sensor validity depends on archived 54-facelet replay
  and the previous full B6 positive proof, not on today's code alone.
- Failure of a matroid axiom means greedy sensor exchange and
  matroid rank/exchange algorithms cannot be invoked on this B6
  family without new problem-specific correctness proofs.
- Neither this result nor the abstract stabilizer support census
  proves the 41-class original 18-HTM shortest-distance lower bound
  with a wholly independent physical engine.

## Next falsification and exploration

1. Physically replay the two named negative exchange designs with
   explicit <=6 + <=6 face-turn collision words and verify their
   exact original-tag difference masks using a second cube engine.
2. Independently recheck that A and B are B6-injective via 41-target
   geodesic lower-bound witnesses or an independent B6 54-facelet
   projection census.
3. Investigate whether a weaker combinatorial exchange structure,
   greedoids, delta-matroids or a specifically proved hypergraph
   relaxation is valid. Do not *assume* any such structure; obtain
   a proof or a small countermodel.
4. Compare the radius-five B5 16-tag layout family to B6 under the
   SAME exchange predicate. A radius-dependent exchange failure
   could expose a useful transition mechanism, but is not yet
   established by this note.
