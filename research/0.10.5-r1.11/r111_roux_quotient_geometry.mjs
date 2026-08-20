import fs from 'node:fs';
import crypto from 'node:crypto';
import { buildR19Core, parseAnnotated, sha } from '../0.10.5-r1.9/r19_quotient_core.mjs';

const OUT=process.env.R111_ROOT||'/tmp/r111';fs.mkdirSync(OUT,{recursive:true});
const core=await buildR19Core();
const {kp,defaultPattern,EDGE,CORNER,ORIENT,faceSupport,opposite}=core;
const attemptKey=r=>`${r.result_id}:${r.attempt_number}`;
const foldOf=k=>parseInt(crypto.createHash('sha256').update(k).digest('hex').slice(0,8),16)%5;
const intersect=(a,b)=>{const s=new Set(b);return a.filter(x=>s.has(x));};
function blockMask(bottom,side){
  const top=opposite[bottom];
  return {bottom,side,top,edges:faceSupport[side].edges.filter(i=>!faceSupport[top].edges.includes(i)),corners:intersect(faceSupport[bottom].corners,faceSupport[side].corners)};
}
const FIRST=blockMask('D','L'),SECOND=blockMask('D','R');
const allCorners=defaultPattern.patternData[CORNER].pieces.map((_,i)=>i);
const allEdges=defaultPattern.patternData[EDGE].pieces.map((_,i)=>i);
const blockEdges=new Set([...FIRST.edges,...SECOND.edges]);
const LSE_EDGES=allEdges.filter(i=>!blockEdges.has(i));
function coordMatch(p,t,orbit,i){const a=p.patternData[orbit],b=t.patternData[orbit];return a.pieces[i]===b.pieces[i]&&a.orientation[i]===b.orientation[i];}
function solvedCoord(p,orbit,i){return coordMatch(p,defaultPattern,orbit,i);}
function blockSolved(p,m){return m.edges.every(i=>solvedCoord(p,EDGE,i))&&m.corners.every(i=>solvedCoord(p,CORNER,i));}
function bothBlocks(p){return blockSolved(p,FIRST)&&blockSolved(p,SECOND);}
function transformState(raw,idx){return raw.applyTransformation(ORIENT[idx]);}
function admissibleTransforms(fbEndpoint){const a=[];for(let i=0;i<ORIENT.length;i++)if(blockSolved(transformState(fbEndpoint,i),FIRST))a.push(i);return a;}
function maskDistance(p,target,masks){let bad=0,total=0;for(const m of masks)for(const i of m.positions){total+=2;const a=p.patternData[m.orbit],b=target.patternData[m.orbit];if(a.pieces[i]!==b.pieces[i])bad++;if(a.orientation[i]!==b.orientation[i])bad++;}return total?bad/total:null;}
function minVariantDistance(p,targets,masks){return Math.min(...targets.map(t=>maskDistance(p,t,masks)));}
function aufVariants(p){const out=[p];let q=p;for(let i=1;i<4;i++){q=q.applyMove('U');out.push(q);}return out;}
function cornersSolvedAUF(p){let q=p;for(let i=0;i<4;i++){if(allCorners.every(j=>solvedCoord(q,CORNER,j)))return true;q=q.applyMove('U');}return false;}
function objectiveBacktrack(ds){let best=Infinity,amp=0;for(const d of ds){best=Math.min(best,d);amp=Math.max(amp,d-best);}return amp;}
function anchorDamage(p,masks){let bad=0,total=0;for(const m of masks)for(const i of m.positions){total+=2;const a=p.patternData[m.orbit],b=defaultPattern.patternData[m.orbit];if(a.pieces[i]!==b.pieces[i])bad++;if(a.orientation[i]!==b.orientation[i])bad++;}return total?bad/total:null;}
function anchorBreak(vals){if(!vals.length)return null;const a0=vals[0];return Math.max(...vals.map(x=>Math.max(0,x-a0)));}
function moveBin(n){return n<=5?'1-5':n<=8?'6-8':n<=12?'9-12':'13+';}
function loadRecords(){
  const a=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R17'}));
  const b=JSON.parse(fs.readFileSync('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R18'}));
  return [...a,...b].filter(r=>r.method==='Roux'&&r.route_source_status==='RAW_ALG_CUBING_LINK');
}
const records=loadRecords(),rows=[],features=[];
const C={manifest_roux:records.length,parse_ok:0,state_certified:0,fb_line:0,unique_transform:0,fb_acquisition_pass:0,sb_line:0,sb_pass:0,cmll_line:0,cmll_pass:0,lse_line:0,lse_pass:0,errors:0};
const opportunities={total:0,failed:0,by_phase:{FB:0,SB:0,CMLL:0,LSE:0},missing_phase:{FB:0,SB:0,CMLL:0,LSE:0}};
function addFeature(r,phase,channel,line,amp,frameIdx){features.push({result_id:r.result_id,attempt_number:r.attempt_number,reco_id:r.reco_id,source:r.source,method:'Roux',phase,channel,move_count:line.end-line.start,move_bin:moveBin(line.end-line.start),observed_amplitude:amp,frame_transform_index:frameIdx,fold:foldOf(attemptKey(r))});}
for(const r of records){
  const rec={result_id:r.result_id,attempt_number:r.attempt_number,reco_id:r.reco_id,source:r.source,status:'START'};
  try{
    const parsed=parseAnnotated(r.raw_alg,'Roux'),moves=parsed.tokens.map(x=>x.move);C.parse_ok++;
    let s=defaultPattern.applyAlg(r.raw_setup),states=[s];for(const m of moves){s=s.applyMove(m);states.push(s);}rec.final_solved=s.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});if(!rec.final_solved){rec.status='FINAL_NOT_SOLVED';rows.push(rec);continue;}C.state_certified++;
    const lineOf=ph=>parsed.lines.find(x=>x.phase===ph&&x.end>x.start)||null;
    const fb=lineOf('ROUX_FB'),sb=lineOf('ROUX_SB'),cmll=lineOf('ROUX_CMLL'),lse=lineOf('ROUX_LSE');rec.lines={FB:fb&&[fb.start,fb.end],SB:sb&&[sb.start,sb.end],CMLL:cmll&&[cmll.start,cmll.end],LSE:lse&&[lse.start,lse.end]};
    for(const [n,l] of [['FB',fb],['SB',sb],['CMLL',cmll],['LSE',lse]])if(!l)opportunities.missing_phase[n]++;
    if(!fb){rec.status='NO_FB_LINE';rows.push(rec);continue;}C.fb_line++;
    const candidates=admissibleTransforms(states[fb.end]);rec.frame_candidate_n=candidates.length;rec.frame_candidates=candidates;
    if(candidates.length!==1){rec.status='FRAME_NOT_UNIQUE';rows.push(rec);continue;}C.unique_transform++;
    const fi=candidates[0],qs=states.map(x=>transformState(x,fi));rec.frame_transform_index=fi;
    rec.fb_acquisition=!blockSolved(qs[fb.start],FIRST)&&blockSolved(qs[fb.end],FIRST);if(rec.fb_acquisition)C.fb_acquisition_pass++;
    if(sb){C.sb_line++;rec.sb_pass=blockSolved(qs[sb.end],FIRST)&&blockSolved(qs[sb.end],SECOND)&&!bothBlocks(qs[sb.start]);if(rec.sb_pass)C.sb_pass++;}
    if(cmll){C.cmll_line++;rec.cmll_pass=bothBlocks(qs[cmll.end])&&cornersSolvedAUF(qs[cmll.end]);if(rec.cmll_pass)C.cmll_pass++;}
    if(lse){C.lse_line++;rec.lse_pass=bothBlocks(qs[lse.end])&&rec.final_solved;if(rec.lse_pass)C.lse_pass++;}
    const phaseDefs=[];
    phaseDefs.push(['FB',fb,[{name:'objective',masks:[{orbit:EDGE,positions:FIRST.edges},{orbit:CORNER,positions:FIRST.corners}],targets:[qs[fb.end]]}],[]]);
    if(sb)phaseDefs.push(['SB',sb,[{name:'objective',masks:[{orbit:EDGE,positions:SECOND.edges},{orbit:CORNER,positions:SECOND.corners}],targets:[qs[sb.end]]}],[{name:'anchor',masks:[{orbit:EDGE,positions:FIRST.edges},{orbit:CORNER,positions:FIRST.corners}]}]]);
    if(cmll)phaseDefs.push(['CMLL',cmll,[{name:'objective',masks:[{orbit:CORNER,positions:allCorners}],targets:aufVariants(qs[cmll.end])}],[{name:'anchor',masks:[{orbit:EDGE,positions:[...FIRST.edges,...SECOND.edges]},{orbit:CORNER,positions:[...FIRST.corners,...SECOND.corners]}]}]]);
    if(lse)phaseDefs.push(['LSE',lse,[{name:'objective',masks:[{orbit:EDGE,positions:LSE_EDGES}],targets:[qs[lse.end]]}],[{name:'anchor',masks:[{orbit:EDGE,positions:[...FIRST.edges,...SECOND.edges]},{orbit:CORNER,positions:[...FIRST.corners,...SECOND.corners]}]}]]);
    let geomFail=0;
    for(const [phase,line,objs,anchors] of phaseDefs){opportunities.total++;opportunities.by_phase[phase]++;
      try{
        for(const o of objs){const ds=[];for(let i=line.start;i<=line.end;i++)ds.push(minVariantDistance(qs[i],o.targets,o.masks));addFeature(r,phase,o.name,line,objectiveBacktrack(ds),fi);}
        for(const a of anchors){const vals=[];for(let i=line.start;i<=line.end;i++)vals.push(anchorDamage(qs[i],a.masks));addFeature(r,phase,a.name,line,anchorBreak(vals),fi);}
      }catch(e){geomFail++;opportunities.failed++;}
    }
    rec.geometry_failures=geomFail;rec.status='FRAME_EVALUATED';rows.push(rec);
  }catch(e){C.errors++;rec.status='ERROR';rec.error=String(e?.message||e).slice(0,300);rows.push(rec);}
}
const rate=(n,d)=>d?n/d:0;
const objectiveN=features.filter(x=>x.channel==='objective').length;
const eligibleAttempts=new Set(features.map(attemptKey)).size;
const geometryFailureRate=rate(opportunities.failed,opportunities.total);
const rates={unique_transform_rate:rate(C.unique_transform,C.fb_line),fb_acquisition_rate:rate(C.fb_acquisition_pass,C.unique_transform),sb_frame_preservation_and_acquisition_rate:rate(C.sb_pass,C.sb_line),cmll_consistency_rate:rate(C.cmll_pass,C.cmll_line),lse_consistency_rate:rate(C.lse_pass,C.lse_line),geometry_failure_rate:geometryFailureRate};
const checks={
  standard_first_block_3e2c:FIRST.edges.length===3&&FIRST.corners.length===2,
  standard_second_block_3e2c:SECOND.edges.length===3&&SECOND.corners.length===2,
  block_edge_masks_disjoint:FIRST.edges.every(x=>!SECOND.edges.includes(x)),
  block_corner_masks_disjoint:FIRST.corners.every(x=>!SECOND.corners.includes(x)),
  orientation_group_24:ORIENT.length===24,
  state_certified_ge_80:C.state_certified>=80,
  fb_line_ge_80:C.fb_line>=80,
  unique_transform_rate_ge_0_95:rates.unique_transform_rate>=.95,
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
const audit={schema_version:'CR0105R111-ROUX-BLOCK-INTERNAL-GEOMETRY-1',status,standard_frame:{bottom:'D',first_side:'L',second_side:'R',top:'U',first_block:FIRST,second_block:SECOND,lse_edges:LSE_EDGES},counts:C,rates,feature_counts:{total:features.length,objective:objectiveN,anchor:features.length-objectiveN,eligible_attempts:eligibleAttempts,phase:Object.fromEntries(['FB','SB','CMLL','LSE'].map(p=>[p,features.filter(x=>x.phase===p).length]))},geometry_opportunities:opportunities,checks,frame_rule:'Unique FB-endpoint whole-cube orientation sending the physical first block to standard (D,L); the selected transform is locked for all later phases.',historical_role:'DEVELOPMENT_AND_CALIBRATION_ONLY',fresh_outcomes_seen:false,human_observations:0};
audit.semantic_sha256=sha(audit);
fs.writeFileSync(`${OUT}/ROUX_BLOCK_INTERNAL_GEOMETRY_AUDIT.json`,JSON.stringify(audit,null,2)+'\n');
fs.writeFileSync(`${OUT}/ROUX_FRAME_ROUTE_ROWS.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-FRAME-ROUTE-ROWS-1',rows,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${OUT}/ROUX_FEATURE_LEDGER.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-FEATURE-LEDGER-1',rows:features,historical_role:'DEVELOPMENT_AND_CALIBRATION_ONLY',human_observations:0},null,2)+'\n');
console.log(JSON.stringify(audit,null,2));
