import fs from "node:fs";
import path from "node:path";
import {parseReconstruction} from "../g7-p2/parse-reconstruction.mjs";
import {solvedStickerCube,applyAlgorithm,applyMoveToken,solvedUpToRotation,toCubieState,cubieSolved,faceActionIndex} from "./sticker-cube.mjs";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const input=val("--input"), outDir=val("--out","g7/p4/build");
if(!input) throw new Error("INPUT_REQUIRED");
const rows=fs.readFileSync(input,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const records=[];
let totalPrefixes=0, exactSolved=0;
for(const x of rows){
  const cube=solvedStickerCube();
  applyAlgorithm(cube,x.parsed.scramble_raw);
  const start=toCubieState(cube);
  const parsed=parseReconstruction(x.parsed.reconstruction_raw);
  if(parsed.status!=="PARSED") throw new Error("UNRESOLVED_AFTER_NORMALIZATION:"+x.source_id);
  const prefixes=[];
  for(let i=0;i<parsed.events.length;i++){
    const e=parsed.events[i];
    if(e.kind==="ANNOTATION") continue;
    applyMoveToken(cube,e.raw);
    const cubie=toCubieState(cube);
    const next=parsed.events[i+1];
    prefixes.push({
      prefix_index:prefixes.length+1,
      raw:e.raw,
      kind:e.kind,
      source_line:e.line,
      face_action_index:faceActionIndex(e.raw),
      boundary_after:next?.kind==="ANNOTATION",
      annotation_after:next?.kind==="ANNOTATION"?next.annotation:null,
      cubie
    });
  }
  const solved_rotation=solvedUpToRotation(cube);
  const solved_canonical=cubieSolved(toCubieState(cube));
  if(solved_rotation&&solved_canonical) exactSolved++;
  records.push({
    source_id:x.source_id,
    solver:x.parsed.solver,
    reconstructor:x.parsed.reconstructor,
    method_family:x.stratum?.method_family??null,
    scramble_raw:x.parsed.scramble_raw,
    move_count:prefixes.length,
    start_cubie:start,
    prefixes,
    final_solved_up_to_rotation:solved_rotation,
    final_canonical_solved:solved_canonical
  });
  totalPrefixes+=prefixes.length;
}
const report={
  schema_version:"g7-p4-exact-trajectory-1",
  solve_count:records.length,
  exact_end_validation_pass:exactSolved,
  total_prefixes:totalPrefixes,
  authority: exactSolved===records.length?"EXACT_EXTENDED_REPLAY_PASS":"HOLD_END_STATE_VALIDATION",
  records
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"exact-trajectories.json"),JSON.stringify(report,null,2)+"\n");
const stateRows=[];
for(const r of records){
  stateRows.push(JSON.stringify({source_id:r.source_id,prefix_index:0,observed_action_index:null,boundary_after:false,cubie:r.start_cubie}));
  for(const p of r.prefixes) stateRows.push(JSON.stringify({
    source_id:r.source_id,prefix_index:p.prefix_index,observed_action_index:p.face_action_index,
    boundary_after:p.boundary_after,annotation_after:p.annotation_after,move_kind:p.kind,raw:p.raw,cubie:p.cubie
  }));
}
fs.writeFileSync(path.join(outDir,"prefix-states.jsonl"),stateRows.join("\n")+"\n");
if(exactSolved!==records.length) throw new Error("P4_END_STATE_VALIDATION");
console.log("G7_P4_EXACT_EXTENDED_REPLAY_PASS");
console.log("SOLVES\t"+records.length);
console.log("TOTAL_PREFIXES\t"+totalPrefixes);
console.log("END_VALIDATION_PASS\t"+exactSolved);
