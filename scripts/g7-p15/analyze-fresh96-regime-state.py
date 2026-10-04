#!/usr/bin/env python3
import argparse,csv,json,pathlib,random
from collections import defaultdict

N=18
ERAS=("E1_2013_2016_OR_EARLIER","E2_2017_2020","E3_2021_2024","E4_2025_2026")
EARLY=set(ERAS[:2]);LATE=set(ERAS[2:])
METHODS=("CFOP","NONCFOP");BANDS=("DOMINANT","NONDOMINANT")

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
    out=stat(list(vals.values()),nperm,seed)
    out["eligible_solve_ids"]=sorted(vals)
    out["per_solve_delta"]={str(k):v for k,v in sorted(vals.items())}
    return out
def sign(x):
    if x is None:return None
    return 1 if x>0 else (-1 if x<0 else 0)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True)
    ap.add_argument("--shell",required=True)
    ap.add_argument("--context",required=True)
    ap.add_argument("--preseal",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--permutations",type=int,default=100000)
    z=ap.parse_args()

    pre=json.load(open(z.preseal,encoding="utf-8"))
    if pre.get("status")!="FROZEN_BEFORE_ANY_P15_GEOMETRY":raise SystemExit("PRESEAL_NOT_FROZEN")

    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    shell={}
    with open(z.shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            shell[(int(x["source_id"]),int(x["prefix_index"]))]={
              "lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),"desc":S(x["desc_actions"])
            }
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
            rows.append({
              "sid":sid,"pi":pi,"maxpi":maxpi[sid],"lb":sh["lb"],
              "k":len(low),"d":len(sh["desc"]),"l":len(low&sh["desc"]),
              "ex":(1 if a in low else 0)-len(low)/N,
              "method":c.get("method_family"),
              "band":c.get("reconstructor_frequency_band"),
              "era":c.get("selection_era"),
              "cell":c.get("sampling_cell"),
              "batch":c.get("cohort")
            })
    if len({r["sid"] for r in rows})!=96:raise SystemExit("FRESH96_SOLVES_REQUIRED")

    out={}
    out["pooled"]=residual(rows,z.permutations,20275000)
    out["era"]={e:residual([r for r in rows if r["era"]==e],z.permutations,20275100+i) for i,e in enumerate(ERAS)}
    out["era_band"]={}
    for ei,e in enumerate(ERAS):
        out["era_band"][e]={b:residual([r for r in rows if r["era"]==e and r["band"]==b],z.permutations,20275200+ei*10+bi) for bi,b in enumerate(BANDS)}
    out["method"]={m:residual([r for r in rows if r["method"]==m],z.permutations,20275300+i) for i,m in enumerate(METHODS)}
    out["band"]={b:residual([r for r in rows if r["band"]==b],z.permutations,20275400+i) for i,b in enumerate(BANDS)}
    out["early"]=residual([r for r in rows if r["era"] in EARLY],z.permutations,20275500)
    out["late"]=residual([r for r in rows if r["era"] in LATE],z.permutations,20275501)
    out["leave_one_era"]={e:residual([r for r in rows if r["era"]!=e],z.permutations,20275600+i) for i,e in enumerate(ERAS)}
    out["method_era"]={}
    for mi,m in enumerate(METHODS):
        out["method_era"][m]={e:residual([r for r in rows if r["method"]==m and r["era"]==e],z.permutations,20275700+mi*10+ei) for ei,e in enumerate(ERAS)}
    out["cell"]={c:residual([r for r in rows if r["cell"]==c],z.permutations,20275800+i) for i,c in enumerate(sorted({r["cell"] for r in rows}))}
    out["batch"]={b:residual([r for r in rows if r["batch"]==b],z.permutations,20275900+i) for i,b in enumerate(sorted({r["batch"] for r in rows}))}

    support_limited=False
    regime={};era_gaps={};era_eval=True;sign_matches=0
    for e in ERAS:
        d=out["era_band"][e]["DOMINANT"];n=out["era_band"][e]["NONDOMINANT"]
        if d["n_solves"]<8 or n["n_solves"]<8 or d["mean"] is None or n["mean"] is None:
            era_gaps[e]={"evaluable":False};era_eval=False;support_limited=True
        else:
            g=d["mean"]-n["mean"];era_gaps[e]={"evaluable":True,"gap":g}
            if (e in EARLY and g>0) or (e in LATE and g<0):sign_matches+=1

    if era_eval:
        eg=M([era_gaps[ERAS[0]]["gap"],era_gaps[ERAS[1]]["gap"]])
        lg=M([era_gaps[ERAS[2]]["gap"],era_gaps[ERAS[3]]["gap"]])
        regime["early_mean_gap_positive"]={"evaluable":True,"pass":eg>0,"value":eg}
        regime["late_mean_gap_negative"]={"evaluable":True,"pass":lg<0,"value":lg}
        regime["early_minus_late_gap"]={"evaluable":True,"pass":eg-lg>=1/18-1e-15,"value":eg-lg}
        regime["era_sign_pattern"]={"evaluable":True,"pass":sign_matches>=3,"matching_eras":sign_matches,"era_gaps":era_gaps}
    else:
        for k in ("early_mean_gap_positive","late_mean_gap_negative","early_minus_late_gap","era_sign_pattern"):
            regime[k]={"evaluable":False,"pass":None}
        regime["era_sign_pattern"]["era_gaps"]=era_gaps

    state={}
    early=out["early"];late=out["late"]
    if early["n_solves"]<20 or late["n_solves"]<20 or early["mean"] is None or late["mean"] is None:
        state["early_late_pooled_invariance"]={"evaluable":False,"pass":None};support_limited=True
    else:
        diff=early["mean"]-late["mean"]
        state["early_late_pooled_invariance"]={"evaluable":True,"pass":abs(diff)<=1/36+1e-15,"difference":diff}

    loo=out["leave_one_era"];loo_ok=True;loo_signs={}
    for e in ERAS:
        x=loo[e]
        if x["n_solves"]<20 or x["mean"] is None:
            loo_ok=False;support_limited=True;loo_signs[e]=None
        else:loo_signs[e]=sign(x["mean"])
    if not loo_ok:
        state["leave_one_era_sign_invariance"]={"evaluable":False,"pass":None,"signs":loo_signs}
    else:
        ss=list(loo_signs.values())
        state["leave_one_era_sign_invariance"]={"evaluable":True,"pass":all(v==ss[0] and v!=0 for v in ss),"signs":loo_signs}

    m1=out["method"]["CFOP"];m2=out["method"]["NONCFOP"]
    b1=out["band"]["DOMINANT"];b2=out["band"]["NONDOMINANT"]
    marginal_eval=(m1["n_solves"]>=20 and m2["n_solves"]>=20 and b1["n_solves"]>=20 and b2["n_solves"]>=20 and
                   None not in (m1["mean"],m2["mean"],b1["mean"],b2["mean"]))
    if not marginal_eval:
        state["small_marginal_gaps"]={"evaluable":False,"pass":None};support_limited=True
    else:
        mg=m1["mean"]-m2["mean"];bg=b1["mean"]-b2["mean"]
        state["small_marginal_gaps"]={"evaluable":True,"pass":abs(mg)<1/18+1e-15 and abs(bg)<1/18+1e-15,
          "method_gap":mg,"band_gap":bg}

    if support_limited:
        verdict="SUPPORT_LIMITED"
    else:
        rp=[v["pass"] for v in regime.values() if "pass" in v]
        sp=[v["pass"] for v in state.values() if "pass" in v]
        regime_full=all(rp) and len(rp)==4
        state_full=all(sp) and len(sp)==3
        if regime_full and not state["early_late_pooled_invariance"]["pass"]:
            verdict="REGIME_CONFIRMED"
        elif state_full and not regime_full:
            verdict="STATE_LOCAL_TRANSPORT"
        else:
            passes=sum(bool(v) for v in rp+sp)
            if passes>0:
                verdict="MIXED_OR_PARTIAL"
            else:
                verdict="NONSTATIONARY_MIXTURE_SUPPORTED"

    report={
      "schema_version":"g7-p15-fresh96-terminal-1",
      "operation_type":"Naturalistic Residual Nonstationarity Confirmation Campaign Readout",
      "fresh_only":True,
      "prior_corpora_pooled":False,
      "r1_reselected":False,
      "q5_fixed":True,
      "solves":96,
      "readouts":out,
      "H_REGIME_STEP":regime,
      "H_STATE_LOCAL":state,
      "verdict":verdict,
      "boundary":[
        "Era/method/reconstructor are archive coordinates, not causal or cognitive states.",
        "Secondary cell/batch/method-era readouts cannot rescue a failed primary package.",
        "Fresh96 terminal verdict is formed before prior-corpus pooling.",
        "No human mechanism promotion."
      ]
    }
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"fresh96-regime-state-terminal.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P15_FRESH96_ANALYSIS_PASS")
    print("REGIME",json.dumps(regime,sort_keys=True))
    print("STATE",json.dumps(state,sort_keys=True))
    print("EARLY",json.dumps(out["early"],sort_keys=True))
    print("LATE",json.dumps(out["late"],sort_keys=True))
    print("METHOD",json.dumps(out["method"],sort_keys=True))
    print("BAND",json.dumps(out["band"],sort_keys=True))
    print("ERA_BAND",json.dumps(out["era_band"],sort_keys=True))
    print("VERDICT",verdict)

if __name__=="__main__":main()
