#!/usr/bin/env python3
"""Adversarial noncube 12-edge transport: same F/B flips and face support, altered R cycle.
This is a falsifier of universal 16+16 claims based solely on flip support and cyclicity,
NOT an alternative physically legal 3x3 Rubik move oracle.
Use the emitted alternate maps with the C++ rank7 and full partition-census programs.
"""
import argparse
import hashlib
import json
from pathlib import Path

SHA="9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1"
R_SLOTS=(0,4,8,11)
CYCLE=(0,4,8,11) # NONPHYSICAL: original R cycle is (0 11 4 8).

def main(args):
    assert hashlib.sha256(args.source.read_bytes()).hexdigest()==SHA
    maps=[[int(x) for x in line.split()] for line in args.maps.read_text().splitlines()]
    assert len(maps)==18 and all(sorted(row)==list(range(24)) for row in maps)
    assert {p:maps[3][p*2]//2 for p in R_SLOTS}=={0:11,11:4,4:8,8:0}
    new=[list(row) for row in maps]
    for j,p in enumerate(CYCLE):
        for move,power in ((3,1),(4,3),(5,2)):
            dest=CYCLE[(j+power)%4]
            for bit in (0,1):new[move][2*p+bit]=2*dest+bit
    assert all(sorted(row)==list(range(24)) for row in new)
    assert all(maps[a]==new[a] for a in range(18) if a not in (3,4,5))
    assert all((maps[a][2*p]&1)==(new[a][2*p]&1)
               for a in range(18) for p in range(12))
    assert maps[5][2*0]//2 in (0,2,4,6) # physical equator preserved
    assert new[5][2*0]//2 not in (0,2,4,6) # mutated R2 leaks into rim
    args.output.write_text("\n".join(" ".join(map(str,row)) for row in new)+"\n")
    print(json.dumps({
        "result":"NONCUBE_R_CYCLE_LOCAL_TRANSITION_FALSIFIER_PASS",
        "original_sha256":SHA,
        "out_of_scope":"R quarter turn is not a physically valid Rubik R turn",
        "altered_generator_original": [0,11,4,8],
        "altered_generator_new":list(CYCLE),
        "changed_actions":["R","R'","R2"],
        "original_face_flip_support_preserved":True,
        "expected_rank7_phase_census_noncube":{"q3_words":128,
          "q3_distinct_partitions":28,"q4_words":448,
          "q4_distinct_partitions":16,
          "all_distinct_partitions":15158},
        "write_map":str(args.output)}))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--maps",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    main(p.parse_args())
