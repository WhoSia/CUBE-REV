import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { parseRecoIndexHtml } from "../reco/parse-reco-html.mjs";

const args=process.argv.slice(2);
const value=(name,def=null)=>{ const i=args.indexOf(name); return i>=0&&i+1<args.length?args[i+1]:def; };
const frozenPath=value("--frozen-index");
const outDir=value("--out","g7/p8/index-covariate-census");
const maxPages=Number(value("--max-pages","400"));
const delayMs=Number(value("--delay-ms","2000"));
const userAgent=value("--user-agent","CUBE-REV-research/0.1 (+https://github.com/WhoSia/CUBE-REV)");
if(!frozenPath) throw new Error("FROZEN_INDEX_REQUIRED");
if(!Number.isInteger(maxPages)||maxPages<1||maxPages>400) throw new Error("MAX_PAGES_OUT_OF_POLICY");
if(!Number.isInteger(delayMs)||delayMs<2000) throw new Error("DELAY_BELOW_2000MS");

const frozenRows=fs.readFileSync(frozenPath,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
if(frozenRows.length!==12941) throw new Error("FROZEN_12941_REQUIRED");
const frozen=new Map(frozenRows.map(x=>[Number(x.source_id),{source_id:Number(x.source_id),puzzle:x.puzzle}]));
if(frozen.size!==12941) throw new Error("FROZEN_IDS_NOT_UNIQUE");
const frozen3=[...frozen.values()].filter(x=>x.puzzle==="3x3");
if(frozen3.length!==10591) throw new Error("FROZEN_3X3_10591_REQUIRED");

function sha256(s){ return crypto.createHash("sha256").update(s).digest("hex"); }
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function disallowedByRobots(text,targetPath){
  let active=false;
  for(const raw of text.split(/\r?\n/)){
    const line=raw.replace(/#.*/,"").trim();
    if(!line) continue;
    const [k,...rest]=line.split(":");
    const key=k.trim().toLowerCase(), val=rest.join(":").trim();
    if(key==="user-agent") active=(val==="*");
    else if(active&&key==="disallow"&&val&&targetPath.startsWith(val)) return true;
  }
  return false;
}
async function get(url){
  const res=await fetch(url,{headers:{"User-Agent":userAgent,"Accept":"text/html,application/xhtml+xml"}});
  if(!res.ok) throw new Error(`HTTP_${res.status}:${url}`);
  return await res.text();
}
function counter(vals){
  const m=new Map();
  for(const v0 of vals){const v=String(v0??"").trim()||"(blank)";m.set(v,(m.get(v)||0)+1);}
  return Object.fromEntries([...m.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])));
}

const robotsRes=await fetch("https://reco.nz/robots.txt",{headers:{"User-Agent":userAgent}});
let robotsCheck;
if(robotsRes.status===200){
  const txt=await robotsRes.text();
  if(disallowedByRobots(txt,"/")) throw new Error("ROBOTS_DISALLOW_ROOT");
  robotsCheck="PRESENT_ALLOW";
}else if(robotsRes.status===404) robotsCheck="ABSENT_404";
else throw new Error("ROBOTS_UNREADABLE_"+robotsRes.status);

const observed=new Map();
const seenLiveIds=new Set();
const pageReceipts=[];
const seenFingerprints=new Set();
let liveRows=0,terminalReason="MAX_PAGE_LIMIT";

for(let page=1;page<=maxPages;page++){
  if(page>1) await sleep(delayMs);
  const url=`https://reco.nz/?page=${page}`;
  const html=await get(url);
  const parsed=parseRecoIndexHtml(html);
  const fingerprint=sha256(parsed.rows.map(r=>r.id).join(","));
  if(parsed.rows.length && seenFingerprints.has(fingerprint)) throw new Error("REPEATED_PAGE_FINGERPRINT_"+page);
  seenFingerprints.add(fingerprint);
  liveRows+=parsed.rows.length;
  pageReceipts.push({page,row_count:parsed.rows.length,min_id:parsed.min_id,max_id:parsed.max_id,html_sha256:sha256(html)});
  for(const r of parsed.rows){
    const sid=Number(r.id);
    seenLiveIds.add(sid);
    if(frozen.has(sid)){
      if(observed.has(sid)) throw new Error("DUPLICATE_FROZEN_ID_LIVE_"+sid);
      observed.set(sid,{
        source_id:sid,
        frozen_puzzle:frozen.get(sid).puzzle,
        live_present:true,
        live_index_page:page,
        method_raw:r.method??null,
        reconstructor:r.reconstructor??null
      });
    }
  }
  if(parsed.rows.length===0){terminalReason="EMPTY_PAGE";break;}
  if(parsed.rows.length<50){terminalReason="SHORT_PAGE";break;}
}
if(!liveRows) throw new Error("NO_LIVE_INDEX_ROWS");

const rows=[...frozen.values()].sort((a,b)=>a.source_id-b.source_id).map(f=>{
  const x=observed.get(f.source_id);
  return x??{source_id:f.source_id,frozen_puzzle:f.puzzle,live_present:false,live_index_page:null,method_raw:null,reconstructor:null};
});
const three=rows.filter(x=>x.frozen_puzzle==="3x3");
const nonempty=x=>x!==null&&x!==undefined&&String(x).trim()!=="";
const matched=rows.filter(x=>x.live_present);
const matched3=three.filter(x=>x.live_present);
const method3=three.filter(x=>x.live_present&&nonempty(x.method_raw));
const recon3=three.filter(x=>x.live_present&&nonempty(x.reconstructor));
const newLive=[...seenLiveIds].filter(id=>!frozen.has(id));

const report={
  schema_version:"g7-p8-frozen-index-covariate-census-1",
  operation_type:"Frozen-Population Index-Only Method×Reconstructor Covariate Census",
  source_contact:"INDEX_ONLY",
  solve_body_requests:0,
  raw_html_retained:false,
  frozen_population_rows:12941,
  frozen_3x3_rows:10591,
  robots_check:robotsCheck,
  pages_fetched:pageReceipts.length,
  terminal_reason:terminalReason,
  live_rows_seen:liveRows,
  frozen_ids_matched:matched.length,
  frozen_ids_missing:12941-matched.length,
  frozen_3x3_ids_matched:matched3.length,
  frozen_3x3_ids_missing:10591-matched3.length,
  method_3x3_nonempty:method3.length,
  method_3x3_coverage_of_frozen:method3.length/10591,
  method_3x3_coverage_of_live_matched:matched3.length?method3.length/matched3.length:null,
  reconstructor_3x3_nonempty:recon3.length,
  reconstructor_3x3_coverage_of_frozen:recon3.length/10591,
  reconstructor_3x3_coverage_of_live_matched:matched3.length?recon3.length/matched3.length:null,
  method_counts_3x3:counter(method3.map(x=>x.method_raw)),
  reconstructor_counts_3x3:counter(recon3.map(x=>x.reconstructor)),
  new_live_id_count:newLive.length,
  page_receipts:pageReceipts,
  boundary:[
    "The frozen G7-P3 source_id universe defines the population; newly observed live IDs are excluded from analysis.",
    "Missing frozen IDs remain explicit live-availability failures and are not replaced.",
    "Only index pages are requested; /solve/{id} is never requested.",
    "Raw index HTML is hashed transiently for receipts and never retained.",
    "Method and reconstructor values are index-surface metadata and are not assumed to be independently validated ground truth."
  ]
};

fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"frozen-index-covariates.jsonl"),rows.map(x=>JSON.stringify(x)).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"census.json"),JSON.stringify(report,null,2)+"\n");
console.log("G7_P8_FROZEN_INDEX_COVARIATE_CENSUS_PASS");
console.log("PAGES\t"+report.pages_fetched);
console.log("LIVE_ROWS\t"+report.live_rows_seen);
console.log("FROZEN_MATCHED\t"+report.frozen_ids_matched);
console.log("FROZEN_MISSING\t"+report.frozen_ids_missing);
console.log("FROZEN_3X3_MATCHED\t"+report.frozen_3x3_ids_matched);
console.log("METHOD_3X3_NONEMPTY\t"+report.method_3x3_nonempty);
console.log("METHOD_3X3_COVERAGE\t"+report.method_3x3_coverage_of_frozen);
console.log("RECONSTRUCTOR_3X3_NONEMPTY\t"+report.reconstructor_3x3_nonempty);
console.log("RECONSTRUCTOR_3X3_COVERAGE\t"+report.reconstructor_3x3_coverage_of_frozen);
console.log("NEW_LIVE_IDS\t"+report.new_live_id_count);
console.log("SOLVE_BODY_REQUESTS\t0");
