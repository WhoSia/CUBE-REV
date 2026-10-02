#!/usr/bin/env python3
import argparse,json,pathlib,math

RIVALS=["H1","H2","H3","TS","FS"]
LOWER=-1.0
UPPER=17.0/18.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--transport",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    x=json.load(open(args.transport,encoding="utf-8"))
    s=float(x["supported_population_mass"])
    u=float(x["unidentified_population_mass"])
    if abs((s+u)-1.0)>1e-9: raise SystemExit("MASS_NOT_ONE")

    rivals={}
    for name in RIVALS:
        m=float(x["overall"][name]["poststrat_supported_mass_mean_excess"])
        lo=s*m+u*LOWER
        hi=s*m+u*UPPER
        if lo>0:
            sign="POSITIVE_IDENTIFIED"
        elif hi<0:
            sign="NEGATIVE_IDENTIFIED"
        else:
            sign="UNIDENTIFIED"
        # For positive supported mean and worst-case unknown=-1:
        # (1-u)*m-u>0 -> u < m/(1+m)
        if m>0:
            threshold=m/(1.0+m)
            margin=threshold-u
        elif m<0:
            threshold=None; margin=None
        else:
            threshold=0.0; margin=-u
        rivals[name]={
          "supported_poststrat_mean":m,
          "full_population_lower_bound":lo,
          "full_population_upper_bound":hi,
          "population_sign":sign,
          "positive_sign_max_unidentified_mass":threshold,
          "current_unidentified_mass":u,
          "margin_to_positive_sign_flip_threshold":margin
        }

    primary=("TS","H1")
    if all(rivals[k]["population_sign"]=="POSITIVE_IDENTIFIED" for k in primary):
        verdict="TS_H1_POPULATION_SIGN_ROBUST_UNDER_FULL_RANGE_ADVERSARIAL_UNIDENTIFIED_MASS"
    else:
        verdict="PRIMARY_POPULATION_SIGN_HOLD"

    report={
      "schema_version":"g7-p7-adversarial-unidentified-mass-bound-1",
      "operation_type":"Adversarial Unidentified-Mass Sign-Bound Court",
      "authority":"POST_TRANSPORT_DETERMINISTIC_BOUND",
      "supported_population_mass":s,
      "unidentified_population_mass":u,
      "metric_bounds":{"lower":LOWER,"upper":UPPER},
      "rivals":rivals,
      "verdict":verdict,
      "boundary":[
        "Bounds use the full structural range of per-state rival excess and therefore require no distributional assumption for the unidentified provenance mass.",
        "The unidentified mass may have any mixture of solves and any dependence structure; only the metric range is used.",
        "Sign identification does not identify the mean magnitude inside the unidentified mass.",
        "The calculation addresses provenance-axis population completion only.",
        "No bound result promotes a rival to a human cognitive mechanism.",
        "No new source contact occurs."
      ]
    }
    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"adversarial-unidentified-mass-sign-bound.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P7_ADVERSARIAL_UNIDENTIFIED_MASS_BOUND_PASS")
    for k in RIVALS:
        r=rivals[k]
        print(f"{k}\tLOW={r['full_population_lower_bound']}\tHIGH={r['full_population_upper_bound']}\tSIGN={r['population_sign']}\tTHRESH={r['positive_sign_max_unidentified_mass']}\tMARGIN={r['margin_to_positive_sign_flip_threshold']}")
    print("VERDICT\t"+verdict)

if __name__=="__main__":
    main()
