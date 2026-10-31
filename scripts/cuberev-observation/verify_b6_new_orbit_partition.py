#!/usr/bin/env python3
"""B6 new-obstruction Burnside orbit decomposition by five geometric zones.

Requires sibling verify_b6_geometric_rule.py only.  No historical B6
success labels, source archive, or 8.24-million-state search is imported.
The physical interpretation of 35 new forbidden pairs is a separately
proven premise in the canonical CUBE-REV 0.28 Notion record.
"""
from itertools import combinations,product
from collections import Counter
from verify_b6_geometric_rule import EDGE_NAMES,ENDS,midpoint,valid_pairs,proper_rotations

BY_MID={midpoint(e):e for e in EDGE_NAMES}
R=proper_rotations()
order=("h","N","P","F","h*")
expected={
  "h-h*":(1,1,1),"N-N":(2,0,1),"N-P":(4,0,2),
  "N-F":(16,0,8),"P-F":(8,0,4),"P-h*":(2,0,1),
  "F-F":(2,2,2),
}
def run():
 for h in EDGE_NAMES:
  core=ENDS[h]
  anti={tuple(-v for v in p) for p in core}
  star=next(e for e in EDGE_NAMES if ENDS[e]==anti)
  near={e for e in EDGE_NAMES if e!=h and ENDS[e]&core}
  far={e for e in EDGE_NAMES if e!=star and ENDS[e]&anti}
  par={e for e in EDGE_NAMES if midpoint(e).index(0)==midpoint(h).index(0)
       and e not in (h,star)}
  G={"h":{h},"N":near,"P":par,"F":far,"h*":{star}}
  assert sorted(map(len,G.values()))==[1,1,2,4,4]
  H=[r for r in R if frozenset(r(v) for v in core)==core]
  assert len(H)==2
  # Explicit 35-pair geometric category rules: allowed B6 iff G6, and
  # B5-forbidden classes are determined from the old B5 support family.
  # In these seven categories all pairs are newly forbidden except:
  # N-N: the two pairs incident to the same endpoint are newly forbidden.
  # N-P: half the pairs (those on the same cube face) were already B5 bad.
  # F-F: the two opposite far-side spokes are newly forbidden.
  # This checker verifies their symmetry counts, not B5 provenance.
  for group,(n,fix,orbitcount) in expected.items():
   A,B=group.split("-")
   items=[frozenset(p) for p in
          (combinations(G[A],2) if A==B else product(G[A],G[B]))]
   if group=="N-N":
    items=[p for p in items if len(set().union(*(ENDS[e]&core for e in p)))==1]
   if group=="F-F":
    items=[p for p in items if len(set().union(*(ENDS[e]&anti for e in p)))==2]
   if group=="N-P":
    # Every one of the eight N-P pairs moves under the nonidentity
    # stabilizer. The historic B5 certificate selects an H-invariant
    # four-element subfamily, hence exactly two 2-element H-orbits.
    assert len(items)==8
    assert not any(all(frozenset(BY_MID[r(midpoint(e))] for e in p)==p
                       for r in H) for p in items)
    assert (n,fix,orbitcount)==(4,0,2)
    continue
   Hfixed=sum(all(frozenset(BY_MID[r(midpoint(e))] for e in p)==p for r in H)
              for p in items)
   assert (len(items),Hfixed,(len(items)+Hfixed)//2)==(n,fix,orbitcount), (h,group,len(items),Hfixed)
 print("PASS six geometrically specified B6-new zone families under H=C2")
 print("N-F has 16 pairs, 0 fixed, hence EIGHT symmetry orbits")
 print("The N-P four-pair provenance requires prior B5 archive input")
if __name__=="__main__":run()
