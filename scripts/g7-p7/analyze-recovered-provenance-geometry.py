#!/usr/bin/env python3
import argparse, csv, json, math, os, random, statistics
from collections import Counter, defaultdict

RIVALS = {
    "H1": ("h1_best","observed_match_h1"),
    "H2": ("h2_best","observed_match_h2"),
    "H3": ("h3_best","observed_match_h3"),
    "TS": ("ts_best","observed_match_ts"),
    "FS": ("fs_best","observed_match_fs"),
}

def mean(xs): return sum(xs)/len(xs) if xs else None
def median(xs): return statistics.median(xs) if xs else None

def signflip_p(values, permutations, seed):
    vals=[float(v) for v in values if v is not None and math.isfinite(float(v))]
    if not vals: return None
    obs=abs(mean(vals))
    rng=random.Random(seed)
    extreme=0
    for _ in range(permutations):
        m=mean([v*(1 if rng.random()<0.5 else -1) for v in vals])
        if abs(m)>=obs-1e-15:
            extreme+=1
    return (extreme+1)/(permutations+1)

def parse_set(s):
    if not s: return []
    return [int(x) for x in s.split(",") if x!=""]

def load_context(path):
    out={}
    with open(path,encoding="utf-8") as f:
        for line in f:
            if line.strip():
                x=json.loads(line)
                out[(int(x["source_id"]),int(x["prefix_index"]))]=x
    return out

def load_solve_rows(features_path, ctx):
    by=defaultdict(list)
    with open(features_path,encoding="utf-8",newline="") as f:
        rd=csv.DictReader(f,delimiter="\t")
        for x in rd:
            sid=int(x["source_id"]); pi=int(x["prefix_index"])
            if int(x["next_action"])<0:
                continue
            c=ctx[(sid,pi)]
            r={
                "source_id":sid,
                "method_family":c.get("method_family"),
                "reconstructor":c.get("reconstructor"),
                "cohort":c.get("cohort"),
                "boundary_after":bool(c.get("boundary_after")),
            }
            for name,(setcol,matchcol) in RIVALS.items():
                s=parse_set(x[setcol]); match=int(x[matchcol])
                r[name]=(match-len(s)/18.0) if match>=0 else None
            by[sid].append(r)

    solves={}
    for sid,xs in by.items():
        solves[sid]={
            "source_id":sid,
            "method_family":xs[0].get("method_family"),
            "reconstructor":xs[0].get("reconstructor"),
            "cohort":xs[0].get("cohort"),
            "face_states":len(xs),
            **{name:mean([x[name] for x in xs if x[name] is not None]) for name in RIVALS},
            "boundary_excess":{name:mean([x[name] for x in xs if x["boundary_after"] and x[name] is not None]) for name in RIVALS},
            "nonboundary_excess":{name:mean([x[name] for x in xs if (not x["boundary_after"]) and x[name] is not None]) for name in RIVALS},
        }
    return solves

def summarize(xs, permutations, seed0):
    rivals={}
    seed=seed0
    for name in RIVALS:
        vals=[x[name] for x in xs if x.get(name) is not None]
        rivals[name]={
            "solves":len(vals),
            "mean_excess":mean(vals),
            "median_excess":median(vals),
            "positive":sum(v>0 for v in vals),
            "zero":sum(v==0 for v in vals),
            "negative":sum(v<0 for v in vals),
            "signflip_p":signflip_p(vals,permutations,seed),
        }
        seed+=1
    return {
        "solves":len(xs),
        "rivals":rivals,
        "method_counts":dict(sorted(Counter((x.get("method_family") or "NULL") for x in xs).items())),
        "reconstructor_counts":dict(sorted(Counter((x.get("reconstructor") or "NULL") for x in xs).items())),
        "cohort_counts":dict(sorted(Counter((x.get("cohort") or "NULL") for x in xs).items())),
    }

def cross_groups(solves, classes, field, min_n, permutations, seed0):
    g=defaultdict(list)
    for sid,x in solves.items():
        g[(classes[str(sid)],x.get(field) or "NULL")].append(x)
    out={}; seed=seed0
    for (prov,val),xs in sorted(g.items()):
        if len(xs)<min_n:
            continue
        out[prov+"::"+val]={
            "provenance_class":prov,
            field:val,
            **summarize(xs,permutations,seed),
        }
        seed+=100
    return out

def boundary_summary(solves, classes, min_n):
    grouped=defaultdict(list)
    for sid,x in solves.items():
        grouped[classes[str(sid)]].append(x)
    out={}
    for prov,xs in sorted(grouped.items()):
        if len(xs)<min_n:
            continue
        rv={}
        for name in RIVALS:
            bvals=[]; nvals=[]; diffs=[]
            for x in xs:
                b=x["boundary_excess"].get(name)
                n=x["nonboundary_excess"].get(name)
                if b is not None: bvals.append(b)
                if n is not None: nvals.append(n)
                if b is not None and n is not None: diffs.append(b-n)
            rv[name]={
                "solves_with_boundary":len(bvals),
                "solves_with_nonboundary":len(nvals),
                "paired_solves":len(diffs),
                "mean_boundary_excess":mean(bvals),
                "mean_nonboundary_excess":mean(nvals),
                "mean_within_solve_boundary_minus_nonboundary":mean(diffs),
            }
        out[prov]={"solves":len(xs),"rivals":rv}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--context",required=True)
    ap.add_argument("--features",required=True)
    ap.add_argument("--recovery",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--permutations",type=int,default=100000)
    args=ap.parse_args()

    ctx=load_context(args.context)
    solves=load_solve_rows(args.features,ctx)
    rec=json.load(open(args.recovery,encoding="utf-8"))
    classes={str(k):v for k,v in rec["source_id_to_broad_provenance_class"].items()}

    if set(map(str,solves))!=set(classes):
        missing=sorted(set(map(str,solves))-set(classes), key=int)
        extra=sorted(set(classes)-set(map(str,solves)), key=int)
        raise SystemExit(f"RECOVERED_PROVENANCE_ID_SET_MISMATCH missing={missing} extra={extra}")

    grouped=defaultdict(list)
    for sid,x in solves.items():
        grouped[classes[str(sid)]].append(x)

    groups={}; seed=20268000
    for prov,xs in sorted(grouped.items()):
        groups[prov]=summarize(xs,args.permutations,seed)
        seed+=100

    report={
        "schema_version":"g7-p7-recovered-provenance-five-rival-geometry-1",
        "operation_type":"Recovered-Provenance Geometry Stress Test",
        "authority":"POST_SOURCE_PROVENANCE_EXPLORATORY_STRESS_TEST",
        "independent_unit":"solve",
        "solves":len(solves),
        "provenance_class_counts":dict(sorted(Counter(classes.values()).items())),
        "groups":groups,
        "provenance_x_method_min3":cross_groups(solves,classes,"method_family",3,args.permutations,20269000),
        "provenance_x_reconstructor_min3":cross_groups(solves,classes,"reconstructor",3,args.permutations,20270000),
        "within_provenance_boundary_vs_nonboundary_min3":boundary_summary(solves,classes,3),
        "boundary":[
            "Broad provenance classes are observational support strata, not randomized treatments.",
            "Classes with fewer than 3 solves are descriptive only.",
            "Sign-flip p-values are exploratory diagnostics.",
            "Manual WCA context recovery remains below exact-attempt linkage authority.",
            "No provenance contrast can identify or promote a human cognitive mechanism.",
            "No new reco.nz source contact occurs."
        ]
    }
    os.makedirs(args.out,exist_ok=True)
    with open(os.path.join(args.out,"recovered-provenance-five-rival-geometry.json"),"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2,ensure_ascii=False); f.write("\n")
    print("G7_P7_RECOVERED_PROVENANCE_GEOMETRY_PASS")
    print("SOLVES\t"+str(report["solves"]))
    print("CLASS_COUNTS\t"+json.dumps(report["provenance_class_counts"],sort_keys=True))
    for prov,g in report["groups"].items():
        print("PROVENANCE\t"+prov+"\tN="+str(g["solves"])+"\tTS="+str(g["rivals"]["TS"]["mean_excess"])+"\tH1="+str(g["rivals"]["H1"]["mean_excess"]))

if __name__=="__main__":
    main()
