import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import {parseRecoSolveHtml} from "../g7-p2/parse-reco-html.mjs";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const execute=args.includes("--execute");
const batchNo=Number(val("--batch"));
const outDir=val("--out");
if(!batchNo||!outDir) throw new Error("ARGS");
const manifest=JSON.parse(fs.readFileSync("g7/p7/reco-campaign-manifest.json","utf8"));
const policy=JSON.parse(fs.readFileSync("g7/p2/reco-acquisition-policy.json","utf8"));
const batch=manifest.batches.find(b=>b.batch===batchNo);
if(!batch) throw new Error("BATCH_NOT_FOUND");
if(batch.records.length!==10) throw new Error("BATCH_SIZE");
if(batch.records.length>policy.max_solves_per_run) throw new Error("POLICY_MAX");
if(policy.bulk_authorized!==false) throw new Error("EXPECTED_BOUNDED");
const delayMs=Number(val("--delay-ms",String(policy.min_delay_ms)));
if(delayMs<policy.min_delay_ms) throw new Error("DELAY");
const ids=batch.records.map(r=>r.source_id);
if(new Set(ids).size!==10) throw new Error("DUP_IDS");

if(!execute){
  console.log("G7_P7_RECO_BATCH_DRY_RUN");
  console.log("BATCH\t"+batchNo);
  console.log("IDS\t"+ids.join(","));
  console.log("MAX_SOLVES\t"+ids.length);
  console.log("DELAY_MS\t"+delayMs);
  console.log("EXECUTION\tREFUSED_WITHOUT_--execute");
  process.exit(0);
}

const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const sha256=s=>crypto.createHash("sha256").update(s).digest("hex");
function disallowedByRobots(text,targetPath){
  let active=false;
  for(const raw of text.split(/\r?\n/)){
    const line=raw.replace(/#.*/,"").trim();
    if(!line) continue;
    const [k,...rest]=line.split(":");
    const key=k.trim().toLowerCase(),v=rest.join(":").trim();
    if(key==="user-agent") active=(v==="*");
    else if(active&&key==="disallow"&&v&&targetPath.startsWith(v)) return true;
  }
  return false;
}
const robots=await fetch("https://reco.nz/robots.txt",{headers:{"User-Agent":policy.user_agent}});
let robotsCheck;
if(robots.status===200){
  const txt=await robots.text();
  if(disallowedByRobots(txt,"/solve/")) throw new Error("ROBOTS_DISALLOW_SOLVE");
  robotsCheck="PRESENT_ALLOW";
}else if(robots.status===404) robotsCheck="ABSENT_404";
else throw new Error("ROBOTS_UNREADABLE:"+robots.status);

fs.mkdirSync(path.join(outDir,"raw","solve"),{recursive:true});
fs.mkdirSync(path.join(outDir,"derived"),{recursive:true});
const records=[];
for(let i=0;i<batch.records.length;i++){
  if(i>0) await sleep(delayMs);
  const meta=batch.records[i], id=meta.source_id, url=`https://reco.nz/solve/${id}`;
  const res=await fetch(url,{headers:{"User-Agent":policy.user_agent,"Accept":"text/html,application/xhtml+xml"}});
  if(!res.ok) throw new Error(`HTTP_${res.status}:${id}`);
  const html=await res.text();
  const parsed=parseRecoSolveHtml(html,url);
  if(parsed.source_record_id!==String(id)) throw new Error("ID_MISMATCH:"+id);
  const rawFile=path.join(outDir,"raw","solve",id+".html");
  fs.writeFileSync(rawFile,html);
  records.push({source_id:id,source_url:url,sha256:sha256(html),raw_file:path.relative(outDir,rawFile),selection:meta,parsed});
}
fs.writeFileSync(path.join(outDir,"derived","solves.jsonl"),records.map(JSON.stringify).join("\n")+"\n");
const capture={
  schema_version:"g7-p7-reco-batch-capture-1",
  batch:batchNo,
  source:"reco_nz",
  campaign_manifest:"g7/p7/reco-campaign-manifest.json",
  selection_frozen_before_body_contact:true,
  solve_count:records.length,
  ids,
  delay_ms:delayMs,
  robots_check:robotsCheck,
  bulk_mirror:"HOLD",
  raw_public_release:"HOLD",
  records:records.map(({parsed,...r})=>r)
};
fs.writeFileSync(path.join(outDir,"capture-manifest.json"),JSON.stringify(capture,null,2)+"\n");
console.log("G7_P7_RECO_BATCH_CAPTURE_PASS");
console.log("BATCH\t"+batchNo);
console.log("SOLVES\t"+records.length);
console.log("ROBOTS_CHECK\t"+robotsCheck);
console.log("IDS\t"+ids.join(","));
