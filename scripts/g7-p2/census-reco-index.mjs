import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { parseRecoIndexHtml } from "./parse-reco-html.mjs";

const args=process.argv.slice(2);
const value=(name,def=null)=>{ const i=args.indexOf(name); return i>=0&&i+1<args.length?args[i+1]:def; };
const policyPath=value("--policy","g7/p2/reco-index-census-policy.json");
const outDir=value("--out","g7/p2/reco-index-census");
const policy=JSON.parse(fs.readFileSync(policyPath,"utf8"));
const maxPages=Number(value("--max-pages",String(policy.max_index_pages)));
const delayMs=Number(value("--delay-ms",String(policy.min_delay_ms)));

if(policy.source_id!=="reco_nz") throw new Error("RECO_CENSUS_POLICY_SOURCE");
if(policy.mode!=="INDEX_CENSUS_ONLY") throw new Error("RECO_CENSUS_POLICY_MODE");
if(policy.solve_body_fetch_authorized!==false) throw new Error("RECO_CENSUS_SOLVE_BODY_MUST_BE_FALSE");
if(policy.index_census_authorized!==true) throw new Error("RECO_CENSUS_NOT_AUTHORIZED");
if(delayMs<policy.min_delay_ms) throw new Error("RECO_CENSUS_DELAY_TOO_LOW");
if(!Number.isInteger(maxPages)||maxPages<1||maxPages>policy.max_index_pages) throw new Error("RECO_CENSUS_PAGE_LIMIT");

const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const sha256=s=>crypto.createHash("sha256").update(s).digest("hex");
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
  const res=await fetch(url,{headers:{"User-Agent":policy.user_agent,"Accept":"text/html,application/xhtml+xml"}});
  if(!res.ok) throw new Error(`HTTP_${res.status}:${url}`);
  return await res.text();
}
function counts(rows,key){
  const m=new Map();
  for(const row of rows){
    const v=String(row[key]??"").trim()||"(blank)";
    m.set(v,(m.get(v)||0)+1);
  }
  return Object.fromEntries([...m.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])));
}
function duplicateGroups(rows,keyFn){
  const m=new Map();
  for(const r of rows){ const k=keyFn(r); if(!m.has(k)) m.set(k,[]); m.get(k).push(r); }
  return [...m.entries()].filter(([,v])=>v.length>1).map(([key,v])=>({key,count:v.length,ids:[...new Set(v.map(x=>x.id))],pages:[...new Set(v.map(x=>x.index_page))]}));
}

const robotsRes=await fetch("https://reco.nz/robots.txt",{headers:{"User-Agent":policy.user_agent}});
let robotsCheck;
if(robotsRes.status===200){
  const robotsText=await robotsRes.text();
  if(disallowedByRobots(robotsText,"/")) throw new Error("RECO_CENSUS_ROBOTS_DISALLOW_ROOT");
  robotsCheck="PRESENT_ALLOW";
}else if(robotsRes.status===404) robotsCheck="ABSENT_404";
else throw new Error("RECO_CENSUS_ROBOTS_UNREADABLE:"+robotsRes.status);

fs.mkdirSync(path.join(outDir,"raw","index"),{recursive:true});
fs.mkdirSync(path.join(outDir,"derived"),{recursive:true});

const rows=[];
const pageReceipts=[];
const seenFingerprints=new Set();
let terminalReason="MAX_PAGE_LIMIT";
for(let page=1;page<=maxPages;page++){
  if(page>1) await sleep(delayMs);
  const url=`https://reco.nz/?page=${page}`;
  const html=await get(url);
  const rawFile=path.join(outDir,"raw","index",`page-${String(page).padStart(4,"0")}.html`);
  fs.writeFileSync(rawFile,html);
  const parsed=parseRecoIndexHtml(html);
  const fingerprint=sha256(parsed.rows.map(r=>r.id).join(","));
  if(seenFingerprints.has(fingerprint)&&parsed.rows.length){
    throw new Error("RECO_CENSUS_REPEATED_PAGE_FINGERPRINT:"+page);
  }
  seenFingerprints.add(fingerprint);
  pageReceipts.push({page,url,row_count:parsed.rows.length,min_id:parsed.min_id,max_id:parsed.max_id,sha256:sha256(html)});
  for(const r of parsed.rows) rows.push({...r,index_page:page});

  if(parsed.rows.length===0){ terminalReason="EMPTY_PAGE"; break; }
  if(parsed.rows.length<50){ terminalReason="SHORT_PAGE"; break; }
}
if(!rows.length) throw new Error("RECO_CENSUS_NO_ROWS");

const ids=rows.map(r=>r.id).filter(Number.isInteger);
const uniqueIds=[...new Set(ids)].sort((a,b)=>a-b);
const minId=uniqueIds[0], maxId=uniqueIds.at(-1);
const idSet=new Set(uniqueIds);
const missingIds=[];
for(let id=minId;id<=maxId;id++) if(!idSet.has(id)) missingIds.push(id);
const dates=rows.map(r=>r.date).filter(x=>/^\d{4}-\d{2}-\d{2}$/.test(x)).sort();

const duplicateIdGroups=duplicateGroups(rows,r=>String(r.id));
const duplicateContentGroups=duplicateGroups(rows,r=>[
  r.puzzle,r.result,r.solver,r.method,r.date,r.competition,r.tags,r.movecount,r.tps,r.reconstructor
].join("\u241f")).filter(g=>g.ids.length>1);

const census={
  schema_version:"g7-p2-reco-index-census-1",
  source_id:"reco_nz",
  generated_at:new Date().toISOString(),
  scope:"INDEX_ONLY_NO_SOLVE_BODY_FETCH",
  robots_check:robotsCheck,
  terminal_reason:terminalReason,
  pages_fetched:pageReceipts.length,
  row_count:rows.length,
  unique_id_count:uniqueIds.length,
  id_range:{min:minId,max:maxId,missing_count:missingIds.length,missing_ids:missingIds},
  date_range:{min:dates[0]??null,max:dates.at(-1)??null},
  puzzle_counts:counts(rows,"puzzle"),
  method_counts:counts(rows,"method"),
  solver_counts:counts(rows,"solver"),
  reconstructor_counts:counts(rows,"reconstructor"),
  duplicate_id_groups:duplicateIdGroups,
  duplicate_content_candidates:duplicateContentGroups,
  page_receipts:pageReceipts
};
fs.writeFileSync(path.join(outDir,"derived","index-rows.jsonl"),rows.map(r=>JSON.stringify(r)).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"derived","census.json"),JSON.stringify(census,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"derived","receipt.md"),[
  "# G7-P2 reco.nz index census receipt",
  "",
  "- scope: INDEX_ONLY_NO_SOLVE_BODY_FETCH",
  `- pages fetched: ${census.pages_fetched}`,
  `- rows: ${census.row_count}`,
  `- unique IDs: ${census.unique_id_count}`,
  `- ID range: ${minId}.. ${maxId}`,
  `- missing IDs in range: ${missingIds.length}`,
  `- date range: ${census.date_range.min} .. ${census.date_range.max}`,
  `- duplicate ID groups: ${duplicateIdGroups.length}`,
  `- duplicate content candidates: ${duplicateContentGroups.length}`,
  `- terminal reason: ${terminalReason}`,
  `- robots: ${robotsCheck}`,
  "",
  "Full solve-body mirroring remains HOLD."
].join("\n")+"\n");

console.log("G7_P2_RECO_INDEX_CENSUS_PASS");
console.log("PAGES\t"+census.pages_fetched);
console.log("ROWS\t"+census.row_count);
console.log("UNIQUE_IDS\t"+census.unique_id_count);
console.log("ID_RANGE\t"+minId+".."+maxId);
console.log("MISSING_IDS\t"+missingIds.length);
console.log("DATE_RANGE\t"+census.date_range.min+".."+census.date_range.max);
console.log("DUPLICATE_ID_GROUPS\t"+duplicateIdGroups.length);
console.log("DUPLICATE_CONTENT_CANDIDATES\t"+duplicateContentGroups.length);
console.log("TERMINAL_REASON\t"+terminalReason);
console.log("SOLVE_BODY_REQUESTS\t0");
