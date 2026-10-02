#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random,statistics
from collections import defaultdict,Counter

N=18
RIVALS=("H1","H2","H3","TS","FS")
COL={"H1":"h1_best","H2":"h2_best","H3":"h3_best","TS":"ts_best","FS":"fs_best"}

def parse_set(s): return {int(x) for x in (s or "").split(",") if x!=""}
def mean(x): return sum(x)/len(x) if x else None
def median(x): return statistics.median(x) if x else None

def signflip(vals,n,seed):
    vals=[float(x) for x in vals if x is not None and math.isfinite(float(x))]
    if not vals:return None
    obs=abs(mean(vals)); rng=random.Random(seed); ext=0
    for _ in range(n):
        m=mean([x*(1 if rng.random()<.5 else -1) for x in vals])
        if abs(m)>=obs-1e-15: ext+=1
    return (ext+1)/(n+1)

def summarize(vals,n,seed):
    return {
      "solves":len(vals),"mean":mean(vals),"median":median(vals),
      "positive":sum(x>0 for x in vals),"zero":sum(x==0 for x in vals),"negative":sum(x<0 for x in vals),
      "signflip_p":signflip(vals,n,seed)
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True)
    ap.add_argument("--context",required=True)
    ap.add_argument("--provenance",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--permutations",type=int,default=100000)
    args=ap.parse_args()

    ctx={}
    for line in open(args.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    prov=json.load(open(args.provenance,encoding="utf-8"))
    pclass={int(k):v for k,v in prov["source_id_to_broad_provenance_class"].items()}

    states=[]; by=defaultdict(list)
    with open(args.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"])
            if a<0: continue
            sets={r:parse_set(x[COL[r]]) for r in RIVALS}
            others=set().union(*(sets[r] for r in RIVALS if r!="TS"))
            unique=sets["TS"]-others
            shared=sets["TS"]&others
            other_only=others-sets["TS"]
            def excess(s): return (1 if a in s else 0)-len(s)/N
            total=excess(sets["TS"]); u=excess(unique); sh=excess(shared); oo=excess(other_only)
            if abs(total-(u+sh))>1e-12: raise SystemExit("TS_DECOMPOSITION_IDENTITY_FAIL")
            row={
              "source_id":sid,"prefix_index":pi,"action":a,
              "ts_total":total,"ts_unique":u,"ts_shared":sh,"other_only":oo,
              "ts_size":len(sets["TS"]),"unique_size":len(unique),"shared_size":len(shared),
              "ts_match":a in sets["TS"],"unique_match":a in unique,"shared_match":a in shared,
              "method_family":ctx[(sid,pi)].get("method_family") or "NULL",
              "cohort":ctx[(sid,pi)].get("cohort") or "NULL",
              "provenance":pclass.get(sid,"MISSING")
            }
            for r in ("H1","H2","H3","FS"):
                row["diff_TS_"+r]=total-excess(sets[r])
            for drop in ("H1","H2","H3","FS"):
                union3=set().union(*(sets[r] for r in ("H1","H2","H3","FS") if r!=drop))
                row["unique_without_"+drop]=excess(sets["TS"]-union3)
            states.append(row);by[sid].append(row)

    if len(by)!=60: raise SystemExit("SOLVES_60_REQUIRED")

    solves={}
    for sid,xs in by.items():
        solves[sid]={
          "source_id":sid,"method_family":xs[0]["method_family"],"cohort":xs[0]["cohort"],"provenance":xs[0]["provenance"],
          "states":len(xs),
          **{k:mean([x[k] for x in xs]) for k in ["ts_total","ts_unique","ts_shared","other_only"]+
             ["diff_TS_"+r for r in ("H1","H2","H3","FS")]+["unique_without_"+r for r in ("H1","H2","H3","FS")]}
        }

    unique_vals=[x["ts_unique"] for x in solves.values()]
    shared_vals=[x["ts_shared"] for x in solves.values()]
    total_vals=[x["ts_total"] for x in solves.values()]
    pair={}
    seed=20269010
    for r in ("H1","H2","H3","FS"):
        vals=[x["diff_TS_"+r] for x in solves.values()]
        pair[r]=summarize(vals,args.permutations,seed);seed+=1

    def groups(field,minn=3):
        g=defaultdict(list)
        for x in solves.values():g[x[field]].append(x["ts_unique"])
        return {k:summarize(v,args.permutations,20269100+i) for i,(k,v) in enumerate(sorted(g.items())) if len(v)>=minn}

    loo_cohort={}
    cohorts=defaultdict(set)
    for sid,x in solves.items():cohorts[x["cohort"]].add(sid)
    for c,ids in sorted(cohorts.items()):
        vals=[x["ts_unique"] for sid,x in solves.items() if sid not in ids]
        loo_cohort[c]={"held_out":len(ids),"remaining_mean":mean(vals)}

    ablations={}
    for i,r in enumerate(("H1","H2","H3","FS")):
        vals=[x["unique_without_"+r] for x in solves.values()]
        ablations[r]=summarize(vals,args.permutations,20269200+i)

    ts_matches=[x for x in states if x["ts_match"]]
    nonempty=[x for x in states if x["unique_size"]>0]
    total_excess=mean(total_vals); unique_excess=mean(unique_vals); shared_excess=mean(shared_vals)
    unique_stat=summarize(unique_vals,args.permutations,20269000)
    shared_stat=summarize(shared_vals,args.permutations,20269001)
    all_pair_positive=all(v["mean"] is not None and v["mean"]>0 for v in pair.values())
    if unique_excess is not None and unique_excess>0 and unique_stat["signflip_p"]<=0.05 and all_pair_positive:
        verdict="TS_SPECIFIC_DESCRIPTIVE_GEOMETRY_SUPPORTED"
    elif unique_excess is not None and unique_excess<=0 and shared_excess is not None and shared_excess>0:
        verdict="TS_SPECIFICITY_FAILURE_SHARED_SUPPORT_CARRIES_ALIGNMENT"
    else:
        verdict="PARTIAL_TS_SPECIFICITY"

    report={
      "schema_version":"g7-p9-rival-support-overlap-specificity-1",
      "operation_type":"Five-Rival Support-Overlap Specificity Audit",
      "states":len(states),"solves":len(solves),
      "identity_max_abs_error":max(abs(x["ts_total"]-(x["ts_unique"]+x["ts_shared"])) for x in states),
      "TS_total":summarize(total_vals,args.permutations,20268999),
      "TS_unique":unique_stat,
      "TS_shared":shared_stat,
      "other_only":summarize([x["other_only"] for x in solves.values()],args.permutations,20269002),
      "support_overlap":{
        "states_with_nonempty_TS_unique":len(nonempty),
        "solves_with_nonempty_TS_unique":len({x["source_id"] for x in nonempty}),
        "mean_TS_set_size":mean([x["ts_size"] for x in states]),
        "mean_TS_unique_size":mean([x["unique_size"] for x in states]),
        "mean_TS_shared_size":mean([x["shared_size"] for x in states]),
        "mean_TS_redundancy_share":mean([x["shared_size"]/x["ts_size"] for x in states if x["ts_size"]>0]),
        "observed_TS_matches":len(ts_matches),
        "observed_TS_unique_matches":sum(x["unique_match"] for x in ts_matches),
        "observed_TS_shared_matches":sum(x["shared_match"] for x in ts_matches),
        "unique_fraction_of_TS_matches":sum(x["unique_match"] for x in ts_matches)/len(ts_matches) if ts_matches else None,
        "shared_fraction_of_TS_matches":sum(x["shared_match"] for x in ts_matches)/len(ts_matches) if ts_matches else None,
        "unique_fraction_of_total_TS_excess":unique_excess/total_excess if total_excess else None,
        "shared_fraction_of_total_TS_excess":shared_excess/total_excess if total_excess else None
      },
      "pairwise_TS_minus_rival":pair,
      "TS_unique_by_method_min3":groups("method_family",3),
      "TS_unique_by_provenance_min3":groups("provenance",3),
      "leave_one_other_rival_out_unique":ablations,
      "leave_one_cohort_out_TS_unique":loo_cohort,
      "verdict":verdict,
      "boundary":[
        "Support-set overlap is computational geometry, not a psychological representation.",
        "TS_unique is defined against the union of H1/H2/H3/FS on the same frozen states.",
        "Solve is the independent unit for sign-flip diagnostics.",
        "Subgroup and ablation readouts are descriptive stress tests.",
        "No result promotes TS or any rival to a human cognitive mechanism."
      ]
    }
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/"rival-support-overlap-specificity.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P9_RIVAL_OVERLAP_AUDIT_PASS")
    print("VERDICT\t"+verdict)
    print("TS_TOTAL\t"+json.dumps(report["TS_total"],sort_keys=True))
    print("TS_UNIQUE\t"+json.dumps(unique_stat,sort_keys=True))
    print("TS_SHARED\t"+json.dumps(shared_stat,sort_keys=True))
    print("OVERLAP\t"+json.dumps(report["support_overlap"],sort_keys=True))
    print("PAIRWISE\t"+json.dumps(pair,sort_keys=True))

if __name__=="__main__":
    main()
