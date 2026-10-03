import fs from "node:fs";
import path from "node:path";

const args=process.argv.slice(2);
const outDir=args[args.indexOf("--out")+1];
if(!outDir) throw new Error("OUT_REQUIRED");
const sources=[];
for(let i=0;i<args.length;i++){
  if(args[i]==="--source"){
    const v=args[++i],j=v.indexOf("=");
    if(j<1) throw new Error("SOURCE_FORMAT");
    sources.push({cohort:v.slice(0,j),dir:v.slice(j+1)});
  }
}
if(sources.length!==8) throw new Error("EXPECTED_EIGHT_BATCHES");
const all=[],meta=[]; const ids=new Set();
for(const s of sources){
  const p=path.join(s.dir,"derived","solves.jsonl");
  const rows=fs.readFileSync(p,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
  if(rows.length!==10) throw new Error("COHORT_SIZE:"+s.cohort+":"+rows.length);
  for(const x of rows){
    const id=Number(x.source_id);
    if(ids.has(id)) throw new Error("SOURCE_ID_DUPLICATE:"+id);
    ids.add(id);
    const sel=x.selection??{};
    const method_family=String(sel.method_raw??"").toUpperCase()==="CFOP"?"CFOP":"NONCFOP";
    const recon_band=String(sel.cell??"").includes("NONDOMINANT_RECONSTRUCTOR")?"NONDOMINANT":"DOMINANT";
    const analysis_meta={
      cohort:s.cohort,
      method_family,
      reconstructor_frequency_band:recon_band,
      sampling_cell:sel.cell??null,
      selection_era:sel.era??null
    };
    all.push({...x,analysis_meta});
    meta.push({
      source_id:id,cohort:s.cohort,
      solver:x.parsed?.solver??null,
      reconstructor:x.parsed?.reconstructor??null,
      result_text:x.parsed?.result_text??null,
      source_display_date:x.parsed?.source_display_date??null,
      solve_date:null,
      competition:x.parsed?.competition??null,
      ...analysis_meta
    });
  }
}
if(all.length!==80||ids.size!==80) throw new Error("FRESH80_REQUIRED");
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"combined-solves.jsonl"),all.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"solve-metadata.jsonl"),meta.map(JSON.stringify).join("\n")+"\n");
const cellCounts=Object.fromEntries([...new Set(meta.map(x=>x.sampling_cell))].sort().map(k=>[k,meta.filter(x=>x.sampling_cell===k).length]));
if(Object.values(cellCounts).some(x=>x!==20)) throw new Error("CELL20_REQUIRED");
fs.writeFileSync(path.join(outDir,"corpus-receipt.json"),JSON.stringify({
  schema_version:"g7-p13-fresh80-corpus-1",solves:80,unique_source_ids:80,
  cohort_counts:Object.fromEntries([...new Set(meta.map(x=>x.cohort))].sort().map(k=>[k,meta.filter(x=>x.cohort===k).length])),
  cell_counts:cellCounts,fresh_only:true,prior100_pooled:false,source_contact_performed:false
},null,2)+"\n");
console.log("G7_P13_FRESH80_MERGE_PASS");
console.log("SOLVES\t80");
console.log("CELLS\t"+JSON.stringify(cellCounts));
