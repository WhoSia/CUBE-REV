#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter

SEED="CUBE_REV_G7_P13_METHOD_PROGRESS_FRESH80_V1"
INVALID={11370,11962,13073}

def h(seed,sid): return hashlib.sha256(f"{seed}|{sid}".encode()).hexdigest()
def year_of(x):
    for key in ("date","source_display_date","solve_date"):
        s=str(x.get(key) or "")
        m=re.search(r"\b(19\d{2}|20\d{2})\b",s)
        if m:return int(m.group(1))
    return None
def era(y):
    if y is None:return "UNKNOWN"
    if y<=2016:return "E1_2013_2016_OR_EARLIER"
    if y<=2020:return "E2_2017_2020"
    if y<=2024:return "E3_2021_2024"
    return "E4_2025_2026"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original-manifest",required=True)
    ap.add_argument("--covariates",required=True)
    ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--legacy60",required=True)
    ap.add_argument("--p11-manifest",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    orig=json.load(open(a.original_manifest,encoding="utf-8"))
    if orig.get("selection_manifest_sha256")!="d63f292547f38e206e39d58c6e4e7eab0025e9f6fccbb45efe52c7a7e183e4bf":
        raise SystemExit("ORIGINAL_MANIFEST_SHA_MISMATCH")
    rows=[dict(r) for r in orig["rows"]]
    byid={int(r["source_id"]):r for r in rows}
    if not INVALID<=set(byid):raise SystemExit("INVALID_IDS_NOT_IN_ORIGINAL")

    cov=[]
    for line in open(a.covariates,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("frozen_puzzle")=="3x3" and x.get("live_present") is not False:cov.append(x)
    if len(cov)!=10591:raise SystemExit("COV10591_REQUIRED")
    idx={}
    for line in open(a.frozen_index,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("puzzle")=="3x3":idx[int(x["source_id"])]=x

    legacy={int(x) for x in json.load(open(a.legacy60,encoding="utf-8"))["source_id_to_broad_provenance_class"]}
    p11={int(r["source_id"]) for r in json.load(open(a.p11_manifest,encoding="utf-8"))["rows"]}
    exclude100=legacy|p11
    if len(exclude100)!=100:raise SystemExit("EXCLUDE100_REQUIRED")

    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    current={int(r["source_id"]) for r in rows}
    replacements={}
    for bad in sorted(INVALID):
        old=byid[bad]
        target_cell=old["cell"];target_era=old["era"];target_batch=int(old["batch"])
        cand=[]
        for x in cov:
            sid=int(x["source_id"])
            if sid in exclude100 or sid in current:continue
            method=str(x.get("method_raw") or "").strip()
            recon=str(x.get("reconstructor") or "NULL")
            dominant=recfreq[recon]>=200
            mc="CFOP" if method.upper()=="CFOP" else "NONCFOP"
            cell=f"{mc}__{'DOMINANT_RECONSTRUCTOR' if dominant else 'NONDOMINANT_RECONSTRUCTOR'}"
            y=year_of(idx[sid]);er=era(y)
            if cell!=target_cell or er!=target_era:continue
            cand.append({
              "source_id":sid,"method_raw":method,"reconstructor":recon,
              "reconstructor_population_frequency":recfreq[recon],
              "cell":cell,"year":y,"era":er,"batch":target_batch
            })
        cand.sort(key=lambda r:(h(SEED+"|"+target_cell+"|"+target_era,r["source_id"]),r["source_id"]))
        if not cand:raise SystemExit("NO_REPLACEMENT_"+str(bad))
        rep=cand[0]
        replacements[str(bad)]=rep
        current.remove(bad);current.add(rep["source_id"])
        rows=[rep if int(r["source_id"])==bad else r for r in rows]
        byid.pop(bad);byid[rep["source_id"]]=rep

    if len(rows)!=80 or len({int(r["source_id"]) for r in rows})!=80:raise SystemExit("SELECT80_REQUIRED")
    cc=Counter(r["cell"] for r in rows); ec=Counter(r["era"] for r in rows); bc=Counter(str(r["batch"]) for r in rows)
    if any(cc[k]!=20 for k in orig["selected_cell_counts"]):raise SystemExit("CELL20_FAIL")
    if any(ec[k]!=20 for k in orig["selected_era_counts"]):raise SystemExit("ERA20_FAIL")
    if any(bc[str(i)]!=10 for i in range(1,9)):raise SystemExit("BATCH10_FAIL")
    if {int(r["source_id"]) for r in rows}&exclude100:raise SystemExit("PRIOR100_LEAK")

    # preserve row ordering except replacement-in-place, then reconstruct batch lists
    core={
      "schema_version":"g7-p13-fresh80-selection-manifest-2-replay-repaired",
      "phase":"G7-P13",
      "status":"SEALED_AFTER_PRE_GEOMETRY_REPLAY_INVALID_REPLACEMENT",
      "supersedes_manifest_sha256":orig["selection_manifest_sha256"],
      "seed":SEED,
      "frozen_population_3x3":10591,
      "prior_body_excluded":100,
      "target_total":80,
      "replacement_amendment":"g7/p13/replay-invalid-replacement-amendment.json",
      "replacements":replacements,
      "selected_cell_counts":dict(sorted(cc.items())),
      "selected_era_counts":dict(sorted(ec.items())),
      "selected_batch_counts":dict(sorted(bc.items())),
      "rows":rows,
      "batches":{str(i):[int(r["source_id"]) for r in rows if int(r["batch"])==i] for i in range(1,9)},
      "contact_authority":{
        "authorized_after_manifest_seal":True,
        "max_solves_per_run":10,"batches":8,"min_delay_ms":2000,
        "raw_public_release":"HOLD","bulk_mirror":"HOLD",
        "outcome_triggered_replacement":"FORBIDDEN"
      }
    }
    canonical=json.dumps(core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    core["selection_manifest_sha256"]=hashlib.sha256(canonical).hexdigest()
    p=pathlib.Path(a.out);p.mkdir(parents=True,exist_ok=True)
    (p/"selection-manifest-repaired.json").write_text(json.dumps(core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for i in range(1,9):
        (p/f"batch-{i}-source-ids.txt").write_text("\n".join(map(str,core["batches"][str(i)]))+"\n",encoding="utf-8")
    print("G7_P13_REPLAY_REPLACEMENT_SELECTION_PASS")
    print("REPLACEMENTS",json.dumps(replacements,sort_keys=True))
    print("CELLS",json.dumps(core["selected_cell_counts"],sort_keys=True))
    print("ERAS",json.dumps(core["selected_era_counts"],sort_keys=True))
    print("BATCHES",json.dumps(core["selected_batch_counts"],sort_keys=True))
    print("MANIFEST_SHA256",core["selection_manifest_sha256"])

if __name__=="__main__":main()
