#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random
from collections import defaultdict
R=("H1","H2","H3","FS"); C={x:x.lower()+"_best" for x in R}; C["TS"]="ts_best"; N=18
def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(x): return sum(x)/len(x) if x else None
def P(v,n,seed):
    o=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        if abs(M([x*(1 if g.random()<.5 else -1) for x in v]))>=o-1e-15:e+=1
    return (e+1)/(n+1)
def stat(v,n,seed):
    return {"n":len(v),"mean":M(v),"positive":sum(x>0 for x in v),"zero":sum(x==0 for x in v),
            "negative":sum(x<0 for x in v),"signflip_p":P(v,n,seed)}
def main():
    a=argparse.ArgumentParser();a.add_argument("--features",required=True);a.add_argument("--out",required=True)
    a.add_argument("--permutations",type=int,default=100000);z=a.parse_args()
    by=defaultdict(list); slots=[0]*5; matches=[0]*5; nonempty=[0]*5; pairerr=0.0
    with open(z.features,encoding="utf-8",newline="") as f:
      for x in csv.DictReader(f,delimiter="\t"):
        sid=int(x["source_id"]);act=int(x["next_action"])
        if act<0:continue
        q={r:S(x[C[r]]) for r in (*R,"TS")}
        buckets=[set() for _ in range(5)]
        for m in q["TS"]: buckets[sum(m in q[r] for r in R)].add(m)
        row={};total=(1 if act in q["TS"] else 0)-len(q["TS"])/N;sm=0.0
        for d,b in enumerate(buckets):
            v=(1 if act in b else 0)-len(b)/N;row[d]=v;sm+=v
            slots[d]+=len(b);matches[d]+=int(act in b);nonempty[d]+=int(bool(b))
        if abs(total-sm)>1e-12:raise SystemExit("DEGREE_SUM_FAIL")
        row["total"]=total;by[sid].append(row)
        for r in R:
            left=total-((1 if act in q[r] else 0)-len(q[r])/N)
            ta=q["TS"]-q[r];ra=q[r]-q["TS"]
            right=((1 if act in ta else 0)-len(ta)/N)-((1 if act in ra else 0)-len(ra)/N)
            pairerr=max(pairerr,abs(left-right))
    if len(by)!=60:raise SystemExit("SOLVE_COUNT_FAIL")
    solve={sid:{d:M([r[d] for r in rows]) for d in range(5)} for sid,rows in by.items()}
    for sid,rows in by.items():solve[sid]["total"]=M([r["total"] for r in rows])
    degree={str(d):stat([x[d] for x in solve.values()],z.permutations,20269400+d) for d in range(5)}
    low01=stat([x[0]+x[1] for x in solve.values()],z.permutations,20269410)
    low012=stat([x[0]+x[1]+x[2] for x in solve.values()],z.permutations,20269411)
    total=M([x["total"] for x in solve.values()]);tslots=sum(slots);tmatches=sum(matches)
    mass={str(d):{"support_slots":slots[d],"support_share":slots[d]/tslots,"states_nonempty":nonempty[d],
                  "observed_matches":matches[d],"observed_match_share":matches[d]/tmatches,
                  "fraction_total_excess":degree[str(d)]["mean"]/total if total else None} for d in range(5)}
    if low012["mean"]>0 and low012["signflip_p"]<=.05:
        verdict="LOW_OVERLAP_TS_EXCESS_SUPPORTED"
    elif degree["4"]["mean"]>0 and degree["4"]["mean"]>=low012["mean"]:
        verdict="HIGH_OVERLAP_SUPPORT_DOMINATES_TS_ALIGNMENT"
    else: verdict="MIXED_OVERLAP_DEGREE_ATTRIBUTION"
    out={"schema_version":"g7-p9-r1-overlap-degree-1","operation_type":"TS Overlap-Degree Attribution Audit",
         "states":sum(len(v) for v in by.values()),"solves":len(by),"degree_excess":degree,
         "low_overlap":{"degree_0_1":low01,"degree_0_1_2":low012},"support_mass":mass,
         "pairwise_symmetric_difference_identity_max_abs_error":pairerr,"verdict":verdict,
         "boundary":["Overlap degree counts H1/H2/H3/FS supports containing each TS-supported move.",
                     "Degree buckets partition TS support exactly.","This is descriptive computational geometry, not cognition."]}
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"ts-overlap-degree-attribution.json").write_text(json.dumps(out,indent=2)+"\n")
    print("G7_P9_R1_OVERLAP_DEGREE_PASS");print("VERDICT",verdict);print("DEGREES",json.dumps(degree));print("LOW012",json.dumps(low012));print("MASS",json.dumps(mass))
if __name__=="__main__":main()
