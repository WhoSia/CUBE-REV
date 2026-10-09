#!/usr/bin/env python3
"""0.18 Rubik exact double-quotient connected-component factorisation.

Once the real 1192x1323 Cube set cover is provably reduced to the
equivalent 398x168 matrix, the residual bipartite graph splits into
disjoint components (334 sources x 80 real 4-HTM words) and
(64 sources x 88 real 4-HTM words). This is an ALL-k decomposition:
M* equals the sum of the two independent component set-cover minima.
"""
import argparse
import hashlib
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--physical',required=True)
p.add_argument('--rows',required=True)
p.add_argument('--columns',required=True)
p.add_argument('--output',required=True)
a=p.parse_args()
physical_raw=Path(a.physical).read_bytes()
raw_rows=Path(a.rows).read_bytes()
raw_cols=Path(a.columns).read_bytes()
physical=json.loads(physical_raw)
row_cert=json.loads(raw_rows)
col_cert=json.loads(raw_cols)
assert physical['counts']=={
  'literal':104976,'partitions':1913,
  'coverageTypes':1477,'maximal':1323,'bases':1192}
assert row_cert['physical_input_sha256']==hashlib.sha256(physical_raw).hexdigest()
assert col_cert['physical_sha256']==hashlib.sha256(physical_raw).hexdigest()
assert col_cert['row_core_sha256']==hashlib.sha256(raw_rows).hexdigest()
retained=row_cert['retained_row_indices']
reps=col_cert['representative_original_candidate_ids']
assert len(retained)==398 and len(reps)==168
masks=[int(c['mask'],16) for c in physical['candidates']]
# Bipartite disjoint-set-union over original row and projected column IDs
parent=list(range(398+168))
def root(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]
        x=parent[x]
    return x
def join(a,b):
    x=root(a);y=root(b)
    if x!=y:parent[y]=x
for i,original_row in enumerate(retained):
    for j,original_col in enumerate(reps):
        if masks[original_col]>>original_row&1:
            join(i,398+j)
cc={}
for v in range(398+168):
    cc.setdefault(root(v),[]).append(v)
assert len(cc)==2,('Unexpected bipartite components',len(cc))
components=[]
for vertices in cc.values():
    r=[i for i in vertices if i<398]
    c=[i-398 for i in vertices if i>=398]
    nslots={physical['bases'][retained[i]].bit_count() for i in r}
    assert len(nslots)==1
    slot=next(iter(nslots))
    for i in r:
        assert any(masks[reps[j]]>>retained[i]&1 for j in c)
        assert all(not(masks[reps[j]]>>retained[i]&1)
                   for j in range(168) if j not in c)
    for j in c:
        assert all(not(masks[reps[j]]>>retained[i]&1)
                   for i in range(398) if i not in r)
    components.append({
      'name':f'cube_{slot}_slot_source_component',
      'slot_count':slot,
      'retained_row_positions':sorted(r),
      'original_source_row_indices':[retained[i] for i in sorted(r)],
      'retained_column_positions':sorted(c),
      'original_maximal_HTM_column_indices':[reps[i] for i in sorted(c)],
      'source_rows':len(r),'real_cube_HTM_columns':len(c)
    })
components.sort(key=lambda q:-q['source_rows'])
assert [(x['slot_count'],x['source_rows'],x['real_cube_HTM_columns'])
        for x in components]==[(5,334,80),(4,64,88)]
assert sum(x['source_rows'] for x in components)==398
assert sum(x['real_cube_HTM_columns'] for x in components)==168
assert len(set(i for c in components for i in c['retained_row_positions']))==398
assert len(set(i for c in components for i in c['retained_column_positions']))==168
result={
 'schema':'cube-rev.018.physical-component-factorisation-v1',
 'physical_sha256':hashlib.sha256(physical_raw).hexdigest(),
 'row_certificate_sha256':hashlib.sha256(raw_rows).hexdigest(),
 'column_certificate_sha256':hashlib.sha256(raw_cols).hexdigest(),
 'components':components,
 'theorem':('For every cardinality k, the original real-3x3 Rubik '
            'dictionary min-cardinality problem equals the sum of '
            'the two component minima, because every retained physical '
            'HTM word distinguishes original sources in exactly one '
            'of the two disjoint independent blocks.'),
 'unverified_numerical_component_optima':{
    'cube_5_slot_source_component':27,
    'cube_4_slot_source_component':7
 }
}
out=Path(a.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print('CUBE_REV_018_EXACT_PHYSICAL_TWO_COMPONENT_FACTORISATION_PASS',
      json.dumps([(x['source_rows'],x['real_cube_HTM_columns'])
                  for x in components]),flush=True)
