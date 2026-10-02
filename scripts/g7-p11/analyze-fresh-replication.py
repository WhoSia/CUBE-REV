#!/usr/bin/env python3
import argparse,csv,json,pathlib,random,statistics
from collections import defaultdict

R=("H1","H2","H3","FS"); C={x:x.lower()+"_best" for x in R}; C["TS"]="ts_best"; N=18
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
    return {"n_solves":len(v),"mean":M(v),"median":MED(v),
      "positive":sum(x>0 for x in v),"zero":sum(x==0 for x in v),"negative":sum(x<0 for x in v),
      "signflip_p":sf(v,n,seed)}
def qbin(p): return min(4,max(0,int(p*5))) if p<1 else 4

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True);ap.add_argument("--context",required=True)
    ap.add_argument("--out",required=True);ap.add_argument("--permutations",type=int,default=100000)
    z=ap.parse_args()
    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    rows=[];maxpi=defaultdict(int)
    with open(z.features,encoding="utf-8",newline="") as f:
      for x in csv.DictReader(f,delimiter="\t"):
        sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"])
        if a<0:continue
        maxpi[sid]=max(maxpi[sid],pi)
        sets={r:S(x[C[r]]) for r in (*R,"TS")}
        low={m for m in sets["TS"] if sum(m in sets[r] for r in R)<=2}
        k=len(low);c=ctx[(sid,pi)]
        rows.append({
          "sid":sid,"pi":pi,"lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),
          "k":k,"avail":int(k>0),"match":int(a in low),"ex":int(a in low)-k/N,
          "cohort":c.get("cohort") or "NULL","method":c.get("method_family") or "NULL",
          "cell":c.get("sampling_cell") or "NULL","boundary":bool(c.get("boundary_after"))
        })
    solves=sorted({r["sid"] for r in rows})
    if len(solves)!=40: raise SystemExit("FRESH40_SOLVES_REQUIRED_"+str(len(solves)))
    for r in rows:r["q"]=qbin(r["pi"]/maxpi[r["sid"]] if maxpi[r["sid"]]>0 else 0)

    g1=[r for r in rows if r["g1"]==1]
    g1_avail=M([r["avail"] for r in g1]) if g1 else None

    lb7_by=defaultdict(list)
    for r in rows:
        if r["lb"]==7 and r["g1"]==0 and r["avail"]:
            lb7_by[r["sid"]].append(r["ex"])
    lb7_vals=[M(v) for v in lb7_by.values()]
    lb7=stat(lb7_vals,z.permutations,20271101)

    st=defaultdict(lambda:{"t":[],"c":[]})
    for r in rows:
        if r["g1"]!=0 or not r["avail"] or r["lb"] not in (6,7,8):continue
        key=(r["sid"],r["q"],str(r["k"]))
        st[key]["t" if r["lb"]==7 else "c"].append(r["ex"])
    per=defaultdict(list)
    for key,d in st.items():
        if d["t"] and d["c"]:
            w=min(len(d["t"]),len(d["c"]))
            per[key[0]].append((M(d["t"])-M(d["c"]),w))
    local_vals={}
    for sid,xs in per.items():
        den=sum(w for _,w in xs);local_vals[sid]=sum(v*w for v,w in xs)/den
    local=stat(list(local_vals.values()),z.permutations,20271102)
    local["eligible_solve_ids"]=sorted(local_vals)
    local["per_solve_delta"]={str(k):v for k,v in sorted(local_vals.items())}

    def group_readout(field):
        out={}
        metas={r["sid"]:r for r in rows}
        keys=sorted({metas[sid][field] for sid in solves})
        for i,k in enumerate(keys):
            sids={sid for sid in solves if metas[sid][field]==k}
            a=[M(lb7_by[sid]) for sid in sids if sid in lb7_by]
            b=[local_vals[sid] for sid in sids if sid in local_vals]
            out[k]={"n_selected_solves":len(sids),
              "lb7_conditional":stat(a,z.permutations,20271200+i*2),
              "lb7_neighbor_local":stat(b,z.permutations,20271201+i*2)}
        return out

    eligible=local["n_solves"]
    if eligible<10:
        verdict="SUPPORT_LIMITED"
    elif lb7["mean"] is not None and lb7["mean"]>0 and local["mean"] is not None and local["mean"]>0:
        verdict="REPLICATED_DIRECTION"
    else:
        verdict="NOT_REPLICATED_DIRECTION"

    rep={
      "schema_version":"g7-p11-fresh-replication-readout-1",
      "operation_type":"Fresh-Reconstruction State-Surface Replication Readout",
      "fresh_only":True,"prior_60_pooled":False,
      "solves":40,"face_next_states":len(rows),
      "g1":{"states":len(g1),"low_overlap_support_availability":g1_avail},
      "primary":{
        "lb7_conditional_solve_excess":lb7,
        "lb7_minus_lb6_8_exact_local":local
      },
      "by_sampling_cell":group_readout("cell"),
      "by_batch":group_readout("cohort"),
      "by_method":group_readout("method"),
      "verdict":verdict,
      "frozen_rule":{
        "support_limited":"exact local eligible solves < 10",
        "replicated_direction":"otherwise both lb7 conditional mean > 0 and exact local mean > 0",
        "not_replicated_direction":"otherwise"
      },
      "boundary":[
        "Fresh-only verdict is formed before any pooling with the prior 60 solves.",
        "Sign-flip p-values are descriptive diagnostics and are not thresholds in the frozen directional verdict.",
        "Method/reconstructor sampling cells are acquisition controls, not latent cognitive mechanisms.",
        "No result promotes TS/PDB geometry to a human cognitive mechanism."
      ]
    }
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"fresh-replication-readout.json").write_text(json.dumps(rep,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P11_FRESH_REPLICATION_READOUT_PASS")
    print("G1",json.dumps(rep["g1"]))
    print("LB7",json.dumps(lb7))
    print("LOCAL",json.dumps(local))
    print("VERDICT",verdict)
if __name__=="__main__":main()
