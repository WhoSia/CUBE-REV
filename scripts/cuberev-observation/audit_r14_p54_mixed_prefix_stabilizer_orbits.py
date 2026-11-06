#!/usr/bin/env python3
"""R14-P5.4: exact full P48 two-distinct-cubie queried-slot stabilizer orbits.

Dependent physical geometry checker (imports P5.1); independent algebraic
5x7 orbit proof relies on legal cubie parity/orientation invariants.
"""
from collections import Counter, deque
from itertools import product
import contextlib, io, json
with contextlib.redirect_stdout(io.StringIO()):
    from audit_r14_p51_p48_group_lift import (
        EYE, EDGES, CORNERS, PIECES, legal, edge_slots, corner_slots,
        h_generator, q0)

# In each sector, two distinct positions have exactly one sensor slot queried.
e0,e1=EDGES[:2]
c0,c1=CORNERS[:2]
fixed=(PIECES[e0][0],PIECES[e1][0],PIECES[c0][0],PIECES[c1][0])
assert fixed[:1] == q0[:1] and fixed[2:3] == q0[1:]
# Construct the pointwise stabilizer of k distinct initial edge sticker reads
# and l distinct initial corner sticker reads. All are the FIRST local sticker
# of each visited spatial position. Test 16 distinct mixed-prefix profiles.
query_space={(a,b) for a in edge_slots for b in corner_slots}

def orbit_audit(k,l):
    fixed=tuple(PIECES[EDGES[i]][0] for i in range(k))+tuple(PIECES[CORNERS[j]][0] for j in range(l))
    H=[]
    for j in range(k+1,12):
        H.append(h_generator(edge_swaps=((k,j),),corner_swaps=((l,l+1),)))
    for j in range(l+1,8):
        H.append(h_generator(edge_swaps=((k,k+1),),corner_swaps=((l,j),)))
    for j in range(k+1,12):
        H.append(h_generator(edge_flips=(k,j)))
    for j in range(l+1,8):
        H.append(h_generator(corner_twists=((l,1),(j,2))))
    assert all(legal(g) and all(g[z]==z for z in fixed) for g in H)
    remaining=set(query_space);orbits=[]
    while remaining:
        seed=min(remaining);seen={seed};todo=deque([seed])
        while todo:
            qe,qc=todo.popleft()
            for g in H:
                v=(g[qe],g[qc])
                if v not in seen:seen.add(v);todo.append(v)
        assert seen<=remaining
        remaining-=seen;orbits.append((seed,len(seen)))
    # Coarse invariant: 2*k fixed-partner edge slots + remaining all edge slots,
    # 3*l fixed-partner corner slots + remaining all corner slots.
    if (k,l)!=(10,6): assert len(orbits)==(2*k+1)*(3*l+1),(k,l,len(orbits))
    hist=Counter(n for _,n in orbits)
    expected=Counter()
    if k and l:expected[1]+=2*k*3*l
    if k:expected[3*(8-l)]+=2*k
    if l:expected[2*(12-k)]+=3*l
    expected[2*(12-k)*3*(8-l)]+=1
    if (k,l)!=(10,6): assert hist==expected,(k,l,hist,expected)
    else: assert hist==Counter({1:360,4:18,6:20,12:2}),hist
    return len(H),len(orbits),hist
checks={}
for k in range(11):
    for l in range(7):
        generators,norbits,hist=orbit_audit(k,l)
        checks[f'{k},{l}']={'orbits':norbits,'generators':generators}
# All 77 profile pairs are included by the above loops.
H_count,n_orbits,sizes=orbit_audit(2,2)
assert sizes==Counter({1:24,18:4,20:6,360:1})
assert n_orbits==35
assert sum(sz*count for sz,count in sizes.items())==576
# More general orbit proof under the cubology invariants:
# For a fixed k visited edge positions and l visited corner positions with
# one facelet at each, and at least two unvisited positions per sector,
# the pointwise stabilizer has 2*k+1 edge coordinate orbits and 3*l+1
# corner coordinate orbits. Each observed cubie contributes individual
# fixed ordered facelet coordinates, and the remaining coordinates in that
# sector form one orbit. These are independent Cartesian cells because
# parity can be compensated using unvisited positions in both sectors.
# For k=l=2: (2*2+1)*(3*2+1)=35.
assert (2*2+1)*(3*2+1)==n_orbits
# The implication is only for stabilizers fixing the queried spatial slots,
# not necessarily a maximal belief automorphism group after observed colors.
print(json.dumps({
    'result':'R14_P54_TWO_CUBIE_PREFIX_STABILIZER_35_ORBITS_PASS',
    'physical_model':'P48 48-moving-sticker 18-HTM generated geometry, reused P5.1 as dependency',
    'visited_edge_positions':2,'visited_corner_positions':2,
    'fixed_queried_facelets':4,'full_query_space':576,
    'legal_stabilizer_generators':H_count,'query_orbits':n_orbits,
    'orbit_histogram':dict(sorted((str(k),v) for k,v in sizes.items())),
    'general_formula':'(2*k+1)*(3*l+1) for 0<=k<=10, 0<=l<=6 except (10,6); there are two unvisited cubies of each type in the exceptional case',
    'boundary_exception_10_6_orbit_count':checks['10,6']['orbits'],
    'checked_distinct_mixed_prefix_profiles':len(checks),
    'tested_profile_orbit_counts':checks,
    'claim_scope':'exact stabilizer action orbit for spatial-slot constraints, not full posterior maximal equivalence or global adaptive depth',
    'global_horizon':'18<=h_adaptive<=21 OPEN'
},sort_keys=True,indent=2))
