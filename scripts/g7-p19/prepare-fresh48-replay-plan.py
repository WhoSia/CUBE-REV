#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter

SEED="CUBE_REV_G7_P19_HYBRID_CONFIRMATION_V1"
BASE_SHA="671e230314aed38ed68e9c8337c2e64b3f57e2bddca181405d08f5805c78d15e"
EXCLUSION_SHA="da2b4ac80970ee77fe64c15ac60745afa24d29995291438bb05026e8220fd1cc"

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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--amendment",required=True)
    ap.add_argument("--base-manifest",required=True)
    ap.add_argument("--covariates",required=True)
    ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--exclusion-census",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    amend=json.load(open(a.amendment,encoding="utf-8"))
    base=json.load(open(a.base_manifest,encoding="utf-8"))
    census=json.load(open(a.exclusion_census,encoding="utf-8"))
    if amend.get("status")!="FROZEN_BEFORE_ANY_P19_MODEL_EVALUATION":raise SystemExit("AMENDMENT_STATUS")
    if amend.get("parent_selection_manifest_sha256")!=BASE_SHA or base.get("selection_manifest_sha256")!=BASE_SHA:
        raise SystemExit("BASE_SHA")
    if census["counts"]["all_prior_contacted_through_p17"]!=418 or census["exclusion_list_sha256"]!=EXCLUSION_SHA:
        raise SystemExit("EXCLUSION_AUTHORITY")
    excluded={int(r["source_id"]) for r in census["contacted_ids"]}
    current={int(r["source_id"]) for r in base["rows"]}
    failed_batches={int(x) for x in amend["failed_batches"]}
    scan_rows=[dict(r) for r in base["rows"] if int(r["batch"]) in failed_batches]
    if len(scan_rows)!=8:raise SystemExit("EXPECTED_8_SCAN_ROWS")

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
    if len(cov)!=10591 or set(idx)!={int(x["source_id"]) for x in cov}:raise SystemExit("FRAME")

    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    maxn=int(amend["repair_rule"]["max_candidates_per_invalid_row"])
    queues={}
    for row in scan_rows:
        cell=row["cell"];pool=[]
        for x in cov:
            sid=int(x["source_id"])
            if sid in excluded or sid in current:continue
            method="CFOP" if str(x.get("method_raw") or "").strip().upper()=="CFOP" else "NONCFOP"
            recon=str(x.get("reconstructor") or "NULL")
            band="DOMINANT" if recfreq[recon]>=200 else "NONDOMINANT"
            y=year_of(idx[sid]);er=era(y)
            c=f"{method}__{band}__{er}"
            if c!=cell:continue
            pool.append({
              "source_id":sid,"method_family":method,"method_raw":str(x.get("method_raw") or ""),
              "reconstructor":recon,"reconstructor_population_frequency":recfreq[recon],
              "reconstructor_frequency_band":band,"year":y,"selection_era":er,
              "cell":c,"selection_round":row["selection_round"],"batch":row["batch"]
            })
        pool.sort(key=lambda r:(h(SEED+"|"+cell,r["source_id"]),r["source_id"]))
        queues[str(row["source_id"])]=pool[:maxn]
        if not queues[str(row["source_id"])]:raise SystemExit("QUEUE_EMPTY_"+str(row["source_id"]))

    plan={
      "schema_version":"g7-p19-p3-r1-replay-plan-1",
      "phase":"G7-P19-P3-R1",
      "status":"FROZEN_PLAN",
      "base_manifest_sha256":BASE_SHA,
      "failed_batches":sorted(failed_batches),
      "scan_rows":scan_rows,
      "candidate_queues":queues,
      "prior418_excluded":True,
      "max_candidates_per_invalid_row":maxn,
      "selection_rule":"retain current if exact-replay PASS; otherwise first exact-replay PASS in frozen same-cell queue",
      "model_evaluation_opened":False
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"fresh48-replay-plan.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P19_P3_R1_REPLAY_PLAN_PASS")
    print("SCAN_IDS",json.dumps([r["source_id"] for r in scan_rows]))
    print("QUEUE_HEADS",json.dumps({k:[x["source_id"] for x in v[:3]] for k,v in queues.items()},sort_keys=True))

if __name__=="__main__":main()
