import fs from 'node:fs';
import crypto from 'node:crypto';
import { buildR19Core, parseAnnotated, sha } from '../0.10.5-r1.9/r19_quotient_core.mjs';

const OUT=process.env.R111_ROOT||'/tmp/r111';fs.mkdirSync(OUT,{recursive:true});
const core=await buildR19Core();
const {defaultPattern,EDGE,CORNER,ORIENT,faces,faceSupport,opposite}=core;
const attemptKey=r=>`${r.result_id}:${r.attempt_number}`;
const foldOf=k=>parseInt(crypto.createHash('sha256').update(k).digest('hex').slice(0,8),16)%5;
const intersect=(a,b)=>{const s=new Set(b);return a.filter(x=>s.has(x));};
function blockMask(bottom,side){
  const top=opposite[bottom];
  return {bottom,side,top,edges:faceSupport[side].edges.filter(i=>!faceSupport[top].edges.includes(i)),corners:intersect(faceSupport[bottom].corners,faceSupport[side].corners)};
}
const frames=[];
for(const bottom of faces)for(const side of faces){
  if(side===bottom||side===opposite[bottom])continue;
  const first=blockMask(bottom,side),second=blockMask(bottom,opposite[side]);
  frames.push({key:`${bottom}|${side}`,bottom,first_side:side,second_side:opposite[side],top:opposite[bottom],first,second,axis_key:`${bottom}|${[side,opposite[side]].sort().join('-')}`});
}
const allCorners=defaultPattern.patternData[CORNER].pieces.map((_,i)=>i);
const allEdges=defaultPattern.patternData[EDGE].pieces.map((_,i)=>i);
function lseEdges(frame){const b=new Set([...frame.first.edges,...frame.second.edges]);return allEdges.filter(i=>!b.has(i));}
function coordMatch(p,t,orbit,i){const a=p.patternData[orbit],b=t.patternData[orbit];return a.pieces[i]===b.pieces[i]&&a.orientation[i]===b.orientation[i];}
function solvedCoord(p,orbit,i){return coordMatch(p,defaultPattern,orbit,i);}
function blockSolved(p,m){return m.edges.every(i=>solvedCoord(p,EDGE,i))&&m.corners.every(i=>solvedCoord(p,CORNER,i));}
function bothBlocks(p,f){return blockSolved(p,f.first)&&blockSolved(p,f.second);}
function transformState(raw,idx){return raw.applyTransformation(ORIENT[idx]);}
function admissibleFrameGroups(fbEndpoint){
  const g=new Map();
  for(let i=0;i<ORIENT.length;i++){
    const q=transformState(fbEndpoint,i);
    for(const f of frames)if(blockSolved(q,f.first)){
      if(!g.has(f.key))g.set(f.key,{frame:f,orientation_indices:[]});
      g.get(f.key).orientation_indices.push(i);
    }
  }
  for(const v of g.values())v.orientation_indices=[...new Set(v.orientation_indices)].sort((a,b)=>a-b);
  return [...g.values()].sort((a,b)=>a.frame.key.localeCompare(b.frame.key));
}
function maskDistance(p,target,masks){let bad=0,total=0;for(const m of masks)for(const i of m.positions){total+=2;const a=p.patternData[m.orbit],b=target.patternData[m.orbit];if(a.pieces[i]!==b.pieces[i])bad++;if(a.orientation[i]!==b.orientation[i])bad++;}return total?bad/total:null;}
function minVariantDistance(p,targets,masks){return Math.min(...targets.map(t=>maskDistance(p,t,masks)));}
function aufVariants(p,face){const out=[p];let q=p;for(let i=1;i<4;i++){q=q.applyMove(face);out.push(q);}return out;}
function cornersSolvedAUF(p,face){let q=p;for(let i=0;i<4;i++){if(allCorners.every(j=>solvedCoord(q,CORNER,j)))return true;q=q.applyMove(face);}return false;}
function objectiveBacktrack(ds){let best=Infinity,amp=0;for(const d of ds){best=Math.min(best,d);amp=Math.max(amp,d-best);}return amp;}
function anchorDamage(p,masks){let bad=0,total=0;for(const m of masks)for(const i of m.positions){total+=2;const a=p.patternData[m.orbit],b=defaultPattern.patternData[m.orbit];if(a.pieces[i]!==b.pieces[i])bad++;if(a.orientation[i]!==b.orientation[i])bad++;}return total?bad/total:null;}
function anchorBreak(vals){if(!vals.length)return null;const a0=vals[0];return Math.max(...vals.map(x=>Math.max(0,x-a0)));}
function moveBin(n){return n<=5?'1-5':n<=8?'6-8':n<=12?'9-12':'13+';}
function loadRecords(){
  const a=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R17'}));
  const b=JSON.parse(fs.readFileSync('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R18'}));
  return [...a,...b].filter(r=>r.method==='Roux'&&r.route_source_status==='RAW_ALG_CUBING_LINK');
}
function evaluateRepresentative(states,lines,frame,orientationIndex){
  const qs=states.map(x=>transformState(x,orientationIndex));
  const {fb,sb,cmll,lse}=lines;
  const status={
    fb_acquisition:!blockSolved(qs[fb.start],frame.first)&&blockSolved(qs[fb.end],frame.first),
    sb_pass:sb?blockSolved(qs[sb.end],frame.first)&&blockSolved(qs[sb.end],frame.second)&&!bothBlocks(qs[sb.start],frame):null,
    cmll_pass:cmll?bothBlocks(qs[cmll.end],frame)&&cornersSolvedAUF(qs[cmll.end],frame.top):null,
    lse_pass:lse?bothBlocks(qs[lse.end],frame):null
  };
  const feats=[];
  function objective(phase,line,masks,targets){const ds=[];for(let i=line.start;i<=line.end;i++)ds.push(minVariantDistance(qs[i],targets,masks));feats.push({phase,channel:'objective',amplitude:objectiveBacktrack(ds),line});}
  function anchor(phase,line,masks){const v=[];for(let i=line.start;i<=line.end;i++)v.push(anchorDamage(qs[i],masks));feats.push({phase,channel:'anchor',amplitude:anchorBreak(v),line});}
  objective('FB',fb,[{orbit:EDGE,positions:frame.first.edges},{orbit:CORNER,positions:frame.first.corners}],[qs[fb.end]]);
  if(sb){objective('SB',sb,[{orbit:EDGE,positions:frame.second.edges},{orbit:CORNER,positions:frame.second.corners}],[qs[sb.end]]);anchor('SB',sb,[{orbit:EDGE,positions:frame.first.edges},{orbit:CORNER,positions:frame.first.corners}]);}
  if(cmll){objective('CMLL',cmll,[{orbit:CORNER,positions:allCorners}],aufVariants(qs[cmll.end],frame.top));anchor('CMLL',cmll,[{orbit:EDGE,positions:[...frame.first.edges,...frame.second.edges]},{orbit:CORNER,positions:[...frame.first.corners,...frame.second.corners]}]);}
  if(lse){objective('LSE',lse,[{orbit:EDGE,positions:lseEdges(frame)}],[qs[lse.end]]);anchor('LSE',lse,[{orbit:EDGE,positions:[...frame.first.edges,...frame.second.edges]},{orbit:CORNER,positions:[...frame.first.corners,...frame.second.corners]}]);}
  return {status,features:feats};
}
function repInvariant(evals){
  if(evals.length<=1)return true;
  const a=evals[0];
  for(let j=1;j<evals.length;j++){
    const b=evals[j];
    for(const k of ['fb_acquisition','sb_pass','cmll_pass','lse_pass'])if(a.status[k]!==b.status[k])return false;
    if(a.features.length!==b.features.length)return false;
    for(let i=0;i<a.features.length;i++)if(a.features[i].phase!==b.features[i].phase||a.features[i].channel!==b.features[i].channel||Math.abs(a.features[i].amplitude-b.features[i].amplitude)>1e-12)return false;
  }
  return true;
}
const records=loadRecords(),rows=[],features=[];
const C={manifest_roux:records.length,parse_ok:0,state_certified:0,fb_line:0,unique_frame_group:0,representative_invariance_pass:0,multi_representative_groups:0,fb_acquisition_pass:0,sb_line:0,sb_pass:0,cmll_line:0,cmll_pass:0,lse_line:0,lse_pass:0,errors:0};
const opportunities={total:0,failed:0,by_phase:{FB:0,SB:0,CMLL:0,LSE:0},missing_phase:{FB:0,SB:0,CMLL:0,LSE:0}};
for(const r of records){
  const rec={result_id:r.result_id,attempt_number:r.attempt_number,reco_id:r.reco_id,source:r.source,status:'START'};
  try{
    const parsed=parseAnnotated(r.raw_alg,'Roux'),moves=parsed.tokens.map(x=>x.move);C.parse_ok++;
    let s=defaultPattern.applyAlg(r.raw_setup),states=[s];for(const m of moves){s=s.applyMove(m);states.push(s);}rec.final_solved=s.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});if(!rec.final_solved){rec.status='FINAL_NOT_SOLVED';rows.push(rec);continue;}C.state_certified++;
    const lineOf=ph=>parsed.lines.find(x=>x.phase===ph&&x.end>x.start)||null;
    const fb=lineOf('ROUX_FB'),sb=lineOf('ROUX_SB'),cmll=lineOf('ROUX_CMLL'),lse=lineOf('ROUX_LSE');const lines={fb,sb,cmll,lse};rec.lines={FB:fb&&[fb.start,fb.end],SB:sb&&[sb.start,sb.end],CMLL:cmll&&[cmll.start,cmll.end],LSE:lse&&[lse.start,lse.end]};
    for(const [n,l] of [['FB',fb],['SB',sb],['CMLL',cmll],['LSE',lse]])if(!l)opportunities.missing_phase[n]++;
    if(!fb){rec.status='NO_FB_LINE';rows.push(rec);continue;}C.fb_line++;
    const groups=admissibleFrameGroups(states[fb.end]);rec.frame_group_n=groups.length;rec.frame_groups=groups.map(g=>({frame_key:g.frame.key,orientation_indices:g.orientation_indices}));
    if(groups.length!==1){rec.status='FRAME_GROUP_NOT_UNIQUE';rows.push(rec);continue;}C.unique_frame_group++;
    const group=groups[0],frame=group.frame;rec.frame_key=frame.key;rec.orientation_representatives=group.orientation_indices;if(group.orientation_indices.length>1)C.multi_representative_groups++;
    const evals=group.orientation_indices.map(i=>evaluateRepresentative(states,lines,frame,i));const invariant=repInvariant(evals);rec.representative_invariant=invariant;
    for(const [ph,l] of [['FB',fb],['SB',sb],['CMLL',cmll],['LSE',lse]])if(l){opportunities.total++;opportunities.by_phase[ph]++;if(!invariant)opportunities.failed++;}
    if(!invariant){rec.status='REPRESENTATIVE_NONINVARIANT';rows.push(rec);continue;}C.representative_invariance_pass++;
    const repIndex=group.orientation_indices[0],ev=evals[0];rec.frame_transform_index=repIndex;rec.fb_acquisition=ev.status.fb_acquisition;if(rec.fb_acquisition)C.fb_acquisition_pass++;
    if(sb){C.sb_line++;rec.sb_pass=ev.status.sb_pass;if(rec.sb_pass)C.sb_pass++;}
    if(cmll){C.cmll_line++;rec.cmll_pass=ev.status.cmll_pass;if(rec.cmll_pass)C.cmll_pass++;}
    if(lse){C.lse_line++;rec.lse_pass=ev.status.lse_pass&&rec.final_solved;if(rec.lse_pass)C.lse_pass++;}
    for(const z of ev.features){features.push({result_id:r.result_id,attempt_number:r.attempt_number,reco_id:r.reco_id,source:r.source,method:'Roux',phase:z.phase,channel:z.channel,move_count:z.line.end-z.line.start,move_bin:moveBin(z.line.end-z.line.start),observed_amplitude:z.amplitude,frame_key:frame.key,frame_transform_index:repIndex,quotient_representative_n:group.orientation_indices.length,fold:foldOf(attemptKey(r))});}
    rec.geometry_failures=0;rec.status='FRAME_EVALUATED';rows.push(rec);
  }catch(e){C.errors++;rec.status='ERROR';rec.error=String(e?.message||e).slice(0,300);rows.push(rec);}
}
const rate=(n,d)=>d?n/d:0;
const objectiveN=features.filter(x=>x.channel==='objective').length;
const eligibleAttempts=new Set(features.map(attemptKey)).size;
const geometryFailureRate=rate(opportunities.failed,opportunities.total);
const axes=new Set(frames.map(f=>f.axis_key));
const rates={unique_frame_group_rate:rate(C.unique_frame_group,C.fb_line),representative_invariance_rate:rate(C.representative_invariance_pass,C.unique_frame_group),fb_acquisition_rate:rate(C.fb_acquisition_pass,C.representative_invariance_pass),sb_frame_preservation_and_acquisition_rate:rate(C.sb_pass,C.sb_line),cmll_consistency_rate:rate(C.cmll_pass,C.cmll_line),lse_consistency_rate:rate(C.lse_pass,C.lse_line),geometry_failure_rate:geometryFailureRate};
const masksValid=frames.every(f=>f.first.edges.length===3&&f.first.corners.length===2&&f.second.edges.length===3&&f.second.corners.length===2&&f.first.edges.every(x=>!f.second.edges.includes(x))&&f.first.corners.every(x=>!f.second.corners.includes(x)));
const checks={
  ordered_frame_space_24:frames.length===24,
  unordered_axes_12:axes.size===12,
  every_frame_two_disjoint_3e2c_blocks:masksValid,
  orientation_group_24:ORIENT.length===24,
  state_certified_ge_80:C.state_certified>=80,
  fb_line_ge_80:C.fb_line>=80,
  unique_frame_group_rate_ge_0_95:rates.unique_frame_group_rate>=.95,
  representative_invariance_rate_ge_0_99:rates.representative_invariance_rate>=.99,
  fb_acquisition_rate_ge_0_95:rates.fb_acquisition_rate>=.95,
  sb_line_ge_75:C.sb_line>=75,
  sb_rate_ge_0_85:rates.sb_frame_preservation_and_acquisition_rate>=.85,
  cmll_line_ge_70:C.cmll_line>=70,
  cmll_rate_ge_0_80:rates.cmll_consistency_rate>=.80,
  lse_line_ge_70:C.lse_line>=70,
  lse_rate_ge_0_90:rates.lse_consistency_rate>=.90,
  eligible_attempts_ge_80:eligibleAttempts>=80,
  total_features_ge_300:features.length>=300,
  objective_features_ge_250:objectiveN>=250,
  geometry_failure_rate_le_0_10:geometryFailureRate<=.10
};
const status=Object.values(checks).every(Boolean)?'PASS_ROUX_BLOCK_INTERNAL_FRAME_GEOMETRY':'HOLD_ROUX_BLOCK_INTERNAL_FRAME_GEOMETRY';
const frameCounts={};for(const z of rows.filter(x=>x.frame_key))frameCounts[z.frame_key]=(frameCounts[z.frame_key]||0)+1;
const audit={schema_version:'CR0105R111-ROUX-BLOCK-INTERNAL-GEOMETRY-R3-1',status,frame_space:{ordered_frames:frames.length,axes:axes.size,rule:'Unique ordered frame group over frozen 24-orientation × 24-frame candidate space; representative-invariant within group.',frame_counts:frameCounts},counts:C,rates,feature_counts:{total:features.length,objective:objectiveN,anchor:features.length-objectiveN,eligible_attempts:eligibleAttempts,phase:Object.fromEntries(['FB','SB','CMLL','LSE'].map(p=>[p,features.filter(x=>x.phase===p).length]))},geometry_opportunities:opportunities,checks,preexecution_design_repair:'research/0.10.5-r1.11/NAPKIN_PREEXEC_DESIGN_REPAIR_R3.json',historical_role:'DEVELOPMENT_AND_CALIBRATION_ONLY',fresh_outcomes_seen:false,human_observations:0};
audit.semantic_sha256=sha(audit);
fs.writeFileSync(`${OUT}/ROUX_BLOCK_INTERNAL_GEOMETRY_AUDIT.json`,JSON.stringify(audit,null,2)+'\n');
fs.writeFileSync(`${OUT}/ROUX_FRAME_ROUTE_ROWS.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-FRAME-ROUTE-ROWS-R3-1',rows,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${OUT}/ROUX_FEATURE_LEDGER.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-FEATURE-LEDGER-R3-1',rows:features,historical_role:'DEVELOPMENT_AND_CALIBRATION_ONLY',human_observations:0},null,2)+'\n');
console.log(JSON.stringify(audit,null,2));
