#!/usr/bin/env python3
"""Reproduce the finite transport/corner/physical routing checks (W audit).

This is a computational audit, not a substitute for the outstanding Lean
universal upper-bound theorem. The original policy certificate is immutable.
"""
import argparse
import hashlib
import json
from pathlib import Path

from verify_19_policy_certificate import verify
from audit_r029_w_transport_all_prefixes import audit_transport, audit_corners
from audit_r029_w_corner_geometric_decoder import check as geometric_corners
from audit_r029_w_joint_routes import test as joint_routes
from audit_r029_w_negative_controls import run as negative_controls
from audit_r029_w_turn_invariants import run as turn_invariants
from audit_r029_w_worked_route import run as worked_replay

POLICY_SHA = '80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227'


def run(path):
    policy = Path(path)
    digest = hashlib.sha256(policy.read_bytes()).hexdigest()
    if digest != POLICY_SHA:
        raise ValueError(f'Unexpected policy bytes: {digest}')
    policy_receipt = verify(policy)
    assert policy_receipt['policy_nodes'] == 141097
    assert policy_receipt['candidate_assignments'] == 144736
    movement = audit_transport()
    assert movement['supported_first_color_count_vectors'] == 1362
    assert movement['transformed_candidate_records'] == 3215616
    corner = audit_corners()
    geom = geometric_corners()
    routes = joint_routes()
    negative = negative_controls()
    generators = turn_invariants()
    here=Path(__file__).resolve().parent
    try:
        worked_replay(here/'worked-physical-replay.json')
    except AssertionError as exc:
        if str(exc) != 'The example corner replies contradict twist legality.':
            raise
        original_rejected = True
    else:
        raise AssertionError('Original inconsistent V worked example was accepted')
    corrected = worked_replay(here/'worked-physical-replay-corrected.json')
    assert original_rejected and corrected['explicit_corner_schedule_checked']
    assert all(receipt.get('status') == 'PASS' for receipt in
               (policy_receipt, geom, routes, negative))
    return {'status':'PASS', 'certificate_sha256':digest,
            'policy_nodes': policy_receipt['policy_nodes'],
            'representatives':policy_receipt['representatives'],
            'candidate_assignments_representatives':policy_receipt['candidate_assignments'],
            'transport':movement,
            'corner_pair_decoder':corner,
            'physical_corner_regression':geom,
            'paired_physical_routes':routes,
            'negative_controls':negative,
            'generator_legality':{key:value for key,value in generators.items() if key!='generator_table'},
            'original_V_example_rejected':original_rejected,
            'corrected_W_example':corrected,
            'trust_scope':'independent finite audits; geometric 18 lower bound separately Lean-proven; universal 19 upper-bound Lean theorem remains open'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    receipt=run(args.certificate)
    content=json.dumps(receipt,indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.write_text(content)
    print(content)
