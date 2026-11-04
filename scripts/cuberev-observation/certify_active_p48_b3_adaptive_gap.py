#!/usr/bin/env python3
"""Proof-carrying P48 B3 adaptive FOUR versus nonadaptive SIX-frame separation.

Generates and independently replays an explicit 4-level adaptive query
decision tree for all 3502 legal B3 states. Verifies every node branch from
raw P48 cube outputs at two stationary complete identity/orientation probes.
Also reruns exhaustive impossibility of depth-3 adaptive policies and 5-frame
nonadaptive fixed-site choices, plus an explicit valid 6-frame placement.

The source P48 engine does not import historical 54-facelet B3 or B6 oracles.
Bounded searches return UNKNOWN, never INVALID/PASS by exhaustion.
"""
import argparse
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
from collections import defaultdict, Counter
from b6_independent_48sticker_goals import EDGE_POS,CORNERS,word
from audit_active_p48_small_ball_decision_trees import ball, observations
from explore_active_p48_b3_horizons import (
    adaptive_policy_optimized,nonadaptive_five,nonadaptive_six
)
from active_p48_fixed_site_scan import joint_position_words,REF_EDGE,REF_CORNER
from active_p48_b6_ten_frame_bridge import measured_inverse_factor

QUERIES=tuple((e,c) for e in range(12) for c in range(8))
QUERY_INDEX={q:i for i,q in enumerate(QUERIES)}

def tree_from_search(subset,certificate,rows):
    if len(subset)==1:
        return {"leaf":subset[0]}
    if not certificate:
        raise AssertionError("missing adaptive certificate")
    if len(certificate)==1:
        qi=certificate[0]
        part=defaultdict(list)
        for i in subset:part[rows[qi][i]].append(i)
        if any(len(g)!=1 for g in part.values()):
            raise AssertionError("noninjective final query")
        return {"query":list(QUERIES[qi]),
                "branches":{str(k):{"leaf":v[0]} for k,v in sorted(part.items())}}
    qi,proof=certificate
    parts=defaultdict(list)
    for i in subset:parts[rows[qi][i]].append(i)
    branches={}
    for members,subcert in proof:
        if not members:raise AssertionError("empty branch")
        value=rows[qi][members[0]]
        if tuple(parts[value])!=tuple(members):
            raise AssertionError("branch members disagree with actual query")
        if str(value) in branches:
            raise AssertionError("duplicate branch")
        branches[str(value)]=tree_from_search(tuple(members),subcert,rows)
    if set(branches)!={str(k) for k in parts}:
        raise AssertionError("uncovered branch")
    return {"query":list(QUERIES[qi]),"branches":branches}

def payload():
    states,_=ball(3)
    factors,queries,rows=observations(states)
    assert len(states)==3502 and queries==QUERIES
    lower,nodes,_cache,_=adaptive_policy_optimized(rows,3,20000)
    if lower!="EXCLUDED":raise AssertionError("adaptive B3 depth-three negative gate not complete")
    upper,search_nodes,_cache,cert=adaptive_policy_optimized(rows,4,20000)
    if upper!="FOUND":raise AssertionError("adaptive B3 depth-four positive gate not complete")
    non5,count=nonadaptive_five(factors)
    if non5 is not None or count!=44352:
        raise AssertionError("nonadaptive B3 five-frame negative gate not complete")
    six,count=nonadaptive_six(factors)
    if six is None:raise AssertionError("nonadaptive B3 six-frame positive gate missing")
    tree=tree_from_search(tuple(range(len(states))),cert,rows)
    return {
      "schema_version":1,
      "radius":3,
      "states":len(states),
      "states_sha256":sha256(b"".join(states)).hexdigest(),
      "sensor_channel":"one full-label+orientation edge-slot and one corner-slot probe, known turns",
      "adaptive_frames":4,
      "adaptive_three_exact_exclusion_belief_nodes":nodes,
      "adaptive_four_search_belief_nodes":search_nodes,
      "adaptive_tree":tree,
      "nonadaptive_frames":6,
      "nonadaptive_five_candidate_count":count if False else 44352,
      "nonadaptive_six": {"edges":list(six[0]),"corners":list(six[1])},
      "limitations":"B6 adaptive horizon and minimum HTM action cost open; RGB readout different"
    }

def verify(p):
    if p.get("schema_version")!=1 or p.get("radius")!=3 or p.get("states")!=3502:
        raise AssertionError("bad B3 proof schema")
    states,_=ball(3)
    if p["states_sha256"]!=sha256(b"".join(states)).hexdigest():
        raise AssertionError("wrong physical state universe")
    factors,queries,rows=observations(states)
    assert queries==QUERIES
    depth_hist=Counter()
    def validate(node,subset,remaining,used):
        if "leaf" in node:
            if len(subset)!=1 or node["leaf"]!=subset[0]:
                raise AssertionError("wrong adaptive state identity")
            depth_hist[used]+=1
            return
        if remaining<=0:raise AssertionError("tree exceeds four observations")
        q=tuple(node.get("query",()))
        if q not in QUERY_INDEX:raise AssertionError("nonphysical query position")
        qi=QUERY_INDEX[q]
        groups=defaultdict(list)
        for idx in subset:groups[rows[qi][idx]].append(idx)
        children=node.get("branches")
        if not isinstance(children,dict) or set(children)!={str(k) for k in groups}:
            raise AssertionError("missing/forged branch")
        for value,subset2 in groups.items():
            validate(children[str(value)],tuple(subset2),remaining-1,used+1)
    validate(p["adaptive_tree"],tuple(range(len(states))),4,0)
    if sum(depth_hist.values())!=3502 or max(depth_hist)>4:
        raise AssertionError("adaptive exact tree incomplete")
    joint_words=joint_position_words()
    frames={}
    for i,state in enumerate(states):
        node=p["adaptive_tree"]
        count=0
        while "leaf" not in node:
            e,c=node["query"];q=(e,c)
            if q not in frames:
                frames[q]=word(" ".join(joint_words[(EDGE_POS[e],CORNERS[c])]))
            frame=frames[q]
            read_edge=measured_inverse_factor(state,EDGE_POS[e],frame,REF_EDGE)
            read_corner=measured_inverse_factor(state,CORNERS[c],frame,REF_CORNER)
            value=str(read_edge*24+read_corner)
            node=node["branches"][value]
            count+=1
        if count>4 or node["leaf"]!=i:
            raise AssertionError("actual fixed physical site measurements not identified")
    # Recompute lower-bound decisions, never trust a status flag in JSON.
    negative,count,_cache,_=adaptive_policy_optimized(rows,3,20000)
    if negative!="EXCLUDED":
        raise AssertionError("not all adaptive three-step policy trees refuted")
    if nonadaptive_five(factors)!=(None,44352):
        raise AssertionError("nonadaptive five-frame enumeration incomplete")
    non6=p["nonadaptive_six"];E=non6["edges"];C=non6["corners"]
    if len(E)!=len(set(E)) or len(E)!=6 or len(C)!=len(set(C)) or len(C)!=6:
        raise AssertionError("invalid six-frame witness")
    if not set(E)<=set(range(12)) or not set(C)<=set(range(8)):
        raise AssertionError("nonphysical six-frame sites")
    indices=E+[12+c for c in C]
    if len({tuple(f[k] for k in indices) for f in factors})!=3502:
        raise AssertionError("six-frame nonadaptive certificate not injective")
    print("ACTIVE_B3_ADAPTIVE_FOUR_FRAME_FULL_P48_TREE_PASS",dict(depth_hist))
    print("ACTIVE_B3_ADAPTIVE_THREE_FRAME_EXHAUSTIVE_EXCLUSION_PASS",count,"belief nodes")
    print("ACTIVE_B3_NONADAPTIVE_FIVE_FRAME_ALL_44352_EXCLUDED")
    print("ACTIVE_B3_NONADAPTIVE_SIX_FRAME_INJECTIVE_CONSTRUCTION_PASS")
    print("BOUNDARY independent P48 B3, ideal identity+orientation, B6 adaptive still open")
    return depth_hist

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--emit")
    parser.add_argument("--verify")
    o=parser.parse_args()
    data=json.loads(Path(o.verify).read_text(encoding="utf8")) if o.verify else payload()
    verify(data)
    if o.emit:
        output=Path(o.emit)
        output.write_text(json.dumps(data,sort_keys=True,separators=(",",":"))+"\n",encoding="utf8")
        print("ACTIVE_B3_CERT_SHA256",sha256(output.read_bytes()).hexdigest())
        print("ACTIVE_B3_CERT_BYTES",output.stat().st_size)
if __name__=="__main__":main()
