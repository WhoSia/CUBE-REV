#!/usr/bin/env python3
"""Exact integer / real-physical source validator of P13 k7 >=2 high-rank theorem.
No SAT, no LP, no SciPy. Checker uses independently supplied source and physical
partition representatives and complete 32 residual integer-dual certificates.
"""
import argparse,hashlib,json
from pathlib import Path
P=argparse.ArgumentParser()
for key in ('physical','partitions','certificates','output'):P.add_argument('--'+key,required=True)
a=P.parse_args()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
bases=json.loads(raw)['bases'];idx=[i for i,b in enumerate(bases) if b.bit_count()==5]
assert len(bases)==1192 and len(idx)==480
classes={5:set(),6:set(),7:set()}
N=0
for line in Path(a.partitions).read_text().splitlines():
 act,blocks=line.split('|');parts=list(map(int,blocks.split()));N+=1
 assert len(parts)==len(set(parts)) and sum(parts)==4095 and sum(v.bit_count() for v in parts)==12
 if len(parts) in classes:
  cover=0
  for j,i in enumerate(idx):
   if all((bases[i]&b).bit_count()<=1 for b in parts):cover|=1<<j
  classes[len(parts)].add(cover)
assert N==14938
assert tuple(map(lambda k:len(classes[k]),(5,6,7)))==(2168,1144,32)
cert=json.loads(Path(a.certificates).read_text())
assert cert['original_source_sha256']==sha
assert cert['raw_rank5_cover_types']==2168
assert cert['raw_rank6_cover_types']==1144
assert cert['raw_rank7_cover_types']==32
low=sorted(classes[5]);strong=sorted(classes[6]|classes[7]);full=(1<<480)-1
entries={int(z['original_480_mask_hex'],16):z for z in cert['certificates']}
assert len(entries)==32
volume=0;intproof=0;smallest_gap=10**99
for h in strong:
 leftover=full&~h
 max_gain=max((leftover&l).bit_count() for l in low)
 if leftover.bit_count()>6*max_gain:
  assert h not in entries
  volume+=1;continue
 z=entries[h];w={int(i):int(k) for i,k in z['weight_original_five_row_index']}
 assert len(w)>0 and all(0<=i<480 and v>0 and not ((h>>i)&1) for i,v in w.items())
 W=sum(w.values());B=max(sum(v for i,v in w.items() if l>>i&1) for l in low)
 assert W==z['total'] and B==z['max_raw_rank5_word'] and W-6*B==z['gap'] and W>6*B
 smallest_gap=min(smallest_gap,W-6*B);intproof+=1
assert volume==1144 and intproof==32
receipt={'status':'CUBE_REV_019_P13_R5_K7_AT_LEAST_TWO_HIGH_RANK_PHYSICAL_INTEGER_PASS',
 'original_physical_source_sha256':sha,'five_source_count':480,'physical_L5_partitions':N,
 'original_physical_rank5_cover_types':2168,'original_physical_high_cover_types':1176,
 'volume_excluded_one_high_cases':volume,'integer_dual_excluded_one_high_cases':intproof,
 'smallest_verified_integer_gap':smallest_gap,
 'theorem':'Any 7-word R5 complete physical dictionary has at least two words with >=6 distinct original-state histories',
 'not_proved':'Full 1192-source k7 SAT or UNSAT is not decided by these necessary conditions'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['status'],json.dumps({k:receipt[k] for k in ('volume_excluded_one_high_cases','integer_dual_excluded_one_high_cases','smallest_verified_integer_gap')}),flush=True)