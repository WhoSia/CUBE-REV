import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import {spawnSync} from "node:child_process";
import {parseRecoSolveHtml} from "../reco/parse-reco-html.mjs";

const args=process.argv.slice(2);
const val=(k)=>{const i=args.indexOf(k);return i>=0?args[i+1]:null;};
const planPath=val("--plan"),basePath=val("--base-manifest"),outDir=val("--out");
if(!planPath||!basePath||!outDir) throw new Error("ARGS");
const plan=JSON.parse(fs.readFileSync(planPath,"utf8"));
const base=JSON.parse(fs.readFileSync(basePath,"utf8"));
if(plan.status!=="FROZEN_PLAN"||plan.base_manifest_sha256!=="671e230314aed38ed68e9c8337c2e64b3f57e2bddca181405d08f5805c78d15e") throw new Error("PLAN");
if(base.selection_manifest_sha256!==plan.base_manifest_sha256) throw new Error("BASE");
const policy=JSON.parse(fs.readFileSync("core/reco/reco-acquisition-policy.json","utf8"));
const delay=Math.max(2000,Number(policy.min_delay_ms));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let lastFetch=0;

function exactReplayOne(record){
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"p19-replay-"));
  const inp=path.join(tmp,"one.jsonl"),out=path.join(tmp,"out");
  fs.writeFileSync(inp,JSON.stringify(record)+"\n");
  const p=spawnSync(process.execPath,["scripts/cube/replay-exact-trajectories.mjs","--input",inp,"--out",out],{encoding:"utf8"});
  let ok=false,detail=(p.stderr||p.stdout||"").trim();
  if(p.status===0){
    const x=JSON.parse(fs.readFileSync(path.join(out,"exact-trajectories.json"),"utf8"));
    ok=x.solve_count===1&&x.exact_end_validation_pass===1;
    detail=ok?"PASS":"END_STATE_FAIL";
  }else if(detail.includes("UNRESOLVED_AFTER_NORMALIZATION")) detail="UNRESOLVED_AFTER_NORMALIZATION";
  else if(detail.includes("P4_END_STATE_VALIDATION")) detail="END_STATE_FAIL";
  else detail="REPLAY_ERROR";
  fs.rmSync(tmp,{recursive:true,force:true});
  return {ok,detail};
}
async function fetchRecord(meta){
  const now=Date.now(),wait=Math.max(0,delay-(now-lastFetch));
  if(wait) await sleep(wait);
  const id=Number(meta.source_id),url=`https://reco.nz/solve/${id}`;
  const res=await fetch(url,{headers:{"User-Agent":policy.user_agent,"Accept":"text/html,application/xhtml+xml"}});
  lastFetch=Date.now();
  if(!res.ok)return {ok:false,detail:"HTTP_"+res.status,id};
  const html=await res.text(),parsed=parseRecoSolveHtml(html,url);
  if(parsed.source_record_id!==String(id))return {ok:false,detail:"ID_MISMATCH",id};
  return {ok:true,id,html,record:{source_id:id,source_url:url,selection:meta,parsed}};
}
const robots=await fetch("https://reco.nz/robots.txt",{headers:{"User-Agent":policy.user_agent}});
if(![200,404].includes(robots.status)) throw new Error("ROBOTS_"+robots.status);

fs.mkdirSync(path.join(outDir,"raw","solve"),{recursive:true});
fs.mkdirSync(path.join(outDir,"batch6","derived"),{recursive:true});
const audit=[],finalBatchRecords=[],finalRows=base.rows.map(x=>({...x}));
const used=new Set(finalRows.map(x=>Number(x.source_id)));
const contacted=new Set();

for(const current of plan.scan_rows){
  const first=await fetchRecord(current);
  if(!first.ok)throw new Error("CURRENT_FETCH_FAIL:"+current.source_id+":"+first.detail);
  contacted.add(Number(current.source_id));
  const rep=exactReplayOne(first.record);
  audit.push({role:"current",source_id:current.source_id,batch:current.batch,cell:current.cell,replay:rep.detail});
  if(rep.ok){
    fs.writeFileSync(path.join(outDir,"raw","solve",current.source_id+".html"),first.html);
    finalBatchRecords.push(first.record);
    continue;
  }
  let chosen=null;
  for(const cand of plan.candidate_queues[String(current.source_id)]){
    if(used.has(Number(cand.source_id))||contacted.has(Number(cand.source_id)))continue;
    const f=await fetchRecord(cand);contacted.add(Number(cand.source_id));
    if(!f.ok){audit.push({role:"candidate",replaces:current.source_id,source_id:cand.source_id,batch:cand.batch,replay:f.detail});continue;}
    const rr=exactReplayOne(f.record);
    audit.push({role:"candidate",replaces:current.source_id,source_id:cand.source_id,batch:cand.batch,cell:cand.cell,replay:rr.detail});
    if(rr.ok){chosen={meta:cand,html:f.html,record:f.record};break;}
  }
  if(!chosen)throw new Error("ADMISSIBILITY_QUEUE_EXHAUSTED:"+current.source_id);
  used.delete(Number(current.source_id));used.add(Number(chosen.meta.source_id));
  const idx=finalRows.findIndex(r=>Number(r.source_id)===Number(current.source_id));
  finalRows[idx]=chosen.meta;
  fs.writeFileSync(path.join(outDir,"raw","solve",chosen.meta.source_id+".html"),chosen.html);
  finalBatchRecords.push(chosen.record);
}
if(finalBatchRecords.length!==8||new Set(finalBatchRecords.map(x=>x.source_id)).size!==8)throw new Error("FINAL8_BATCH6");
fs.writeFileSync(path.join(outDir,"batch6","derived","solves.jsonl"),finalBatchRecords.map(JSON.stringify).join("\n")+"\n");
const cc={};for(const r of finalRows)cc[r.cell]=(cc[r.cell]||0)+1;
if(Object.keys(cc).length!==16||Object.values(cc).some(v=>v!==3))throw new Error("CELL16X3");
const batches={};for(let i=1;i<=6;i++)batches[String(i)]=finalRows.filter(r=>Number(r.batch)===i).map(r=>Number(r.source_id));
if(Object.values(batches).some(v=>v.length!==8))throw new Error("BATCH6X8");
const finalManifest={
  schema_version:"g7-p19-p3-fresh48-selection-manifest-2-replay-repaired",
  phase:"G7-P19-P3",
  status:"SEALED_AFTER_FAILED_BATCH_REPLAY_ADMISSIBILITY_REPAIR",
  supersedes_manifest_sha256:base.selection_manifest_sha256,
  target_total:48,
  prior_body_contacted_excluded:418,
  selected_cell_counts:cc,
  rows:finalRows,
  batches,
  repair_audit:audit,
  newly_contacted_during_repair:[...contacted].sort((a,b)=>a-b),
  selection_rule:plan.selection_rule
};
const canonical=JSON.stringify(finalManifest,Object.keys(finalManifest).sort());
finalManifest.selection_manifest_sha256=crypto.createHash("sha256").update(canonical).digest("hex");
fs.writeFileSync(path.join(outDir,"selection-manifest-repaired.json"),JSON.stringify(finalManifest,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"replay-admissibility-audit.json"),JSON.stringify(audit,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"repair-contacted-source-ids.txt"),[...contacted].sort((a,b)=>a-b).join("\n")+"\n");
console.log("G7_P19_P3_R1_ADMISSIBILITY_SCAN_PASS");
console.log("FINAL_BATCH6\t"+finalBatchRecords.map(x=>x.source_id).join(","));
console.log("REPAIR_AUDIT\t"+JSON.stringify(audit));
console.log("REPAIR_CONTACTED\t"+[...contacted].sort((a,b)=>a-b).join(","));
console.log("FINAL_MANIFEST_SHA256\t"+finalManifest.selection_manifest_sha256);
