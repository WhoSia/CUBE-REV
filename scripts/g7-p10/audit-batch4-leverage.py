#!/usr/bin/env python3
import argparse,csv,json,pathlib
from collections import defaultdict,Counter
R=("H1","H2","H3","FS");C={x:x.lower()+"_best" for x in R};C["TS"]="ts_best";N=18
def S(x):return {int(v) for v in (x or "").split(",") if v!=""}
def M(x):return sum(x)/len(x) if x else None
def qbin(p):return min(4,max(0,int(p*5))) if p<1 else 4
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--features",required=True);ap.add_argument("--context",required=True)
    ap.add_argument("--provenance",required=True);ap.add_argument("--out",required=True);z=ap.parse_args()
    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    p=json.load(open(z.provenance,encoding="utf-8"));prov={int(k):v for k,v in p["source_id_to_broad_provenance_class"].items()}
    allface=[];eligible=[]
    with open(z.features,encoding="utf-8",newline="") as f:
      for x in csv.DictReader(f,delimiter="\t"):
        sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"])
        if a<0:continue
        allface.append((sid,pi))
        sets={r:S(x[C[r]]) for r in (*R,"TS")}
        low={m for m in sets["TS"] if sum(m in sets[r] for r in R)<=2}
        if not low or int(x["is_g1"])!=0:continue
        c=ctx[(sid,pi)]
        eligible.append({"sid":sid,"pi":pi,"lb":int(x["phase1_lb"]),"k":len(low),
                         "ex":(1 if a in low else 0)-len(low)/N,
                         "cohort":c.get("cohort") or "NULL","method":c.get("method_family") or "NULL",
                         "reconstructor":c.get("reconstructor") or "NULL","provenance":prov.get(sid,"MISSING")})
    maxpi=defaultdict(int)
    for sid,pi in allface:maxpi[sid]=max(maxpi[sid],pi)
    for r in eligible:r["q"]=qbin(r["pi"]/maxpi[r["sid"]] if maxpi[r["sid"]]>0 else 0)
    meta={}
    for r in eligible:meta[r["sid"]]={k:r[k] for k in ("cohort","method","reconstructor","provenance")}

    st=defaultdict(lambda:{"t":[],"c":[]})
    for r in eligible:
        if r["lb"] not in (6,7,8):continue
        key=(r["sid"],r["q"],r["k"])
        st[key]["t" if r["lb"]==7 else "c"].append(r["ex"])
    per=defaultdict(list)
    for key,d in st.items():
        if d["t"] and d["c"]:
            w=min(len(d["t"]),len(d["c"]))
            per[key[0]].append((M(d["t"])-M(d["c"]),w))
    delta={}
    for sid,xs in per.items():
        den=sum(w for _,w in xs);delta[sid]=sum(v*w for v,w in xs)/den
    if not delta:raise SystemExit("NO_MATCHED_DELTAS")
    b4={sid:v for sid,v in delta.items() if meta[sid]["cohort"]=="P7_BATCH4"}
    oth={sid:v for sid,v in delta.items() if meta[sid]["cohort"]!="P7_BATCH4"}
    overall=M(list(delta.values()));raw_b4=M(list(b4.values()));raw_oth=M(list(oth.values()));raw_diff=raw_b4-raw_oth

    strata=defaultdict(lambda:{"b":[],"o":[]})
    for sid,v in delta.items():
        key=(meta[sid]["method"],meta[sid]["provenance"])
        strata[key]["b" if sid in b4 else "o"].append(v)
    common=[];num=den=0.0
    for key,d in sorted(strata.items()):
        if not d["b"] or not d["o"]:continue
        diff=M(d["b"])-M(d["o"]);w=min(len(d["b"]),len(d["o"]))
        common.append({"method":key[0],"provenance":key[1],"n_batch4":len(d["b"]),"n_other":len(d["o"]),
                       "mean_batch4":M(d["b"]),"mean_other":M(d["o"]),"difference":diff,"weight":w})
        num+=w*diff;den+=w
    std_diff=num/den if den else None

    jack={}
    signflips=[]
    influences=[]
    for sid in sorted(b4):
        rem=[v for s,v in delta.items() if s!=sid];m=M(rem)
        jack[str(sid)]={"removed_delta":b4[sid],"remaining_mean":m}
        if (overall>0 and m<=0) or (overall<0 and m>=0):signflips.append(sid)
        influences.append((abs(overall-m),sid,m))
    influences.sort(reverse=True)

    def comp(ids,field):
        return dict(sorted(Counter(meta[s][field] for s in ids).items()))
    rows=[]
    for sid,v in sorted(b4.items()):
        rows.append({"source_id":sid,"delta":v,**meta[sid]})
    if signflips:
        verdict="SPARSE_BATCH4_SOLVE_LEVERAGE"
    elif std_diff is not None and abs(std_diff)<=0.01:
        verdict="BATCH4_RAW_LEVERAGE_COMPOSITION_EXPLAINED"
    elif std_diff is not None and std_diff>0.01:
        verdict="POSITIVE_BATCH4_RESIDUAL_AFTER_COMPOSITION_STANDARDIZATION"
    else:
        verdict="NO_POSITIVE_BATCH4_RESIDUAL_AFTER_STANDARDIZATION"
    rep={"schema_version":"g7-p10-r3-batch4-leverage-1","operation_type":"P7-Batch4 LB7 Leverage Fragility Audit",
      "eligible_solves":len(delta),"overall_mean":overall,
      "batch4":{"n":len(b4),"mean":raw_b4,"rows":rows,
                "method_counts":comp(b4,"method"),"provenance_counts":comp(b4,"provenance"),"reconstructor_counts":comp(b4,"reconstructor")},
      "non_batch4":{"n":len(oth),"mean":raw_oth,
                    "method_counts":comp(oth,"method"),"provenance_counts":comp(oth,"provenance"),"reconstructor_counts":comp(oth,"reconstructor")},
      "raw_batch4_minus_other":raw_diff,"common_support_strata":common,
      "standardized_batch4_minus_other":std_diff,"standardization_weight_sum":den,
      "leave_one_batch4_solve_out":jack,"batch4_single_solve_sign_flips":signflips,
      "largest_single_solve_influences":[{"source_id":sid,"abs_change":d,"remaining_mean":m} for d,sid,m in influences[:10]],
      "verdict":verdict,
      "boundary":["Batch4 is an acquisition cohort, not a causal treatment.",
                  "Common-support standardization uses method family × broad provenance only.",
                  "Reconstructor composition is reported descriptively and is not jointly standardized because of sparse cells.",
                  "No result identifies a cognitive mechanism."]}
    out=pathlib.Path(z.out);out.mkdir(parents=True,exist_ok=True)
    (out/"batch4-leverage-audit.json").write_text(json.dumps(rep,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P10_R3_BATCH4_LEVERAGE_PASS");print("VERDICT",verdict)
    print("RAW",json.dumps({"overall":overall,"batch4":raw_b4,"other":raw_oth,"diff":raw_diff}))
    print("STANDARDIZED",std_diff);print("SIGN_FLIPS",json.dumps(signflips));print("BATCH4_ROWS",json.dumps(rows))
if __name__=="__main__":main()
