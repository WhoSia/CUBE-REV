#!/usr/bin/env python3
"""R4 exact bounded two-frame six-color B2 comparison.

This is a finite B2 *posterior ambiguity* court, NOT full-group identification:
frame 1 at the fixed probes; choose an identity/no-motion or one legal
18-HTM move before frame 2. A feedback policy may choose that move after
observing the first color pair. For comparison, a nonadaptive second move
is fixed independently of the first readout. Both have <= 1 HTM cost
between frames; moves are physically applied in P48.

The reported mean posterior *cardinality* assumes an explicit uniform
prior over all 262 radius-two states. It is not a measured human cost or
a universal lower bound on observation horizons.
"""
from collections import defaultdict
from b6_independent_48sticker_goals import MOVES
from audit_active_p48_small_ball_decision_trees import ball
from audit_color_probe_information_bounds import two_one_facelet_colors

IDENTITY=bytes(range(48))
ACTIONS=(("IDENTITY",IDENTITY),)+tuple(MOVES.items())

def partition(indices,states,frame):
    groups=defaultdict(list)
    for idx in indices:
        groups[two_one_facelet_colors(states[idx],frame)].append(idx)
    return tuple(tuple(part) for part in groups.values())

def sum_squares(parts):
    return sum(len(part)**2 for part in parts)

def court():
    states,_=ball(2)
    assert len(states)==262
    branches=partition(tuple(range(len(states))),states,IDENTITY)
    assert sum(map(len,branches))==262
    # Explicitly enumerate each feasible second turn and each physically
    # attained observation partition. No surrogate information oracle.
    choices={}
    for branch in branches:
        candidates=[]
        for name,turn in ACTIONS:
            outcomes=partition(branch,states,turn)
            candidates.append((sum_squares(outcomes),max(map(len,outcomes)),
                               int(name!="IDENTITY"),name))
        choices[branch]=min(candidates)
    adaptive_numerator=sum(v[0] for v in choices.values())
    adaptive_worst=max(v[1] for v in choices.values())
    fixed_options=[]
    for name,turn in ACTIONS:
        outcomes=[partition(branch,states,turn) for branch in branches]
        fixed_options.append((sum(sum_squares(p) for p in outcomes),
                              max(max(map(len,p)) for p in outcomes),
                              int(name!="IDENTITY"),name))
    best_fixed=min(fixed_options)
    worst_fixed=min((item[1],item[2],item[3]) for item in fixed_options)
    # Independently minimize worst-case residual cardinality by branch.
    worst_adaptive=max(min(max(map(len,partition(branch,states,turn)))
                           for _,turn in ACTIONS) for branch in branches)
    assert adaptive_worst>=worst_adaptive
    assert adaptive_numerator==1976,(adaptive_numerator,choices)
    assert best_fixed[0]==2242,best_fixed
    assert worst_adaptive==worst_fixed[0]==18,(worst_adaptive,worst_fixed)
    # A cheaper one-frame stop is allowed on singleton branches; the fixed
    # policy can use the same stop rule, so this is NOT an adaptation gain.
    assert sum(1 for b in branches if len(b)==1)==5
    print("R4_COLOR_B2_TWO_FRAME_UNIFORM_POSTERIOR_PASS",
          "adaptive",adaptive_numerator,"fixed",best_fixed[0],
          "denominator",len(states),"fixed_move",best_fixed[3])
    print("R4_COLOR_B2_WORST_AMBIGUITY_PASS",
          "adaptive",worst_adaptive,"fixed",worst_fixed[0])
    print("R4_BOUNDARY finite B2, uniform prior only; 1-HTM second move;"
          " no complete identification, no measured cognitive costs")
    return adaptive_numerator,best_fixed[0],worst_adaptive

if __name__=="__main__":
    court()
