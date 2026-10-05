#!/usr/bin/env python3
import argparse,json,random,hashlib,pathlib

AXES=("method_family","reconstructor_frequency_band","selection_era")
REQ={
 "method_family":{"CFOP","NONCFOP"},
 "reconstructor_frequency_band":{"DOMINANT","NONDOMINANT"},
 "selection_era":{"E1","E2","E3","E4"},
}

def mean(xs): return sum(xs)/len(xs) if xs else None
def pct(xs,p):
    y=sorted(xs)
    if not y:return None
    k=(len(y)-1)*p; lo=int(k); hi=min(lo+1,len(y)-1); f=k-lo
    return y[lo]*(1-f)+y[hi]*f
def rng(seed):
    return random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:16],16))
def boot_diff(a,b,n,seed):
    g=rng(seed);out=[]
    for _ in range(n):
        aa=[a[g.randrange(len(a))] for __ in range(len(a))]
        bb=[b[g.randrange(len(b))] for __ in range(len(b))]
        out.append(mean(bb)-mean(aa))
    return {"p05":pct(out,.05),"p95":pct(out,.95),"mean":mean(out)}
def boot_pool(a,b,n,seed):
    x=a+b;g=rng(seed);out=[]
    for _ in range(n):
        s=[x[g.randrange(len(x))] for __ in range(len(x))]
        out.append(mean(s))
    return {"p05":pct(out,.05),"p95":pct(out,.95),"mean":mean(out)}
def norm_era(v):
    s=str(v)
    if s.startswith("E1"):return "E1"
    if s.startswith("E2"):return "E2"
    if s.startswith("E3"):return "E3"
    if s.startswith("E4"):return "E4"
    return s

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--p17",required=True);ap.add_argument("--p19",required=True)
    ap.add_argument("--preseal",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal))
    if pre["status"]!="FROZEN_BEFORE_SOLVE_LEVEL_P17_P19_HETEROGENEITY_READOUT":
        raise SystemExit("PRESEAL")
    x17=json.load(open(a.p17));x19=json.load(open(a.p19))
    s17=x17["per_solve"];s19=x19["per_solve"]
    if len(s17)!=48 or len(s19)!=48: verdict="SUPPORT_LIMITED"
    else: verdict=None
    # normalize common effect HYBRID-HAND
    a17=[]
    for r in s17:
        rr=dict(r);rr["effect"]=r["hybrid_nll"]-r["hand_nll"]
        rr["selection_era"]=norm_era(r.get("selection_era"))
        a17.append(rr)
    a19=[]
    for r in s19:
        rr=dict(r);rr["effect"]=r["hybrid_minus_hand"]
        rr["selection_era"]=norm_era(r.get("selection_era"))
        a19.append(rr)
    # support metadata
    missing=[]
    for axis in AXES:
        v17={r.get(axis) for r in a17};v19={r.get(axis) for r in a19}
        if not REQ[axis].issubset(v17) or not REQ[axis].issubset(v19): missing.append(axis)
    if missing: verdict="SUPPORT_LIMITED"

    e17=[r["effect"] for r in a17];e19=[r["effect"] for r in a19]
    diff=mean(e19)-mean(e17)
    bd=boot_diff(e17,e19,pre["bootstrap"]["repetitions"],"CUBE_REV_G7_P20_COHORT_DIFF_V1")
    bp=boot_pool(e17,e19,pre["bootstrap"]["repetitions"],"CUBE_REV_G7_P20_POOLED96_V1")
    axes={}
    coherent=[]
    sign=1 if diff>0 else (-1 if diff<0 else 0)
    for axis in AXES:
        levels=sorted(REQ[axis])
        d={}
        for lv in levels:
            r17=[r["effect"] for r in a17 if r.get(axis)==lv]
            r19=[r["effect"] for r in a19 if r.get(axis)==lv]
            d[lv]={"n17":len(r17),"n19":len(r19),"mean17":mean(r17),"mean19":mean(r19),"delta":mean(r19)-mean(r17)}
        coh=(sign!=0 and all(v["delta"]!=0 and (1 if v["delta"]>0 else -1)==sign for v in d.values()))
        axes[axis]={"levels":d,"coherent":coh}
        if coh:coherent.append(axis)
    eg=axes["selection_era"]["levels"]
    axes["selection_era"]["early_delta"]=mean([eg["E1"]["delta"],eg["E2"]["delta"]])
    axes["selection_era"]["late_delta"]=mean([eg["E3"]["delta"],eg["E4"]["delta"]])

    ci_excludes=(bd["p05"]>0 or bd["p95"]<0)
    if verdict is None:
        if ci_excludes:
            verdict="HETEROGENEITY_LOCALIZED" if len(coherent)==1 else "EFFECT_SIZE_NONSTATIONARY"
        else:
            verdict="STABLE_COMPLEMENTARITY_SURFACE" if len(coherent)==0 else "STABLE_DIRECTION_VARIABLE_MAGNITUDE"

    report={
      "schema_version":"g7-p20-heterogeneity-audit-1","phase":"G7-P20",
      "new_body_contact":0,"retrained":False,
      "cohort":{"p17_mean":mean(e17),"p19_mean":mean(e19),"difference_p19_minus_p17":diff,
                "bootstrap90":bd,"ci_excludes_zero":ci_excludes},
      "pooled_fresh96":{"mean":mean(e17+e19),"bootstrap90":bp,"authority":"DESCRIPTIVE_ONLY"},
      "axes":axes,"coherent_axes":coherent,"missing_axes":missing,"verdict":verdict,
      "boundary":[
        "Post-result heterogeneity audit; not independent confirmation.",
        "P17 generated the HYBRID successor rival, so pooled fresh96 is descriptive only.",
        "No subgroup can retroactively rescue P19 or authorize mechanism claims.",
        "No new body contact or retraining occurred."
      ]
    }
    p=pathlib.Path(a.out);p.mkdir(parents=True,exist_ok=True)
    (p/"p20-heterogeneity-audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print("G7_P20_HETEROGENEITY_AUDIT_PASS")
    print("COHORT",json.dumps(report["cohort"],sort_keys=True))
    print("POOLED96",json.dumps(report["pooled_fresh96"],sort_keys=True))
    print("COHERENT_AXES",json.dumps(coherent))
    print("AXES",json.dumps(axes,sort_keys=True))
    print("VERDICT",verdict)
if __name__=="__main__":main()
