#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random
from collections import defaultdict
R=("H1","H2","H3","FS");C={x:x.lower()+"_best" for x in R};C["TS"]="ts_best";N=18
def S(x):return {int(v) for v in (x or "").split(",") if v!=""}
def M(x):return sum(x)/len(x) if x else None
def P(v,n,seed):
    if not v:return None
    o=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        if abs(M([x*(1 if g.random()<.5 else -1) for x in v]))>=o-1e-15:e+=1
    return (e+1)/(n+1)
def stat(v,n,seed,infer=True):
    return {"n":len(v),"mean":M(v),"positive":sum(x>0 for x in v),"zero":sum(x==0 for x in v),
            "negative":sum(x<0 for x in v),"signflip_p":P(v,n,seed) if infer else None}
def epoch(c):
    s=str(c or "")
    if s.startswith("P4_"):return "P4_PREDECESSOR"
    if s.startswith("P7_"):return "P7_FRESH_CAMPAIGN"
    return "OTHER"
def main():
    a=argparse.ArgumentParser();a.add_argument("--features",required=True);a.add_argument("--context",required=True)
    a.add_argument("--provenance",required=True);a.add_argument("--out",required=True);a.add_argument("--permutations",type=int,default=100000)
    z=a.parse_args()
    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    q=json.load(open(z.provenance,encoding="utf-8"));prov={int(k):v for k,v in q["source_id_to_broad_provenance_class"].items()}
    by=defaultdict(list)
    with open(z.features,encoding="utf-8",newline="") as f:
      for x in csv.DictReader(f,delimiter="\t"):
        sid=int(x["source_id"]);pi=int(x["prefix_index"]);act=int(x["next_action"])
        if act<0:continue
        sets={r:S(x[C[r]]) for r in (*R,"TS")}
        low={m for m in sets["TS"] if sum(m in sets[r] for r in R)<=2}
        ex=(1 if act in low else 0)-len(low)/N
        by[sid].append((ex,len(low),ctx[(sid,pi)]))
    if len(by)!=60:raise SystemExit("SOLVES_60_REQUIRED")
    solves={}
    for sid,rows in by.items():
        c=rows[0][2]
        solves[sid]={"value":M([r[0] for r in rows]),"support_size":M([r[1] for r in rows]),
          "method":c.get("method_family") or "NULL","cohort":c.get("cohort") or "NULL",
          "epoch":epoch(c.get("cohort")),"provenance":prov.get(sid,"MISSING")}
    overall=stat([x["value"] for x in solves.values()],z.permutations,20269500)
    def grouped(field):
        g=defaultdict(list)
        for x in solves.values():g[x[field]].append(x["value"])
        out={};i=0
        for k,v in sorted(g.items()):
            if len(v)<3:continue
            out[k]=stat(v,z.permutations,20269510+i,len(v)>=5);i+=1
        return out
    def loo(field):
        g=defaultdict(set)
        for sid,x in solves.items():g[x[field]].add(sid)
        out={}
        for k,ids in sorted(g.items()):
            if len(ids)<3:continue
            v=[x["value"] for sid,x in solves.items() if sid not in ids]
            out[k]={"held_out":len(ids),"remaining_n":len(v),"remaining_mean":M(v)}
        return out
    groups={f:grouped(f) for f in ("method","provenance","cohort","epoch")}
    leave={f:loo(f) for f in ("method","provenance","cohort")}
    flips={f:[k for k,v in leave[f].items() if v["remaining_mean"]<=0] for f in leave}
    ep=groups["epoch"];epoch_bad=[k for k,v in ep.items() if v["mean"]<=0]
    verdict="LOW_OVERLAP_SIGNAL_GROUP_CONCENTRATED" if any(flips.values()) or epoch_bad else "LOW_OVERLAP_SIGNAL_TRANSPORT_STABLE"
    out={"schema_version":"g7-p9-r2-low-overlap-transport-1","operation_type":"Low-Overlap TS Specificity Transport Stress Test",
      "solves":60,"overall":overall,"groups":groups,"leave_one_group_out":leave,"leave_one_out_nonpositive":flips,
      "campaign_epoch_nonpositive":epoch_bad,"mean_low_overlap_support_size_by_solve":M([x["support_size"] for x in solves.values()]),
      "verdict":verdict,
      "boundary":["Low-overlap means TS moves shared with at most two of H1/H2/H3/FS.",
                  "Solve is the independent unit.","Subgroup and deletion analyses are stress diagnostics, not new confirmation.",
                  "No result identifies a cognitive mechanism."]}
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"low-overlap-transport-stress.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P9_R2_LOW_OVERLAP_TRANSPORT_PASS");print("VERDICT",verdict)
    print("OVERALL",json.dumps(overall));print("EPOCH",json.dumps(ep));print("FLIPS",json.dumps(flips))
if __name__=="__main__":main()
