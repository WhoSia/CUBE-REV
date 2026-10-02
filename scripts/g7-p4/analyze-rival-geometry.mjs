import fs from "node:fs";
import path from "node:path";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const exactPath=val("--exact"), featurePath=val("--features"), outDir=val("--out","g7/p4/build");
if(!exactPath||!featurePath) throw new Error("ARGS_REQUIRED");
const exact=JSON.parse(fs.readFileSync(exactPath,"utf8"));
const lines=fs.readFileSync(featurePath,"utf8").trim().split(/\r?\n/);
const hdr=lines.shift().split("\t");
const rows=lines.filter(Boolean).map(line=>{
  const vals=line.split("\t"), x={};
  hdr.forEach((h,i)=>x[h]=vals[i]);
  for(const k of ["prefix_index","q_rank","lb","ts_lb","fs_lb","is_g1","boundary_after","obs_next_action","h1_regret","h2_regret","h3_regret","horizon_optimal_count","h1_opt_count","h2_opt_count","h3_opt_count"]) x[k]=Number(x[k]);
  x.source_id=Number(x.source_id);
  return x;
});
const meta=new Map(exact.records.map(r=>[r.source_id,r]));
const mean=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
const rate=(a,p)=>a.length?a.filter(p).length/a.length:null;

const moveKindCounts={};
const chunkLengths=[];
const rawAnnotations=[];
for(const r of exact.records){
  let chunk=0;
  for(const p of r.prefixes){
    moveKindCounts[p.kind]=(moveKindCounts[p.kind]||0)+1;
    chunk++;
    if(p.boundary_after){
      chunkLengths.push(chunk); chunk=0;
      if(p.annotation_after) rawAnnotations.push(p.annotation_after);
    }
  }
  if(chunk>0) chunkLengths.push(chunk);
}
const observed=rows.filter(x=>x.obs_next_action>=0);
const boundary=rows.filter(x=>x.boundary_after===1);
const nonBoundary=rows.filter(x=>x.boundary_after===0);

function groupSummary(groupRows){
  const obs=groupRows.filter(x=>x.obs_next_action>=0);
  return {
    states:groupRows.length,
    observed_face_next:obs.length,
    mean_phase1_lb:mean(groupRows.map(x=>x.lb)),
    g1_rate:rate(groupRows,x=>x.is_g1===1),
    h1_zero_regret_rate:rate(obs,x=>x.h1_regret===0),
    h2_zero_regret_rate:rate(obs,x=>x.h2_regret===0),
    h3_zero_regret_rate:rate(obs,x=>x.h3_regret===0),
    mean_h1_regret:mean(obs.map(x=>x.h1_regret)),
    mean_h2_regret:mean(obs.map(x=>x.h2_regret)),
    mean_h3_regret:mean(obs.map(x=>x.h3_regret)),
    horizon_1_2_3_optimal_stability_rate:rate(obs,x=>x.horizon_optimal_count===3)
  };
}
const byMethod={};
for(const m of new Set(exact.records.map(r=>r.method_family))){
  const ids=new Set(exact.records.filter(r=>r.method_family===m).map(r=>r.source_id));
  byMethod[m]=groupSummary(rows.filter(x=>ids.has(x.source_id)));
  byMethod[m].solves=ids.size;
}
const byReconstructor={};
for(const rec of exact.records){
  const rr=rows.filter(x=>x.source_id===rec.source_id);
  byReconstructor[rec.reconstructor]={
    source_id:rec.source_id,method_family:rec.method_family,...groupSummary(rr)
  };
}
const annotationLex={};
for(const a of rawAnnotations){
  const k=a.toLowerCase().replace(/\([^)]*\)/g,"").replace(/\s+/g," ").trim();
  annotationLex[k]=(annotationLex[k]||0)+1;
}
const report={
  schema_version:"g7-p4-policy-geometry-1",
  exact_replay:{
    solves:exact.solve_count,
    end_validation_pass:exact.exact_end_validation_pass,
    total_prefixes:exact.total_prefixes,
    authority:exact.authority
  },
  observational_geometry:{
    move_kind_counts:moveKindCounts,
    source_annotation_boundaries:rawAnnotations.length,
    chunk_count:chunkLengths.length,
    mean_chunk_moves:mean(chunkLengths),
    median_chunk_moves:[...chunkLengths].sort((a,b)=>a-b)[Math.floor(chunkLengths.length/2)]??null,
    min_chunk_moves:Math.min(...chunkLengths),
    max_chunk_moves:Math.max(...chunkLengths),
    normalized_annotation_lexemes:annotationLex
  },
  search_representation_geometry:{
    all_states:groupSummary(rows),
    source_boundary_states:groupSummary(boundary),
    non_boundary_states:groupSummary(nonBoundary),
    observed_face_next_states:observed.length,
    by_method_family:byMethod,
    by_reconstructor:byReconstructor,
    authority_note:"phase-1 PDB rival geometry is representation-specific and is not a direct measure of internal planning"
  },
  measurement_boundary:{
    reconstructor_conditioning_required:true,
    same_reconstructor_multi_method_support:"INSUFFICIENT_IN_PILOT",
    pooled_mechanism_claim:"NOT_AUTHORIZED",
    source_comments_are_internal_states:false
  }
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"policy-geometry.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"policy-geometry-receipt.md"),[
  "# G7-P4 policy geometry receipt","",
  `- exact replay: ${report.exact_replay.end_validation_pass}/${report.exact_replay.solves}`,
  `- total prefixes: ${report.exact_replay.total_prefixes}`,
  `- source annotation boundaries: ${report.observational_geometry.source_annotation_boundaries}`,
  `- chunks: ${report.observational_geometry.chunk_count}`,
  `- mean chunk moves: ${report.observational_geometry.mean_chunk_moves.toFixed(3)}`,
  `- observed face-next states: ${report.search_representation_geometry.observed_face_next_states}`,
  `- horizon-3 zero-regret rate: ${(report.search_representation_geometry.all_states.h3_zero_regret_rate??0).toFixed(6)}`,
  `- 1/2/3 optimal-stability rate: ${(report.search_representation_geometry.all_states.horizon_1_2_3_optimal_stability_rate??0).toFixed(6)}`,
  "- pooled mechanism claim: NOT_AUTHORIZED"
].join("\n")+"\n");
console.log("G7_P4_POLICY_GEOMETRY_PASS");
console.log("EXACT_REPLAY\t"+exact.exact_end_validation_pass+"/"+exact.solve_count);
console.log("PREFIXES\t"+exact.total_prefixes);
console.log("ANNOTATION_BOUNDARIES\t"+rawAnnotations.length);
console.log("CHUNKS\t"+chunkLengths.length);
console.log("OBSERVED_FACE_NEXT\t"+observed.length);
console.log("H1_ZERO_REGRET_RATE\t"+report.search_representation_geometry.all_states.h1_zero_regret_rate);
console.log("H2_ZERO_REGRET_RATE\t"+report.search_representation_geometry.all_states.h2_zero_regret_rate);
console.log("H3_ZERO_REGRET_RATE\t"+report.search_representation_geometry.all_states.h3_zero_regret_rate);
