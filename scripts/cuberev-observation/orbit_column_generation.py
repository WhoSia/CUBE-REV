#!/usr/bin/env python3
"""Sensor-equivariant column generation for L7 robust dictionary MILP.

Do not optimize only on orbit representatives: a group rotation also
permutes target source rows. Canonicalize for GENERATION; then EXPAND
every action orbit into actual columns before exact source-set cover.
"""
from __future__ import annotations
import argparse,itertools,json,random
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
from sensor_symmetry import rotations,conjugacy_candidate

HERE=Path(__file__).resolve().parents[2]
SEED=HERE/"docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json"
SOURCES=[tuple(s) for r in (3,4) for s in itertools.combinations(range(12),r)]

def sensor_group(moves):
    group=[]
    for _,_,tr in rotations():
        _,alpha,T=conjugacy_candidate(tr)
        if all((T[x]&1)==(x&1) for x in range(24)) and all(
            T[moves[a][x]]==moves[alpha[a]][T[x]]
            for a in range(18) for x in range(24)):
            group.append(alpha)
    assert len(group)==4
    return group

def signature_cover(moves,w):
    hist=signatures(moves,w)
    good={(a,b) for a in range(12) for b in range(a+1,12)
          if (hist[a]^hist[b]).bit_count()>=3}
    return sum(1<<j for j,sub in enumerate(SOURCES)
               if all(p in good for p in itertools.combinations(sub,2)))

def columns(seed=20261026,mutations=16000,top=1250):
    moves=edge_transitions()
    group=sensor_group(moves)
    canon=lambda w:min(tuple(alpha[a] for a in w) for alpha in group)
    incumbent=[tuple(ACTIONS.index(a) for a in word)
               for word in json.loads(SEED.read_text())["words"]]
    rng=random.Random(seed)
    reps={canon(w) for w in incumbent}
    for _ in range(mutations):
        w=list(incumbent[rng.randrange(len(incumbent))])
        for k in rng.sample(range(7),rng.choice((1,1,2,2,3,4))):
            w[k]=rng.randrange(18)
        reps.add(canon(tuple(w)))
    ranked=sorted(((signature_cover(moves,w).bit_count(),w) for w in reps),
                  reverse=True)
    kept={canon(w) for w in incumbent}
    kept.update(w for _,w in ranked[:top])
    incidence={}
    for rep in kept:
        for alpha in group:
            w=tuple(alpha[a] for a in rep)
            incidence[w]=signature_cover(moves,w)
    return {"representatives_generated":len(reps),
            "representatives_selected":len(kept),
            "orbit_words":len(incidence),
            "distinct_columns":len(set(incidence.values())),
            "word_to_cover":incidence}

def run(seed=20261026,mutations=16000,top=1250,seconds=30):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import csc_matrix
    pool=columns(seed,mutations,top)
    unique={}
    for word,mask in pool.pop("word_to_cover").items():
        unique.setdefault(mask,word)
    records=list(unique.items())
    rr=[];cc=[]
    for j,(mask,word) in enumerate(records):
        while mask:
            low=mask&-mask
            rr.append(low.bit_length()-1);cc.append(j);mask-=low
    mat=csc_matrix((np.ones(len(rr),dtype=np.int8),(rr,cc)),
                   shape=(len(SOURCES),len(records)))
    out=milp(np.ones(len(records)),integrality=np.ones(len(records)),
             bounds=Bounds(0,1),
             constraints=LinearConstraint(mat,np.ones(len(SOURCES)),np.inf),
             options={"time_limit":seconds,"mip_rel_gap":0})
    pool.update({"solver_status":str(out.message),
                 "finite_pool_dual":float(out.mip_dual_bound)
                      if out.mip_dual_bound is not None else None,
                 "global_optimum_proven":False})
    if out.x is not None:
        selected=[records[i][1] for i,x in enumerate(out.x) if x>0.5]
        moves=edge_transitions()
        assert __import__("functools").reduce(int.__or__,
            (signature_cover(moves,w) for w in selected),0)==(1<<len(SOURCES))-1
        pool["selected_words"]=[[ACTIONS[a] for a in w] for w in selected]
        pool["verified_upper_bound"]=len(selected)
    else:
        pool["selected_words"]=[]
        pool["verified_upper_bound"]=None
    return pool

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--mutations",type=int,default=16000)
    p.add_argument("--top",type=int,default=1250)
    p.add_argument("--seconds",type=float,default=30)
    x=p.parse_args()
    print(json.dumps(run(mutations=x.mutations,top=x.top,seconds=x.seconds),
                     sort_keys=True,indent=2))
