#!/usr/bin/env python3
"""Fail-closed static package/CI preflight. Not a Lean kernel proof."""
from __future__ import annotations
import json
from pathlib import Path
import tomllib

ROOT=Path(__file__).resolve().parent
EXTERNAL={'Lean','Std'}
REQUIRED={
 'PhysicalEighteen','EighteenCertified','EighteenDataReceipt',
 'NineteenDataReceipt','NineteenReadData','NineteenSector',
 'PhysicalPolicyCompilerFast','CornerPairDecoder','NineteenSchedule',
 'CornerTurnGenerators','ReachableCornerCoordinates','CornerConservation',
 'ReachableCornerIdentification','CornerPermutation','NineteenCornerTranscript','ObservationTransport','ElevenPrefix','NineteenSymmetry','SymmetryWordTransport'
}


def check():
    config=tomllib.loads((ROOT/'lakefile.toml').read_text())
    names=[obj['name'] for obj in config['lean_lib']]
    default=config['defaultTargets']
    assert len(default)==len(set(default)), 'Duplicate defaultTargets'
    assert len(names)==len(set(names)), 'Duplicate Lean lib declarations'
    assert set(default)==set(names), 'Lean libs must all be default build targets'
    assert REQUIRED <= set(names), 'Missing a primary formal theorem or bridge module'
    for x in names:
        assert (ROOT/f'{x}.lean').is_file(), f'Missing Lean module {x}'
    imports={}
    for name in names:
        path=ROOT/f'{name}.lean'
        imports[name]=[imp for line in path.read_text().splitlines()
                       if line.startswith('import ')
                       for imp in line[7:].split() if imp not in EXTERNAL]
        assert all(dep in names for dep in imports[name]),f'Missing import for {name}'
        if name in ('CornerTurnGenerators','ReachableCornerCoordinates','CornerConservation',
                 'ReachableCornerIdentification','CornerPermutation','NineteenCornerTranscript','ObservationTransport','ElevenPrefix','NineteenSymmetry','SymmetryWordTransport'):
            text=path.read_text()
            assert not any(token in text for token in ('sorry','admit','axiom ')),f'Unjustified placeholder in {name}'
    trace = (ROOT/'NineteenCornerTranscript.lean').read_text()
    for theorem in ('nineteen_schedule_contains_required_corner_pairs',
                    'same_scheduled_colors_implies_fourteen',
                    'same_nineteen_corner_answers_force_all_corner_colors'):
        assert f'theorem {theorem}' in trace, f'Missing nineteen-frame bridge theorem: {theorem}'
        assert f'#print axioms {theorem}' in trace, f'Missing axiom audit: {theorem}'
    transport = (ROOT/'ObservationTransport.lean').read_text()
    for theorem in ('Policy.run_fixed_reply_equiv', 'transport_certified_policy'):
        assert f'theorem {theorem}' in transport, f'Missing transport theorem: {theorem}'
        assert f'#print axioms {theorem}' in transport, f'Missing transport axiom audit: {theorem}'
    assert 'Policy.adapt_fits' in transport and 'Policy.adapt_run' in transport, (
        'Transport must explicitly preserve budget and observation semantics')
    prefix = (ROOT/'ElevenPrefix.lean').read_text()
    for theorem in ('Policy.withPrefix_fits','Policy.withPrefix_run',
                    'first_eleven_address_count',
                    'first_eleven_matches_frozen_corner_schedule',
                    'first_eleven_edge_addresses',
                    'nineteen_budget_of_eight_read_continuations'):
        assert f'theorem {theorem}' in prefix, f'Missing prefix theorem: {theorem}'
        assert f'#print axioms {theorem}' in prefix or (
            f'#print axioms CubeRev029.{theorem}' in prefix), (
            f'Missing kernel-axiom inspection: {theorem}')
    symmetry = (ROOT/'NineteenSymmetry.lean').read_text()
    for theorem in ('symmetry_preserves_edge_type_bijection',
                    'symmetry_even_flip_offset',
                    'symmetry_preserves_oriented_edge_colors'):
        assert f'theorem {theorem}' in symmetry, f'Missing color symmetry result: {theorem}'
        assert f'#print axioms {theorem}' in symmetry, f'Missing axiom audit: {theorem}'
    assert symmetry.count('decide +kernel') >= 3, (
        'All finite symmetry proofs must be kernel-computed, not native_decide')
    word_transport = (ROOT/'SymmetryWordTransport.lean').read_text()
    for theorem in ('relabelEdgeValue_label',
                    'relabelEdgeValue_flip',
                    'relabelEdgeWord_labels',
                    'relabelEdgeWord_flip_formula',
                    'symmetry_preserves_flipBit_for_all_complete_words',
                    'symmetry_relabelEdgeValue_responses'):
        assert f'theorem {theorem}' in word_transport, f'Missing word-transport theorem: {theorem}'
        assert f'#print axioms {theorem}' in word_transport, f'Missing axiom audit: {theorem}'
    for necessary in ('complete.map', 'symmetry_even_flip_offset', 'symmetry_preserves_oriented_edge_colors'):
        assert necessary in word_transport, f'Missing cubie legality or observation bridge: {necessary}'
    visiting=set();visited=set()
    def visit(x):
        if x in visiting:raise ValueError(f'Import cycle at {x}')
        if x in visited:return
        visiting.add(x)
        for y in imports[x]:visit(y)
        visiting.remove(x);visited.add(x)
    for name in names:visit(name)
    workflow=(ROOT.parents[1]/'.github/workflows/cuberev029-lean.yml').read_text()
    assert 'contents: read' in workflow
    assert 'persist-credentials: false' in workflow
    steps=['restore_pinned_data.py','validate_19_corner_schedule.py',
           'audit_corner_turn_generators.py','audit_reachable_corner_bridge.py',
           'lake-package-directory: formal/029']
    assert all(s in workflow for s in steps)
    return {'status':'PASS','lean_modules':len(names),
            'import_edges':sum(map(len,imports.values())),
            'primary_theorems_in_default_build':True,
            'read_only_ci':True,
            'scope':'Static dependency and workflow audit, not Lean compilation'}

if __name__=='__main__':print(json.dumps(check(),indent=2))
