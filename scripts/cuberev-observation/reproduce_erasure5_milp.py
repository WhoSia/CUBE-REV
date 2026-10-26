#!/usr/bin/env python3
"""Reproduce a 5-word finite-pool known-erasure upper bound (seed 261026).

Generate 5500 action mutations around the earlier seven-word witness, keep
600 highest-coverage candidates and all seven originals, deduplicate actual
715-row incidence columns, and solve the finite-pool set cover with HiGHS.
This does not examine all 18^7 physical sequences.
"""
from __future__ import annotations
import itertools,json,random,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import milp,linprog,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"docs/observation-generalization/L7_ERASURE1_7_WORD_COVER.json"
TARGETS=[c for size in (3,4) for c in itertools.combinations(range(12),size)]
PAIRS=[tuple(itertools.combinations(c,2)) for c in TARGETS]
def cover(moves,word):
    h=signatures(moves,word)
    good={(i,j) for i in range(12) for j in range(i+1,12)
          if (h[i]^h[j]).bit_count()>=2}
    return sum(1<<k for k,pairs in enumerate(PAIRS)
               if all(p in good for p in pairs))
def solve(seed=261026,trials=5500,top=600,seconds=25):
    moves=edge_transitions()
    base=[tuple(ACTIONS.index(a) for a in w)
          for w in json.loads(BASE.read_text())["words"]]
    rng=random.Random(seed)
    pool={w:cover(moves,w) for w in base}
    for _ in range(trials):
        w=list(base[rng.randrange(len(base))])
        for j in rng.sample(range(7),rng.choice((1,1,2,2,3,4))):
            w[j]=rng.randrange(18)
        w=tuple(w)
        if w not in pool: pool[w]=cover(moves,w)
    ranked=sorted(pool.items(),key=lambda kv:kv[1].bit_count(),reverse=True)
    shortlist=dict(ranked[:top]+[(w,pool[w]) for w in base])
    unique={}
    for word,mask in shortlist.items():unique.setdefault(mask,word)
    masks=list(unique)
    rr=[];cc=[]
    for j,mask in enumerate(masks):
        while mask:
            low=mask&-mask;rr.append(low.bit_length()-1);cc.append(j);mask-=low
    A=csc_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(TARGETS),len(masks)))
    lp=linprog(np.ones(len(masks)),A_ub=-A,b_ub=-np.ones(len(TARGETS)),
               bounds=(0,None),method="highs")
    assert lp.success
    optimum=milp(np.ones(len(masks)),integrality=np.ones(len(masks)),
                 bounds=Bounds(0,1),
                 constraints=LinearConstraint(A,np.ones(len(TARGETS)),np.inf),
                 options={"time_limit":seconds,"mip_rel_gap":0})
    result={"generated_words":len(pool),"distinct_columns":len(masks),
            "lp_relaxation":float(lp.fun),"solver_message":str(optimum.message),
            "finite_pool_dual_bound":float(optimum.mip_dual_bound)
                if optimum.mip_dual_bound is not None else None,
            "global_lower_bound_proven":False}
    if optimum.x is not None:
        selected=[unique[masks[j]] for j,x in enumerate(optimum.x) if x>0.5]
        union=0
        for word in selected:union|=cover(moves,word)
        assert union==(1<<len(TARGETS))-1
        result.update({"physical_upper_bound":len(selected),
                       "selected_words":[[ACTIONS[a] for a in word] for word in selected],
                       "physical_715_clause_replay_pass":True})
    return result
if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--seconds",type=float,default=25)
    x=a.parse_args()
    print(json.dumps(solve(seconds=x.seconds),sort_keys=True))
