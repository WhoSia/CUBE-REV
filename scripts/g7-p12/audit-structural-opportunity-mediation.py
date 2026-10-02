#!/usr/bin/env python3
import argparse,csv,json,pathlib,random,statistics
from collections import defaultdict,Counter

R=("H1","H2","H3","FS"); C={x:x.lower()+"_best" for x in R}; C["TS"]="ts_best"; N=18
P11_LOCAL=0.056231231231231235
P10_LOCAL=0.048695054945054946

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(x): return sum(x)/len(x) if x else None
def MED(x):
    if not x:return None
    y=sorted(x);m=len(y)//2
    return y[m] if len(y)%2 else (y[m-1]+y[m])/2
def sf(v,n,seed):
    if not v:return None
    o=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        z=M([x*(1 if g.random()<.5 else -1) for x in v])
        if abs(z)>=o-1e-15:e+=1
    return (e+1)/(n+1)
def stat(v,n,seed):
    return {"n_solves":len(v),"mean":M(v),"median":MED(v),"positive":sum(x>0 for x in v),
            "zero":sum(x==0 for x in v),"negative":sum(x<0 for x in v),"signflip_p":sf(v,n,seed)}
def qbin(p): return min(4,max(0,int(p*5))) if p<1 else 4
def kbin(k): return "1" if k==1 else ("2" if k==2 else "3+")
def dbin(d): return "0-2" if d<=2 else ("3-5" if d<=5 else "6+")
def ldbin(d): return "0" if d==0 else ("1" if d==1 else "2+")

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
            key=(int(x["source_id"]),int(x["prefix_index"]))
            shell[key]={
              "lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),
              "next_lbs":[int(v) for v in x["next_lbs"].split(",")],
              "desc":S(x["desc_actions"]),"eq":S(x["plateau_actions"]),"asc":S(x["asc_actions"]),
              "g1_next":S(x["g1_next_actions"])
            }
    rows=[];maxpi=defaultdict(int)
    with open(z.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"])
            if a<0:continue
            key=(sid,pi); c=ctx[key]; sh=shell[key]
            if int(x["phase1_lb"])!=sh["lb"] or int(x["is_g1"])!=sh["g1"]:raise SystemExit("SHELL_FEATURE_MISMATCH")
            maxpi[sid]=max(maxpi[sid],pi)
            sets={r:S(x[C[r]]) for r in (*R,"TS")}
            low={m for m in sets["TS"] if sum(m in sets[r] for r in R)<=2}
            k=len(low); low_desc=low & sh["desc"]
            ancestry="FRESH40" if str(c.get("cohort") or "").startswith("P11_") else "LEGACY60"
            rows.append({
              "sid":sid,"pi":pi,"a":a,"lb":sh["lb"],"g1":sh["g1"],"next_lbs":sh["next_lbs"],
              "k":k,"low":low,"desc_count":len(sh["desc"]),"eq_count":len(sh["eq"]),"asc_count":len(sh["asc"]),
              "g1_next_count":len(sh["g1_next"]),"low_desc_count":len(low_desc),
              "low_desc_frac":len(low_desc)/k if k else None,
              "low_share_desc":len(low_desc)/len(sh["desc"]) if sh["desc"] else None,
              "ex":(1 if a in low else 0)-k/N,
              "ancestry":ancestry,"cohort":c.get("cohort") or "NULL","method":c.get("method_family") or "NULL",
              "cell":c.get("sampling_cell") or "NULL"
            })
    if len({r["sid"] for r in rows if r["ancestry"]=="LEGACY60"})!=60:raise SystemExit("LEGACY60_REQUIRED")
    if len({r["sid"] for r in rows if r["ancestry"]=="FRESH40"})!=40:raise SystemExit("FRESH40_REQUIRED")
    for r in rows:r["q"]=qbin(r["pi"]/maxpi[r["sid"]] if maxpi[r["sid"]]>0 else 0)

    def surf(rs):
        out={}
        for lb in (6,7,8):
            xs=[r for r in rs if r["lb"]==lb and r["g1"]==0]
            avail=[r for r in xs if r["k"]>0]
            delta=Counter()
            for r in xs:
                for nl in r["next_lbs"]:delta[nl-lb]+=1
            out[str(lb)]={
              "states":len(xs),"solves":len({r["sid"] for r in xs}),
              "support_availability":M([1 if r["k"]>0 else 0 for r in xs]),
              "mean_low_overlap_support_size":M([r["k"] for r in xs]),
              "mean_descending_actions":M([r["desc_count"] for r in xs]),
              "mean_plateau_actions":M([r["eq_count"] for r in xs]),
              "mean_ascending_actions":M([r["asc_count"] for r in xs]),
              "mean_g1_next_actions":M([r["g1_next_count"] for r in xs]),
              "available_states":len(avail),
              "mean_low_overlap_descending_actions":M([r["low_desc_count"] for r in avail]),
              "mean_low_descending_fraction_of_low_support":M([r["low_desc_frac"] for r in avail]),
              "mean_low_overlap_share_of_descending_actions":M([r["low_share_desc"] for r in avail if r["low_share_desc"] is not None]),
              "next_lb_delta_action_counts":dict(sorted((str(k),v) for k,v in delta.items()))
            }
        return out

    def contrast(rs,structural=False,coarse=False,seed=20271300):
        st=defaultdict(lambda:{"t":[],"c":[]})
        for r in rs:
            if r["g1"]!=0 or r["k"]==0 or r["lb"] not in (6,7,8):continue
            if structural:
                if coarse:key=(r["sid"],r["q"],kbin(r["k"]),dbin(r["desc_count"]),ldbin(r["low_desc_count"]))
                else:key=(r["sid"],r["q"],str(r["k"]),r["desc_count"],r["low_desc_count"])
            else:key=(r["sid"],r["q"],str(r["k"]))
            st[key]["t" if r["lb"]==7 else "c"].append(r["ex"])
        per=defaultdict(list)
        for key,d in st.items():
            if d["t"] and d["c"]:
                w=min(len(d["t"]),len(d["c"]))
                per[key[0]].append((M(d["t"])-M(d["c"]),w))
        vals={}
        for sid,xs in per.items():
            den=sum(w for _,w in xs);vals[sid]=sum(v*w for v,w in xs)/den
        s=stat(list(vals.values()),z.permutations,seed)
        s["eligible_solve_ids"]=sorted(vals)
        return s

    scopes={
      "FRESH40":[r for r in rows if r["ancestry"]=="FRESH40"],
      "LEGACY60":[r for r in rows if r["ancestry"]=="LEGACY60"],
      "ALL100":rows
    }
    report={}
    for i,(name,rs) in enumerate(scopes.items()):
        report[name]={
          "shell_surfaces":surf(rs),
          "baseline_q_support_exact":contrast(rs,False,False,20271300+i*10),
          "structural_exact":contrast(rs,True,False,20271301+i*10),
          "structural_coarse_parallel":contrast(rs,True,True,20271302+i*10)
        }

    fresh_base=report["FRESH40"]["baseline_q_support_exact"]
    legacy_base=report["LEGACY60"]["baseline_q_support_exact"]
    if fresh_base["mean"] is None or abs(fresh_base["mean"]-P11_LOCAL)>1e-12:raise SystemExit("P11_BASELINE_REPRO_FAIL")
    if legacy_base["mean"] is None or abs(legacy_base["mean"]-P10_LOCAL)>1e-12:raise SystemExit("P10_BASELINE_REPRO_FAIL")

    fresh=report["FRESH40"]["structural_exact"]
    if fresh["n_solves"]<10:
        verdict="STRUCTURAL_MEDIATION_UNIDENTIFIED_SUPPORT_LIMITED"
        ratio=None
    else:
        ratio=abs(fresh["mean"])/abs(P11_LOCAL)
        if fresh["mean"]<=0 or ratio<=0.5:
            verdict="STRUCTURAL_OPPORTUNITY_DOMINANT"
        else:
            verdict="RESIDUAL_LB7_ALIGNMENT_AFTER_STRUCTURAL_OPPORTUNITY_MATCHING"

    out={
      "schema_version":"g7-p12-structural-opportunity-mediation-1",
      "operation_type":"Structural-Opportunity Mediation Audit",
      "states":len(rows),"solves":100,
      "ancestry_solve_counts":{"LEGACY60":60,"FRESH40":40},
      "scopes":report,
      "fresh_parent_local_mean":P11_LOCAL,
      "fresh_structural_to_parent_abs_ratio":ratio,
      "verdict":verdict,
      "boundary":[
        "One-move local geometry is reconstructed exactly for observed states only, not the complete global phase1 shell.",
        "P12 is post-P11 explanatory analysis and is not an independent replication.",
        "Exact structural matching is descriptive mediation diagnostics rather than causal adjustment.",
        "Fresh and legacy ancestry remain explicit in every primary readout.",
        "No result identifies a human cognitive mechanism."
      ]
    }
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"structural-opportunity-mediation.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P12_STRUCTURAL_OPPORTUNITY_AUDIT_PASS")
    print("FRESH_BASE",json.dumps(fresh_base))
    print("FRESH_STRUCTURAL",json.dumps(fresh))
    print("LEGACY_STRUCTURAL",json.dumps(report["LEGACY60"]["structural_exact"]))
    print("FRESH_SURFACE",json.dumps(report["FRESH40"]["shell_surfaces"]))
    print("RATIO",ratio)
    print("VERDICT",verdict)

if __name__=="__main__":
    main()
