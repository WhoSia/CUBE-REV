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

def audit(max_nodes=1000):
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
    print("BOUNDARY B3 exhaustive statements only for searches that completed; B6 adaptive open")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--max-nodes",type=int,default=1000)
    audit(parser.parse_args().max_nodes)
