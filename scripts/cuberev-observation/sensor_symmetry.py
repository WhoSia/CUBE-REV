#!/usr/bin/env python3
"""Exact action/readout automorphisms induced by the 24 proper cube rotations.

For a 24-state oriented edge transition system, a sensor-preserving symmetry
is a bijection T of states and an action alphabet permutation alpha such that
T(m_a(s)) == m_{alpha(a)}(T(s)) and o(T(s)) == o(s), for EVERY state/action.

This is stricter than being a geometric symmetry of an unobserved cube.
The tested finite 24 proper signed-axis rotations are not claimed to exhaust
all possible abstract automorphisms of the observed transition automaton.
"""
from __future__ import annotations
import itertools, json
from physical_edges import ACTIONS, EDGES, NORMAL, edge_transitions

NORMAL_TO_FACE={v:k for k,v in NORMAL.items()}

def determinant(p,sgn):
    inversions=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
    return (-1 if inversions%2 else 1)*sgn[0]*sgn[1]*sgn[2]

def rotations():
    for p in itertools.permutations(range(3)):
        for sgn in itertools.product((-1,1),repeat=3):
            if determinant(p,sgn)!=1:continue
            def transform(x,p=p,sgn=sgn):
                return tuple(sgn[i]*x[p[i]] for i in range(3))
            yield p,sgn,transform

def conjugacy_candidate(transform):
    labels={face:NORMAL_TO_FACE[transform(normal)] for face,normal in NORMAL.items()}
    alpha=tuple(ACTIONS.index(labels[a[0]]+a[1:]) for a in ACTIONS)
    state_perm=[]
    for slot,(fa,fb) in enumerate(EDGES):
        a,b=labels[fa],labels[fb]
        if (a,b) in EDGES:
            j=EDGES.index((a,b)); flip=0
        else:
            j=EDGES.index((b,a)); flip=1
        state_perm.extend((2*j+flip,2*j+(flip^1)))
    return labels,alpha,tuple(state_perm)

def analyze():
    moves=edge_transitions()
    results=[]
    for p,sign,transform in rotations():
        labels,alpha,T=conjugacy_candidate(transform)
        assert sorted(T)==list(range(24))
        action_equivariant=all(T[moves[a][s]]==moves[alpha[a]][T[s]]
                               for a in range(18) for s in range(24))
        readout_invariant=all((T[s]&1)==(s&1) for s in range(24))
        # A physical geometric relabeling can fail readout preservation even
        # if it intertwines the complete state automaton.
        results.append({"axes":list(p),"signs":list(sign),
                        "faces":labels,"automaton_intertwines":action_equivariant,
                        "flip_readout_preserved":readout_invariant,
                        "certified":action_equivariant and readout_invariant,
                        "source_permutation":[T[2*k]//2 for k in range(12)]})
    return {"tested_proper_cube_rotations":len(results),
            "full_transition_readout_checks_per_candidate":18*24+24,
            "automaton_intertwining_count":sum(x["automaton_intertwines"] for x in results),
            "certified_sensor_automorphisms":[x for x in results if x["certified"]],
            "rejected_sensor_automorphisms":[x for x in results if not x["certified"]],
            "scope":"PROPER_3D_CUBE_ROTATIONS_ONLY",
            "not_all_abstract_automorphisms":True}

if __name__=="__main__":
    print(json.dumps(analyze(),ensure_ascii=False,sort_keys=True,indent=2))
