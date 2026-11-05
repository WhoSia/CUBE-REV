#!/usr/bin/env python3
"""Comparable HTM action-cost court for 21/22/24 fixed color-probe scans.

All scans use the SAME one-facelet-six-color, one stationary edge and one
stationary corner readout channel, and known deterministic 18 HTM controls.
For each certified scan-site schedule, a deterministic nearest-neighbor plus
two-opt heuristic reorders fixed physical readout frame representatives.
Every physical relative action word is checked exactly as a full P48 map.
Every reordered scan is retested on all B2 states. Numbers are achieved
costs for these specific frame sets, NOT global route optima.
"""
from collections import OrderedDict
from b6_independent_48sticker_goals import compose,inverse,word
from audit_active_p48_small_ball_decision_trees import ball
from construct_color_p48_24_frame_scanner import scan_plan,reconstruct_from_colors
from construct_color_p48_22_frame_parity_scan import plan22,reconstruction22
from construct_color_p48_21_frame_legality_scan import plan21,recover21
from optimize_color_p48_24_frame_route import (
    frames_and_weights,best_route,route_cost,directed_transition
)

def audit():
    balls,_=ball(2)
    tasks=(
        (24,scan_plan(),lambda state,rows:reconstruct_from_colors(state,rows)),
        (22,plan22(),lambda state,config:reconstruction22(state,config)),
        (21,plan21(),lambda state,config:recover21(state,config)),
    )
    results={}
    for count,config,recover in tasks:
        if count==24:plan=config;metadata=None
        else:plan=config[0];metadata=config[1:]
        words,weights,initial,_=frames_and_weights(plan)
        original_cost=route_cost(tuple(range(count)),weights,initial)
        optimized_cost,order=best_route(weights,initial)
        assert len(order)==len(set(order))==count
        arranged=[plan[i] for i in order]
        actual_frame=bytes(range(48))
        last=()
        total=0
        for _,_,commands in arranged:
            path=directed_transition(last,commands)
            actual_frame=compose(word(" ".join(path)),actual_frame)
            assert actual_frame==word(" ".join(commands))
            total+=len(path);last=commands
        assert total==optimized_cost
        if count==24:reconstruction_input=arranged
        else:reconstruction_input=(arranged,)+metadata
        for state in balls:
            assert recover(state,reconstruction_input)==tuple(state)
        results[count]={"initial_HTM":original_cost,
                        "reordered_HTM":optimized_cost,"order":order}
        print(f"COLOR_P48_PARETO_{count}_FRAMES_EXACT_PHYSICAL_REPLAY_PASS",
              "initial_HTM",original_cost,"optimized_HTM",optimized_cost,
              "tested_B2_states",len(balls))
    assert set(results)=={21,22,24}
    assert results[24]["reordered_HTM"]==136
    print("COLOR_P48_OBSERVATION_ACTION_CONCRETE_TRADEOFF_PASS")
    print("BOUNDARY heuristics only; no optimal route, joint-frame, or sensor equivalence theorem beyond declared color channel")
    return results

if __name__=="__main__":
    audit()
