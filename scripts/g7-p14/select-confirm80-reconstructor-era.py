#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter,defaultdict

SEED="CUBE_REV_G7_P14_RECONSTRUCTOR_ERA_CONFIRM80_V1"
METHODS=("CFOP","NONCFOP")
BANDS=("DOMINANT","NONDOMINANT")
ERAS=("E1_2013_2016_OR_EARLIER","E2_2017_2020","E3_2021_2024","E4_2025_2026")
CELLS=[f"{m}__{b}__{e}" for m in METHODS for b in BANDS for e in ERAS]

def h(s,sid): return hashlib.sha256(f"{s}|{sid}".encode()).hexdigest()
def year_of(x):
    for key in ("date","source_display_date","solve_date"):
        s=str(x.get(key) or "")
        m=re.search(r"\b(19\d{2}|20\d{2})\b",s)
        if m:return int(m.group(1))
    return None
def era(y):
    if y is None:return "UNKNOWN"
    if y<=2016:return ERAS[0]
    if y<=2020:return ERAS[1]
    if y<=2024:return ERAS[2]
    return ERAS[3]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--covariates",required=True)
    ap.add_argument("--frozen-index",required=True)
    ap.add_argument("--legacy60",required=True)
    ap.add_argument("--p11-manifest",required=True)
    ap.add_argument("--p13-original",required=True)
    ap.add_argument("--p13-repaired",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    cov=[]
    for line in open(a.covariates,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("frozen_puzzle")=="3x3" and x.get("live_present") is not False:cov.append(x)
    if len(cov)!=10591:raise SystemExit(f"COVARIATE_10591_REQUIRED_{len(cov)}")
    idx={}
    for line in open(a.frozen_index,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("puzzle")=="3x3":idx[int(x["source_id"])]=x
    if set(idx)!={int(x["source_id"]) for x in cov}:raise SystemExit("INDEX_COVARIATE_SET_MISMATCH")

    legacy={int(x) for x in json.load(open(a.legacy60,encoding="utf-8"))["source_id_to_broad_provenance_class"]}
    p11={int(r["source_id"]) for r in json.load(open(a.p11_manifest,encoding="utf-8"))["rows"]}
    p13o={int(r["source_id"]) for r in json.load(open(a.p13_original,encoding="utf-8"))["rows"]}
    p13r={int(r["source_id"]) for r in json.load(open(a.p13_repaired,encoding="utf-8"))["rows"]}
    if (len(legacy),len(p11),len(p13o),len(p13r))!=(60,40,80,80):raise SystemExit("PRIOR_CARDINALITY")
    exclude=legacy|p11|p13o|p13r
    if len(exclude)!=183:raise SystemExit(f"EXCLUDE183_REQUIRED_{len(exclude)}")

    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    pools=defaultdict(list)
    for x in cov:
        sid=int(x["source_id"])
        if sid in exclude:continue
        method="CFOP" if str(x.get("method_raw") or "").strip().upper()=="CFOP" else "NONCFOP"
        recon=str(x.get("reconstructor") or "NULL")
        band="DOMINANT" if recfreq[recon]>=200 else "NONDOMINANT"
        y=year_of(idx[sid]);er=era(y)
        if er=="UNKNOWN":continue
        cell=f"{method}__{band}__{er}"
        pools[cell].append({
          "source_id":sid,"method_family":method,"method_raw":str(x.get("method_raw") or ""),
          "reconstructor":recon,"reconstructor_population_frequency":recfreq[recon],
          "reconstructor_frequency_band":band,"year":y,"selection_era":er,"cell":cell
        })

    counts={c:len(pools[c]) for c in CELLS}
    if any(counts[c]<5 for c in CELLS):raise SystemExit("CELL_SUPPORT_LT5_"+json.dumps(counts,sort_keys=True))

    chosen={}
    for c in CELLS:
        chosen[c]=sorted(pools[c],key=lambda r:(h(SEED+"|"+c,r["source_id"]),r["source_id"]))[:5]

    # Five rounds; every cell contributes one row per round.
    # 16 rows/round distributed by (cell index + 3*round) mod 8 -> exactly 2 rows/batch/round.
    selected=[]
    for ri in range(5):
        for ci,c in enumerate(CELLS):
            r=dict(chosen[c][ri])
            r["selection_round"]=ri+1
            r["batch"]=((ci+3*ri)%8)+1
            selected.append(r)
    if len(selected)!=80 or len({r["source_id"] for r in selected})!=80:raise SystemExit("SELECT80_FAIL")
    if {r["source_id"] for r in selected}&exclude:raise SystemExit("PRIOR183_LEAK")
    cc=Counter(r["cell"] for r in selected);bc=Counter(str(r["batch"]) for r in selected)
    if any(cc[c]!=5 for c in CELLS):raise SystemExit("CELL5_FAIL")
    if any(bc[str(i)]!=10 for i in range(1,9)):raise SystemExit("BATCH10_FAIL")

    selected.sort(key=lambda r:(r["batch"],r["selection_round"],r["cell"],r["source_id"]))
    core={
      "schema_version":"g7-p14-confirm80-selection-manifest-1",
      "phase":"G7-P14",
      "status":"SEALED_BEFORE_CONFIRM80_BODY_CONTACT",
      "seed":SEED,
      "frozen_population_3x3":10591,
      "prior_body_contacted_excluded":183,
      "target_total":80,
      "cell_axes":["method_family","reconstructor_frequency_band","selection_era"],
      "cell_target":5,
      "eligible_cell_counts":counts,
      "selected_cell_counts":dict(sorted(cc.items())),
      "selected_batch_counts":dict(sorted(bc.items())),
      "rows":selected,
      "batches":{str(i):[r["source_id"] for r in selected if r["batch"]==i] for i in range(1,9)},
      "contact_authority":{
        "authorized_after_manifest_seal":True,"max_solves_per_run":10,"batches":8,"min_delay_ms":2000,
        "raw_public_release":"HOLD","bulk_mirror":"HOLD","outcome_triggered_replacement":"FORBIDDEN"
      }
    }
    canonical=json.dumps(core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    core["selection_manifest_sha256"]=hashlib.sha256(canonical).hexdigest()
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"selection-manifest.json").write_text(json.dumps(core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for i in range(1,9):
        (out/f"batch-{i}-source-ids.txt").write_text("\n".join(map(str,core["batches"][str(i)]))+"\n",encoding="utf-8")
    print("G7_P14_CONFIRM80_SELECTION_PASS")
    print("EXCLUDED",len(exclude))
    print("ELIGIBLE_CELLS",json.dumps(counts,sort_keys=True))
    print("SELECTED_CELLS",json.dumps(core["selected_cell_counts"],sort_keys=True))
    print("BATCHES",json.dumps(core["selected_batch_counts"],sort_keys=True))
    print("MANIFEST_SHA256",core["selection_manifest_sha256"])
    for i in range(1,9):print(f"BATCH_{i}",",".join(map(str,core["batches"][str(i)])))

if __name__=="__main__":main()
