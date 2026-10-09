#!/usr/bin/env python3
"""Independent replay of four physically specified L6..L9 experiment dictionaries.
Reads the fresh physical 0.18 source + 18x24 sticker-derived legal HTM maps.
Exact integer/orientation histories only. M*(6) remains just bounded 3..4.
"""
import argparse, hashlib, json
from collections import defaultdict
from pathlib import Path
a=argparse.ArgumentParser()
a.add_argument('--physical',required=True);a.add_argument('--maps',required=True)
args=a.parse_args()
raw=Path(args.physical).read_bytes()
assert hashlib.sha256(raw).hexdigest()=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
sources=json.loads(raw)['bases']
moves=json.loads(Path(args.maps).read_text())
assert len(sources)==1192 and len(moves)==18
assert all(len(m)==24 and len(set(m))==24 for m in moves)
ACTIONS=[f+s for f in 'URFDLB' for s in ('',"'",'2')]
WORDS={
 6: ["F B U2 L F B","F' B' U L2 F B","F B U2 D F B","F B' U2 R F B"],
 7: ["F' B L D2 B U2 F","F' B R D2 B' U2 F","F B R F U' F B"],
 8: ["F U2 F B U2 D F B","F U2 F B U D2 F B"],
 9: ["F B U R2 F B' U F B"],
}
expected_ranks={6:[9,9,9,9],7:[10,10,9],8:[11,11],9:[12]}
def replay(text):
    word=[ACTIONS.index(t) for t in text.split()]
    s=[2*i for i in range(12)]
    h=[0]*12
    for k,act in enumerate(word):
        s=[moves[act][v] for v in s]
        h=[v|((s[i]&1)<<k) for i,v in enumerate(h)]
    blocks=defaultdict(list)
    for i,v in enumerate(h):blocks[v].append(i)
    count=0;cover=0
    for r,A in enumerate(sources):
        output=[h[i] for i in range(12) if A>>i&1]
        if len(set(output))==len(output):cover|=1<<r;count+=1
    return len(word),len(blocks),[g for g in blocks.values() if len(g)>1],count,cover,h
result={}
for L,words in WORDS.items():
    covered=0;checks=[]
    for w in words:
        length,rank,collisions,count,mask,h=replay(w)
        assert length==L
        covered |=mask
        checks.append({'word':w,'rank':rank,'merged_classes':collisions,'covered_source_sets':count})
    assert covered.bit_count()==1192,(L,covered.bit_count())
    assert [x['rank'] for x in checks]==expected_ranks[L]
    result[L]=checks
assert result[8][0]['merged_classes']==[[0,2]]
assert result[8][1]['merged_classes']==[[4,6]]
assert result[7][0]['merged_classes']==[[0,4],[1,8]]
assert result[7][1]['merged_classes']==[[2,6],[5,8]]
assert result[7][2]['merged_classes']==[[3,10],[7,11],[8,9]]
# Special source-family geometry: all triples, all mixed quartets, no source
# contains one of the three homogeneous four-edge position classes.
F=[1,5,8,9];B=[3,7,10,11];N=[0,2,4,6]
sets=set(sources)
from itertools import combinations
assert all(sum(1<<i for i in c) in sets for c in combinations(range(12),3))
assert sum(x.bit_count()==4 for x in sources)==492
for g in (F,B,N):
 mask=sum(1<<i for i in g)
 assert all((A&mask)!=mask for A in sources)
print('CUBE_REV_019_ALL_1192_L6_TO_L9_PHYSICAL_DICTIONARY_WITNESSES_PASS',
      json.dumps({str(L):[x['covered_source_sets'] for x in checks]
       for L,checks in result.items()},sort_keys=True))
print('CUBE_REV_019_TWO_WORD_COLLISION_SOURCE_FAMILY_GEOMETRY_PASS')
