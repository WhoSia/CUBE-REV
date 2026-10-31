#!/usr/bin/env python3
"""N-F mixed-obstruction orbit classification by three binary invariants.

No archived B5/B6 labels: standalone Q3 combinatorics.  A fourth check
shows the orientation-reversing stabilizer toggles the third invariant.
"""
from itertools import product,permutations
from collections import defaultdict
V=list(product((-1,1),repeat=3))
E=list(dict.fromkeys(frozenset((a,b)) for a in V for b in V
    if sum(x!=y for x,y in zip(a,b))==1))
assert len(E)==12
h=frozenset(((-1,-1,-1),(-1,-1,1)))
star=frozenset(((1,1,-1),(1,1,1)))
N=[e for e in E if e!=h and e&h]
F=[e for e in E if e!=star and e&star]
assert len(N)==len(F)==4
maps=[]
for p in permutations(range(3)):
 parity=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 for s in product((-1,1),repeat=3):
  det=parity*s[0]*s[1]*s[2]
  fn=lambda v,p=p,s=s:tuple(s[i]*v[p[i]] for i in range(3))
  if frozenset(map(fn,h))==h:maps.append((det,fn))
assert len(maps)==4
H=[fn for det,fn in maps if det==1]
K=[fn for det,fn in maps]
assert len(H)==2

def label(e,side):
 endpoint=next(v for v in e if v in side)
 axis=next(i for i in range(3) if len({v[i] for v in e})==2)
 assert axis in (0,1)
 return endpoint[2],axis

def signature(n,f):
 (z1,a1),(z2,a2)=label(n,h),label(f,star)
 return (z1*z2,a1==a2,z1*(1 if a1==0 else -1))

families=defaultdict(set)
for n in N:
 for f in F:
  families[signature(n,f)].add((n,f))
assert len(families)==8 and all(len(v)==2 for v in families.values())
for key,types in families.items():
 representative=next(iter(types))
 orbit={(frozenset(map(fn,representative[0])),
         frozenset(map(fn,representative[1]))) for fn in H}
 assert orbit==types
 for det,fn in maps:
  n,f=representative
  mirror=(frozenset(map(fn,n)),frozenset(map(fn,f)))
  nextkey=signature(*mirror)
  if det==1:assert nextkey==key
  else:assert nextkey==key[:2]+(-key[2],)
full_orbits=set()
for n in N:
 for f in F:
  full_orbits.add(frozenset(
   (frozenset(map(fn,n)),frozenset(map(fn,f))) for fn in K))
assert len(full_orbits)==4 and all(len(o)==4 for o in full_orbits)
print("PASS all 16 N-F pairs classified by exactly 8 three-bit signatures")
print("PASS proper stabilizer C2 orbits all size2")
print("PASS full stabilizer C2xC2 orbits all size4")
print("PASS mirror reflection toggles only the third / chirality bit")
