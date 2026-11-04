#!/usr/bin/env python3
"""Measure exact 18-HTM motion costs of a certified B3 adaptive scan tree.

A full, physically replayed P48 B3 adaptive policy uses at most four
observation frames; the optimal nonadaptive observation count is six.
This program adds action costs by recomputing shortest <=6 HTM transitions
between the CANONICAL full-48-sticker frame representatives chosen for every
interrogated (original edge site, original corner site) pair.

The route for every history is physically replayed; the 3502 legal B3
starting states produce a complete worst/average distribution. Six-frame
nonadaptive comparison optimizes order of a specified B3 valid six-frame
design by exact Held--Karp DP, again at fixed frame representatives.

These are NOT globally minimum motion costs over all alternative frame
representatives or over all adaptive policies of the same observation depth.
"""
from collections import Counter,defaultdict
from fractions import Fraction
from hashlib import sha256
from b6_independent_48sticker_goals import (
    CORNERS,EDGE_POS,compose,inverse,word,
)
from active_p48_fixed_site_scan import joint_position_words
from audit_active_p48_small_ball_decision_trees import ball,observations
from audit_active_p48_frame_route_cost import ball3_words,shortest_six,exact_route
from certify_active_p48_b3_adaptive_gap import payload,verify

ID=bytes(range(48))
def profile():
    proof=payload()
    verify(proof)
    states,_=ball(3)
    factors,queries,rows=observations(states)
    lookup={q:i for i,q in enumerate(queries)}
    mappings=joint_position_words()
    canonical={query:word(" ".join(mappings[(EDGE_POS[query[0]],CORNERS[query[1]])]))
               for query in queries}
    words=ball3_words()
    candidates=sorted(((s,inverse(s),seq) for s,seq in words.items()),key=lambda item:len(item[2]))
    edges={}
    def travel(before,after):
        key=(before,after)
        if key not in edges:
            first=ID if before is None else canonical[before]
            delta=compose(canonical[after],inverse(first))
            route=shortest_six(delta,words,candidates)
            assert word(" ".join(route))==delta
            edges[key]=route
        return edges[key]
    move_hist=Counter()
    depth_hist=Counter()
    detailed=[]
    trajectories=0
    for i,state in enumerate(states):
        node=proof["adaptive_tree"]
        current=None
        path=[]
        total=0
        while "leaf" not in node:
            pair=tuple(node["query"])
            actions=travel(current,pair)
            total+=len(actions)
            path.extend(actions)
            result=str(rows[lookup[pair]][i])
            node=node["branches"][result]
            current=pair
        if node["leaf"]!=i:
            raise AssertionError("policy leaf wrong under actual inverse factors")
        physical=word(" ".join(path))
        assert physical==canonical[current]
        move_hist[total]+=1
        # Observation count is reconstructed from the checked policy tree.
        detailed.append(total)
        trajectories+=1
    # Count observation frames from the independent policy tree.
    obs_hist=Counter()
    for i in range(len(states)):
        node=proof["adaptive_tree"];n=0
        while "leaf" not in node:
            pair=tuple(node["query"])
            node=node["branches"][str(rows[lookup[pair]][i])]
            n+=1
        obs_hist[n]+=1
    assert trajectories==3502 and sum(move_hist.values())==3502
    assert obs_hist==Counter({1:104,2:2939,3:443,4:16}),obs_hist
    assert len(edges)>0
    report=proof["nonadaptive_six"]
    fixed=[(EDGE_POS[e],CORNERS[c],mappings[(EDGE_POS[e],CORNERS[c])])
           for e,c in zip(report["edges"],report["corners"])]
    baseline=exact_route(fixed,words)
    assert baseline["n"]==6
    mean=Fraction(sum(detailed),len(detailed))
    print("ACTIVE_B3_ADAPTIVE_4_PHYSICAL_ACTION_COST_PASS",
          "states",len(states),"min_HTM",min(detailed),"max_HTM",max(detailed),
          "mean_HTM",str(mean),"distinct_transitions",len(edges))
    print("ACTIVE_B3_ADAPTIVE_OBSERVATION_HISTOGRAM",dict(sorted(obs_hist.items())))
    print("ACTIVE_B3_ADAPTIVE_HTM_HISTOGRAM",dict(sorted(move_hist.items())))
    print("ACTIVE_B3_NONADAPTIVE_6_FIXED_FRAME_ROUTE",
          "ordered_HTM",baseline["fixed_frame_sequence_cost"],
          "optimized_HTM",baseline["best_fixed_frame_sequence_cost"],
          "order",",".join(map(str,baseline["route"])))
    print("BOUNDARY optimal only for fixed canonical representatives and chosen policy/design")
    return {"states":len(states),"observation_histogram":obs_hist,
            "htm_histogram":move_hist,"max_htm":max(detailed),
            "mean_htm_numerator":mean.numerator,"mean_htm_denominator":mean.denominator,
            "nonadaptive_fixed_frame_optimized_htm":baseline["best_fixed_frame_sequence_cost"],
            "n_distinct_physical_transitions":len(edges)}

if __name__=="__main__":
    profile()
