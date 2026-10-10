import json,time,os
from pathlib import Path
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import numpy as np
p=Path(os.environ.get('P13_DATA_ROOT',Path(__file__).parent));src=json.loads((p/'original_physical.json').read_text())['bases'];n=len(src)
byrank={5:set(),6:set()}
for line in (p/'original_L5_partitions.tsv').read_text().splitlines():
 _,s=line.split('|');v=list(map(int,s.split()))
 if len(v) in byrank:byrank[len(v)].add(sum(1<<i for i,a in enumerate(src) if all((a&z).bit_count()<=1 for z in v)))
low=sorted(byrank[5]|byrank[6]);maxs=[]
for m in sorted(low,key=int.bit_count,reverse=True):
 if not any(m&~x==0 for x in maxs):maxs.append(m)
rows=[];cols=[]
for j,m in enumerate(maxs):
 while m:
  bit=m&-m;rows.append(bit.bit_length()-1);cols.append(j);m-=bit
A=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(n,len(maxs)))
branches=[]
for x,y in [(0,24),(24,49),(49,74)]:branches+=json.loads((p/f'P13_t0_conditional_integer_duals_{x}_{y}.json').read_text())['open_cases']
assert len(branches)==9
records=[]
for x in branches:
 mask=int(x['representative_mask_hex'],16)
 available=np.array([not bool(mask>>i&1) for i in range(n)])
 k=np.flatnonzero(available)
 opt=linprog(np.ones(len(maxs)),A_ub=-A[available],b_ub=-np.ones(int(available.sum())),bounds=(0,None),method='highs')
 assert opt.success
 D=10**7;w={int(k[i]):int(v*D) for i,v in enumerate(np.maximum(0,-opt.ineqlin.marginals)) if int(v*D)>0}
 W=sum(w.values());byweight=lambda m:sum(weight for row,weight in w.items() if m>>row&1)
 B=max(map(byweight,low));T=W-5*B
 eligible={r:[m for m in byrank[r] if byweight(m)>=T] for r in (5,6)}
 record={'first_orbit':x['index'],'first_coverage_hex':hex(mask),'W':W,'B':B,'remaining_six_per_word_threshold':T,
 'initial_rank5_words':len(byrank[5]),'eligible_rank5_words':len(eligible[5]),'initial_rank6_words':len(byrank[6]),'eligible_rank6_words':len(eligible[6]),'rows_weights':{str(k):v for k,v in w.items()}}
 records.append(record)
 print('ORB',x['index'],'RANK5',len(eligible[5]),'RANK6',len(eligible[6]),'W/B',round(W/B,5),flush=True)
(p/'P13_t0_nine_open_weight_filters.json').write_text(json.dumps({'source_sha256':'9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1','records':records,'proof':'For any six-word residual cover with each column weighted mass <= B, each of six selected words must have weight >= W-5B. All W/B are checked over every ORIGINAL physical rank5/6 source-coverage mask.'},indent=2))