#!/usr/bin/env python3
"""Verify B7 MIDPOINT tagged-cubie difference supports, not just end-state supports.

Requires verify_short_support_phase.py in the same directory.
The source of the witness words is existing cubing algorithm literature.
No claim of complete B7 census or HTM shortest-word optimality.
"""
from itertools import combinations
from verify_short_support_phase import (
    WORDS, initial, play, factors, proper24
)

EDGE13=[
 "L F R' F' L' U2 R U R U' R2 U2 R",
 "U F U F2 D' L' U' L U D F2 U2 F'",
 "F R' F' L' U2 R U R U' R2 U2 R L",
]

def invert(seq):
 return [m[:-1] if m.endswith("'") else m if m.endswith('2') else m+"'"
         for m in reversed(seq)]

def midpoint_support(word,k):
 moves=word.split()
 a=factors(play(' '.join(invert(moves[:k]))))
 b=factors(play(' '.join(moves[k:])))
 return {tag for tag in a if a[tag]!=b[tag]}

def main():
 base=factors(initial())
 rot=proper24()
 edge_positions={tag:v[0] for tag,v in base.items() if len(tag)==2}
 orbits={}
 for i,word in enumerate(EDGE13):
  endpoint={t for t in base if base[t]!=factors(play(word))[t]}
  assert len(endpoint)==2 and all(len(t)==2 for t in endpoint)
  for k in (6,7):
   diff=midpoint_support(word,k)
   assert len(diff)==2 and all(len(t)==2 for t in diff)
   midpoint_positions=[edge_positions[t] for t in diff]
   orb=frozenset(frozenset(R(p) for p in midpoint_positions) for R in rot)
   orbits.setdefault(orb,[]).append((i,k))
   print('word',i+1,'cut',k,'tags',sorted(diff),'orbit',len(orb))
 assert sorted(map(len,orbits))==[12,12,24]
 certified=set().union(*orbits)
 assert len(certified)==48

 # A cube edge is parallel to the coordinate axis where its midpoint is zero.
 # The 12 edges therefore split into three parallelism classes of four.
 groups={axis:[pos for pos in edge_positions.values() if pos[axis]==0]
         for axis in range(3)}
 assert sorted(map(len,groups.values()))==[4,4,4]
 all_nonparallel={frozenset((a,b))
     for a,b in combinations(edge_positions.values(),2)
     if next(i for i,x in enumerate(a) if x==0)!=next(i for i,x in enumerate(b) if x==0)}
 assert len(all_nonparallel)==48 and certified==all_nonparallel
 all_pairs={frozenset((a,b)) for a,b in combinations(edge_positions.values(),2)}
 assert len(all_pairs)==66 and len(all_pairs-certified)==18

 for name,k,expected in [
     ('face_diagonal_corners_12',6,12),
     ('body_diagonal_corners_12',6,4),
     ('adjacent_corners_14',7,12)]:
  diff=midpoint_support(WORDS[name],k)
  assert len(diff)==2 and all(len(t)==3 for t in diff)
  positions=[base[t][0] for t in diff]
  orb={frozenset(R(p) for p in positions) for R in rot}
  assert len(orb)==expected

 print('PASS B7 two-edge witness subgraph = K_(4,4,4), 48 support pairs')
 print('PASS parallel 2-edge pairs left as UNCHECKED by these witnesses = 18')
 print('PASS 17-tag B7 necessary candidate upper bound = 8*18 = 144')
 print('PASS B6/B7 physical midpoint two-corner orbit checks')
if __name__=='__main__': main()
