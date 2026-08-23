#!/usr/bin/env python3
import csv, hashlib, json, math, os, re, statistics, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "CUBE-REV 0.10.5-R1.23"
UPSTREAM_REPO = "2017YANR02/cuberoot.me"
UPSTREAM_COMMIT = "e5a6bb14961b5b26c882f9fb3bf13d61d9eba890"
RECONS_BLOB = "681adbeba019ef1fc657d6927287fd00dbca6c87"
ATTEMPTS_BLOB = "78949e0be591c8d99dfa5e5e5754b76eb4013df9"
BASE = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_COMMIT}/data/recon_backup"
OUT = Path(os.environ.get("R123_OUT", "r1_23_out"))
OUT.mkdir(parents=True, exist_ok=True)

OLD_EVENT_MAP = {
    "3x3":"333", "2x2":"222", "OH":"333oh",
    "3BLD":"333bf", "4BLD":"444bf", "5BLD":"555bf",
    "5x5":"555", "6x6":"666", "7x7":"777",
    "Pyraminx":"pyram", "Skewb":"skewb", "SQ1":"sq1",
    "Megaminx":"minx", "Clock":"clock",
}
OLD_ROUND_MAP = {
    "R1":["1","d"], "R2":["2","e"], "R3":["3","g"], "Fi":["f","c","b"]
}
# Pinned repo client semantics: wca-events.ts + wca-results-api.ts.
REPAIRED_EVENT_MAP = {
    "3x3":"333", "2x2":"222", "4x4":"444", "5x5":"555", "6x6":"666", "7x7":"777",
    "3bld":"333bf", "4bld":"444bf", "5bld":"555bf", "mbld":"333mbf",
    "oh":"333oh", "fmc":"333fm", "feet":"333ft",
    "pyra":"pyram", "pyraminx":"pyram", "mega":"minx", "megaminx":"minx",
    "square1":"sq1", "square-1":"sq1", "sq1":"sq1", "clock":"clock", "skewb":"skewb",
}
ROUND_VARIANTS = {
    "1":["1","b","d"],
    "2":["2","e"],
    "3":["3","g"],
    "f":["f","c","h"],
}
LEGACY_ROUND_TO_CANON = {"R1":"1","R2":"2","R3":"3","Fi":"f"}
NORMAL_TIMED = {
    "333","222","444","555","666","777","333bf","444bf","555bf","333oh",
    "minx","pyram","clock","skewb","sq1","333ft"
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def download(name, blob):
    url = f"{BASE}/{name}"
    data = urllib.request.urlopen(url, timeout=120).read()
    got = git_blob_sha1(data)
    if got != blob:
        raise RuntimeError(f"git blob mismatch for {name}: {got} != {blob}")
    (OUT / name).write_bytes(data)
    return data

def write_json(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def write_csv(name, rows, fields):
    with (OUT/name).open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def norm_event(x):
    if x is None: return ""
    s=str(x).strip().lower()
    return REPAIRED_EVENT_MAP.get(s, s)

def norm_round(x):
    if x is None: return None, "MISSING"
    s=str(x).strip()
    if s in ROUND_VARIANTS: return s, "CURRENT_RAW_RECON_ROUND"
    if s in LEGACY_ROUND_TO_CANON: return LEGACY_ROUND_TO_CANON[s], "LEGACY_DISPLAY_ROUND_NORMALIZED"
    return None, "UNRECOGNIZED_ROUND"

def recon_cs(r):
    # R1.21 verified source display semantics: millisecond cleanup then truncate to hundredths.
    x=r.get("rawTime")
    if isinstance(x,(int,float)) and math.isfinite(float(x)) and float(x)>=0:
        ms=round(float(x)*1000)
        return ms//10
    v=r.get("value")
    if isinstance(v,(int,float)) and float(v)>=0:
        return int(float(v)*100 + 1e-9)
    if isinstance(v,str):
        m=re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*",v)
        if m: return int(float(m.group(1))*100 + 1e-9)
    return None

def hhi(counter):
    n=sum(counter.values())
    return sum((v/n)**2 for v in counter.values()) if n else None

recons=json.loads(download("recons_backup.json", RECONS_BLOB))
side=json.loads(download("wca_attempts.json", ATTEMPTS_BLOB))
by_id={int(r["id"]):r for r in recons if str(r.get("id","")).isdigit()}
wca=[r for r in recons if r.get("official")=="wca"]

# Strict old builder eligibility from current input, from scratch (not stale existing cache).
strict_rows=[]
for r in wca:
    event=r.get("event"); rnd=r.get("round")
    ok_event=event in OLD_EVENT_MAP
    ok_round=rnd in OLD_ROUND_MAP
    ok_core=bool(r.get("compWcaId") and r.get("personId") and r.get("solveNum") and r.get("id"))
    if ok_event and ok_round and ok_core:
        strict_rows.append(r)

# Repaired crosswalk.
all_rows=[]; admitted=[]
for r in wca:
    rid=int(r["id"])
    comp=r.get("compWcaId") or ""
    person=r.get("personId") or ""
    event=norm_event(r.get("event"))
    rr, round_sem=norm_round(r.get("round"))
    sn=r.get("solveNum")
    try: sn_i=int(sn) if sn is not None and str(sn).strip()!="" else None
    except: sn_i=None
    status=""
    candidates=[]
    selected_key=None; attempt=None; value_status="NOT_CHECKED"; rcs=recon_cs(r)
    if not comp or not person or not event or rr is None or sn_i is None or sn_i<=0:
        status="META_INSUFFICIENT" if rr is not None else "ROUND_UNRECOGNIZED"
    elif event not in {"333","222","444","555","666","777","333bf","444bf","555bf","333mbf","333oh","333fm","333ft","minx","pyram","clock","skewb","sq1"}:
        status="EVENT_UNRECOGNIZED"
    else:
        pdata=side.get(comp,{}).get(person,{})
        for rt in ROUND_VARIANTS[rr]:
            k=f"{event}_{rt}"
            if k in pdata and isinstance(pdata[k],dict) and isinstance(pdata[k].get("a"),list):
                candidates.append(k)
        if len(candidates)==0:
            status="WCA_RESULT_GROUP_NOT_CACHED"
        elif len(candidates)>1:
            status="AMBIGUOUS_ROUND_VARIANT"
        else:
            selected_key=candidates[0]
            arr=side[comp][person][selected_key]["a"]
            if sn_i>len(arr):
                status="ATTEMPT_POSITION_OUT_OF_RANGE"
            else:
                attempt=arr[sn_i-1]
                if attempt==0:
                    status="ATTEMPT_SLOT_EMPTY"
                    value_status="WCA_ZERO_SLOT"
                else:
                    # Identity is explicit key + unique source result group + attempt position.
                    status="EXACT_REPAIRED_LINK"
                    if event in NORMAL_TIMED and isinstance(attempt,int) and attempt>0 and rcs is not None:
                        delta=attempt-rcs
                        if delta==0:
                            value_status="VALUE_MATCH"
                        elif delta==200:
                            value_status="PLUS2_COMPATIBLE"
                        else:
                            value_status="VALUE_MISMATCH_REMAND"
                            status="KEY_POSITION_VALUE_CONFLICT"
                    elif isinstance(attempt,int) and attempt<0:
                        value_status="NEGATIVE_WCA_RESULT_EVENT_SPECIFIC"
                    else:
                        value_status="EVENT_SPECIFIC_OR_UNAVAILABLE"
    row={
        "recon_id":rid,"official":r.get("official"),"event_raw":r.get("event"),"event_wca":event,
        "competition_id":comp,"person_id":person,"round_raw":r.get("round"),"round_canonical":rr,
        "round_semantics":round_sem,"solve_num":sn_i,"selected_event_round":selected_key,
        "candidate_group_count":len(candidates),"wca_attempt":attempt,"recon_cs":rcs,
        "value_status":value_status,"status":status,"date":r.get("date"),"method":r.get("method"),
        "reconstructor":r.get("reconer"),"reconstructor_id":r.get("reconerId"),
        "stm":r.get("stm"),"tps":r.get("tps")
    }
    all_rows.append(row)
    if status=="EXACT_REPAIRED_LINK": admitted.append(row)

# Legacy r referential integrity + reproducibility audit.
legacy=[]
for comp, persons in side.items():
    if not isinstance(persons,dict): continue
    for person,pdata in persons.items():
        if not isinstance(pdata,dict): continue
        for er,entry in pdata.items():
            if not isinstance(entry,dict) or not isinstance(entry.get("r"),dict): continue
            for sn,rid0 in entry["r"].items():
                try: rid=int(rid0); sn_i=int(sn)
                except: continue
                r=by_id.get(rid)
                semantic="ORPHAN_LEGACY_R" if r is None else ""
                repaired_row=next((x for x in all_rows if x["recon_id"]==rid),None)
                if r is not None:
                    if repaired_row and repaired_row["selected_event_round"]==er and repaired_row["solve_num"]==sn_i:
                        semantic="SEMANTICALLY_REPAIRED_CURRENT"
                    elif repaired_row and repaired_row["status"]=="AMBIGUOUS_ROUND_VARIANT":
                        semantic="AMBIGUOUS_UNDER_REPAIRED_OPERATOR"
                    else:
                        semantic="LEGACY_POSITION_DISAGREES_CURRENT_INPUT"
                old_repro=False
                if r:
                    old_repro=(r.get("event") in OLD_EVENT_MAP and r.get("round") in OLD_ROUND_MAP and
                               bool(r.get("compWcaId") and r.get("personId") and r.get("solveNum") and r.get("id")))
                legacy.append({
                    "competition_id":comp,"person_id":person,"event_round":er,"attempt_index":sn_i,
                    "legacy_recon_id":rid,"current_recon_present":r is not None,
                    "old_builder_current_input_reproducible":old_repro,
                    "repaired_status":repaired_row["status"] if repaired_row else None,
                    "repaired_event_round":repaired_row["selected_event_round"] if repaired_row else None,
                    "referential_status":semantic,
                })

# Positivity / coverage strata.
def strata(field_fn):
    den=Counter(); num=Counter(); conflict=Counter(); missing=Counter()
    for r,row in zip(wca,all_rows):
        k=field_fn(r,row)
        den[k]+=1
        if row["status"]=="EXACT_REPAIRED_LINK": num[k]+=1
        elif row["status"]=="KEY_POSITION_VALUE_CONFLICT": conflict[k]+=1
        else: missing[k]+=1
    out=[]
    for k in sorted(den, key=lambda x: str(x)):
        out.append({"stratum":k,"denominator_wca_recons":den[k],"exact_repaired":num[k],
                    "coverage":num[k]/den[k],"value_conflict":conflict[k],"other_not_admitted":missing[k]})
    return out

pos_event=strata(lambda r,x: x["event_wca"] or "<missing>")
pos_round=strata(lambda r,x: x["round_canonical"] or f"RAW:{r.get('round')}")
pos_year=strata(lambda r,x: str(r.get("date") or "<missing>")[:4])

# Reconstruction concentration among admitted bridge rows.
recon_ctr=Counter((x["reconstructor_id"] or x["reconstructor"] or "<missing>") for x in admitted)
solver_ctr=Counter(x["person_id"] or "<missing>" for x in admitted)
cluster_ctr=Counter((x["competition_id"],x["person_id"],x["selected_event_round"]) for x in admitted)

status_counts=Counter(x["status"] for x in all_rows)
round_raw_counts=Counter(str(r.get("round")) for r in wca)
event_counts=Counter(norm_event(r.get("event")) for r in wca)
legacy_ref_counts=Counter(x["referential_status"] for x in legacy)
value_counts=Counter(x["value_status"] for x in all_rows if x["status"] in {"EXACT_REPAIRED_LINK","KEY_POSITION_VALUE_CONFLICT"})

# Bridge decision: usable descriptive bridge requires nontrivial coverage and multiple source-support strata.
coverage=len(admitted)/len(wca) if wca else 0
positive_events=sum(1 for x in pos_event if x["exact_repaired"]>0)
positive_years=sum(1 for x in pos_year if x["exact_repaired"]>0)
positive_rounds=sum(1 for x in pos_round if x["exact_repaired"]>0)
bridge_pass=(coverage>=0.25 and positive_events>=2 and positive_rounds>=2 and positive_years>=3)

summary={
    "schema_version":"CUBE-REV-R1.23-CROSSWALK-REGEN-1",
    "version":VERSION,
    "source":{
        "repo":UPSTREAM_REPO,"commit":UPSTREAM_COMMIT,"recons_blob_sha1":RECONS_BLOB,"attempts_blob_sha1":ATTEMPTS_BLOB,
        "recons_n":len(recons),"wca_classified_n":len(wca),"sidecar_competitions":len(side)
    },
    "strict_old_builder":{
        "current_input_rows_eligible_for_recon_index":len(strict_rows),
        "share_of_wca_recons":len(strict_rows)/len(wca) if wca else 0,
        "interpretation":"from-scratch current-input eligibility under pinned build_wca_attempts.ts old event/round contract; existing stale r cache excluded"
    },
    "repaired_operator":{
        "status_counts":dict(status_counts),"exact_repaired_n":len(admitted),"coverage":coverage,
        "value_validation_counts":dict(value_counts),"positive_event_strata":positive_events,
        "positive_round_strata":positive_rounds,"positive_year_strata":positive_years
    },
    "legacy_r_integrity":{
        "legacy_r_count":len(legacy),"referential_counts":dict(legacy_ref_counts),
        "old_builder_reproducible_count":sum(1 for x in legacy if x["old_builder_current_input_reproducible"])
    },
    "schema_drift":{
        "wca_round_raw_counts":dict(round_raw_counts),"wca_event_counts":dict(event_counts),
        "old_builder_missing_generic_4x4":True,
        "pinned_client_event_normalizer_has_4x4":True,
        "old_builder_round_inputs":["R1","R2","R3","Fi"],
        "pinned_client_recon_round_inputs":["1","2","3","f"],
        "pinned_client_round_variants":ROUND_VARIANTS
    },
    "selection_dependence":{
        "admitted_reconstructor_hhi":hhi(recon_ctr),"admitted_solver_hhi":hhi(solver_ctr),
        "admitted_unique_reconstructors":len(recon_ctr),"admitted_unique_solvers":len(solver_ctr),
        "admitted_unique_comp_person_round_clusters":len(cluster_ctr),
        "top_reconstructors":recon_ctr.most_common(10),"top_solvers":solver_ctr.most_common(10)
    },
    "court":{
        "question":"Can the pinned official-outcome cache and current reconstruction snapshot support a referentially repaired, positivity-qualified macro–meso descriptive bridge?",
        "bridge_pass_restricted_descriptive":bridge_pass,
        "authority":"RESTRICTED_DESCRIPTIVE_BRIDGE" if bridge_pass else "HOLD_MACRO_MESO_BRIDGE",
        "prohibitions":["no causal selection correction","no population cognitive prevalence","no name/time-only linkage","no generic scramble inheritance","no unqualified cross-source pooling"]
    }
}

write_json("CUBE_REV_0.10.5-R1.23_REGEN_SUMMARY.json", summary)
write_json("CUBE_REV_0.10.5-R1.23_OPERATOR_CONTRACT.json", {
    "version":VERSION,"repaired_event_map":REPAIRED_EVENT_MAP,"round_variants":ROUND_VARIANTS,
    "identity_key":["compWcaId","personId","normalized WCA event","matched round variant","solveNum"],
    "value_check":"secondary falsification layer; ordinary positive timed results remanded on unexplained mismatch",
    "source_witnesses":["client/lib/recon-attempt-lookup.ts","client/lib/wca-events.ts","client/lib/wca-results-api.ts"],
    "legacy_builder_defects":["expects R1/R2/R3/Fi while current recon snapshot uses 1/2/3/f","generic 4x4 absent from EVENT_MAP","incremental existing r mappings are not deleted when current recon_index no longer produces them"]
})
fields=list(all_rows[0].keys()) if all_rows else []
write_csv("CUBE_REV_0.10.5-R1.23_ALL_WCA_CROSSWALK.csv", all_rows, fields)
write_csv("CUBE_REV_0.10.5-R1.23_REGENERATED_EXACT_PANEL.csv", admitted, fields)
write_csv("CUBE_REV_0.10.5-R1.23_LEGACY_R_REFERENTIAL_AUDIT.csv", legacy, list(legacy[0].keys()) if legacy else [])
write_csv("CUBE_REV_0.10.5-R1.23_POSITIVITY_EVENT.csv", pos_event, list(pos_event[0].keys()) if pos_event else [])
write_csv("CUBE_REV_0.10.5-R1.23_POSITIVITY_ROUND.csv", pos_round, list(pos_round[0].keys()) if pos_round else [])
write_csv("CUBE_REV_0.10.5-R1.23_POSITIVITY_YEAR.csv", pos_year, list(pos_year[0].keys()) if pos_year else [])

manifest={}
for p in sorted(OUT.iterdir()):
    if p.is_file():
        manifest[p.name]={"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
write_json("CUBE_REV_0.10.5-R1.23_ACTION_MANIFEST.json", manifest)
print(json.dumps(summary, ensure_ascii=False, indent=2))
