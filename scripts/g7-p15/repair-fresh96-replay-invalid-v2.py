#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter

SEED="CUBE_REV_G7_P15_REGIME_STATE_FRESH96_V1"
BASE_SHA="74d1b5becd25d5dd66028dce46cf73a95b9fc68a53ff6bb51d8366c97fb117cc"

def h(s,sid): return hashlib.sha256(f"{s}|{sid}".encode()).hexdigest()
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
def ids(path):
    return {int(r["source_id"]) for r in json.load(open(path,encoding="utf-8"))["rows"]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--amendment",required=True)
    ap.add_argument("--base-manifest",required=True)
    ap.add_argument("--covariates",required=True)
    ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--legacy60",required=True)
    ap.add_argument("--p11-manifest",required=True)
    ap.add_argument("--p13-original",required=True)
    ap.add_argument("--p13-repaired",required=True)
    ap.add_argument("--p14-original",required=True)
    ap.add_argument("--p14-repaired",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    amend=json.load(open(a.amendment,encoding="utf-8"))
    if amend.get("status")!="FROZEN_BEFORE_ANY_P15_GEOMETRY" or amend.get("base_manifest_sha256")!=BASE_SHA:
        raise SystemExit("AMENDMENT_NOT_FROZEN")
    base=json.load(open(a.base_manifest,encoding="utf-8"))
    if base.get("selection_manifest_sha256")!=BASE_SHA:raise SystemExit("BASE_SHA_FAIL")
    if base.get("status")!="SEALED_AFTER_PRE_GEOMETRY_REPLAY_INVALID_REPLACEMENT":raise SystemExit("BASE_STATUS")

    invalid={int(x) for x in amend["replacement_rule"]["replace_only"]}
    contacted_extra={int(x) for x in amend["replacement_rule"]["exclude_all_contacted_ids"]}
    rows=[dict(r) for r in base["rows"]];byid={int(r["source_id"]):r for r in rows}
    if invalid!={2013}:raise SystemExit("EXPECTED_2013_ONLY")
    if not invalid<=set(byid):raise SystemExit("INVALID_NOT_IN_BASE")

    cov=[]
    for line in open(a.covariates,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("frozen_puzzle")=="3x3" and x.get("live_present") is not False:cov.append(x)
    idx={}
    for line in open(a.frozen_index,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("puzzle")=="3x3":idx[int(x["source_id"])]=x
    if len(cov)!=10591 or set(idx)!={int(x["source_id"]) for x in cov}:raise SystemExit("FROZEN_FRAME")

    legacy={int(x) for x in json.load(open(a.legacy60,encoding="utf-8"))["source_id_to_broad_provenance_class"]}
    prior=legacy|ids(a.p11_manifest)|ids(a.p13_original)|ids(a.p13_repaired)|ids(a.p14_original)|ids(a.p14_repaired)
    if len(prior)!=267:raise SystemExit("PRIOR267_REQUIRED")

    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    current={int(r["source_id"]) for r in rows}
    replacements={}
    for bad in sorted(invalid):
        old=byid[bad];cell=old["cell"];batch=int(old["batch"])
        forbidden=prior|current|contacted_extra
        cand=[]
        for x in cov:
            sid=int(x["source_id"])
            if sid in forbidden:continue
            method="CFOP" if str(x.get("method_raw") or "").strip().upper()=="CFOP" else "NONCFOP"
            recon=str(x.get("reconstructor") or "NULL")
            band="DOMINANT" if recfreq[recon]>=200 else "NONDOMINANT"
            y=year_of(idx[sid]);er=era(y)
            c=f"{method}__{band}__{er}"
            if c!=cell:continue
            cand.append({
              "source_id":sid,"method_family":method,"method_raw":str(x.get("method_raw") or ""),
              "reconstructor":recon,"reconstructor_population_frequency":recfreq[recon],
              "reconstructor_frequency_band":band,"year":y,"selection_era":er,
              "cell":c,"selection_round":old["selection_round"],"batch":batch
            })
        cand.sort(key=lambda r:(h(SEED+"|"+cell,r["source_id"]),r["source_id"]))
        if not cand:raise SystemExit("NO_REPLACEMENT")
        rep=cand[0]
        replacements[str(bad)]=rep
        rows=[rep if int(r["source_id"])==bad else r for r in rows]

    cc=Counter(r["cell"] for r in rows);bc=Counter(str(r["batch"]) for r in rows)
    if len(rows)!=96 or len({int(r["source_id"]) for r in rows})!=96:raise SystemExit("SELECT96")
    if len(cc)!=16 or any(v!=6 for v in cc.values()):raise SystemExit("CELL16X6")
    if any(bc[str(i)]!=8 for i in range(1,13)):raise SystemExit("BATCH12X8")
    if {int(r["source_id"]) for r in rows}&prior:raise SystemExit("PRIOR_LEAK")
    if {int(r["source_id"]) for r in rows}&contacted_extra:raise SystemExit("CONTACTED_EXTRA_LEAK")

    core={
      "schema_version":"g7-p15-fresh96-selection-manifest-3-replay-repaired",
      "phase":"G7-P15",
      "status":"SEALED_AFTER_SECOND_PRE_GEOMETRY_REPLAY_INVALID_REPLACEMENT",
      "supersedes_manifest_sha256":BASE_SHA,
      "seed":SEED,
      "frozen_population_3x3":10591,
      "prior_body_contacted_excluded":267,
      "target_total":96,
      "replacement_amendment":"g7/p15/replay-invalid-replacement-amendment-v2.json",
      "replacements":replacements,
      "selected_cell_counts":dict(sorted(cc.items())),
      "selected_batch_counts":dict(sorted(bc.items())),
      "rows":rows,
      "batches":{str(i):[int(r["source_id"]) for r in rows if int(r["batch"])==i] for i in range(1,13)},
      "contact_authority":{"max_solves_per_run":8,"batches":12,"min_delay_ms":2000,"raw_public_release":"HOLD","bulk_mirror":"HOLD"}
    }
    canonical=json.dumps(core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    core["selection_manifest_sha256"]=hashlib.sha256(canonical).hexdigest()
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"selection-manifest-repaired-v2.json").write_text(json.dumps(core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for i in range(1,13):
        (out/f"batch-{i}-source-ids.txt").write_text("\n".join(map(str,core["batches"][str(i)]))+"\n",encoding="utf-8")
    print("G7_P15_SECOND_REPLAY_REPAIR_PASS")
    print("REPLACEMENTS",json.dumps(replacements,sort_keys=True))
    print("MANIFEST_SHA256",core["selection_manifest_sha256"])
    print("BATCH1",core["batches"]["1"])

if __name__=="__main__":main()
