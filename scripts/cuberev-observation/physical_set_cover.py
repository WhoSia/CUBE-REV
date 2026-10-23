#!/usr/bin/env python3
"""Reusable physical set-cover/SAT machinery for robust observation dictionaries.

Derived algorithmically from existing CUBE-REV 0.18:
  - a source-set is a clause;
  - each legal observation word is a candidate;
  - selection is a 0/1 variable, and an at-most-k constraint gives a decision test.
No external code copied. Optional PySAT supplies exact SAT/UNSAT within the
*given candidate pool only*, not all 18^L physical experiments.
"""
from __future__ import annotations
import argparse, json
from dictionary_coverage import SEED_WORDS, covered_by_word
from physical_edges import edge_transitions

def build(words=SEED_WORDS, min_distance=3):
    moves=edge_transitions()
    return [set(covered_by_word(moves,word,min_distance))
            for word in words]

def greedy(covers, target=None):
    remaining=set().union(*covers) if target is None else set(target)
    chosen=[]
    while remaining:
        best=max((len(c&remaining),-i,i) for i,c in enumerate(covers) if i not in chosen)
        if best[0]==0: return {"status":"INFEASIBLE_IN_POOL","uncovered":len(remaining),"indices":chosen}
        i=best[2];chosen.append(i);remaining-=covers[i]
    return {"status":"COVERED_IN_POOL","indices":chosen,"size":len(chosen)}

def lower_bound(covers, target):
    """Rigorous elementary cover lower bound for the candidate pool."""
    target=set(target)
    if not target:return 0
    greatest=max((len(c&target) for c in covers),default=0)
    if not greatest:return None
    return (len(target)+greatest-1)//greatest

def exact_sat(covers, target, maximum=None):
    try:
        from pysat.card import CardEnc, EncType
        from pysat.formula import CNF, IDPool
        from pysat.solvers import Glucose4
    except ImportError as err:
        raise RuntimeError("Install pinned python-sat to enable solver") from err
    target=set(target);n=len(covers)
    if not target: return {"status":"SAT","indices":[],"k":0}
    cnf=CNF()
    for mask in sorted(target):
        covering=[j+1 for j,cov in enumerate(covers) if mask in cov]
        if not covering:return {"status":"UNSAT_ALL_K_IN_POOL","uncovered_mask":mask}
        cnf.append(covering)
    upper=n if maximum is None else min(maximum,n)
    for k in range(1,upper+1):
        vpool=IDPool(start_from=n+1)
        f=cnf.copy()
        f.extend(CardEnc.atmost(lits=list(range(1,n+1)),bound=k,
                                encoding=EncType.seqcounter,vpool=vpool).clauses)
        with Glucose4(bootstrap_with=f.clauses) as solver:
            if solver.solve():
                model=set(x for x in solver.get_model() if x>0)
                selected=[j for j in range(n) if j+1 in model]
                assert target<=set().union(*(covers[i] for i in selected))
                return {"status":"SAT","indices":selected,"k":k,
                        "proof_scope":"EXACT_ONLY_WITHIN_SUPPLIED_CANDIDATE_POOL"}
    return {"status":"NO_SOLUTION_UP_TO_K_IN_POOL","k":upper}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--solver",choices=["greedy","sat"],default="greedy")
    p.add_argument("--max-k",type=int,default=None)
    args=p.parse_args()
    covers=build()
    target=set().union(*covers)
    g=greedy(covers,target)
    result={"source":"PHYSICAL_REPLAY","word_count":len(covers),
            "target_count":len(target),
            "lower_bound_simple":lower_bound(covers,target),
            "greedy":g,"exact":exact_sat(covers,target,args.max_k) if args.solver=="sat" else None,
            "candidate_pool_only":True,"global_robust_Mstar_not_proven":True}
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
