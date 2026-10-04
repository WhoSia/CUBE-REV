#!/usr/bin/env python3
import argparse,csv,json,pathlib,itertools
from collections import defaultdict

N=18
def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(xs): return sum(xs)/len(xs) if xs else None
def qbin(pi,mx):
    if mx<=0:return 0
    p=pi/mx
    return min(4,max(0,int(p*5))) if p<1 else 4
def cells(r): return (r["l"],r["k"]-r["l"],r["d"]-r["l"],N-r["k"]-r["d"]+r["l"])
def du(a,b): return sum(abs(x-y) for x,y in zip(cells(a),cells(b)))/2.0

def solve_residuals(rows):
    by=defaultdict(list)
    for r in rows:by[(r["sid"],qbin(r["pi"],r["maxpi"]))].append(r)
    per=defaultdict(list)
    for (sid,q),grp in by.items():
        ts=[r for r in grp if r["lb"]==7];cs=[r for r in grp if r["lb"] in (6,8)]
        if not ts or not cs:continue
        for t in ts:
            cand=[c for c in cs if du(t,c)<=1.0+1e-15]
            if cand:per[sid].append(t["ex"]-M([c["ex"] for c in cand]))
    return {sid:M(v) for sid,v in per.items() if v}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True);ap.add_argument("--context",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    ctx={}
    for line in open(a.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    shell={}
    with open(a.shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            shell[(int(x["source_id"]),int(x["prefix_index"]))]={"lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),"desc":S(x["desc_actions"])}
    maxpi=defaultdict(int)
    for (sid,pi),c in ctx.items():
        if c.get("next_action_index") is not None:maxpi[sid]=max(maxpi[sid],pi)
    rows=[]
    meta={}
    with open(a.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);aa=int(x["next_action"])
            c=ctx[(sid,pi)];sh=shell[(sid,pi)]
            meta[sid]={
              "method":c.get("method_family") or "NULL",
              "recon":c.get("reconstructor_frequency_band") or "NULL",
              "era":c.get("selection_era") or "NULL",
              "batch":c.get("cohort") or "NULL",
              "cell":c.get("sampling_cell") or "NULL"
            }
            if aa<0 or c.get("next_action_index") is None or sh["g1"] or sh["lb"] not in (6,7,8):continue
            rivals={r:S(x[r.lower()+"_best"]) for r in ("H1","H2","H3","FS")}
            ts=S(x["ts_best"]);low={m for m in ts if sum(m in rivals[r] for r in rivals)<=2}
            if not low:continue
            rows.append({"sid":sid,"pi":pi,"maxpi":maxpi[sid],"lb":sh["lb"],"k":len(low),"d":len(sh["desc"]),"l":len(low&sh["desc"]),
              "ex":(1 if aa in low else 0)-len(low)/N})
    sr=solve_residuals(rows)
    if len(sr)<40:raise SystemExit("INSUFFICIENT_Q5_SOLVE_SUPPORT")
    axes={
      "method_family":["method"],
      "reconstructor_frequency_band":["recon"],
      "selection_era":["era"],
      "method_x_reconstructor":["method","recon"],
      "method_x_era":["method","era"],
      "reconstructor_x_era":["recon","era"],
      "method_x_reconstructor_x_era":["method","recon","era"]
    }
    def eval_axis(keys,exclude_batch=None):
        groups=defaultdict(list)
        for sid,val in sr.items():
            mm=meta[sid]
            if exclude_batch and mm["batch"]==exclude_batch:continue
            label=" × ".join(mm[k] for k in keys)
            groups[label].append(val)
        levels={k:{"n":len(v),"mean":M(v),"sign":0 if M(v)==0 else (1 if M(v)>0 else -1)} for k,v in sorted(groups.items())}
        eligible={k:v for k,v in levels.items() if v["n"]>=5}
        pairs=[]
        for la,lb in itertools.combinations(sorted(eligible),2):
            gap=abs(eligible[la]["mean"]-eligible[lb]["mean"])
            pairs.append((gap,la,lb))
        top=max(pairs,default=(None,None,None))
        return {"levels":levels,"eligible_level_count":len(eligible),
                "max_abs_gap":top[0],"max_gap_pair":[top[1],top[2]] if top[1] else None,
                "all_retained_levels_support_ge5":len(eligible)==len(levels) and len(levels)>=2}
    batches=sorted({m["batch"] for m in meta.values()})
    result={}
    ranking=[]
    for name,keys in axes.items():
        base=eval_axis(keys)
        loo={b:eval_axis(keys,b) for b in batches}
        if base["max_gap_pair"]:
            a,b=base["max_gap_pair"];base_dir=None
            # signed direction of b-a based on base pair labels
            lev=base["levels"];base_dir=1 if lev[b]["mean"]-lev[a]["mean"]>0 else -1
            stable=0;den=0
            for z in loo.values():
                if a in z["levels"] and b in z["levels"] and z["levels"][a]["n"]>=5 and z["levels"][b]["n"]>=5:
                    d=z["levels"][b]["mean"]-z["levels"][a]["mean"]
                    if d!=0:
                        den+=1;stable+=((1 if d>0 else -1)==base_dir)
            stability=stable/den if den else None
        else: stability=None
        result[name]={"base":base,"leave_one_batch_out":loo,"directional_stability":stability}
        if base["all_retained_levels_support_ge5"] and base["max_abs_gap"] is not None:
            ranking.append((base["max_abs_gap"],stability if stability is not None else -1,-len(base["levels"]),name))
    ranking.sort(reverse=True)
    report={
      "schema_version":"g7-p14-d1-composition-sign-exchange-map-1",
      "operation_type":"Composition Sign-Exchange Rival Map",
      "development_only":True,"fresh80_only":True,"q5_fixed":True,"r1_reselected":False,
      "q5_solve_support":len(sr),
      "axes":result,
      "ranking":[{"rank":i+1,"axis":x[3],"max_abs_gap":x[0],"directional_stability":x[1],"levels":-x[2]} for i,x in enumerate(ranking)],
      "top_candidate":ranking[0][3] if ranking else None,
      "boundary":["Development-only rival generation; no coordinate promotion.","Same fresh80 cannot confirm a ranked coordinate.","Independent new sample required for promotion."]
    }
    p=pathlib.Path(a.out);p.mkdir(parents=True,exist_ok=True)
    (p/"composition-sign-exchange-map.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P14_D1_COMPOSITION_MAP_PASS")
    print("SUPPORT",len(sr))
    print("RANKING",json.dumps(report["ranking"],sort_keys=True))
    print("TOP",report["top_candidate"])
    for n in axes:print("AXIS",n,json.dumps(result[n]["base"],sort_keys=True))
if __name__=="__main__":main()
