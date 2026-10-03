#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random
from collections import defaultdict

N=18
PARENT={"FRESH40":0.056231231231231235,"LEGACY60":0.048695054945054946}

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(xs): return sum(xs)/len(xs) if xs else None
def MED(xs):
    if not xs:return None
    y=sorted(xs);m=len(y)//2
    return y[m] if len(y)%2 else (y[m-1]+y[m])/2
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
def qbin(pi,mx,bins):
    if mx<=0:return 0
    p=pi/mx
    return min(bins-1,max(0,int(p*bins))) if p<1 else bins-1
def cells(r): return (r["l"],r["k"]-r["l"],r["d"]-r["l"],N-r["k"]-r["d"]+r["l"])
def du(a,b): return sum(abs(x-y) for x,y in zip(cells(a),cells(b)))/2.0

def residual(rows,bins=5,edge_included=True,aggregation="target",nperm=100000,seed=1,override=None):
    by=defaultdict(list)
    for r in rows:
        q=qbin(r["pi"],r["maxpi"],bins)
        rr=dict(r);rr["qv"]=q
        by[(r["sid"],q)].append(rr)
    solve_q=defaultdict(list)
    for (sid,q),grp in by.items():
        def lab(r): return override.get((r["sid"],r["pi"]),r["lb"]) if override else r["lb"]
        ts=[r for r in grp if lab(r)==7]
        cs=[r for r in grp if lab(r) in (6,8)]
        if not ts or not cs:continue
        deltas=[]
        for t in ts:
            cand=[c for c in cs if (du(t,c)<=1.0+1e-15 if edge_included else du(t,c)<1.0-1e-15)]
            if not cand:continue
            deltas.append(t["ex"]-M([c["ex"] for c in cand]))
        if deltas: solve_q[sid].append((q,deltas))
    vals={}
    for sid,qsets in solve_q.items():
        if aggregation=="target":
            allv=[x for _,ds in qsets for x in ds]
            vals[sid]=M(allv)
        else:
            vals[sid]=M([M(ds) for _,ds in qsets])
    out=stat(list(vals.values()),nperm,seed)
    out["eligible_solve_ids"]=sorted(vals)
    out["abs_ratio_to_parent"]=None
    return out

def rotated_labels(rows,bins):
    by=defaultdict(list);out={}
    for r in rows:by[(r["sid"],qbin(r["pi"],r["maxpi"],bins))].append(r)
    for key,grp in by.items():
        grp=sorted(grp,key=lambda r:r["pi"]);labs=[r["lb"] for r in grp]
        rot=labs[1:]+labs[:1] if len(labs)>1 else labs
        for r,l in zip(grp,rot):out[(r["sid"],r["pi"])]=l
    return out

def attenuated(x,parent,support_floor):
    return x["n_solves"]>=support_floor and x["mean"] is not None and abs(x["mean"])<=0.5*abs(parent)

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
                         "ancestry":"FRESH40" if str(c.get("cohort") or "").startswith("P11_") else "LEGACY60",
                         "cohort":c.get("cohort") or "NULL","method":c.get("method_family") or "NULL","cell":c.get("sampling_cell") or "NULL"})
    scopes={a:[r for r in rows if r["ancestry"]==a] for a in ("FRESH40","LEGACY60")}
    variants=[
      ("BASE_Q5_TARGET_EQUAL",5,True,"target"),
      ("Q4_TARGET_EQUAL",4,True,"target"),
      ("Q6_TARGET_EQUAL",6,True,"target"),
      ("Q10_TARGET_EQUAL",10,True,"target"),
      ("Q5_STRATUM_EQUAL",5,True,"stratum"),
      ("Q5_EDGE_EXCLUDED",5,False,"target")]
    outv={}
    seed=20271600
    for anc,rs in scopes.items():
        outv[anc]={}
        for i,(name,bins,edge,agg) in enumerate(variants):
            x=residual(rs,bins,edge,agg,z.permutations,seed+i+(0 if anc=="FRESH40" else 100))
            x["abs_ratio_to_parent"]=abs(x["mean"])/abs(PARENT[anc]) if x["mean"] is not None else None
            x["attenuated"]=attenuated(x,PARENT[anc],15 if anc=="FRESH40" else 25)
            outv[anc][name]=x
    # exact base reproduction
    if abs(outv["FRESH40"]["BASE_Q5_TARGET_EQUAL"]["mean"]-(-0.0014245014245014228))>1e-12:raise SystemExit("R3_FRESH_BASE_REPRO_FAIL")
    if abs(outv["LEGACY60"]["BASE_Q5_TARGET_EQUAL"]["mean"]-0.018244949494949494)>1e-12:raise SystemExit("R3_LEGACY_BASE_REPRO_FAIL")

    # subgroup / leave-out stress using BASE
    transport={"FRESH40":{},"LEGACY60":{}}
    fresh=scopes["FRESH40"];legacy=scopes["LEGACY60"]
    for cohort in sorted({r["cohort"] for r in fresh}):
        x=residual([r for r in fresh if r["cohort"]!=cohort],5,True,"target",z.permutations,20271700+len(transport["FRESH40"]))
        x["excluded"]=cohort;transport["FRESH40"]["leave_out_"+cohort]=x
    for method in sorted({r["method"] for r in fresh}):
        transport["FRESH40"]["method_"+method]=residual([r for r in fresh if r["method"]==method],5,True,"target",z.permutations,20271800+len(transport["FRESH40"]))
    for cell in sorted({r["cell"] for r in fresh}):
        transport["FRESH40"]["cell_"+cell]=residual([r for r in fresh if r["cell"]==cell],5,True,"target",z.permutations,20271900+len(transport["FRESH40"]))
    for method in sorted({r["method"] for r in legacy}):
        transport["LEGACY60"]["method_"+method]=residual([r for r in legacy if r["method"]==method],5,True,"target",z.permutations,20272000+len(transport["LEGACY60"]))
    lcoh=sorted({r["cohort"] for r in legacy})
    for cohort in lcoh:
        x=residual([r for r in legacy if r["cohort"]!=cohort],5,True,"target",z.permutations,20272100+len(transport["LEGACY60"]))
        x["excluded"]=cohort;transport["LEGACY60"]["leave_out_"+cohort]=x

    # negative controls BASE/Q4/Q6/Q10
    neg={}
    for anc,rs in scopes.items():
        neg[anc]={}
        for i,(name,bins,edge,agg) in enumerate(variants[:4]):
            rot=rotated_labels(rs,bins)
            base=residual(rs,bins,True,"target",z.permutations,20272200+i,rot)
            neg[anc][name]=base

    fresh_alt=["Q4_TARGET_EQUAL","Q6_TARGET_EQUAL","Q10_TARGET_EQUAL","Q5_STRATUM_EQUAL"]
    legacy_alt=fresh_alt
    fa=sum(outv["FRESH40"][k]["attenuated"] for k in fresh_alt)
    la=sum(outv["LEGACY60"][k]["attenuated"] for k in legacy_alt)
    loo_bad=0
    for k,x in transport["FRESH40"].items():
        if k.startswith("leave_out_") and x["n_solves"]>=15 and x["mean"] is not None and abs(x["mean"])>abs(PARENT["FRESH40"]):
            loo_bad+=1
    fresh_fail=sum((outv["FRESH40"][k]["n_solves"]>=15 and not outv["FRESH40"][k]["attenuated"]) for k in fresh_alt)
    if fa>=3 and la>=3 and loo_bad==0:
        verdict="R1_ATTENUATION_ROBUST_ACROSS_PRESEALED_PERTURBATIONS"
    elif fresh_fail>=2:
        verdict="R1_ATTENUATION_FRAGILE_UNDER_PRESEALED_PERTURBATIONS"
    else:
        verdict="R1_ATTENUATION_MIXED_ROBUSTNESS"

    report={"schema_version":"g7-p12-r4-fixed-r1-robustness-1",
      "operation_type":"Structural-Attenuation Robustness Stress Test",
      "independent_replication":False,"r1_reselected":False,
      "variant_results":outv,"transport_slices":transport,"negative_controls":neg,
      "summary":{"fresh_attenuated_alt_count":fa,"legacy_attenuated_alt_count":la,"fresh_leave_out_parent_exceed_count":loo_bad},
      "verdict":verdict,
      "boundary":["Post-result robustness analysis, not independent confirmation.","R1 fixed throughout.","Subgroup readouts are diagnostics only.","No causal or cognitive mechanism promotion."]}
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"fixed-r1-robustness-stress.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P12_R4_ROBUSTNESS_STRESS_PASS")
    print("VARIANTS",json.dumps(outv,sort_keys=True))
    print("SUMMARY",json.dumps(report["summary"],sort_keys=True))
    print("TRANSPORT",json.dumps(transport,sort_keys=True))
    print("VERDICT",verdict)
if __name__=="__main__":main()
