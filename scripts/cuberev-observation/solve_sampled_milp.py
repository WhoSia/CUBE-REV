#!/usr/bin/env python3
"""Reproducible finite-candidate MILP improvement for physical robust M-star.

Rebuilds 13,000 pseudo-random length-seven words (seed 25), the four earlier
witnesses, and the 715 3/4-source clauses; solves with SciPy/HiGHS. All
solutions are independently replayed through 54-sticker-derived transitions.
Never promote a candidate-pool dual bound to a global L7 lower bound.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import csc_matrix
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
from dictionary_coverage import SEED_WORDS
from generate_sampled_dictionary import candidate_coverage

def solve(seed=25,samples=13000,seconds=20):
    import random
    rng=random.Random(seed)
    moves=edge_transitions()
    words=[]
    covers=[]
    initial=[tuple(ACTIONS.index(a) for a in w) for w in SEED_WORDS]
    source=initial+[tuple(rng.randrange(18) for _ in range(7)) for _ in range(samples)]
    universe=sorted(sum(1<<j for j in s) for r in (3,4)
                    for s in itertools.combinations(range(12),r))
    index={mask:i for i,mask in enumerate(universe)}
    rr=[];cc=[]
    for w in source:
        masks=candidate_coverage(signatures(moves,w))
        if not masks:
            continue
        j=len(words)
        words.append(w)
        covered={index[x] for x in masks if x in index}
        covers.append(covered)
        for i in covered:
            rr.append(i);cc.append(j)
    A=csc_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(universe),len(words)))
    result=milp(c=np.ones(len(words)),
                integrality=np.ones(len(words)),
                bounds=Bounds(np.zeros(len(words)),np.ones(len(words))),
                constraints=LinearConstraint(A,np.ones(len(universe)),
                                             np.full(len(universe),np.inf)),
                options={"time_limit":seconds,"mip_rel_gap":0.0})
    receipt={"solver":"SciPy HiGHS","seed":seed,"samples":samples,
             "columns":len(words),"rows":len(universe),
             "solver_message":str(result.message),
             "numeric_pool_dual_bound":float(result.mip_dual_bound)
                        if result.mip_dual_bound is not None else None,
             "global_lower_bound_certified":False,
             "selected_words":[],"physically_verified":False}
    if result.x is not None:
        selected=[i for i,x in enumerate(result.x) if x>0.5]
        assert set().union(*(covers[i] for i in selected))==set(range(len(universe)))
        receipt["selected_words"]=[[ACTIONS[a] for a in words[i]] for i in selected]
        receipt["physically_verified"]=True
        receipt["upper_bound"]=len(selected)
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seconds",type=float,default=20)
    p.add_argument("--seed",type=int,default=25)
    p.add_argument("--samples",type=int,default=13000)
    p.add_argument("--out",type=Path)
    args=p.parse_args()
    d=solve(seed=args.seed,samples=args.samples,seconds=args.seconds)
    output=json.dumps(d,ensure_ascii=False,indent=2)+"\n"
    if args.out:args.out.write_text(output,encoding="utf-8")
    else:print(output,end="")

if __name__=="__main__":main()
