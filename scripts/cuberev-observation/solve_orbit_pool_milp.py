#!/usr/bin/env python3
"""Exact finite orbit-pool MILP: eleven seed words transformed under V4.

Does NOT prove a global lower bound over all length-7 legal words.
"""
from __future__ import annotations
import itertools,json
import numpy as np
from scipy.sparse import csc_matrix
from scipy.optimize import milp,Bounds,LinearConstraint
from physical_edges import ACTIONS,edge_transitions
from sensor_symmetry import rotations,conjugacy_candidate
from robust_observation import signatures
from verify_sensor_orbits import CERT,SOURCES

def solve():
    moves=edge_transitions()
    original=[tuple(ACTIONS.index(a) for a in w) for w in json.loads(CERT.read_text())["words"]]
    transformed=set()
    for _,_,transform in rotations():
        _,alpha,T=conjugacy_candidate(transform)
        if all((T[x]&1)==(x&1) for x in range(24)) and all(
            T[moves[a][x]]==moves[alpha[a]][T[x]] for a in range(18) for x in range(24)):
            for w in original: transformed.add(tuple(alpha[a] for a in w))
    words=sorted(transformed)
    rows=[];cols=[]
    for j,w in enumerate(words):
        hist=signatures(moves,w)
        for i,mask in enumerate(SOURCES):
            subset=[s for s in range(12) if mask>>s&1]
            if all((hist[a]^hist[b]).bit_count()>=3
                   for a,b in itertools.combinations(subset,2)):
                rows.append(i);cols.append(j)
    A=csc_matrix((np.ones(len(rows)),(rows,cols)),
                 shape=(len(SOURCES),len(words)))
    result=milp(np.ones(len(words)),integrality=np.ones(len(words)),
         bounds=Bounds(np.zeros(len(words)),np.ones(len(words))),
         constraints=LinearConstraint(A,np.ones(len(SOURCES)),np.inf),
         options={"mip_rel_gap":0})
    assert result.success and round(result.fun)==11
    assert result.mip_dual_bound>=11-1e-6
    chosen=[i for i,z in enumerate(result.x) if z>.5]
    assert np.all(A[:,chosen].sum(axis=1)>=1-1e-8)
    return {"status":"FINITE_44_WORD_ORBIT_POOL_OPTIMUM_PASS",
            "candidate_words":len(words),"finite_pool_optimum":len(chosen),
            "global_minimum_proven":False,
            "selected":[[ACTIONS[a] for a in words[i]] for i in chosen]}
if __name__=="__main__":print(json.dumps(solve(),sort_keys=True))
