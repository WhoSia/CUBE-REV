#!/usr/bin/env python3
"""Exactly count V4 action-word and source-row orbits for physical L7 pricing.

Burnside: certified sensor-preserving rotations have 18 fixed actions for
identity and 6 fixed actions for each of three half-turns, so action-word
orbits = (18^7+3*6^7)/4 = 153264960. This is a COMPLETE orbit count,
NOT an enumerated column dictionary or a k=4 impossibility proof.

On all 3/4-source sets, 715 source rows form 190 orbits. Every feasible
global LP dual can be averaged to V4 invariance with the same objective.
But pricing still has to check all legal physical word-orbits, transporting
source rows jointly, before its objective is a global M* lower bound.
"""
from __future__ import annotations
import collections
import itertools
import json
from physical_edges import ACTIONS,edge_transitions
from sensor_symmetry import rotations,conjugacy_candidate

def audit(length=7):
    transitions=edge_transitions()
    group=[]
    for _,_,transform in rotations():
        _,alpha,T=conjugacy_candidate(transform)
        if (all((T[s]&1)==(s&1) for s in range(24))
            and all(T[transitions[a][s]]==transitions[alpha[a]][T[s]]
                    for a in range(18) for s in range(24))):
            group.append((alpha,tuple(T[2*i]//2 for i in range(12))))
    assert len(group)==4
    fixed=[sum(alpha[a]==a for a in range(18)) for alpha,_ in group]
    assert sorted(fixed)==[6,6,6,18]
    fixed_words=[k**length for k in fixed]
    assert sum(fixed_words)%4==0
    count=sum(fixed_words)//4
    if length==7:assert count==153264960

    masks={frozenset(s) for size in (3,4)
           for s in itertools.combinations(range(12),size)}
    orbit_sizes=collections.Counter()
    orbit_sizes_by_source_size=collections.Counter()
    while masks:
        base=min(masks,key=lambda s:(len(s),tuple(sorted(s))))
        orbit={frozenset(p[i] for i in base) for _,p in group}
        assert orbit<=masks or orbit.isdisjoint(masks)==False
        masks-=orbit
        orbit_sizes[len(orbit)]+=1
        orbit_sizes_by_source_size[(len(base),len(orbit))]+=1
    assert orbit_sizes=={4:169,2:18,1:3}
    assert sum(orbit_sizes.values())==190
    assert sum(size*n for size,n in orbit_sizes.items())==715
    return {"status":"EXACT_V4_BURNSIDE_CENSUS_PASS",
            "action_words":18**length,
            "sensor_preserving_group_order":4,
            "fixed_action_counts":sorted(fixed),
            "distinct_action_word_orbits":count,
            "source_sets":715,"source_row_orbits":190,
            "source_row_orbit_sizes":{str(k):v for k,v in sorted(orbit_sizes.items())},
            "source_row_orbits_by_target_size":{
                str(k):sum(n for (size,_),n in orbit_sizes_by_source_size.items()
                           if size==k) for k in (3,4)},
            "complete_physical_word_cover_pricing_verified":False,
            "k4_global_decision_proven":False}

if __name__=="__main__":
    print(json.dumps(audit(),sort_keys=True,indent=2))
