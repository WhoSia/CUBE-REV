import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const dir=process.argv[2] ?? "/tmp/reco-index-census";
const derived=path.join(dir,"derived");
const censusPath=path.join(derived,"census.json");
const rowsPath=path.join(derived,"index-rows.jsonl");
const logPath=path.join(derived,"execution.log");

for(const p of [censusPath,rowsPath,logPath]){
  if(!fs.existsSync(p) || fs.statSync(p).size===0) throw new Error("CENSUS_REQUIRED_FILE:"+p);
}
const census=JSON.parse(fs.readFileSync(censusPath,"utf8"));
const log=fs.readFileSync(logPath,"utf8");
const rows=fs.readFileSync(rowsPath,"utf8").trim().split(/\r?\n/).filter(Boolean);

if(census.source_id!=="reco_nz") throw new Error("CENSUS_SOURCE");
if(census.scope!=="INDEX_ONLY_NO_SOLVE_BODY_FETCH") throw new Error("CENSUS_SCOPE");
if(!log.includes("G7_P2_RECO_INDEX_CENSUS_PASS")) throw new Error("CENSUS_PASS_MARKER");
if(!log.includes("SOLVE_BODY_REQUESTS\t0")) throw new Error("CENSUS_SOLVE_BODY_NONZERO_OR_MISSING");
if(rows.length!==census.row_count) throw new Error("CENSUS_ROW_COUNT_MISMATCH");
if(census.unique_id_count>census.row_count) throw new Error("CENSUS_UNIQUE_GT_ROWS");
if(!["SHORT_PAGE","EMPTY_PAGE","MAX_PAGE_LIMIT"].includes(census.terminal_reason)) throw new Error("CENSUS_TERMINAL_REASON");

const rawDir=path.join(dir,"raw","index");
const raw=fs.existsSync(rawDir)?fs.readdirSync(rawDir).filter(x=>x.endsWith(".html")).sort():[];
if(raw.length!==census.pages_fetched) throw new Error("CENSUS_RAW_PAGE_COUNT_MISMATCH");

const files=[];
function walk(root){
  for(const ent of fs.readdirSync(root,{withFileTypes:true})){
    const p=path.join(root,ent.name);
    if(ent.isDirectory()) walk(p);
    else if(ent.name!=="SHA256SUMS.txt") files.push(p);
  }
}
walk(dir);
files.sort();
const lines=files.map(p=>{
  const digest=crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
  return digest+"  "+path.relative(dir,p).replaceAll("\\","/");
});
fs.writeFileSync(path.join(dir,"SHA256SUMS.txt"),lines.join("\n")+"\n");

console.log("G7_P2_RECO_INDEX_CENSUS_CUSTODY_PASS");
console.log("PAGES\t"+census.pages_fetched);
console.log("ROWS\t"+census.row_count);
console.log("UNIQUE_IDS\t"+census.unique_id_count);
console.log("RAW_INDEX_FILES\t"+raw.length);
console.log("SOLVE_BODY_REQUESTS\t0");
console.log("SHA256_FILES\t"+files.length);
