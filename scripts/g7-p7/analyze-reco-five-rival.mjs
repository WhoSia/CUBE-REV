import fs from "node:fs";
import path from "node:path";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const ctxPath=val("--context"), featPath=val("--features"), outDir=val("--out");
if(!ctxPath||!featPath||!outDir) throw new Error("ARGS_REQUIRED");
const ctx=fs.readFileSync(ctxPath,"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const context=new Map(ctx.map(x=>[x.source_id+"|"+x.prefix_index,x]));
const lines=fs.readFileSync(featPath,"utf8").trim().split(/\r?\n/);
const head=lines.shift().split("\t");
const numeric=new Set(["prefix_index","phase1_lb","ts_lb","fs_lb","is_g1","boundary_after","next_action","rival_unique_sets","mean_pairwise_jaccard_distance","observed_match_h1","observed_match_h2","observed_match_h3","observed_match_ts","observed_match_fs"]);
const rows=lines.filter(Boolean).map(line=>{
  const v=line.split("\t"), f={}; head.forEach((h,i)=>f[h]=numeric.has(h)?Number(v[i]):v[i]);
  const c=context.get(Number(f.source_id)+"|"+f.prefix_index); if(!c) throw new Error("CTX:"+f.source_id+":"+f.prefix_index);
  return {...f,...c,source_id:Number(f.source_id)};
});
if(rows.length!==ctx.length) throw new Error("ROW_MISMATCH");

const rivals=[
 ["H1","h1_best","observed_match_h1"],
 ["H2","h2_best","observed_match_h2"],
 ["H3","h3_best","observed_match_h3"],
 ["TS","ts_best","observed_match_ts"],
 ["FS","fs_best","observed_match_fs"]
];
const mean=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
const median=a=>{if(!a.length)return null;const x=[...a].sort((a,b)=>a-b);const m=Math.floor(x.length/2);return x.length%2?x[m]:(x[m-1]+x[m])/2;};
const rate=(a,p)=>a.length?a.filter(p).length/a.length:null;
const norm=s=>String(s??"").toLowerCase().replace(/\s+/g," ").trim();
function stageFamily(method,raw){
  const s=norm(raw),m=String(method??"UNKNOWN");
  if(!s) return null;
  if(s.includes("inspection")) return "INSPECTION";
  if(m==="ROUX"){
    if(/^(fb|first block)$/.test(s)) return "ROUX_FIRST_BLOCK";
    if(/^(ss|sb|second block)$/.test(s)) return "ROUX_SECOND_BLOCK";
    if(s.includes("cmll")) return "ROUX_CMLL";
    if(/lse|eolr|eolrb|\bep\b/.test(s)) return "ROUX_LSE";
  }
  if(m==="PETRUS"){
    if(/2x2x2|2x2x3/.test(s)) return "PETRUS_BLOCK";
    if(/^eo$/.test(s)) return "EDGE_ORIENTATION";
  }
  if(m==="ZZ" && /eoline/.test(s)) return "ZZ_EOLINE";
  if(/cross/.test(s)) return "CROSS_OR_XCROSS";
  if(/pair|f2l|cls|vls|zbls/.test(s)) return "PAIR_OR_F2L";
  if(/oll|coll|cll|ollcp/.test(s)) return "LL_ORIENTATION";
  if(/pll|epll|zbll|2gll|1lll|last layer|^ll$/.test(s)) return "LAST_LAYER";
  if(/^eo$/.test(s)) return "EDGE_ORIENTATION";
  return "METHOD_SPECIFIC_OTHER";
}
for(const r of rows) r.stage_family=stageFamily(r.method_family,r.annotation_after);

function summarize(xs){
  const face=xs.filter(x=>x.next_action>=0);
  const out={
    states:xs.length,
    solves:new Set(xs.map(x=>x.source_id)).size,
    face_next_states:face.length,
    boundary_rate:rate(xs,x=>x.boundary_after===1),
    mean_phase1_lb:mean(xs.map(x=>x.phase1_lb)),
    g1_rate:rate(xs,x=>x.is_g1===1),
    mean_rival_unique_sets:mean(xs.map(x=>x.rival_unique_sets)),
    mean_pairwise_jaccard_distance:mean(xs.map(x=>x.mean_pairwise_jaccard_distance)),
    unique_set_distribution:Object.fromEntries([...new Set(xs.map(x=>x.rival_unique_sets))].sort((a,b)=>a-b).map(k=>[k,xs.filter(x=>x.rival_unique_sets===k).length])),
    observed_match_rates:{}
  };
  for(const [name,,col] of rivals) out.observed_match_rates[name]=rate(face,x=>x[col]===1);
  return out;
}
function grouped(field){
  const out={};
  for(const k of [...new Set(rows.map(x=>x[field]??"NULL"))].sort()){
    const xs=rows.filter(x=>(x[field]??"NULL")===k); out[k]=summarize(xs);
  }
  return out;
}
const pairwise={};
for(let i=0;i<rivals.length;i++) for(let j=i+1;j<rivals.length;j++){
  const [a,ca]=rivals[i],[b,cb]=rivals[j];
  pairwise[a+"__"+b]=rate(rows,x=>x[ca]!==x[cb]);
}
const boundary=rows.filter(x=>x.boundary_after===1), non=rows.filter(x=>x.boundary_after===0);
const solveIds=[...new Set(rows.map(x=>x.source_id))].sort((a,b)=>a-b);
const paired=[];
for(const id of solveIds){
  const s=rows.filter(x=>x.source_id===id),b=s.filter(x=>x.boundary_after===1),n=s.filter(x=>x.boundary_after===0);
  if(!b.length||!n.length) continue;
  const rec={
    source_id:id,
    method_family:s[0].method_family,reconstructor:s[0].reconstructor,
    boundary_minus_nonboundary_diversity:mean(b.map(x=>x.mean_pairwise_jaccard_distance))-mean(n.map(x=>x.mean_pairwise_jaccard_distance)),
    boundary_minus_nonboundary_unique_sets:mean(b.map(x=>x.rival_unique_sets))-mean(n.map(x=>x.rival_unique_sets))
  };
  for(const [name,,col] of rivals){
    const bf=b.filter(x=>x.next_action>=0), nf=n.filter(x=>x.next_action>=0);
    rec["boundary_minus_nonboundary_match_"+name]=(bf.length&&nf.length)?rate(bf,x=>x[col]===1)-rate(nf,x=>x[col]===1):null;
  }
  paired.push(rec);
}
const contrastVals=paired.map(x=>x.boundary_minus_nonboundary_diversity);
const rawAnn={};
for(const r of boundary){
  const k=norm(r.annotation_after)||"NULL";
  if(!rawAnn[k]) rawAnn[k]=[];
  rawAnn[k].push(r);
}
const annotationSummary={};
for(const [k,xs] of Object.entries(rawAnn).filter(([,xs])=>xs.length>=2).sort((a,b)=>b[1].length-a[1].length)) annotationSummary[k]=summarize(xs);

const winnerPatterns={};
for(const x of rows.filter(x=>x.next_action>=0)){
  const k=rivals.filter(([, ,col])=>x[col]===1).map(([name])=>name).join("+")||"NONE";
  winnerPatterns[k]=(winnerPatterns[k]||0)+1;
}
const report={
  schema_version:"g7-p7-reco-five-rival-analysis-1",
  authority:"DESCRIPTIVE_NATURALISTIC_MEASUREMENT",
  inference_boundary:[
    "reco.nz annotations are measurements supplied by reconstructors, not latent cognitive-state ground truth",
    "five-rival geometry is computational representation geometry, not direct evidence of internal representation",
    "rows are repeated within solves; no row-level independence claim is made",
    "reconstructor and method composition remain explicit conditioning variables"
  ],
  corpus:{
    solves:solveIds.length,states:rows.length,
    cohorts:Object.fromEntries([...new Set(rows.map(x=>x.cohort))].sort().map(k=>[k,new Set(rows.filter(x=>x.cohort===k).map(x=>x.source_id)).size])),
    method_solve_counts:Object.fromEntries([...new Set(rows.map(x=>x.method_family??"NULL"))].sort().map(k=>[k,new Set(rows.filter(x=>(x.method_family??"NULL")===k).map(x=>x.source_id)).size])),
    reconstructor_solve_counts:Object.fromEntries([...new Set(rows.map(x=>x.reconstructor??"NULL"))].sort().map(k=>[k,new Set(rows.filter(x=>(x.reconstructor??"NULL")===k).map(x=>x.source_id)).size]))
  },
  all_states:summarize(rows),
  boundary_states:summarize(boundary),
  nonboundary_states:summarize(non),
  rival_pair_disagreement_rates:pairwise,
  observed_match_pattern_counts:winnerPatterns,
  by_method:grouped("method_family"),
  by_cohort:grouped("cohort"),
  by_reconstructor:grouped("reconstructor"),
  by_stage_family:grouped("stage_family"),
  raw_annotation_summary_min_n2:annotationSummary,
  within_solve_boundary_contrast:{
    eligible_solves:paired.length,
    mean_boundary_minus_nonboundary_diversity:mean(contrastVals),
    median_boundary_minus_nonboundary_diversity:median(contrastVals),
    positive:contrastVals.filter(x=>x>0).length,
    zero:contrastVals.filter(x=>x===0).length,
    negative:contrastVals.filter(x=>x<0).length,
    solve_rows:paired
  },
  stage_family_authority:"DESCRIPTIVE_HELPER_ONLY"
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"five-rival-analysis.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"five-rival-analysis-receipt.md"),[
 "# G7-P7 reco.nz five-rival naturalistic analysis","",
 `- solves: ${report.corpus.solves}`,
 `- exact states: ${report.corpus.states}`,
 `- boundary states: ${report.boundary_states.states}`,
 `- face-next states: ${report.all_states.face_next_states}`,
 `- mean rival-set diversity: ${report.all_states.mean_pairwise_jaccard_distance}`,
 `- boundary minus non-boundary within-solve diversity: ${report.within_solve_boundary_contrast.mean_boundary_minus_nonboundary_diversity}`,
 ...Object.entries(report.all_states.observed_match_rates).map(([k,v])=>`- observed next-action match ${k}: ${v}`)
].join("\n")+"\n");
console.log("G7_P7_RECO_FIVE_RIVAL_ANALYSIS_PASS");
console.log("SOLVES\t"+report.corpus.solves);
console.log("STATES\t"+report.corpus.states);
console.log("BOUNDARIES\t"+report.boundary_states.states);
console.log("FACE_NEXT\t"+report.all_states.face_next_states);
console.log("MEAN_RIVAL_DIVERSITY\t"+report.all_states.mean_pairwise_jaccard_distance);
console.log("BOUNDARY_DELTA\t"+report.within_solve_boundary_contrast.mean_boundary_minus_nonboundary_diversity);
