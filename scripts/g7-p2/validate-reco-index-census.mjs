import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const dir=process.argv[2] ?? "/tmp/reco-index-census";
const censusPath=path.join(dir,"derived","census.json");
const rowsPath=path.join(dir,"derived","index-rows.jsonl");
const logPath=path.join(dir,"derived","execution.log");

for(const p of [censusPath,rowsPath,logPath]){
  if(!fs.existsSync(p) || fs.statSync(p).size===0) throw new Error("CENSUS_ARTIFACT_MISSING:"+p);
}

const census=JSON.parse(fs.readFileSync(censusPath,"utf8"));
const rows=fs.readFileSync(rowsPath,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const log=fs.readFileSync(logPath,"utf8");

if(census.source_id!=="reco_nz") throw new Error("CENSUS_SOURCE");
if(census.scope!=="INDEX_ONLY_NO_SOLVE_BODY_FETCH") throw new Error("CENSUS_SCOPE");
if(census.robots_check!=="ABSENT_404" && census.robots_check!=="PRESENT_ALLOW") throw new Error("CENSUS_ROBOTS");
if(!["SHORT_PAGE","EMPTY_PAGE"].includes(census.terminal_reason)) throw new Error("CENSUS_NOT_COMPLETE:"+census.terminal_reason);
if(census.row_count!==rows.length) throw new Error("CENSUS_ROW_COUNT");
if(census.unique_id_count!==new Set(rows.map(r=>r.id)).size) throw new Error("CENSUS_UNIQUE_ID_COUNT");
if(census.duplicate_id_groups.length!==0) throw new Error("CENSUS_DUPLICATE_IDS");
if(!log.includes("G7_P2_RECO_INDEX_CENSUS_PASS")) throw new Error("CENSUS_PASS_MARKER_MISSING");
if(!/SOLVE_BODY_REQUESTS\s+0/.test(log)) throw new Error("CENSUS_SOLVE_BODY_ZERO_MISSING");

const pageFiles=fs.readdirSync(path.join(dir,"raw","index")).filter(x=>x.endsWith(".html"));
if(pageFiles.length!==census.pages_fetched) throw new Error("CENSUS_PAGE_FILE_COUNT");

const sumFile=path.join(dir,"SHA256SUMS.txt");
const files=[];
for(const base of ["raw/index","derived"]){
  const root=path.join(dir,base);
  for(const name of fs.readdirSync(root)){
    const p=path.join(root,name);
    if(fs.statSync(p).isFile()){
      const rel=path.relative(dir,p).replaceAll(path.sep,"/");
      const digest=crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
      files.push({rel,digest});
    }
  }
}
files.sort((a,b)=>a.rel.localeCompare(b.rel));
fs.writeFileSync(sumFile,files.map(x=>x.digest+"  "+x.rel).join("\n")+"\n");

console.log("G7_P2_RECO_INDEX_CENSUS_ARTIFACT_PASS");
console.log("PAGES\t"+census.pages_fetched);
console.log("ROWS\t"+census.row_count);
console.log("UNIQUE_IDS\t"+census.unique_id_count);
console.log("TERMINAL_REASON\t"+census.terminal_reason);
console.log("SOLVE_BODY_REQUESTS\t0");
