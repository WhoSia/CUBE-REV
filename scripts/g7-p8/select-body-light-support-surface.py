#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,unicodedata
from collections import defaultdict,Counter

PLATFORM={"speedcubedb","speed cube database","cubesolv.es","cubesolves","cubedb"}

def norm(x):
    s=unicodedata.normalize("NFKC",str(x or "")).replace("’","'").replace("′","'")
    return " ".join(s.casefold().split())

def year_band(y):
    try: y=int(y)
    except: return "UNKNOWN"
    if y<2015: return "PRE_2015"
    if y<=2020: return "2015_2020"
    if y<=2023: return "2021_2023"
    return "2024_PLUS"

def rank_key(seed,sid):
    return hashlib.sha256(f"{seed}|{sid}".encode()).hexdigest()

def choose_balanced(rows,n,seed):
    by=defaultdict(list)
    for r in rows: by[r["year_band"]].append(r)
    for b in by:
        by[b].sort(key=lambda x:(rank_key(seed,x["source_id"]),x["source_id"]))
    bands=sorted(by)
    out=[]; pos={b:0 for b in bands}
    while len(out)<min(n,len(rows)):
        progressed=False
        for b in bands:
            if len(out)>=n: break
            i=pos[b]
            if i<len(by[b]):
                out.append(by[b][i]); pos[b]+=1; progressed=True
        if not progressed: break
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--index",required=True)
    ap.add_argument("--base-rows",required=True)
    ap.add_argument("--v2",required=True)
    ap.add_argument("--frozen60",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--seed",default="CUBE_REV_G7_P8_SUPPORT_SURFACE_V1")
    args=ap.parse_args()

    base={}
    for line in open(args.base_rows,encoding="utf-8"):
        if line.strip():
            x=json.loads(line); base[int(x["source_id"])]=x
    if len(base)!=10591: raise SystemExit("BASE_10591_REQUIRED")

    idx={}
    for line in open(args.index,encoding="utf-8"):
        if not line.strip(): continue
        x=json.loads(line)
        if x.get("puzzle")=="3x3": idx[int(x["source_id"])]=x
    if len(idx)!=10591 or set(idx)!=set(base): raise SystemExit("INDEX_BASE_MISMATCH")

    v2=json.load(open(args.v2,encoding="utf-8"))
    label_class={x["source_label"]:x["reconciliation_class"] for x in v2["labels"]}
    frozen=json.load(open(args.frozen60,encoding="utf-8"))
    frozen_ids={int(x) for x in frozen["source_id_to_broad_provenance_class"]}
    if len(frozen_ids)!=60: raise SystemExit("FROZEN60_REQUIRED")

    def primary_stratum(sid):
        b=base[sid]["source_label_class"]
        comp=idx[sid].get("competition")
        n=norm(comp)
        if b=="EXACT_NORMALIZED_WCA_COMPETITION_NAME":
            return "WCA_CONTEXT_VISIBLE_OR_RECOVERED"
        if b=="OTHER_UNMATCHED_SOURCE_LABEL" and label_class.get(comp)=="WCA_COMPETITION_ALIAS_STRONG_CONTEXT_RECOVERED_V2":
            return "WCA_CONTEXT_VISIBLE_OR_RECOVERED"
        if b=="MONKEY_LEAGUE_LABEL" or "monkey league" in n:
            return "MONKEY_LEAGUE"
        if b=="RECONSTRUCTION_PLATFORM_LABEL" or n in PLATFORM:
            return "RECONSTRUCTION_PLATFORM"
        if b=="NO_SOURCE_COMPETITION_CONTEXT" or not n or n=="unofficial":
            return "NO_SOURCE_COMPETITION_CONTEXT"
        return "OTHER_OR_UNRESOLVED_SOURCE_LABEL"

    rows=[]
    for sid,x in idx.items():
        if sid in frozen_ids: continue
        y=base[sid].get("year")
        rows.append({
          "source_id":sid,
          "primary_stratum":primary_stratum(sid),
          "year":y,
          "year_band":year_band(y),
          "index_source_label_class":base[sid]["source_label_class"],
          "index_wca_context_support":base[sid]["wca_context_support"],
          "competition":x.get("competition"),
          "solver":x.get("solver"),
          "result":x.get("result")
        })

    strata=[
      "WCA_CONTEXT_VISIBLE_OR_RECOVERED",
      "NO_SOURCE_COMPETITION_CONTEXT",
      "MONKEY_LEAGUE",
      "RECONSTRUCTION_PLATFORM",
      "OTHER_OR_UNRESOLVED_SOURCE_LABEL"
    ]
    pool=defaultdict(list)
    for r in rows: pool[r["primary_stratum"]].append(r)

    selected=[]; allocation={}
    residual=0
    for s in strata:
        take=min(40,len(pool[s]))
        chosen=choose_balanced(pool[s],take,args.seed+"|"+s)
        selected.extend(chosen)
        allocation[s]={"eligible":len(pool[s]),"initial_target":40,"selected":len(chosen)}
        residual+=40-len(chosen)

    if residual:
        # deterministic redistribution across strata with remaining capacity
        remaining=[]
        selected_ids={r["source_id"] for r in selected}
        for s in strata:
            for r in pool[s]:
                if r["source_id"] not in selected_ids:
                    remaining.append(r)
        remaining.sort(key=lambda x:(rank_key(args.seed+"|REDISTRIBUTE",x["source_id"]),x["source_id"]))
        extra=remaining[:residual]
        selected.extend(extra)
        for r in extra: allocation[r["primary_stratum"]]["selected"]+=1

    if len(selected)!=200 or len({r["source_id"] for r in selected})!=200:
        raise SystemExit(f"SELECTION_200_FAILED_{len(selected)}")

    selected.sort(key=lambda r:(strata.index(r["primary_stratum"]),r["year_band"],rank_key(args.seed,r["source_id"]),r["source_id"]))
    manifest_core={
      "schema_version":"g7-p8-body-light-selection-manifest-1",
      "phase":"G7-P8",
      "status":"SEALED_BEFORE_SOURCE_CONTACT",
      "seed":args.seed,
      "population_rows_3x3":10591,
      "frozen60_excluded":60,
      "target_total":200,
      "allocation":allocation,
      "year_band_counts":dict(sorted(Counter(r["year_band"] for r in selected).items())),
      "stratum_counts":dict(sorted(Counter(r["primary_stratum"] for r in selected).items())),
      "rows":selected,
      "contact_authority":{
        "authorized_after_manifest_seal":True,
        "max_body_requests":200,
        "raw_html_retention":False,
        "raw_reconstruction_moves_retention":False
      }
    }
    canonical=json.dumps(manifest_core,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    manifest_core["selection_manifest_sha256"]=hashlib.sha256(canonical).hexdigest()

    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"selection-manifest.json").write_text(json.dumps(manifest_core,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with open(out/"selected-source-ids.txt","w",encoding="utf-8") as f:
        for r in selected: f.write(str(r["source_id"])+"\n")
    print("G7_P8_SELECTION_MANIFEST_PASS")
    print("SELECTED\t200")
    print("STRATA\t"+json.dumps(manifest_core["stratum_counts"],sort_keys=True))
    print("YEAR_BANDS\t"+json.dumps(manifest_core["year_band_counts"],sort_keys=True))
    print("MANIFEST_SHA256\t"+manifest_core["selection_manifest_sha256"])

if __name__=="__main__":
    main()
