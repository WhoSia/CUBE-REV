#!/usr/bin/env python3
"""New P12 short triangle-pair certificate (finite list as premise).
The original 17-profile completeness / physical 18-HTM semantic bridge
remain separate finite and formal proof obligations.
"""
import json
from itertools import combinations
from pathlib import Path
P=Path(__file__).resolve().parents[2]
C=json.loads((P/'docs/0.16/P12_CORE_CERTIFICATE.json').read_text())
profile={int(k):v for k,v in C["light_profiles_17_with_multiplicity"].items()}
assert len(profile)==17 and sum(profile.values())==3008
edges={frozenset(i for i in range(8) if not (p>>i&1))
       for p in profile if p.bit_count()==6}
T1=[1,3,7];T2=[2,4,6]
triangle_edges=lambda t:{frozenset(e) for e in combinations(t,2)}
outer={frozenset(t) for t in [(0,2),(0,4),(1,5),(5,7)]}
assert len(edges)==10
assert edges==triangle_edges(T1)|triangle_edges(T2)|outer
def cover(b):
    return all(any((b>>i)&1 for i in e) for e in edges)
covers=[b for b in range(256) if b.bit_count()==4 and cover(b)]
assert covers==[150]  # exactly one minimum vertex cover
# Human implication: each disjoint triangle needs 2 vertices; four total
# bars outside vertices 0,5; the exterior edges force 2,4 and 1,7.
assert set(i for i in range(8) if 150>>i&1)=={1,2,4,7}
# Affine F2^3 structure of the SEVEN weight-four profiles.
p4={p for p in profile if p.bit_count()==4}
affine=lambda a,parity:sum(1<<i for i in range(8)
   if ((i&a).bit_count()&1)==parity)
affine_family={affine(a,k) for a in (1,3,5,7) for k in (0,1)}
assert len(affine_family)==8 and p4==affine_family-{150}
assert affine(7,0)==105 and affine(7,1)==150
assert all(not (p&150)==150 for p in profile)
print('P12_TWO_DISJOINT_TRIANGLES_UNIQUE_FOUR_COVER_PASS')
print('P12_FOUR_BIT_PROFILES_AFFINE_F2_COSSETS_SEVEN_OF_EIGHT_PASS')
print('GRAPH_EDGES',len(edges),'UNIQUE_FOUR_COVER',covers,
      'MISSING_AFFINE_HYPERPLANE',150)
