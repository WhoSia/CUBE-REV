import csv,sys
rows=list(csv.DictReader(open(sys.argv[1],encoding="utf-8"),delimiter="\t"))
grid=[r for r in rows if r["kind"]=="grid"]
transport=[r for r in rows if r["kind"]=="transport"]
hard=[r for r in rows if r["kind"]=="hard"]
assert len(grid)==256
assert len(transport)==5
assert len(hard)==5
for r in grid:
 n=int(r["n"]); f=r["family"]
 if f=="B":
  assert r["depth"]==str(n)
  assert r["memory"]==(str(n) if r["target"]=="exact" else "1")
 elif f=="LI":
  assert r["depth"]==str(n)
 elif f=="TL":
  assert r["recoverable"]=="true" and r["depth"]=="1"
 elif f=="M2O":
  assert r["recoverable"]=="false" and r["note"]=="PERMANENT_TARGET_COLLISION"
 elif f=="E":
  assert (r["note"],int(r["external"]),int(r["internal"])) in [("raw",0,n-1),("normalized",1,0)]
 elif f=="HM":
  p=int(r["p"])
  if r["target"]=="exact":
   z=1<<(n-p); expected=(1<<p)*z*(z-1)//2
  else:
   expected=0 if p==n else 1<<(2*n-p-2)
  assert int(r["ambiguity"])==expected
  assert (r["recoverable"]=="true")== (expected==0)
assert all(r["recoverable"]=="true" for r in hard)
print("P3_INDEPENDENT_GRID_AUDIT_PASS")
