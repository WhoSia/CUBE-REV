#!/usr/bin/env python3
"""Exact bounded full-54-sticker adaptive goal-policy family benchmark.

CUBE-REV 0.24 physical geometry is reused from fullcube_goal_info_conflict.
The sensor follows the original UR edge piece; one noiseless bit after each
18HTM action. Goal means that the COMPLETE physical cube is solved.

Baselines are FIRST-MOVE heuristics with exact adaptive continuation:
(1) minimum next-step worst goal distance and (2) maximum next-step binary
information (minimum largest observation-branch population). They are not
end-to-end greedy policies. Exact minimax is the third policy.

A no-policy within horizon result is NOT global impossibility. But two
distinct full cubes with identical tracked UR edge position and orientation
are permanently indistinguishable under every adaptive action sequence.
"""
from __future__ import annotations
import collections
import functools
import itertools
import json
import random
from fullcube_goal_info_conflict import A,F,physical_cube

INF=10**7

class Benchmark:
    def __init__(self,radius=4):
        self.perms,self.edges=physical_cube()
        self.solved=''.join(f*9 for f in F)
        self.depth={self.solved:0}
        self.layers=[[self.solved]]
        for d in range(1,radius+1):
            layer=[]
            for state in self.layers[-1]:
                for action in range(18):
                    next_state=self.turn(state,action)
                    if next_state not in self.depth:
                        self.depth[next_state]=d
                        layer.append(next_state)
            self.layers.append(layer)
        assert [len(a) for a in self.layers[:5]]==[1,18,243,3240,43239]

    @functools.lru_cache(maxsize=500000)
    def turn(self,state,action):
        after=['?']*54
        for i,j in enumerate(self.perms[action]):
            after[j]=state[i]
        return ''.join(after)

    @functools.lru_cache(maxsize=500000)
    def factor(self,state):
        for slot,(i,j) in enumerate(self.edges):
            if {state[i],state[j]}=={'U','R'}:
                return (slot,int(state[i]!='U'))
        raise AssertionError("original UR edge absent")

    def observe(self,state):
        return self.factor(state)[1]

    def branches(self,belief,action):
        parts=collections.defaultdict(set)
        for state in belief:
            next_state=self.turn(state,action)
            parts[self.observe(next_state)].add(next_state)
        return [tuple(sorted(z)) for _,z in sorted(parts.items())]

    @functools.lru_cache(maxsize=1000000)
    def value(self,belief,horizon):
        if all(s==self.solved for s in belief):
            return 0
        if horizon==0:
            return INF
        if any(self.depth.get(s,INF)>horizon for s in belief):
            return INF
        best=INF
        for action in range(18):
            parts=self.branches(belief,action)
            if any(any(self.depth.get(s,INF)>horizon-1 for s in part)
                   for part in parts):
                continue
            worst=0
            for part in parts:
                worst=max(worst,self.value(part,horizon-1))
                if worst+1>=best:
                    break
            best=min(best,1+worst)
        return best

    def forced_first_cost(self,belief,action,horizon):
        return 1+max(self.value(b,horizon-1)
                     for b in self.branches(belief,action))

    def evaluate(self,belief,horizon=5):
        belief=tuple(sorted(belief))
        best=next((h for h in range(horizon+1)
                   if self.value(belief,h)<INF),None)
        actions=[]
        for action in range(18):
            parts=self.branches(belief,action)
            cost=self.forced_first_cost(belief,action,horizon)
            actions.append((action,
                max(self.depth.get(s,INF) for part in parts for s in part),
                max(len(part) for part in parts),
                cost if cost<INF else None))
        goal=min(actions,key=lambda x:(x[1],x[0]))
        info=min(actions,key=lambda x:(x[2],x[1],x[0]))
        return {
            "opt":best,
            "goal":{"action":A[goal[0]],"cost":goal[3],
                    "next_worst_distance":goal[1]},
            "information":{"action":A[info[0]],"cost":info[3],
                           "max_branch_size":info[2]},
            "optimal_first_actions":[A[x[0]] for x in actions
                                     if best is not None and x[3]==best]
        }

def summary(cases):
    def category(item,method):
        if item["opt"] is None:return "NO_POLICY_WITHIN_HORIZON"
        cost=item[method]["cost"]
        if cost is None:return ">HORIZON"
        return "equal" if cost==item["opt"] else "+"+str(cost-item["opt"])
    return {
        "cases":len(cases),
        "optimal_cost":dict(sorted(collections.Counter(
            ">HORIZON" if r["opt"] is None else str(r["opt"])
            for r in cases).items())),
        "goal_first":dict(sorted(collections.Counter(
            category(r,"goal") for r in cases).items())),
        "information_first":dict(sorted(collections.Counter(
            category(r,"information") for r in cases).items()))
    }

def benchmark():
    m=Benchmark(radius=4)
    states=m.layers[1]
    groups=collections.defaultdict(list)
    for i,state in enumerate(states):
        groups[m.factor(state)].append(A[i])
    assert sorted(map(len,groups.values()))==[1,1,1,1,1,1,12]
    # Check factor closure in the finite sample: the argument for all
    # states is geometric, since actions move the tracked cubie alone.
    for group in groups.values():
        for action in range(18):
            outcomes={m.factor(m.turn(m.turn(m.solved,A.index(w)),action))
                      for w in group}
            assert len(outcomes)==1
    pairs=[]
    for i,j in itertools.combinations(range(18),2):
        if m.factor(states[i])==m.factor(states[j]):
            continue
        pairs.append(m.evaluate((states[i],states[j]),horizon=5))
    assert len(pairs)==87
    triples=[]
    for ids in itertools.combinations(range(18),3):
        if len({m.factor(states[i]) for i in ids})!=3:
            continue
        triples.append(m.evaluate(tuple(states[i] for i in ids),horizon=5))
    assert len(triples)==200
    rng=random.Random(261030)
    depth2=[]
    same_factor=0
    for _ in range(90):
        a,b=rng.sample(m.layers[2],2)
        if m.observe(a)!=m.observe(b):continue
        same_factor+=m.factor(a)==m.factor(b)
        depth2.append(m.evaluate((a,b),horizon=4))
    example=m.evaluate((states[A.index('U')],states[A.index("U'")]),horizon=5)
    assert example["opt"]==3
    assert example["goal"]["action"]=="U" and example["goal"]["cost"]==5
    assert example["information"]["action"]=="F"
    assert example["information"]["cost"]==3
    result={
        "schema":"cube-rev.fullcube-goal-information-family-v1",
        "physics":"CUBE-REV 0.24 exact 54-facelet 18HTM",
        "readout":"original UR edge piece orientation, noiseless",
        "objective":"minimax total turns to entire cube solved",
        "baseline_scope":"first greedy move, then exact adaptive completion",
        "solved_ball_counts":{str(i):len(a) for i,a in enumerate(m.layers)},
        "one_move_factor_classes":{str(k):v for k,v in groups.items()},
        "two_state_depth1":{"total":153,
            "unbounded_impossible_by_closed_factor":66,**summary(pairs)},
        "three_state_depth1":{"total":816,
            "unbounded_impossible_by_closed_factor":616,**summary(triples)},
        "two_state_depth2_sample":{"attempts":90,"accepted":len(depth2),
            "seed":261030,"same_initial_readout":True,
            "unbounded_impossible_by_closed_factor":same_factor,
            **summary(depth2)},
        "U_vs_Uprime":example,
        "visited_belief_horizon_states":m.value.cache_info().currsize,
        "global_cube_planning_optimum_proven":False
    }
    assert result["two_state_depth1"]["optimal_cost"]=={"3":60,"5":27}
    assert result["two_state_depth1"]["goal_first"]=={"equal":27,"+1":4,"+2":56}
    assert result["two_state_depth1"]["information_first"]=={"equal":87}
    assert result["three_state_depth1"]["optimal_cost"]=={"5":56,">HORIZON":144}
    assert result["two_state_depth2_sample"]["accepted"]==85
    return result

if __name__=="__main__":
    print(json.dumps(benchmark(),sort_keys=True,indent=2))
