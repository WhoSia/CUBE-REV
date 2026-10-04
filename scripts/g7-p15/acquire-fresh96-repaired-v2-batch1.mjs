import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import {parseRecoSolveHtml} from "../reco/parse-reco-html.mjs";
const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const execute=args.includes("--execute"), manifestPath=val("--manifest"), outDir=val("--out");
if(!manifestPath||!outDir) throw new Error("ARGS");
const manifest=JSON.parse(fs.readFileSync(manifestPath,"utf8"));
const policy=JSON.parse(fs.readFileSync("core/reco/reco-acquisition-policy.json","utf8"));
if(manifest.phase!=="G7-P15"||manifest.status!=="SEALED_AFTER_SECOND_PRE_GEOMETRY_REPLAY_INVALID_REPLACEMENT") throw new Error("P15_V2_MANIFEST_NOT_SEALED");
if(manifest.selection_manifest_sha256!=="7e7d99682436c7b75bb6a7d2cd28eac54bbb87d3d3cef163e7ceacb7c16c3bb6") throw new Error("P15_V2_MANIFEST_SHA");
const ids=manifest.batches?.["1"];
if(!Array.isArray(ids)||ids.length!==8) throw new Error("BATCH1_8_REQUIRED");
const rowsById=new Map(manifest.rows.map(x=>[Number(x.source_id),x]));
const delayMs=Math.max(2000,Number(policy.min_delay_ms));
if(!execute){console.log("G7_P15_V2_BATCH1_DRY_RUN");console.log(ids.join(","));process.exit(0);}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const sha256=s=>crypto.createHash("sha256").update(s).digest("hex");
const robots=await fetch("https://reco.nz/robots.txt",{headers:{"User-Agent":policy.user_agent}});
if(![200,404].includes(robots.status)) throw new Error("ROBOTS_UNREADABLE:"+robots.status);
let robotsCheck=robots.status===404?"ABSENT_404":"PRESENT";
fs.mkdirSync(path.join(outDir,"raw","solve"),{recursive:true});
fs.mkdirSync(path.join(outDir,"derived"),{recursive:true});
const records=[];
for(let i=0;i<ids.length;i++){
 if(i) await sleep(delayMs);
 const id=Number(ids[i]),url=`https://reco.nz/solve/${id}`;
 const res=await fetch(url,{headers:{"User-Agent":policy.user_agent,"Accept":"text/html,application/xhtml+xml"}});
 if(!res.ok) throw new Error(`HTTP_${res.status}:${id}`);
 const html=await res.text(),parsed=parseRecoSolveHtml(html,url);
 if(parsed.source_record_id!==String(id)) throw new Error("ID_MISMATCH:"+id);
 const rawFile=path.join(outDir,"raw","solve",id+".html");fs.writeFileSync(rawFile,html);
 records.push({source_id:id,source_url:url,sha256:sha256(html),raw_file:path.relative(outDir,rawFile),selection:rowsById.get(id),parsed});
}
fs.writeFileSync(path.join(outDir,"derived","solves.jsonl"),records.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(outDir,"capture-manifest.json"),JSON.stringify({
 schema_version:"g7-p15-fresh96-repaired-v2-batch1-capture-1",phase:"G7-P15",batch:1,
 selection_manifest_sha256:manifest.selection_manifest_sha256,solve_count:8,ids,delay_ms:delayMs,
 robots_check:robotsCheck,raw_public_release:"HOLD",bulk_mirror:"HOLD"
},null,2)+"\n");
console.log("G7_P15_V2_BATCH1_CAPTURE_PASS");console.log("IDS\t"+ids.join(","));
