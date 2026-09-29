import hashlib,json
C=[
 ("constant",0,lambda x:0),
 ("first_bit",1,lambda x:x&1),
 ("parity",2,lambda x:x.bit_count()&1),
 ("hamming_weight",3,lambda x:x.bit_count()),
 ("identity",4,lambda x:x),
]
def parity(x): return x.bit_count()&1
def support(spurious):
 out=[]
 for n in range(2,6):
  for x in range(1<<n):
   if spurious and (x&1)!=parity(x): continue
   out.append((n,x,parity(x)))
 return out
def fit(data):
 scored=[]
 for name,cost,enc in C:
  err=sum(enc(x)!=y for _,x,y in data)
  scored.append((err,cost,name,enc))
 return sorted(scored,key=lambda z:(z[0],z[1],z[2]))[0]
def held(name,enc):
 fail=[]; dig={}
 for n in range(6,13):
  labels=[enc(x) for x in range(1<<n)]
  bad=next((x for x,a in enumerate(labels) if a!=parity(x)),None)
  if bad is not None: fail.append({"n":n,"x":bad})
  dig[str(n)]=hashlib.sha256(",".join(map(str,labels)).encode()).hexdigest()
 return {"model":name,"pass":not fail,"failures":fail,"partition_sha256":dig}
full=fit(support(False)); spur=fit(support(True))
fr=held(full[2],full[3]); sr=held(spur[2],spur[3])
assert full[0]==0 and full[2]=="parity" and fr["pass"]
assert spur[0]==0 and spur[2]=="first_bit" and not sr["pass"] and sr["failures"][0]["x"]==2
print(json.dumps({
 "schema":"cube-rev.g5-p3.learned-quotient.v1",
 "authority":"MODEL_DEPENDENT_ORACLE_FIRST",
 "candidate_grammar":[x[0] for x in C],
 "training_ns":[2,3,4,5],
 "full_support":{"selected":full[2],"training_errors":full[0],"heldout":fr},
 "spurious_support":{"selected":spur[2],"training_errors":spur[0],"heldout":sr},
 "verdict":"LEARNED_QUOTIENT_GENERALIZATION_IS_SUPPORT_DEPENDENT",
 "claim_ceiling":"finite candidate grammar; no embedding-geometry or human claim",
},sort_keys=True,separators=(",",":")))
