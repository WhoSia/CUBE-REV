#!/usr/bin/env python3
"""Exact shortest 18-HTM travel between fixed active probe frames, then TSP DP.

This is a physical MOVE-COST result, not just a count of observations.
Each frame is a specific 48-sticker permutation derived by physical P48
joint cubie-position reachability. Exact <=6 pairwise HTM geodesics are
certified via a complete radius-three meet-in-the-middle search; then
Held--Karp dynamic programming finds the shortest route over the frames.
It does NOT optimize which different physical transformation realizes each
interrogated site pair, nor adaptive per-observation branches.
"""
from collections import deque
from functools import lru_cache
from b6_independent_48sticker_goals import MOVES,compose,inverse,word,EDGE_POS,CORNERS
from active_p48_fixed_site_scan import eleven_frame_scan
from active_p48_b6_ten_frame_bridge import ten_frame_b6_plan

ID=bytes(range(48))

def ball3_words():
    words={ID:()}
    q=deque([ID])
    while q:
        state=q.popleft()
        seq=words[state]
        if len(seq)==3:continue
        for token,turn in MOVES.items():
            next_state=compose(turn,state)
            if next_state not in words:
                words[next_state]=seq+(token,)
                q.append(next_state)
    assert len(words)==3502, len(words)
    return words

def shortest_six(delta,records,inv_records=None):
    """Return true shortest word of length <=6 by exact 3+3 splitting."""
    if inv_records is None:inv_records=[(s,inverse(s),seq) for s,seq in records.items()]
    current=None
    for state,inv,initial in inv_records:
        if current is not None and len(initial)>=len(current):break
        companion=compose(delta,inv)
        end=records.get(companion)
        if end is None:continue
        candidate=initial+end
        if word(" ".join(candidate))!=delta:
            raise AssertionError("P48 factor group path mismatch")
        if current is None or len(candidate)<len(current):
            current=candidate
        if current is not None and len(current)<=1:break
    if current is None:raise AssertionError("six-turn geometric bound violated")
    return current

def exact_route(plan,records):
    frames=[word(" ".join(w)) for e,c,w in plan]
    if len(set(frames))!=len(frames):
        raise AssertionError("duplicate full physical frame states")
    inv_records=sorted(((s,inverse(s),w) for s,w in records.items()),key=lambda p:len(p[2]))
    start=[shortest_six(s,records,inv_records) for s in frames]
    n=len(frames)
    transition={}
    for i in range(n):
        for j in range(n):
            if i!=j:
                delta=compose(frames[j],inverse(frames[i]))
                transition[(i,j)]=shortest_six(delta,records,inv_records)
    for (i,j),moves in transition.items():
        if len(moves)!=len(transition[(j,i)]):
            raise AssertionError("non-symmetric HTM word metric")
        if compose(word(" ".join(moves)),frames[i])!=frames[j]:
            raise AssertionError("relative frame HTM wrong")
    full=(1<<n)-1
    dp={}
    predecessor={}
    for j in range(n):
        dp[(1<<j,j)]=len(start[j])
        predecessor[(1<<j,j)]=None
    for mask in range(1,full+1):
        for last in range(n):
            key=(mask,last)
            if key not in dp:continue
            for next_i in range(n):
                if mask>>next_i&1:continue
                successor=(mask|(1<<next_i),next_i)
                cost=dp[key]+len(transition[(last,next_i)])
                if successor not in dp or cost<dp[successor]:
                    dp[successor]=cost
                    predecessor[successor]=last
    last=min(range(n),key=lambda j:dp[(full,j)])
    optimum=dp[(full,last)]
    reverse=[]
    mask=full
    while True:
        reverse.append(last)
        prev=predecessor[(mask,last)]
        if prev is None:break
        mask ^= 1<<last
        last=prev
    route=tuple(reversed(reverse))
    if len(route)!=n or len(set(route))!=n:
        raise AssertionError("Held Karp route invalid")
    current=ID
    relative=[]
    for step,i in enumerate(route):
        commands=start[i] if step==0 else transition[(route[step-1],i)]
        current=compose(word(" ".join(commands)),current)
        if current!=frames[i]:raise AssertionError("optimal route physical replay failure")
        relative.extend(commands)
    if len(relative)!=optimum:raise AssertionError("route cost mismatch")
    baseline=len(start[0])+sum(len(transition[(i-1,i)]) for i in range(1,n))
    assert optimum<=baseline
    return {"n":n,"fixed_frame_sequence_cost":baseline,
            "best_fixed_frame_sequence_cost":optimum,
            "route":route,"movement_word":tuple(relative),
            "unique_frame_states":len(set(frames)),
            "completed_pairwise_geodesics":len(transition)//2,
            "ball3_states":len(records)}

def audit():
    records=ball3_words()
    for scenario,plan in (
      ("G_FULL_11",eleven_frame_scan()),
      ("B6_10",ten_frame_b6_plan()[0])
    ):
        report=exact_route(plan,records)
        print("ACTIVE_ROUTE",scenario,"observations",report["n"],
              "baseline_HTM",report["fixed_frame_sequence_cost"],
              "optimal_fixed_frame_HTM",report["best_fixed_frame_sequence_cost"],
              "pairwise_checked",report["completed_pairwise_geodesics"])
        print("ACTIVE_ROUTE_ORDER",scenario,"indices",",".join(map(str,report["route"])))
        print("ACTIVE_ROUTE_MOVES",scenario," ".join(report["movement_word"]))
    print("ACTIVE_FIXED_FRAME_ROUTE_EXACT_PASS")
    print("BOUNDARY fixed frame representatives only; global motion-cost optimum OPEN")

if __name__=="__main__":
    audit()
