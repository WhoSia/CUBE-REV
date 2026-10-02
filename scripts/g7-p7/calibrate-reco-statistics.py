#!/usr/bin/env python3
import argparse, csv, json, math, random, statistics
from collections import defaultdict

RIVALS = {
    "H1": ("h1_best","observed_match_h1"),
    "H2": ("h2_best","observed_match_h2"),
    "H3": ("h3_best","observed_match_h3"),
    "TS": ("ts_best","observed_match_ts"),
    "FS": ("fs_best","observed_match_fs"),
}

def mean(xs):
    return sum(xs)/len(xs) if xs else None

def median(xs):
    return statistics.median(xs) if xs else None

def signflip_p(values, permutations, seed):
    vals=[float(v) for v in values if v is not None and math.isfinite(float(v))]
    if not vals:
        return None
    obs=abs(sum(vals)/len(vals))
    rng=random.Random(seed)
    extreme=0
    for _ in range(permutations):
        m=sum(v*(1 if rng.random()<0.5 else -1) for v in vals)/len(vals)
        if abs(m)>=obs-1e-15:
            extreme+=1
    return (extreme+1)/(permutations+1)

def parse_set(s):
    if s is None or s=="":
        return []
    return [int(x) for x in s.split(",") if x!=""]

def load_context(path):
    out={}
    with open(path,encoding="utf-8") as f:
        for line in f:
            if line.strip():
                x=json.loads(line)
                out[(int(x["source_id"]),int(x["prefix_index"]))]=x
    return out

def load_features(path, ctx):
    rows=[]
    with open(path,encoding="utf-8",newline="") as f:
        rd=csv.DictReader(f,delimiter="\t")
        for x in rd:
            sid=int(x["source_id"]); pi=int(x["prefix_index"])
            c=ctx[(sid,pi)]
            row={
                "source_id":sid,
                "prefix_index":pi,
                "phase1_lb":int(x["phase1_lb"]),
                "is_g1":int(x["is_g1"]),
                "boundary_after":bool(c["boundary_after"]),
                "method_family":c.get("method_family"),
                "reconstructor":c.get("reconstructor"),
                "cohort":c.get("cohort"),
                "next_action":int(x["next_action"]),
                "mean_pairwise_jaccard_distance":float(x["mean_pairwise_jaccard_distance"]),
            }
            for name,(setcol,matchcol) in RIVALS.items():
                s=parse_set(x[setcol])
                match=int(x[matchcol])
                row[name+"_set_size"]=len(s)
                row[name+"_match"]=match
                row[name+"_excess"]=(match-len(s)/18.0) if match>=0 else None
            rows.append(row)
    return rows

def solve_choice_summaries(rows):
    by=defaultdict(list)
    for r in rows:
        if r["next_action"]>=0:
            by[r["source_id"]].append(r)
    out={}
    for sid,xs in by.items():
        out[sid]={}
        for name in RIVALS:
            vals=[x[name+"_excess"] for x in xs if x[name+"_excess"] is not None]
            out[sid][name]=mean(vals)
        out[sid]["n_face_states"]=len(xs)
        out[sid]["method_family"]=xs[0].get("method_family")
        out[sid]["reconstructor"]=xs[0].get("reconstructor")
    return out

def boundary_matched(rows):
    bysolve=defaultdict(list)
    for r in rows:
        bysolve[r["source_id"]].append(r)
    solve_out={}
    for sid,xs in bysolve.items():
        strata=defaultdict(lambda:{"b":[],"n":[]})
        for r in xs:
            key=(r["phase1_lb"],r["is_g1"])
            strata[key]["b" if r["boundary_after"] else "n"].append(r["mean_pairwise_jaccard_distance"])
        num=0.0; den=0
        details=[]
        for key,d in sorted(strata.items()):
            if not d["b"] or not d["n"]:
                continue
            delta=mean(d["b"])-mean(d["n"])
            w=min(len(d["b"]),len(d["n"]))
            num+=w*delta; den+=w
            details.append({"phase1_lb":key[0],"is_g1":key[1],"n_boundary":len(d["b"]),"n_nonboundary":len(d["n"]),"weight":w,"delta":delta})
        if den:
            solve_out[sid]={
                "matched_delta":num/den,
                "matched_weight":den,
                "matched_strata":details,
                "method_family":xs[0].get("method_family"),
                "reconstructor":xs[0].get("reconstructor")
            }
    return solve_out

def subgroup_choice(summaries, field, min_solves=5):
    values=defaultdict(list)
    for sid,x in summaries.items():
        values[x.get(field) or "NULL"].append(x)
    out={}
    for k,xs in sorted(values.items()):
        if len(xs)<min_solves:
            continue
        out[k]={
            "solves":len(xs),
            "mean_excess":{name:mean([x[name] for x in xs if x[name] is not None]) for name in RIVALS}
        }
    return out

def subgroup_boundary(summaries, field, min_solves=5):
    values=defaultdict(list)
    for sid,x in summaries.items():
        values[x.get(field) or "NULL"].append(x)
    out={}
    for k,xs in sorted(values.items()):
        if len(xs)<min_solves:
            continue
        vals=[x["matched_delta"] for x in xs]
        out[k]={"solves":len(xs),"mean_matched_delta":mean(vals),"median_matched_delta":median(vals)}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--context",required=True)
    ap.add_argument("--features",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--permutations",type=int,default=100000)
    args=ap.parse_args()

    ctx=load_context(args.context)
    rows=load_features(args.features,ctx)
    choice=solve_choice_summaries(rows)
    boundary=boundary_matched(rows)

    choice_result={}
    for i,(name,_) in enumerate(RIVALS.items()):
        vals=[x[name] for x in choice.values() if x[name] is not None]
        face_rows=[r for r in rows if r["next_action"]>=0 and r[name+"_excess"] is not None]
        choice_result[name]={
            "face_states":len(face_rows),
            "mean_best_set_size":mean([r[name+"_set_size"] for r in face_rows]),
            "raw_match_rate":mean([r[name+"_match"] for r in face_rows]),
            "uniform_set_coverage":mean([r[name+"_set_size"]/18.0 for r in face_rows]),
            "state_mean_excess":mean([r[name+"_excess"] for r in face_rows]),
            "solve_mean_excess":mean(vals),
            "solve_median_excess":median(vals),
            "solve_signflip_p":signflip_p(vals,args.permutations,20261002+i),
            "positive_solves":sum(v>0 for v in vals),
            "zero_solves":sum(v==0 for v in vals),
            "negative_solves":sum(v<0 for v in vals),
            "solves":len(vals)
        }

    pairwise={}
    names=list(RIVALS)
    seed=20261100
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            a,b=names[i],names[j]
            vals=[x[a]-x[b] for x in choice.values() if x[a] is not None and x[b] is not None]
            pairwise[a+"__"+b]={
                "solves":len(vals),
                "mean_solve_excess_difference":mean(vals),
                "median_solve_excess_difference":median(vals),
                "solve_signflip_p":signflip_p(vals,args.permutations,seed),
                "a_better":sum(v>0 for v in vals),
                "tie":sum(v==0 for v in vals),
                "b_better":sum(v<0 for v in vals)
            }
            seed+=1

    bvals=[x["matched_delta"] for x in boundary.values()]
    report={
        "schema_version":"g7-p7-reco-statistical-calibration-result-1",
        "authority":"POST_DESCRIPTIVE_EXPLORATORY_CALIBRATION",
        "independent_unit":"solve",
        "rows":len(rows),
        "solves":len({r["source_id"] for r in rows}),
        "choice_calibration":choice_result,
        "pairwise_solve_calibration":pairwise,
        "progress_matched_boundary_calibration":{
            "eligible_solves":len(bvals),
            "mean_matched_delta":mean(bvals),
            "median_matched_delta":median(bvals),
            "positive_solves":sum(v>0 for v in bvals),
            "zero_solves":sum(v==0 for v in bvals),
            "negative_solves":sum(v<0 for v in bvals),
            "solve_signflip_p":signflip_p(bvals,args.permutations,20261003),
            "solve_rows":[{"source_id":sid,**x} for sid,x in sorted(boundary.items())]
        },
        "subgroups":{
            "choice_by_method_min5":subgroup_choice(choice,"method_family",5),
            "choice_by_reconstructor_min5":subgroup_choice(choice,"reconstructor",5),
            "boundary_by_method_min5":subgroup_boundary(boundary,"method_family",5),
            "boundary_by_reconstructor_min5":subgroup_boundary(boundary,"reconstructor",5)
        },
        "inference_boundary":[
            "This calibration was frozen after raw descriptive readout and is not preregistered confirmation.",
            "Solve, not state row, is the independent unit for sign-flip inference.",
            "Uniform set coverage is a calibration baseline, not a psychological random-choice model.",
            "Boundary matching controls only observed phase1_lb and G1 membership; residual progress and reconstruction-label confounding may remain.",
            "No computational rival is promoted to a human internal representation by this result."
        ]
    }
    import os
    os.makedirs(args.out,exist_ok=True)
    with open(os.path.join(args.out,"statistical-calibration.json"),"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2,ensure_ascii=False);f.write("\n")
    with open(os.path.join(args.out,"statistical-calibration-receipt.md"),"w",encoding="utf-8") as f:
        f.write("# G7-P7 reco.nz statistical calibration\n\n")
        for name,x in choice_result.items():
            f.write(f"- {name}: raw={x['raw_match_rate']:.6f}, coverage={x['uniform_set_coverage']:.6f}, solve excess={x['solve_mean_excess']:.6f}, p={x['solve_signflip_p']:.6g}\n")
        b=report["progress_matched_boundary_calibration"]
        f.write(f"- progress-matched boundary diversity delta: {b['mean_matched_delta']} over {b['eligible_solves']} solves; p={b['solve_signflip_p']}\n")
    print("G7_P7_RECO_STATISTICAL_CALIBRATION_PASS")
    for name,x in choice_result.items():
        print(f"{name}_RAW\t{x['raw_match_rate']}")
        print(f"{name}_COVERAGE\t{x['uniform_set_coverage']}")
        print(f"{name}_SOLVE_EXCESS\t{x['solve_mean_excess']}")
        print(f"{name}_P\t{x['solve_signflip_p']}")
    b=report["progress_matched_boundary_calibration"]
    print("BOUNDARY_MATCHED_SOLVES\t"+str(b["eligible_solves"]))
    print("BOUNDARY_MATCHED_DELTA\t"+str(b["mean_matched_delta"]))
    print("BOUNDARY_MATCHED_P\t"+str(b["solve_signflip_p"]))

if __name__=="__main__":
    main()
