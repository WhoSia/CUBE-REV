#!/usr/bin/env python3
import argparse,json,pathlib,math

LOW=-1.0
HIGH=17.0/18.0

def sign(x):
    if x is None: return "NA"
    return "POSITIVE" if x>0 else ("NEGATIVE" if x<0 else "ZERO")

def bound(supported_mass, supported_mean):
    u=1-supported_mass
    lo=supported_mass*supported_mean+u*LOW
    hi=supported_mass*supported_mean+u*HIGH
    s="POSITIVE_IDENTIFIED" if lo>0 else ("NEGATIVE_IDENTIFIED" if hi<0 else "UNIDENTIFIED")
    return {"supported_mass":supported_mass,"zero_support_mass":u,"lower":lo,"upper":hi,"sign":s}

def conditional_axis(axis, exclude=None):
    exclude=set(exclude or [])
    groups=axis["groups"]
    keep=[(k,g) for k,g in groups.items() if k not in exclude and g["sample_n"]>0 and g["population_n"]>0]
    mass=sum(g["population_share"] for _,g in keep)
    out={}
    for r in ["TS","H1","H2","H3","FS"]:
        val=sum(g["population_share"]*g["rivals"][r]["mean_excess"] for _,g in keep)/mass if mass else None
        out[r]=val
    return {"population_mass":mass,"means":out}

def era_reports(axis):
    eras={}
    for key,g in axis["groups"].items():
        era,cell=key.split("::",1)
        eras.setdefault(era,[]).append((cell,g))
    out={}
    for era,cells in sorted(eras.items()):
        total_pop=sum(g["population_n"] for _,g in cells)
        supported=[(c,g) for c,g in cells if g["sample_n"]>0]
        supported_pop=sum(g["population_n"] for _,g in supported)
        sm=supported_pop/total_pop if total_pop else 0
        rr={}
        for r in ["TS","H1"]:
            m=(sum(g["population_n"]*g["rivals"][r]["mean_excess"] for _,g in supported)/supported_pop) if supported_pop else None
            rr[r]={"poststrat_supported_mean":m,"sign":sign(m),"adversarial":bound(sm,m) if m is not None else None}
        out[era]={
          "population_n":total_pop,
          "supported_population_n":supported_pop,
          "supported_mass":sm,
          "zero_support_cells":[c for c,g in cells if g["sample_n"]==0 and g["population_n"]>0],
          "rivals":rr
        }
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--court",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    x=json.load(open(args.court,encoding="utf-8"))
    if x["frozen_population_rows_3x3"]!=10591 or x["solve_body_geometry_rows"]!=60:
        raise SystemExit("P8_COURT_AUTHORITY_MISMATCH")

    method=x["axes"]["method_family"]
    method_loo={}
    reversals={"TS":[],"H1":[]}
    contributions={}
    for r in ["TS","H1"]:
        full=method["overall"][r]["poststrat_supported_mass_mean_excess"]
        loo=method["overall"][r]["leave_one_supported_class_out"]
        method_loo[r]={}
        contributions[r]={}
        for cls,g in method["groups"].items():
            if g["sample_n"]<=0 or g["population_n"]<=0: continue
            v=loo.get(cls)
            method_loo[r][cls]={
              "leave_out_mean":v,
              "leave_out_sign":sign(v),
              "delta_full_minus_leave_out":full-v if v is not None else None
            }
            if v is not None and sign(v)!=sign(full): reversals[r].append(cls)
            contributions[r][cls]=g["population_share"]*g["rivals"][r]["mean_excess"]

    non_cfop=conditional_axis(method,exclude=["CFOP"])

    era_method=era_reports(x["axes"]["era_x_method"])
    era_recon=era_reports(x["axes"]["era_x_reconstructor_band"])
    era_reversals={
      "method_TS":[e for e,v in era_method.items() if v["rivals"]["TS"]["sign"]!="POSITIVE"],
      "method_H1":[e for e,v in era_method.items() if v["rivals"]["H1"]["sign"]!="POSITIVE"],
      "reconstructor_TS":[e for e,v in era_recon.items() if v["rivals"]["TS"]["sign"]!="POSITIVE"],
      "reconstructor_H1":[e for e,v in era_recon.items() if v["rivals"]["H1"]["sign"]!="POSITIVE"]
    }

    joint=x["axes"]["method_x_reconstructor_band"]
    joint_margin={}
    for r in ["TS","H1"]:
        b=joint["overall"][r]["adversarial_zero_support_bound"]
        joint_margin[r]={
          "poststrat":joint["overall"][r]["poststrat_supported_mass_mean_excess"],
          "zero_support_mass":joint["zero_sample_support_population_mass"],
          "adversarial_lower":b["lower"],
          "adversarial_sign":b["sign"],
          "margin_to_positive_sign_flip_threshold":b["margin_to_positive_sign_flip_threshold"]
        }

    ts_robust=(len(reversals["TS"])==0 and not era_reversals["method_TS"] and not era_reversals["reconstructor_TS"])
    h1_cfop_only=(reversals["H1"]==["CFOP"])
    if ts_robust and h1_cfop_only:
        verdict="TS_COMPOSITION_ROBUST_H1_CFOP_CRITICAL_METHOD_SENSITIVE"
    elif ts_robust and reversals["H1"]:
        verdict="TS_COMPOSITION_ROBUST_H1_METHOD_COMPOSITION_SENSITIVE"
    elif not ts_robust:
        verdict="TS_TEMPORAL_OR_METHOD_COMPOSITION_INSTABILITY"
    else:
        verdict="NO_METHOD_DOMINANCE_REVERSAL_DETECTED"

    report={
      "schema_version":"g7-p8-r1-method-dominance-sensitivity-1",
      "operation_type":"Method-Dominance Sensitivity Stress Test",
      "p8_parent_verdict":x["verdict"],
      "method_leave_one_out":method_loo,
      "method_sign_reversals":reversals,
      "population_weighted_method_contributions":contributions,
      "non_cfop_conditional":non_cfop,
      "era_x_method":era_method,
      "era_x_reconstructor_band":era_recon,
      "era_nonpositive":era_reversals,
      "joint_axis_margin":joint_margin,
      "surface_agreement_60":x["surface_agreement_60"],
      "verdict":verdict,
      "boundary":[
        "This is a post-Court sensitivity decomposition; it does not create a new confirmatory claim.",
        "Method labels are reconstruction metadata, not latent cognitive-state labels.",
        "Population-weighted contribution is descriptive and not causal attribution.",
        "Era analyses retain zero-support cells explicitly and use full-range adversarial bounds.",
        "No result identifies a human cognitive mechanism."
      ]
    }
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/"method-dominance-sensitivity.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P8_R1_METHOD_DOMINANCE_SENSITIVITY_PASS")
    print("VERDICT\t"+verdict)
    print("TS_REVERSALS\t"+json.dumps(reversals["TS"]))
    print("H1_REVERSALS\t"+json.dumps(reversals["H1"]))
    print("NON_CFOP_TS\t"+str(non_cfop["means"]["TS"]))
    print("NON_CFOP_H1\t"+str(non_cfop["means"]["H1"]))
    print("ERA_NONPOSITIVE\t"+json.dumps(era_reversals,sort_keys=True))
    print("JOINT_TS\t"+json.dumps(joint_margin["TS"],sort_keys=True))
    print("JOINT_H1\t"+json.dumps(joint_margin["H1"],sort_keys=True))

if __name__=="__main__":
    main()
