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
def ss(v,n,seed):
    return {"n_solves":len(v),"mean":M(v),"median":MED(v),"positive":sum(x>0 for x in v),
            "zero":sum(x==0 for x in v),"negative":sum(x<0 for x in v),"signflip_p":sf(v,n,seed)}
def qbin(p):return min(4,max(0,int(p*5))) if p<1 else 4
def sbin(k):return "1" if k==1 else ("2" if k==2 else "3+")
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
        k=len(low);match=int(a in low);ex=match-k/N
        c=ctx[(sid,pi)]
        raw.append({"sid":sid,"pi":pi,"lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),
          "boundary":bool(c.get("boundary_after")),"k":k,"avail":int(k>0),"match":match,"ex":ex})
    if len(raw)!=2725:raise SystemExit("STATE_COUNT_FAIL")
    maxpi=defaultdict(int)
    for r in raw:maxpi[r["sid"]]=max(maxpi[r["sid"]],r["pi"])
    for r in raw:r["q"]=qbin(r["pi"]/maxpi[r["sid"]] if maxpi[r["sid"]]>0 else 0)

    def surface(fn,seed0):
        g=defaultdict(list)
        for r in raw:g[fn(r)].append(r)
        out={};seed=seed0
        for key,rows in sorted(g.items(),key=lambda x:str(x[0])):
            by=defaultdict(list)
            for r in rows:by[r["sid"]].append(r)
            solve_av=[M([x["avail"] for x in xs]) for xs in by.values()]
            cond=[]
            for xs in by.values():
                a=[x for x in xs if x["avail"]]
                if a:cond.append(M([x["ex"] for x in a]))
            ar=M([r["avail"] for r in rows]); ce=M([r["ex"] for r in rows if r["avail"]])
            total=M([r["ex"] for r in rows]); residual=total-(ar*ce if ce is not None else 0)
            out[str(key)]={
              "states":len(rows),"solves":len(by),"availability_state_rate":ar,
              "availability_solve_clustered":ss(solve_av,z.permutations,seed),
              "available_states":sum(r["avail"] for r in rows),
              "conditional_state_excess":ce,
              "conditional_match_rate":M([r["match"] for r in rows if r["avail"]]),
              "conditional_uniform_baseline":M([r["k"]/N for r in rows if r["avail"]]),
              "conditional_solve_excess":ss(cond,z.permutations,seed+1) if cond else None,
              "unconditional_state_excess":total,"factorization_residual":residual
            };seed+=2
        return out

    lb=surface(lambda r:r["lb"],20270100);g1=surface(lambda r:r["g1"],20270200);q=surface(lambda r:r["q"],20270300)

    # nonempty-support boundary contrast, structurally matched within solve
    st=defaultdict(lambda:{"b":[],"n":[]})
    for r in raw:
        if not r["avail"]:continue
        key=(r["sid"],r["lb"],r["g1"],r["q"],sbin(r["k"]))
        st[key]["b" if r["boundary"] else "n"].append(r["ex"])
    bysolve=defaultdict(list)
    for key,d in st.items():
        if d["b"] and d["n"]:
            bysolve[key[0]].append((M(d["b"])-M(d["n"]),min(len(d["b"]),len(d["n"]))))
    bd=[]
    for sid,xs in bysolve.items():
        den=sum(w for _,w in xs);bd.append(sum(v*w for v,w in xs)/den)
    boundary=ss(bd,z.permutations,20270400);boundary["eligible_solves"]=len(bd)

    target={}
    for name,surf,key in [("lb3",lb,"3"),("lb7",lb,"7"),("non_g1",g1,"0"),("g1",g1,"1"),("q3",q,"3"),("q4",q,"4")]:
        target[name]=surf.get(key)
    positives=[]
    for name in ("lb7","non_g1","q3"):
        x=target[name]
        positives.append(bool(x and x["conditional_solve_excess"] and x["conditional_solve_excess"]["mean"]>0))
    availability_structural=bool(target["g1"] and target["g1"]["availability_state_rate"]==0) or (
        max(x["availability_state_rate"] for x in lb.values())-min(x["availability_state_rate"] for x in lb.values())>0.25)
    if all(positives) and availability_structural:verdict="MIXED_AVAILABILITY_AND_CONDITIONAL_CHOICE_LOCALIZATION"
    elif all(positives):verdict="CONDITIONAL_CHOICE_LOCALIZATION_PRESENT"
    else:verdict="LOCALIZATION_LARGELY_AVAILABILITY_DRIVEN_OR_UNSTABLE"
    rep={"schema_version":"g7-p10-r1-support-choice-factorization-1",
      "operation_type":"Low-Overlap Support-Emergence vs Conditional-Choice Factorization Audit",
      "states":len(raw),"solves":len({r["sid"] for r in raw}),"by_phase1_lb":lb,"by_g1":g1,"by_progress_quintile":q,
      "targeted_reanalysis":target,"matched_boundary_nonempty_support":boundary,"verdict":verdict,
      "max_factorization_abs_residual":max(abs(x["factorization_residual"]) for surf in (lb,g1,q) for x in surf.values()),
      "boundary":["Absent low-overlap support implies undefined conditional preference, not zero preference.",
                  "State-weighted factorization is exact; inference remains solve-clustered.",
                  "Targeted surfaces were selected after P10 cartography and are stress diagnostics.",
                  "No result identifies a cognitive mechanism."]}
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"support-choice-factorization.json").write_text(json.dumps(rep,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P10_R1_FACTORISATION_PASS");print("VERDICT",verdict);print("TARGET",json.dumps(target));print("BOUNDARY",json.dumps(boundary))
if __name__=="__main__":main()
