import fs from "node:fs";
import path from "node:path";
import { parseReconstruction } from "../g7-p2/parse-reconstruction.mjs";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const input=val("--input"), outDir=val("--out","g7/p4/build");
if(!input) throw new Error("INPUT_REQUIRED");
const rows=fs.readFileSync(input,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const out=[];
const statusCounts={};
for(const x of rows){
  const p=parseReconstruction(x.parsed.reconstruction_raw);
  const moves=p.events.filter(e=>e.kind!=="ANNOTATION");
  const annotations=p.events.filter(e=>e.kind==="ANNOTATION");
  const kinds={};
  for(const e of moves) kinds[e.kind]=(kinds[e.kind]||0)+1;
  statusCounts[p.geometry_status]=(statusCounts[p.geometry_status]||0)+1;
  const chunkMoveCounts=[];
  let n=0;
  for(const e of p.events){
    if(e.kind==="ANNOTATION"){ chunkMoveCounts.push(n); n=0; }
    else n++;
  }
  if(n||!chunkMoveCounts.length) chunkMoveCounts.push(n);
  out.push({
    source_id:x.source_id,
    solver:x.parsed.solver,
    reconstructor:x.parsed.reconstructor,
    puzzle:x.parsed.puzzle,
    result_text:x.parsed.result_text,
    solve_date:x.parsed.solve_date,
    stratum:x.stratum,
    parse_status:p.status,
    geometry_status:p.geometry_status,
    move_count:moves.length,
    annotation_count:annotations.length,
    move_kind_counts:kinds,
    chunk_move_counts:chunkMoveCounts,
    mean_chunk_moves:chunkMoveCounts.reduce((a,b)=>a+b,0)/chunkMoveCounts.length,
    events:p.events
  });
}
const totalMoves=out.reduce((s,x)=>s+x.move_count,0);
const totalAnnotations=out.reduce((s,x)=>s+x.annotation_count,0);
const report={
  schema_version:"g7-p4-pilot-trajectory-1",
  solve_count:out.length,
  geometry_status_counts:statusCounts,
  total_moves:totalMoves,
  total_annotations:totalAnnotations,
  mean_moves_per_solve:totalMoves/out.length,
  mean_annotations_per_solve:totalAnnotations/out.length,
  exact_replay_authority:"ONLY_AFTER_NOTATION_KERNEL_SUPPORT_AND_END_STATE_VALIDATION",
  source_annotation_authority:"OBSERVED_ANNOTATION_ONLY",
  records:out
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"pilot-trajectory.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"pilot-trajectory-receipt.md"),[
  "# G7-P4 pilot trajectory receipt","",
  `- solves: ${out.length}`,
  `- total moves: ${totalMoves}`,
  `- total annotations: ${totalAnnotations}`,
  `- geometry status: ${JSON.stringify(statusCounts)}`,
  "- source annotations are observational labels, not direct internal-state measurements",
  "- exact replay authority is withheld until notation support and solved-end validation pass"
].join("\n")+"\n");
console.log("G7_P4_PILOT_TRAJECTORY_PASS");
console.log("SOLVES\t"+out.length);
console.log("TOTAL_MOVES\t"+totalMoves);
console.log("TOTAL_ANNOTATIONS\t"+totalAnnotations);
for(const [k,v] of Object.entries(statusCounts)) console.log("GEOMETRY_"+k+"\t"+v);
