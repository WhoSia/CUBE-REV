#!/usr/bin/env python3
"""Exact 648-state physical 9E5C suffix full AND-OR paired query game. Uses archived P5.1 physical sticker orientation only."""
from pathlib import Path
import io,contextlib,sys,importlib.util,json
from itertools import product,permutations
from functools import lru_cache
from collections import Counter
source=Path('/mnt/data/CUBEREV_028_R14_P51_P48_GROUP_LIFT.py')
if not source.exists():source=Path(__file__).with_name('audit_r14_p51_p48_group_lift.py')
with contextlib.redirect_stdout(io.StringIO()):
 sp=importlib.util.spec_from_file_location('p51_physical_648',source)
 p=importlib.util.module_from_spec(sp);sys.modules[sp.name]=p;sp.loader.exec_module(p)
faces={j:next(f for f,n in p.FACES.items() if n==p.SLOTS[j][1]) for j in range(48)}
E=tuple(''.join(faces[j] for j in p.PIECES[pos]) for pos in p.EDGES)
C=tuple(''.join(faces[j] for j in p.PIECES[pos]) for pos in p.CORNERS)
def sign(a):return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2
def sector(words,prefix,mod):
 n=len(words)-prefix;g=[[],[]]
 for perm in permutations(range(n)):
  for head in product(range(mod),repeat=n-1):
   ori=head+((-sum(head))%mod,)
   word=''.join(words[:prefix])+''.join(words[prefix+perm[i]][(j+ori[i])%mod] for i in range(n) for j in range(mod))
   g[sign(perm)].append(word)
 return g
es=sector(E,9,2);cs=sector(C,5,3)
states=tuple((e,c) for z in range(2) for e in es[z] for c in cs[z]);assert len(states)==648
# Full 576 possible P48 query pairs are equivalent to 54 informative ones when the prefix is fixed.
queries=tuple(product(range(18,24),range(15,24)))
byq=[]
for qe,qc in queries:
 d={}
 for i,(e,c) in enumerate(states):
  label=e[qe]+c[qc];d[label]=d.get(label,0)|(1<<i)
 byq.append(d)
whole=(1<<648)-1
@lru_cache(None)
def win(mask,depth):
 if mask.bit_count()==1:return True
 if not depth or mask.bit_count()>36**depth:return False
 for q in byq:
  children=[mask & z for z in q.values() if mask&z]
  if len(children)<2 or max(z.bit_count() for z in children)>36**(depth-1):continue
  if all(win(z,depth-1) for z in sorted(children,key=int.bit_count,reverse=True)):
   return True
 return False
results={}
for depth in (2,3,4,5):
 results[str(depth)]=win(whole,depth)
 print('ROOT_BELLMAN',depth,results[str(depth)],'cache',win.cache_info().currsize,flush=True)
 if results[str(depth)]:break
D=next(int(d) for d,v in results.items() if v)
@lru_cache(None)
def policy(mask,depth):
 if mask.bit_count()==1:return {'leaf':mask.bit_length()-1}
 for i,q in enumerate(byq):
  buckets={y:mask&m for y,m in q.items() if mask&m}
  if len(buckets)>1 and all(win(z,depth-1) for z in buckets.values()):
   return {'q':i,'branches':{y:policy(m,depth-1) for y,m in sorted(buckets.items())}}
 raise AssertionError('policy unreachable')
tree=policy(whole,D)
def replay(i):
 e,c=states[i];node=tree;depth=0
 while 'q' in node:
  qe,qc=queries[node['q']];node=node['branches'][e[qe]+c[qc]];depth+=1
 assert node['leaf']==i
 return depth
hist=Counter(replay(i) for i in range(648))
receipt={'result':'R14_P83_EXACT_648_PHYSICAL_SUFFIX_ANDOR_PASS','physical_prefix':{'fully_observed_edges':9,'fully_observed_corners':5},'legal_states':648,'informative_paired_actions':len(queries),'exact_root_win_depths':results,'exact_minimax_depth':D,'decoder_replays':648,'depth_histogram':dict(sorted(hist.items())),'root_query_local':queries[tree['q']],'root_adversarial_depth_minus_one':[{ 'query':q,'bad_output':next((y for y,m in byq[i].items() if not win(whole&m,D-2)),None)} for i,q in enumerate(queries)] if D>=2 else [],'bellman_memo_entries':win.cache_info().currsize,'scope':'Only physical P48 9E5C fully-read suffix conditioned on fixed prior cube information; NOT original 20-frame root result.'}
assert len(receipt['root_adversarial_depth_minus_one'])==54 and all(q['bad_output'] is not None for q in receipt['root_adversarial_depth_minus_one'])
Path(__file__).with_name('R14_P83_PHYSICAL_648_EXACT_ANDOR_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
