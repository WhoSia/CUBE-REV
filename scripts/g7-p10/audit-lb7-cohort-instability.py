#!/usr/bin/env python3
import argparse,csv,json,pathlib,statistics
from collections import defaultdict,Counter

R=("H1","H2","H3","FS")
C={x:x.lower()+"_best" for x in R}; C["TS"]="ts_best"; N=18
FOCAL="P7_BATCH4"

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(xs): return sum(xs)/len(xs) if xs else None
def qbin(p): return min(4,max(0,int(p*5))) if p<1 else 4
def tvd(a,b):
    ks=set(a)|set(b)
    return 0.5*sum(abs(a.get(k,0)-b.get(k,0)) for k in ks)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True)
    ap.add_argument("--context",required=True)
    ap.add_argument("--out",required=True)
    z=ap.parse_args()

    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x

    maxpi=defaultdict(int)
    feat_rows=[]
    with open(z.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="	"):
            sid=int(x["source_id"]); pi=int(x["prefix_index"]); a=int(x["next_action"])
            if a<0: continue
            maxpi[sid]=max(maxpi[sid],pi)
            feat_rows.append(x)

    raw=[]
    for x in feat_rows:
        sid=int(x["source_id"]); pi=int(x["prefix_index"]); a=int(x["next_action"])
        sets={r:S(x[C[r]]) for r in (*R,"TS")}
        low={m for m in sets["TS"] if sum(m in sets[r] for r in R)<=2}
        k=len(low)
        lb=int(x["phase1_lb"]); g1=int(x["is_g1"])
        if k==0 or g1!=0 or lb not in {6,7,8}: continue
        c=ctx[(sid,pi)]
        raw.append({
          "sid":sid,"pi":pi,"lb":lb,"k":k,
          "q":qbin(pi/maxpi[sid] if maxpi[sid]>0 else 0),
          "ex":(1 if a in low else 0)-k/N,
          "cohort":c.get("cohort") or "NULL",
          "method":c.get("method_family") or "NULL"
        })

    if not raw: raise SystemExit("NO_ELIGIBLE_ROWS")

    # R2-style exact within-solve matched delta.
    def per_solve(rows):
        st=defaultdict(lambda:{"t":[],"c":[]})
        for r in rows:
            key=(r["sid"],r["q"],r["k"])
            st[key]["t" if r["lb"]==7 else "c"].append(r["ex"])
        per=defaultdict(list)
        for key,d in st.items():
            if d["t"] and d["c"]:
                w=min(len(d["t"]),len(d["c"]))
                per[key[0]].append((M(d["t"])-M(d["c"]),w))
        out={}
        for sid,xs in per.items():
            den=sum(w for _,w in xs)
            out[sid]=sum(v*w for v,w in xs)/den
        return out

    ps=per_solve(raw)
    meta={}
    for r in raw:
        meta[r["sid"]]={"cohort":r["cohort"],"method":r["method"]}

    focal_vals=[v for sid,v in ps.items() if meta[sid]["cohort"]==FOCAL]
    other_vals=[v for sid,v in ps.items() if meta[sid]["cohort"]!=FOCAL]
    raw_focal=M(focal_vals); raw_other=M(other_vals)
    raw_diff=(raw_focal-raw_other) if raw_focal is not None and raw_other is not None else None

    # State support composition by exact (q,k) stratum.
    groups={"P7_BATCH4":defaultdict(lambda:{"t":[],"c":[]}),
            "OTHER_COHORTS":defaultdict(lambda:{"t":[],"c":[]})}
    methods=defaultdict(lambda:{"P7_BATCH4":defaultdict(lambda:{"t":[],"c":[]}),
                                "OTHER_COHORTS":defaultdict(lambda:{"t":[],"c":[]})})
    for r in raw:
        g="P7_BATCH4" if r["cohort"]==FOCAL else "OTHER_COHORTS"
        s=(r["q"],r["k"])
        groups[g][s]["t" if r["lb"]==7 else "c"].append(r["ex"])
        methods[r["method"]][g][s]["t" if r["lb"]==7 else "c"].append(r["ex"])

    def decompose(groupmap):
        common=[]
        details={}
        for s in sorted(set(groupmap["P7_BATCH4"])|set(groupmap["OTHER_COHORTS"])):
            ok=True; gd={}
            for g in ("P7_BATCH4","OTHER_COHORTS"):
                d=groupmap[g][s]
                if not d["t"] or not d["c"]: ok=False
                gd[g]=d
            if ok:
                common.append(s)
                pooled_t=len(gd["P7_BATCH4"]["t"])+len(gd["OTHER_COHORTS"]["t"])
                pooled_c=len(gd["P7_BATCH4"]["c"])+len(gd["OTHER_COHORTS"]["c"])
                w=min(pooled_t,pooled_c)
                details[str(s)]={
                  "weight":w,
                  "P7_BATCH4":{"target_n":len(gd["P7_BATCH4"]["t"]),"comp_n":len(gd["P7_BATCH4"]["c"]),
                               "delta":M(gd["P7_BATCH4"]["t"])-M(gd["P7_BATCH4"]["c"])},
                  "OTHER_COHORTS":{"target_n":len(gd["OTHER_COHORTS"]["t"]),"comp_n":len(gd["OTHER_COHORTS"]["c"]),
                                   "delta":M(gd["OTHER_COHORTS"]["t"])-M(gd["OTHER_COHORTS"]["c"])}
                }
        if not common:
            return {"common_strata":0,"details":{}}
        den=sum(details[str(s)]["weight"] for s in common)
        means={}
        exposure={}
        for g in ("P7_BATCH4","OTHER_COHORTS"):
            means[g]=sum(details[str(s)]["weight"]*details[str(s)][g]["delta"] for s in common)/den
            eg={}
            ed=0
            for s in common:
                d=groupmap[g][s]
                w=min(len(d["t"]),len(d["c"]))
                eg[str(s)]=w; ed+=w
            exposure[g]={k:(v/ed if ed else 0) for k,v in eg.items()}
        return {
          "common_strata":len(common),
          "common_stratum_keys":[list(s) for s in common],
          "common_weight_means":means,
          "common_weight_difference":means["P7_BATCH4"]-means["OTHER_COHORTS"],
          "composition_tvd":tvd(exposure["P7_BATCH4"],exposure["OTHER_COHORTS"]),
          "matched_exposure_distributions":exposure,
          "details":details
        }

    dec=decompose(groups)

    focal_n=len(focal_vals); other_n=len(other_vals)
    if dec.get("common_strata",0)<3 or focal_n<5 or other_n<5 or raw_diff is None:
        verdict="UNIDENTIFIED_COMMON_SUPPORT_TOO_SPARSE"
        shrink=None
    else:
        cd=dec["common_weight_difference"]
        shrink=(abs(cd)/abs(raw_diff)) if raw_diff!=0 else None
        if raw_diff==0:
            verdict="MIXED_NUMERICAL_EDGE"
        elif raw_diff*cd<=0 or abs(cd)<=0.5*abs(raw_diff):
            verdict="COMPOSITION_DOMINANT_COHORT_INSTABILITY"
        else:
            verdict="CONDITIONAL_CHOICE_DRIFT_PERSISTS_AFTER_STANDARDIZATION"

    method_out={}
    for m,gmap in sorted(methods.items()):
        mps={sid:v for sid,v in ps.items() if meta[sid]["method"]==m}
        fn=sum(1 for sid in mps if meta[sid]["cohort"]==FOCAL)
        on=sum(1 for sid in mps if meta[sid]["cohort"]!=FOCAL)
        d=decompose(gmap)
        d["focal_eligible_solves"]=fn; d["other_eligible_solves"]=on
        if fn>=3 and on>=3:
            fv=[v for sid,v in mps.items() if meta[sid]["cohort"]==FOCAL]
            ov=[v for sid,v in mps.items() if meta[sid]["cohort"]!=FOCAL]
            d["raw_matched_means"]={"P7_BATCH4":M(fv),"OTHER_COHORTS":M(ov)}
            d["raw_difference"]=M(fv)-M(ov)
        method_out[m]=d

    cohort_counts=Counter(r["cohort"] for r in raw)
    result={
      "schema_version":"g7-p10-r3-cohort-instability-decomposition-1",
      "operation_type":"LB7 Cohort-Instability Decomposition Audit",
      "eligible_state_rows":len(raw),
      "r2_style_eligible_solves":len(ps),
      "cohort_state_counts":dict(sorted(cohort_counts.items())),
      "raw_matched":{
        "P7_BATCH4":{"n_solves":focal_n,"mean":raw_focal},
        "OTHER_COHORTS":{"n_solves":other_n,"mean":raw_other},
        "difference":raw_diff
      },
      "common_support_standardization":dec,
      "standardized_to_raw_abs_ratio":shrink,
      "method_sensitivity":method_out,
      "verdict":verdict,
      "boundary":[
        "Cohort is acquisition ancestry, not a randomized treatment.",
        "Common-weight re-expression is descriptive standardization, not causal adjustment.",
        "The audit diagnoses whether R2 cohort sensitivity can be explained by matched-stratum composition under the frozen q×support-size grammar.",
        "Method-specific decompositions are secondary and may be support-limited.",
        "No result identifies a cognitive mechanism and no new source contact occurs."
      ]
    }
    out=pathlib.Path(z.out); out.mkdir(parents=True,exist_ok=True)
    (out/"lb7-cohort-instability-decomposition.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P10_R3_COHORT_INSTABILITY_AUDIT_PASS")
    print("RAW",json.dumps(result["raw_matched"],sort_keys=True))
    print("COMMON",json.dumps({k:v for k,v in dec.items() if k!="details"},sort_keys=True))
    print("RATIO",shrink)
    print("VERDICT",verdict)

if __name__=="__main__":
    main()
