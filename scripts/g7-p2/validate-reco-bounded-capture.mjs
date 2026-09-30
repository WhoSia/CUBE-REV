import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const dir=process.argv[2] ?? "g7/p2/reco-capture";
const expected=Number(process.argv[3] ?? "10");
if(!Number.isInteger(expected)||expected<1) throw new Error("BOUNDED_EXPECTED_COUNT");

const manifestPath=path.join(dir,"capture-manifest.json");
const solvesPath=path.join(dir,"derived","solves.jsonl");
if(!fs.existsSync(manifestPath)) throw new Error("BOUNDED_MANIFEST_MISSING");
if(!fs.existsSync(solvesPath)) throw new Error("BOUNDED_SOLVES_MISSING");

const manifest=JSON.parse(fs.readFileSync(manifestPath,"utf8"));
const lines=fs.readFileSync(solvesPath,"utf8").trim().split(/\r?\n/).filter(Boolean);
const rows=lines.map(JSON.parse);
const rawSolveDir=path.join(dir,"raw","solve");
const rawFiles=fs.existsSync(rawSolveDir)
  ? fs.readdirSync(rawSolveDir).filter(x=>x.endsWith(".html")).sort()
  : [];
const sha256=s=>crypto.createHash("sha256").update(s).digest("hex");

if(manifest.source_id!=="reco_nz") throw new Error("BOUNDED_SOURCE");
if(manifest.solve_count!==expected) throw new Error(`BOUNDED_MANIFEST_COUNT:${manifest.solve_count}`);
if(rows.length!==expected) throw new Error(`BOUNDED_ROWS_COUNT:${rows.length}`);
if(rawFiles.length!==expected) throw new Error(`BOUNDED_RAW_COUNT:${rawFiles.length}`);
if(manifest.puzzle_filter!=="3x3") throw new Error("BOUNDED_PUZZLE_FILTER");
if(manifest.robots_check!=="ABSENT_404" && manifest.robots_check!=="PRESENT_ALLOW") throw new Error("BOUNDED_ROBOTS");

const manifestById=new Map((manifest.records??[]).map(x=>[String(x.id),x]));
const ids=[];
for(const r of rows){
  const id=String(r.source_record_id??"");
  ids.push(id);
  if(!/^\d+$/.test(id)) throw new Error("BOUNDED_BAD_ID:"+id);
  if(r.puzzle!=="3x3") throw new Error("BOUNDED_NON_3X3:"+id);
  if(!r.scramble_raw || !r.reconstruction_raw) throw new Error("BOUNDED_EMPTY_RECON:"+id);
  if(!r.stats || !r.stats.Time || !r.stats.STM) throw new Error("BOUNDED_STATS_MISSING:"+id);
  const m=manifestById.get(id);
  if(!m) throw new Error("BOUNDED_MANIFEST_RECORD_MISSING:"+id);
  const rawPath=path.join(dir,m.raw_file);
  if(!fs.existsSync(rawPath)) throw new Error("BOUNDED_RAW_MISSING:"+id);
  const html=fs.readFileSync(rawPath,"utf8");
  if(sha256(html)!==m.sha256) throw new Error("BOUNDED_SHA_MISMATCH:"+id);
}
if(new Set(ids).size!==expected) throw new Error("BOUNDED_DUPLICATE_ID");

console.log("G7_P2_RECO_BOUNDED_CAPTURE_VALIDATION_PASS");
console.log("EXPECTED\t"+expected);
console.log("SOLVES\t"+rows.length);
console.log("RAW_HTML_FILES\t"+rawFiles.length);
console.log("IDS\t"+ids.join(","));
console.log("RECONSTRUCTIONS_NONEMPTY\t"+rows.filter(r=>r.reconstruction_raw.length>0).length);
console.log("STATS_PRESENT\t"+rows.filter(r=>r.stats?.Time?.Total && r.stats?.STM?.Total).length);
console.log("ROBOTS_CHECK\t"+manifest.robots_check);
console.log("RAW_PUBLIC_RELEASE\tNO");
