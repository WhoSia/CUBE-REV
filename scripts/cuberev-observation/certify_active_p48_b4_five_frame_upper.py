#!/usr/bin/env python3
"""Construct and replay a complete five-frame adaptive P48 B4 scan policy.

All 46741 physical B4 states, 96 fixed edge/corner joint slot queries.
A greedy balanced-split construction supplies an upper bound only. The
four-frame adaptive decision problem is NOT decided by greedy failure.
"""
import argparse,json,hashlib
from collections import Counter
import numpy as np
from b6_independent_48sticker_goals import EDGE_POS,CORNERS,word,compose
from audit_active_p48_small_ball_decision_trees import observations
from audit_active_p48_b4_nonadaptive_horizon import b4_factors
from active_p48_fixed_site_scan import joint_position_words,REF_EDGE,REF_CORNER
from active_p48_b6_ten_frame_bridge import measured_inverse_factor
from b6_independent_48sticker_goals import MOVES

def full_states():
    eye=bytes(range(48));seen={eye};layer={eye}
    for _ in range(4):
        nxt={compose(turn,s) for s in layer for turn in MOVES.values()}
        layer=nxt-seen;seen.update(layer)
    assert len(seen)==46741
    return tuple(sorted(seen))

def build():
    states=full_states()
    factors,queries,_=observations(states)
    ff=np.asarray(factors,dtype=np.uint16)
    rows=np.asarray([ff[:,e]*24+ff[:,12+c] for e,c in queries],dtype=np.uint16)
    assert rows.shape==(96,46741)
    depth_counts=Counter()
    def create(group,depth):
        if len(group)==1:
            depth_counts[depth]+=1
            return {"leaf":int(group[0])}
        if depth>=5:raise AssertionError("greedy B4 policy exceeds 5 frames")
        best=None
        for q in range(96):
            hist=np.bincount(rows[q,group],minlength=576)
            ambiguity=int(hist@(hist-1))
            if best is None or ambiguity<best[0]:best=(ambiguity,q)
        q=best[1]
        readings=rows[q,group]
        ordering=np.argsort(readings,kind="stable")
        indices=group[ordering];vals=readings[ordering]
        starts=np.r_[0,np.flatnonzero(vals[1:]!=vals[:-1])+1,len(group)]
        if len(starts)<=2:raise AssertionError("unseparated nontrivial belief")
        branches={}
        for j in range(len(starts)-1):
            lo,hi=starts[j],starts[j+1]
            branches[str(int(vals[lo]))]=create(indices[lo:hi],depth+1)
        return {"query":list(queries[q]),"branches":branches}
    tree=create(np.arange(len(states)),0)
    assert dict(depth_counts)=={1:4,2:18120,3:27782,4:743,5:92},depth_counts
    frames=joint_position_words()
    frame_map={(e,c):word(" ".join(frames[(EDGE_POS[e],CORNERS[c])])) for e,c in queries}
    # Every decision is checked by actual physical P48 frame rotation and
    # stationary-slot occupancy/orientation, not merely by the search matrix.
    for i,s in enumerate(states):
        current=tree;depth=0
        while "leaf" not in current:
            e,c=current["query"];frame=frame_map[(e,c)]
            a=measured_inverse_factor(s,EDGE_POS[e],frame,REF_EDGE)
            b=measured_inverse_factor(s,CORNERS[c],frame,REF_CORNER)
            current=current["branches"][str(a*24+b)]
            depth+=1
        if current["leaf"]!=i or depth>5:
            raise AssertionError("physical B4 observed path does not identify state")
    result={"radius":4,"states":len(states),"adaptive_upper":5,
            "physical_state_sha256":hashlib.sha256(b"".join(states)).hexdigest(),
            "depth_histogram":dict(sorted(depth_counts.items())),
            "adaptive_tree":tree,
            "scope":"ideal two-slot complete cubie probes, no global action-cost proof"}
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--emit");o=p.parse_args()
    v=build()
    print("ACTIVE_B4_P48_ADAPTIVE_FIVE_FRAME_FULL_PHYSICAL_TREE_PASS",v["states"])
    print("ACTIVE_B4_ADAPTIVE_FIVE_DEPTH_HISTOGRAM",v["depth_histogram"])
    print("BOUNDARY adaptive B4 lower bound remains four, not disproved by greedy")
    if o.emit:
        with open(o.emit,"w") as f:json.dump(v,f,separators=(",",":"),sort_keys=True)
        with open(o.emit,"rb") as f:print("ACTIVE_B4_TREE_SHA256",hashlib.sha256(f.read()).hexdigest())

if __name__=="__main__":main()
