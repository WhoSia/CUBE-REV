#!/usr/bin/env python3
import argparse,csv,json,pathlib,random
from collections import defaultdict

N=18
PARTS=(4,5,6,10)

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(xs): return sum(xs)/len(xs) if xs else None
def MED(xs):
    if not xs:return None
    y=sorted(xs);m=len(y)//2
    return y[m] if len(y)%2 else (y[m-1]+y[m])/2
def qbin(pi,mx,bins):
    if mx<=0:return 0
    p=pi/mx
    return min(bins-1,max(0,int(p*bins))) if p<1 else bins-1
def cells(r): return (r["l"],r["k"]-r["l"],r["d"]-r["l"],N-r["k"]-r["d"]+r["l"])
def du(a,b): return sum(abs(x-y) for x,y in zip(cells(a),cells(b)))/2.0
def sf(v,n,seed):
    if not v:return None
    obs=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        z=M([x*(1 if g.random()<.5 else -1) for x in v])
        if abs(z)>=obs-1e-15:e+=1
    return (e+1)/(n+1)
def stat(vals,n,seed):
    return {"n_solves":len(vals),"mean":M(vals),"median":MED(vals),
      "positive":sum(x>0 for x in vals),"zero":sum(x==0 for x in vals),
      "negative":sum(x<0 for x in vals),"signflip_p":sf(vals,n,seed)}
def residual(rows,bins,nperm,seed):
    by=defaultdict(list)
    for r in rows:by[(r["sid"],qbin(r["pi"],r["maxpi"],bins))].append(r)
    per=defaultdict(list)
    for (sid,q),grp in by.items():
        ts=[r for r in grp if r["lb"]==7]; cs=[r for r in grp if r["lb"] in (6,8)]
        if not ts or not cs:continue
        for t in ts:
            cand=[c for c in cs if du(t,c)<=1.0+1e-15]
            if cand:per[sid].append(t["ex"]-M([c["ex"] for c in cand]))
    vals={sid:M(xs) for sid,xs in per.items() if xs}
    out=stat(list(vals.values()),nperm,seed)
    out["eligible_solve_ids"]=sorted(vals);out["per_solve_delta"]={str(k):v for k,v in sorted(vals.items())}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True);ap.add_argument("--context",required=True)
    ap.add_argument("--out",required=True);ap.add_argument("--permutations",type=int,default=100000)
    z=ap.parse_args()
    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    shell={}
    with open(z.shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            shell[(int(x["source_id"]),int(x["prefix_index"]))]={"lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),"desc":S(x["desc_actions"])}
    maxpi=defaultdict(int)
    for (sid,pi),c in ctx.items():
        if c.get("next_action_index") is not None:maxpi[sid]=max(maxpi[sid],pi)
    rows=[]
    with open(z.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"])
            c=ctx[(sid,pi)];sh=shell[(sid,pi)]
            if a<0 or c.get("next_action_index") is None or sh["g1"] or sh["lb"] not in (6,7,8):continue
            rivals={r:S(x[r.lower()+"_best"]) for r in ("H1","H2","H3","FS")}
            ts=S(x["ts_best"]);low={m for m in ts if sum(m in rivals[r] for r in rivals)<=2}
            if not low:continue
            rows.append({"sid":sid,"pi":pi,"maxpi":maxpi[sid],"lb":sh["lb"],"k":len(low),"d":len(sh["desc"]),"l":len(low&sh["desc"]),
              "ex":(1 if a in low else 0)-len(low)/N,
              "method":c.get("method_family") or "NULL","cell":c.get("sampling_cell") or "NULL","cohort":c.get("cohort") or "NULL"})
    if len({r["sid"] for r in rows})!=80:raise SystemExit("FRESH80_SOLVES_REQUIRED")

    pooled={};methods={};cellsout={};batches={}
    for i,q in enumerate(PARTS):
        pooled[str(q)]=residual(rows,q,z.permutations,20273000+i)
        methods[str(q)]={}
        for j,m in enumerate(("CFOP","NONCFOP")):
            methods[str(q)][m]=residual([r for r in rows if r["method"]==m],q,z.permutations,20273100+i*10+j)
    for j,c in enumerate(sorted({r["cell"] for r in rows})):
        cellsout[c]=residual([r for r in rows if r["cell"]==c],5,z.permutations,20273200+j)
    for j,b in enumerate(sorted({r["cohort"] for r in rows})):
        batches[b]=residual([r for r in rows if r["cohort"]==b],5,z.permutations,20273300+j)

    # Frozen support and predictions
    cf=methods["5"]["CFOP"];nf=methods["5"]["NONCFOP"];pq5=pooled["5"]
    support_limited=False
    pred={}
    if cf["n_solves"]<20 or nf["n_solves"]<20:
        pred["method_sign_divergence"]={"evaluable":False,"pass":None};support_limited=True
    else:
        gap=nf["mean"]-cf["mean"]
        pred["method_sign_divergence"]={"evaluable":True,"pass":cf["mean"]<0 and nf["mean"]>0 and gap>=1/18-1e-15,"gap":gap}
    if pq5["n_solves"]<40:
        pred["q5_composition_cancellation"]={"evaluable":False,"pass":None};support_limited=True
    else:
        rhs=.5*((abs(cf["mean"])+abs(nf["mean"]))/2)
        pred["q5_composition_cancellation"]={"evaluable":True,"pass":abs(pq5["mean"])<=rhs+1e-15,"lhs":abs(pq5["mean"]),"rhs":rhs}
    diffs={}
    ok=0;all_support=True
    for q in ("4","6","10"):
        if pooled[q]["n_solves"]<30:all_support=False
        d=abs(pooled[q]["mean"]-pq5["mean"]) if pooled[q]["mean"] is not None and pq5["mean"] is not None else None
        diffs[q]=d
        if pooled[q]["n_solves"]>=30 and d is not None and d>=1/36-1e-15:ok+=1
    if not all_support:
        pred["progress_fragility"]={"evaluable":False,"pass":None,"differences":diffs};support_limited=True
    else:
        pred["progress_fragility"]={"evaluable":True,"pass":ok>=2,"differences":diffs,"qualifying_count":ok}

    if support_limited:
        verdict="SUPPORT_LIMITED"
    else:
        n=sum(1 for v in pred.values() if v["pass"])
        verdict="REPLICATED_HETEROGENEITY" if n==3 else ("PARTIAL_REPLICATION" if n in (1,2) else "NOT_REPLICATED")

    report={
      "schema_version":"g7-p13-fresh80-method-progress-replication-1",
      "operation_type":"Fresh Method×Progress Heterogeneity Replication Readout",
      "fresh_only":True,"prior100_pooled":False,"r1_reselected":False,"solves":80,
      "pooled_by_progress":pooled,"method_by_progress":methods,
      "q5_by_sampling_cell":cellsout,"q5_by_batch":batches,
      "primary_predictions":pred,"verdict":verdict,
      "boundary":[
        "Fresh80 terminal verdict is formed before any pooling with the prior100.",
        "R1 caliper and progress partitions are fixed from the P13 constitution.",
        "Secondary cell/batch readouts cannot redefine primary success.",
        "No method label or computational geometry is interpreted as a latent cognitive state."
      ]
    }
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"fresh80-method-progress-replication.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P13_FRESH80_ANALYSIS_PASS")
    print("POOLED",json.dumps(pooled,sort_keys=True))
    print("METHODS",json.dumps(methods,sort_keys=True))
    print("PREDICTIONS",json.dumps(pred,sort_keys=True))
    print("VERDICT",verdict)
if __name__=="__main__":main()
