import fs from "node:fs";
const exact=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const metadata=fs.readFileSync(process.argv[3],"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const meta=new Map(metadata.map(x=>[Number(x.source_id),x]));
const outTsv=process.argv[4],outCtx=process.argv[5];
if(!outTsv||!outCtx) throw new Error("OUTPUTS_REQUIRED");
const header=["source_id","prefix_index","boundary_after","next_action","cp","co","ep","eo"];
const tsv=[header.join("\t")], ctx=[];
for(const r of exact.records){
  const m=meta.get(Number(r.source_id)); if(!m) throw new Error("META:"+r.source_id);
  const states=[{prefix_index:0,boundary_after:false,annotation_after:null,move_kind:null,raw:null,cubie:r.start_cubie},...r.prefixes];
  for(let i=0;i<states.length;i++){
    const s=states[i], next=i===0?r.prefixes[0]??null:r.prefixes[i]??null;
    const nextAction=next?.face_action_index??-1;
    tsv.push([
      r.source_id,s.prefix_index,s.boundary_after?1:0,nextAction,
      s.cubie.cp.join(","),s.cubie.co.join(","),s.cubie.ep.join(","),s.cubie.eo.join(",")
    ].join("\t"));
    ctx.push({
      source_id:Number(r.source_id),prefix_index:s.prefix_index,
      boundary_after:!!s.boundary_after,annotation_after:s.annotation_after??null,
      current_move_kind:s.move_kind??null,current_move_raw:s.raw??null,
      next_action_index:nextAction>=0?nextAction:null,next_move_kind:next?.kind??null,
      ...m
    });
  }
}
fs.writeFileSync(outTsv,tsv.join("\n")+"\n");
fs.writeFileSync(outCtx,ctx.map(JSON.stringify).join("\n")+"\n");
console.log("G7_P7_PREFIX_CONTEXT_PASS");
console.log("STATE_ROWS\t"+ctx.length);
console.log("BOUNDARY_ROWS\t"+ctx.filter(x=>x.boundary_after).length);
console.log("FACE_NEXT_ROWS\t"+ctx.filter(x=>x.next_action_index!==null).length);
