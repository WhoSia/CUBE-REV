#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter,defaultdict

SEED="CUBE_REV_G7_P14_RECONSTRUCTOR_ERA_CONFIRM80_V1"
INVALID={3276,11912,14005,7309}

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
    ap.add_argument("--original-manifest",required=True)
    ap.add_argument("--covariates",required=True)
    ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--legacy60",required=True)
    ap.add_argument("--p11-manifest",required=True)
    ap.add_argument("--p13-original",required=True)
    ap.add_argument("--p13-repaired",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    orig=json.load(open(a.original_manifest,encoding="utf-8"))
    if orig.get("selection_manifest_sha256")!="39fa29383ab3b61fb8f2969861ee531a04e50762eaae4fcea4f4144ee8078658":raise SystemExit("ORIGINAL_SHA")
    rows=[dict(r) for r in orig["rows"]];byid={int(r["source_id"]):r for r in rows}
    if not INVALID<=set(byid):raise SystemExit("INVALID_NOT_SELECTED")

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
    legacy={int(x) for x in json.load(open(a.legacy60,encoding="utf-8"))["source_id_to_broad_provenance_class"]}
    p11={int(r["source_id"]) for r in json.load(open(a.p11_manifest,encoding="utf-8"))["rows"]}
    p13o={int(r["source_id"]) for r in json.load(open(a.p13_original,encoding="utf-8"))["rows"]}
    p13r={int(r["source_id"]) for r in json.load(open(a.p13_repaired,encoding="utf-8"))["rows"]}
    prior=legacy|p11|p13o|p13r
    if len(prior)!=183:raise SystemExit("PRIOR183_REQUIRED")
    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    original_ids={int(r["source_id"]) for r in rows}
    current=set(original_ids);replacements={}
    for bad in sorted(INVALID):
      old=byid[bad];cell=old["cell"];batch=int(old["batch"])
      cand=[]
      for x in cov:
        sid=int(x["source_id"])
        if sid in prior or sid in original_ids or sid in current:continue
        method="CFOP" if str(x.get("method_raw") or "").strip().upper()=="CFOP" else "NONCFOP"
        recon=str(x.get("reconstructor") or "NULL")
        band="DOMINANT" if recfreq[recon]>=200 else "NONDOMINANT"
        er=era(year_of(idx[sid]))
        c=f"{method}__{band}__{er}"
        if c!=cell:continue
        cand.append({"source_id":sid,"method_family":method,"method_raw":str(x.get("method_raw") or ""),
          "reconstructor":recon,"reconstructor_population_frequency":recfreq[recon],
          "reconstructor_frequency_band":band,"year":year_of(idx[sid]),"selection_era":er,
          "cell":c,"selection_round":old["selection_round"],"batch":batch})
      cand.sort(key=lambda r:(h(SEED+"|"+cell,r["source_id"]),r["source_id"]))
      if not cand:raise SystemExit("NO_REPLACEMENT_"+str(bad))
      rep=cand[0]
      replacements[str(bad)]=rep
      current.remove(bad);current.add(rep["source_id"])
      rows=[rep if int(r["source_id"])==bad else r for r in rows]
      byid.pop(bad);byid[rep["source_id"]]=rep

    cc=Counter(r["cell"] for r in rows);bc=Counter(str(r["batch"]) for r in rows)
    if len(rows)!=80 or len({r["source_id"] for r in rows})!=80:raise SystemExit("SELECT80")
    if len(cc)!=16 or any(v!=5 for v in cc.values()):raise SystemExit("CELL16X5")
    if any(bc[str(i)]!=10 for i in range(1,9)):raise SystemExit("BATCH8X10")
    if {int(r["source_id"]) for r in rows}&prior:raise SystemExit("PRIOR_LEAK")
    core={
      "schema_version":"g7-p14-confirm80-selection-manifest-2-replay-repaired","phase":"G7-P14",
      "status":"SEALED_AFTER_PRE_GEOMETRY_REPLAY_INVALID_REPLACEMENT",
      "supersedes_manifest_sha256":orig["selection_manifest_sha256"],"seed":SEED,
      "frozen_population_3x3":10591,"prior_body_contacted_excluded":183,"target_total":80,
      "replacement_amendment":"g7/p14/replay-invalid-replacement-amendment.json","replacements":replacements,
      "selected_cell_counts":dict(sorted(cc.items())),"selected_batch_counts":dict(sorted(bc.items())),
      "rows":rows,"batches":{str(i):[int(r["source_id"]) for r in rows if int(r["batch"])==i] for i in range(1,9)},
      "contact_authority":{"authorized_after_manifest_seal":True,"max_solves_per_run":10,"batches":8,"min_delay_ms":2000,
        "raw_public_release":"HOLD","bulk_mirror":"HOLD","outcome_triggered_replacement":"FORBIDDEN"}
    }
    canonical=json.dumps(core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    core["selection_manifest_sha256"]=hashlib.sha256(canonical).hexdigest()
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"selection-manifest-repaired.json").write_text(json.dumps(core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for i in range(1,9):(out/f"batch-{i}-source-ids.txt").write_text("\n".join(map(str,core["batches"][str(i)]))+"\n",encoding="utf-8")
    print("G7_P14_REPLAY_REPAIR_PASS");print("REPLACEMENTS",json.dumps(replacements,sort_keys=True));print("MANIFEST_SHA256",core["selection_manifest_sha256"])
if __name__=="__main__":main()
