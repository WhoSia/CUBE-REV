#!/usr/bin/env python3
"""Proof obligations for global lower bounds in physical L7 erasure cover.

Given rows R and a rational weight y_R >= 0, the inequality
sum_R y_R > k and sum_{R covered by w} y_R <= 1 for EVERY PHYSICAL
word w proves that no k experiments suffice. A screened-pool LP dual
does NOT satisfy the second requirement without a universal pricing
oracle (complete enumeration, sound branch-and-bound or another proof).
V4 allows a symmetry reduction only when the weight is orbit-invariant.

This module implements exact-rational checks for a *provided* sample and
computes symmetry orbits of the 715 source sets. Its results explicitly
are NOT an exhaustive global proof.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction
from sensor_symmetry import rotations,conjugacy_candidate
from physical_edges import edge_transitions
from channel_model_transfer import ALL_SOURCE_MASKS,word_coverage

def sensor_source_group():
    moves=edge_transitions();group=[]
    for _,_,transform in rotations():
        _,alpha,T=conjugacy_candidate(transform)
        if all(T[s]&1==s&1 for s in range(24)) and all(
            T[moves[a][s]]==moves[alpha[a]][T[s]]
            for a in range(18) for s in range(24)):
            p=tuple(T[2*i]//2 for i in range(12))
            group.append(p)
    assert len(group)==4
    return group

def transport(mask,p):
    return sum(1<<p[i] for i in range(12) if (mask>>i)&1)

def row_orbits():
    group=sensor_source_group()
    unseen=set(ALL_SOURCE_MASKS);orbits=[]
    while unseen:
        item=min(unseen)
        orbit={transport(item,p) for p in group}
        assert orbit <= set(ALL_SOURCE_MASKS)
        unseen-=orbit;orbits.append(tuple(sorted(orbit)))
    assert sum(map(len,orbits))==715
    return orbits

def check_sampled_dual(weights,words):
    """Weights are str(Fraction) keyed by decimal source mask."""
    values={int(k):Fraction(v) for k,v in weights.items()}
    assert set(values)==set(ALL_SOURCE_MASKS)
    assert min(values.values())>=0
    group=sensor_source_group()
    symmetry_ok=all(values[m]==values[transport(m,p)]
                    for m in ALL_SOURCE_MASKS for p in group)
    moves=edge_transitions();worst=Fraction(0)
    for word in words:
        c=word_coverage(moves,word,"erasure1")
        worst=max(worst,sum((values[m] for m in c),Fraction(0)))
    return {"tested_words":len(words),"sample_max_pricing":str(worst),
            "weights_V4_invariant":symmetry_ok,
            "sum_weights":str(sum(values.values())),
            "global_dual_feasibility_proven":False}

if __name__=="__main__":
    o=row_orbits()
    print(json.dumps({"sensor_group_size":4,"source_row_orbits":len(o),
                      "orbit_size_counts":{str(n):sum(len(a)==n for a in o)
                         for n in (1,2,4)},
                      "global_lower_bound_improved":False},sort_keys=True))
