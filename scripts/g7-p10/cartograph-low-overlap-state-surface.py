#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random,statistics
from collections import defaultdict,Counter
R=("H1","H2","H3","FS"); C={x:x.lower()+"_best" for x in R}; C["TS"]="ts_best"; N=18
def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(x): return sum(x)/len(x) if x else None
def MED(x): return statistics.median(x) if x else None
def sf(v,n,seed):
    if not v:return None
    o=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        if abs(M([x*(1 if g.random()<.5 else -1) for x in v]))>=o-1e-15:e+=1
    return (e+1)/(n+1)
def stat(v,n,seed):
    return {"n_solves":len(v),"mean":M(v),"median":MED(v),"positive":sum(x>0 for x in v),
            "zero":sum(x==0 for x in v),"negative":sum(x<0 for x in v),"signflip_p":sf(v,n,seed)}
def qbin(p): return min(4,max(0,int(p*5))) if p<1 else 4
def sbin(k): return "0" if k==0 else ("1" if k==1 else ("2" if k==2 else "3+"))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True);ap.add_argument("--context",required=True)
    ap.add_argument("--out",required=True);ap.add_argument("--permutations",type=int,default=100000)
    z=ap.parse_args()
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
        ex=(1 if a in low else 0)-len(low)/N
        c=ctx[(sid,pi)]
        raw.append({"sid":sid,"pi":pi,"ex":ex,"lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),
                    "boundary":bool(c.get("boundary_after")),"support":len(low),
                    "cohort":c.get("cohort") or "NULL","method":c.get("method_family") or "NULL"})
    if len(raw)!=2725 or len({r["sid"] for r in raw})!=60:raise SystemExit("FROZEN_GEOMETRY_MISMATCH")
    maxpi=defaultdict(int)
    for r in raw:maxpi[r["sid"]]=max(maxpi[r["sid"]],r["pi"])
    for r in raw:
        r["progress"]=r["pi"]/maxpi[r["sid"]] if maxpi[r["sid"]]>0 else 0
        r["q"]=qbin(r["progress"]);r["sb"]=sbin(r["support"])

    def solve_group(keyfn,minsol=1,seed0=20269600):
        cell=defaultdict(lambda:defaultdict(list))
        for r in raw:cell[keyfn(r)][r["sid"]].append(r["ex"])
        out={};seed=seed0
        for k,sm in sorted(cell.items(),key=lambda x:str(x[0])):
            vals=[M(v) for v in sm.values()]
            if len(vals)<minsol:continue
            out[str(k)]=stat(vals,z.permutations,seed);seed+=1
            out[str(k)]["state_rows"]=sum(len(v) for v in sm.values())
        return out

    by_lb=solve_group(lambda r:r["lb"])
    by_g1=solve_group(lambda r:r["g1"],seed0=20269700)
    by_q=solve_group(lambda r:r["q"],seed0=20269800)
    structural=solve_group(lambda r:(r["lb"],r["g1"],r["q"]),minsol=5,seed0=20269900)

    # exact within-solve matched boundary contrast
    strata=defaultdict(lambda:{"b":[],"n":[]})
    for r in raw:
        key=(r["sid"],r["lb"],r["g1"],r["q"],r["sb"])
        strata[key]["b" if r["boundary"] else "n"].append(r["ex"])
    per=defaultdict(list)
    for key,d in strata.items():
        if not d["b"] or not d["n"]:continue
        delta=M(d["b"])-M(d["n"]);w=min(len(d["b"]),len(d["n"]))
        per[key[0]].append((delta,w))
    bvals=[]
    for sid,xs in per.items():
        den=sum(w for _,w in xs); bvals.append(sum(d*w for d,w in xs)/den)
    boundary=stat(bvals,z.permutations,20270000)
    boundary["eligible_solves"]=len(bvals)

    # descriptive structural hotspot and cohort-deletion sensitivity
    cell_members=defaultdict(lambda:defaultdict(list))
    for r in raw:cell_members[(r["lb"],r["g1"],r["q"])][r["sid"]].append(r["ex"])
    eligible=[]
    for k,sm in cell_members.items():
        vals={sid:M(v) for sid,v in sm.items()}
        if len(vals)>=5: eligible.append((k,vals,M(list(vals.values()))))
    eligible.sort(key=lambda x:x[2],reverse=True)
    hotspot=[]
    cohorts=defaultdict(set)
    for r in raw:cohorts[r["cohort"]].add(r["sid"])
    for k,vals,m in eligible[:10]:
        loo={}
        for c,ids in cohorts.items():
            rem=[v for sid,v in vals.items() if sid not in ids]
            if rem:loo[c]=M(rem)
        hotspot.append({"cell":{"phase1_lb":k[0],"is_g1":k[1],"progress_quintile":k[2]},
                        "solves":len(vals),"mean":m,"leave_one_cohort_out":dict(sorted(loo.items())),
                        "all_loo_positive":all(v>0 for v in loo.values()) if loo else None})

    method_cells=defaultdict(lambda:defaultdict(list))
    for r in raw:method_cells[(r["lb"],r["g1"],r["q"],r["method"])][r["sid"]].append(r["ex"])
    method_out={}
    for k,sm in sorted(method_cells.items(),key=lambda x:str(x[0])):
        if len(sm)<3:continue
        vals=[M(v) for v in sm.values()]
        method_out[str(k)]={"n_solves":len(vals),"mean":M(vals)}

    report={"schema_version":"g7-p10-state-surface-cartography-1",
      "operation_type":"TS Low-Overlap State-Surface Cartography & Matched-State Stress Test",
      "states":len(raw),"solves":60,
      "by_phase1_lb":by_lb,"by_g1":by_g1,"by_progress_quintile":by_q,
      "structural_cells_min5":structural,
      "matched_boundary_minus_nonboundary":boundary,
      "top_structural_cells_exploratory":hotspot,
      "method_structural_cells_min3":method_out,
      "boundary":["Solve-level aggregation precedes structural-cell inference.",
                  "Structural hotspot ranking is exploratory across many cells.",
                  "Boundary contrast is within-solve matched on phase1_lb, G1, progress quintile, and low-overlap support-size bin.",
                  "Computational coordinates do not identify a cognitive mechanism."]}
    positive_stable=[x for x in hotspot if x["mean"]>0 and x["all_loo_positive"]]
    report["verdict"]="DESCRIPTIVE_STRUCTURAL_LOCALIZATION_PRESENT" if positive_stable else "LOW_OVERLAP_SIGNAL_DIFFUSE_OR_UNSTABLE"
    out=pathlib.Path(z.out);out.mkdir(parents=True,exist_ok=True)
    (out/"state-surface-cartography.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P10_STATE_SURFACE_PASS");print("VERDICT",report["verdict"])
    print("BY_LB",json.dumps(by_lb));print("BY_G1",json.dumps(by_g1));print("BY_Q",json.dumps(by_q))
    print("BOUNDARY",json.dumps(boundary));print("HOTSPOT",json.dumps(hotspot[:5]))
if __name__=="__main__":main()
