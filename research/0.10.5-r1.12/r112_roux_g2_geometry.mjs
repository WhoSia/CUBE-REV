import fs from 'node:fs';
import crypto from 'node:crypto';
import { buildR19Core, parseAnnotated, sha } from '../0.10.5-r1.9/r19_quotient_core.mjs';

const ROOT=process.env.R112_ROOT||'/tmp/r112'; fs.mkdirSync(ROOT,{recursive:true});
const core=await buildR19Core();
const {defaultPattern,EDGE,CORNER,faces,faceSupport,opposite,canonicalizeByCenters}=core;
const attemptKey=r=>`${r.result_id}:${r.attempt_number}`;
const foldOf=k=>parseInt(crypto.createHash('sha256').update(k).digest('hex').slice(0,8),16)%5;
const intersect=(a,b)=>{const s=new Set(b);return a.filter(x=>s.has(x));};
const moveBin=n=>n<=4?'1-4':n<=8?'5-8':n<=12?'9-12':'13+';

function blockMask(bottom,side){
  const top=opposite[bottom];
  return {bottom,side,top,edges:faceSupport[side].edges.filter(i=>!faceSupport[top].edges.includes(i)),corners:intersect(faceSupport[bottom].corners,faceSupport[side].corners)};
}
const orderedFrames=[];
for(const bottom of faces)for(const side of faces){
  if(side===bottom||side===opposite[bottom])continue;
  const first=blockMask(bottom,side),second=blockMask(bottom,opposite[side]);
  orderedFrames.push({key:`${bottom}|${side}`,bottom,top:opposite[bottom],first_side:side,second_side:opposite[side],first,second,axis_key:`${bottom}|${[side,opposite[side]].sort().join('-')}`});
}
const axisMap=new Map();
for(const f of orderedFrames){
  if(!axisMap.has(f.axis_key))axisMap.set(f.axis_key,{key:f.axis_key,bottom:f.bottom,top:f.top,side_a:f.first_side,side_b:f.second_side,block_a:f.first,block_b:f.second});
}
const axes=[...axisMap.values()].sort((a,b)=>a.key.localeCompare(b.key));
const allCorners=defaultPattern.patternData[CORNER].pieces.map((_,i)=>i);
const allEdges=defaultPattern.patternData[EDGE].pieces.map((_,i)=>i);

function coordSolved(p,orbit,i){const a=p.patternData[orbit],b=defaultPattern.patternData[orbit];return a.pieces[i]===b.pieces[i]&&a.orientation[i]===b.orientation[i];}
function blockSolved(p,m){return m.edges.every(i=>coordSolved(p,EDGE,i))&&m.corners.every(i=>coordSolved(p,CORNER,i));}
function axisSolved(p,a){return blockSolved(p,a.block_a)&&blockSolved(p,a.block_b);}
function blockMasks(block){return [{orbit:EDGE,positions:block.edges},{orbit:CORNER,positions:block.corners}];}
function twoBlockMasks(frame){return [{orbit:EDGE,positions:[...frame.first.edges,...frame.second.edges]},{orbit:CORNER,positions:[...frame.first.corners,...frame.second.corners]}];}
function lseEdges(frame){const b=new Set([...frame.first.edges,...frame.second.edges]);return allEdges.filter(i=>!b.has(i));}
function maskDistance(p,target,masks){let bad=0,total=0;for(const m of masks)for(const i of m.positions){total+=2;const a=p.patternData[m.orbit],b=target.patternData[m.orbit];if(a.pieces[i]!==b.pieces[i])bad++;if(a.orientation[i]!==b.orientation[i])bad++;}return total?bad/total:null;}
function minTargetDistance(p,targets,masks){return Math.min(...targets.map(t=>maskDistance(p,t,masks)));}
function objectiveBacktrack(ds){let best=Infinity,amp=0;for(const d of ds){best=Math.min(best,d);amp=Math.max(amp,d-best);}return amp;}
function anchorDamage(p,masks){return maskDistance(p,defaultPattern,masks);}
function anchorBreak(states,masks){if(!states.length)return null;const vals=states.map(p=>anchorDamage(p,masks));const a0=vals[0];return Math.max(...vals.map(x=>Math.max(0,x-a0)));}
function aufVariants(p,face){const out=[p];let q=p;for(let i=1;i<4;i++){q=q.applyMove(face);out.push(q);}return out;}
function cornersSolvedAUF(p,face){let q=p;for(let i=0;i<4;i++){if(allCorners.every(j=>coordSolved(q,CORNER,j)))return true;q=q.applyMove(face);}return false;}

function ordinaryFbComment(c){const s=String(c||'');if(/\bpseudo\s+fb\b/i.test(s)||/\bfbdr\b/i.test(s))return false;return /\bfb\b/i.test(s);}
function firstContiguousSpan(lines,phase,afterIndex=-1){
  let first=-1;
  for(let i=0;i<lines.length;i++)if(lines[i].phase===phase&&lines[i].end>lines[i].start&&lines[i].start>=afterIndex){first=i;break;}
  if(first<0)return null;
  let last=first;
  for(let i=first+1;i<lines.length;i++){
    if(lines[i].phase!==phase||lines[i].end<=lines[i].start)break;
    last=i;
  }
  return {first_line_index:first,last_line_index:last,start:lines[first].start,end:lines[last].end,lines:lines.slice(first,last+1)};
}
function firstLineAfter(lines,phase,afterIndex){return lines.find(x=>x.phase===phase&&x.end>x.start&&x.start>=afterIndex)||null;}

function loadRecords(){
  const c=JSON.parse(fs.readFileSync('research/0.10.5-r1.12/evidence-census/SEALED_ROUTE_CENSUS.json','utf8'));
  const a=JSON.parse(fs.readFileSync('research/0.10.5-r1.12/evidence-acquisition/ROUX_EXPANSION_ROUTE_MANIFEST.json','utf8'));
  const rows=[];
  for(const r of c.all_clean_attempts)rows.push({...r,source:'SEALED_R111'});
  for(const r of a.records)if(r.route_source_status==='RAW_ALG_CUBING_LINK')rows.push({...r,source:'R112_EXPANSION'});
  const by=new Map();
  for(const r of rows){const k=attemptKey(r);if(!by.has(k))by.set(k,r);}
  return [...by.values()].sort((x,y)=>attemptKey(x).localeCompare(attemptKey(y)));
}

const records=loadRecords();
const rows=[],features=[];
const counts={
  raw_unique_attempts:records.length,parse_ok:0,state_certified:0,ordinary_fb:0,forked_pseudo_fb:0,forked_fbdr:0,fb_missing_or_nonordinary:0,
  sb_search_eligible:0,center_canonical_all_states:0,sb_any_completion:0,sb_first_completion_multi_axis:0,unique_axis_completion:0,
  fb_oriented_unique_axis:0,g2_admitted:0,cmll_opportunities:0,cmll_consistent:0,lse_opportunities:0,lse_consistent:0,errors:0
};
const rejection=Object.create(null);
const inc=k=>rejection[k]=(rejection[k]||0)+1;
const axisCounts=Object.create(null),frameCounts=Object.create(null),sbFamily=Object.create(null);

for(const r of records){
  const rec={result_id:r.result_id,attempt_number:r.attempt_number,reco_id:r.reco_id??null,source:r.source,attempt_key:attemptKey(r),status:'START'};
  try{
    const parsed=parseAnnotated(r.raw_alg,'Roux'); counts.parse_ok++;
    const moves=parsed.tokens.map(x=>x.move);
    let s=defaultPattern.applyAlg(r.raw_setup),states=[s];for(const m of moves){s=s.applyMove(m);states.push(s);}
    rec.final_solved=s.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});
    if(!rec.final_solved){rec.status='FINAL_NOT_SOLVED';inc(rec.status);rows.push(rec);continue;} counts.state_certified++;
    const fbLines=parsed.lines.filter(x=>x.phase==='ROUX_FB'&&x.end>x.start);
    rec.fb_line_count=fbLines.length;
    if(fbLines.length!==1){rec.status='FB_LINE_COUNT_NOT_ONE';counts.fb_missing_or_nonordinary++;inc(rec.status);rows.push(rec);continue;}
    const fb=fbLines[0]; rec.fb_comment=fb.comment;
    if(/\bpseudo\s+fb\b/i.test(fb.comment)){counts.forked_pseudo_fb++;rec.status='FORK_PSEUDO_FB';inc(rec.status);rows.push(rec);continue;}
    if(/\bfbdr\b/i.test(fb.comment)){counts.forked_fbdr++;rec.status='FORK_FBDR';inc(rec.status);rows.push(rec);continue;}
    if(!ordinaryFbComment(fb.comment)){counts.fb_missing_or_nonordinary++;rec.status='FB_NOT_ORDINARY_EXACT_LABEL';inc(rec.status);rows.push(rec);continue;}
    counts.ordinary_fb++;
    const sb=firstContiguousSpan(parsed.lines,'ROUX_SB',fb.end);
    if(!sb){rec.status='NO_SB_SPAN';inc(rec.status);rows.push(rec);continue;}
    counts.sb_search_eligible++; rec.sb_span={start:sb.start,end:sb.end,line_count:sb.lines.length,comments:sb.lines.map(x=>x.comment)};
    for(const line of sb.lines){const c=String(line.comment||'');let fam=/flipped\s+sp/i.test(c)?'FLIPPED_SP':/\bsp\b/i.test(c)?'SP':/\bss\b/i.test(c)?'SS':/\bsb\b/i.test(c)?'SB':'OTHER';sbFamily[fam]=(sbFamily[fam]||0)+1;}
    const canon=[];let canonFail=null;
    for(let i=0;i<states.length;i++){const z=canonicalizeByCenters(states[i]);if(!z.ok){canonFail={index:i,count:z.count};break;}canon.push(z.pattern);}
    if(canonFail){rec.status='CENTER_CANONICALIZATION_FAIL';rec.center_failure=canonFail;inc(rec.status);rows.push(rec);continue;}counts.center_canonical_all_states++;
    let firstCompletion=null;
    for(let i=sb.start;i<=sb.end;i++){
      const completed=axes.filter(a=>axisSolved(canon[i],a));
      if(completed.length){firstCompletion={index:i,axes:completed.map(a=>a.key)};break;}
    }
    if(!firstCompletion){rec.status='NO_TWO_BLOCK_COMPLETION_IN_SB_SPAN';inc(rec.status);rows.push(rec);continue;}counts.sb_any_completion++;rec.first_completion=firstCompletion;
    if(firstCompletion.axes.length!==1){counts.sb_first_completion_multi_axis++;rec.status='FIRST_COMPLETION_MULTI_AXIS';inc(rec.status);rows.push(rec);continue;}counts.unique_axis_completion++;
    const axis=axes.find(a=>a.key===firstCompletion.axes[0]);axisCounts[axis.key]=(axisCounts[axis.key]||0)+1;
    const fbState=canon[fb.end],aSolved=blockSolved(fbState,axis.block_a),bSolved=blockSolved(fbState,axis.block_b);
    rec.fb_axis_state={axis_key:axis.key,block_a_solved:aSolved,block_b_solved:bSolved};
    if(Number(aSolved)+Number(bSolved)!==1){rec.status='FB_CANNOT_ORIENT_UNIQUE_AXIS';inc(rec.status);rows.push(rec);continue;}counts.fb_oriented_unique_axis++;
    const frame=aSolved?{key:`${axis.bottom}|${axis.side_a}`,bottom:axis.bottom,top:axis.top,first_side:axis.side_a,second_side:axis.side_b,first:axis.block_a,second:axis.block_b}:{key:`${axis.bottom}|${axis.side_b}`,bottom:axis.bottom,top:axis.top,first_side:axis.side_b,second_side:axis.side_a,first:axis.block_b,second:axis.block_a};
    frameCounts[frame.key]=(frameCounts[frame.key]||0)+1;rec.frame_key=frame.key;rec.axis_key=axis.key;rec.sb_completion_index=firstCompletion.index;
    if(!blockSolved(canon[firstCompletion.index],frame.first)||!blockSolved(canon[firstCompletion.index],frame.second)){rec.status='COMPLETION_FRAME_INCONSISTENT';inc(rec.status);rows.push(rec);continue;}
    counts.g2_admitted++;

    function addFeature(phase,channel,start,end,amplitude){features.push({result_id:r.result_id,attempt_number:r.attempt_number,reco_id:r.reco_id??null,source:r.source,method:'Roux',generation:'ROUX-MEASUREMENT-G2',phase,channel,move_count:end-start,move_bin:moveBin(end-start),observed_amplitude:amplitude,axis_key:axis.key,frame_key:frame.key,fold:foldOf(attemptKey(r))});}
    const fbStates=canon.slice(fb.start,fb.end+1),fbMasks=blockMasks(frame.first),fbDs=fbStates.map(p=>maskDistance(p,defaultPattern,fbMasks));addFeature('FB','objective',fb.start,fb.end,objectiveBacktrack(fbDs));
    const sbEnd=firstCompletion.index,sbStates=canon.slice(sb.start,sbEnd+1),sbMasks=blockMasks(frame.second),sbDs=sbStates.map(p=>maskDistance(p,defaultPattern,sbMasks));addFeature('SB','objective',sb.start,sbEnd,objectiveBacktrack(sbDs));addFeature('SB','anchor',sb.start,sbEnd,anchorBreak(sbStates,blockMasks(frame.first)));

    const cmll=firstLineAfter(parsed.lines,'ROUX_CMLL',sbEnd);
    if(cmll){counts.cmll_opportunities++;const endpoint=canon[cmll.end],consistent=blockSolved(endpoint,frame.first)&&blockSolved(endpoint,frame.second)&&cornersSolvedAUF(endpoint,frame.top);rec.cmll_consistent=consistent;if(consistent)counts.cmll_consistent++;
      const targets=aufVariants(endpoint,frame.top),masks=[{orbit:CORNER,positions:allCorners}],phaseStates=canon.slice(cmll.start,cmll.end+1),ds=phaseStates.map(p=>minTargetDistance(p,targets,masks));addFeature('CMLL','objective',cmll.start,cmll.end,objectiveBacktrack(ds));addFeature('CMLL','anchor',cmll.start,cmll.end,anchorBreak(phaseStates,twoBlockMasks(frame)));
    }
    const lse=firstContiguousSpan(parsed.lines,'ROUX_LSE',sbEnd);
    if(lse){counts.lse_opportunities++;const endpoint=canon[lse.end],consistent=blockSolved(endpoint,frame.first)&&blockSolved(endpoint,frame.second);rec.lse_consistent=consistent;if(consistent)counts.lse_consistent++;
      const masks=[{orbit:EDGE,positions:lseEdges(frame)}],phaseStates=canon.slice(lse.start,lse.end+1),ds=phaseStates.map(p=>maskDistance(p,endpoint,masks));addFeature('LSE','objective',lse.start,lse.end,objectiveBacktrack(ds));addFeature('LSE','anchor',lse.start,lse.end,anchorBreak(phaseStates,twoBlockMasks(frame)));rec.lse_span={start:lse.start,end:lse.end,line_count:lse.lines.length};
    }
    rec.status='G2_ADMITTED';rows.push(rec);
  }catch(e){counts.errors++;rec.status='ERROR';rec.error=String(e?.stack||e?.message||e).slice(0,600);inc(rec.status);rows.push(rec);}
}

const rate=(n,d)=>d?n/d:0;
const rates={
  sb_any_completion_rate:rate(counts.sb_any_completion,counts.sb_search_eligible),
  unique_axis_completion_rate_given_any_completion:rate(counts.unique_axis_completion,counts.sb_any_completion),
  fb_orientation_rate_given_unique_axis:rate(counts.fb_oriented_unique_axis,counts.unique_axis_completion),
  end_to_end_sb_completion_rate:rate(counts.g2_admitted,counts.sb_search_eligible),
  cmll_consistency_rate:rate(counts.cmll_consistent,counts.cmll_opportunities),
  lse_consistency_rate:rate(counts.lse_consistent,counts.lse_opportunities),
  geometry_failure_rate:1-rate(counts.g2_admitted,counts.sb_search_eligible)
};
const objectiveN=features.filter(x=>x.channel==='objective').length;
const checks={
  ordered_physical_frames_24:orderedFrames.length===24,
  physical_axes_12:axes.length===12,
  every_frame_two_disjoint_3e2c_blocks:orderedFrames.every(f=>f.first.edges.length===3&&f.first.corners.length===2&&f.second.edges.length===3&&f.second.corners.length===2&&f.first.edges.every(i=>!f.second.edges.includes(i))&&f.first.corners.every(i=>!f.second.corners.includes(i))),
  state_certified_ge_100:counts.state_certified>=100,
  primary_exact_fb_attempts_ge_100:counts.g2_admitted>=100,
  sb_any_completion_rate_ge_0_90:rates.sb_any_completion_rate>=.90,
  unique_axis_completion_rate_given_any_completion_ge_0_90:rates.unique_axis_completion_rate_given_any_completion>=.90,
  fb_orientation_rate_given_unique_axis_ge_0_90:rates.fb_orientation_rate_given_unique_axis>=.90,
  end_to_end_sb_completion_rate_ge_0_90:rates.end_to_end_sb_completion_rate>=.90,
  cmll_consistency_rate_ge_0_80:rates.cmll_consistency_rate>=.80,
  lse_consistency_rate_ge_0_90:rates.lse_consistency_rate>=.90,
  geometry_failure_rate_le_0_10:rates.geometry_failure_rate<=.10,
  total_features_ge_350:features.length>=350,
  objective_features_ge_275:objectiveN>=275,
  no_center_color_relabel:true,
  all_features_g2:features.every(x=>x.generation==='ROUX-MEASUREMENT-G2')
};
const pass=Object.values(checks).every(Boolean);
const audit={
  schema_version:'CR0105R112-ROUX-G2-CENTER-CONSISTENT-GEOMETRY-1',
  generation:'ROUX-MEASUREMENT-G2',
  status:pass?'PASS_ROUX_G2_GEOMETRY':'HOLD_ROUX_G2_GEOMETRY',
  operator:{center_canonicalization:'unique center-default physical orientation at every queried state',ordered_physical_frames:orderedFrames.length,physical_axes:axes.length,sb_completion:'first state in frozen contiguous SB span with any completed axis; first completion must be unique',fb_orientation:'unique completion axis oriented by exactly one solved block at ordinary FB endpoint',color_relabel:false,lse_target:'last endpoint of first contiguous ROUX_LSE span after SB completion'},
  counts,rates,checks,rejection_reasons:rejection,
  feature_counts:{total:features.length,objective:objectiveN,anchor:features.length-objectiveN,eligible_attempts:new Set(features.map(attemptKey)).size,phase:Object.fromEntries(['FB','SB','CMLL','LSE'].map(p=>[p,features.filter(x=>x.phase===p).length]))},
  axis_counts:axisCounts,frame_counts:frameCounts,sb_annotation_family_counts:sbFamily,
  candidate_sources:{SEALED_R111:records.filter(x=>x.source==='SEALED_R111').length,R112_EXPANSION:records.filter(x=>x.source==='R112_EXPANSION').length},
  post_result_gate_change:false,
  fresh_network_read_in_geometry:false,
  acquired_public_routes_role:'DEVELOPMENT_AND_CALIBRATION_ONLY',
  fresh_confirmatory_scoring:false,
  human_observations:0
};
audit.semantic_sha256=sha(audit);
fs.writeFileSync(`${ROOT}/ROUX_G2_GEOMETRY_AUDIT.json`,JSON.stringify(audit,null,2)+'\n');
fs.writeFileSync(`${ROOT}/ROUX_G2_ROUTE_ROWS.json`,JSON.stringify({schema_version:'CR0105R112-ROUX-G2-ROUTE-ROWS-1',generation:'ROUX-MEASUREMENT-G2',rows,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${ROOT}/ROUX_G2_FEATURE_LEDGER.json`,JSON.stringify({schema_version:'CR0105R112-ROUX-G2-FEATURE-LEDGER-1',generation:'ROUX-MEASUREMENT-G2',rows:features,human_observations:0},null,2)+'\n');
console.log(JSON.stringify({status:audit.status,counts,rates,feature_counts:audit.feature_counts,checks,semantic_sha256:audit.semantic_sha256},null,2));
