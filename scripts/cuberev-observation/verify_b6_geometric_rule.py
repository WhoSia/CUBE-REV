#!/usr/bin/env python3
"""CUBE-REV 0.28 — intrinsic graph for B6 optimal omitted-edge pairs.

A 16-tag radius-six candidate omits two adjacent corner tags, hence one cube
edge h, and two edge tags. This module DEFINES the proposed geometric rule,
without importing any B5/B6 classification or success flags. The separate
bridge checker validates this rule against physical B6 witness certificates.
"""
from itertools import product, permutations, combinations

FACES={'U':(0,1,0),'R':(1,0,0),'F':(0,0,1),
       'D':(0,-1,0),'L':(-1,0,0),'B':(0,0,-1)}
EDGE_NAMES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
CORNERS=list(product((-1,1),repeat=3))
def midpoint(edge):
    return tuple(FACES[edge[0]][i]+FACES[edge[1]][i] for i in range(3))
def endpoints(edge):
    m=midpoint(edge)
    k=m.index(0)
    return frozenset(tuple(sign if i==k else m[i] for i in range(3))
                     for sign in (-1,1))
ENDS={edge:endpoints(edge) for edge in EDGE_NAMES}

def admissible(core_edge, edge_a, edge_b):
    """Coordinate-independent four-case criterion for omitted two edges."""
    assert edge_a!=edge_b
    core=ENDS[core_edge]
    opposite=frozenset(tuple(-v for v in c) for c in core)
    other=next(e for e in EDGE_NAMES if ENDS[e]==opposite)
    near={e for e in EDGE_NAMES if e!=core_edge and ENDS[e]&core}
    far={e for e in EDGE_NAMES if e!=other and ENDS[e]&opposite}
    parallel={e for e in EDGE_NAMES
              if midpoint(e).index(0)==midpoint(core_edge).index(0)
              and e not in (core_edge,other)}
    assert len(near)==4 and len(far)==4 and len(parallel)==2
    corner=sorted(core)[0]
    return (
      # One edge emanating from EACH endpoint of the missing corner edge.
      (edge_a in near and edge_b in near
       and (corner in ENDS[edge_a])!=(corner in ENDS[edge_b]))
      # Two far-side spokes that belong to a common cube face.
      or (edge_a in far and edge_b in far
          and bool(set(edge_a)&set(edge_b)))
      # The opposite parallel edge with any far-side spoke.
      or (edge_a==other and edge_b in far)
      or (edge_b==other and edge_a in far)
      # The two remaining, side-parallel edges.
      or {edge_a,edge_b}==parallel
    )

def valid_pairs(core_edge):
    return {frozenset((a,b)) for a,b in combinations(EDGE_NAMES,2)
            if admissible(core_edge,a,b)}

def graph_components(edges):
    remaining=set(EDGE_NAMES)
    components=[]
    while remaining:
        start=min(remaining)
        seen={start};todo=[start]
        while todo:
            vertex=todo.pop()
            for e in edges:
                if vertex in e:
                    for next_vertex in e-seen:
                        seen.add(next_vertex)
                        todo.append(next_vertex)
        remaining-=seen
        degree=sorted(sum(vertex in edge for edge in edges)
                      for vertex in seen)
        components.append((len(seen),sum(edge<=seen for edge in edges),
                           tuple(degree)))
    return sorted(components,reverse=True)

def proper_rotations():
    result=[]
    for p in permutations(range(3)):
        parity=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        for signs in product((-1,1),repeat=3):
            if parity*signs[0]*signs[1]*signs[2]==1:
                result.append(lambda xyz,p=p,signs=signs:
                              tuple(signs[i]*xyz[p[i]] for i in range(3)))
    assert len(result)==24
    return result

def verify_geometry():
    mid_to_edge={midpoint(e):e for e in EDGE_NAMES}
    expected=[(5,8,(3,3,3,3,4)),(4,4,(2,2,2,2)),
              (2,1,(1,1)),(1,0,(0,))]
    for h in EDGE_NAMES:
        graph=valid_pairs(h)
        assert len(graph)==13
        assert graph_components(graph)==expected
        for r in proper_rotations():
            h_r=mid_to_edge[r(midpoint(h))]
            transformed={frozenset(mid_to_edge[r(midpoint(e))]
                         for e in pair) for pair in graph}
            assert transformed==valid_pairs(h_r)
    print("PASS 12 core edges × 13 admissible pairs = 156 geometric layouts")
    print("PASS each 12-vertex graph W5 ⊔ C4 ⊔ K2 ⊔ K1; 13 edges")
    print("PASS proper 24 cube rotations preserve the four-case criterion")

if __name__=="__main__":
    verify_geometry()
