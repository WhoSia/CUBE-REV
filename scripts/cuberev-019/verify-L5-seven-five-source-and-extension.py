#!/usr/bin/env python3
"""CUBE-REV 0.19 P10: fixed seven-HTM-word R5 cover and its one-word extension obstruction.
Source-locked original 1192 R, independent sticker-derived 18x24 map replay,
full exact 14938 physically attainable 5-turn output partitions enumeration.
Does NOT infer R5 6-word UNSAT or full-source 7/8-word optimality.
"""
import argparse,hashlib,json,collections
from pathlib import Path
p=argparse.ArgumentParser()
for z in ('physical','maps','partitions','output'):p.add_argument('--'+z,required=True)
a=p.parse_args();raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
bases=json.loads(raw)['bases'];assert len(bases)==1192
maps=[list(map(int,s.split())) for s in Path(a.maps).read_text().splitlines()];assert len(maps)==18 and all(len(x)==24 and len(set(x))==24 for x in maps)
actions=[f+s for f in 'URFDLB' for s in ('',"'",'2')]
words=["F' B' U F B", "F' B D F B", "F B' L F B", "F B' D F B", "F B' R F B", "F B U F B", "F B' U2 L2 F"]
def blocks(word):
 states=[2*i for i in range(12)];hist=[0]*12
 for k,act in enumerate(word):
  states=[maps[act][v] for v in states]
  hist=[v|((states[i]&1)<<k) for i,v in enumerate(hist)]
 d={}
 for i,v in enumerate(hist):d[v]=d.get(v,0)|(1<<i)
 return tuple(sorted(d.values()))
def coverage(cuts):
 return sum(1<<j for j,A in enumerate(bases) if all((A&b).bit_count()<=1 for b in cuts))
U=0;perword=[]
for text in words:
 word=[actions.index(t) for t in text.split()];assert len(word)==5
 cuts=blocks(word);cov=coverage(cuts);U|=cov
 perword.append({'word':text,'physical_move_ids':word,'output_partition_rank':len(cuts),'original_sources_covered':cov.bit_count(), 'five_sources_covered':sum((cov>>j)&1 for j,r in enumerate(bases) if r.bit_count()==5)})
five=[j for j,r in enumerate(bases) if r.bit_count()==5];assert len(five)==480
assert all((U>>j)&1 for j in five)
miss=[j for j in range(1192) if not((U>>j)&1)]
assert len(miss)==72 and collections.Counter(bases[j].bit_count() for j in miss)=={4:64,3:8}
missmask=sum(1<<j for j in miss)
max_extension=0;winning_examples=[];partitions=0
for row in Path(a.partitions).read_text().splitlines():
 wtxt,btxt=row.split('|');word=tuple(map(int,wtxt.split()));got=tuple(sorted(map(int,btxt.split())))
 assert blocks(word)==got, 'actual physical oracle partition mismatch'
 c=coverage(got)&missmask;n=c.bit_count();partitions+=1
 if n>max_extension:max_extension=n;winning_examples=[wtxt]
 elif n==max_extension and len(winning_examples)<5:winning_examples.append(wtxt)
assert partitions==14938 and max_extension==36
receipt={'schema':'cube-rev.019.P10.original-R5-seven-witness-extension-obstruction.v1','source_sha256':sha,
 'original_five_set_count':len(five),'seven_words':perword,'R5_source_coverage_complete':True,
 'original_1192_source_coverage':U.bit_count(),'uncov_triples':8,'uncov_four_sets':64,'uncov_five_sets':0,
 'uncovered_original_source_indices':miss,
 'physical_5_HTM_partitions_exhaustively_checked':partitions,
 'maximum_uncovered72_sources_separable_by_one_additional_real_5_HTM_word':max_extension,
 'witness_additional_word_ids':winning_examples,
 'theorem_for_this_particular_seven_word_dictionary':'No one additional physical 5-HTM word can make THIS dictionary cover original 1192 sources.',
 'not_claimed':'No general M*(5)>=8 theorem or R5 k6 UNSAT theorem; alternate seven-word dictionaries may differ.'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print('CUBE_REV_019_P10_480_FIVE_SOURCE_SEVEN_WORD_UPPER_PHYSICAL_PASS',len(words),'words')
print('CUBE_REV_019_P10_SEVEN_WORD_EXTENSION_ONE_WORD_IMPOSSIBLE_PHYSICAL_14938_PARTITIONS_MAX36_PASS')