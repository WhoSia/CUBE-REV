import fs from 'node:fs';
import { parseAnnotated, sha } from '../0.10.5-r1.9/r19_quotient_core.mjs';
import { buildRouxFrameCore } from './r110_roux_frame_core.mjs';

const OUT=process.env.R110_LOCAL_ROOT||'/tmp/r110local';fs.mkdirSync(OUT,{recursive:true});
const napkin=JSON.parse(fs.readFileSync('research/0.10.5-r1.10/NAPKIN_INTENT_AND_PREREGISTRATION.json','utf8'));
const c=await buildRouxFrameCore();
const {kp,defaultPattern,opposite,frames,solvedBlock,bothBlocks,cornersSolvedAUF}=c;
const axes=[...new Set(frames.map(f=>f.axis_key))];
const structural={frames_24:frames.length===24,axes_12:axes.length===12,every_block_3_edges_2_corners:frames.every(f=>f.first.edges.length===3&&f.first.corners.length===2&&f.second.edges.length===3&&f.second.corners.length===2),paired_blocks_disjoint:frames.every(f=>f.first.edges.every(i=>!f.second.edges.includes(i))&&f.first.corners.every(i=>!f.second.corners.includes(i)))};
function records(){
 const a=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R17'}));
 const b=JSON.parse(fs.readFileSync('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R18'}));
 return [...a,...b].filter(r=>r.method==='Roux');
}
const line=(p,x)=>p.lines.find(z=>z.phase===x&&z.end>z.start)||null;
const outRows=[];let route=0,state=0,ordN=0,ordU=0,axisN=0,axisU=0,cmN=0,cmP=0,lseN=0,lseP=0,errors=0;
for(const r of records()){
 const row={result_id:r.result_id,attempt_number:r.attempt_number,reco_id:r.reco_id,source:r.source};
 if(r.route_source_status!=='RAW_ALG_CUBING_LINK'){row.status='NO_ROUTE';outRows.push(row);continue;}route++;
 try{
  const p=parseAnnotated(r.raw_alg,'Roux'),moves=p.tokens.map(x=>x.move);let s=defaultPattern.applyAlg(r.raw_setup),states=[s];for(const m of moves){s=s.applyMove(m);states.push(s);}
  if(!s.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true})){row.status='FINAL_NOT_SOLVED';outRows.push(row);continue;}state++;
  const fb=line(p,'ROUX_FB'),sb=line(p,'ROUX_SB'),cm=line(p,'ROUX_CMLL'),ls=line(p,'ROUX_LSE');
  row.lines={fb:fb&&[fb.start,fb.end],sb:sb&&[sb.start,sb.end],cmll:cm&&[cm.start,cm.end],lse:ls&&[ls.start,ls.end]};
  const ordered=[];
  if(fb&&sb&&fb.end<=sb.start){ordN++;for(const f of frames){if(!solvedBlock(states[fb.start],f.first)&&solvedBlock(states[fb.end],f.first)&&solvedBlock(states[sb.end],f.first)&&solvedBlock(states[sb.end],f.second)&&!bothBlocks(states[sb.start],f))ordered.push(f);}if(ordered.length===1)ordU++;}
  const amap=new Map();
  if(sb){axisN++;for(const f of frames)if(bothBlocks(states[sb.end],f)&&!bothBlocks(states[sb.start],f)&&!amap.has(f.axis_key))amap.set(f.axis_key,f);if(amap.size===1)axisU++;}
  row.ordered_candidate_n=ordered.length;row.ordered_candidates=ordered.map(f=>({bottom:f.bottom,first_side:f.first_side,second_side:f.second_side}));row.axis_candidate_n=amap.size;row.axis_candidates=[...amap.values()].map(f=>({bottom:f.bottom,sides:[f.first_side,f.second_side].sort()}));
  const chosen=ordered.length===1?ordered[0]:(amap.size===1?[...amap.values()][0]:null);row.frame_source=ordered.length===1?'ORDERED_FB_SB':amap.size===1?'SB_AXIS_ONLY':null;
  if(chosen&&cm){cmN++;row.cmll_consistent=bothBlocks(states[cm.end],chosen)&&cornersSolvedAUF(states[cm.end],opposite[chosen.bottom]);if(row.cmll_consistent)cmP++;}
  if(chosen&&ls){lseN++;row.lse_consistent=bothBlocks(states[ls.start],chosen)&&states[ls.end].experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});if(row.lse_consistent)lseP++;}
  row.status='STATE_CERTIFIED';outRows.push(row);
 }catch(e){errors++;row.status='ERROR';row.error=String(e?.message||e).slice(0,240);outRows.push(row);}
}
const ordRate=ordU/Math.max(1,ordN),axisRate=axisU/Math.max(1,axisN),cmRate=cmP/Math.max(1,cmN),lseRate=lseP/Math.max(1,lseN);
const g=napkin.roux_block_frame;
const checks={...structural,historical_roux_attempts_92:records().length===92,roux_state_certified_ge_80:state>=80,ordered_eligible_ge_15:ordN>=g.minimum_ordered_eligible_attempts,ordered_unique_rate_ge_0_80:ordRate>=g.minimum_ordered_unique_rate,axis_eligible_ge_30:axisN>=g.minimum_axis_eligible_attempts,axis_unique_rate_ge_0_80:axisRate>=g.minimum_axis_unique_rate,cmll_consistency_rate_ge_0_85:cmN>0&&cmRate>=g.minimum_cmll_consistency_rate};
const status=Object.values(checks).every(Boolean)?'PASS_ROUX_BLOCK_FRAME_IDENTIFICATION':'HOLD_ROUX_BLOCK_FRAME_IDENTIFICATION';
const result={schema_version:'CR0105R110-ROUX-BLOCK-FRAME-1',status,structural,counts:{historical_roux_attempts:records().length,route_source:route,state_certified:state,ordered_eligible:ordN,ordered_unique:ordU,axis_eligible:axisN,axis_unique:axisU,cmll_consistency_n:cmN,cmll_consistency_pass:cmP,lse_consistency_n:lseN,lse_consistency_pass:lseP,errors},rates:{ordered_unique_rate:ordRate,axis_unique_rate:axisRate,cmll_consistency_rate:cmRate,lse_consistency_rate:lseRate},checks,future_roux_scoring_authority:false,interpretation:'State-derived 1x2x3 frame-identification engineering court only; comments choose route lines but do not define cubie frame. PASS never releases Roux scoring authority in R1.10.',human_observations:0};result.semantic_sha256=sha(result);
fs.writeFileSync(`${OUT}/ROUX_BLOCK_FRAME_ROWS.json`,JSON.stringify({schema_version:'CR0105R110-ROUX-BLOCK-FRAME-ROWS-1',rows:outRows,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${OUT}/ROUX_BLOCK_FRAME_IDENTIFICATION.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
