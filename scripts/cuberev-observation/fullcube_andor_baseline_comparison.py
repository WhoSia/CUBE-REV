#!/usr/bin/env python3
"""Fair same-domain AND/OR contingent-planning algorithm comparison.

Three admissible pruning baselines share the SAME 54-facelet actions, sensors,
belief transitions, worst-case goal and 18HTM action cost:
- plain (unpruned) classical finite-horizon AND/OR DP
- projected UR+DF+BL edge-pattern database lower bound
- solved-ball exact radius-4 lower bound (0.24-style small geodesic frontier)
- combined max of both admissible bounds.

No third-party FOND/POMDP solver is claimed to have run, and stopwatch
times are diagnostic only (not a controlled hardware benchmark). An
unlisted cube state has true solved distance >=5 from radius-4 BFS.
"""
from __future__ import annotations
import collections,functools,json,time
from fullcube_policy_family_benchmark import Benchmark,INF
from fullcube_goal_info_conflict import A
from fullcube_sensor_goal_theorem import factor
from fullcube_goal_pattern_databases import build_pattern_database

TAGS=(0,5,10)

class MultiSensorBenchmark(Benchmark):
    def __init__(self):
        super().__init__(radius=4)
    @functools.lru_cache(maxsize=300000)
    def observe(self,state):
        return tuple(factor(state,t)&1 for t in TAGS)

def solve_case(m,pdb,starts,horizon,mode):
    initial=tuple(sorted(m.turn(m.solved,A.index(a)) for a in starts))
    @functools.lru_cache(None)
    def lower(state):
        if mode=='plain':return 0
        b=pdb[tuple(factor(state,t) for t in TAGS)] if mode in ('pdb','combined') else 0
        if mode in ('radius4','combined'):
            b=max(b,m.depth.get(state,5))
        return b
    counters={'expanded_beliefs':0,'evaluated_actions':0}
    @functools.lru_cache(None)
    def dp(belief,h):
        if all(x==m.solved for x in belief):return 0
        if h==0:return INF
        if any(lower(x)>h for x in belief):return INF
        counters['expanded_beliefs']+=1
        best=INF
        for action in range(18):
            children=m.branches(belief,action)
            if any(any(lower(x)>h-1 for x in child) for child in children):
                continue
            counters['evaluated_actions']+=1
            worst=0
            for child in children:
                worst=max(worst,dp(child,h-1))
                if 1+worst>=best:break
            best=min(best,1+worst)
        return best
    start=time.perf_counter()
    result=dp(initial,horizon)
    elapsed=time.perf_counter()-start
    return {'exact_cost_within_horizon':result if result<INF else None,
            'cached_belief_horizon_states':dp.cache_info().currsize,
            **counters,'diagnostic_seconds':round(elapsed,6)}

def audit():
    m=MultiSensorBenchmark()
    pdb=build_pattern_database(TAGS)
    assert len(pdb)==10560
    cases=[('U',"U'"),('F','D'),('B','L'),('U','R')]
    rows=[]
    for starts in cases:
        result={mode:solve_case(m,pdb,starts,3,mode)
                for mode in ('plain','pdb','radius4','combined')}
        assert {r['exact_cost_within_horizon'] for r in result.values()}=={3}
        assert result['plain']['evaluated_actions']>result['pdb']['evaluated_actions']
        assert result['pdb']['evaluated_actions']>result['radius4']['evaluated_actions']
        rows.append({'initial_full_cube_scrambles':list(starts),'methods':result})
    return {'status':'FAIR_SAME_DOMAIN_ANDOR_BASELINE_PASS',
            'sensors':['UR','DF','BL'],'action_alphabet':18,
            'goal':'all 54 stickers solved','readout':'noiseless tag orientations after each move',
            'objective':'worst-case turn cost','horizon':3,
            'cases':rows,'external_third_party_solver_benchmarked':False,
            'historic_027_large_solver_invoked':False,
            'global_significance':'restricted finite states/horizon only'}
if __name__=='__main__':
    print(json.dumps(audit(),sort_keys=True,indent=2))
