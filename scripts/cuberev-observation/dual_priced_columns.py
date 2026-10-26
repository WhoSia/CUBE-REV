#!/usr/bin/env python3
"""Price physically real L7 robust dictionary columns using a restricted LP dual.

The LP min sum(x_w) s.t. incidence @ x >= 1 produces dual weights y>=0
with incidence.T @ y <= 1 ONLY for supplied columns. A legal new word
with sum_{R covered by word} y_R > 1 has strictly negative reduced cost.
This is a column-generation direction, NOT a global lower-bound proof.
"""
from __future__ import annotations
import argparse,random,json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix
from orbit_column_generation import columns,signature_cover,SOURCES
from physical_edges import ACTIONS,edge_transitions
from pathlib import Path

def price(seed=20261026,mutations=16000,top=1250,proposals=32000,keep=200):
    pool=columns(seed=seed,mutations=mutations,top=top)
    base=pool.pop("word_to_cover")
    distinct={}
    for word,mask in base.items():
        if mask: distinct.setdefault(mask,word)
    masks=list(distinct);words=list(distinct.values())
    rr=[];cc=[]
    for j,mask in enumerate(masks):
        while mask:
            bit=mask&-mask;rr.append(bit.bit_length()-1);cc.append(j);mask-=bit
    A=csc_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(SOURCES),len(words)))
    lp=linprog(np.ones(len(words)),A_ub=-A,b_ub=-np.ones(len(SOURCES)),
               bounds=(0,None),method="highs")
    assert lp.success,lp.message
    y=-lp.ineqlin.marginals
    assert np.all(y>=-1e-7)
    assert float(np.max(A.T@y))<=1+1e-6
    rng=random.Random(seed+1)
    parents=words[:]
    parents+= [words[int(i)] for i in np.argsort(-lp.x)[:60]]
    physical=edge_transitions()
    new={}
    for _ in range(proposals):
        candidate=list(parents[rng.randrange(len(parents))])
        for index in rng.sample(range(7),rng.choice((1,1,2,2,3,4))):
            candidate[index]=rng.randrange(18)
        word=tuple(candidate)
        mask=signature_cover(physical,word)
        if not mask or mask in distinct or mask in new:continue
        indices=[j for j in range(len(SOURCES)) if mask>>j&1]
        weight=float(y[indices].sum())
        if weight>1+1e-8:new[mask]=(weight,word)
    ranked=sorted(new.values(),reverse=True)[:keep]
    return {"scope":"FINITE_PHYSICAL_CANDIDATE_POOL",
            "lp_primal_dual_optimum":float(lp.fun),
            "existing_columns":len(words),
            "negative_reduced_cost_columns":len(new),
            "max_new_column_dual_weight":max((x[0] for x in new.values()),default=0),
            "top_priced_words":[{"dual_weight":score,
                "actions":[ACTIONS[a] for a in word]} for score,word in ranked],
            "global_lower_bound_proven":False}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--mutations",type=int,default=16000)
    p.add_argument("--top",type=int,default=1250)
    p.add_argument("--proposals",type=int,default=32000)
    p.add_argument("--keep",type=int,default=200)
    p.add_argument("--out",type=Path)
    a=p.parse_args()
    result=price(mutations=a.mutations,top=a.top,
                 proposals=a.proposals,keep=a.keep)
    output=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.out:a.out.write_text(output)
    else:print(output,end="")
