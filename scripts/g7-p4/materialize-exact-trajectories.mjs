import fs from "node:fs";
import path from "node:path";
import {parseReconstruction} from "../g7-p2/parse-reconstruction.mjs";
import {solvedStickers,applyAlg,applyToken,stateSignature,isSolvedUpToRotation,validateStickerState,normalizeToken} from "./facelet-kernel.mjs";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const input=val("--input"), outDir=val("--out","g7/p4/build");
if(!input) throw new Error("INPUT_REQUIRED");
const rows=fs.readFileSync(input,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);

function centerMap(stickers){
  const m=new Map();
  for(const s of stickers){
    const nonzero=s.pos.filter(v=>v!==0).length;
    if(nonzero===1 && s.pos.every((v,i)=>v===s.normal[i])) m.set(s.normal.join(","),s.color);
  }
  if(m.size!==6) throw new Error("CENTER_MAP");
  return m;
}
function solvedness(stickers){
  const centers=centerMap(stickers);
  let correct=0;
  const faceCounts={};
  for(const s of stickers){
    const k=s.normal.join(",");
    const ok=s.color===centers.get(k);
    if(ok) correct++;
    if(!faceCounts[k]) faceCounts[k]={correct:0,total:0};
    faceCounts[k].total++;
    if(ok) faceCounts[k].correct++;
  }
  return {
    center_relative_correct_facelets:correct,
    solved_faces:Object.values(faceCounts).filter(x=>x.correct===x.total).length
  };
}

const records=[];
const support={SUPPORTED:0,UNSUPPORTED_TOKEN:0,END_STATE_NOT_SOLVED:0};
for(const x of rows){
  const parsed=parseReconstruction(x.parsed.reconstruction_raw);
  const moveEvents=parsed.events.filter(e=>e.kind!=="ANNOTATION");
  let cube=solvedStickers();
  let replayStatus="SUPPORTED", error=null;
  try{
    cube=applyAlg(cube,x.parsed.scramble_raw);
  }catch(e){
    replayStatus="UNSUPPORTED_TOKEN"; error="SCRAMBLE:"+e.message;
  }
  const prefixes=[];
  let moveIndex=0;
  if(replayStatus==="SUPPORTED"){
    for(const e of parsed.events){
      if(e.kind==="ANNOTATION"){
        const g=solvedness(cube);
        prefixes.push({
          event_ordinal:e.ordinal,
          move_index:moveIndex,
          event_kind:"ANNOTATION",
          annotation:e.annotation,
          state_signature:stateSignature(cube),
          ...g
        });
        continue;
      }
      try{
        normalizeToken(e.raw);
        cube=applyToken(cube,e.raw);
      }catch(err){
        replayStatus="UNSUPPORTED_TOKEN"; error="MOVE_"+moveIndex+":"+e.raw+":"+err.message; break;
      }
      if(!validateStickerState(cube)){replayStatus="UNSUPPORTED_TOKEN";error="INVALID_STATE";break;}
      moveIndex++;
      const g=solvedness(cube);
      prefixes.push({
        event_ordinal:e.ordinal,
        move_index:moveIndex,
        event_kind:e.kind,
        raw:e.raw,
        state_signature:stateSignature(cube),
        solved_up_to_rotation:isSolvedUpToRotation(cube),
        ...g
      });
    }
  }
  const endSolved=replayStatus==="SUPPORTED" ? isSolvedUpToRotation(cube) : false;
  if(replayStatus==="SUPPORTED"&&!endSolved) replayStatus="END_STATE_NOT_SOLVED";
  support[replayStatus]=(support[replayStatus]||0)+1;
  records.push({
    source_id:x.source_id,
    solver:x.parsed.solver,
    reconstructor:x.parsed.reconstructor,
    method_family:x.stratum?.method_family??null,
    scramble_raw:x.parsed.scramble_raw,
    reconstruction_raw:x.parsed.reconstruction_raw,
    geometry_status:parsed.geometry_status,
    move_count:moveEvents.length,
    replay_status:replayStatus,
    error,
    end_solved_up_to_rotation:endSolved,
    prefixes
  });
}
const report={
  schema_version:"g7-p4-exact-trajectory-1",
  solve_count:records.length,
  replay_status_counts:support,
  supported_fraction:(support.SUPPORTED||0)/records.length,
  state_metric:"CENTER_RELATIVE_FACELET_CORRECTNESS",
  authority_note:"mechanical trajectory validation only; no direct internal-state interpretation",
  records
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"exact-trajectories.json"),JSON.stringify(report,null,2)+"\n");
console.log("G7_P4_EXACT_TRAJECTORY_PASS");
console.log("SOLVES\t"+records.length);
console.log("SUPPORTED\t"+(support.SUPPORTED||0));
console.log("UNSUPPORTED_TOKEN\t"+(support.UNSUPPORTED_TOKEN||0));
console.log("END_STATE_NOT_SOLVED\t"+(support.END_STATE_NOT_SOLVED||0));
