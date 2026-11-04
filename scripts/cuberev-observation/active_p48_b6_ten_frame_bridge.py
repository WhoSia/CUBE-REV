#!/usr/bin/env python3
"""Exact finite-radius fixed-SLOT sensing bridge, source P48.

Original-cubie sensors in inverse(g) correspond bijectively to complete
fixed-slot occupant observations in g. For B6 this yields an exact TEN-frame
NONADAPTIVE two-stationary-slot scan; it does not certify the minimum over
ADAPTIVE observation decision trees. No historical 54-facelet engine used.
"""
from itertools import product
from b6_independent_48sticker_goals import (
    CORNERS, EDGE_POS, EDGE_NAMES, EDGE_POSITION, PIECES, SLOTS,
    compose, inverse, word, factor_value, valid_pairs
)
from active_p48_fixed_site_scan import (
    joint_position_words, REF_EDGE, REF_CORNER, observe,
)

def endpoints(edge):
    mid=EDGE_POSITION[edge]
    return frozenset(p for p in CORNERS
                     if all(p[i]==mid[i] for i in range(3) if mid[i]))

def ten_frame_b6_plan():
    """Make exactly ten readouts, visiting ten edge and six corner *slots*."""
    h="DL"
    absent_edges=min(valid_pairs(h),key=lambda p:tuple(sorted(p)))
    absent_edge_positions={EDGE_POSITION[e] for e in absent_edges}
    retained_edges=tuple(p for p in EDGE_POS if p not in absent_edge_positions)
    retained_corners=tuple(p for p in CORNERS if p not in endpoints(h))
    assert len(retained_edges)==10 and len(retained_corners)==6
    actions=joint_position_words()
    plan=[(edge,retained_corners[i%6],
           actions[(edge,retained_corners[i%6])])
          for i,edge in enumerate(retained_edges)]
    sampled={site for edge,corner,turns in plan for site in (edge,corner)}
    assert len(plan)==10 and len(sampled)==16
    assert sampled==set(retained_edges+retained_corners)
    return plan,sampled,absent_edges

def measured_inverse_factor(original_state,initial_slot,frame,probe):
    """Reconstruct factor of inverse(original_state) from actual slot output.

    One fixed-site probe reports the label and oriented sticker destination
    slots of its present occupant; remove the known frame turn to recover
    the same initial-slot observation.
    """
    physical=compose(frame,original_state)
    label,sticker_slots=observe(physical,probe)
    revert=inverse(frame)
    before=tuple(revert[j] for j in sticker_slots)
    if {SLOTS[j][0] for j in before}!={initial_slot}:
        raise AssertionError("the probe did not interrogate requested initial site")
    identity_slots=PIECES[label]
    origin_sites=PIECES[initial_slot]
    back_image=tuple(identity_slots[before.index(site)] for site in origin_sites)
    width=len(origin_sites)
    destination_slots=PIECES[label]
    rotation=destination_slots.index(back_image[0])
    if any(back_image[i]!=destination_slots[(i+rotation)%width]
           for i in range(width)):
        raise AssertionError("invalid oriented inverse original cubie")
    kind=EDGE_POS if width==2 else CORNERS
    return kind.index(label)*width+rotation

def scan_inverse_factor_signature(state,plan):
    """Ten frame readings interpreted as original-labelled inverse factors."""
    result={}
    for edge,corner,turns in plan:
        frame=word(" ".join(turns))
        for initial_slot,probe in ((edge,REF_EDGE),(corner,REF_CORNER)):
            sensed=measured_inverse_factor(state,initial_slot,frame,probe)
            if initial_slot in result and result[initial_slot]!=sensed:
                raise AssertionError("inconsistent repeated slot measurement")
            result[initial_slot]=sensed
    return result

def audit():
    plan,selected,missing=ten_frame_b6_plan()
    samples=["","U","R F2 U' D L B2","F R F2 D2 B2",
             "U2 R' B D2 B' R U2 R' B D2 B' R",
             "L F R' F' L' U2 R U R U' R2 U2 R"]
    for w in samples:
        state=word(w)
        recorded=scan_inverse_factor_signature(state,plan)
        true_inverse=inverse(state)
        assert set(recorded)==selected
        expected={p:factor_value(p,true_inverse) for p in selected}
        assert recorded==expected,(w,recorded,expected)
    print("ACTIVE_B6_P48_TEN_FRAME_FIXED_SLOT_INVERSE_FACTOR_PASS")
    print("ACTIVE_B6_P48_SELECT 10 edge positions + 6 corner positions")
    print("ACTIVE_B6_P48_NONADAPTIVE_HORIZON_EXACT_10 (with 41-class P48 B6 base certificate)")
    print("BOUNDARY: ADAPTIVE B6 horizon lower bound remains OPEN")
    print("BOUNDARY: 11-frame full-group adaptive lower bound remains separately valid")
    return plan,selected

if __name__=="__main__":
    audit()
