#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,statistics
from collections import Counter,defaultdict

RIVALS={
  "H1":("h1_best","observed_match_h1"),
  "H2":("h2_best","observed_match_h2"),
  "H3":("h3_best","observed_match_h3"),
  "TS":("ts_best","observed_match_ts"),
  "FS":("fs_best","observed_match_fs"),
}
LOWER=-1.0
UPPER=17.0/18.0

def mean(xs): return sum(xs)/len(xs) if xs else None
def parse_set(s): return [int(x) for x in s.split(",") if x] if s else []
def nonempty(x): return x is not None and str(x).strip()!=""

def era(date):
    s=str(date or "")
    try: y=int(s[:4])
    except: return "ERA_UNKNOWN"
    if 2013<=y<=2016:return "E1_2013_2016"
    if 2017<=y<=2020:return "E2_2017_2020"
    if 2021<=y<=2024:return "E3_2021_2024"
    if 2025<=y<=2026:return "E4_2025_2026"
    return "OUTSIDE_PRESEALED_ERAS"

def freq_band(n):
    if n==1:return "singleton"
    if 2<=n<=9:return "sparse"
    if 10<=n<=49:return "mid"
    if 50<=n<=199:return "high"
    if n>=200:return "dominant"
    return "RECONSTRUCTOR_MISSING"

def load_context(path):
    out={}
    with open(path,encoding="utf-8") as f:
        for line in f:
            if line.strip():
                x=json.loads(line)
                out[(int(x["source_id"]),int(x["prefix_index"]))]=x
    return out

def load_solves(features,ctx):
    by=defaultdict(list)
    with open(features,encoding="utf-8",newline="") as f:
        rd=csv.DictReader(f,delimiter="\t")
        for x in rd:
            sid=int(x["source_id"]); pi=int(x["prefix_index"])
            if int(x["next_action"])<0: continue
            c=ctx[(sid,pi)]
            r={
              "source_id":sid,
              "method_family":c.get("method_family"),
              "reconstructor":c.get("reconstructor")
            }
            for name,(setcol,matchcol) in RIVALS.items():
                ss=parse_set(x[setcol]); m=int(x[matchcol])
                r[name]=(m-len(ss)/18.0) if m>=0 else None
            by[sid].append(r)
    out={}
    for sid,xs in by.items():
        out[sid]={
          "source_id":sid,
          "method_family":xs[0].get("method_family") or "METHOD_MISSING",
          "reconstructor":xs[0].get("reconstructor") or "RECONSTRUCTOR_MISSING",
          **{name:mean([x[name] for x in xs if x[name] is not None]) for name in RIVALS}
        }
    return out

def tvd(pop_counts,sample_counts,pop_n,sample_n):
    ks=set(pop_counts)|set(sample_counts)
    return .5*sum(abs(pop_counts.get(k,0)/pop_n-sample_counts.get(k,0)/sample_n) for k in ks)

def adversarial(supported_mass,supported_mean):
    u=1-supported_mass
    lo=supported_mass*supported_mean+u*LOWER
    hi=supported_mass*supported_mean+u*UPPER
    sign="POSITIVE_IDENTIFIED" if lo>0 else ("NEGATIVE_IDENTIFIED" if hi<0 else "UNIDENTIFIED")
    thresh=supported_mean/(1+supported_mean) if supported_mean>0 else None
    return {
      "lower":lo,"upper":hi,"sign":sign,
      "zero_support_mass":u,
      "positive_sign_max_zero_support_mass":thresh,
      "margin_to_positive_sign_flip_threshold":(thresh-u if thresh is not None else None)
    }

def axis_report(name,pop_assign,sample_assign,solves):
    pop_n=len(pop_assign); sample_n=len(sample_assign)
    pc=Counter(pop_assign.values()); sc=Counter(sample_assign.values())
    supported=sorted(k for k,n in pc.items() if n>0 and sc.get(k,0)>0)
    zero=sorted(k for k,n in pc.items() if n>0 and sc.get(k,0)==0)
    support_mass=sum(pc[k] for k in supported)/pop_n
    groups={}
    for k in sorted(sc):
        sids=[sid for sid,c in sample_assign.items() if c==k and sid in solves]
        groups[k]={
          "sample_n":len(sids),
          "population_n":pc.get(k,0),
          "population_share":pc.get(k,0)/pop_n,
          "sample_share":len(sids)/sample_n,
          "poststrat_factor":((pc.get(k,0)/pop_n)/(len(sids)/sample_n) if len(sids)>0 and pc.get(k,0)>0 else None),
          "rivals":{r:{"mean_excess":mean([solves[sid][r] for sid in sids if solves[sid][r] is not None])} for r in RIVALS}
        }
    overall={}
    for r in RIVALS:
        unweighted=mean([x[r] for x in solves.values() if x[r] is not None])
        class_means={k:groups[k]["rivals"][r]["mean_excess"] for k in supported}
        denom=sum(pc[k] for k in supported)/pop_n
        post=(sum((pc[k]/pop_n)*class_means[k] for k in supported)/denom) if denom>0 else None
        loo={}
        for drop in supported:
            keep=[k for k in supported if k!=drop]
            d=sum(pc[k] for k in keep)/pop_n
            loo[drop]=(sum((pc[k]/pop_n)*class_means[k] for k in keep)/d) if d>0 else None
        vals=[v for v in loo.values() if v is not None]
        overall[r]={
          "unweighted_60_mean_excess":unweighted,
          "poststrat_supported_mass_mean_excess":post,
          "leave_one_supported_class_out":loo,
          "loo_min":min(vals) if vals else None,
          "loo_max":max(vals) if vals else None,
          "adversarial_zero_support_bound":adversarial(support_mass,post) if post is not None else None
        }
    return {
      "axis":name,
      "population_n":pop_n,
      "sample_n":sample_n,
      "population_counts":dict(sorted(pc.items())),
      "sample_counts":dict(sorted(sc.items())),
      "tvd":tvd(pc,sc,pop_n,sample_n),
      "supported_classes":supported,
      "zero_sample_support_classes":zero,
      "positive_sample_support_population_mass":support_mass,
      "zero_sample_support_population_mass":1-support_mass,
      "groups":groups,
      "overall":overall
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--covariates",required=True)
    ap.add_argument("--census",required=True)
    ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--ontology",required=True)
    ap.add_argument("--context",required=True)
    ap.add_argument("--features",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    census=json.load(open(args.census,encoding="utf-8"))
    if census["frozen_3x3_rows"]!=10591 or census["solve_body_requests"]!=0:
        raise SystemExit("CENSUS_AUTHORITY_MISMATCH")

    cov={}
    for line in open(args.covariates,encoding="utf-8"):
        if line.strip():
            x=json.loads(line); cov[int(x["source_id"])]=x
    if len(cov)!=12941: raise SystemExit("COVARIATE_12941_REQUIRED")

    frozen={}
    for line in open(args.frozen_index,encoding="utf-8"):
        if line.strip():
            x=json.loads(line); frozen[int(x["source_id"])]=x
    three={sid:x for sid,x in frozen.items() if x.get("puzzle")=="3x3"}
    if len(three)!=10591: raise SystemExit("FROZEN_3X3_REQUIRED")

    ontology=json.load(open(args.ontology,encoding="utf-8"))
    rawmap={k:v["family"] for k,v in ontology["raw_label_map"].items()}
    fallback=ontology["fallback"]["family"]

    def pop_method(sid):
        x=cov[sid]
        if not x.get("live_present") or not nonempty(x.get("method_raw")): return "METHOD_MISSING"
        return rawmap.get(x["method_raw"],fallback)

    recon_counts=Counter(
      str(cov[sid]["reconstructor"]).strip()
      for sid in three
      if cov[sid].get("live_present") and nonempty(cov[sid].get("reconstructor"))
    )
    def pop_recon_raw(sid):
        x=cov[sid]
        if not x.get("live_present") or not nonempty(x.get("reconstructor")): return "RECONSTRUCTOR_MISSING"
        return str(x["reconstructor"]).strip()
    def recon_band_label(label):
        if label=="RECONSTRUCTOR_MISSING": return "RECONSTRUCTOR_MISSING"
        n=recon_counts.get(label,0)
        return freq_band(n) if n else "OUTSIDE_LIVE_POPULATION_SUPPORT"
    def pop_recon_band(sid): return recon_band_label(pop_recon_raw(sid))

    pop_method_assign={sid:pop_method(sid) for sid in three}
    pop_raw_recon_assign={sid:pop_recon_raw(sid) for sid in three}
    pop_band_assign={sid:pop_recon_band(sid) for sid in three}
    pop_joint_assign={sid:pop_method_assign[sid]+"::"+pop_band_assign[sid] for sid in three}
    pop_era_method={sid:era(three[sid].get("date"))+"::"+pop_method_assign[sid] for sid in three}
    pop_era_band={sid:era(three[sid].get("date"))+"::"+pop_band_assign[sid] for sid in three}

    ctx=load_context(args.context)
    solves=load_solves(args.features,ctx)
    if len(solves)!=60: raise SystemExit("SOLVES_60_REQUIRED")
    if not set(solves).issubset(three): raise SystemExit("SAMPLE_NOT_IN_FROZEN_POP")

    sample_method={sid:(solves[sid]["method_family"] or "METHOD_MISSING") for sid in solves}
    sample_raw_recon={sid:(str(solves[sid]["reconstructor"]).strip() if nonempty(solves[sid]["reconstructor"]) else "RECONSTRUCTOR_MISSING") for sid in solves}
    sample_band={sid:recon_band_label(sample_raw_recon[sid]) for sid in solves}
    sample_joint={sid:sample_method[sid]+"::"+sample_band[sid] for sid in solves}
    sample_era_method={sid:era(three[sid].get("date"))+"::"+sample_method[sid] for sid in solves}
    sample_era_band={sid:era(three[sid].get("date"))+"::"+sample_band[sid] for sid in solves}

    # Surface agreement diagnostic: body-derived labels vs newly re-read index labels on the same 60 IDs.
    method_agree=0; method_comp=0; recon_agree=0; recon_comp=0
    mismatches=[]
    for sid in sorted(solves):
        if cov[sid].get("live_present") and nonempty(cov[sid].get("method_raw")):
            method_comp+=1
            idxm=rawmap.get(cov[sid]["method_raw"],fallback)
            if idxm==sample_method[sid]: method_agree+=1
            else: mismatches.append({"source_id":sid,"field":"method_family","body":sample_method[sid],"index":idxm})
        if cov[sid].get("live_present") and nonempty(cov[sid].get("reconstructor")):
            recon_comp+=1
            idxr=str(cov[sid]["reconstructor"]).strip()
            if idxr==sample_raw_recon[sid]: recon_agree+=1
            else: mismatches.append({"source_id":sid,"field":"reconstructor","body":sample_raw_recon[sid],"index":idxr})

    axes={
      "method_family":axis_report("method_family",pop_method_assign,sample_method,solves),
      "reconstructor_frequency_band":axis_report("reconstructor_frequency_band",pop_band_assign,sample_band,solves),
      "method_x_reconstructor_band":axis_report("method_x_reconstructor_band",pop_joint_assign,sample_joint,solves),
      "raw_reconstructor_diagnostic":axis_report("raw_reconstructor_diagnostic",pop_raw_recon_assign,sample_raw_recon,solves),
      "era_x_method":axis_report("era_x_method",pop_era_method,sample_era_method,solves),
      "era_x_reconstructor_band":axis_report("era_x_reconstructor_band",pop_era_band,sample_era_band,solves)
    }

    primary=["method_family","reconstructor_frequency_band","method_x_reconstructor_band"]
    primary_status={}
    for ax in primary:
        ar=axes[ax]
        primary_status[ax]={}
        for r in ["TS","H1"]:
            rr=ar["overall"][r]
            b=rr["adversarial_zero_support_bound"]
            primary_status[ax][r]={
              "poststrat":rr["poststrat_supported_mass_mean_excess"],
              "zero_support_mass":ar["zero_sample_support_population_mass"],
              "adversarial_sign":b["sign"] if b else None,
              "lower_bound":b["lower"] if b else None
            }

    ts_all=all(primary_status[a]["TS"]["adversarial_sign"]=="POSITIVE_IDENTIFIED" for a in primary)
    h1_all=all(primary_status[a]["H1"]["adversarial_sign"]=="POSITIVE_IDENTIFIED" for a in primary)
    if ts_all and h1_all:
        verdict="TS_H1_SIGN_ROBUST_ACROSS_METHOD_RECONSTRUCTOR_SUPPORT_AXES"
    elif all((primary_status[a]["TS"]["poststrat"] or 0)>0 for a in primary):
        verdict="TS_SUPPORTED_CELL_DIRECTION_ROBUST_METHOD_RECONSTRUCTOR_POPULATION_SIGN_HOLD"
    else:
        verdict="METHOD_RECONSTRUCTOR_TRANSPORT_INSTABILITY"

    report={
      "schema_version":"g7-p8-method-reconstructor-geometry-transport-1",
      "operation_type":"Method×Reconstructor Population-Support & Geometry Transport Court",
      "frozen_population_rows_3x3":10591,
      "solve_body_geometry_rows":60,
      "index_covariate_coverage":{
        "method_3x3_coverage_of_frozen":census["method_3x3_coverage_of_frozen"],
        "reconstructor_3x3_coverage_of_frozen":census["reconstructor_3x3_coverage_of_frozen"],
        "frozen_3x3_ids_missing":census["frozen_3x3_ids_missing"]
      },
      "surface_agreement_60":{
        "method_comparable":method_comp,"method_agree":method_agree,
        "method_agreement_share":method_agree/method_comp if method_comp else None,
        "reconstructor_comparable":recon_comp,"reconstructor_agree":recon_agree,
        "reconstructor_agreement_share":recon_agree/recon_comp if recon_comp else None,
        "mismatches":mismatches
      },
      "reconstructor_population_distinct_nonempty":len(recon_counts),
      "axes":axes,
      "primary_status":primary_status,
      "verdict":verdict,
      "boundary":[
        "Index method/reconstructor fields are surface metadata, not independently validated cognitive labels.",
        "Descriptive post-stratification is not inverse-probability weighting.",
        "Zero-sample-support cells are not imputed; adversarial bounds use the full rival-excess range [-1,17/18].",
        "Raw reconstructor-label transport is diagnostic; the presealed primary reconstructor axis is frequency band.",
        "Current live index rows outside the frozen G7-P3 population receive zero analytical weight.",
        "No result identifies a human cognitive mechanism or authorizes human contact."
      ]
    }
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/"method-reconstructor-geometry-transport.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P8_METHOD_RECONSTRUCTOR_TRANSPORT_PASS")
    print("VERDICT\t"+verdict)
    print("METHOD_AGREEMENT\t"+str(report["surface_agreement_60"]["method_agreement_share"]))
    print("RECONSTRUCTOR_AGREEMENT\t"+str(report["surface_agreement_60"]["reconstructor_agreement_share"]))
    for ax in primary:
        a=axes[ax]
        print("AXIS\t"+ax+"\tZERO_SUPPORT_MASS="+str(a["zero_sample_support_population_mass"])+"\tTVD="+str(a["tvd"]))
        print("TS\t"+str(a["overall"]["TS"]))
        print("H1\t"+str(a["overall"]["H1"]))

if __name__=="__main__":
    main()
