import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const input=val("--input"), samplingPath=val("--sampling","core/reco/sampling-geometry.json"), ontologyPath=val("--ontology","core/reco/method-ontology.json"), constitutionPath=val("--constitution","g7/p7/reco-campaign-constitution.json"), outDir=val("--out");
if(!input||!outDir) throw new Error("ARGS");
const rows=fs.readFileSync(input,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const pre=JSON.parse(fs.readFileSync(samplingPath,"utf8"));
const ontology=JSON.parse(fs.readFileSync(ontologyPath,"utf8"));
const c=JSON.parse(fs.readFileSync(constitutionPath,"utf8"));
const excluded=new Set(c.campaign.exclude_previously_contacted_ids.map(Number));
const hash=(x)=>crypto.createHash("sha256").update(c.campaign.seed+"|"+x).digest("hex");
const count=(xs,key)=>{const m=new Map();for(const x of xs){const k=key(x);m.set(k,(m.get(k)||0)+1);}return m;};
const solverCounts=count(rows,r=>String(r.solver??"").trim());
const reconCounts=count(rows,r=>String(r.reconstructor??"").trim());
function band(n){for(const [id,[lo,hi]] of Object.entries(pre.frequency_bands))if(n>=lo&&(hi===null||n<=hi))return id;throw new Error("BAND");}
function era(date){const y=Number(String(date??"").slice(0,4));return pre.temporal_eras.find(e=>y>=e.start_year&&y<=e.end_year)?.id??"OUTSIDE";}
function family(method){return (ontology.raw_label_map[method]??ontology.fallback).family;}
const eligible=rows.filter(r=>r.puzzle==="3x3"&&!excluded.has(Number(r.id)));
const strata=new Map();
for(const r of eligible){
  const k=[family(r.method),era(r.date),band(solverCounts.get(String(r.solver??"").trim())),band(reconCounts.get(String(r.reconstructor??"").trim()))].join("␟");
  if(!strata.has(k))strata.set(k,[]);
  strata.get(k).push(r);
}
for(const [k,v] of strata)v.sort((a,b)=>hash(k+"|"+a.id).localeCompare(hash(k+"|"+b.id))||a.id-b.id);
const ordered=[...strata.entries()].sort((a,b)=>a[1].length-b[1].length||hash("stratum|"+a[0]).localeCompare(hash("stratum|"+b[0]))||a[0].localeCompare(b[0]));
const selected=[];
let depth=0;
while(selected.length<c.campaign.total_solve_bodies){
  let added=0;
  for(const [k,v] of ordered){
    if(selected.length>=c.campaign.total_solve_bodies)break;
    if(depth<v.length){
      const r=v[depth];
      selected.push({
        source_id:Number(r.id),index_page:r.index_page,solver:r.solver,reconstructor:r.reconstructor,date:r.date,method:r.method,
        method_family:family(r.method),temporal_era:era(r.date),
        solver_frequency_band:band(solverCounts.get(String(r.solver??"").trim())),
        reconstructor_frequency_band:band(reconCounts.get(String(r.reconstructor??"").trim())),
        stratum:k,residual_stratum_size:v.length,within_stratum_rank:depth+1
      });added++;
    }
  }
  if(!added)throw new Error("INSUFFICIENT");
  depth++;
}
if(new Set(selected.map(x=>x.source_id)).size!==selected.length)throw new Error("DUP_IDS");
if(selected.some(x=>excluded.has(x.source_id)))throw new Error("PRIOR_CONTACT");
const batches=Array.from({length:c.campaign.batches},()=>[]);
selected.forEach((x,i)=>batches[i%c.campaign.batches].push(x));
if(batches.some(x=>x.length!==c.campaign.solves_per_batch))throw new Error("BATCH_SIZE");
const manifest={schema_version:"g7-p7-reco-campaign-manifest-1",source:"reco_nz",selection_frozen_before_body_contact:true,index_rows_sha256:c.predecessor.index_rows_sha256,seed:c.campaign.seed,total:selected.length,records:selected,batches:batches.map((x,i)=>({batch:i+1,records:x}))};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"campaign-manifest.json"),JSON.stringify(manifest,null,2)+"\n");
batches.forEach((records,i)=>fs.writeFileSync(path.join(outDir,`batch-${String(i+1).padStart(2,"0")}.json`),JSON.stringify({schema_version:"g7-p7-reco-batch-1",batch:i+1,selection_frozen_before_body_contact:true,records},null,2)+"\n"));
const by=(k)=>Object.fromEntries([...count(selected,x=>x[k])].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0]))));
fs.writeFileSync(path.join(outDir,"selection-receipt.md"),[
"# G7-P7 reco.nz bounded body-campaign selection","",
`- eligible residual 3x3 index rows: ${eligible.length}`,
`- residual nonempty strata: ${strata.size}`,
`- selected solve bodies: ${selected.length}`,
`- batches: ${batches.length} × ${batches[0].length}`,
`- previously contacted IDs excluded: ${excluded.size}`,
`- method-family support: ${JSON.stringify(by("method_family"))}`,
`- temporal-era support: ${JSON.stringify(by("temporal_era"))}`,
`- solver-band support: ${JSON.stringify(by("solver_frequency_band"))}`,
`- reconstructor-band support: ${JSON.stringify(by("reconstructor_frequency_band"))}`,
"- body requests during selection: 0",
"- bulk mirror: HOLD"
].join("\n")+"\n");
console.log("G7_P7_RECO_CAMPAIGN_SELECTION_PASS");
console.log("SELECTED\t"+selected.length);
console.log("BATCHES\t"+batches.length);
console.log("BODY_REQUESTS\t0");
