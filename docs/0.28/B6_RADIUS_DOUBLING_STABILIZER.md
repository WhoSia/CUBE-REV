# B6 as a short-word pointwise-stabilizer problem

Status: **exact group-theoretic equivalence, not an independent B6 HTM lower-bound proof**.
Uses the original 3x3 cube, 18-HTM distance and original-tagged cubies with
full position+orientation observations. No alternate observation protocol.

## 1. Exact radius doubling theorem

Let G be any group with a finite symmetric generator alphabet A, and B_r
its word ball. Let G act faithfully on oriented tagged objects on the LEFT.
For a set S of original observable tagged objects, let

    H_S = {g in G : g(s)=s for every s in S}.

Then the map x -> (x(s))_{s in S} is injective on B_r if and only if

    H_S intersect B_{2r} = {identity}.

Proof: equality of sensor outputs from x,y in B_r is equivalent to
x^-1*y fixing every s. Triangle inequality bounds |x^-1*y|<=2r.
Conversely, any g in B_{2r} has a geodesic word decomposed g=u*v with
|u|<=r, |v|<=r. Let x=u^-1, y=v, then x,y in B_r, x^-1*y=g, and
their selected original-tag observations agree. Symmetry of the alphabet
guarantees |u^-1|=|u|. QED.

Key exact set identity: B_r^-1 B_r = B_{2r} (for the symmetric HTM alphabet).
The equality includes, but is not exhausted by, pairs at exactly depth r.

## 2. Only twelve FULL-cube states lie in the 16-sensor stabilizer

Fix 16 observed original cubies; omit two distinct original corner tags
and two distinct original edge tags, with all other tags fixed in both
location and orientation. Standard solvability constraints for a 3x3 cube:
(1) corner and edge permutation parity agree; (2) sum of corner twists is
zero mod 3; (3) sum of edge flips is zero mod 2.

Only two corner positions and two edge positions are unobserved.
Each pair's permutation is identity or a transposition, and matching
parity forces the two swaps to happen simultaneously or neither to happen:
2 choices total. The corner twists on the two unobserved corners have
3 possibilities (t,-t mod3); edge flips have 2 (f,f mod2).
Every such configuration is legal in the standard cube group, so

    |H_S| = 2*3*2 = 12, with 11 nonidentity targets.

These are the full legal *states* compatible with preserving 16 selected
original oriented cubie tags, not all 12 reachable in <=12 moves.
They form a pointwise stabilizer subgroup; this subgroup order is fixed,
but word distances of its elements depend on which four tags are omitted.

For radius 6, exact identifiability is equivalent to all 11 targets having
HTM word distance >=13. This is much smaller in number of target states
than pairwise comparison of all 8,240,087 B6 states, but checking short
word NONEXISTENCE for a specified target remains a hard separate obligation.

## 3. The historic 66=18+35+13 now has a word-metric meaning

Fix two omitted adjacent corner tags (the endpoints of edge h), and omit
two edge tags. There are 66 choices. The prior certified B5 and B6
obstruction filtration, plus the separate B6 positive full-state census,
implies the following statement about

    d(S) = min{|g|_HTM : g in H_S and g != identity}:

- 18 old B5 failures: d(S) <= 10.
- 35 B5 successes that newly fail at B6: 11 <= d(S) <= 12.
- 13 B6 successes: d(S) >= 13.

This is a faithful *reformulation* of the existing historical evidence,
not a new source-independent proof of d(S)>=13 for the successful 13.
Existing B6 negative witnesses (19 physical support orbits) construct
specific g in H_S intersect B12; the B6 full-state positive census proves
the absence of such elements for the remaining 13.

The existing four-case relative geometry rule gives the thirteen as:
N-N 4, F-F 4, F-h* 4, P-P 1, per omitted corner edge h.
The actual theoretical gap is to derive the corresponding >=13 word
metric lower bound by a short independent human/checkable certificate.

## 4. Important chronological convention: shared first moves

Physical face turns act on ORIGINAL tags by left composition. If two
chronological words share their FIRST executed move p, write their full
transformations as x=A*p and y=B*p. Then the element fixing the
observed original tags is

    x^-1*y = p^-1 * A^-1 * B * p,

NOT simply A^-1*B. The latter is a conjugate and may not fix the same
original tags. HTM word length is invariant under rigid cube-frame
symmetries, but NOT generally under conjugation by arbitrary face turns.

Consequently a formal '10-move relative' expression obtained by
cancelling a shared early chronological prefix is NOT automatically a
<=10-move stabilizer witness at the same original-tag set; that would
contradict the B5-injective N-F cases. In contrast, if the two
chronological witness words had the SAME LAST executed move, that final
bijection could be canceled without changing which original tags agree.
The four archived N-F seed pairs share their first, not their last move.

See test_b6_word_order.py for a small explicit S4 countermodel.

## 5. Evidence dependencies and next gate

- verify_b6_geometric_rule.py: source of existing four-case geometry.
- verify_b6_geometric_bridge.py: physical 19-orbit negative witnesses.
- verify_b6_16_bases.cpp: positive B6 injectivity from 8,240,087 states.
- verify_b6_nf_four_seeds.py: explicit 6-vs-6 HTM witness family.
- test_b6_radius_stabilizer.py: independent small S3/S4 exhaustive
  verification of radius doubling, plus 12-state legal cube configuration
  count. It does NOT compute 3x3 HTM distances.
- test_b6_word_order.py: correct left-action conjugation convention.

**Next worthwhile target:** For the EIGHT historically positive proper-rotation
orbit representatives, individually certify that all 11 nonidentity
stabilizer states have HTM distance >=13. That is at most 8*11=88
target exclusions before further symmetry reduction, instead of rerunning
millions of paired B6 projections. Exact distance proof machinery
(PDB, verified bidirectional bounded search, or proof-producing SAT)
must be chosen and independently verified. The number 88 is a proposed
workload, not a completed verification.

No fresh B6 hardness claim, no new ad hoc invariant, and no new protocol.
