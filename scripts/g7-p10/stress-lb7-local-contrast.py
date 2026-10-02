#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random,statistics
from collections import defaultdict
R=("H1","H2","H3","FS");C={x:x.lower()+"_best" for x in R};C["TS"]="ts_best";N=18
def S(x):return {int(v) for v in (x or "").split(",") if v!=""}
def M(x):return sum(x)/len(x) if x else None
def MED(x):return statistics.median(x) if x else None
def sf(v,n,seed):
    if not v:return None
    o=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        if abs(M([x*(1 if g.random()<.5 else -1) for x in v]))>=o-1e-15:e+=1
    return (e+1)/(n+1)
def stat(v,n,seed):
    return {"n_solves":len(v),"mean":M(v),"median":MED(v),"positive":sum(x>0 for x in v),
            "zero":sum(x==0 for x in v),"negative":sum(x<0 for x in v),"signflip_p":sf(v,n,seed)}
def qbin(p):return min(4,max(0,int(p*5))) if p<1 else 4
def kb(k):return "1" if k==1 else ("2" if k==2 else "3+")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--features",required=True);ap.add_argument("--context",required=True)
    ap.add_argument("--out",required=True);ap.add_argument("--permutations",type=int,default=100000);z=ap.parse_args()
    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    raw=[]
    with open(z.features,encoding="utf-8",newline="") as f:
      for x in csv.DictReader(f,delimiter="\t"):
        sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"])
        if a<0:continue
        sets={r:S(x[C[r]]) for r in (*R,"TS")}
        low={m for m in sets["TS"] if sum(m in sets[r] for r in R)<=2}
        k=len(low)
        if k==0 or int(x["is_g1"])!=0:continue
        c=ctx[(sid,pi)]
        raw.append({"sid":sid,"pi":pi,"lb":int(x["phase1_lb"]),"k":k,
          "ex":(1 if a in low else 0)-k/N,"cohort":c.get("cohort") or "NULL",
          "method":c.get("method_family") or "NULL"})
    maxpi=defaultdict(int)
    # Max progress denominator must be over all face-next rows, not only eligible rows.
    with open(z.features,encoding="utf-8",newline="") as f:
      for x in csv.DictReader(f,delimiter="\t"):
        if int(x["next_action"])>=0:maxpi[int(x["source_id"])]=max(maxpi[int(x["source_id"])],int(x["prefix_index"]))
    for r in raw:r["q"]=qbin(r["pi"]/maxpi[r["sid"]] if maxpi[r["sid"]]>0 else 0)
    meta={}
    for r in raw:meta[r["sid"]]={"cohort":r["cohort"],"method":r["method"]}

    def contrast(target,comp,coarse=False,seed=20270500):
        st=defaultdict(lambda:{"t":[],"c":[]})
        for r in raw:
            if r["lb"] not in target and r["lb"] not in comp:continue
            sk=kb(r["k"]) if coarse else str(r["k"])
            key=(r["sid"],r["q"],sk)
            st[key]["t" if r["lb"] in target else "c"].append(r["ex"])
        per=defaultdict(list)
        for key,d in st.items():
            if not d["t"] or not d["c"]:continue
            w=min(len(d["t"]),len(d["c"]))
            per[key[0]].append((M(d["t"])-M(d["c"]),w))
        vals={}
        for sid,xs in per.items():
            den=sum(w for _,w in xs);vals[sid]=sum(v*w for v,w in xs)/den
        s=stat(list(vals.values()),z.permutations,seed)
        s["eligible_solve_ids"]=sorted(vals)
        s["per_solve_delta"]={str(k):v for k,v in sorted(vals.items())}
        return s,vals

    exact_union,vals=contrast({7},{6,8},False,20270500)
    exact_6,_=contrast({7},{6},False,20270501)
    exact_8,_=contrast({7},{8},False,20270502)
    coarse_union,_=contrast({7},{6,8},True,20270503)
    coarse_6,_=contrast({7},{6},True,20270504)
    coarse_8,_=contrast({7},{8},True,20270505)
    lb3_exact,_=contrast({3},{4,5},False,20270506)

    cohorts=defaultdict(set)
    for sid in vals:cohorts[meta[sid]["cohort"]].add(sid)
    loo={}
    for c,ids in sorted(cohorts.items()):
        rem=[v for sid,v in vals.items() if sid not in ids]
        loo[c]={"held_out":len(ids),"remaining_n":len(rem),"remaining_mean":M(rem)}
    methods=defaultdict(list)
    for sid,v in vals.items():methods[meta[sid]["method"]].append(v)
    meth={k:stat(v,z.permutations,20270600+i) for i,(k,v) in enumerate(sorted(methods.items())) if len(v)>=5}

    verdict="LB7_LOCALIZED_AGAINST_NEIGHBORS" if exact_union["mean"] is not None and exact_union["mean"]>0 else "LB7_NOT_LOCALIZED_AGAINST_NEIGHBORS"
    rep={"schema_version":"g7-p10-r2-lb7-local-contrast-1","operation_type":"LB7 Local-Contrast Matching Stress Test",
      "eligible_state_rows":len(raw),
      "exact_support_size":{"lb7_minus_lb6_8":exact_union,"lb7_minus_lb6":exact_6,"lb7_minus_lb8":exact_8},
      "coarse_support_size":{"lb7_minus_lb6_8":coarse_union,"lb7_minus_lb6":coarse_6,"lb7_minus_lb8":coarse_8},
      "lb3_minus_lb4_5_exact":lb3_exact,"leave_one_cohort_out":loo,"method_groups_min5":meth,
      "verdict":verdict,
      "boundary":["All states have nonempty d<=2 TS support and are outside G1.",
                  "Primary matching is exact within solve on progress quintile and exact low-overlap support-set size.",
                  "Coarse support-size matching is a parallel sensitivity readout, not a result-triggered fallback.",
                  "Matched contrasts are observational stress tests and are not causal counterfactuals or cognitive-mechanism evidence."]}
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"lb7-local-contrast.json").write_text(json.dumps(rep,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P10_R2_LB7_LOCAL_CONTRAST_PASS");print("VERDICT",verdict)
    print("EXACT_UNION",json.dumps(exact_union));print("EXACT_6",json.dumps(exact_6));print("EXACT_8",json.dumps(exact_8))
    print("COARSE_UNION",json.dumps(coarse_union));print("LB3",json.dumps(lb3_exact));print("LOO",json.dumps(loo))
if __name__=="__main__":main()
