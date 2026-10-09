#!/usr/bin/env python3
"""CUBE-REV 0.18: exact *double* all-k Rubik dictionary quotient.

First: all 1192 Cube source coverage clauses -> 398 logically stronger rows.
Second: on those same 398 rows, each of the genuine 1323 maximal physical
4-HTM experiments can be replaced by a covering-dominating member of a
168-member antichain. Both operations are exact for ANY cardinality k.

No near-tight k24 hypothesis is used; this supplies a NEW all-k justification.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--physical',required=True)
p.add_argument('--row-core',required=True)
p.add_argument('--output',required=True)
a=p.parse_args()
source=Path(a.physical)
raw=source.read_bytes()
d=json.loads(raw)
r=json.loads(Path(a.row_core).read_text())
assert d['counts']=={
    'literal':104976,'partitions':1913,
    'coverageTypes':1477,'maximal':1323,'bases':1192
}
assert r['physical_input_sha256']==hashlib.sha256(raw).hexdigest()
rows=r['retained_row_indices']
assert len(rows)==398
original_masks=[int(x['mask'],16) for x in d['candidates']]
assert len(original_masks)==1323
# A second, independent calculation of the 398-row projection.
projected=[]
for col in original_masks:
    projected.append(sum(1<<i for i,original in enumerate(rows)
                         if col>>original&1))
assert len(projected)==1323
representatives={}
for i,m in enumerate(projected):
    representatives.setdefault(m,i)
assert len(representatives)==361
sorted_projection=sorted(representatives.items(),
                         key=lambda z:(-z[0].bit_count(),z[1]))
maximal=[]
for mask,original_idx in sorted_projection:
    if not any((mask&~other)==0 for other,_ in maximal):
        maximal.append((mask,original_idx))
assert len(maximal)==168
assert len(set(k for _,k in maximal))==168
assert Counter(d['candidates'][j]['mass'] for _,j in maximal)=={20:162,16:6}
# Assign an explicit, independently checkable dominant representative
# to every one of the original 1323 Rubik word candidates.
dominator_indices=[]
for mask in projected:
    valid=[j for m,j in maximal if (mask&~m)==0]
    assert valid,"Physical cube candidate has no projected dominator"
    dominator_indices.append(valid[0])
max_ids=[j for _,j in maximal]
assert set(dominator_indices).issubset(set(max_ids))
# Covering *only* these 398 original rows implies all 1192,
# using the separately certified row-subsumption lemma. Conversely
# each reduced candidate is one actual original physical move word.
record={
  'schema':'cube-rev.018.physical-double-dominance-all-k-v1',
  'physical_sha256':hashlib.sha256(raw).hexdigest(),
  'row_core_sha256':hashlib.sha256(Path(a.row_core).read_bytes()).hexdigest(),
  'original_source_rows':1192,
  'core_original_source_rows':398,
  'original_maximal_physical_columns':1323,
  'distinct_projected_column_masks':361,
  'equivalent_maximal_physical_columns':168,
  'representative_original_candidate_ids':max_ids,
  'dominator_original_id_for_each_original_candidate':dominator_indices,
  'representative_original_HTM_words':[d['candidates'][j]['word'] for j in max_ids],
  'mass_numerator_histogram':{'20':162,'16':6},
  'statement':('For every cardinality bound k, original physical Rubik '
               'dictionary size <=k exists iff 398 retained source '
               'conditions are covered by <=k of the listed 168 original '
               'four-HTM word representatives. The 1192->398 row '
               'implication and 1323->168 column dominance each have '
               'explicit independently checkable witnesses.')
}
out=Path(a.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2)+'\n')
print('CUBE_REV_018_FULL_ALL_K_398_X_168_DOUBLE_QUOTIENT_PASS',
      json.dumps({k:record[k] for k in
       ('original_source_rows','core_original_source_rows',
        'original_maximal_physical_columns',
        'distinct_projected_column_masks','equivalent_maximal_physical_columns')},
       sort_keys=True),flush=True)
