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
 'CornerTurnGenerators','ReachableCornerCoordinates'
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
        if name in ('CornerTurnGenerators','ReachableCornerCoordinates'):
            text=path.read_text()
            assert not any(token in text for token in ('sorry','admit','axiom ')),f'Unjustified placeholder in {name}'
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
