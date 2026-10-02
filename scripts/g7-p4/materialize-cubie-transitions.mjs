import fs from "node:fs";
import path from "node:path";
import {parseReconstruction} from "../g7-p2/parse-reconstruction.mjs";
import {solvedStickers,applyAlg,applyToken,isSolvedUpToRotation} from "./facelet-kernel.mjs";
import {toCubie,findSingleHtmTransition,phase1,cubieEqual} from "./cubie-bridge.mjs";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const input=val("--input"),outDir=val("--out","g7/p4/build");
if(!input) throw new Error("INPUT_REQUIRED");
const rows=fs.readFileSync(input,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const records=[],tsv=["source_id\tmove_index\trank_before\trank_after\taction_index\tmethod_family\treconstructor"];
const counts={FRAME_ONLY:0,SINGLE_HTM:0,MULTI_ACTION_EXTENDED:0,UNSUPPORTED:0};
for(const x of rows){
  let stickers=solvedStickers(),error=null;
  try{stickers=applyAlg(stickers,x.parsed.scramble_raw);}catch(e){error="SCRAMBLE:"+e.message;}
  const parsed=parseReconstruction(x.parsed.reconstruction_raw);
  const events=[];
  let moveIndex=0;
  if(!error){
    for(const e of parsed.events){
      if(e.kind==="ANNOTATION"){
        events.push({kind:"ANNOTATION",move_index:moveIndex,annotation:e.annotation,phase1_rank:phase1(toCubie(stickers)).rank});
        continue;
      }
      try{
        const before=toCubie(stickers),q0=phase1(before);
        const afterStickers=applyToken(stickers,e.raw);
        const after=toCubie(afterStickers),q1=phase1(after);
        const tr=findSingleHtmTransition(before,after);
        counts[tr.kind]=(counts[tr.kind]||0)+1;
        moveIndex++;
        const rec={kind:"MOVE",move_index:moveIndex,raw:e.raw,transition_kind:tr.kind,action_index:tr.action_index,canonical_move:tr.move,phase1_before:q0,phase1_after:q1};
        events.push(rec);
        if(tr.kind==="SINGLE_HTM"){
          tsv.push([x.source_id,moveIndex,q0.rank,q1.rank,tr.action_index,x.stratum?.method_family??"",String(x.parsed.reconstructor??"").replace(/\t/g," ")].join("\t"));
        }
        stickers=afterStickers;
      }catch(err){error="MOVE_"+moveIndex+":"+e.raw+":"+err.message;counts.UNSUPPORTED++;break;}
    }
  }
  records.push({
    source_id:x.source_id,
    solver:x.parsed.solver,
    reconstructor:x.parsed.reconstructor,
    method_family:x.stratum?.method_family??null,
    error,
    move_count:moveIndex,
    annotation_count:events.filter(e=>e.kind==="ANNOTATION").length,
    end_solved_up_to_rotation:!error&&isSolvedUpToRotation(stickers),
    events
  });
}
const report={
  schema_version:"g7-p4-cubie-transition-1",
  solve_count:records.length,
  transition_counts:counts,
  single_htm_fraction:(counts.SINGLE_HTM||0)/Math.max(1,(counts.SINGLE_HTM||0)+(counts.FRAME_ONLY||0)+(counts.MULTI_ACTION_EXTENDED||0)),
  records
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"cubie-transitions.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"phase1-single-htm.tsv"),tsv.join("\n")+"\n");
console.log("G7_P4_CUBIE_TRANSITION_PASS");
console.log("SOLVES\t"+records.length);
for(const k of ["SINGLE_HTM","FRAME_ONLY","MULTI_ACTION_EXTENDED","UNSUPPORTED"]) console.log(k+"\t"+(counts[k]||0));
