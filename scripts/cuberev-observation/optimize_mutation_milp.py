#!/usr/bin/env python3
"""Seed-392 incumbent mutation + MILP column selection (reproducible heuristic).

Reuses physical_edges and 0.18-style set-cover constraints. The verified
15-word JSON is the authoritative *certificate*; this is its search recipe.
Different SciPy/HiGHS versions may return a different equally valid optimum
from the fixed candidate pool.
"""
from __future__ import annotations
import argparse,itertools,random,json
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures

ROOT=Path(__file__).resolve().parents[2]
INCUMBENT=ROOT/"docs/observation-generalization/L7_ROBUST_25_WORD_COVER.json"
TARGETS=[tuple(c) for k in (3,4) for c in itertools.combinations(range(12),k)]
PAIRS=[tuple(itertools.combinations(c,2)) for c in TARGETS]
ALL=(1<<len(TARGETS))-1

def cover(moves,word):
    hist=signatures(moves,word)
    good={(a,b) for a in range(12) for b in range(a+1,12)
          if (hist[a]^hist[b]).bit_count()>=3}
    mask=0
    for idx,pairs in enumerate(PAIRS):
        if all(p in good for p in pairs):mask|=1<<idx
    return mask

def solve(seed=392,mutations=50000,top=2200,seconds=60):
    moves=edge_transitions()
    base=[tuple(ACTIONS.index(a) for a in word)
          for word in json.loads(INCUMBENT.read_text())["words"]]
    assert len(base)==25
    covers={w:cover(moves,w) for w in base}
    rng=random.Random(seed)
    for _ in range(mutations):
        word=list(base[rng.randrange(len(base))])
        for j in rng.sample(range(7),rng.choice((1,1,1,2,2,3))):
            word[j]=rng.randrange(18)
        w=tuple(word)
        if w not in covers:covers[w]=cover(moves,w)
    ranked=sorted(covers,key=lambda w:(covers[w].bit_count(),w),reverse=True)
    pool=list(dict.fromkeys(base+[w for w in ranked if covers[w] and w not in base][:top]))
    rr=[];cc=[]
    for j,w in enumerate(pool):
        bits=covers[w]
        while bits:
            low=bits&-bits;rr.append(low.bit_length()-1);cc.append(j);bits-=low
    matrix=csc_matrix((np.ones(len(rr),dtype=np.int8),(rr,cc)),
                      shape=(len(TARGETS),len(pool)))
    result=milp(np.ones(len(pool)),integrality=np.ones(len(pool)),
                bounds=Bounds(0,1),
                constraints=LinearConstraint(matrix,np.ones(len(TARGETS)),np.inf),
                options={"time_limit":seconds,"mip_rel_gap":0})
    chosen=[pool[i] for i,x in enumerate(result.x) if x>.5] if result.x is not None else []
    if chosen:
        union=0
        for w in chosen:union|=cover(moves,w)
        assert union==ALL
    return {"candidate_pool_size":len(pool),"selected_count":len(chosen),
            "selected_words":[[ACTIONS[a] for a in w] for w in chosen],
            "solver_status":str(result.message),
            "pool_numeric_bound":float(result.mip_dual_bound)
                if result.mip_dual_bound is not None else None,
            "global_minimum_proven":False,"physical_replay_pass":bool(chosen)}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seconds",type=float,default=60)
    a=p.parse_args()
    print(json.dumps(solve(seconds=a.seconds),indent=2))
