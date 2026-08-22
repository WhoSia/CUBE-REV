import fs from 'node:fs';
import crypto from 'node:crypto';
import { Alg } from 'cubing/alg';
import { cube3x3x3 } from 'cubing/puzzles';
import { experimentalSolve3x3x3IgnoringCenters } from 'cubing/search';

const OUT = process.env.R18_NULL_ROOT || '/tmp/r18null';
fs.mkdirSync(OUT,{recursive:true});
const MANIFEST_PATH='research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json';
const NULL_FREEZE_PATH='research/0.10.5-r1.8/NAPKIN_NULL_AGGREGATION_FREEZE.json';
const manifest=JSON.parse(fs.readFileSync(MANIFEST_PATH,'utf8'));
const freeze=JSON.parse(fs.readFileSync(NULL_FREEZE_PATH,'utf8'));
const kp=await cube3x3x3.kpuzzle();
const defaultPattern=kp.defaultPattern();

function stable(x){
  if(Array.isArray(x)) return '['+x.map(stable).join(',')+']';
  if(x&&typeof x==='object') return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';
  return JSON.stringify(x);
}
function sha(x){return crypto.createHash('sha256').update(typeof x==='string'?x:stable(x)).digest('hex');}
function thash(t){return sha(t.transformationData);}
function quantileUpper(xs,q){
  if(!xs.length)return null;
  const a=[...xs].sort((x,y)=>x-y);
  return a[Math.max(0,Math.min(a.length-1,Math.ceil(q*a.length)-1))];
}
function physicalSolvedTransform(t){return defaultPattern.applyTransformation(t).experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});}
function physicalSolvedPattern(p){return p.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});}

// ---------- Phase grammar frozen from R1.7 ----------
const phasePatterns={
 INSPECTION:[/\binspection\b/i],
 CROSS:[/\b(?:cross|xcross|xxcross|xxxcross)\b/i,/\bpseudo\s+cross\b/i,/\bmissed\s+cross\b/i],
 F2L:[/\bf2l\b/i,/\b(?:1st|2nd|3rd|4th|first|second|third|fourth)\s*(?:\/\s*)?pair/i,/\bpairs?\b/i,/\bzbls\b/i,/\bsvls\b/i],
 LL_ORIENT:[/\boll(?:\b|cp)/i,/\beoll\b/i,/\bcoll\b/i,/\bollcp\b/i],
 LL_PERMUTE:[/\bpll\b/i,/\bepll\b/i,/\bauf\b/i],
 LL_ONELOOK:[/\bzbll\b/i,/\b2gll\b/i,/\bell\b/i,/\bcll\b/i],
 ROUX_FB:[/\bfb\b/i,/\bfbdr\b/i,/\bpseudo\s+fb\b/i],
 ROUX_SB:[/\bsb\b/i,/\bss\b/i,/\bsp\b/i,/\bflipped\s+sp\b/i],
 ROUX_CMLL:[/\bcmll\b/i],
 ROUX_LSE:[/\blse\b/i,/\beolr\b/i,/\beolrb\b/i,/\bep\b/i],
};
function classify(method,comment){
  const c=String(comment||'').trim().toLowerCase();if(!c)return {phase:'UNKNOWN',hits:[]};
  let hits=[];for(const [phase,ps] of Object.entries(phasePatterns))if(ps.some(p=>p.test(c)))hits.push(phase);
  if(method!=='Roux')hits=hits.filter(x=>!x.startsWith('ROUX_'));
  if(method==='Roux'&&hits.includes('LL_ONELOOK')&&/\bcll\b/i.test(c)&&!hits.includes('ROUX_CMLL')){hits=hits.filter(x=>x!=='LL_ONELOOK');hits.push('ROUX_CMLL');}
  hits=[...new Set(hits)];return {phase:hits.length===1?hits[0]:(hits.length?'AMBIGUOUS':'UNKNOWN'),hits};
}
function parseAnnotated(raw,method){
  const tokens=[],lines=[];let lineId=0;
  for(const rawLine of String(raw||'').split(/\r?\n/)){
    const idx=rawLine.indexOf('//');const left=(idx>=0?rawLine.slice(0,idx):rawLine).trim();const comment=(idx>=0?rawLine.slice(idx+2):'').trim();
    if(!left&&!comment)continue;
    const cls=classify(method,comment);let moves=[];
    if(left){const a=Alg.fromString(left).expand();moves=Array.from(a.experimentalLeafMoves()).map(m=>m.toString());}
    const start=tokens.length;for(const move of moves)tokens.push({move,phase:cls.phase,line_id:lineId,comment});
    lines.push({line_id:lineId,start,end:tokens.length,comment,phase:cls.phase,hits:cls.hits,moves});lineId++;
  }
  return {tokens,lines};
}

// ---------- Whole-cube orientation group ----------
function orientationGroup(){
  const gens=['x','y','z'].map(m=>kp.moveToTransformation(m));
  const id=kp.identityTransformation();
  const seen=new Map([[thash(id),id]]), queue=[id];
  while(queue.length){
    const a=queue.shift();
    for(const g of gens){
      const b=a.applyTransformation(g),h=thash(b);
      if(!seen.has(h)){seen.set(h,b);queue.push(b);}
    }
  }
  return [...seen.values()];
}
const ORIENT=orientationGroup();

function orbitName(regex){return Object.keys(defaultPattern.patternData).find(k=>regex.test(k));}
const EDGE_ORBIT=orbitName(/edge/i), CORNER_ORBIT=orbitName(/corner/i), CENTER_ORBIT=orbitName(/center/i);
if(!EDGE_ORBIT||!CORNER_ORBIT)throw new Error(`R18_ORBITS_NOT_FOUND ${Object.keys(defaultPattern.patternData)}`);
function mismatchForOrbit(a,b,name){
  const x=a.patternData[name],y=b.patternData[name];
  let piece=0,ori=0;
  if(x.pieces.length!==y.pieces.length||x.orientation.length!==y.orientation.length)throw new Error('R18_ORBIT_LENGTH_MISMATCH');
  for(let i=0;i<x.pieces.length;i++){
    if(x.pieces[i]!==y.pieces[i])piece++;
    if(x.orientation[i]!==y.orientation[i])ori++;
  }
  return {piece,orientation:ori,n:x.pieces.length};
}
function rawDistance(a,b){
  const e=mismatchForOrbit(a,b,EDGE_ORBIT),c=mismatchForOrbit(a,b,CORNER_ORBIT);
  const primary=.5*((e.piece+e.orientation)/12)+.5*((c.piece+c.orientation)/8);
  const secondary=e.piece+e.orientation+c.piece+c.orientation;
  return {primary,secondary,edge:e,corner:c};
}
function distance(a,b){
  let best=null,bestOri=-1;
  for(let i=0;i<ORIENT.length;i++){
    const r=rawDistance(a.applyTransformation(ORIENT[i]),b);
    if(!best||r.primary<best.primary-1e-12||(Math.abs(r.primary-best.primary)<1e-12&&r.secondary<best.secondary)) {best=r;bestOri=i;}
  }
  return {...best,orientation_index:bestOri};
}
function excursion(ds){
  // ds are state distances including line-start state at 0 and phase endpoint at index n.
  let frontier=ds[0],maxAny=0,bestCandidate=0,best=null;
  for(let t=1;t<ds.length;t++){
    const pre=frontier,amp=ds[t]-pre;
    if(amp>maxAny)maxAny=amp;
    if(amp>=freeze.minimum_candidate_floor-1e-12){
      // A return at the final endpoint is intentionally ineligible. k <= ds.length-2.
      for(let k=t+1;k<=ds.length-2;k++){
        if(ds[k]<=pre+1e-12){
          if(amp>bestCandidate){bestCandidate=amp;best={peak_index:t,return_index:k,pre_frontier:pre,peak_distance:ds[t],return_distance:ds[k],amplitude:amp};}
          break;
        }
      }
    }
    if(ds[t]<frontier)frontier=ds[t];
  }
  return {max_excursion_amplitude:maxAny,candidate_reversal_amplitude:bestCandidate,candidate:best};
}
function pathForMoves(start,target,moves){
  let p=start;const primary=[distance(p,target).primary],secondary=[distance(p,target).secondary];
  for(const m of moves){p=p.applyMove(m);const d=distance(p,target);primary.push(d.primary);secondary.push(d.secondary);}
  return {end:p,primary,secondary,excursion:excursion(primary),secondary_excursion:excursion(secondary.map(x=>x/40))};
}

// ---------- Validator court before any null values ----------
const validatorChecks={};
validatorChecks.orientation_group_size_24=ORIENT.length===24;
validatorChecks.orbits_found=!!EDGE_ORBIT&&!!CORNER_ORBIT;
const p0=defaultPattern,pA=p0.applyAlg("R U F2 L' D"),pAx=pA.applyAlg('x'),pAy=pA.applyAlg('y2'),pB=p0.applyAlg("R U2 F");
validatorChecks.identity_zero=Math.abs(distance(pA,pA).primary)<1e-12;
validatorChecks.rotated_equivalent_x_zero=Math.abs(distance(pAx,pA).primary)<1e-12;
validatorChecks.rotated_equivalent_y2_zero=Math.abs(distance(pAy,pA).primary)<1e-12;
validatorChecks.nontrivial_positive=distance(p0,pB).primary>0;
validatorChecks.symmetry=Math.abs(distance(pA,pB).primary-distance(pB,pA).primary)<1e-12;
validatorChecks.orientation_invariance_general=Math.abs(distance(pAx,pB).primary-distance(pA,pB).primary)<1e-12;
const synNo=excursion([.3,.2,.3,0]);
const synYes=excursion([.3,.2,.3,.1,0]);
validatorChecks.final_endpoint_does_not_create_recovery=synNo.candidate_reversal_amplitude===0;
validatorChecks.preendpoint_return_creates_reversal=synYes.candidate_reversal_amplitude>0;
validatorChecks.distance_quantum_edge_halfweight=Math.abs(.5*(1/12)-freeze.minimum_candidate_floor)<1e-12;

const validator={
  schema_version:'CR0105R18-PHASE-DISTANCE-VALIDATOR-1',
  status:Object.values(validatorChecks).every(Boolean)?'PASS':'HOLD',
  cubing_version:'0.63.3',
  cubing_source_commit:'c223a53ba37e0941fe8242571aef1cccb978bb24',
  edge_orbit:EDGE_ORBIT,corner_orbit:CORNER_ORBIT,center_orbit:CENTER_ORBIT,
  orientation_group_size:ORIENT.length,
  primary_distance:'0.5*(edge piece+orientation mismatch / 12) + 0.5*(corner piece+orientation mismatch / 8), minimum over 24 whole-cube orientations; centers excluded',
  checks:validatorChecks,
  synthetic:{endpoint_only_return:synNo,preendpoint_return:synYes},
  human_observations:0
};
fs.writeFileSync(`${OUT}/PHASE_DISTANCE_VALIDATOR.json`,JSON.stringify(validator,null,2)+'\n');
if(validator.status!=='PASS'){console.log(JSON.stringify(validator,null,2));process.exit(20);}

// ---------- State-certify R1.7 calibration routes and produce phase segments ----------
const routes=[],segments=[];let parseFail=0,stateFail=0;
for(const r of manifest.records){
  if(r.route_source_status!=='RAW_ALG_CUBING_LINK')continue;
  try{
    const parsed=parseAnnotated(r.raw_alg,r.method),moves=parsed.tokens.map(x=>x.move);
    const rawT=kp.algToTransformation(r.raw_alg),expandedT=kp.algToTransformation(moves.join(' '));
    if(!rawT.isIdentical(expandedT))throw new Error('EXPANSION_TRANSFORM_MISMATCH');
    const setupPattern=defaultPattern.applyAlg(r.raw_setup),end=setupPattern.applyTransformation(rawT);
    if(!physicalSolvedPattern(end)){stateFail++;continue;}
    const states=[setupPattern];let p=setupPattern;for(const m of moves){p=p.applyMove(m);states.push(p);}
    const route={reco_id:r.reco_id,result_id:r.result_id,attempt_number:r.attempt_number,method:r.method,state_certified:true,eligible_phase_lines:0};
    for(const line of parsed.lines){
      if(['INSPECTION','UNKNOWN','AMBIGUOUS'].includes(line.phase)||line.end-line.start<3)continue;
      const start=states[line.start],target=states[line.end],pmoves=moves.slice(line.start,line.end);
      const actual=pathForMoves(start,target,pmoves);
      if(distance(actual.end,target).primary>1e-12)throw new Error('LINE_ENDPOINT_DISTANCE_NONZERO');
      segments.push({
        segment_id:`${r.reco_id}:${line.line_id}`,reco_id:r.reco_id,result_id:r.result_id,attempt_number:r.attempt_number,
        method:r.method,phase:line.phase,line_id:line.line_id,comment:line.comment,moves:pmoves,start,target,
        actual_excursion:actual.excursion.max_excursion_amplitude,actual_candidate_reversal:actual.excursion.candidate_reversal_amplitude,
        actual_candidate:actual.excursion.candidate,actual_primary_path:actual.primary
      });
      route.eligible_phase_lines++;
    }
    routes.push(route);
  }catch(e){parseFail++;}
}

// ---------- Representation null: exact opposite-face commutation variants ----------
const outer=/^([URFDLB])(?:2'?|')?$/;
const opposite=new Set(['UD','DU','RL','LR','FB','BF']);
function family(m){const x=m.match(outer);return x?x[1]:null;}
function representationVariants(moves){
  const out=[],seen=new Set([moves.join(' ')]);
  for(let i=0;i<moves.length-1;i++){
    const a=family(moves[i]),b=family(moves[i+1]);
    if(a&&b&&opposite.has(a+b)){
      const z=[...moves];[z[i],z[i+1]]=[z[i+1],z[i]];const s=z.join(' ');
      if(!seen.has(s)){seen.add(s);out.push(z);}
    }
  }
  // Deterministic local canonicalization of adjacent commuting opposite faces.
  const order={U:0,D:1,R:2,L:3,F:4,B:5};
  let z=[...moves],changed=true,passes=0;
  while(changed&&passes++<moves.length*moves.length){
    changed=false;
    for(let i=0;i<z.length-1;i++){
      const a=family(z[i]),b=family(z[i+1]);
      if(a&&b&&opposite.has(a+b)&&order[a]>order[b]){[z[i],z[i+1]]=[z[i+1],z[i]];changed=true;}
    }
  }
  const s=z.join(' ');if(!seen.has(s)){seen.add(s);out.push(z);}
  return out.slice(0,16);
}

let repVariantGenerated=0,repVariantAccepted=0,solverAttempted=0,solverExactAccepted=0,solverPhysicalOnly=0,solverErrors=0;
const envelopeRows=[];
let solverInitialized=false;
for(let si=0;si<segments.length;si++){
  const seg=segments[si];
  const originalT=kp.algToTransformation(seg.moves.join(' '));
  let envelope=seg.actual_excursion;
  const repAmps=[];
  for(const z of representationVariants(seg.moves)){
    repVariantGenerated++;
    try{
      const tz=kp.algToTransformation(z.join(' '));
      if(!tz.isIdentical(originalT))continue;
      repVariantAccepted++;
      const a=pathForMoves(seg.start,seg.target,z).excursion.max_excursion_amplitude;
      repAmps.push(a);if(a>envelope)envelope=a;
    }catch{}
  }
  let solver={attempted:false,exact_accepted:false,physical_equivalent:false,error:null,amplitude:null,moves:null};
  try{
    solverAttempted++;solver.attempted=true;
    // Solve the relative endpoint from default, invert solve to obtain an alternate generator of the relative transformation.
    const relPattern=defaultPattern.applyTransformation(originalT);
    const solveAlg=await experimentalSolve3x3x3IgnoringCenters(relPattern);
    solverInitialized=true;
    const altAlg=solveAlg.invert(),altMoves=Array.from(altAlg.expand().experimentalLeafMoves()).map(m=>m.toString());
    const altT=kp.algToTransformation(altMoves.join(' '));
    solver.moves=altMoves;
    solver.exact_accepted=altT.isIdentical(originalT);
    const altEnd=seg.start.applyTransformation(altT);
    solver.physical_equivalent=distance(altEnd,seg.target).primary<1e-12;
    if(solver.exact_accepted){
      solverExactAccepted++;
      const a=pathForMoves(seg.start,seg.target,altMoves).excursion.max_excursion_amplitude;
      solver.amplitude=a;if(a>envelope)envelope=a;
    } else if(solver.physical_equivalent) solverPhysicalOnly++;
  }catch(e){solverErrors++;solver.error=String(e?.message||e).slice(0,300);}
  envelopeRows.push({
    segment_id:seg.segment_id,reco_id:seg.reco_id,result_id:seg.result_id,attempt_number:seg.attempt_number,method:seg.method,phase:seg.phase,
    move_count:seg.moves.length,actual_excursion:seg.actual_excursion,actual_candidate_reversal:seg.actual_candidate_reversal,
    representation_variant_n:repAmps.length,representation_max:repAmps.length?Math.max(...repAmps):null,
    solver_attempted:solver.attempted,solver_exact_accepted:solver.exact_accepted,solver_physical_equivalent:solver.physical_equivalent,solver_amplitude:solver.amplitude,
    null_envelope:envelope
  });
  if((si+1)%250===0)console.log(`R18_NULL_PROGRESS ${si+1}/${segments.length}`);
}

// ---------- Frozen threshold hierarchy ----------
const byMethodPhase=new Map(),byPhase=new Map();
for(const z of envelopeRows){
  const mp=`${z.method}|${z.phase}`;
  if(!byMethodPhase.has(mp))byMethodPhase.set(mp,[]);byMethodPhase.get(mp).push(z.null_envelope);
  if(!byPhase.has(z.phase))byPhase.set(z.phase,[]);byPhase.get(z.phase).push(z.null_envelope);
}
const globalVals=envelopeRows.map(z=>z.null_envelope),global995=quantileUpper(globalVals,.995);
const keys=[...new Set(envelopeRows.map(z=>`${z.method}|${z.phase}`))].sort();
const thresholds={};
for(const key of keys){
  const [method,phase]=key.split('|'),mp=byMethodPhase.get(key)||[],ph=byPhase.get(phase)||[];
  let level,q,vals;
  if(mp.length>=40){level='METHOD_PHASE_99';q=.99;vals=mp;}
  else if(ph.length>=80){level='PHASE_99';q=.99;vals=ph;}
  else {level='GLOBAL_99_5';q=.995;vals=globalVals;}
  thresholds[key]={method,phase,level,q,n:vals.length,threshold:quantileUpper(vals,q),method_phase_n:mp.length,phase_n:ph.length};
}

const calibration={
  schema_version:'CR0105R18-ALGORITHM-NULL-CALIBRATION-1',status:'PASS',
  calibration_source:'R1.7 frozen 900-attempt route manifest; no R1.8 holdout route outcomes read',
  r17_manifest_sha256:sha(fs.readFileSync(MANIFEST_PATH)),
  state_certified_routes:routes.length,route_parse_or_expansion_failures:parseFail,route_state_failures:stateFail,
  eligible_phase_segments:segments.length,
  observed_actual_candidate_reversal_segments:envelopeRows.filter(z=>z.actual_candidate_reversal>=freeze.minimum_candidate_floor-1e-12).length,
  representation:{generated:repVariantGenerated,exact_transformation_accepted:repVariantAccepted},
  solver:{attempted:solverAttempted,worker_initialized:solverInitialized,exact_transformation_accepted:solverExactAccepted,physical_only_not_primary:solverPhysicalOnly,errors:solverErrors},
  null_aggregation:'one envelope observation per phase segment = max observed/accepted exact-transformation null realization',
  global:{n:globalVals.length,p50:quantileUpper(globalVals,.5),p90:quantileUpper(globalVals,.9),p95:quantileUpper(globalVals,.95),p99:quantileUpper(globalVals,.99),p995:global995,max:Math.max(...globalVals)},
  thresholds,
  human_observations:0
};
const thresholdSeal={
  schema_version:'CR0105R18-NULL-THRESHOLD-SEAL-1',status:'SEALED_BEFORE_HOLDOUT_SCORE',
  napkin_freeze_sha256:sha(fs.readFileSync(NULL_FREEZE_PATH)),
  r17_manifest_sha256:calibration.r17_manifest_sha256,
  distance_validator_sha256:sha(validator),
  calibration_summary:{state_certified_routes:routes.length,eligible_phase_segments:segments.length,representation_exact_accepted:repVariantAccepted,solver_exact_accepted:solverExactAccepted,global:calibration.global},
  threshold_hierarchy:freeze.threshold_hierarchy,quantile_rule:freeze.quantile_rule,minimum_candidate_floor:freeze.minimum_candidate_floor,large_reversal_floor:freeze.large_reversal_floor,
  thresholds,
  holdout_outcomes_seen:false,
  human_observations:0
};
thresholdSeal.seal_sha256=sha(thresholdSeal);
fs.writeFileSync(`${OUT}/ALGORITHM_NULL_CALIBRATION.json`,JSON.stringify(calibration,null,2)+'\n');
fs.writeFileSync(`${OUT}/NULL_THRESHOLD_SEAL.json`,JSON.stringify(thresholdSeal,null,2)+'\n');
// Compact row ledger; deliberately no raw move paths needed for threshold seal.
fs.writeFileSync(`${OUT}/NULL_SEGMENT_LEDGER.json`,JSON.stringify({schema_version:'CR0105R18-NULL-SEGMENT-LEDGER-1',rows:envelopeRows,human_observations:0},null,2)+'\n');
console.log(JSON.stringify({validator:validator.status,state_certified_routes:routes.length,eligible_phase_segments:segments.length,representation_exact_accepted:repVariantAccepted,solver_exact_accepted:solverExactAccepted,solver_physical_only:solverPhysicalOnly,solver_errors:solverErrors,global:calibration.global,threshold_count:Object.keys(thresholds).length,seal_sha256:thresholdSeal.seal_sha256},null,2));
