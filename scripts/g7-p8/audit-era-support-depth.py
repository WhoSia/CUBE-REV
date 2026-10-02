#!/usr/bin/env python3
import argparse,json,pathlib
from collections import defaultdict

LOW=-1.0
HIGH=17.0/18.0
RIVALS=("TS","H1")

def sgn(x):
    if x is None:return "NA"
    if x>0:return "POSITIVE"
    if x<0:return "NEGATIVE"
    return "ZERO"

def adv(supported_mass,mean):
    if mean is None:return None
    u=1-supported_mass
    lo=supported_mass*mean+u*LOW
    hi=supported_mass*mean+u*HIGH
    sign="POSITIVE_IDENTIFIED" if lo>0 else ("NEGATIVE_IDENTIFIED" if hi<0 else "UNIDENTIFIED")
    return {"supported_mass":supported_mass,"zero_support_mass":u,"lower":lo,"upper":hi,"sign":sign}

def parse_axis(axis):
    pop_by_era=defaultdict(dict)
    for key,n in axis["population_counts"].items():
        era,cell=key.split("::",1)
        pop_by_era[era][cell]=int(n)
    group_by_era=defaultdict(dict)
    for key,g in axis["groups"].items():
        era,cell=key.split("::",1)
        group_by_era[era][cell]=g
    return pop_by_era,group_by_era

def weighted(cells,pop,groups,rival,total):
    supp=sum(pop[c] for c in cells)
    if not supp:return {"supported_population_n":0,"supported_mass":0,"mean":None,"adversarial":None}
    m=sum(pop[c]*groups[c]["rivals"][rival]["mean_excess"] for c in cells)/supp
    return {"supported_population_n":supp,"supported_mass":supp/total,"mean":m,"sign":sgn(m),"adversarial":adv(supp/total,m)}

def era_audit(axis,thresholds):
    pops,groups=parse_axis(axis)
    out={}
    for era,pop in sorted(pops.items()):
        era_groups=groups.get(era,{})
        total=sum(pop.values())
        all_supported=[c for c in pop if c in era_groups and era_groups[c]["sample_n"]>0]
        zero=[c for c in pop if c not in era_groups or era_groups[c]["sample_n"]==0]
        thresholds_out={}
        for k in thresholds:
            eligible=[c for c in all_supported if era_groups[c]["sample_n"]>=k]
            thresholds_out[str(k)]={
              "eligible_cells":eligible,
              "omitted_cells":[c for c in pop if c not in eligible],
              "rivals":{r:weighted(eligible,pop,era_groups,r,total) for r in RIVALS}
            }

        leverage={}
        for r in RIVALS:
            rows=[]
            for c in all_supported:
                m=era_groups[c]["rivals"][r]["mean_excess"]
                rows.append({
                  "cell":c,
                  "population_n":pop[c],
                  "population_share_within_era":pop[c]/total,
                  "sample_n":era_groups[c]["sample_n"],
                  "cell_mean":m,
                  "signed_population_contribution":(pop[c]/total)*m,
                  "absolute_population_contribution":abs((pop[c]/total)*m)
                })
            leverage[r]=sorted(rows,key=lambda z:(-z["absolute_population_contribution"],z["cell"]))

        loo={}
        for drop in all_supported:
            keep=[c for c in all_supported if c!=drop]
            loo[drop]={
              "dropped_population_n":pop[drop],
              "dropped_sample_n":era_groups[drop]["sample_n"],
              "rivals":{r:weighted(keep,pop,era_groups,r,total) for r in RIVALS}
            }

        out[era]={
          "population_n":total,
          "population_cells":dict(sorted(pop.items())),
          "sample_observed_cells":sorted(all_supported),
          "zero_sample_cells":sorted(zero),
          "zero_sample_population_n":sum(pop[c] for c in zero),
          "threshold_sweep":thresholds_out,
          "cell_leverage":leverage,
          "leave_one_cell_out":loo
        }
    return out

def find_drop(report,era,cell):
    return report.get(era,{}).get("leave_one_cell_out",{}).get(cell)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--court",required=True)
    ap.add_argument("--r1",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    court=json.load(open(args.court,encoding="utf-8"))
    r1=json.load(open(args.r1,encoding="utf-8"))
    if court["frozen_population_rows_3x3"]!=10591: raise SystemExit("COURT_POPULATION_MISMATCH")
    if r1["operation_type"]!="Method-Dominance Sensitivity Stress Test": raise SystemExit("R1_AUTHORITY_MISMATCH")
    thresholds=[1,2,3,5]
    method=era_audit(court["axes"]["era_x_method"],thresholds)
    recon=era_audit(court["axes"]["era_x_reconstructor_band"],thresholds)

    # Compare R1's group-only era denominator with repaired parent population_counts denominator.
    repairs=[]
    for axis_name,new,old in [
      ("era_x_method",method,r1["era_x_method"]),
      ("era_x_reconstructor_band",recon,r1["era_x_reconstructor_band"])
    ]:
        for era in sorted(new):
            oldrow=old.get(era)
            for rival in RIVALS:
                oldmean=(oldrow or {}).get("rivals",{}).get(rival,{}).get("poststrat_supported_mean")
                fresh=new[era]["threshold_sweep"]["1"]["rivals"][rival]
                repairs.append({
                  "axis":axis_name,"era":era,"rival":rival,
                  "r1_supported_mean":oldmean,
                  "repaired_supported_mean":fresh["mean"],
                  "repaired_supported_mass":fresh["supported_mass"],
                  "repaired_adversarial_sign":fresh["adversarial"]["sign"] if fresh["adversarial"] else None,
                  "repaired_lower":fresh["adversarial"]["lower"] if fresh["adversarial"] else None,
                  "repaired_upper":fresh["adversarial"]["upper"] if fresh["adversarial"] else None
                })

    # Explicit leverage diagnostics frozen in preseal.
    e2_dom=find_drop(recon,"E2_2017_2020","dominant")
    e4_zb=find_drop(method,"E4_2025_2026","ZB")

    identified_nonpositive={"TS":[],"H1":[]}
    sparse_sensitive={"TS":[],"H1":[]}
    for axis_name,rr in [("method",method),("reconstructor",recon)]:
        for era,e in rr.items():
            for rival in RIVALS:
                k1=e["threshold_sweep"]["1"]["rivals"][rival]
                k3=e["threshold_sweep"]["3"]["rivals"][rival]
                if k1["adversarial"] and k1["adversarial"]["sign"] in ("NEGATIVE_IDENTIFIED","ZERO"):
                    identified_nonpositive[rival].append(axis_name+"::"+era)
                if k1["adversarial"] and k1["adversarial"]["sign"]!="UNIDENTIFIED":
                    if (not k3["adversarial"]) or k3["adversarial"]["sign"]=="UNIDENTIFIED" or k3["adversarial"]["sign"]!=k1["adversarial"]["sign"]:
                        sparse_sensitive[rival].append(axis_name+"::"+era)

    if not identified_nonpositive["TS"]:
        ts_status="NO_IDENTIFIED_TEMPORAL_TS_SIGN_REVERSAL_AFTER_ZERO_SUPPORT_REPAIR"
    else:
        ts_status="IDENTIFIED_TS_TEMPORAL_NONPOSITIVE_ERA_REMAINS"
    if "method::E4_2025_2026" in identified_nonpositive["H1"] and "method::E4_2025_2026" in sparse_sensitive["H1"]:
        h1_status="E4_METHOD_H1_NEGATIVE_AT_K1_BUT_SPARSE_SUPPORT_SENSITIVE"
    elif identified_nonpositive["H1"]:
        h1_status="IDENTIFIED_H1_TEMPORAL_NONPOSITIVE_ERA_REMAINS"
    else:
        h1_status="NO_IDENTIFIED_TEMPORAL_H1_SIGN_REVERSAL_AFTER_ZERO_SUPPORT_REPAIR"

    report={
      "schema_version":"g7-p8-r2-era-support-depth-audit-1",
      "operation_type":"Era×Composition Support-Depth Audit",
      "thresholds":thresholds,
      "era_x_method":method,
      "era_x_reconstructor_band":recon,
      "r1_accounting_repair":repairs,
      "explicit_leverage_deletions":{
        "E2_reconstructor_dominant":e2_dom,
        "E4_method_ZB":e4_zb
      },
      "identified_nonpositive_full_era":identified_nonpositive,
      "sparse_support_sensitive":sparse_sensitive,
      "TS_status":ts_status,
      "H1_status":h1_status,
      "verdict":ts_status+"__"+h1_status,
      "boundary":[
        "R1 era summaries omitted zero-sample population cells from era denominators; R2 repairs this using parent Court population_counts.",
        "Threshold sweeps are post-R1 diagnostics, not confirmatory tests.",
        "Cells below the threshold are treated as unidentified population mass and receive full-range adversarial bounds; they are never imputed.",
        "A sample-supported negative cell mean is not an identified era-level population sign unless the full-era adversarial bound remains nonpositive.",
        "Method/reconstructor metadata are observational support strata, not cognitive mechanisms."
      ]
    }
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/"era-support-depth-audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P8_R2_ERA_SUPPORT_DEPTH_AUDIT_PASS")
    print("VERDICT\t"+report["verdict"])
    print("IDENTIFIED_NONPOSITIVE\t"+json.dumps(identified_nonpositive,sort_keys=True))
    print("SPARSE_SENSITIVE\t"+json.dumps(sparse_sensitive,sort_keys=True))
    for tag,row in report["explicit_leverage_deletions"].items():
        print("DROP\t"+tag+"\t"+json.dumps(row,sort_keys=True))
    for x in repairs:
        if x["axis"]=="era_x_reconstructor_band" and x["era"]=="E2_2017_2020":
            print("E2_RECON_REPAIR\t"+json.dumps(x,sort_keys=True))

if __name__=="__main__":
    main()
