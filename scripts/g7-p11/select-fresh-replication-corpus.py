#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter,defaultdict

SEED="CUBE_REV_G7_P11_FRESH_REPLICATION_V1"
CELLS=[
  "CFOP__DOMINANT_RECONSTRUCTOR",
  "CFOP__NONDOMINANT_RECONSTRUCTOR",
  "NONCFOP__DOMINANT_RECONSTRUCTOR",
  "NONCFOP__NONDOMINANT_RECONSTRUCTOR",
]

def h(seed,sid):
    return hashlib.sha256(f"{seed}|{sid}".encode()).hexdigest()

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

def balanced(rows,n,seed):
    by=defaultdict(list)
    for r in rows:by[r["era"]].append(r)
    for k in by:by[k].sort(key=lambda x:(h(seed+"|"+k,x["source_id"]),x["source_id"]))
    keys=sorted(by)
    pos={k:0 for k in keys};out=[]
    while len(out)<min(n,len(rows)):
        moved=False
        for k in keys:
            if len(out)>=n:break
            i=pos[k]
            if i<len(by[k]):
                out.append(by[k][i]);pos[k]+=1;moved=True
        if not moved:break
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--covariates",required=True)
    ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--exclude60",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    cov=[]
    for line in open(a.covariates,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("frozen_puzzle")=="3x3" and x.get("live_present") is not False:
                cov.append(x)
    if len(cov)!=10591:raise SystemExit(f"COVARIATE_10591_REQUIRED_{len(cov)}")
    cov_ids={int(x["source_id"]) for x in cov}
    if len(cov_ids)!=10591:raise SystemExit("COVARIATE_IDS_NOT_UNIQUE")

    idx={}
    for line in open(a.frozen_index,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("puzzle")=="3x3":idx[int(x["source_id"])]=x
    if set(idx)!=cov_ids:raise SystemExit("INDEX_COVARIATE_ID_SET_MISMATCH")

    reg=json.load(open(a.exclude60,encoding="utf-8"))
    exclude={int(x) for x in reg["source_id_to_broad_provenance_class"]}
    if len(exclude)!=60:raise SystemExit("EXCLUDE60_REQUIRED")

    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    rows=[]
    for x in cov:
        sid=int(x["source_id"])
        if sid in exclude:continue
        method=str(x.get("method_raw") or "").strip()
        recon=str(x.get("reconstructor") or "NULL")
        dominant=recfreq[recon]>=200
        mc="CFOP" if method.upper()=="CFOP" else "NONCFOP"
        cell=f"{mc}__{'DOMINANT_RECONSTRUCTOR' if dominant else 'NONDOMINANT_RECONSTRUCTOR'}"
        y=year_of(idx[sid])
        rows.append({
          "source_id":sid,"method_raw":method,"reconstructor":recon,
          "reconstructor_population_frequency":recfreq[recon],
          "cell":cell,"year":y,"era":era(y)
        })

    pool=defaultdict(list)
    for r in rows:pool[r["cell"]].append(r)
    counts={k:len(pool[k]) for k in CELLS}
    if any(counts[k]<10 for k in CELLS):raise SystemExit("CELL_SUPPORT_LT10_"+json.dumps(counts,sort_keys=True))

    selected=[]
    for c in CELLS:
        chosen=balanced(pool[c],10,SEED+"|"+c)
        if len(chosen)!=10:raise SystemExit("CELL_SELECTION_FAIL_"+c)
        for r in chosen:r["batch"]=CELLS.index(c)+1
        selected.extend(chosen)

    if len(selected)!=40 or len({r["source_id"] for r in selected})!=40:raise SystemExit("SELECT40_FAIL")
    if {r["source_id"] for r in selected}&exclude:raise SystemExit("PRIOR60_LEAK")

    selected.sort(key=lambda r:(r["batch"],r["era"],h(SEED+"|FINAL",r["source_id"]),r["source_id"]))
    core={
      "schema_version":"g7-p11-fresh-selection-manifest-1",
      "phase":"G7-P11",
      "status":"SEALED_BEFORE_FRESH_BODY_CONTACT",
      "seed":SEED,
      "frozen_population_3x3":10591,
      "prior_body_excluded":60,
      "target_total":40,
      "cell_definition":{
        "method":"CFOP versus NONCFOP from frozen P8 index covariate",
        "dominant_reconstructor":"raw reconstructor frequency >=200 in frozen 10,591 population"
      },
      "eligible_cell_counts":counts,
      "selected_cell_counts":dict(sorted(Counter(r["cell"] for r in selected).items())),
      "selected_era_counts":dict(sorted(Counter(r["era"] for r in selected).items())),
      "rows":selected,
      "batches":{
        str(i):[r["source_id"] for r in selected if r["batch"]==i] for i in range(1,5)
      },
      "contact_authority":{
        "authorized_after_this_manifest_is_sealed":True,
        "max_solves_per_run":10,
        "batches":4,
        "min_delay_ms":2000,
        "raw_public_release":"HOLD",
        "outcome_triggered_replacement":"FORBIDDEN"
      }
    }
    canonical=json.dumps(core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    core["selection_manifest_sha256"]=hashlib.sha256(canonical).hexdigest()

    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"selection-manifest.json").write_text(json.dumps(core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for i in range(1,5):
        (out/f"batch-{i}-source-ids.txt").write_text("\n".join(map(str,core["batches"][str(i)]))+"\n",encoding="utf-8")
    print("G7_P11_FRESH_SELECTION_PASS")
    print("ELIGIBLE_CELLS\t"+json.dumps(counts,sort_keys=True))
    print("SELECTED_CELLS\t"+json.dumps(core["selected_cell_counts"],sort_keys=True))
    print("ERAS\t"+json.dumps(core["selected_era_counts"],sort_keys=True))
    print("MANIFEST_SHA256\t"+core["selection_manifest_sha256"])
    for i in range(1,5):print(f"BATCH_{i}\t"+",".join(map(str,core["batches"][str(i)])))

if __name__=="__main__":
    main()
