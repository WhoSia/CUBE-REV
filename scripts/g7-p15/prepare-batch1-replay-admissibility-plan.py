#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter

SEED="CUBE_REV_G7_P15_REGIME_STATE_FRESH96_V1"
BASE_SHA="7e7d99682436c7b75bb6a7d2cd28eac54bbb87d3d3cef163e7ceacb7c16c3bb6"

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
    ap.add_argument("--amendment",required=True);ap.add_argument("--base-manifest",required=True)
    ap.add_argument("--covariates",required=True);ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--legacy60",required=True);ap.add_argument("--p11-manifest",required=True)
    ap.add_argument("--p13-original",required=True);ap.add_argument("--p13-repaired",required=True)
    ap.add_argument("--p14-original",required=True);ap.add_argument("--p14-repaired",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    amend=json.load(open(a.amendment,encoding="utf-8"))
    base=json.load(open(a.base_manifest,encoding="utf-8"))
    if amend.get("status")!="FROZEN_BEFORE_ANY_P15_GEOMETRY":raise SystemExit("AMENDMENT_STATUS")
    if amend.get("base_manifest_sha256")!=BASE_SHA or base.get("selection_manifest_sha256")!=BASE_SHA:
        raise SystemExit("BASE_SHA")
    batch1=[dict(r) for r in base["rows"] if int(r["batch"])==1]
    if len(batch1)!=8:raise SystemExit("BATCH1_8_REQUIRED")

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

    legacy={int(x) for x in json.load(open(a.legacy60,encoding="utf-8"))["source_id_to_broad_provenance_class"]}
    prior=legacy|ids(a.p11_manifest)|ids(a.p13_original)|ids(a.p13_repaired)|ids(a.p14_original)|ids(a.p14_repaired)
    if len(prior)!=267:raise SystemExit("PRIOR267")
    current={int(r["source_id"]) for r in base["rows"]}
    contacted=set(int(x) for x in amend["previously_contacted_repair_ids"])
    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    maxn=int(amend["repair_rule"]["max_candidates_per_invalid_row"])

    queues={}
    for row in batch1:
        cell=row["cell"];pool=[]
        for x in cov:
            sid=int(x["source_id"])
            if sid in prior or sid in current or sid in contacted:continue
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
              "cell":c,"selection_round":row["selection_round"],"batch":1
            })
        pool.sort(key=lambda r:(h(SEED+"|"+cell,r["source_id"]),r["source_id"]))
        queues[str(row["source_id"])]=pool[:maxn]
        if len(queues[str(row["source_id"])])<maxn:raise SystemExit("QUEUE_LT_MAX_"+str(row["source_id"]))

    plan={
      "schema_version":"g7-p15-batch1-replay-admissibility-plan-1",
      "phase":"G7-P15","status":"FROZEN_PLAN",
      "base_manifest_sha256":BASE_SHA,
      "batch1_rows":batch1,
      "candidate_queues":queues,
      "prior267_excluded":True,
      "previously_contacted_repair_ids":sorted(contacted),
      "max_candidates_per_invalid_row":maxn,
      "selection_rule":"retain current if exact-replay PASS; otherwise first exact-replay PASS in frozen queue",
      "geometry_opened":False
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"batch1-replay-plan.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P15_BATCH1_REPLAY_PLAN_PASS")
    print("CURRENT",json.dumps([r["source_id"] for r in batch1]))
    print("QUEUE_HEADS",json.dumps({k:[x["source_id"] for x in v[:4]] for k,v in queues.items()},sort_keys=True))
if __name__=="__main__":main()
