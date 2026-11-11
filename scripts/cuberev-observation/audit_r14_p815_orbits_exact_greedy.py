#!/usr/bin/env python3
"""CUBE-REV R14-P8.15: 24-rotation orbits and exact greedy B6 deletion law.

This enumerates geometry and rational Markov probabilities CONDITIONAL on
historical complete physical B6 16-tag/short-support certificates. It
does NOT rerun P48 B12 distances or supply a Lean kernel receipt.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
import json
import random

F={'U':(0,1,0),'R':(1,0,0),'F':(0,0,1),
   'D':(0,-1,0),'L':(-1,0,0),'B':(0,0,-1)}
EDGES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
CORNERS=tuple(product((-1,1),repeat=3))
def mid(e): return tuple(F[e[0]][i]+F[e[1]][i] for i in range(3))
def ends(e):
    p=mid(e);k=p.index(0)
    return frozenset(tuple(s if j==k else p[j] for j in range(3)) for s in (-1,1))
ENDS={e:ends(e) for e in EDGES}
MID_TO_EDGE={mid(e):e for e in EDGES}
def allowed(h,a,b):
    c=ENDS[h]
    opposite=frozenset(tuple(-v for v in p) for p in c)
    other=next(e for e in EDGES if ENDS[e]==opposite)
    near={e for e in EDGES if e!=h and ENDS[e]&c}
    far={e for e in EDGES if e!=other and ENDS[e]&opposite}
    parallel={e for e in EDGES if e not in (h,other)
              and mid(e).index(0)==mid(h).index(0)}
    vertex=min(c)
    return ((a in near and b in near and ((vertex in ENDS[a])!=(vertex in ENDS[b])))
            or (a in far and b in far and bool(set(a)&set(b)))
            or (a==other and b in far) or (b==other and a in far)
            or ({a,b}==parallel))
P={h:{frozenset((a,b)) for a,b in combinations(EDGES,2)
      if allowed(h,a,b)} for h in EDGES}
assert all(len(p)==13 for p in P.values())
tags=frozenset({('C',c) for c in CORNERS}|{('E',e) for e in EDGES})
p4=frozenset(frozenset({('C',c) for c in ENDS[h]}|
                      {('E',e) for e in q}) for h in EDGES for q in P[h])
assert len(p4)==156
p3={frozenset({('C',c)}|{('E',e) for e in q})
    for c in CORNERS for q in combinations(EDGES,2)}
p3|={frozenset({('C',c) for c in ENDS[h]}|{('E',e)})
     for h in EDGES for e in EDGES}
p2={frozenset(q) for q in combinations(tags,2)
    if sum(t=='C' for t,_ in q)<2
    or any(ENDS[h]==frozenset(v for t,v in q if t=='C') for h in EDGES)}
levels={0:{frozenset()},1:{frozenset({x}) for x in tags},
        2:p2,3:p3,4:p4}
assert [len(levels[k]) for k in range(5)]==[1,20,174,672,156]
minimal17={o for o in p3 if not any(o|{t} in p4 for t in tags-o)}
assert len(minimal17)==276

rotations=[]
for axes in permutations(range(3)):
    parity=(-1)**sum(axes[i]>axes[j] for i in range(3) for j in range(i+1,3))
    for signs in product((-1,1),repeat=3):
        if parity*signs[0]*signs[1]*signs[2]==1:
            rotations.append((axes,signs))
assert len(rotations)==24
def turn(x,r):
    axes,signs=r
    return tuple(signs[i]*x[axes[i]] for i in range(3))
def moved(o,r):
    return frozenset((typ,turn(v,r) if typ=='C' else
                      MID_TO_EDGE[turn(mid(v),r)]) for typ,v in o)
assert all(moved(o,r) in minimal17 for o in minimal17 for r in rotations)
def orbits_of(s):
    remain=set(s);answer=[]
    while remain:
        origin=next(iter(remain))
        orbit={moved(origin,r) for r in rotations}
        assert orbit<=remain
        remain-=orbit
        answer.append(orbit)
    assert sum(map(len,answer))==len(s)
    return answer
orbit17=orbits_of(minimal17)
orbit16=orbits_of(p4)
assert Counter((sum(t=='C' for t,v in next(iter(o))),len(o)) for o in orbit17)=={
    (1,24):11,(2,12):1}
assert len(orbit16)==8

# Rational, NOT Monte Carlo: start with 20 sensors and choose uniformly
# among CURRENTLY removable sensors until none remains.
weight={frozenset():Fraction(1)}
terminal={}
for k in range(5):
    for omission in levels[k]:
        p=weight.get(omission,Fraction())
        actions=[omission|{tag} for tag in tags-omission
                 if omission|{tag} in levels.get(k+1,set())]
        if not actions:
            terminal[omission]=p
        else:
            for child in actions:
                weight[child]=weight.get(child,Fraction())+p/len(actions)
assert sum(terminal.values())==1
assert set(terminal)==minimal17|set(p4)
p16=sum((terminal[o] for o in p4),Fraction())
p17=sum((terminal[o] for o in minimal17),Fraction())
assert p16==Fraction(1166,1995) and p17==Fraction(829,1995)
assert sum(terminal.values())==p16+p17
assert Counter((sum(t=='C' for t,v in next(iter(orb))),len(orb),
                str(sum((terminal[x] for x in orb),Fraction())))
               for orb in orbit17)=={
  (1,24,'241/6650'):11,
  (2,12,'337/19950'):1}
# All 264 minimal 1C2E outcomes have exactly the same probability
# but the 156 MINIMUM 16-tag outcomes do NOT.
assert len({terminal[o] for o in minimal17
            if sum(t=='C' for t,v in o)==1})==1
min16_weight_hist=Counter(str(terminal[o]) for o in p4)
assert min16_weight_hist=={
 '8143/2872800':48,'53/11970':48,'2843/718200':24,
 '53/17955':24,'1397/239400':12}
assert all(len({terminal[o] for o in orb})==1 for orb in orbit16+orbit17)

# Independent seeded simulation as a diagnostic, not a substitute for
# the exact rational recurrence.
rng=random.Random(20261110)
draws=100000
hits=Counter()
for _ in range(draws):
    o=frozenset()
    while True:
        # Stable ordering is required for a reproducible seeded Monte Carlo
        # receipt across distinct PYTHONHASHSEED / interpreter processes.
        actions=sorted((o|{t} for t in tags-o
                        if o|{t} in levels.get(len(o)+1,set())),
                       key=lambda x: tuple(sorted(x)))
        if not actions:
            hits[20-len(o)]+=1
            break
        o=rng.choice(actions)
assert abs(Fraction(hits[16],draws)-p16)<Fraction(1,125)
def priority_greedy(preferred_type):
    """Choose uniformly among currently removable sensors of preferred type,
    falling back to the other type only if none is removable. Exact rational.
    """
    masses={frozenset():Fraction(1)}
    terminal_sizes=Counter()
    for k in range(5):
        for omitted in levels[k]:
            p=masses.get(omitted,Fraction())
            candidates=[(t,omitted|{t}) for t in tags-omitted
                        if omitted|{t} in levels.get(k+1,set())]
            preferred=[new for t,new in candidates if t[0]==preferred_type]
            nexts=preferred if preferred else [new for t,new in candidates]
            if not nexts:
                terminal_sizes[20-len(omitted)]+=p
            else:
                for new in nexts:
                    masses[new]=masses.get(new,Fraction())+p/len(nexts)
    assert sum(terminal_sizes.values())==1
    return terminal_sizes
corner_priority=priority_greedy('C')
edge_priority=priority_greedy('E')
assert corner_priority[16]==Fraction(11,12)
assert corner_priority[17]==Fraction(1,12)
assert edge_priority[16]==Fraction(1,2)
assert edge_priority[17]==Fraction(1,2)

# Constructive explanation of 11/12: after two adjacent corners are
# omitted, all 12 first edge omissions are possible; exactly the core
# edge h is isolated from every admissible second omitted edge.
assert all(frozenset(EDGES)-set().union(*P[h])=={h} for h in EDGES)

print(json.dumps({
 "status":"R14_P815_ORBITS_EXACT_GREEDY_GEOMETRY_PASS",
 "conditional_on":"historic full physical B6 certificate",
 "all_positive_states_examined":sum(len(levels[k]) for k in levels),
 "proper_rotations":24,"minimal17_orbits":12,"minimum16_orbits":8,
 "minimal17_orbit_sizes":{"1_corner_2_edges":[24]*11,"2_corners_1_edge":[12]},
 "prob_minimum16":str(p16),"prob_minimal17":str(p17),
 "expected_sensor_count":str(16*p16+17*p17),
 "minimum16_per_layout_probability_histogram":dict(min16_weight_hist),
 "seeded_monte_carlo_samples":draws,"seeded_monte_carlo_16":hits[16],
 "physical_41_distance_classes_replayed":False,
 "lean_kernel_proven":False
},sort_keys=True))
