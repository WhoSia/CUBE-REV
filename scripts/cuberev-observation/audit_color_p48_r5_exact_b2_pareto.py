#!/usr/bin/env python3
"""CUBE-REV 0.28 R5: exact finite B2 two-frame information/action Pareto court.

Same physical six-color edge/corner probes and P48 B2 262-state world as R4.
Observation 1 is at the identity frame. For observation 2, select either
identity (0 HTM) or one legal face move (1 HTM), possibly after seeing the
first two colors. Every query uses actual moving-facelet P48 replay.

Exact cost vector (A,M):
  A = sum_{first-color branches taking a move} |branch|
      = 262 * E[additional HTM] under uniform B2 state prior.
  M = sum_{terminal joint-color histories} |belief|^2
      = 262 * E[terminal belief cardinality] under the same prior.
Both are integers with explicit physical meaning. Calculate all nondominated
(A,M) possibilities through an exact multiple-choice integer DP, not weights
or a heuristic. This is NOT a full-group horizon result or cognitive metric.
"""
from collections import defaultdict
from audit_active_p48_small_ball_decision_trees import ball
from audit_color_probe_information_bounds import two_one_facelet_colors
from b6_independent_48sticker_goals import MOVES

IDENTITY=bytes(range(48))
ACTIONS=(("NO_TURN",IDENTITY),)+tuple(MOVES.items())

def partition(indices,states,frame):
    groups=defaultdict(list)
    for idx in indices:
        groups[two_one_facelet_colors(states[idx],frame)].append(idx)
    return tuple(tuple(x) for x in groups.values())

def square_sum(groups):
    return sum(len(x)**2 for x in groups)

def dominated_frontier(points):
    """Points (moved-state mass, ambiguity numerator); minimize both."""
    answer=[]
    best=float("inf")
    for cost,score in sorted(points.items()):
        if score<best:
            answer.append((cost,score))
            best=score
    return answer

def court():
    states,_=ball(2)
    assert len(states)==262
    branches=partition(tuple(range(len(states))),states,IDENTITY)
    assert sum(map(len,branches))==262
    base=sum(len(b)**2 for b in branches)
    # For a first-reading belief branch, all physical one-move actions cost
    # the SAME amount |branch| in uniform-prior expected move units.
    # Thus only the one-move action with smallest residual matters for Pareto.
    options=[]
    for b in branches:
        candidates=[]
        for name,turn in ACTIONS:
            sub=partition(b,states,turn)
            candidates.append((name, square_sum(sub), max(map(len,sub))))
        free=next(row for row in candidates if row[0]=="NO_TURN")
        best=min((x for x in candidates if x[0]!="NO_TURN"),
                 key=lambda x:(x[1],x[2],x[0]))
        assert free[1]==len(b)**2
        options.append((len(b),free,best,candidates))
    # Exact multiple-choice knapsack: each observed first-color branch chooses
    # NO_TURN or one physical move; store the minimum possible ambiguity
    # for every exact expected movement mass (0..262).
    dp={0:(0,())}
    for n,free,best,candidates in options:
        updated={}
        for cost,(score,actions) in dp.items():
            for next_cost,next_score,name in (
                (cost,score+free[1],"NO_TURN"),
                (cost+n,score+best[1],best[0])
            ):
                old=updated.get(next_cost)
                if old is None or next_score<old[0]:
                    updated[next_cost]=(next_score,actions+(name,))
        dp=updated
    pareto=dominated_frontier({cost:x[0] for cost,x in dp.items()})
    assert pareto and pareto[0]==(0,base)
    # A parallel independent scalar solver checks each supported slope:
    # min over branches of [score + lambda * moved-state mass].
    for penalty in (0,1,2,3,5,8,13,21,34,55,89,144):
        direct=sum(min(free[1],best[1]+penalty*n)
                   for n,free,best,candidates in options)
        via_dp=min(score+penalty*cost for cost,(score,_) in dp.items())
        assert direct==via_dp,(penalty,direct,via_dp)
    # Recover baseline R4, while exposing actual movement usage.
    unconstrained=sum(min(c[1] for c in candidates)
                      for n,free,best,candidates in options)
    assert unconstrained==1976,unconstrained
    fixed=[]
    for name,turn in ACTIONS:
        score=sum(square_sum(partition(b,states,turn)) for b in branches)
        # Fixed joint second move, even if first observation is already
        # singleton. Execution is uniformly specified; no branch early stop.
        moved_mass=0 if name=="NO_TURN" else len(states)
        fixed.append((moved_mass,score,name))
    best_fixed=min(x[1] for x in fixed if x[0]>0)
    assert best_fixed==2242,best_fixed
    fixed_pareto=dominated_frontier(
        {0:next(x[1] for x in fixed if x[0]==0),
         262:best_fixed})
    # Most states remain ambiguous after two reads; neither is full ID.
    worst_adaptive=max(min(c[2] for c in candidates)
                       for n,free,best,candidates in options)
    worst_fixed=min(max(max(map(len,partition(b,states,turn)))
                        for b in branches) for name,turn in ACTIONS)
    assert worst_adaptive==worst_fixed==18,(worst_adaptive,worst_fixed)
    assert pareto[-1][1]==1976,(pareto[-1],unconstrained)
    assert all(0<=a<=262 and 1976<=m<=base for a,m in pareto)
    assert len(pareto)>=2
    assert len(pareto)==152,len(pareto)
    assert base==15194,base
    assert (113,3640) in pareto and (111,13760) in pareto
    assert pareto[-1]==(257,1976),pareto[-1]
    # Identify which actual color belief and physical turn produce the largest
    # one-branch reduction; this is a local structural explanation, not a
    # universal 'phase transition' theorem.
    branch_explanations=[]
    for b,(n,free,best,candidates) in zip(branches,options):
        first_color=two_one_facelet_colors(states[b[0]],IDENTITY)
        assert all(two_one_facelet_colors(states[i],IDENTITY)==first_color for i in b)
        branch_explanations.append((free[1]-best[1],n,first_color,best[0],
                                    free[1],best[1]))
    branch_explanations.sort(reverse=True)
    for saving,mass,colors,action,prior,after in branch_explanations[:5]:
        print("R5_B2_LARGEST_SINGLE_BRANCH_GAIN",
              "first_colors",",".join(colors),"mass",mass,
              "HTM",action,"ambiguity_before",prior,"after",after,
              "saving",saving)
    for a in (111,113,257):
        score,chosen=dp[a]
        moved=[(",".join(two_one_facelet_colors(states[b[0]],IDENTITY)),
                len(b),action) for b,action in zip(branches,chosen)
                if action!="NO_TURN"]
        assert sum(n for colors,n,action in moved)==a
        print("R5_B2_POLICY_AT_MASS",a,"M",score,
              "moved",repr(sorted(moved)))
    print("R5_B2_EXACT_PARETO_PASS",
          "states",len(states),"first_branches",len(branches),
          "points",len(pareto),"baseline_ambiguity",base)
    print("R5_B2_ADAPTIVE_PARETO_POINTS",
          ";".join(f"{a}:{m}" for a,m in pareto))
    print("R5_B2_FIXED_PARETO_POINTS",
          ";".join(f"{a}:{m}" for a,m in fixed_pareto))
    print("R5_B2_EXTREME_PASS",
          "adaptive_best",pareto[-1][1],"fixed_best",best_fixed,
          "worst_adaptive",worst_adaptive,"worst_fixed",worst_fixed)
    print("R5_B2_POLICY_BOUNDARY exact B2 uniform-prior/one-turn decision;"
          " no adaptive full-group optimality or human cognitive cost")
    return {"adaptive_pareto":pareto,"fixed_pareto":fixed_pareto,
            "first_branches":len(branches),"base":base,
            "adaptive_best":unconstrained,"fixed_best":best_fixed}

if __name__=="__main__":
    court()
