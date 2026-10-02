#!/usr/bin/env python3
import argparse, csv, json, math, random, statistics
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
    rng=random.Random(seed); extreme=0
    for _ in range(permutations):
        m=mean([v*(1 if rng.random()<0.5 else -1) for v in vals])
        if abs(m)>=obs-1e-15: extreme+=1
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

def load_choice(path,ctx):
    by=defaultdict(list)
    with open(path,encoding="utf-8",newline="") as f:
        rd=csv.DictReader(f,delimiter="\t")
        for x in rd:
            sid=int(x["source_id"]); pi=int(x["prefix_index"])
            if int(x["next_action"])<0: continue
            c=ctx[(sid,pi)]
            r={"source_id":sid,"method_family":c.get("method_family"),"reconstructor":c.get("reconstructor"),"cohort":c.get("cohort")}
            for name,(setcol,matchcol) in RIVALS.items():
                s=parse_set(x[setcol]); match=int(x[matchcol])
                r[name]=(match-len(s)/18.0) if match>=0 else None
            by[sid].append(r)
    out={}
    for sid,xs in by.items():
        out[sid]={
            "source_id":sid,
            "method_family":xs[0].get("method_family"),
            "reconstructor":xs[0].get("reconstructor"),
            "cohort":xs[0].get("cohort"),
            **{name:mean([x[name] for x in xs if x[name] is not None]) for name in RIVALS},
            "face_states":len(xs)
        }
    return out

def summarize(xs,permutations,seed0):
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
            "signflip_p":signflip_p(vals,permutations,seed)
        }
        seed+=1
    return {
      "solves":len(xs),
      "rivals":rivals,
      "method_counts":dict(sorted(Counter((x.get("method_family") or "NULL") for x in xs).items())),
      "reconstructor_counts":dict(sorted(Counter((x.get("reconstructor") or "NULL") for x in xs).items())),
      "cohort_counts":dict(sorted(Counter((x.get("cohort") or "NULL") for x in xs).items()))
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--context",required=True)
    ap.add_argument("--features",required=True)
    ap.add_argument("--source-world",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--permutations",type=int,default=100000)
    args=ap.parse_args()

    ctx=load_context(args.context)
    choice=load_choice(args.features,ctx)
    audit=json.load(open(args.source_world,encoding="utf-8"))
    worlds={int(x["source_id"]):x["source_world_support"] for x in audit["rows"]}

    grouped=defaultdict(list)
    for sid,x in choice.items():
        grouped[worlds.get(sid,"MISSING_SOURCE_WORLD")].append(x)

    report_groups={}
    seed=20264000
    for world,xs in sorted(grouped.items()):
        report_groups[world]=summarize(xs,args.permutations,seed)
        seed+=100

    # Observed support classes are selected, not randomized. Contrasts are descriptive only.
    contrasts={}
    exact=report_groups.get("WCA_EXACT_ATTEMPT_LINKED")
    for world,g in report_groups.items():
        if world=="WCA_EXACT_ATTEMPT_LINKED" or not exact: continue
        contrasts[world]={}
        for name in RIVALS:
            a=exact["rivals"][name]["mean_excess"]
            b=g["rivals"][name]["mean_excess"]
            contrasts[world][name]={
              "exact_linked_minus_group_mean_excess": None if a is None or b is None else a-b,
              "same_sign": None if a is None or b is None else ((a>0)==(b>0))
            }

    report={
      "schema_version":"g7-p7-source-world-five-rival-geometry-1",
      "operation_type":"Source-World Conditional Geometry Stress Test",
      "authority":"POST_LINKAGE_POST_SOURCE_WORLD_EXPLORATORY_STRESS_TEST",
      "independent_unit":"solve",
      "groups":report_groups,
      "exact_linked_descriptive_contrasts":contrasts,
      "boundary":[
        "Source-world support classes are observational and selected, not randomized.",
        "WCA context support without exact scramble is not official-attempt identity.",
        "Groups with small solve counts are reported descriptively and are not promoted by p-values.",
        "No source-world contrast may promote a computational rival to a human cognitive mechanism.",
        "No new reco.nz source contact occurs."
      ]
    }
    import os
    os.makedirs(args.out,exist_ok=True)
    with open(os.path.join(args.out,"source-world-five-rival-geometry.json"),"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2,ensure_ascii=False); f.write("\n")
    print("G7_P7_SOURCE_WORLD_FIVE_RIVAL_GEOMETRY_PASS")
    for world,g in report_groups.items():
        print("SOURCE_WORLD\t"+world+"\tN="+str(g["solves"])+"\tTS="+str(g["rivals"]["TS"]["mean_excess"])+"\tH1="+str(g["rivals"]["H1"]["mean_excess"]))

if __name__=="__main__":
    main()
