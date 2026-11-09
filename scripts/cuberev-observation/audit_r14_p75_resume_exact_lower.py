#!/usr/bin/env python3
"""Resume exact D-1 six-edge AND/OR court after first twelve P7.4 cases.
Per-case 16-second gate; timeouts are UNRESOLVED, never negative proof.
Stand-alone state and color partitions, prior P7.4 source receipts dependencies explicit.
"""
import json,time,signal,sys
from pathlib import Path
from itertools import permutations,product
from functools import lru_cache
H=Path(__file__).resolve().parent
U=json.loads((H/'R14_P74_SIX_EDGE_ORBIT_POLICY_RECEIPT.json').read_text())['rows']
old=json.loads((H/'R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES_RECEIPT.json').read_text())['rows']
assert len(U)==30 and len(old)==12
rows=list(old);fail=[]
case_sec=float(sys.argv[1]) if len(sys.argv)>1 else 10
max_new=int(sys.argv[2]) if len(sys.argv)>2 else 18
start_index=int(sys.argv[3]) if len(sys.argv)>3 else 13
class CaseTimeout(Exception):pass
def timeout(a,b):raise CaseTimeout()
signal.signal(signal.SIGALRM,timeout)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
for nr,r in enumerate(U[start_index-1:start_index-1+max_new],start=start_index):
 L=r['representative'];N=len(L);t=time.monotonic();estimated=r['one_step_worst_depth'];words=[]
 for p in permutations(range(N)):
  if parity(p):continue
  for ff in product((0,1),repeat=N-1):
   f=ff+(sum(ff)%2,)
   words.append(''.join(L[p[i]][s^f[i]] for i in range(N) for s in range(2)))
 assert len(words)==11520 and len(set(words))==11520
 masks=[{} for _ in range(12)]
 for ix,w in enumerate(words):
  for q,c in enumerate(w):masks[q][c]=masks[q].get(c,0)|(1<<ix)
 def children(B,q):return [z for mask in masks[q].values() if (z:=B&mask)]
 @lru_cache(None)
 def win(B,k):
  z=B.bit_count()
  if z==1:return True
  if k==0 or z>6**k:return False
  opts=[]
  for q in range(12):
   ch=children(B,q)
   if len(ch)<=1:continue
   ns=[v.bit_count() for v in ch]
   if max(ns)>6**(k-1):continue
   opts.append(((max(ns),len(ch),sum(v*v for v in ns),q),ch))
  for _,ch in sorted(opts,key=lambda x:x[0]):
   if all(win(c,k-1) for c in sorted(ch,key=int.bit_count,reverse=True)):return True
  return False
 try:
  signal.setitimer(signal.ITIMER_REAL,case_sec)
  solution=win((1<<11520)-1,estimated-1)
  signal.setitimer(signal.ITIMER_REAL,0)
  new={'representative':L,'orbit_size':r['orbit_size'],'policy_upper':estimated,'cannot_finish_one_fewer':not solution,'recursion_states':win.cache_info().currsize,'seconds':round(time.monotonic()-t,3),'case_index':nr,'status':'EXACT'}
  rows.append(new)
  if solution:fail.append(new)
  print('EXACT',nr,'D',estimated,'no_shorter',not solution,'states',win.cache_info().currsize,flush=True)
 except CaseTimeout:
  signal.setitimer(signal.ITIMER_REAL,0)
  new={'representative':L,'orbit_size':r['orbit_size'],'policy_upper':estimated,'recursion_states_before_timeout':win.cache_info().currsize,'seconds':round(time.monotonic()-t,3),'case_index':nr,'status':'TIMEOUT_UNRESOLVED'}
  fail.append(new)
  print('TIMEOUT',nr,'D',estimated,'states',win.cache_info().currsize,flush=True)
 del win,masks,words
 obj={'result':'R14_P75_RESUMABLE_EXACT_LOWER_PARTIAL','original_exact12':12,'attempted_new':min(max_new,31-start_index),'start_index':start_index,'total_exact_lower_successes':len(rows),'unresolved_or_counterexamples':fail,'rows':rows,'claims':'Only exact rows with cannot_finish_one_fewer=true prove optimality. TIMEOUT_UNRESOLVED is not evidence for lower. Exact short-policy existence means greedy counterexample and must be explicitly preserved.'}
 (H/'R14_P75_RESUMED_LOWER_PARTIAL_RECEIPT.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print('R14_P75_RESUMED_COURT',len(rows),'exact completed',len(fail),'not negative / unresolved')
