#!/usr/bin/env python3
"""Finite-horizon minimax adaptive cube-edge identification with one visible erasure.

This is a REAL action-contingent policy: next HTM turn may depend on the
received bit or erasure symbol. State = remaining possible (source,edge-state)
pairs, erasures remaining; the source identity never enters policy choices.
Each turn costs one; STOP costs zero only with one possible source.
Solver uses full search with memoization on caller-bounded horizons.
A reported infeasible horizon is certified only for that specified initial
source group, alphabet and horizon, never for the global M* dictionary.
"""
from __future__ import annotations
from functools import lru_cache
import argparse,itertools,json
from physical_edges import ACTIONS,edge_transitions

INF=10**6
MOVES=edge_transitions()

def solve(sources, max_turns=3, alphabet=tuple(range(18)), erasures=1):
    initial=tuple((p,2*p) for p in sorted(sources))
    assert len({p for p,_ in initial})==len(initial)
    @lru_cache(None)
    def dp(belief,remaining,life):
        if len(belief)==1:return (0,None)
        if life==0:return (INF,None)
        best=(INF,None)
        for a in alphabet:
            moved=[(p,MOVES[a][state]) for p,state in belief]
            partition={0:[],1:[]}
            for p,state in moved:partition[state&1].append((p,state))
            branches=[(tuple(partition[b]),remaining) for b in (0,1) if partition[b]]
            if remaining>0:branches.append((tuple(moved),remaining-1))
            worst=0
            for next_b,r in branches:
                cost,_=dp(next_b,r,life-1)
                worst=max(worst,cost)
                if worst+1>=best[0]:break
            if worst<INF and (1+worst,a)<best:best=(1+worst,a)
        return best
    score,action=dp(initial,erasures,max_turns)
    return {"sources":list(sources),"horizon":max_turns,
            "action_count":len(alphabet),"one_known_erasure":bool(erasures),
            "status":"ADAPTIVE_POLICY_FEASIBLE" if score<INF else "NO_POLICY_WITHIN_SPECIFIED_HORIZON",
            "worst_case_turn_cost":score if score<INF else None,
            "initial_action":ACTIONS[action] if action is not None else None,
            "memoized_belief_states":dp.cache_info().currsize,
            "global_dictionary_optimality_proven":False}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--sources",default="0,1")
    p.add_argument("--horizon",type=int,default=3)
    p.add_argument("--max-actions",type=int,default=18)
    args=p.parse_args()
    src=tuple(int(x) for x in args.sources.split(","))
    assert 1<=args.horizon<=7 and 1<=args.max_actions<=18
    print(json.dumps(solve(src,args.horizon,tuple(range(args.max_actions))),
                     sort_keys=True))
