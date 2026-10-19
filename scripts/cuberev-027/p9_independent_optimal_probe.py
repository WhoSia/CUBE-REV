#!/usr/bin/env python3
"""Independent 54-site proof-checking interface to RubikOptimal 1.1.0.
Selftest runs offline without the external pruning tables.
"""
import hashlib, json, random, re, sys
F='URFDLB'; O='UDRLFB'; SRC="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2"
WIT="F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2"
FACE='LLRUURDDURDFLRLRBLLBFBFBBFDLDBUDRBLFBFFFLUURDDFUDBRUUR'
P_HASH='b8358549a11138ee057b9a2451249425e1cf1d35c7bb3fe01be500ff56882568'
def pos(i):
 f,j=divmod(i,9);a,b=divmod(j,3);a-=1;b-=1
 return ((a,1,b),(a,-1,b),(1,a,b),(-1,a,b),(a,b,1),(a,b,-1))[f]
def nrm(f):return ((0,1,0),(0,-1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1))[f]
def rot(v,axis,k):
 for _ in range(k%4):
  x,y,z=v;v=((x,-z,y),(z,y,-x),(-y,x,z))[axis]
 return v
def mktables():
 site={(pos(i),nrm(i//9)):i for i in range(54)};assert len(site)==54
 out=[]
 for a in range(18):
  axis,layer,sign=((1,1,-1),(0,1,-1),(2,1,-1),(1,-1,1),(0,-1,1),(2,-1,1))[a//3]
  mat=[-1]*54
  for i in range(54):
   p,n=pos(i),nrm(i//9)
   if p[axis]==layer:p,n=rot(p,axis,sign*(1,2,3)[a%3]),rot(n,axis,sign*(1,2,3)[a%3])
   j=site[(p,n)];assert mat[j]==-1;mat[j]=i
  assert sorted(mat)==list(range(54));out.append(mat)
 return out
P=mktables();assert hashlib.sha256(bytes(sum(P,[]))).hexdigest()==P_HASH
def stdsite(i):
 f=i//9;x,y,z=pos(i)
 if f==0:r,c=z+1,x+1
 elif f==2:r,c=1-y,1-z
 elif f==4:r,c=1-y,x+1
 elif f==1:r,c=1-z,x+1
 elif f==3:r,c=1-y,z+1
 else:r,c=1-y,1-x
 return F.index(O[f])*9+3*r+c
sites=[stdsite(i) for i in range(54)];assert sorted(sites)==list(range(54))
def parse_word(s):
 ans=[]
 for tok in s.split():
  assert re.fullmatch(r"[URFDLB](?:2|')?",tok),tok
  ans.append(3*F.index(tok[0])+{'':0,'2':1,"'":2}[tok[1:]])
 return ans
def replay(state,word):
 for a in word:state=tuple(state[P[a][j]] for j in range(54))
 return state
def stdstr(state):
 out=['?']*54
 for i,v in enumerate(state):out[sites[i]]=O[v//9]
 return ''.join(out)
solved=tuple(range(54));source=replay(solved,parse_word(SRC))
assert stdstr(source)==FACE and replay(source,parse_word(WIT))==solved
def check(raw):
 seq=[];note=None
 for t in raw.strip().split():
  if re.fullmatch(r'[URFDLB][123]',t):seq.append(3*F.index(t[0])+int(t[1])-1)
  elif re.fullmatch(r'\(\d+f\*?\)',t):assert note is None;note=t
  else:raise ValueError('untrusted optimal solver text: '+t)
 assert note is not None and len(seq)==int(re.fullmatch(r'\((\d+)f\*?\)',note).group(1))
 assert replay(source,seq)==solved, 'NOT a correct solution of original 54-sticker source'
 return {'length':len(seq),'actual_54_sticker_solution':True,'solver_note_not_independently_optimality_verified':note,'solution':' '.join(F[a//3]+('', '2', "'")[a%3] for a in seq)}
def selftest():
 text=' '.join(F[a//3]+str(a%3+1) for a in parse_word(WIT))+' (18f*)'
 assert check(text)['length']==18
 rng=random.Random(20261019)
 for _ in range(4000):
  state=replay(solved,[rng.randrange(18) for _ in range(rng.randrange(28))]);face=stdstr(state)
  assert all(face.count(f)==9 for f in F)
 for bad in ('U1 U1 (2f*)','X1 (1f*)','F1 U1 (1f*)'):
  try:check(bad)
  except (ValueError,AssertionError):pass
  else:raise RuntimeError('negative control accepted')
 print('P9_FACELET_ADAPTER_AND_54_PHYSICAL_CONTRACT_PASS',FACE,flush=True)
if __name__=='__main__':
 selftest()
 if '--selftest' in sys.argv:sys.exit(0)
 import optimal.solver as solver
 raw=solver.solve(FACE)
 print('P9_EXTERNAL_OPTIMAL_SOLVER_UNVERIFIED_RAW_OUTPUT',repr(raw),flush=True)
 print('P9_EXTERNAL_OPTIMAL_SOLVER_54_SITE_WITNESS_PASS',json.dumps(check(raw),sort_keys=True),flush=True)
