#!/usr/bin/env python3
"""Emit 41 physical HTM targets and exact cubie-action tables from the original archive.

Usage (from scripts/cuberev-observation):
 python emit_b6_41_mitm_inputs.py HISTORICAL_B1_B5.zip OUTPUT_DIRECTORY

Requires existing make_b6_factor_table.py, build_b6_stabilizer_goals.py
and audit_b6_full48_target_orbits.py. No previous B6-positive verdict
or selected-sensor projected state set is read.
"""
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path
from audit_b6_full48_target_orbits import main as physical_orbits

ARCHIVE_SHA="002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94"
CLASS_SHA="c3dbf41177e16d8d0cb0cd76b433304e14f9cdac4a14f205d6231dc9dd8abc1e"
TARGETS_SHA="6395e34efe736eecb1bfab8fa9cc713d2378e721ab79f009ec54d37ff69cb340"

def emit(archive,output_dir):
    archive=Path(archive).resolve()
    output=Path(output_dir).resolve()
    output.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==ARCHIVE_SHA

    # Recompute goal symmetries from actual original 54-facelet configurations.
    classes=physical_orbits(str(archive))
    minima=sorted(min(group) for group in classes.values())
    assert len(minima)==41
    assert hashlib.sha256(b"".join(minima)).hexdigest()==CLASS_SHA

    with zipfile.ZipFile(archive) as z:
        cube={"__name__":"archive_cube","__file__":"independent_b4.py"}
        exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),cube)

    # Exact corner factor identifiers: same deterministic order as the
    # existing make_b6_factor_table.py generator.
    solved=cube["START"]
    front=[solved];visited={solved};states=[solved]
    for depth in range(1,4):
        nextfront=[]
        for state in front:
            for action in range(18):
                child=cube["turn"](state,action)
                if child not in visited:
                    visited.add(child)
                    nextfront.append(child)
        states.extend(nextfront)
        front=nextfront
    assert len(states)==3502
    corner_keys=[{} for _ in range(8)]
    for state in states:
        corners=cube["cv"](state)
        for i in range(8):
            corner_keys[i].setdefault(corners[4*i:4*i+4],len(corner_keys[i]))
    assert all(len(keys)==24 for keys in corner_keys)

    lines=["# SHA256 canonical 54-facelet class minima "+CLASS_SHA]
    for i,state in enumerate(minima):
        corners=cube["cv"](state)
        factors=list(cube["ev"](state))+[
            corner_keys[j][corners[4*j:4*j+4]] for j in range(8)]
        assert len(factors)==20 and all(0<=v<24 for v in factors)
        lines.append(str(i)+" "+" ".join(map(str,factors)))
    manifest=output/"targets41.txt"
    manifest.write_text("\n".join(lines)+"\n",encoding="utf-8")
    assert hashlib.sha256(manifest.read_bytes()).hexdigest()==TARGETS_SHA
    print("PASS canonical 41-goal input digest:",TARGETS_SHA)

    maker=Path(__file__).with_name("make_b6_factor_table.py")
    subprocess.run([sys.executable,str(maker),str(archive)],cwd=output,check=True)
    assert (output/"b6_factor_table.hpp").is_file()
    print("PASS physical factor table + 41-goal manifest")
    return manifest

if __name__=="__main__":
    if len(sys.argv)!=3:
        raise SystemExit("Usage: emit_b6_41_mitm_inputs.py HISTORICAL.zip OUTPUT_DIRECTORY")
    emit(sys.argv[1],sys.argv[2])
