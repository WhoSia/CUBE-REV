#!/usr/bin/env python3
import argparse,csv,json,pathlib,random
from collections import defaultdict
N=18
def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(xs): return sum(xs)/len(xs) if xs else None
def MED(xs):
    if not xs:return None
    y=sorted(xs);m=len(y)//2
    return y[m] if len(y)%2 else (y[m-1]+y[m])/2
def qbin(pi,mx):
    if mx<=0:return 0
    p=pi/mx
    return min(4,max(0,int(p*5))) if p<1 else 4
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
def residual(rows,nperm,seed):
    by=defaultdict(list)
    for r in rows:by[(r["sid"],qbin(r["pi"],r["maxpi"]))].append(r)
    per=defaultdict(list)
    for (sid,q),grp in by.items():
      ts=[r for r in grp if r["lb"]==7];cs=[r for r in grp if r["lb"] in (6,8)]
      if not ts or not cs:continue
      for t in ts:
        cand=[c for c in cs if du(t,c)<=1+1e-15]
        if cand:per[sid].append(t["ex"]-M([c["ex"] for c in cand]))
    vals={sid:M(v) for sid,v in per.items() if v}
    out=stat(list(vals.values()),nperm,seed);out["eligible_solve_ids"]=sorted(vals)
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
        sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"]);c=ctx[(sid,pi)];sh=shell[(sid,pi)]
        if a<0 or c.get("next_action_index") is None or sh["g1"] or sh["lb"] not in (6,7,8):continue
        rivals={r:S(x[r.lower()+"_best"]) for r in ("H1","H2","H3","FS")}
        ts=S(x["ts_best"]);low={m for m in ts if sum(m in rivals[r] for r in rivals)<=2}
        if not low:continue
        rows.append({"sid":sid,"pi":pi,"maxpi":maxpi[sid],"lb":sh["lb"],"k":len(low),"d":len(sh["desc"]),"l":len(low&sh["desc"]),
          "ex":(1 if a in low else 0)-len(low)/N,"method":c.get("method_family"),"band":c.get("reconstructor_frequency_band"),
          "era":c.get("selection_era"),"cell":c.get("sampling_cell"),"batch":c.get("cohort")})
    if len({r["sid"] for r in rows})!=80:raise SystemExit("CONFIRM80_SOLVES_REQUIRED")
    out={}
    out["band"]={b:residual([r for r in rows if r["band"]==b],z.permutations,20274000+i) for i,b in enumerate(("DOMINANT","NONDOMINANT"))}
    out["method_band"]={}
    for mi,m in enumerate(("CFOP","NONCFOP")):
      out["method_band"][m]={b:residual([r for r in rows if r["method"]==m and r["band"]==b],z.permutations,20274100+mi*10+i) for i,b in enumerate(("DOMINANT","NONDOMINANT"))}
    out["era_band"]={}
    eras=sorted({r["era"] for r in rows})
    for ei,e in enumerate(eras):
      out["era_band"][e]={b:residual([r for r in rows if r["era"]==e and r["band"]==b],z.permutations,20274200+ei*10+i) for i,b in enumerate(("DOMINANT","NONDOMINANT"))}
    out["pooled"]=residual(rows,z.permutations,20274300)
    out["batch"]={b:residual([r for r in rows if r["batch"]==b],z.permutations,20274400+i) for i,b in enumerate(sorted({r["batch"] for r in rows}))}

    pred={};support_limited=False
    d=out["band"]["DOMINANT"];n=out["band"]["NONDOMINANT"]
    if d["n_solves"]<20 or n["n_solves"]<20:
      pred["reconstructor_band_sign_separation"]={"evaluable":False,"pass":None};support_limited=True
    else:
      gap=d["mean"]-n["mean"];pred["reconstructor_band_sign_separation"]={"evaluable":True,"pass":d["mean"]>0 and n["mean"]<0 and gap>=1/18-1e-15,"gap":gap}
    method_detail={};m_ok=True
    gaps=[]
    for m in ("CFOP","NONCFOP"):
      dd=out["method_band"][m]["DOMINANT"];nn=out["method_band"][m]["NONDOMINANT"]
      if dd["n_solves"]<8 or nn["n_solves"]<8:
        method_detail[m]={"evaluable":False};m_ok=False;support_limited=True
      else:
        g=dd["mean"]-nn["mean"];gaps.append(g);method_detail[m]={"evaluable":True,"gap":g}
    if not m_ok:pred["method_invariant_band_direction"]={"evaluable":False,"pass":None,"methods":method_detail}
    else:
      pred["method_invariant_band_direction"]={"evaluable":True,"pass":all(g>0 for g in gaps) and all(g>=1/36-1e-15 for g in gaps) and any(g>=1/18-1e-15 for g in gaps),"methods":method_detail}
    positive=0;large=0;era_detail={};era_eval=True
    for e in eras:
      dd=out["era_band"][e]["DOMINANT"];nn=out["era_band"][e]["NONDOMINANT"]
      if dd["n_solves"]<5 or nn["n_solves"]<5:
        era_detail[e]={"evaluable":False};era_eval=False;support_limited=True
      else:
        g=dd["mean"]-nn["mean"];era_detail[e]={"evaluable":True,"gap":g};positive+=g>0;large+=g>=1/18-1e-15
    pred["within_era_band_transport"]={"evaluable":era_eval,"pass":(positive>=3 and large>=2) if era_eval else None,"positive_eras":positive,"large_eras":large,"eras":era_detail}
    if support_limited:verdict="SUPPORT_LIMITED"
    else:
      k=sum(1 for v in pred.values() if v["pass"])
      verdict="CONFIRMED_RECONSTRUCTOR_BAND_COORDINATE" if k==3 else ("PARTIAL_CONFIRMATION" if k==2 else "NOT_CONFIRMED")
    report={"schema_version":"g7-p14-confirm80-terminal-1","operation_type":"Independent Composition-Coordinate Confirmation Campaign Readout",
      "fresh_only":True,"prior_development_samples_pooled":False,"r1_reselected":False,"q5_fixed":True,"solves":80,
      "readouts":out,"primary_predictions":pred,"verdict":verdict,
      "boundary":["Reconstructor band is a corpus/composition coordinate, not cognition.","Interaction secondary readouts cannot rescue failed primary predictions.","No causal/mechanism promotion."]}
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"confirm80-reconstructor-band.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P14_CONFIRM80_ANALYSIS_PASS");print("BAND",json.dumps(out["band"],sort_keys=True));print("METHOD_BAND",json.dumps(out["method_band"],sort_keys=True));print("ERA_BAND",json.dumps(out["era_band"],sort_keys=True));print("PREDICTIONS",json.dumps(pred,sort_keys=True));print("VERDICT",verdict)
if __name__=="__main__":main()
