#!/usr/bin/env python3
"""Improve P48 two single-facelet 24-frame scanner via physical no-reset routing.

The 24 readout frame permutations are prescribed by the independently built
576-sticker-pair orbit and provide full-group reconstruction. This program
changes their order, NOT their 24 physical query pairs, and minimizes the
length of a valid no-reset turn word under simple adjacent same-face move
cancellation. It uses deterministic best-start nearest-neighbor + best
two-opt improvement, then verifies every transition with actual P48 48-slot
permutation equality. No claim of the globally minimum HTM route is made.
"""
from b6_independent_48sticker_goals import compose,inverse,word
from construct_color_p48_24_frame_scanner import (
    scan_plan,reconstruct_from_colors, inverted_token,
)
from audit_active_p48_small_ball_decision_trees import ball

def normalized(tokens):
    """Only adjacent same-face reductions; exact in 18 HTM."""
    stack=[]
    for token in tokens:
        face=token[0]
        power=2 if token.endswith("2") else 3 if token.endswith("'") else 1
        if stack and stack[-1][0]==face:
            _,old=stack.pop()
            power=(power+old)%4
        if power:
            stack.append((face,power))
    return tuple(f+("2" if n==2 else "'" if n==3 else "")
                 for f,n in stack)

def directed_transition(a,b):
    raw=tuple(inverted_token(t) for t in reversed(a))+tuple(b)
    short=normalized(raw)
    assert word(" ".join(short))==compose(word(" ".join(b)),
                                          inverse(word(" ".join(a))))
    return short

def frames_and_weights(plan):
    words=[commands for e,c,commands in plan]
    n=len(words)
    weights=[[0]*n for _ in range(n)]
    transitions={}
    for i in range(n):
        for j in range(n):
            if i==j:continue
            path=directed_transition(words[i],words[j])
            weights[i][j]=len(path)
            transitions[(i,j)]=path
    initial=[len(normalized(seq)) for seq in words]
    assert all(weights[i][j]==weights[j][i] for i in range(n) for j in range(n))
    return words,weights,initial,transitions

def route_cost(order,weights,initial):
    return initial[order[0]]+sum(weights[a][b] for a,b in
                                zip(order,order[1:]))

def best_route(weights,initial):
    n=len(initial)
    best=None
    for first in range(n):
        remaining=set(range(n));remaining.remove(first);sequence=[first]
        while remaining:
            chosen=min(remaining,key=lambda x:(weights[sequence[-1]][x],x))
            sequence.append(chosen);remaining.remove(chosen)
        improved=True
        while improved:
            improved=False
            baseline=route_cost(sequence,weights,initial)
            for i in range(n-1):
                for j in range(i+1,n):
                    alternative=sequence[:i]+list(reversed(sequence[i:j+1]))+sequence[j+1:]
                    value=route_cost(alternative,weights,initial)
                    if value<baseline:
                        sequence=alternative
                        improved=True
                        break
                if improved:break
        actual=route_cost(sequence,weights,initial)
        if best is None or actual<best[0] or (actual==best[0] and tuple(sequence)<best[1]):
            best=(actual,tuple(sequence))
    return best

def audit():
    plan=scan_plan()
    words,weights,initial,transitions=frames_and_weights(plan)
    original=tuple(range(24))
    initial_cost=route_cost(original,weights,initial)
    optimum_heuristic,ordered=best_route(weights,initial)
    assert optimum_heuristic<=initial_cost
    optimized=[plan[i] for i in ordered]
    # Execute all 24 exact physical relative turns from the solved frame.
    physical=bytes(range(48));previous=()
    moves=0
    for e,c,commands in optimized:
        path=directed_transition(previous,commands)
        physical=compose(word(" ".join(path)),physical)
        assert physical==word(" ".join(commands))
        moves+=len(path)
        previous=commands
    assert moves==optimum_heuristic
    # All distinct sticker slots remain read once, independent of order.
    b2states,_=ball(2)
    for state in b2states:
        assert reconstruct_from_colors(state,optimized)==tuple(state)
    print("COLOR_P48_REORDER_24_FRAMES_PHYSICAL_REPLAY_PASS",len(optimized))
    print("COLOR_P48_REORDER_HTM",initial_cost,"->",optimum_heuristic)
    print("COLOR_P48_REORDER_QUERY_INDICES",",".join(map(str,ordered)))
    print("COLOR_P48_REORDER_B2_262_STATES_PASS")
    print("BOUNDARY deterministic 2opt local improvement only, not global HTM optimum")
    return {"initial_reduced_htm":initial_cost,"heuristic_htm":optimum_heuristic,
            "order":ordered,"frames":len(optimized)}

if __name__=="__main__":
    audit()
