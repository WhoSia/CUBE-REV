import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { parseRecoIndexHtml, parseRecoSolveHtml } from "./parse-reco-html.mjs";

const args=process.argv.slice(2);
const has=x=>args.includes(x);
const value=(name,def=null)=>{
  const i=args.indexOf(name);
  return i>=0 && i+1<args.length ? args[i+1] : def;
};

const policyPath=value("--policy","g7/p2/reco-acquisition-policy.json");
const policy=JSON.parse(fs.readFileSync(policyPath,"utf8"));
const execute=has("--execute");
const refresh=has("--refresh");
const outDir=value("--out","g7/p2/reco-capture");
const pageStart=Number(value("--page-start","1"));
const pages=Number(value("--pages","1"));
const maxSolves=Number(value("--max-solves","5"));
const delayMs=Number(value("--delay-ms",String(policy.min_delay_ms)));

if(policy.source_id!=="reco_nz") throw new Error("RECO_POLICY_SOURCE");
if(policy.bulk_authorized!==true){
  if(pages>policy.max_index_pages_per_run) throw new Error("RECO_INDEX_PAGE_LIMIT");
  if(maxSolves>policy.max_solves_per_run) throw new Error("RECO_SOLVE_LIMIT");
}
if(delayMs<policy.min_delay_ms) throw new Error("RECO_DELAY_TOO_LOW");
if(!Number.isInteger(pageStart)||pageStart<1||!Number.isInteger(pages)||pages<1) throw new Error("RECO_PAGE_ARGS");
if(!Number.isInteger(maxSolves)||maxSolves<1) throw new Error("RECO_SOLVE_ARGS");

const indexUrls=Array.from({length:pages},(_,i)=>`https://reco.nz/?page=${pageStart+i}`);
if(!execute){
  console.log("G7_P2_RECO_ACQUISITION_DRY_RUN");
  console.log("MODE\t"+policy.mode);
  console.log("INDEX_URLS\t"+indexUrls.join(","));
  console.log("MAX_SOLVES\t"+maxSolves);
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
    const key=k.trim().toLowerCase();
    const val=rest.join(":").trim();
    if(key==="user-agent") active=(val==="*");
    else if(active && key==="disallow" && val && targetPath.startsWith(val)) return true;
  }
  return false;
}

async function get(url){
  const res=await fetch(url,{headers:{"User-Agent":policy.user_agent,"Accept":"text/html,application/xhtml+xml"}});
  if(!res.ok) throw new Error(`HTTP_${res.status}:${url}`);
  return {text:await res.text(),headers:Object.fromEntries(res.headers.entries())};
}

const robotsRes=await fetch("https://reco.nz/robots.txt",{headers:{"User-Agent":policy.user_agent}});
if(!robotsRes.ok) throw new Error("RECO_ROBOTS_UNREADABLE:"+robotsRes.status);
const robotsText=await robotsRes.text();
for(const target of ["/","/solve/"]){
  if(disallowedByRobots(robotsText,target)) throw new Error("RECO_ROBOTS_DISALLOW:"+target);
}

fs.mkdirSync(path.join(outDir,"raw","index"),{recursive:true});
fs.mkdirSync(path.join(outDir,"raw","solve"),{recursive:true});
fs.mkdirSync(path.join(outDir,"derived"),{recursive:true});

const discovered=[];
for(let i=0;i<indexUrls.length;i++){
  const url=indexUrls[i];
  const page=pageStart+i;
  const target=path.join(outDir,"raw","index",`page-${String(page).padStart(4,"0")}.html`);
  let html;
  if(fs.existsSync(target)&&!refresh){
    html=fs.readFileSync(target,"utf8");
  }else{
    if(i>0) await sleep(delayMs);
    html=(await get(url)).text;
    fs.writeFileSync(target,html);
  }
  const parsed=parseRecoIndexHtml(html);
  for(const id of parsed.solve_ids) discovered.push(id);
}
const ids=[...new Set(discovered)].slice(0,maxSolves);

const manifest=[];
for(let i=0;i<ids.length;i++){
  const id=ids[i];
  const url=`https://reco.nz/solve/${id}`;
  const target=path.join(outDir,"raw","solve",`${id}.html`);
  let html,source="cache";
  if(fs.existsSync(target)&&!refresh){
    html=fs.readFileSync(target,"utf8");
  }else{
    await sleep(delayMs);
    const got=await get(url);
    html=got.text;
    fs.writeFileSync(target,html);
    source="network";
  }
  const parsed=parseRecoSolveHtml(html,url);
  if(parsed.source_record_id!==String(id)) throw new Error("RECO_ID_MISMATCH:"+id);
  manifest.push({id,url,raw_file:path.relative(outDir,target),sha256:sha256(html),source,parsed});
}
fs.writeFileSync(path.join(outDir,"derived","solves.jsonl"),manifest.map(x=>JSON.stringify(x.parsed)).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"capture-manifest.json"),JSON.stringify({
  source_id:"reco_nz",
  captured_at:new Date().toISOString(),
  policy_sha256:sha256(JSON.stringify(policy)),
  page_start:pageStart,
  pages,
  delay_ms:delayMs,
  solve_count:manifest.length,
  records:manifest.map(({parsed,...x})=>x)
},null,2)+"\n");

console.log("G7_P2_RECO_BOUNDED_CAPTURE_PASS");
console.log("INDEX_PAGES\t"+pages);
console.log("SOLVES\t"+manifest.length);
console.log("RAW_HTML_PRESERVED\tYES");
console.log("ROBOTS_CHECK\tPASS");
