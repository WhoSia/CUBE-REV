#!/usr/bin/env python3
import argparse, json
from collections import Counter

MANUAL_TO_BROAD = {
    "WCA_COMPETITION_ALIAS_PERSON_RESULT_SUPPORTED": "WCA_MANUAL_CONTEXT_RECOVERED_NOT_EXACT_LINKAGE",
    "WCA_PERSON_RESULT_SUPPORTED_SCRAMBLE_ASSIGNMENT_CONFLICT": "WCA_MANUAL_CONTEXT_RECOVERED_NOT_EXACT_LINKAGE",
    "WCA_PERSON_RESULT_SUPPORTED_NAME_VARIANT_SCRAMBLE_UNSUPPORTED": "WCA_MANUAL_CONTEXT_RECOVERED_NOT_EXACT_LINKAGE",
    "EXTERNAL_LEAGUE_SURFACE": "EXTERNAL_LEAGUE_SURFACE",
    "RECONSTRUCTION_DATABASE_SOURCE_LABEL": "RECONSTRUCTION_DATABASE_SOURCE_LABEL",
    "SOURCE_DECLARED_UNOFFICIAL": "SOURCE_DECLARED_UNOFFICIAL",
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-world",required=True)
    ap.add_argument("--recovery",required=True)
    args=ap.parse_args()

    sw=json.load(open(args.source_world,encoding="utf-8"))
    rec=json.load(open(args.recovery,encoding="utf-8"))

    manual={}
    for x in rec["manual_recovery_rows"]:
        sid=int(x["source_id"])
        cls=MANUAL_TO_BROAD.get(x["recovery_class"])
        if cls is None:
            raise SystemExit(f"UNKNOWN_MANUAL_CLASS:{x['recovery_class']}")
        if sid in manual:
            raise SystemExit(f"DUP_MANUAL:{sid}")
        manual[sid]=cls

    expected={}
    for x in sw["rows"]:
        sid=int(x["source_id"])
        if sid in manual:
            cls=manual[sid]
        elif x["source_world_support"]=="WCA_EXACT_ATTEMPT_LINKED":
            cls="WCA_EXACT_ATTEMPT_LINKED"
        elif x["source_world_support"]=="WCA_ATTEMPT_CONTEXT_SUPPORTED_SCRAMBLE_UNSUPPORTED":
            cls="WCA_CONTEXT_SUPPORTED_SCRAMBLE_UNSUPPORTED"
        elif x["source_world_support"]=="NO_EXACT_WCA_COMPETITION_CONTEXT_MATCH" and x.get("competition_source")=="unofficial":
            cls="SOURCE_DECLARED_UNOFFICIAL"
        elif x["source_world_support"]=="NO_SOURCE_COMPETITION_CONTEXT":
            cls="NO_SOURCE_COMPETITION_CONTEXT"
        else:
            raise SystemExit(f"UNRESOLVED_SOURCE_ID:{sid}:{x['source_world_support']}:{x.get('competition_source')}")
        expected[str(sid)]=cls

    actual={str(k):v for k,v in rec["source_id_to_broad_provenance_class"].items()}
    if set(expected)!=set(actual):
        missing=sorted(set(expected)-set(actual), key=int)
        extra=sorted(set(actual)-set(expected), key=int)
        raise SystemExit(f"REGISTRY_ID_SET_MISMATCH missing={missing} extra={extra}")
    mismatches={k:(expected[k],actual[k]) for k in expected if expected[k]!=actual[k]}
    if mismatches:
        raise SystemExit("REGISTRY_CLASS_MISMATCH:"+json.dumps(mismatches,sort_keys=True))

    counts=Counter(actual.values())
    declared={k:v for k,v in rec["broad_provenance_support_census"].items() if k!="total"}
    if dict(counts)!=declared:
        raise SystemExit("REGISTRY_COUNT_MISMATCH expected="+json.dumps(dict(counts),sort_keys=True)+" declared="+json.dumps(declared,sort_keys=True))
    if len(actual)!=60 or rec["broad_provenance_support_census"]["total"]!=60:
        raise SystemExit("REGISTRY_60_INVARIANT")

    print("G7_P7_PROVENANCE_REGISTRY_EXACT_ID_CLASS_PASS")
    print("SOURCE_IDS\t60")
    print("CLASS_COUNTS\t"+json.dumps(dict(sorted(counts.items())),sort_keys=True))

if __name__=="__main__":
    main()
