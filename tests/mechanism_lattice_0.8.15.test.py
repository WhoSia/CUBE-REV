#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import importlib.util
import json
import tempfile
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD_PATH=ROOT/'analysis/cognitive_mechanism_lattice_0_8_15.py'
spec=importlib.util.spec_from_file_location('cr0815_lattice',MOD_PATH)
mod=importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

BANK=ROOT/'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json'
CONFIG=ROOT/'cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json'

def digest_tree(path: Path):
    return {p.relative_to(path).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.rglob('*')) if p.is_file()}

with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
    da,db=Path(a),Path(b)
    ra=mod.run(BANK,CONFIG,da,120,8152026)
    rb=mod.run(BANK,CONFIG,db,120,8152026)
    assert digest_tree(da)==digest_tree(db), 'NONDETERMINISTIC_OUTPUT'

    assert ra['stimulus_count']==28
    assert ra['schedule_count']==24
    assert ra['orbit_audit']['orbit_count']==27
    assert ra['orbit_audit']['repeated_orbit_count']==1
    assert ra['orbit_audit']['repeated_orbits']==[['CR086-S002','CR086-S003']]
    assert ra['horizon_audit']['h1_vs_h3_disjoint']==13
    assert ra['horizon_audit']['h1_vs_h2_different']==23
    assert ra['horizon_audit']['all_same']==3

    pairs=ra['predeclared_pair_results']
    assert pairs['h1_vs_h3']['balanced_accuracy_mean']>=0.95
    assert pairs['stationary_h1_vs_switch']['balanced_accuracy_mean']>=0.95
    assert 0.35<=pairs['open_vs_closed_loop']['balanced_accuracy_mean']<=0.65
    assert 0.35<=pairs['high_vs_low_capacity_same_policy']['balanced_accuracy_mean']<=0.65
    assert pairs['open_vs_closed_loop']['classification']=='NON_IDENTIFIABLE'
    assert pairs['high_vs_low_capacity_same_policy']['classification']=='NON_IDENTIFIABLE'

    assert ra['orientation_pair_audit']['pair_count']==1
    pair=ra['orientation_pair_audit']['pairs'][0]
    assert pair['rotation_mapping_count']==1
    assert pair['a_before_b_count']==18 and pair['b_before_a_count']==6
    assert pair['min_separation']==7 and pair['max_separation']==21

    bal=ra['schedule_balance_audit']
    assert bal['mean_second_minus_first']==0.0
    assert bal['max_absolute_difference']<=0.0714

    conclusions=ra['instrument_conclusions']
    assert conclusions['planning_horizon']=='IDENTIFIABLE'
    assert conclusions['strategy_transition']=='IDENTIFIABLE'
    assert conclusions['open_vs_closed_loop']=='NON_IDENTIFIABLE'
    assert conclusions['visuospatial_capacity_trait']=='NON_IDENTIFIABLE'
    assert conclusions['orientation_equivariance']=='PARTIAL_SINGLE_ROTATIONAL_PAIR'
    assert conclusions['chunk_boundary_cost']=='NOT_IDENTIFIABLE_SINGLE_ACTION_TRIALS'
    assert conclusions['recovery_monitoring']=='NOT_IDENTIFIABLE_NO_POST_ERROR_TRAJECTORY'

    registry=json.loads((da/'CUBE_REV_0.8.15_MECHANISM_AXIS_REGISTRY.json').read_text())
    assert registry['epistemic_rule']=='BEHAVIORAL_SIGNATURE_FIRST_PSYCHOLOGICAL_LABEL_SECOND'
    assert registry['measurement_rule']=='NO_TRIALWISE_SELF_REPORT_ADDED_IN_0_8_15'
    assert len(registry['axes'])>=8
    assert len(registry['forbidden_claims'])>=5
    assert all(
        'falsifier' in x or
        'required_extension' in x or
        'measurement_hazard' in x or
        x['status'].startswith('NOT_IDENTIFIABLE')
        for x in registry['axes']
    )

print('CR0815_MECHANISM_LATTICE_TEST_PASS deterministic=true positive_controls=2 negative_controls=2 stimuli=28 schedules=24')
