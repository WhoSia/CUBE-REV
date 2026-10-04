#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
from collections import Counter,defaultdict

SEED="CUBE_REV_G7_P15_REGIME_STATE_FRESH96_V1"
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

def ids_from_manifest(path):
    x=json.load(open(path,encoding="utf-8"))
    return {int(r["source_id"]) for r in x["rows"]},x

def main():
    ap=argparse.ArgumentParser()
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

    cov=[]
    for line in open(a.covariates,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("frozen_puzzle")=="3x3" and x.get("live_present") is not False:cov.append(x)
    if len(cov)!=10591:raise SystemExit(f"COVARIATE_10591_REQUIRED_{len(cov)}")
    covids={int(x["source_id"]) for x in cov}
    if len(covids)!=10591:raise SystemExit("COVARIATE_IDS_NOT_UNIQUE")

    idx={}
    for line in open(a.frozen_index,encoding="utf-8"):
        if line.strip():
            x=json.loads(line)
            if x.get("puzzle")=="3x3":idx[int(x["source_id"])]=x
    if set(idx)!=covids:raise SystemExit("INDEX_COVARIATE_SET_MISMATCH")

    legacy={int(x) for x in json.load(open(a.legacy60,encoding="utf-8"))["source_id_to_broad_provenance_class"]}
    p11,p11m=ids_from_manifest(a.p11_manifest)
    p13o,p13om=ids_from_manifest(a.p13_original)
    p13r,p13rm=ids_from_manifest(a.p13_repaired)
    p14o,p14om=ids_from_manifest(a.p14_original)
    p14r,p14rm=ids_from_manifest(a.p14_repaired)

    if len(legacy)!=60 or len(p11)!=40 or len(p13o)!=80 or len(p13r)!=80 or len(p14o)!=80 or len(p14r)!=80:
        raise SystemExit("PRIOR_CARDINALITY_FAIL")
    if p13om.get("selection_manifest_sha256")!="d63f292547f38e206e39d58c6e4e7eab0025e9f6fccbb45efe52c7a7e183e4bf":
        raise SystemExit("P13_ORIGINAL_AUTHORITY")
    if p14om.get("selection_manifest_sha256")!="39fa29383ab3b61fb8f2969861ee531a04e50762eaae4fcea4f4144ee8078658":
        raise SystemExit("P14_ORIGINAL_AUTHORITY")
    if not str(p13rm.get("status","")).startswith("SEALED_AFTER_PRE_GEOMETRY"):
        raise SystemExit("P13_REPAIRED_NOT_SEALED")
    if not str(p14rm.get("status","")).startswith("SEALED_AFTER_PRE_GEOMETRY"):
        raise SystemExit("P14_REPAIRED_NOT_SEALED")

    p13_contact=p13o|p13r
    p14_contact=p14o|p14r
    if len(p13_contact)!=83:raise SystemExit(f"P13_CONTACT83_REQUIRED_{len(p13_contact)}")
    if len(p14_contact)!=84:raise SystemExit(f"P14_CONTACT84_REQUIRED_{len(p14_contact)}")
    prior=legacy|p11|p13_contact|p14_contact
    if len(prior)!=267:raise SystemExit(f"PRIOR267_REQUIRED_{len(prior)}")

    recfreq=Counter(str(x.get("reconstructor") or "NULL") for x in cov)
    pools=defaultdict(list)
    for x in cov:
        sid=int(x["source_id"])
        if sid in prior:continue
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
    if any(counts[c]<6 for c in CELLS):raise SystemExit("CELL_SUPPORT_LT6_"+json.dumps(counts,sort_keys=True))

    chosen={}
    for c in CELLS:
        chosen[c]=sorted(pools[c],key=lambda r:(h(SEED+"|"+c,r["source_id"]),r["source_id"]))[:6]

    # Six rounds; each cell contributes exactly one row per round.
    # Batch map is frozen arithmetic: ((9*cell_index + 7*round_index) mod 12)+1.
    # It yields 12x8 exact counts; every batch contains both methods, both bands,
    # and exactly two eras, preventing batch purity on any selection axis.
    selected=[]
    for ri in range(6):
        for ci,c in enumerate(CELLS):
            r=dict(chosen[c][ri])
            r["selection_round"]=ri+1
            r["batch"]=((9*ci+7*ri)%12)+1
            selected.append(r)

    if len(selected)!=96 or len({r["source_id"] for r in selected})!=96:raise SystemExit("SELECT96_FAIL")
    if {r["source_id"] for r in selected}&prior:raise SystemExit("PRIOR267_LEAK")
    cc=Counter(r["cell"] for r in selected);bc=Counter(str(r["batch"]) for r in selected)
    if any(cc[c]!=6 for c in CELLS):raise SystemExit("CELL6_FAIL")
    if any(bc[str(i)]!=8 for i in range(1,13)):raise SystemExit("BATCH8_FAIL")
    batch_mix={}
    for i in range(1,13):
        rr=[r for r in selected if r["batch"]==i]
        mix={
          "method_families":sorted({r["method_family"] for r in rr}),
          "reconstructor_bands":sorted({r["reconstructor_frequency_band"] for r in rr}),
          "eras":sorted({r["selection_era"] for r in rr})
        }
        if len(mix["method_families"])<2 or len(mix["reconstructor_bands"])<2 or len(mix["eras"])<2:
            raise SystemExit("BATCH_AXIS_PURITY_"+str(i))
        batch_mix[str(i)]=mix

    selected.sort(key=lambda r:(r["batch"],r["selection_round"],r["cell"],r["source_id"]))
    core={
      "schema_version":"g7-p15-fresh96-selection-manifest-1",
      "phase":"G7-P15",
      "status":"SEALED_BEFORE_FRESH96_BODY_CONTACT",
      "seed":SEED,
      "frozen_population_3x3":10591,
      "prior_body_contacted_excluded":267,
      "prior_contact_breakdown":{
        "legacy60":60,"p11":40,"p13_original_plus_repairs_unique":83,
        "p14_original_plus_repairs_unique":84
      },
      "target_total":96,
      "cell_axes":["method_family","reconstructor_frequency_band","selection_era"],
      "cell_target":6,
      "eligible_cell_counts":counts,
      "selected_cell_counts":dict(sorted(cc.items())),
      "selected_batch_counts":dict(sorted(bc.items())),
      "batch_axis_mix":batch_mix,
      "rows":selected,
      "batches":{str(i):[r["source_id"] for r in selected if r["batch"]==i] for i in range(1,13)},
      "contact_authority":{
        "authorized_after_manifest_seal":True,"max_solves_per_run":8,"batches":12,"min_delay_ms":2000,
        "raw_public_release":"HOLD","bulk_mirror":"HOLD","outcome_triggered_replacement":"FORBIDDEN",
        "replay_invalid_replacement":"SEPARATE_PRE_GEOMETRY_AMENDMENT_REQUIRED"
      }
    }
    canonical=json.dumps(core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    core["selection_manifest_sha256"]=hashlib.sha256(canonical).hexdigest()
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"selection-manifest.json").write_text(json.dumps(core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for i in range(1,13):
        (out/f"batch-{i}-source-ids.txt").write_text("\n".join(map(str,core["batches"][str(i)]))+"\n",encoding="utf-8")
    print("G7_P15_FRESH96_SELECTION_PASS")
    print("PRIOR_CONTACTED_EXCLUDED",len(prior))
    print("P13_CONTACT_UNIQUE",len(p13_contact))
    print("P14_CONTACT_UNIQUE",len(p14_contact))
    print("ELIGIBLE_CELLS",json.dumps(counts,sort_keys=True))
    print("SELECTED_CELLS",json.dumps(core["selected_cell_counts"],sort_keys=True))
    print("BATCHES",json.dumps(core["selected_batch_counts"],sort_keys=True))
    print("BATCH_MIX",json.dumps(batch_mix,sort_keys=True))
    print("MANIFEST_SHA256",core["selection_manifest_sha256"])
    for i in range(1,13):print(f"BATCH_{i}",",".join(map(str,core["batches"][str(i)])))

if __name__=="__main__":main()
