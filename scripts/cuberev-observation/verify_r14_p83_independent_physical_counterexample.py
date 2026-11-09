#!/usr/bin/env python3
"""Independent full 648-state counterexample replay. Imports P5.1 geometry only, never P8.3 producer or matching count DP."""
import sys,contextlib,io,importlib.util,json
from itertools import product,permutations
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=Path('/mnt/data/CUBEREV_028_R14_P51_P48_GROUP_LIFT.py')
if not source.exists():source=HERE/'audit_r14_p51_p48_group_lift.py'
with contextlib.redirect_stdout(io.StringIO()):
 spec=importlib.util.spec_from_file_location('p51_for_p83',source)
 p51=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p51;spec.loader.exec_module(p51)
faces={i:next(f for f,n in p51.FACES.items() if n==p51.SLOTS[i][1]) for i in range(48)}
T={n:tuple(''.join(faces[k] for k in p51.PIECES[p]) for p in positions) for n,positions in ((2,p51.EDGES),(3,p51.CORNERS))}
assert len(T[2])==12 and len(T[3])==8

def parity(seq):
 return sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))%2

def completions(nfix,k):
 words=T[k];n=len(words)-nfix
 arr=[[],[]]
 for p in permutations(range(n)):
  for angles in product(range(k),repeat=n):
   if sum(angles)%k:continue
   state=''.join(words[:nfix])+''.join(words[nfix+p[i]][(a+angles[i])%k] for i in range(n) for a in range(k))
   arr[parity(p)].append(state)
 return arr
E=completions(9,2);C=completions(5,3)
assert (list(map(len,E)),list(map(len,C)))==([12,12],[27,27])
S=tuple((e,c,sign) for sign in range(2) for e in E[sign] for c in C[sign]);assert len(S)==648
A=((0,19,'R'),(0,20,'F'),(1,15,'D'))
B=((0,19,'R'),(0,20,'F'),(1,16,'R'),(1,19,'R'))

def compatible(state,reads):return all(state[s][q]==color for s,q,color in reads)
def verify(reads):
 survivors=[(e,c,p) for e,c,p in S if compatible((e,c,p),reads)]
 ep=[sum(all(e[q]==col for s,q,col in reads if s==0) for e in E[p]) for p in range(2)]
 cp=[sum(all(c[q]==col for s,q,col in reads if s==1) for c in C[p]) for p in range(2)]
 assert (ep,cp)==([1,1],[3,3]);assert len(survivors)==6
 hist=Counter();winners=[];partition_samples={}
 for qe,qc in product(range(24),repeat=2):
  groups=defaultdict(list)
  for i,(e,c,p) in enumerate(survivors):groups[(e[qe],c[qc])].append(i)
  partition=tuple(sorted((len(v) for v in groups.values()),reverse=True))
  hist[partition]+=1
  if all(len(v)==1 for v in groups.values()):winners.append((qe,qc))
  if qe==20 and qc==15:partition_samples['(20,15)']=partition
 assert winners
 return dict(source_counts=ep,corner_counts=cp,joint_count=len(survivors), joint_parity_strata=[sum(p==z for _,_,p in survivors) for z in range(2)],hist=[{'partition':list(k),'queries':v} for k,v in sorted(hist.items())],winning_single_frame_queries=len(winners),example_winning_query=winners[0],example_partition=partition_samples)
a=verify(A);b=verify(B)
assert a['hist']!=b['hist']
aH={tuple(x['partition']):x['queries'] for x in a['hist']};bH={tuple(x['partition']):x['queries'] for x in b['hist']}
assert aH[(2,2,1,1)]==132 and bH.get((2,2,1,1),0)==0
assert bH[(2,2,2)]==132 and aH.get((2,2,2),0)==0
receipt={'result':'R14_P83_INDEPENDENT_PHYSICAL_648_COUNTEREXAMPLE_PASS', 'original_geometry_dependency':str(source), 'fully_observed_initial_prefix':{'edges':9,'corners':5,'states':648},'history_A':A,'history_B':B,'A':a,'B':b,'different_all_query_partition_multisets':True,'same_four_sector_counts':True,'same_Bellman_depth_1':True,'limitations':'All 576 physically indexed observation query partitions of six-state beliefs; independent P5.1-orientation state enumeration, no unconditioned full-cube 20-frame result.'}
(HERE/'R14_P83_INDEPENDENT_PHYSICAL_COUNTEREXAMPLE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
