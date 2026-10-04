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
if(!outDir||sources.length!==12) throw new Error("ARGS_EXPECT_12_SOURCES");

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
      method_family:sel.method_family??(String(sel.method_raw??"").toUpperCase()==="CFOP"?"CFOP":"NONCFOP"),
      reconstructor_frequency_band:sel.reconstructor_frequency_band??null,
      selection_era:sel.selection_era??null,
      sampling_cell:sel.cell??null
    };
    if(!analysis_meta.reconstructor_frequency_band||!analysis_meta.selection_era||!analysis_meta.sampling_cell)
      throw new Error("MISSING_BALANCE_META:"+id);
    all.push({...x,analysis_meta});
    meta.push({
      source_id:id,
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
if(all.length!==96||ids.size!==96) throw new Error("FRESH96_REQUIRED");

fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"combined-solves.jsonl"),all.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"solve-metadata.jsonl"),meta.map(JSON.stringify).join("\n")+"\n");

const cellCounts=Object.fromEntries([...new Set(meta.map(x=>x.sampling_cell))].sort().map(k=>[k,meta.filter(x=>x.sampling_cell===k).length]));
const cohortCounts=Object.fromEntries([...new Set(meta.map(x=>x.cohort))].sort().map(k=>[k,meta.filter(x=>x.cohort===k).length]));
if(Object.keys(cellCounts).length!==16||Object.values(cellCounts).some(x=>x!==6)) throw new Error("CELL16X6_REQUIRED");
if(Object.keys(cohortCounts).length!==12||Object.values(cohortCounts).some(x=>x!==8)) throw new Error("BATCH12X8_REQUIRED");

fs.writeFileSync(path.join(outDir,"corpus-receipt.json"),JSON.stringify({
  schema_version:"g7-p15-fresh96-corpus-1",
  phase:"G7-P15",
  solves:96,
  unique_source_ids:96,
  cell_counts:cellCounts,
  cohort_counts:cohortCounts,
  fresh_only:true,
  prior_corpora_pooled:false
},null,2)+"\n");
console.log("G7_P15_FRESH96_MERGE_PASS");
console.log("SOLVES\t96");
console.log("CELLS\t"+JSON.stringify(cellCounts));
console.log("COHORTS\t"+JSON.stringify(cohortCounts));
