import fs from "node:fs";
import path from "node:path";

const args=process.argv.slice(2);
const outDir=args[args.indexOf("--out")+1];
if(!outDir) throw new Error("OUT_REQUIRED");
const sources=[];
for(let i=0;i<args.length;i++){
  if(args[i]==="--source"){
    const v=args[++i]; const j=v.indexOf("=");
    if(j<1) throw new Error("SOURCE_FORMAT");
    sources.push({cohort:v.slice(0,j),dir:v.slice(j+1)});
  }
}
if(sources.length!==6) throw new Error("EXPECTED_SIX_ARTIFACT_DIRS");

const all=[], meta=[];
const ids=new Set();
for(const s of sources){
  const p=path.join(s.dir,"derived","solves.jsonl");
  const rows=fs.readFileSync(p,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
  if(rows.length!==10) throw new Error("COHORT_SIZE:"+s.cohort+":"+rows.length);
  for(const x of rows){
    const id=Number(x.source_id);
    if(ids.has(id)) throw new Error("SOURCE_ID_DUPLICATE:"+id);
    ids.add(id);
    const strata=x.stratum??x.selection??{};
    const analysis_meta={
      cohort:s.cohort,
      sampling_role:x.selection?.sampling_role??(s.cohort==="P4_PILOT"?"P4_COVERAGE_PILOT":s.cohort==="P4_CONFIRMATORY"?"P4_POPULATION_CONFIRMATORY":null),
      method_family:strata.method_family??null,
      temporal_era:strata.temporal_era??null,
      solver_frequency_band:strata.solver_frequency_band??null,
      reconstructor_frequency_band:strata.reconstructor_frequency_band??null
    };
    all.push({...x,analysis_meta});
    meta.push({
      source_id:id,cohort:s.cohort,
      solver:x.parsed?.solver??null,reconstructor:x.parsed?.reconstructor??null,
      result_text:x.parsed?.result_text??null,solve_date:x.parsed?.solve_date??null,
      competition:x.parsed?.competition??null,
      ...analysis_meta
    });
  }
}
if(all.length!==60) throw new Error("CORPUS_SIZE");
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"combined-solves.jsonl"),all.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"solve-metadata.jsonl"),meta.map(JSON.stringify).join("\n")+"\n");
const counts=Object.fromEntries([...new Set(meta.map(x=>x.cohort))].sort().map(k=>[k,meta.filter(x=>x.cohort===k).length]));
fs.writeFileSync(path.join(outDir,"corpus-receipt.json"),JSON.stringify({
  schema_version:"g7-p7-reco-60-corpus-1",
  solves:all.length,unique_source_ids:ids.size,cohort_counts:counts,
  raw_public_release:"HOLD",
  source_contact_performed:false
},null,2)+"\n");
console.log("G7_P7_RECO_60_CORPUS_MERGE_PASS");
console.log("SOLVES\t"+all.length);
console.log("COHORTS\t"+JSON.stringify(counts));
