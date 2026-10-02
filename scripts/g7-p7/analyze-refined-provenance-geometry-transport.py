#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,statistics
from collections import defaultdict,Counter

RIVALS={
  "H1":("h1_best","observed_match_h1"),
  "H2":("h2_best","observed_match_h2"),
  "H3":("h3_best","observed_match_h3"),
  "TS":("ts_best","observed_match_ts"),
  "FS":("fs_best","observed_match_fs"),
}

def mean(xs): return sum(xs)/len(xs) if xs else None
def parse_set(s): return [int(x) for x in s.split(",") if x] if s else []

def load_context(path):
    out={}
    with open(path,encoding="utf-8") as f:
        for line in f:
            if line.strip():
                x=json.loads(line); out[(int(x["source_id"]),int(x["prefix_index"]))]=x
    return out

def load_solves(features,ctx):
    by=defaultdict(list)
    with open(features,encoding="utf-8",newline="") as f:
        rd=csv.DictReader(f,delimiter="\t")
        for x in rd:
            sid=int(x["source_id"]); pi=int(x["prefix_index"])
            if int(x["next_action"])<0: continue
            c=ctx[(sid,pi)]
            r={"method_family":c.get("method_family"),"reconstructor":c.get("reconstructor"),"boundary_after":bool(c.get("boundary_after"))}
            for name,(setcol,matchcol) in RIVALS.items():
                ss=parse_set(x[setcol]); m=int(x[matchcol])
                r[name]=(m-len(ss)/18.0) if m>=0 else None
            by[sid].append(r)
    out={}
    for sid,xs in by.items():
        out[sid]={
          "source_id":sid,
          "method_family":xs[0].get("method_family"),
          "reconstructor":xs[0].get("reconstructor"),
          **{name:mean([x[name] for x in xs if x[name] is not None]) for name in RIVALS},
          "boundary":{name:mean([x[name] for x in xs if x["boundary_after"] and x[name] is not None]) for name in RIVALS},
          "nonboundary":{name:mean([x[name] for x in xs if (not x["boundary_after"]) and x[name] is not None]) for name in RIVALS},
        }
    return out

def weighted_mean(class_means,pop_shares,classes):
    denom=sum(pop_shares[c] for c in classes)
    if denom<=0: return None
    return sum(pop_shares[c]*class_means[c] for c in classes)/denom

def summarize_cells(solves,classes,field,min_n=3):
    g=defaultdict(list)
    for sid,x in solves.items():
        g[(classes[sid],x.get(field) or "NULL")].append(x)
    out={}
    for (prov,val),xs in sorted(g.items()):
        if len(xs)<min_n: continue
        out[prov+"::"+val]={
          "provenance_class":prov,field:val,"solves":len(xs),
          "rivals":{name:{"mean_excess":mean([x[name] for x in xs if x[name] is not None])} for name in RIVALS}
        }
    return out

def boundary_groups(solves,classes,min_n=3):
    g=defaultdict(list)
    for sid,x in solves.items(): g[classes[sid]].append(x)
    out={}
    for prov,xs in sorted(g.items()):
        if len(xs)<min_n: continue
        rr={}
        for name in RIVALS:
            diffs=[]
            for x in xs:
                b=x["boundary"][name]; n=x["nonboundary"][name]
                if b is not None and n is not None: diffs.append(b-n)
            rr[name]={"paired_solves":len(diffs),"mean_boundary_minus_nonboundary":mean(diffs)}
        out[prov]={"solves":len(xs),"rivals":rr}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--context",required=True)
    ap.add_argument("--features",required=True)
    ap.add_argument("--transport",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    t=json.load(open(args.transport,encoding="utf-8"))
    if t["population_rows"]!=10591 or t["sample_rows"]!=60:
        raise SystemExit("TRANSPORT_AUTHORITY_MISMATCH")
    classes={int(k):v for k,v in t["sample_refined_source_ids"].items()}
    if len(classes)!=60: raise SystemExit("REFINED_SAMPLE_60_REQUIRED")
    pop_shares={k:v["share"] for k,v in t["refined_population"].items()}

    ctx=load_context(args.context)
    solves=load_solves(args.features,ctx)
    if set(solves)!=set(classes): raise SystemExit("SOLVE_CLASS_ID_SET_MISMATCH")

    grouped=defaultdict(list)
    for sid,x in solves.items(): grouped[classes[sid]].append(x)
    supported=sorted(grouped)
    absent=sorted(set(pop_shares)-set(supported))
    supported_mass=sum(pop_shares[c] for c in supported)
    absent_mass=sum(pop_shares[c] for c in absent)

    groups={}
    for c,xs in sorted(grouped.items()):
        groups[c]={
          "solves":len(xs),
          "population_share":pop_shares[c],
          "sample_share":len(xs)/60,
          "descriptive_poststrat_factor":pop_shares[c]/(len(xs)/60),
          "rivals":{name:{
             "mean_excess":mean([x[name] for x in xs if x[name] is not None]),
             "median_excess":statistics.median([x[name] for x in xs if x[name] is not None])
          } for name in RIVALS}
        }

    overall={}
    for name in RIVALS:
        unweighted=mean([x[name] for x in solves.values() if x[name] is not None])
        cm={c:groups[c]["rivals"][name]["mean_excess"] for c in supported}
        post=weighted_mean(cm,pop_shares,supported)
        loo={}
        for drop in supported:
            keep=[c for c in supported if c!=drop]
            loo[drop]=weighted_mean(cm,pop_shares,keep) if keep else None
        vals=[v for v in loo.values() if v is not None]
        overall[name]={
          "unweighted_60_mean_excess":unweighted,
          "poststrat_supported_mass_mean_excess":post,
          "supported_population_mass":supported_mass,
          "unidentified_population_mass":absent_mass,
          "leave_one_supported_class_out":loo,
          "loo_min":min(vals) if vals else None,
          "loo_max":max(vals) if vals else None,
          "direction_stable_unweighted_vs_poststrat":(unweighted==0 and post==0) or (unweighted is not None and post is not None and unweighted*post>0),
          "direction_stable_across_loo": all((post==0 and v==0) or (post*v>0) for v in vals) if post is not None else None
        }

    primary_ts=overall["TS"]
    if not primary_ts["direction_stable_unweighted_vs_poststrat"]:
        verdict="TRANSPORT_INSTABILITY"
    elif absent_mass>0.01:
        verdict="SUPPORTED_MASS_ROBUSTNESS_POPULATION_WIDE_HOLD"
    else:
        verdict="PROVENANCE_AXIS_TRANSPORT_SUPPORT"

    report={
      "schema_version":"g7-p7-refined-provenance-geometry-transport-court-1",
      "operation_type":"Refined Provenance-Conditioned Five-Rival Geometry Transport Court",
      "authority":"POST_V2_GEOMETRY_TRANSPORT_STRESS",
      "solves":60,
      "population_rows":10591,
      "supported_classes":supported,
      "absent_population_classes":absent,
      "supported_population_mass":supported_mass,
      "unidentified_population_mass":absent_mass,
      "groups":groups,
      "overall":overall,
      "provenance_x_method_min3":summarize_cells(solves,classes,"method_family",3),
      "provenance_x_reconstructor_min3":summarize_cells(solves,classes,"reconstructor",3),
      "within_refined_provenance_boundary_vs_nonboundary_min3":boundary_groups(solves,classes,3),
      "verdict":verdict,
      "boundary":[
        "Post-stratification factors are descriptive; the 60-body corpus is not a probability sample.",
        "Means are renormalized only over population classes with positive sample support.",
        "Zero-support population classes are never imputed.",
        "Method and reconstructor are not population-weighted because those covariates are unavailable for all 10,591 rows.",
        "Leave-one-supported-class-out ranges are sensitivity analyses, not confidence intervals.",
        "Provenance-axis transport support cannot identify a cognitive mechanism.",
        "No new reco.nz source contact occurs."
      ]
    }
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/"refined-provenance-five-rival-geometry-transport.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P7_REFINED_PROVENANCE_GEOMETRY_TRANSPORT_PASS")
    print("SUPPORTED_MASS\t"+str(supported_mass))
    print("UNIDENTIFIED_MASS\t"+str(absent_mass))
    for name in RIVALS:
        x=overall[name]
        print(f"{name}\tUNWEIGHTED={x['unweighted_60_mean_excess']}\tPOSTSTRAT={x['poststrat_supported_mass_mean_excess']}\tLOO=[{x['loo_min']},{x['loo_max']}]")
    print("VERDICT\t"+verdict)

if __name__=="__main__":
    main()
