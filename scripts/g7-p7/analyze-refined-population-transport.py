#!/usr/bin/env python3
import argparse,json,pathlib
from collections import Counter

def shares(c,total):
    return {k:{"count":int(v),"share":v/total if total else None} for k,v in sorted(c.items())}

def tvd(a,b):
    ks=set(a)|set(b)
    return 0.5*sum(abs(a.get(k,0)-b.get(k,0)) for k in ks)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--index",required=True)
    ap.add_argument("--base-rows",required=True)
    ap.add_argument("--v2",required=True)
    ap.add_argument("--sample-registry",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    idx={}
    for line in open(args.index,encoding="utf-8"):
        if not line.strip(): continue
        x=json.loads(line)
        if x.get("puzzle")=="3x3":
            idx[int(x["source_id"])]=x
    if len(idx)!=10591: raise SystemExit("INDEX_3X3_10591_REQUIRED")

    base={}
    for line in open(args.base_rows,encoding="utf-8"):
        if line.strip():
            x=json.loads(line); base[int(x["source_id"])]=x
    if len(base)!=10591: raise SystemExit("BASE_ROWS_10591_REQUIRED")

    v2=json.load(open(args.v2,encoding="utf-8"))
    label_class={x["source_label"]:x["reconciliation_class"] for x in v2["labels"]}

    sample=json.load(open(args.sample_registry,encoding="utf-8"))
    sample_ids={int(x) for x in sample["source_id_to_broad_provenance_class"]}
    if len(sample_ids)!=60: raise SystemExit("SAMPLE_60_REQUIRED")

    def refined(source_id):
        b=base[source_id]["source_label_class"]
        if b!="OTHER_UNMATCHED_SOURCE_LABEL":
            return b
        label=idx[source_id].get("competition")
        v=label_class.get(label)
        mapping={
          "WCA_COMPETITION_ALIAS_STRONG_CONTEXT_RECOVERED_V2":"STRONG_WCA_ALIAS_RECOVERED_V2",
          "WCA_COMPETITION_ALIAS_EVIDENCE_CANDIDATE_V2":"EVIDENCE_CANDIDATE_V2",
          "NO_EXPLICIT_YEAR_NO_AUTO_RECOVERY":"NO_YEAR_NO_AUTO_RECOVERY",
          "NO_WCA_YEAR_WIDE_PERSON_RESULT_SUPPORT":"NO_YEAR_WIDE_SUPPORT"
        }
        if v not in mapping:
            raise SystemExit("V2_LABEL_CLASS_MISSING_"+str(label))
        return mapping[v]

    pop_classes={sid:refined(sid) for sid in idx}
    samp_classes={sid:pop_classes[sid] for sid in sample_ids}

    pop_count=Counter(pop_classes.values())
    samp_count=Counter(samp_classes.values())
    pop_share={k:v/10591 for k,v in pop_count.items()}
    samp_share={k:v/60 for k,v in samp_count.items()}

    old_pop=Counter(base[sid]["source_label_class"] for sid in idx)
    old_samp=Counter(base[sid]["source_label_class"] for sid in sample_ids)
    old_pop_share={k:v/10591 for k,v in old_pop.items()}
    old_samp_share={k:v/60 for k,v in old_samp.items()}

    absent={k:v for k,v in pop_count.items() if samp_count.get(k,0)==0}
    absent_mass=sum(absent.values())/10591

    # Strong alias rows gain competition-context authority. Exact person+result support
    # is counted conservatively from v2 best-candidate support_rows, not all alias rows.
    strong_labels=[x for x in v2["labels"] if x["reconciliation_class"]=="WCA_COMPETITION_ALIAS_STRONG_CONTEXT_RECOVERED_V2"]
    strong_alias_rows=sum(x["rows"] for x in strong_labels)
    strong_exact_support=sum((x.get("best_candidate") or {}).get("support_rows",0) for x in strong_labels)

    old_wca=Counter(base[sid]["wca_context_support"] for sid in idx)
    old_comp_context=10591-old_wca["NO_EXACT_WCA_COMPETITION_CONTEXT"]
    old_exact_result=old_wca["WCA_COMPETITION_SOLVER_RESULT_EXACT_CONTEXT"]

    # Descriptive post-stratification feasibility only: positive support classes.
    supported_mass=sum(v for k,v in pop_count.items() if samp_count.get(k,0)>0)/10591
    weights={}
    for k,n in samp_count.items():
        if n>0:
            weights[k]=(pop_count[k]/10591)/(n/60)

    out={
      "schema_version":"g7-p7-refined-population-provenance-transport-1",
      "operation_type":"Population Provenance Reconstitution & Selection-Transport Stress Test",
      "population_rows":10591,
      "sample_rows":60,
      "old_source_label_population":shares(old_pop,10591),
      "old_source_label_sample":shares(old_samp,60),
      "old_tvd":tvd(old_pop_share,old_samp_share),
      "refined_population":shares(pop_count,10591),
      "refined_sample":shares(samp_count,60),
      "refined_tvd":tvd(pop_share,samp_share),
      "sample_absent_population_classes":shares(Counter(absent),10591),
      "sample_absent_population_mass":absent_mass,
      "positive_support_population_mass":supported_mass,
      "descriptive_poststratification_weights":dict(sorted(weights.items())),
      "wca_context_reconstitution":{
        "old_competition_context_rows":old_comp_context,
        "strong_alias_rows_added_to_competition_context":strong_alias_rows,
        "refined_competition_context_rows":old_comp_context+strong_alias_rows,
        "old_exact_person_result_rows":old_exact_result,
        "strong_alias_exact_person_result_support_rows":strong_exact_support,
        "refined_exact_person_result_lower_bound":old_exact_result+strong_exact_support
      },
      "sample_refined_source_ids":{str(sid):cls for sid,cls in sorted(samp_classes.items())},
      "boundary":[
        "The 60-body corpus is not a probability sample; reported weights are descriptive post-stratification factors, not inverse-probability weights.",
        "No method/reconstructor population covariates are available, so transport is only evaluated on retained provenance classes.",
        "Population classes absent from the sample are non-transportable mass and are not imputed.",
        "Strong alias recovery establishes competition-context support, not exact attempt or scramble identity.",
        "Exact person+result reconstitution is a conservative lower bound based only on v2 supported rows.",
        "No cognitive-mechanism claim follows from transport similarity."
      ]
    }
    p=pathlib.Path(args.out);p.mkdir(parents=True,exist_ok=True)
    (p/"refined-population-provenance-transport.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P7_REFINED_POPULATION_TRANSPORT_PASS")
    print("OLD_TVD\t"+str(out["old_tvd"]))
    print("REFINED_TVD\t"+str(out["refined_tvd"]))
    print("ABSENT_MASS\t"+str(absent_mass))
    print("SUPPORTED_MASS\t"+str(supported_mass))
    print("REFINED_POP\t"+json.dumps({k:v["count"] for k,v in out["refined_population"].items()},sort_keys=True))
    print("REFINED_SAMPLE\t"+json.dumps({k:v["count"] for k,v in out["refined_sample"].items()},sort_keys=True))
    print("WCA_CONTEXT\t"+json.dumps(out["wca_context_reconstitution"],sort_keys=True))

if __name__=="__main__":
    main()
