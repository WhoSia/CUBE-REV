#!/usr/bin/env python3
"""54-facelet physical counterexample: observation gain versus goal progress.

Independent Python port of CUBE-REV 0.24's exact sticker-coordinate outer
HTM rotations. Compare the two full cube states U(SOLVED), U'(SOLVED).
Readout = orientation of the ORIGINAL UR edge cubie, tracked by its stickers,
not just orientation of a positional slot. Goal distance is exact within
the depth-two solved-ball. Scope: one-step goal-distance versus immediate
binary readout, NOT a full adaptive goal-policy optimality claim.
"""
from __future__ import annotations
import json
from collections import deque

F="URFDLB"
N={"U":(0,1,0),"R":(1,0,0),"F":(0,0,1),
   "D":(0,-1,0),"L":(-1,0,0),"B":(0,0,-1)}
G={"U":(1,1,-1),"R":(0,1,-1),"F":(2,1,-1),
   "D":(1,-1,1),"L":(0,-1,1),"B":(2,-1,1)}
A=tuple(f+s for f in F for s in ("","'","2"))
EDGES=(("U","R"),("U","F"),("U","L"),("U","B"),
       ("D","R"),("D","F"),("D","L"),("D","B"),
       ("F","R"),("F","L"),("B","L"),("B","R"))

def rotate(v,axis,count):
    x,y,z=v
    for _ in range(count%4):
        if axis==0:y,z=-z,y
        elif axis==1:x,z=z,-x
        else:x,y=-y,x
    return x,y,z

def physical_cube():
    slots=[]
    for f in F:
        n=N[f];face=[]
        for x in (-1,0,1):
            for y in (-1,0,1):
                p=(n[0],x,y) if n[0] else ((x,n[1],y) if n[1] else (x,y,n[2]))
                face.append((p,n))
        face.sort(key=lambda q:",".join(map(str,q[0])))
        slots.extend(face)
    assert len(set(slots))==54
    loc={s:i for i,s in enumerate(slots)}
    perms=[]
    for action in A:
        axis,layer,quarter=G[action[0]]
        power=3 if action.endswith("'") else 2 if action.endswith("2") else 1
        perm=[]
        for p,n in slots:
            t=(rotate(p,axis,quarter*power),rotate(n,axis,quarter*power)) if p[axis]==layer else (p,n)
            perm.append(loc[t])
        assert sorted(perm)==list(range(54))
        perms.append(perm)
    edges=[]
    for f,g in EDGES:
        n,m=N[f],N[g]
        p=tuple(n[i]+m[i] for i in range(3))
        edges.append((loc[(p,n)],loc[(p,m)]))
    return perms,edges

def run():
    perms,edges=physical_cube()
    solved="".join(f*9 for f in F)
    def turn(s,action):
        out=["?"]*54
        for i,j in enumerate(perms[A.index(action)]):out[j]=s[i]
        return "".join(out)
    def read(s):
        for i,j in edges:
            if {s[i],s[j]}=={"U","R"}:
                return int(s[i]!="U")
        raise AssertionError("lost original UR cubie")
    depths={solved:0};frontier=[solved]
    for d in (1,2):
        nxt=[]
        for s in frontier:
            for action in A:
                new=turn(s,action)
                if new not in depths:
                    depths[new]=d;nxt.append(new)
        frontier=nxt
    assert sum(d==1 for d in depths.values())==18
    assert sum(d==2 for d in depths.values())==243
    state_u=turn(solved,"U")
    state_up=turn(solved,"U'")
    assert read(state_u)==read(state_up)==0
    columns=[]
    for action in A:
        after=(turn(state_u,action),turn(state_up,action))
        assert all(s in depths for s in after)
        columns.append({"action":action,"immediately_distinguishes":read(after[0])!=read(after[1]),
                        "worst_goal_distance_after_action":max(depths[s] for s in after)})
    min_goal=min(c["worst_goal_distance_after_action"] for c in columns)
    goal_best=[c["action"] for c in columns if c["worst_goal_distance_after_action"]==min_goal]
    informative=[c for c in columns if c["immediately_distinguishes"]]
    assert goal_best==["U","U'","U2"],goal_best
    assert [c["action"] for c in informative]==["F","F'","B","B'"],informative
    assert min(c["worst_goal_distance_after_action"] for c in informative)==2
    return {"status":"FULL54_GOAL_INFORMATION_CONFLICT_PASS",
            "initial_scrambles":["U","U'"],"tracked_cubie":"original UR edge",
            "initial_readouts":[0,0],"goal_optimal_actions":goal_best,
            "goal_optimal_worst_distance":1,
            "information_actions":[c["action"] for c in informative],
            "informative_worst_goal_distance":2,
            "full_cubie_bfs_counts":{"radius_0":1,"radius_1":18,"radius_2":243},
            "all_actions":columns,
            "scope":"ONE_STEP_EXACT_GOAL_DISTANCE_AND_ONE_BIT_READOUT_NOT_LONG_HORIZON_POLICY"}
if __name__=="__main__":print(json.dumps(run(),sort_keys=True,indent=2))
