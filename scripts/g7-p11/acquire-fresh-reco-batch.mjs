import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import {parseRecoSolveHtml} from "../reco/parse-reco-html.mjs";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const execute=args.includes("--execute");
const manifestPath=val("--manifest");
const batchNo=Number(val("--batch"));
const outDir=val("--out");
if(!manifestPath||!batchNo||!outDir) throw new Error("ARGS");
const manifest=JSON.parse(fs.readFileSync(manifestPath,"utf8"));
const policy=JSON.parse(fs.readFileSync("core/reco/reco-acquisition-policy.json","utf8"));
if(manifest.status!=="SEALED_BEFORE_FRESH_BODY_CONTACT") throw new Error("MANIFEST_NOT_SEALED");
if(manifest.target_total!==40) throw new Error("TARGET40");
const ids=manifest.batches?.[String(batchNo)];
if(!Array.isArray(ids)||ids.length!==10) throw new Error("BATCH10_REQUIRED");
if(new Set(ids).size!==10) throw new Error("DUP_IDS");
if(ids.length>policy.max_solves_per_run) throw new Error("POLICY_MAX");
if(policy.bulk_authorized!==false) throw new Error("EXPECTED_BOUNDED");
const rowsById=new Map(manifest.rows.map(x=>[Number(x.source_id),x]));
for(const id of ids) if(!rowsById.has(Number(id))) throw new Error("ID_NOT_IN_MANIFEST:"+id);
const delayMs=Number(val("--delay-ms",String(policy.min_delay_ms)));
if(delayMs<policy.min_delay_ms) throw new Error("DELAY");

if(!execute){
  console.log("G7_P11_RECO_BATCH_DRY_RUN");
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
for(let i=0;i<ids.length;i++){
  if(i>0) await sleep(delayMs);
  const id=Number(ids[i]), selection=rowsById.get(id), url=`https://reco.nz/solve/${id}`;
  const res=await fetch(url,{headers:{"User-Agent":policy.user_agent,"Accept":"text/html,application/xhtml+xml"}});
  if(!res.ok) throw new Error(`HTTP_${res.status}:${id}`);
  const html=await res.text();
  const parsed=parseRecoSolveHtml(html,url);
  if(parsed.source_record_id!==String(id)) throw new Error("ID_MISMATCH:"+id);
  const rawFile=path.join(outDir,"raw","solve",id+".html");
  fs.writeFileSync(rawFile,html);
  records.push({
    source_id:id,source_url:url,sha256:sha256(html),
    raw_file:path.relative(outDir,rawFile),selection,parsed
  });
}
fs.writeFileSync(path.join(outDir,"derived","solves.jsonl"),records.map(JSON.stringify).join("\n")+"\n");
const capture={
  schema_version:"g7-p11-fresh-reco-batch-capture-1",
  phase:"G7-P11",batch:batchNo,source:"reco_nz",
  selection_manifest_sha256:manifest.selection_manifest_sha256,
  selection_frozen_before_body_contact:true,
  solve_count:records.length,ids,delay_ms:delayMs,robots_check:robotsCheck,
  bulk_mirror:"HOLD",raw_public_release:"HOLD",
  records:records.map(({parsed,...r})=>r)
};
fs.writeFileSync(path.join(outDir,"capture-manifest.json"),JSON.stringify(capture,null,2)+"\n");
console.log("G7_P11_RECO_BATCH_CAPTURE_PASS");
console.log("BATCH\t"+batchNo);
console.log("SOLVES\t"+records.length);
console.log("ROBOTS_CHECK\t"+robotsCheck);
console.log("IDS\t"+ids.join(","));
