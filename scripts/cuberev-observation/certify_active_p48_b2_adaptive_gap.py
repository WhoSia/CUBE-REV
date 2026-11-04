#!/usr/bin/env python3
"""Proof-carrying B2 adaptive-vs-nonadaptive fixed-site observation gap.

B2 is all 262 states in the independent P48 18-HTM ball. Two stationary
ideal full-identity/full-orientation probes interrogate one edge site and
one corner site per frame; all 96 site pairs are physically addressable.

The generated certificate includes a complete two-frame ADAPTIVE decision
tree, a collision pair for every 1848 nonadaptive two-frame joint
site selections, and one valid three-frame nonadaptive placement.
Each row is checked against independently regenerated P48 observations.
No transfer of the B2 decision-tree gap to B6 is claimed.
"""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
from audit_active_p48_small_ball_decision_trees import (
    ball, observations, nonadaptive_witness,
)
from active_p48_fixed_site_scan import joint_position_words, REF_EDGE, REF_CORNER
from active_p48_b6_ten_frame_bridge import measured_inverse_factor
from b6_independent_48sticker_goals import word, EDGE_POS, CORNERS

QUERY_PAIRS=tuple((e,c) for e in range(12) for c in range(8))
assert len(QUERY_PAIRS)==96

def payload():
    states,_=ball(2)
    factors,queries,rows=observations(states)
    assert len(states)==262 and queries==QUERY_PAIRS
    root_id=None; policy=None; roots=None
    for qid,root_row in enumerate(rows):
        groups=defaultdict(list)
        for i,value in enumerate(root_row):
            groups[value].append(i)
        choices={}
        for value,members in groups.items():
            decision=next((j for j,row in enumerate(rows)
                           if len({row[i] for i in members})==len(members)),None)
            if decision is None:break
            choices[str(value)]=list(QUERY_PAIRS[decision])
        if len(choices)==len(groups):
            root_id=qid;policy=choices;roots=groups
            break
    if root_id is None:raise AssertionError("adaptive B2 depth two does not exist")
    collisions=[]
    for ea,eb in combinations(range(12),2):
        for ca,cb in combinations(range(8),2):
            seen={}
            found=None
            for i,values in enumerate(factors):
                sig=(values[ea],values[eb],values[12+ca],values[12+cb])
                if sig in seen:
                    found=(seen[sig],i);break
                seen[sig]=i
            if found is None:
                raise AssertionError("a nonadaptive B2 depth-two base exists")
            collisions.append([ea,eb,ca,cb,*found])
    assert len(collisions)==66*28==1848
    upper=nonadaptive_witness(factors,3)
    if upper is None:raise AssertionError("three-frame nonadaptive upper missing")
    return {
        "schema_version":1,
        "radius":2,
        "states":262,
        "state_order":"lexicographically sorted P48 original-to-slot permutation bytes",
        "state_sha256":sha256(b"".join(states)).hexdigest(),
        "query_model":"fixed edge and corner slots; full incoming cubie identity+orientation",
        "root_pair":list(QUERY_PAIRS[root_id]),
        "second_pair_by_first_observation":policy,
        "nonadaptive_two_frame_collision_rows":collisions,
        "nonadaptive_three_frame_site_sets":{
            "edge_indices":list(upper[0]),"corner_indices":list(upper[1])
        },
        "claim":"B2 adaptive=2, nonadaptive=3",
        "scope_limit":"B6 adaptive remains open; no HTM movement-cost optimum claimed"
    }

def verify(p):
    if not isinstance(p,dict) or p.get("schema_version")!=1 or p.get("radius")!=2:
        raise ValueError("wrong certificate schema or state ball")
    states,_=ball(2)
    if p.get("states")!=262 or p.get("state_sha256")!=sha256(b"".join(states)).hexdigest():
        raise AssertionError("P48 state identity/seal mismatch")
    factors,queries,rows=observations(states)
    root=tuple(p["root_pair"])
    if root not in QUERY_PAIRS:raise AssertionError("bad root site pair")
    decisions=p["second_pair_by_first_observation"]
    if not isinstance(decisions,dict):raise AssertionError("missing branch policy")
    query_id={q:i for i,q in enumerate(QUERY_PAIRS)}
    root_row=rows[query_id[root]]
    outcomes=set()
    observed_first=set()
    joint_words=joint_position_words()
    for i,state in enumerate(states):
        first=root_row[i]
        observed_first.add(str(first))
        if str(first) not in decisions:raise AssertionError("missing policy branch")
        second=tuple(decisions[str(first)])
        if second not in query_id:raise AssertionError("nonphysical second pair")
        second_value=rows[query_id[second]][i]
        history=(first,second_value)
        if history in outcomes:raise AssertionError("non-injective adaptive history")
        outcomes.add(history)
        # Independent source of the same ideal sensor outputs: actually replay
        # the absolute physical turn words and read fixed probe sticker slots.
        for pair,expected in ((root,first),(second,second_value)):
            edge,corner=pair
            frame=word(" ".join(joint_words[(EDGE_POS[edge],CORNERS[corner])]))
            got_edge=measured_inverse_factor(state,EDGE_POS[edge],frame,REF_EDGE)
            got_corner=measured_inverse_factor(state,CORNERS[corner],frame,REF_CORNER)
            if got_edge*24+got_corner!=expected:
                raise AssertionError("actual P48 fixed-slot probe disagrees with inverse factor")
    if len(outcomes)!=262 or set(decisions)!=observed_first:
        raise AssertionError("adaptive certificate incomplete or surplus branches")
    # Exhaust all 96 one-frame readings (adaptive depth one is nonadaptive).
    if any(len(set(row))==262 for row in rows):
        raise AssertionError("one-frame query unexpectedly injective")
    negative=p["nonadaptive_two_frame_collision_rows"]
    choices={(a,b,c,d) for a,b in combinations(range(12),2)
                        for c,d in combinations(range(8),2)}
    if len(negative)!=len(choices):raise AssertionError("not 1848 negative rows")
    checked=set()
    for row in negative:
        if not isinstance(row,list) or len(row)!=6:
            raise AssertionError("bad collision witness format")
        ea,eb,ca,cb,x,y=row
        key=(ea,eb,ca,cb)
        if key not in choices or key in checked:
            raise AssertionError("missing/duplicate query pair")
        checked.add(key)
        if not isinstance(x,int) or not isinstance(y,int) or not(0<=x<y<262):
            raise AssertionError("bad state indices for collision")
        a,b=factors[x],factors[y]
        if (a[ea],a[eb],a[12+ca],a[12+cb])!=(
            b[ea],b[eb],b[12+ca],b[12+cb]):
            raise AssertionError("fabricated nonadaptive collision")
    if checked!=choices:raise AssertionError("uncovered nonadaptive query")
    upper=p["nonadaptive_three_frame_site_sets"]
    edges=upper["edge_indices"];corners=upper["corner_indices"]
    if (len(edges),len(set(edges)),len(corners),len(set(corners)))!=(3,3,3,3):
        raise AssertionError("invalid nonadaptive upper placement")
    if not set(edges)<=set(range(12)) or not set(corners)<=set(range(8)):
        raise AssertionError("invalid query positions")
    positions=edges+[12+i for i in corners]
    if len({tuple(f[j] for j in positions) for f in factors})!=262:
        raise AssertionError("three-frame upper not injective")
    print("ACTIVE_B2_ADAPTIVE_TWO_FRAME_DECISION_TREE_PASS",len(decisions),"branches",len(outcomes),"states")
    print("ACTIVE_B2_NONADAPTIVE_TWO_FRAME_ALL_1848_COLLISIONS_PASS")
    print("ACTIVE_B2_NONADAPTIVE_THREE_FRAME_CONSTRUCTION_PASS")
    print("ACTIVE_B2_SINGLE_FRAME_ALL_96_NONINJECTIVE_PASS")
    print("BOUNDARY requires full ideal labelled orientation, action cost not optimized, B6 adaptive open")
    return len(decisions)

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--emit")
    parser.add_argument("--verify")
    opts=parser.parse_args()
    if opts.verify:
        item=json.loads(Path(opts.verify).read_text(encoding="utf8"))
    else:item=payload()
    verify(item)
    if opts.emit:
        Path(opts.emit).write_text(json.dumps(item,indent=2,sort_keys=True)+"\n",encoding="utf8")
        print("ACTIVE_B2_PROOF_CERT_SHA256",sha256(Path(opts.emit).read_bytes()).hexdigest())

if __name__=="__main__":main()
