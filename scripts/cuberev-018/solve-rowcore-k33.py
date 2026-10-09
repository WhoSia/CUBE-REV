#!/usr/bin/env python3
"""CUBE-REV 0.18: exact k=33 SAT/DRUP on the logically equivalent 398-row core.

The certificate of equivalence is independently verified against the full
original 1192 x 1323 *physical Rubik* incidence. The solver sees exactly
398 coverage clauses + <=33 cardinality and NO P6-based dual cuts.
An UNSAT claim is not accepted without a separate proof checker.
"""
import argparse
import hashlib
import json
from pathlib import Path
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose4

p = argparse.ArgumentParser()
p.add_argument('--physical',required=True)
p.add_argument('--core',required=True)
p.add_argument('--output',required=True)
p.add_argument('--conflicts',type=int,default=2500000)
a=p.parse_args()
physical_path=Path(a.physical)
raw=physical_path.read_bytes()
data=json.loads(raw)
core=json.loads(Path(a.core).read_text())
assert data["counts"]=={
    "literal":104976,"partitions":1913,
    "coverageTypes":1477,"maximal":1323,"bases":1192
}
assert core["schema"]=="cube-rev.018.row-implication-all-k-v1"
assert core["physical_input_sha256"]==hashlib.sha256(raw).hexdigest()
assert core["original_constraints"]==1192
assert core["original_words"]==1323
assert core["retained_constraints"]==398
rows=list(map(int,core["retained_row_indices"]))
witness=list(map(int,core["removed_row_implication_witnesses"]))
assert len(set(rows))==398 and len(witness)==1192
masks=[int(c["mask"],16) for c in data["candidates"]]
support=[0]*1192
for j,mask in enumerate(masks):
    assert mask>>1192==0
    while mask:
        b=mask&-mask
        support[b.bit_length()-1]|=1<<j
        mask^=b
for i,r in enumerate(witness):
    assert r in rows
    assert (support[r]&~support[i])==0,("Bad row implication",i,r)
for i in rows:
    for j in rows:
        if i!=j:
            assert (support[j]&~support[i])!=0,("Core not minimal",i,j)
cnf=CNF()
for index in rows:
    clause=[j+1 for j in range(1323) if support[index]>>j&1]
    assert clause
    cnf.append(clause)
pool=IDPool(start_from=1324)
cnf.extend(CardEnc.atmost(lits=list(range(1,1324)),
                           bound=33,encoding=EncType.seqcounter,
                           vpool=pool).clauses)
output=Path(a.output)
output.mkdir(parents=True,exist_ok=True)
cnffile=output/'cube_original_398row_k33.cnf'
cnf.to_file(str(cnffile))
result={
    "name":"CUBE_REV_018_PHYSICAL_CORE398_K33",
    "state":"UNSOLVED",
    "k":33,
    "physical_instance_sha256":hashlib.sha256(raw).hexdigest(),
    "row_certificate_sha256":hashlib.sha256(Path(a.core).read_bytes()).hexdigest(),
    "cnf_sha256":hashlib.sha256(cnffile.read_bytes()).hexdigest(),
    "full_constraints":1192,
    "equivalent_core_constraints":398,
    "original_cover_decision_variables":1323,
    "cnf_nvars":cnf.nv,
    "cnf_nclauses":len(cnf.clauses),
    "conflict_budget":a.conflicts,
    "certification":("UNSAT result requires external DRUP checker and "
                     "full physical source-to-CNF correspondence; "
                     "SAT witness requires actual Rubik action replay.")
}
print("CUBE_REV_018_EQUIVALENT_CORE_K33_CNF",
      json.dumps(result,sort_keys=True),flush=True)
with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as solver:
    solver.conf_budget(a.conflicts)
    ans=solver.solve_limited(expect_interrupt=False)
    if ans is False:
        lines=solver.get_proof()
        assert lines and lines[-1].strip()=='0'
        trace=output/'cube_original_398row_k33.drup'
        trace.write_text('\n'.join(lines)+'\n')
        result["state"]="UNSAT_EXTERNAL_CHECK_PENDING"
        result["proof_lines"]=len(lines)
        result["proof_sha256"]=hashlib.sha256(trace.read_bytes()).hexdigest()
        print("CUBE_REV_018_CORE398_K33_UNSAT_PROOF_EMITTED",
              len(lines),flush=True)
    elif ans is True:
        values=set(solver.get_model())
        chosen=[j for j in range(1323) if j+1 in values]
        assert len(chosen)<=33
        coverage=0
        for j in chosen:
            coverage |= int(data["candidates"][j]["mask"],16)
        assert coverage.bit_count()==1192
        words=[data["candidates"][j]["word"] for j in chosen]
        (output/'sat_witness.json').write_text(json.dumps(
            {"schema":"cube-rev.018.core398-k33-candidate-v1",
             "words":words,"indices":chosen,"k":len(chosen)},indent=2)+'\n')
        result["state"]="SAT_FULL1192_BITSET_VALID_ACTION_REPLAY_PENDING"
        result["witness_count"]=len(chosen)
        print("CUBE_REV_018_CORE398_K33_SAT_CUBE_REPLAY_PENDING",
              len(chosen),flush=True)
    else:
        result["state"]="UNKNOWN_CONFLICT_BUDGET"
        print("CUBE_REV_018_CORE398_K33_UNKNOWN",a.conflicts,flush=True)
(output/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
