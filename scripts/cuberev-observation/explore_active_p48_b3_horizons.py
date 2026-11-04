#!/usr/bin/env python3
"""B3 active fixed-site ideal observation exploration with bounded decision tree.

All 3,502 P48 18-HTM radius-three states are reconstructed. Exhaustively
checks the 12C3*8C3 predetermined three-frame site choices, optionally all
12C4*8C4 four-frame choices, and exact two-step adaptive decisions.
The harder three-step adaptive recursion returns UNKNOWN when its explicit
belief-state node budget is exhausted. Do not recode UNKNOWN as impossible.
"""
import argparse
from itertools import combinations
from audit_active_p48_small_ball_decision_trees import (
    ball,observations,nonadaptive_witness,can_adapt,BudgetExceeded
)

def nonadaptive_four(factors):
    n=len(factors);scanned=0
    for ee in combinations(range(12),4):
        for cc in combinations(range(8),4):
            scanned+=1
            columns=ee+tuple(12+i for i in cc)
            seen=set()
            for f in factors:
                key=tuple(f[i] for i in columns)
                if key in seen:break
                seen.add(key)
            else:return (ee,cc),scanned
    return None,scanned

def nonadaptive_five(factors):
    """Exhaust 12C5 * 8C5 = 44,352 five-edge/five-corner schedules."""
    n=len(factors);scanned=0
    for ee in combinations(range(12),5):
        for cc in combinations(range(8),5):
            scanned+=1
            columns=ee+tuple(12+i for i in cc)
            seen=set()
            for f in factors:
                key=tuple(f[i] for i in columns)
                if key in seen:break
                seen.add(key)
            else:return (ee,cc),scanned
    return None,scanned

def nonadaptive_six(factors):
    """Exhaust 12C6 * 8C6 = 25,872 full six-edge/six-corner schedules."""
    n=len(factors);scanned=0
    for ee in combinations(range(12),6):
        for cc in combinations(range(8),6):
            scanned+=1
            columns=ee+tuple(12+i for i in cc)
            seen=set()
            for f in factors:
                key=tuple(f[i] for i in columns)
                if key in seen:break
                seen.add(key)
            else:return (ee,cc),scanned
    return None,scanned

def adaptive_three_optimized(rows,max_nodes=25000):
    """Try exact three-frame B3 belief recursion; NEVER treat timeout as false.

    More discriminating query partitions first; within each candidate, test
    largest ambiguous observation cells first. A FOUND/EXCLUDED is exhaustive
    over all ninety-six queries; UNKNOWN is a hard explicit resource bound.
    """
    from collections import defaultdict
    cache={};calls=[0]
    class Budget(Exception):pass
    def test(group,depth):
        if len(group)<=1:return (True,())
        if depth==0:return (False,None)
        key=(group,depth)
        if key in cache:return cache[key]
        calls[0]+=1
        if calls[0]>max_nodes:raise Budget
        if depth==1:
            for qi,row in enumerate(rows):
                if len({row[i] for i in group})==len(group):
                    cache[key]=(True,(qi,))
                    return cache[key]
            cache[key]=(False,None)
            return cache[key]
        candidates=[]
        for qi,row in enumerate(rows):
            parts=defaultdict(list)
            for i in group:parts[row[i]].append(i)
            if len(parts)<=1:continue
            sorted_parts=tuple(sorted((tuple(x) for x in parts.values()),
                                      key=len,reverse=True))
            candidates.append((len(parts),qi,sorted_parts))
        candidates.sort(key=lambda item:item[0],reverse=True)
        for _,qi,parts in candidates:
            proof=[];ok=True
            for part in parts:
                verdict,sub=test(part,depth-1)
                if not verdict:
                    ok=False;break
                proof.append((part,sub))
            if ok:
                cache[key]=(True,(qi,proof))
                return cache[key]
        cache[key]=(False,None)
        return cache[key]
    try:
        verdict,cert=test(tuple(range(len(rows[0]))),3)
        return ("FOUND" if verdict else "EXCLUDED",calls[0],len(cache),cert)
    except Budget:
        return ("UNKNOWN_BOUND_EXHAUSTED",calls[0],len(cache),None)

def audit(max_nodes=1000,optimized_budget=25000):
    states,layers=ball(3)
    assert len(states)==3502 and layers==[1,18,243,3240]
    factors,queries,rows=observations(states)
    non3=nonadaptive_witness(factors,3)
    print("ACTIVE_B3_P48_STATES",len(states),"edge_corner_queries",len(rows))
    print("ACTIVE_B3_NONADAPTIVE_3","FOUND" if non3 is not None else "EXCLUDED_12320_SITESETS")
    four,count=nonadaptive_four(factors)
    print("ACTIVE_B3_NONADAPTIVE_4","FOUND" if four else "EXCLUDED",
          "candidates_tested",count,"certificate",four)
    five,count5=nonadaptive_five(factors)
    print("ACTIVE_B3_NONADAPTIVE_5","FOUND" if five else "EXCLUDED",
          "candidates_tested",count5,"certificate",five)
    six,count6=nonadaptive_six(factors)
    print("ACTIVE_B3_NONADAPTIVE_6","FOUND" if six else "EXCLUDED",
          "candidates_tested",count6,"certificate",six)
    adaptive2,nodes,_=can_adapt(rows,2,budget=50000)
    print("ACTIVE_B3_ADAPTIVE_2","FOUND" if adaptive2 else "EXCLUDED","belief_nodes",nodes)
    if not adaptive2:
        try:
            adaptive3,nodes,_=can_adapt(rows,3,budget=max_nodes)
            print("ACTIVE_B3_ADAPTIVE_3","FOUND" if adaptive3 else "EXCLUDED",
                  "belief_nodes",nodes)
        except BudgetExceeded as exc:
            print("ACTIVE_B3_ADAPTIVE_3 UNKNOWN_BOUND_EXHAUSTED",exc)
    status,nodes,cached,certificate=adaptive_three_optimized(rows,optimized_budget)
    print("ACTIVE_B3_ADAPTIVE_3_OPTIMIZED",status,"belief_nodes",nodes,"memoized",cached)
    print("BOUNDARY B3 exhaustive statements only for searches that completed; B6 adaptive open")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--max-nodes",type=int,default=1000)
    parser.add_argument("--optimized-budget",type=int,default=25000)
    opt=parser.parse_args()
    audit(opt.max_nodes,opt.optimized_budget)
