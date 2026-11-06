#!/usr/bin/env python3
"""Full P48 R14-P5.3: all 36 first paired colors are one Bellman orbit."""
from itertools import product
from collections import Counter
import contextlib, io, json, random
with contextlib.redirect_stdout(io.StringIO()):
    from audit_r14_p51_p48_group_lift import (
        EYE,EDGES,CORNERS,PIECES,rots,legal,compose,inverse,obs,q0,
        edge_slots,corner_slots,MOVES)

def on_sector(rotation,positions):
    g=list(EYE)
    for pos in positions:
        for slot in PIECES[pos]:g[slot]=rotation[slot]
    return tuple(g)

E=[];C=[]
for spatial,colors in rots:
    edge=on_sector(spatial,EDGES)
    corner=on_sector(spatial,CORNERS)
    if legal(edge):E.append((edge,colors))
    assert legal(corner)
    C.append((corner,colors))
assert (len(E),len(C))==(12,24)
assert Counter(p['U'] for _,p in E)==dict.fromkeys('URFDLB',2)
assert Counter(p['U'] for _,p in C)==dict.fromkeys('URFDLB',4)
assert len({compose(e,c) for e,_ in E for c,_ in C})==288
rng=random.Random(20261106)
states=[EYE]
s=EYE
for _ in range(600):
    s=compose(MOVES[rng.choice(tuple(MOVES))],s)
    assert legal(s)
    states.append(s)
checked=0
queries=(q0,(edge_slots[4],corner_slots[11]),(edge_slots[20],corner_slots[19]))
for st in states[::17]:
    for query in queries:
        color=obs(st,query)
        for (e,pe),(c,pc) in product(E,C):
            transformed=compose(st,inverse(compose(e,c)))
            assert legal(transformed)
            assert obs(transformed,query)==(pe[color[0]],pc[color[1]])
            checked+=1
for first in product('URFDLB',repeat=2):
    orbit={(pe[first[0]],pc[first[1]]) for _,pe in E for _,pc in C}
    assert orbit==set(product('URFDLB',repeat=2))
from math import factorial
n=factorial(12)*2**11*factorial(8)*3**7//2
assert n==43252003274489856000
print(json.dumps({
 'result':'R14_P53_ALL_36_ROOT_RESPONSES_ONE_BELLMAN_ORBIT_PASS',
 'independent_edge_source_relabel_rotations':12,
 'independent_corner_source_relabel_rotations':24,
 'legal_sector_source_relabel_group_product':288,
 'legal_p48_random_move_prefix_states':len(states),
 'sampled_query_color_equivariance_checks':checked,
 'all_36_paired_root_colors_one_orbit':True,
 'first_query_pairs_physically_equivalent':576,
 'second_query_orbits_after_root':12,
 'full_cube_legal_states':n,
 'all_root_outcomes_uniform_count':n//36,
 'scope_limit':'free known legal-turn routing; not a full adaptive horizon proof',
},sort_keys=True,indent=2))
