#!/usr/bin/env python3
"""Exact projected HTM pattern databases from CUBE-REV 0.24 physical geometry.

Each pattern tracks the (position,orientation) of a fixed set of original
edge cubies, not a stationary facelet. All action transitions are induced
from the full 54-facelet engine. Reverse BFS is exact for each projected
target but ONLY a lower bound for the full-cube solved target.
Uses the small projected-geodesic/PDB principle also present in the
historical CUBE-REV 0.24-0.27 research; does not invoke 0.27's large search.
"""
from __future__ import annotations
import collections,itertools,json
from fullcube_goal_info_conflict import A,F,EDGES
from fullcube_sensor_goal_theorem import SOLVED,turn,factor

def transitions_for_tag(tag):
    representatives={factor(SOLVED,tag):SOLVED}
    todo=collections.deque([SOLVED])
    while todo:
        s=todo.popleft()
        for a in range(18):
            t=turn(s,a);k=factor(t,tag)
            if k not in representatives:
                representatives[k]=t;todo.append(t)
    assert len(representatives)==24
    T=[[factor(turn(representatives[x],a),tag)
        for x in range(24)] for a in range(18)]
    assert all(sorted(row)==list(range(24)) for row in T)
    return T

def build_pattern_database(tags):
    trans=[transitions_for_tag(t) for t in tags]
    solved=tuple(factor(SOLVED,t) for t in tags)
    depth={solved:0}
    queue=collections.deque([solved])
    while queue:
        state=queue.popleft();next_depth=depth[state]+1
        for a in range(18):
            nxt=tuple(trans[i][a][k] for i,k in enumerate(state))
            if nxt not in depth:
                depth[nxt]=next_depth;queue.append(nxt)
    return depth

def admissible_h(state,tags,pdb):
    key=tuple(factor(state,t) for t in tags)
    return pdb[key]

def audit():
    configs=((0,),(0,5),(0,5,10))  # UR; UR+DF; UR+DF+BL
    expected=((24,3),(528,5),(10560,7))
    result=[]
    for tags,(expected_size,expected_diameter) in zip(configs,expected):
        pdb=build_pattern_database(tags)
        hist=dict(sorted(collections.Counter(pdb.values()).items()))
        assert len(pdb)==expected_size and max(pdb.values())==expected_diameter
        assert pdb[tuple(factor(SOLVED,t) for t in tags)]==0
        # Verify each stored projected shortest path has a predecessor
        # exactly one step closer to the goal, and triangle inequality.
        trans=[transitions_for_tag(t) for t in tags]
        for state,dist in pdb.items():
            neighbors=[tuple(trans[i][a][p] for i,p in enumerate(state))
                       for a in range(18)]
            assert all(abs(dist-pdb[n])<=1 for n in neighbors)
            if dist:assert any(pdb[n]==dist-1 for n in neighbors)
        result.append({'tagged_edges':[''.join(EDGES[t]) for t in tags],
                       'states':len(pdb),'diameter':max(pdb.values()),
                       'distance_layers':hist})
    return {'status':'FULL54_THREE_PATTERN_DATABASES_PASS',
            'patterns':result,'full_goal_admissibility':'h_pattern(s) <= d_18HTM(s,SOLVED)',
            'large_027_solver_executed':False,
            'global_k4_dictionary_certified':False}
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,indent=2))
