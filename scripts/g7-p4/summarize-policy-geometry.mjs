import fs from "node:fs";
import path from "node:path";
const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const pdbPath=val("--pdb-tsv"), cubiePath=val("--cubie-json"), exactPath=val("--exact-json"), outDir=val("--out","g7/p4/build");
if(!pdbPath||!cubiePath||!exactPath) throw new Error("INPUT_REQUIRED");
const cubie=JSON.parse(fs.readFileSync(cubiePath,"utf8"));
const exact=JSON.parse(fs.readFileSync(exactPath,"utf8"));
const lines=fs.readFileSync(pdbPath,"utf8").trim().split(/\r?\n/).filter(Boolean);
const header=lines[0].split("\t");
const rows=lines.slice(1).map(line=>Object.fromEntries(header.map((h,i)=>[h,line.split("\t")[i]])));
const num=(x,k)=>Number(x[k]);
function stats(xs){
  if(!xs.length) return {n:0};
  const mean=k=>xs.reduce((s,x)=>s+num(x,k),0)/xs.length;
  return {
    n:xs.length,
    descent_rate:xs.filter(x=>num(x,"descent")===1).length/xs.length,
    best_rival_tie_rate:xs.filter(x=>num(x,"local_regret")===0).length/xs.length,
    mean_local_regret:mean("local_regret"),
    mean_h_before:mean("h_before"),
    mean_h_after:mean("h_after"),
    g1_before_rate:xs.filter(x=>num(x,"rank_before")===0).length/xs.length
  };
}
function grouped(key){
  const m=new Map();
  for(const r of rows){const v=r[key]||"(blank)";if(!m.has(v))m.set(v,[]);m.get(v).push(r);}
  return Object.fromEntries([...m].sort((a,b)=>b[1].length-a[1].length||a[0].localeCompare(b[0])).map(([k,v])=>[k,stats(v)]));
}
let annotationBearing=0,totalAnnotations=0;
const chunkLengths=[],boundaryFacelets=[],boundarySolvedFaces=[];
for(const rec of exact.records){
  const anns=rec.prefixes.filter(x=>x.event_kind==="ANNOTATION");
  if(anns.length) annotationBearing++;
  totalAnnotations+=anns.length;
  let prev=0;
  for(const a of anns){
    chunkLengths.push(a.move_index-prev); prev=a.move_index;
    if(Number.isFinite(a.center_relative_correct_facelets)) boundaryFacelets.push(a.center_relative_correct_facelets);
    if(Number.isFinite(a.solved_faces)) boundarySolvedFaces.push(a.solved_faces);
  }
  if(rec.move_count>prev) chunkLengths.push(rec.move_count-prev);
}
const mean=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:null;
const sorted=a=>[...a].sort((x,y)=>x-y);
const median=a=>{if(!a.length)return null;const s=sorted(a),i=Math.floor(s.length/2);return s.length%2?s[i]:(s[i-1]+s[i])/2;};
const report={
  schema_version:"g7-p4-policy-summary-1",
  solve_count:exact.solve_count,
  exact_replay:exact.replay_status_counts,
  supported_fraction:exact.supported_fraction,
  transition_counts:cubie.transition_counts,
  single_htm_fraction:cubie.single_htm_fraction,
  search_alignment:stats(rows),
  by_method:grouped("method_family"),
  by_reconstructor:grouped("reconstructor"),
  annotation_geometry:{
    annotation_bearing_solves:annotationBearing,
    total_annotations:totalAnnotations,
    chunk_count:chunkLengths.length,
    mean_chunk_moves:mean(chunkLengths),
    median_chunk_moves:median(chunkLengths),
    mean_boundary_correct_facelets:mean(boundaryFacelets),
    mean_boundary_solved_faces:mean(boundarySolvedFaces)
  },
  authority_note:"descriptive exact-state/search-representation geometry; no direct latent planning-state identification"
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"policy-summary.json"),JSON.stringify(report,null,2)+"\n");
console.log("G7_P4_POLICY_SUMMARY_PASS");
console.log("SOLVES\t"+report.solve_count);
console.log("SUPPORTED_FRACTION\t"+report.supported_fraction);
console.log("SEARCH_EVENTS\t"+report.search_alignment.n);
console.log("ANNOTATION_BEARING_SOLVES\t"+annotationBearing);
console.log("MEAN_LOCAL_REGRET\t"+report.search_alignment.mean_local_regret);
