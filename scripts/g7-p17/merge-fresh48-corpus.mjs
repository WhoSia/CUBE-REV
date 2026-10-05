import fs from "node:fs";
import path from "node:path";

const args=process.argv.slice(2);
const outDir=args[args.indexOf("--out")+1];
const sources=[];
for(let i=0;i<args.length;i++){
  if(args[i]==="--source"){
    const v=args[++i],j=v.indexOf("=");
    if(j<1) throw new Error("SOURCE_FORMAT");
    sources.push({cohort:v.slice(0,j),dir:v.slice(j+1)});
  }
}
if(!outDir||sources.length!==6) throw new Error("ARGS_EXPECT_6_SOURCES");

const all=[],meta=[],ids=new Set();
for(const s of sources){
  const p=path.join(s.dir,"derived","solves.jsonl");
  const rows=fs.readFileSync(p,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
  if(rows.length!==8) throw new Error("COHORT_SIZE:"+s.cohort+":"+rows.length);
  for(const x of rows){
    const id=Number(x.source_id);
    if(ids.has(id)) throw new Error("DUP:"+id);
    ids.add(id);
    const sel=x.selection??{};
    const analysis_meta={
      cohort:s.cohort,
      method_family:sel.method_family??null,
      reconstructor_frequency_band:sel.reconstructor_frequency_band??null,
      selection_era:sel.selection_era??null,
      sampling_cell:sel.cell??null
    };
    if(!analysis_meta.method_family||!analysis_meta.reconstructor_frequency_band||!analysis_meta.selection_era||!analysis_meta.sampling_cell)
      throw new Error("MISSING_META:"+id);
    all.push({...x,analysis_meta});
    meta.push({source_id:id,...analysis_meta});
  }
}
if(all.length!==48||ids.size!==48) throw new Error("FRESH48_REQUIRED");
const cells=[...new Set(meta.map(x=>x.sampling_cell))].sort();
const cc=Object.fromEntries(cells.map(k=>[k,meta.filter(x=>x.sampling_cell===k).length]));
if(cells.length!==16||Object.values(cc).some(v=>v!==3)) throw new Error("CELL16X3_REQUIRED");

fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"combined-solves.jsonl"),all.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"solve-metadata.jsonl"),meta.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"corpus-receipt.json"),JSON.stringify({
  schema_version:"g7-p17-p3-fresh48-corpus-1",
  phase:"G7-P17-P3",solves:48,unique_source_ids:48,cell_counts:cc,
  fresh_only:true,prior_contacted_overlap:0
},null,2)+"\n");
console.log("G7_P17_FRESH48_MERGE_PASS");
console.log("SOLVES\t48");
console.log("CELLS\t"+JSON.stringify(cc));
