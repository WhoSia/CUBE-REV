#!/usr/bin/env python3
import argparse,csv,json,pathlib

EXPECTED={"P11":40,"P13":80,"P14":80,"P15":96}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",action="append",required=True,
                    help="STAGE=prefix-states.tsv,context.jsonl")
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    sources=[]
    for spec in a.source:
        stage,rest=spec.split("=",1)
        states,context=rest.split(",",1)
        if stage not in EXPECTED: raise SystemExit("BAD_STAGE_"+stage)
        sources.append((stage,states,context))
    if {s[0] for s in sources}!=set(EXPECTED): raise SystemExit("STAGES_REQUIRED")

    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    all_rows=[];all_ctx=[];seen=set();stage_solves={}
    header=None
    for stage,sp,cp in sources:
        ctx={}
        for line in open(cp,encoding="utf-8"):
            if line.strip():
                x=json.loads(line)
                x["development_stage"]=stage
                k=(int(x["source_id"]),int(x["prefix_index"]))
                ctx[k]=x
        solves={k[0] for k in ctx}
        if len(solves)!=EXPECTED[stage]:
            raise SystemExit(f"{stage}_SOLVES_{len(solves)}")
        if seen & solves:
            raise SystemExit(f"CROSS_STAGE_SOURCE_OVERLAP_{stage}_{sorted(seen&solves)[:10]}")
        seen |= solves;stage_solves[stage]=len(solves)

        with open(sp,encoding="utf-8",newline="") as f:
            r=csv.DictReader(f,delimiter="\t")
            if header is None: header=r.fieldnames
            elif r.fieldnames!=header: raise SystemExit("HEADER_MISMATCH_"+stage)
            for x in r:
                k=(int(x["source_id"]),int(x["prefix_index"]))
                if k not in ctx: raise SystemExit("STATE_CONTEXT_MISS")
                all_rows.append(x);all_ctx.append(ctx[k])

    if len(seen)!=296: raise SystemExit("UNIQUE296_"+str(len(seen)))
    with open(out/"multicohort-prefix-states.tsv","w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=header,delimiter="\t",lineterminator="\n")
        w.writeheader();w.writerows(all_rows)
    with open(out/"multicohort-context.jsonl","w",encoding="utf-8") as f:
        for x in all_ctx:f.write(json.dumps(x,ensure_ascii=False)+"\n")
    receipt={
      "schema_version":"g7-p16-r2-multicohort-development-reservoir-1",
      "stages":stage_solves,"unique_solves":len(seen),
      "state_rows":len(all_rows),
      "development_only":True,
      "fresh_confirmation_consumed":False,
      "cross_stage_source_overlap":0
    }
    (out/"reservoir-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print("G7_P16_R2_MULTICOHORT_RESERVOIR_PASS")
    print("STAGES",json.dumps(stage_solves,sort_keys=True))
    print("UNIQUE_SOLVES",len(seen),"STATE_ROWS",len(all_rows))

if __name__=="__main__":main()
