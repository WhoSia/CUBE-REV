#!/usr/bin/env python3
import hashlib, json, pathlib, pickletools, sys
root=pathlib.Path(sys.argv[1])
manifest=json.load(open("g7/p6/nuzzi-intake-manifest.json",encoding="utf-8"))
rows=[]
for entry in manifest["files"]:
    p=root/pathlib.Path(entry["path"]).name
    data=p.read_bytes()
    protocols=[]
    globals_seen=[]
    opcounts={}
    error=None
    try:
        for op,arg,pos in pickletools.genops(data):
            opcounts[op.name]=opcounts.get(op.name,0)+1
            if op.name=="PROTO": protocols.append(arg)
            if op.name in ("GLOBAL","STACK_GLOBAL"): globals_seen.append(str(arg))
    except Exception as e:
        error=f"{type(e).__name__}:{e}"
    rows.append({
      "file":entry["path"],"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
      "pickle_protocols":protocols,"opcode_count":sum(opcounts.values()),
      "global_opcode_count":len(globals_seen),"global_opcode_args":globals_seen[:100],
      "static_parse_error":error
    })
report={
 "schema_version":"g7-p6-nuzzi-static-audit-1",
 "source_commit":manifest["source"]["commit"],
 "files":rows,
 "unpickle_performed":False,
 "raw_public_release":"HOLD"
}
out=root/"static-audit.json"
out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("G7_P6_NUZZI_STATIC_AUDIT_PASS")
for r in rows:
 print(f"{r['file']}\t{r['bytes']}\t{r['sha256']}\t{r['static_parse_error'] or 'PARSED'}")
