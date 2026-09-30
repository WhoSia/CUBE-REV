import fs from "node:fs";
import path from "node:path";

const dir=process.argv[2] ?? "g7/p2/reco-live-probe";
const manifest=JSON.parse(fs.readFileSync(path.join(dir,"capture-manifest.json"),"utf8"));
const lines=fs.readFileSync(path.join(dir,"derived","solves.jsonl"),"utf8").trim().split(/\r?\n/).filter(Boolean);
const rows=lines.map(JSON.parse);

if(manifest.source_id!=="reco_nz") throw new Error("PROBE_SOURCE");
if(manifest.solve_count!==5 || rows.length!==5) throw new Error("PROBE_COUNT");
if(manifest.puzzle_filter!=="3x3") throw new Error("PROBE_PUZZLE_FILTER");
for(const r of rows){
  if(r.puzzle!=="3x3") throw new Error("PROBE_NON_3X3:"+r.source_record_id);
  if(!r.scramble_raw || !r.reconstruction_raw) throw new Error("PROBE_EMPTY_RECON:"+r.source_record_id);
  if(!r.stats || !r.stats.Time || !r.stats.STM) throw new Error("PROBE_STATS_MISSING:"+r.source_record_id);
}
console.log("G7_P2_RECO_LIVE_PROBE_PASS");
console.log("SOLVES\t"+rows.length);
console.log("IDS\t"+rows.map(r=>r.source_record_id).join(","));
console.log("PUZZLES\t"+[...new Set(rows.map(r=>r.puzzle))].join(","));
console.log("RECONSTRUCTIONS_NONEMPTY\t"+rows.filter(r=>r.reconstruction_raw.length>0).length);
console.log("STATS_PRESENT\t"+rows.filter(r=>r.stats?.Time?.Total && r.stats?.STM?.Total).length);
console.log("RAW_PUBLIC_RELEASE\tNO");
