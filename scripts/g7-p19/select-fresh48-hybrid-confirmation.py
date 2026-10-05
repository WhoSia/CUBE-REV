#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter,defaultdict

SEED="CUBE_REV_G7_P19_HYBRID_CONFIRMATION_V1"
EXCLUSION_SHA="da2b4ac80970ee77fe64c15ac60745afa24d29995291438bb05026e8220fd1cc"
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
    ap.add_argument("--exclusion-census",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    census=json.load(open(a.exclusion_census,encoding="utf-8"))
    if census["counts"]["all_prior_contacted_through_p17"]!=418:raise SystemExit("PRIOR418_REQUIRED")
    if census["exclusion_list_sha256"]!=EXCLUSION_SHA:raise SystemExit("EXCLUSION_SHA")
    excluded={int(r["source_id"]) for r in census["contacted_ids"]}
    if len(excluded)!=418:raise SystemExit("EXCLUSION_CARDINALITY")

    cov=[]
    for line in open(a.covariates,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("frozen_puzzle")=="3x3" and x.get("live_present") is not False:cov.append(x)
    if len(cov)!=10591:raise SystemExit("COV10591")
    covids={int(x["source_id"]) for x in cov}

    idx={}
    for line in open(a.frozen_index,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("puzzle")=="3x3":idx[int(x["source_id"])]=x
    if set(idx)!=covids:raise SystemExit("FRAME_MISMATCH")

    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    pools=defaultdict(list)
    for x in cov:
        sid=int(x["source_id"])
        if sid in excluded:continue
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

    elig={c:len(pools[c]) for c in CELLS}
    if any(elig[c]<3 for c in CELLS):raise SystemExit("CELL_SUPPORT_LT3_"+json.dumps(elig,sort_keys=True))

    chosen={}
    for c in CELLS:
        chosen[c]=sorted(pools[c],key=lambda r:(h(SEED+"|"+c,r["source_id"]),r["source_id"]))[:3]

    selected=[]
    for ri in range(3):
        for ci,c in enumerate(CELLS):
            r=dict(chosen[c][ri]);r["selection_round"]=ri+1
            r["batch"]=((ci+2*ri)%6)+1
            selected.append(r)

    if len(selected)!=48 or len({r["source_id"] for r in selected})!=48:raise SystemExit("SELECT48")
    if {r["source_id"] for r in selected}&excluded:raise SystemExit("CONTACT_LEAK")
    cc=Counter(r["cell"] for r in selected);bc=Counter(str(r["batch"]) for r in selected)
    if any(cc[c]!=3 for c in CELLS):raise SystemExit("CELL16X3")
    if any(bc[str(i)]!=8 for i in range(1,7)):raise SystemExit("BATCH6X8")

    mix={}
    for i in range(1,7):
        rr=[r for r in selected if r["batch"]==i]
        m={
          "method_families":sorted({r["method_family"] for r in rr}),
          "reconstructor_bands":sorted({r["reconstructor_frequency_band"] for r in rr}),
          "eras":sorted({r["selection_era"] for r in rr})
        }
        if len(m["method_families"])<2 or len(m["reconstructor_bands"])<2 or len(m["eras"])<2:
            raise SystemExit("BATCH_PURITY_"+str(i))
        mix[str(i)]=m

    selected.sort(key=lambda r:(r["batch"],r["selection_round"],r["cell"],r["source_id"]))
    core={
      "schema_version":"g7-p19-p2-fresh48-selection-manifest-1",
      "phase":"G7-P19-P2",
      "status":"SEALED_BEFORE_FRESH48_BODY_CONTACT",
      "seed":SEED,
      "frozen_population_3x3":10591,
      "prior_body_contacted_excluded":418,
      "exclusion_list_sha256":EXCLUSION_SHA,
      "target_total":48,
      "selected_cell_counts":dict(sorted(cc.items())),
      "selected_batch_counts":dict(sorted(bc.items())),
      "batch_axis_mix":mix,
      "rows":selected,
      "batches":{str(i):[r["source_id"] for r in selected if r["batch"]==i] for i in range(1,7)},
      "contact_authority":{"max_solves_per_batch":8,"batches":6,"min_delay_ms":2000,"raw_public_release":"HOLD","bulk_mirror":"HOLD"}
    }
    canon=json.dumps(core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    core["selection_manifest_sha256"]=hashlib.sha256(canon).hexdigest()

    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"selection-manifest.json").write_text(json.dumps(core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for i in range(1,7):
        (out/f"batch-{i}-source-ids.txt").write_text("\n".join(map(str,core["batches"][str(i)]))+"\n",encoding="utf-8")

    print("G7_P19_P2_FRESH48_SELECTION_PASS")
    print("EXCLUDED",len(excluded))
    print("CELLS",json.dumps(core["selected_cell_counts"],sort_keys=True))
    print("BATCHES",json.dumps(core["selected_batch_counts"],sort_keys=True))
    print("MANIFEST_SHA256",core["selection_manifest_sha256"])

if __name__=="__main__":main()
