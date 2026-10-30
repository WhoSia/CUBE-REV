#!/usr/bin/env python3
"""Independently re-execute the SMALL-radius CUBE-REV 0.27 P22 court.

Historical 0.27 P22 source in WhoSia/CUBE-REV:
docs/0.27/P22_INDUCTIVE_STATE_SUPERSET_CERTIFICATE_AND_MIXED_RADIUS.md
The full WCA source is the exact fixed 20-action published scramble in
the 0.27 Notion genealogy. We independently regenerate the physical
source and goal radius-3 balls from 0.24 54-sticker actions.

P22: both radius-3 balls have layers (1,18,243,3240), 9432
directed action transitions from layers 0-2, and are disjoint.
Consequently source-to-goal HTM distance >=7. This does NOT re-run
0.27's deep C++ depth-11/B6 search or assert d>=17 or d=18.
"""
from __future__ import annotations
import json
from fullcube_edge_kernel_radius4 import START,turn
from fullcube_goal_info_conflict import A
FROZEN_WCA="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2".split()
def ball3(root):
    visited={root};layers=[[root]]
    for depth in range(1,4):
        nxt=[]
        for state in layers[-1]:
            for a in range(18):
                nxtstate=turn(state,a)
                if nxtstate not in visited:
                    visited.add(nxtstate);nxt.append(nxtstate)
        layers.append(nxt)
    assert [len(x) for x in layers]==[1,18,243,3240]
    return visited,layers

def audit():
    s=START
    for action in FROZEN_WCA:
        s=turn(s,A.index(action))
    source,source_layers=ball3(s)
    goal,goal_layers=ball3(START)
    common=source.intersection(goal)
    assert not common
    directed=2*(1+18+243)*18
    assert directed==9432
    return {'status':'INDEPENDENT_027_P22_RADIUS3_PHYSICAL_BRIDGE_PASS',
        'original_WCA_scramble':FROZEN_WCA,
        'source_and_goal_radius3_layers':[1,18,243,3240],
        'radius3_source_goal_intersection_size':len(common),
        'checked_directed_radius0_to2_successors':directed,
        'proved_full_cube_goal_HTM_lower_bound':7,
        'historical_027_deep_depth11_B6_backend_actually_run':False,
        'global_027_WCA_distance_17_or_18_decided':False}
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,indent=2))
