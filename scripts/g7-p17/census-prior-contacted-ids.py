#!/usr/bin/env python3
import argparse,hashlib,json,pathlib

def manifest_ids(path):
    x=json.load(open(path,encoding="utf-8"))
    return {int(r["source_id"]) for r in x["rows"]},x

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--legacy60",required=True)
    ap.add_argument("--p11",required=True)
    ap.add_argument("--p13-original",required=True)
    ap.add_argument("--p13-repaired",required=True)
    ap.add_argument("--p14-original",required=True)
    ap.add_argument("--p14-repaired",required=True)
    ap.add_argument("--p15-original",required=True)
    ap.add_argument("--p15-v3-amendment",required=True)
    ap.add_argument("--p15-v3-audit",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    legacy={int(x) for x in json.load(open(a.legacy60,encoding="utf-8"))["source_id_to_broad_provenance_class"]}
    p11,_=manifest_ids(a.p11)
    p13o,_=manifest_ids(a.p13_original);p13r,_=manifest_ids(a.p13_repaired)
    p14o,_=manifest_ids(a.p14_original);p14r,_=manifest_ids(a.p14_repaired)
    p15o,p15m=manifest_ids(a.p15_original)
    if len(legacy)!=60 or len(p11)!=40 or len(p13o)!=80 or len(p13r)!=80 or len(p14o)!=80 or len(p14r)!=80 or len(p15o)!=96:
        raise SystemExit("CARDINALITY_FAIL")
    prior267=legacy|p11|(p13o|p13r)|(p14o|p14r)
    if len(p13o|p13r)!=83:raise SystemExit("P13_83")
    if len(p14o|p14r)!=84:raise SystemExit("P14_84")
    if len(prior267)!=267:raise SystemExit(f"PRIOR267_{len(prior267)}")

    amend=json.load(open(a.p15_v3_amendment,encoding="utf-8"))
    if amend.get("status")!="FROZEN_BEFORE_ANY_P15_GEOMETRY":raise SystemExit("P15_V3_STATUS")
    prev={int(x) for x in amend["previously_contacted_repair_ids"]}
    audit=json.load(open(a.p15_v3_audit,encoding="utf-8"))
    audit_ids={int(x["source_id"]) for x in audit}
    p15_contact=p15o|prev|audit_ids
    all_contact=prior267|p15_contact
    if all_contact & set()==set(): pass
    rows=[]
    for sid in sorted(all_contact):
        tags=[]
        if sid in legacy:tags.append("LEGACY60")
        if sid in p11:tags.append("P11")
        if sid in p13o:tags.append("P13_ORIGINAL")
        if sid in p13r:tags.append("P13_REPAIRED")
        if sid in p14o:tags.append("P14_ORIGINAL")
        if sid in p14r:tags.append("P14_REPAIRED")
        if sid in p15o:tags.append("P15_ORIGINAL")
        if sid in prev:tags.append("P15_PREVIOUS_REPAIR_CONTACT")
        if sid in audit_ids:tags.append("P15_V3_SCAN_CONTACT")
        rows.append({"source_id":sid,"contact_tags":tags})
    canonical="\n".join(str(r["source_id"]) for r in rows)+"\n"
    sha=hashlib.sha256(canonical.encode()).hexdigest()
    report={
      "schema_version":"g7-p17-p1-prior-contact-census-1",
      "phase":"G7-P17-P1",
      "status":"SEALED_PRIOR_CONTACT_EXCLUSION_AUTHORITY",
      "counts":{
        "legacy60":len(legacy),"p11":len(p11),"p13_contact_union":len(p13o|p13r),
        "p14_contact_union":len(p14o|p14r),"prior_through_p14":len(prior267),
        "p15_original":len(p15o),"p15_previous_repair_contact_ids":len(prev),
        "p15_v3_scan_contact_ids":len(audit_ids),"p15_contact_union":len(p15_contact),
        "all_prior_contacted_through_p15":len(all_contact)
      },
      "p15_extra_beyond_original":sorted(p15_contact-p15o),
      "contacted_ids":rows,
      "exclusion_list_sha256":sha,
      "fresh_contact":0
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"prior-contact-census.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (out/"prior-contacted-source-ids.txt").write_text(canonical,encoding="utf-8")
    print("G7_P17_P1_PRIOR_CONTACT_CENSUS_PASS")
    print("COUNTS",json.dumps(report["counts"],sort_keys=True))
    print("P15_EXTRA",json.dumps(report["p15_extra_beyond_original"]))
    print("TOTAL",len(all_contact))
    print("SHA256",sha)

if __name__=="__main__":main()
