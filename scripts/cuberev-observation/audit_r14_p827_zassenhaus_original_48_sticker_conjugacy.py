"""Source-first six-turn 48-sticker conjugacy test of Zassenhaus (1982).
The six historical permutations are transcribed from Physica 114A pp629-637,
PDF Drive ID 1i0gVO3XuLtBYZSknKCaMChTXJ641D59U.
The reference physical 3D turns are independently generated from coordinates.
"""
from itertools import permutations,product
import json
H=[
[(1,2,3,4),(9,10,11,12),(17,18,19,20),(-1,-2,-3,-4),(-13,-14,-15,-16)],
[(10,13,8,19),(18,21,16,3),(2,5,24,11),(-8,-14,-18,-9),(-20,-2,-6,-21)],
[(20,11,16,7),(4,19,24,15),(12,3,8,23),(-15,-20,-12,-19),(-3,-8,-24,-7)],
[(9,14,5,18),(17,22,13,2),(1,6,21,10),(-5,-10,-6,-13),(-17,-22,-18,-1)],
[(12,15,6,17),(20,23,14,1),(4,7,22,9),(-7,-11,-17,-16),(-19,-23,-5,-4)],
[(21,22,23,24),(5,6,7,8),(13,14,15,16),(-21,-22,-23,-24),(-9,-10,-11,-12)],
]
labels=tuple(range(1,25))+tuple(range(-1,-25,-1))
assert len(labels)==48
label_ix={l:i for i,l in enumerate(labels)}
def perm_from_cycles(cycles):
    a=list(range(48))
    for cycle in cycles:
        for i,j in zip(cycle,cycle[1:]+cycle[:1]):
            a[label_ix[i]]=label_ix[j]
    return tuple(a)
Hist=[perm_from_cycles(c) for c in H]
assert all(sum(a[i]!=i for i in range(48))==20 for a in Hist)
assert all(set(range(48))==set(a) for a in Hist)
normal={'U':(0,1,0),'R':(1,0,0),'F':(0,0,1),'D':(0,-1,0),'L':(-1,0,0),'B':(0,0,-1)}
def dot(a,b):return sum(x*y for x,y in zip(a,b))
slots=tuple((p,normal[f]) for p in product((-1,0,1),repeat=3)
            if sum(v!=0 for v in p) in (2,3) for f in 'URFDLB' if dot(p,normal[f])==1)
assert len(slots)==48
ix={x:i for i,x in enumerate(slots)}
def rot(p,axis,power):
    x,y,z=p
    for _ in range(power%4):
        if axis==0:y,z=-z,y
        elif axis==1:x,z=z,-x
        else:x,y=-y,x
    return (x,y,z)
def make_phys(f,clock_sign=1):
    n=normal[f];axis=next(i for i,z in enumerate(n) if z)
    return tuple(ix[(rot(p,axis,-n[axis]*clock_sign),rot(v,axis,-n[axis]*clock_sign))]
                 if p[axis]==n[axis] else ix[(p,v)] for p,v in slots)
# Original historical positive-index and negative-index stickers remain invariant
# under generator actions: two distinct components (24 each).
assert all(all((i<24)==(p[i]<24) for i in range(48)) for p in Hist)

# To test conjugacy via an unconstrained labelling of 48 stickers:
# Pick each possible mapping of six source generators to six physical faces
# together with the quarter-turn directions. Conjugacy must satisfy
# bijection pi:  pi(H_i(s)) = PhysicalFace_i(pi(s)), ALL six i and 48 s.
# Build pi by orbital propagation seeded at one source corner and one edge.
faces='URFDLB'
physical={f:{1:make_phys(f,1),-1:make_phys(f,-1)} for f in faces}
# candidate face maps filtered by commutation relation (opposite turn pairs)
def commute(p,q):return all(p[q[i]]==q[p[i]] for i in range(48))
hopp={tuple(sorted((i,j))) for i in range(6) for j in range(i+1,6) if commute(Hist[i],Hist[j])}
assert len(hopp)==3,hopp
popp={tuple(sorted((a,b))) for a in faces for b in faces if a<b and commute(physical[a][1],physical[b][1])}
assert len(popp)==3,popp
# Source orbit classifier by graph closure

def closure(start,acts):
    out={start};stack=[start]
    while stack:
        x=stack.pop()
        for p in acts:
            y=p[x]
            if y not in out:out.add(y);stack.append(y)
    return out
assert closure(0,Hist)==set(range(24))
assert closure(24,Hist)==set(range(24,48))
C={i for i,(p,_) in enumerate(slots) if sum(x!=0 for x in p)==3}
E=set(range(48))-C
assert len(C)==len(E)==24

def propagate(gens,seed_s,seed_t):
    pi={seed_s:seed_t};todo=[seed_s]
    while todo:
        i=todo.pop();j=pi[i]
        for h,p in zip(Hist,gens):
            ni=h[i];nj=p[j]
            if ni in pi:
                if pi[ni]!=nj:return None
            else:
                if nj in pi.values():return None
                pi[ni]=nj;todo.append(ni)
    return pi
solutions=[]
for assignment in permutations(faces):
    if {tuple(sorted((i,j))) for i in range(6) for j in range(i+1,6)
        if tuple(sorted((assignment[i],assignment[j]))) in popp}!=hopp:continue
    # We also permit inverse turns, since historical turn arrows may be opposite.
    for dirs in product((-1,1),repeat=6):
        gens=[physical[f][sgn] for f,sgn in zip(assignment,dirs)]
        first=None
        for candidate in C:
            first=propagate(gens,0,candidate)
            if first is not None and len(first)==24:break
        if first is None or len(first)!=24:continue
        second=None
        for candidate in E:
            second=propagate(gens,24,candidate)
            if second is not None and len(second)==24:break
        if second is None or len(second)!=24:continue
        mapping=dict(first,**second) if False else {**first,**second}
        assert len(mapping)==48 and len(set(mapping.values()))==48
        assert all(mapping[h[i]]==p[mapping[i]] for h,p in zip(Hist,gens) for i in range(48))
        solutions.append({'source_T1_to_T6_faces':''.join(assignment),'turn_direction_signs':dirs,
                          'source_label_to_physical_sticker_slot':{str(labels[i]):mapping[i] for i in range(48)}})
# Complete, not first-witness-only, isomorphism enumeration. For EVERY
# permitted face/direction renaming, each of the two transitive 24-sticker
# orbits may carry an independent commuting relabelling (gauge).
# Enumerate all 24 corner-sticker seed images and all 24 edge seed images.
all_maps=[]
for entry in solutions:
    facenames=entry['source_T1_to_T6_faces']
    directions=entry['turn_direction_signs']
    gens=[physical[f][sgn] for f,sgn in zip(facenames,directions)]
    cmaps=[pi for seed in sorted(C) if (pi:=propagate(gens,0,seed)) is not None and len(pi)==24]
    emaps=[pi for seed in sorted(E) if (pi:=propagate(gens,24,seed)) is not None and len(pi)==24]
    assert len(cmaps)==3 and len(emaps)==2, (facenames,len(cmaps),len(emaps))
    for cm in cmaps:
        for em in emaps:
            pi={**cm,**em}
            assert len(pi)==48 and len(set(pi.values()))==48
            assert all(pi[h[i]]==f[pi[i]] for h,f in zip(Hist,gens) for i in range(48))
            all_maps.append({'source_T1_to_T6_faces':facenames,
                             'turn_direction_signs':directions,
                             'source_label_to_physical_sticker_slot':{str(labels[i]):pi[i] for i in range(48)}})
assert len(solutions)==48
assert len(all_maps)==288
# A fixed historical face-generator alignment leaves exactly six possible
# original sticker-label maps, not just one: 3 global corner-sticker rotations
# x 2 global edge-sticker swaps. This is the centralizer of the P48 turn action.
assert len({(x['source_T1_to_T6_faces'],tuple(x['turn_direction_signs'])) for x in all_maps})==48
assert len({tuple(x['source_label_to_physical_sticker_slot'][str(i)] for i in labels) for x in all_maps})==288
assert sorted(set(tuple(x['turn_direction_signs']) for x in solutions))==[(-1,)*6,(1,)*6]

print(json.dumps({'status':'PASS','source':'Zassenhaus 1982 Physica 114A 629-637','turns':6,
                  'historical_turns_supports':[sum(x!=i for i,x in enumerate(h)) for h in Hist],
                  'historical_opp_pairs':[list(x) for x in sorted(hopp)],
                  'distinct_face_label_and_direction_assignments':len(solutions),
                  'centralizer_size_fixed_face_assignment':6,
                  'independent_corner_sticker_gauge_choices':3,
                  'independent_edge_sticker_gauge_choices':2,
                  'total_explicit_P48_generator_conjugacies':len(all_maps),
                  'first_solution':all_maps[0]},ensure_ascii=False,indent=2))
