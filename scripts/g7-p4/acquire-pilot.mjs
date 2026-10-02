import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { parseRecoSolveHtml } from "../g7-p2/parse-reco-html.mjs";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const execute=args.includes("--execute");
const outDir=val("--out","g7/p4/pilot-capture");
const preseal=JSON.parse(fs.readFileSync(val("--preseal","g7/p4/preseal.json"),"utf8"));
const manifest=JSON.parse(fs.readFileSync(val("--manifest","g7/p4/pilot-manifest.json"),"utf8"));
const policy=JSON.parse(fs.readFileSync(val("--policy","g7/p2/reco-acquisition-policy.json"),"utf8"));
const delayMs=Number(val("--delay-ms",String(policy.min_delay_ms)));

if(policy.bulk_authorized!==false) throw new Error("EXPECTED_BOUNDED_POLICY");
if(preseal.pilot_contact.bulk_mirror!=="HOLD") throw new Error("P4_BULK_AUTHORITY_DRIFT");
const ids=manifest.records.map(x=>x.source_id);
if(ids.length!==preseal.pilot_contact.max_solve_bodies) throw new Error("P4_PILOT_COUNT");
if(ids.length>policy.max_solves_per_run) throw new Error("P4_POLICY_SOLVE_LIMIT");
if(JSON.stringify(ids)!==JSON.stringify(preseal.pilot_contact.ids)) throw new Error("P4_MANIFEST_PRESEAL_MISMATCH");
if(delayMs<policy.min_delay_ms) throw new Error("P4_DELAY_TOO_LOW");

if(!execute){
  console.log("G7_P4_PILOT_DRY_RUN");
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
    const key=k.trim().toLowerCase(), v=rest.join(":").trim();
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
  const id=ids[i], url=`https://reco.nz/solve/${id}`;
  const res=await fetch(url,{headers:{"User-Agent":policy.user_agent,"Accept":"text/html,application/xhtml+xml"}});
  if(!res.ok) throw new Error(`HTTP_${res.status}:${id}`);
  const html=await res.text();
  const parsed=parseRecoSolveHtml(html,url);
  if(parsed.source_record_id!==String(id)) throw new Error("ID_MISMATCH:"+id);
  const rawFile=path.join(outDir,"raw","solve",id+".html");
  fs.writeFileSync(rawFile,html);
  records.push({
    source_id:id,
    source_url:url,
    raw_file:path.relative(outDir,rawFile),
    sha256:sha256(html),
    parsed,
    stratum:manifest.records[i]
  });
}
fs.writeFileSync(path.join(outDir,"derived","solves.jsonl"),records.map(x=>JSON.stringify(x)).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"capture-manifest.json"),JSON.stringify({
  schema_version:"g7-p4-pilot-capture-1",
  source:"reco_nz",
  captured_at:new Date().toISOString(),
  selection_frozen_before_contact:true,
  ids,
  solve_count:records.length,
  delay_ms:delayMs,
  robots_check:robotsCheck,
  bulk_mirror:"HOLD",
  raw_public_release:"HOLD",
  records:records.map(({parsed,...x})=>x)
},null,2)+"\n");
console.log("G7_P4_PILOT_CAPTURE_PASS");
console.log("SOLVES\t"+records.length);
console.log("IDS\t"+ids.join(","));
console.log("ROBOTS_CHECK\t"+robotsCheck);
console.log("SOLVE_BODY_REQUESTS\t"+records.length);
console.log("BULK_MIRROR\tHOLD");
