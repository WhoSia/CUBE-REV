#!/usr/bin/env python3
"""Multi-axis CUBE-REV 54-facelet goal-planning controls.

Sensors: one, two, or three tagged edge orientation bits, observed after
each 18HTM turn. Targets: full cube SOLVED vs tagged original UR edge
back at its solved position/orientation. The second target is a proper
goal relaxation: it must never be reported as a full cube solve.
Finite-horizon exact AND/OR solution (<=5) for designated start sets.
"""
from __future__ import annotations
import functools,json
from fullcube_policy_family_benchmark import Benchmark,INF
from fullcube_goal_info_conflict import A
from fullcube_sensor_goal_theorem import factor

SENSORS=((0,),(0,5),(0,5,10))
CASES=(('U',"U'"),('F','D'),('B','L'),('U','R'),('U','F'),('U',"U'",'U2'))

class MultiSensor(Benchmark):
    def __init__(self,tags):
        super().__init__(radius=4)
        self.tags=tags
    @functools.lru_cache(maxsize=300000)
    def observe(self,state):
        return tuple(factor(state,t)%2 for t in self.tags)

def audit():
    results=[]
    for tags in SENSORS:
        m=MultiSensor(tags)
        cohort=[]
        for starts in CASES:
            belief=tuple(sorted(m.turn(m.solved,A.index(x)) for x in starts))
            optimum=next((h for h in range(6)
                         if m.value(belief,h)<INF),None)
            # The edge-home target is independently satisfied for F,D,
            # although full solved is impossible with UR alone.
            goal_UR_home_all=all(factor(s,0)==factor(m.solved,0)
                                 for s in belief)
            cohort.append({'starts':list(starts),
                           'exact_full_cube_minimax_cost_le5':optimum,
                           'already_satisfies_UR_edge_home_goal':goal_UR_home_all})
        results.append({'tagged_edge_sensors':[
            ''.join(('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')[t])
            for t in tags],
            'cohorts':cohort})
    check=lambda i,j:results[i]['cohorts'][j]['exact_full_cube_minimax_cost_le5']
    assert check(0,1) is None and check(1,1)==3 and check(2,1)==3
    assert check(0,2) is None and check(1,2) is None and check(2,2)==3
    assert all(check(i,0)==3 for i in range(3))
    assert results[0]['cohorts'][1]['already_satisfies_UR_edge_home_goal']
    return {'status':'FULL54_MULTISENSOR_MULTI_GOAL_PASS',
            'full_cube_goal':'all 54 facelets solved',
            'alternate_goal':'original UR tagged edge is home',
            'observable':'orientation bits of selected tagged edge cubies, noiseless',
            'policy':'exact bounded minimax AND/OR with 18 HTM actions',
            'max_horizon':5,'results':results,
            'large_027_full_solver_used':False}
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,indent=2))
