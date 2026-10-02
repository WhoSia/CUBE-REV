#!/usr/bin/env python3
import argparse,json,pathlib
from collections import Counter

def nonempty(x):
    return x is not None and str(x).strip()!=""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--index",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    rows=[]
    with open(args.index,encoding="utf-8") as f:
        for line in f:
            if line.strip(): rows.append(json.loads(line))
    three=[x for x in rows if x.get("puzzle")=="3x3"]
    keys=Counter()
    for x in rows:
        for k in x.keys(): keys[k]+=1

    method_key="method" if any("method" in x for x in rows) else ("method_family" if any("method_family" in x for x in rows) else None)
    recon_key="reconstructor" if any("reconstructor" in x for x in rows) else None

    def coverage(xs,key):
        if not key: return {"key":None,"present_rows":0,"nonempty_rows":0,"share_nonempty":0.0}
        present=sum(key in x for x in xs)
        ne=sum(nonempty(x.get(key)) for x in xs)
        return {"key":key,"present_rows":present,"nonempty_rows":ne,"share_nonempty":ne/len(xs) if xs else None}

    result={
      "schema_version":"g7-p8-index-method-reconstructor-coverage-audit-1",
      "operation_type":"No-Contact Index Method/Reconstructor Coverage Audit",
      "source_contact":"NONE",
      "rows_all":len(rows),
      "rows_3x3":len(three),
      "all_observed_keys":dict(sorted(keys.items())),
      "method_all":coverage(rows,method_key),
      "method_3x3":coverage(three,method_key),
      "reconstructor_all":coverage(rows,recon_key),
      "reconstructor_3x3":coverage(three,recon_key),
      "sample_values":{
        "method":[str(x.get(method_key)) for x in three if method_key and nonempty(x.get(method_key))][:20],
        "reconstructor":[str(x.get(recon_key)) for x in three if recon_key and nonempty(x.get(recon_key))][:20]
      },
      "boundary":[
        "This audit inspects only retained artifact fields and performs no reco.nz source contact.",
        "Presence of a field in the retained artifact does not establish semantic normalization or correctness.",
        "If coverage is sufficient, population method/reconstructor analysis should prefer the retained index authority over new body contact."
      ]
    }
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/"index-method-reconstructor-coverage-audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P8_INDEX_METHOD_RECONSTRUCTOR_COVERAGE_AUDIT_PASS")
    print("ROWS_ALL\t"+str(len(rows)))
    print("ROWS_3X3\t"+str(len(three)))
    print("METHOD_3X3\t"+json.dumps(result["method_3x3"],sort_keys=True))
    print("RECONSTRUCTOR_3X3\t"+json.dumps(result["reconstructor_3x3"],sort_keys=True))
    print("KEYS\t"+json.dumps(sorted(keys)))

if __name__=="__main__":
    main()
