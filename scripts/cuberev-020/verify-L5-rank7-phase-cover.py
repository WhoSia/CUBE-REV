#!/usr/bin/env python3
"""P1-E: exact restricted all-rank7 L5 M-star=8 on original 1,192 Rubik source demands.
A 12-original-source certificate excludes all 4,368 selections of five q4 partitions.
The q3-exclusive requirements independently force two q3 partitions.
Scope: all chosen words have rank seven. The unrestricted theorem is P13, not this file.
"""
import argparse
import collections
import csv
import hashlib
import itertools
import json
from pathlib import Path

SHA="9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1"
OBSTRUCTION=(0x303,0xcc0,0x1105,0x1206,0x2448,0x2888,
             0x4450,0x4890,0x6018,0x8121,0x8222,0x9024)
TOKENS=("U","U'","U2","R","R'","R2","F","F'","F2",
        "D","D'","D2","L","L'","L2","B","B'","B2")
EIGHT=("F' B' L F B","F' B' R F B","F' B' D F B",
       "F L2 B' D2 F","F U2 B R2 F","F' B' U F B",
       "F B L F B","F B R F B")

def physical_key(word,maps):
    position=[2*i for i in range(12)]
    observations=[0]*12
    for a in word:
        position=[maps[a][x] for x in position]
        observations=[(h<<1)|(x&1) for h,x in zip(observations,position)]
    labels={};key=0
    for i,h in enumerate(observations):
        if h not in labels:labels[h]=len(labels)
        key|=labels[h]<<(4*i)
    return key

def covered(key,requirements):
    code=[(key>>(4*i))&15 for i in range(12)]
    return sum(1<<i for i,req in enumerate(requirements)
               if len({code[p] for p in range(12) if req>>p&1})==req.bit_count())

def main(args):
    physical=args.source.read_bytes()
    sha=hashlib.sha256(physical).hexdigest()
    assert sha==SHA,("original input drift",sha)
    requirements=json.loads(physical)["bases"]
    assert len(requirements)==1192
    maps=[[int(x) for x in l.split()] for l in args.maps.read_text().splitlines()]
    assert len(maps)==18 and all(len(row)==24 for row in maps)
    by_phase={3:set(),4:set()}
    rows=list(csv.DictReader(args.records.open()))
    assert len(rows)==640
    for row in rows:
        q=int(row["q"])
        assert q in by_phase
        word=[int(row["a"+str(i)]) for i in range(5)]
        k=physical_key(word,maps)
        assert k==int(row["key"])
        assert len({(k>>(4*i))&15 for i in range(12)})==7
        by_phase[q].add(k)
    assert all(len(values)==16 for values in by_phase.values())
    assert not by_phase[3]&by_phase[4]
    cols={q:[covered(k,requirements) for k in sorted(by_phase[q])]
          for q in (3,4)}
    unions={}
    for q in (3,4):
        u=0
        for mask in cols[q]:u|=mask
        unions[q]=u
    assert unions[3].bit_count()==604
    assert unions[4].bit_count()==1110
    all_req=(1<<1192)-1
    assert unions[3]|unions[4]==all_req
    only3=unions[3]&~unions[4]
    only4=unions[4]&~unions[3]
    assert (only3.bit_count(),only4.bit_count())==(82,588)
    assert all((col&only3).bit_count()==41 for col in cols[3])
    supports={}
    for i,mask in enumerate(requirements):
        if not(only4>>i&1):continue
        support=sum(1<<j for j,col in enumerate(cols[4]) if col>>i&1)
        supports.setdefault(support,[]).append(i)
    assert len(supports)==87
    minimal={m for m in supports if not any(n!=m and n&m==n for n in supports)}
    assert len(minimal)==36
    assert set(OBSTRUCTION)<=minimal
    # Each support comes from an actual original source requirement whose
    # original source mask is recorded in the proof receipt.
    for choice in itertools.combinations(range(16),5):
        selected=sum(1<<j for j in choice)
        assert any(selected & support == 0 for support in OBSTRUCTION)
    witness_six=next((c for c in itertools.combinations(range(16),6)
                      if all(sum(1<<j for j in c)&m for m in minimal)),None)
    assert witness_six is not None
    # A single q3 word can cover only 41 of 82 q3-only requirements.
    # All choices of five q4 words fail 12 independently instantiated rows.
    # Hence every all-rank7 full cover needs at least 2+6=8 words.
    upper=0
    positive=[]
    for w in EIGHT:
        word=[TOKENS.index(tok) for tok in w.split()]
        q=sum(a in (6,7,15,16) for a in word)
        assert q in (3,4)
        key=physical_key(word,maps)
        assert key in by_phase[q]
        upper|=covered(key,requirements)
        positive.append({"word":w,"q":q})
    assert upper==all_req
    assert collections.Counter(p["q"] for p in positive)=={3:2,4:6}
    certificate=[{"support_hex":hex(m),
                  "original_source_index":supports[m][0],
                  "original_source_mask":requirements[supports[m][0]]}
                 for m in OBSTRUCTION]
    print(json.dumps({
      "schema":"cube-rev.020.P1-E.rank7-only-eight.v1",
      "result":"CUBE_REV_020_P1E_RANK7_ONLY_MSTAR5_EIGHT_EXACT_LOCAL_PASS",
      "original_physical_sha256":sha,
      "source_requirements":1192,
      "phase_q3_rank7_partitions":16,
      "phase_q4_rank7_partitions":16,
      "phase_q3_union_requirements":604,
      "phase_q4_union_requirements":1110,
      "rank7_q3_exclusive_requirements":82,
      "rank7_q4_exclusive_requirements":588,
      "q3_per_word_exclusive_coverage":41,
      "q4_all_minimal_supports":36,
      "q4_selected_12_original_source_court":certificate,
      "q4_five_column_selections_checked":4368,
      "q4_six_column_witness":list(witness_six),
      "all_rank7_exact_minimum":8,
      "actual_real_physical_eight_word_upper_witness":positive,
      "scope":"rank-seven words only; unrestricted P13 lower bound separate",
      "external_CI":"NOT_YET_CONFIRMED"},indent=2,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True,type=Path)
    ap.add_argument("--maps",required=True,type=Path)
    ap.add_argument("--records",required=True,type=Path)
    main(ap.parse_args())
