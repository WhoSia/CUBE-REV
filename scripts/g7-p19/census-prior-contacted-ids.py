#!/usr/bin/env python3
import argparse,hashlib,json,pathlib

def manifest_ids(path):
    x=json.load(open(path,encoding="utf-8"))
    return {int(r["source_id"]) for r in x["rows"]},x

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--prior368-census",required=True)
    ap.add_argument("--p17-selection",required=True)
    ap.add_argument("--p17-p3-receipt",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    prior=json.load(open(a.prior368_census,encoding="utf-8"))
    if prior["counts"]["all_prior_contacted_through_p15"]!=368:raise SystemExit("PRIOR368_REQUIRED")
    if prior["exclusion_list_sha256"]!="f714bec91222c7232eb1138a3a42caaf52f93abe75381aa0b448fe2cc1afa550":
        raise SystemExit("PRIOR368_SHA")
    prior_ids={int(r["source_id"]) for r in prior["contacted_ids"]}
    if len(prior_ids)!=368:raise SystemExit("PRIOR368_CARDINALITY")

    p17,p17m=manifest_ids(a.p17_selection)
    if len(p17)!=48:raise SystemExit("P17_ORIGINAL48_REQUIRED")
    if p17m.get("selection_manifest_sha256")!="4c315f97f5cb80476734d28f20f97716ded859e40f63b5ee0fb6e6d4e771ae1b":
        raise SystemExit("P17_SELECTION_SHA")

    p3=json.load(open(a.p17_p3_receipt,encoding="utf-8"))
    reps={int(x) for x in p3["freshness_ledger"]["new_unique_repair_candidates_contacted"]}
    if reps!={7865,12695}:raise SystemExit("P17_REPAIR_SET")
    all_ids=prior_ids|p17|reps
    if len(all_ids)!=418:raise SystemExit(f"CONTACT418_REQUIRED_{len(all_ids)}")

    rows=[]
    for sid in sorted(all_ids):
        tags=[]
        if sid in prior_ids:tags.append("PRIOR_THROUGH_P15")
        if sid in p17:tags.append("P17_ORIGINAL_SELECTION_CONTACT")
        if sid in reps:tags.append("P17_REPAIR_REPLACEMENT_CONTACT")
        rows.append({"source_id":sid,"contact_tags":tags})

    canonical="\n".join(str(r["source_id"]) for r in rows)+"\n"
    sha=hashlib.sha256(canonical.encode()).hexdigest()
    report={
      "schema_version":"g7-p19-p1-prior-contact-census-1",
      "phase":"G7-P19-P1",
      "status":"SEALED_PRIOR_CONTACT_EXCLUSION_AUTHORITY",
      "counts":{
        "prior_through_p15":len(prior_ids),
        "p17_original_selection_contacted":len(p17),
        "p17_unique_repair_replacements":len(reps),
        "all_prior_contacted_through_p17":len(all_ids)
      },
      "p17_repair_replacement_ids":sorted(reps),
      "contacted_ids":rows,
      "exclusion_list_sha256":sha,
      "fresh_contact":0
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"prior-contact-census.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (out/"prior-contacted-source-ids.txt").write_text(canonical,encoding="utf-8")
    print("G7_P19_P1_PRIOR_CONTACT_CENSUS_PASS")
    print("TOTAL",len(all_ids))
    print("REPAIRS",json.dumps(sorted(reps)))
    print("SHA256",sha)

if __name__=="__main__":main()
