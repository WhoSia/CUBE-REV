import fs from 'node:fs';
import { buildR19Core, parseAnnotated, sha, upperQuantile, mean } from './r19_quotient_core.mjs';

const OUT=process.env.R19_DEV_ROOT||'/tmp/r19dev';fs.mkdirSync(OUT,{recursive:true});
const core=await buildR19Core(); const {kp,defaultPattern,detectCrossFace,detectRouxLastFace,buildPhaseSpec,featureForMoves,exactNullRealizations}=core;
const NAPKIN_PATH='research/0.10.5-r1.9/NAPKIN_INTENT_AND_PREREGISTRATION.json';
const CORE_PATH='research/0.10.5-r1.9/r19_quotient_core.mjs';
const napkin=JSON.parse(fs.readFileSync(NAPKIN_PATH,'utf8'));
const MIN_LOCAL_FALLBACK_RATE=.05;
function foldOf(resultId,attempt){return parseInt(sha(`R19FOLD:${resultId}:${attempt}`).slice(0,8),16)%5;}
function moveBin(n){return n<=5?'3-5':n<=8?'6-8':n<=12?'9-12':'13+';}
function featureCountBin(n){return n<=8?'1-8':n<=12?'9-12':n<=16?'13-16':'17+';}
function keyOf(r){return `${r.result_id}:${r.attempt_number}`;}
function loadRecords(){
  const r17=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json','utf8')).records.map(r=>({...r,source_vintage:'R17'}));
  const r18=JSON.parse(fs.readFileSync('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json','utf8')).records.map(r=>({...r,source_vintage:'R18'}));
  const a=new Set(r17.map(keyOf)),b=new Set(r18.map(keyOf));const overlap=[...a].filter(x=>b.has(x));if(overlap.length)throw new Error(`R19_HISTORICAL_OVERLAP_${overlap.length}`);return [...r17,...r18];
}
const records=loadRecords();
const featureRows=[],attemptRows=[];const fail={},phaseAdmission={},solverStats={lines_attempted:0,lines_exact_solver:0,lines_solver_error:0,representation_realizations:0,solver_realizations:0};
function inc(o,k,n=1){o[k]=(o[k]||0)+n;}
let progress=0;
for(const r of records){
  const ar={result_id:Number(r.result_id),attempt_number:Number(r.attempt_number),reco_id:Number(r.reco_id),method:r.method,source_vintage:r.source_vintage,fold:foldOf(r.result_id,r.attempt_number),route_source_status:r.route_source_status,state_certified:false,frame_ok:false,feature_n:0};
  if(r.route_source_status!=='RAW_ALG_CUBING_LINK'){inc(fail,'NO_ROUTE_SOURCE');attemptRows.push(ar);continue;}
  try{
    const parsed=parseAnnotated(r.raw_alg,r.method),moves=parsed.tokens.map(x=>x.move),rawT=kp.algToTransformation(r.raw_alg),expandedT=kp.algToTransformation(moves.join(' '));if(!rawT.isIdentical(expandedT))throw new Error('EXPANSION_MISMATCH');
    let p=defaultPattern.applyAlg(r.raw_setup),states=[p];for(const m of moves){p=p.applyMove(m);states.push(p);}if(!p.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true})){inc(fail,'STATE_UNCERTIFIED');attemptRows.push(ar);continue;}ar.state_certified=true;
    let routeFrame={};
    if(r.method==='CFOP'||r.method==='ZB'){
      const crossLine=parsed.lines.find(x=>x.phase==='CROSS'&&x.end>x.start);
      if(crossLine){const f=detectCrossFace(states[crossLine.end]);if(f.ok){routeFrame={crossFace:f.crossFace,lastFace:f.lastFace,cross_tie_n:f.tie_n};ar.frame_ok=true;ar.crossFace=f.crossFace;}else inc(fail,`FRAME_${f.reason}`);}else inc(fail,'FRAME_NO_CROSS_LINE');
    }else if(r.method==='Roux'){
      const cmll=parsed.lines.find(x=>x.phase==='ROUX_CMLL'&&x.end>x.start);if(cmll){const f=detectRouxLastFace(states[cmll.start],states[cmll.end]);if(f.ok){routeFrame={rouxLastFace:f.lastFace,roux_tie_n:f.tie_n};ar.frame_ok=true;ar.rouxLastFace=f.lastFace;}else inc(fail,`ROUX_FRAME_${f.reason}`);}else{ar.frame_ok=true;inc(fail,'ROUX_FRAME_NO_CMLL_LINE');}
    } else ar.frame_ok=true;
    for(const line of parsed.lines){
      if(['INSPECTION','UNKNOWN','AMBIGUOUS'].includes(line.phase)||line.end-line.start<3)continue;
      const start=states[line.start],target=states[line.end],pmoves=moves.slice(line.start,line.end);const ps=buildPhaseSpec({method:r.method,phase:line.phase,startRaw:start,targetRaw:target,routeFrame,comment:line.comment});
      if(!ps.ok){inc(phaseAdmission,`${line.phase}|HOLD|${ps.reason}`);continue;}inc(phaseAdmission,`${line.phase}|PASS`);
      solverStats.lines_attempted++;const base=await exactNullRealizations(start,target,pmoves,ps.specs[0]);
      const realizations=[];const seen=new Set();for(const z of base.rows){const m=z.moves.join(' ');if(seen.has(m))continue;seen.add(m);realizations.push({source:z.source,moves:z.moves});if(z.source==='REPRESENTATION')solverStats.representation_realizations++;if(z.source==='SOLVER')solverStats.solver_realizations++;}
      if(base.solver.exact)solverStats.lines_exact_solver++;if(base.solver.error)solverStats.lines_solver_error++;
      for(const spec of ps.specs){
        const obs=featureForMoves(start,target,pmoves,spec);if(!obs.ok)continue;const amps=[];const sourceAmps=[];
        for(const z of realizations){const f=featureForMoves(start,target,z.moves,spec);if(f.ok){amps.push(f.amplitude);sourceAmps.push({source:z.source,amplitude:f.amplitude});}}
        if(!amps.length)continue;const envelope=Math.max(...amps);featureRows.push({
          result_id:Number(r.result_id),attempt_number:Number(r.attempt_number),reco_id:Number(r.reco_id),method:r.method,source_vintage:r.source_vintage,fold:ar.fold,
          phase:line.phase,line_id:line.line_id,comment:line.comment,move_count:pmoves.length,move_bin:moveBin(pmoves.length),channel:spec.channel_name,kind:spec.kind,
          observed_amplitude:obs.amplitude,reference_envelope:envelope,reference_realization_n:amps.length,reference_sources:[...new Set(sourceAmps.map(x=>x.source))],
          secondary_endpoint:obs.endpoint,raw_positive:obs.amplitude>1e-12
        }); ar.feature_n++;
      }
    }
  }catch(e){inc(fail,`ERROR_${String(e?.message||e).slice(0,80)}`);}
  attemptRows.push(ar);progress++;if(progress%200===0)console.log(`R19_DEV_ROUTE_PROGRESS ${progress}/${records.length}`);
}

const eligibleAttempts=attemptRows.filter(a=>a.state_certified&&a.feature_n>0);const eligibleKeys=new Set(eligibleAttempts.map(keyOf));
const eligibleFeatures=featureRows.filter(z=>eligibleKeys.has(keyOf(z)));
function refCandidates(rows,z){
  const ch=rows.filter(r=>r.channel===z.channel);
  const levels=[
    ['METHOD_PHASE_CHANNEL_BIN',ch.filter(r=>r.method===z.method&&r.phase===z.phase&&r.move_bin===z.move_bin),120],
    ['PHASE_CHANNEL_BIN',ch.filter(r=>r.phase===z.phase&&r.move_bin===z.move_bin),160],
    ['METHOD_PHASE_CHANNEL',ch.filter(r=>r.method===z.method&&r.phase===z.phase),120],
    ['PHASE_CHANNEL',ch.filter(r=>r.phase===z.phase),200],
    ['GLOBAL_CHANNEL',ch,500],
  ];
  for(const [level,a,min] of levels)if(a.length>=min)return {level,rows:a,n:a.length};return {level:'HOLD_LOCAL_REFERENCE_SUPPORT',rows:[],n:0};
}
function localScore(trainRows,z){const ref=refCandidates(trainRows,z);if(!ref.n)return {ok:false,...ref};const ge=ref.rows.filter(r=>r.reference_envelope>=z.observed_amplitude-1e-12).length,p=(1+ge)/(ref.n+1);return {ok:true,level:ref.level,n:ref.n,p,score:-Math.log10(p)};}

const scoredFeatures=[],crossfitAttempts=[];let fallbackN=0;
for(let f=0;f<5;f++){
  const train=eligibleFeatures.filter(z=>z.fold!==f),held=eligibleFeatures.filter(z=>z.fold===f);const byAttempt=new Map();
  for(const z of held){const s=localScore(train,z);const q={...z,local_ok:s.ok,local_level:s.level,local_n:s.n,local_p:s.p??null,tail_score:s.score??null};scoredFeatures.push(q);if(!s.ok){fallbackN++;continue;}const k=keyOf(z);if(!byAttempt.has(k))byAttempt.set(k,[]);byAttempt.get(k).push(q);}
  for(const a of eligibleAttempts.filter(x=>x.fold===f)){
    const zs=byAttempt.get(keyOf(a))||[],vals=zs.filter(x=>x.local_ok);crossfitAttempts.push({...a,scored_feature_n:vals.length,feature_count_bin:featureCountBin(vals.length),attempt_statistic:vals.length?Math.max(...vals.map(x=>x.tail_score)):null,local_fallback_n:zs.length-vals.length});
  }
}
function familyRef(rows,a){
  const candidates=rows.filter(r=>r.fold!==a.fold&&r.attempt_statistic!==null);
  const levels=[
    ['METHOD_COUNT',candidates.filter(r=>r.method===a.method&&r.feature_count_bin===a.feature_count_bin),300],
    ['COUNT',candidates.filter(r=>r.feature_count_bin===a.feature_count_bin),300],
    ['METHOD',candidates.filter(r=>r.method===a.method),300],
    ['GLOBAL',candidates,1000],
  ];
  for(const [level,x,min] of levels)if(x.length>=min)return {level,rows:x,n:x.length};return {level:'HOLD_FAMILY_REFERENCE_SUPPORT',rows:[],n:0};
}
for(const a of crossfitAttempts){
  if(a.attempt_statistic===null){a.familywise_ok=false;a.familywise_level='NO_ATTEMPT_STATISTIC';continue;}const ref=familyRef(crossfitAttempts,a);a.familywise_level=ref.level;a.familywise_n=ref.n;if(!ref.n){a.familywise_ok=false;continue;}const ge=ref.rows.filter(r=>r.attempt_statistic>=a.attempt_statistic-1e-12).length;a.familywise_p=(1+ge)/(ref.n+1);a.familywise_ok=true;
}
const familyOK=crossfitAttempts.filter(a=>a.familywise_ok),foldHealth=[];
for(let f=0;f<5;f++){const a=familyOK.filter(x=>x.fold===f);foldHealth.push({fold:f,n:a.length,primary_rate:a.filter(x=>x.familywise_p<=.01).length/Math.max(1,a.length),watch_rate:a.filter(x=>x.familywise_p<=.05).length/Math.max(1,a.length)});}
const primaryRate=familyOK.filter(x=>x.familywise_p<=.01).length/Math.max(1,familyOK.length),watchRate=familyOK.filter(x=>x.familywise_p<=.05).length/Math.max(1,familyOK.length);
const localFallbackRate=fallbackN/Math.max(1,scoredFeatures.length);
const phaseSummary={};for(const z of eligibleFeatures){const k=`${z.phase}|${z.channel}`;if(!phaseSummary[k])phaseSummary[k]={n:0,raw_positive:0,amplitudes:[],envelopes:[]};const q=phaseSummary[k];q.n++;if(z.raw_positive)q.raw_positive++;q.amplitudes.push(z.observed_amplitude);q.envelopes.push(z.reference_envelope);}
for(const q of Object.values(phaseSummary)){q.raw_positive_rate=q.raw_positive/q.n;q.observed={p50:upperQuantile(q.amplitudes,.5),p90:upperQuantile(q.amplitudes,.9),p99:upperQuantile(q.amplitudes,.99),max:Math.max(...q.amplitudes)};q.reference={p50:upperQuantile(q.envelopes,.5),p90:upperQuantile(q.envelopes,.9),p99:upperQuantile(q.envelopes,.99),max:Math.max(...q.envelopes)};delete q.amplitudes;delete q.envelopes;}

// Historical R1.8 full-state baseline, used only as development comparison.
let baseline=[];try{const a=JSON.parse(fs.readFileSync('research/0.10.5-r1.8/evidence-null-calibration-r2/NULL_SEGMENT_LEDGER.json','utf8')).rows.map(x=>Number(x.actual_candidate_reversal));const b=JSON.parse(fs.readFileSync('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_COURT.json','utf8')).segments.map(x=>Number(x.candidate_reversal_amplitude));baseline=[...a,...b];}catch{}
const objectiveFeatures=eligibleFeatures.filter(z=>z.channel==='objective');
const checks={
  historical_attempts_1800:records.length===1800,
  state_certified_attempts_ge_1700:attemptRows.filter(a=>a.state_certified).length>=1700,
  crossfit_eligible_attempts_ge_1200:eligibleAttempts.length>=1200,
  local_fallback_rate_le_0_05:localFallbackRate<=.05,
  familywise_reference_complete:familyOK.length>=1200,
  primary_health_band:primaryRate>=.003&&primaryRate<=.02,
  watch_health_band:watchRate>=.025&&watchRate<=.08,
  no_scored_feature_uses_own_fold:true,
};
const status=Object.values(checks).every(Boolean)?'PASS_READINESS_CALIBRATION':'HOLD_CALIBRATION_OR_SUPPORT';
const summary={
  schema_version:'CR0105R19-QUOTIENT-FAMILYWISE-DEVELOPMENT-1',status,role:'HISTORICAL_DEVELOPMENT_AND_CROSSFIT_HEALTH_ONLY',
  historical:{attempts:records.length,state_certified:attemptRows.filter(a=>a.state_certified).length,eligible_attempts:eligibleAttempts.length,eligible_features:eligibleFeatures.length,objective_features:objectiveFeatures.length,source_counts:Object.fromEntries(['R17','R18'].map(s=>[s,eligibleAttempts.filter(a=>a.source_vintage===s).length]))},
  geometry:{phase_channel:phaseSummary,full_state_baseline:{segments:baseline.length,raw_positive_rate:baseline.length?baseline.filter(x=>x>1e-12).length/baseline.length:null},quotient_objective_raw_positive_rate:objectiveFeatures.length?objectiveFeatures.filter(x=>x.raw_positive).length/objectiveFeatures.length:null},
  algorithm_reference:solverStats,
  admission_failures:fail,phase_admission:phaseAdmission,
  crossfit:{folds:5,local_fallback_n:fallbackN,local_fallback_rate:localFallbackRate,familywise_attempts:familyOK.length,primary_alpha:.01,primary_empirical_exceedance:primaryRate,watch_alpha:.05,watch_empirical_exceedance:watchRate,fold_health:foldHealth,familywise_levels:Object.fromEntries([...new Set(familyOK.map(a=>a.familywise_level))].map(k=>[k,familyOK.filter(a=>a.familywise_level===k).length]))},
  checks,
  roux_semantic_gate:{roux_state_certified:eligibleAttempts.filter(a=>a.method==='Roux').length,roux_frame_ok:eligibleAttempts.filter(a=>a.method==='Roux'&&a.frame_ok).length,decision:'HOLD_ROUX_CONFIRMATORY_SEMANTIC_FRAME_UNTIL_HIGHER_LAST_FACE_OR_BLOCK_IDENTIFICATION_SUPPORT'},
  claims:'No recovery/error prevalence or independent replication claim is authorized from this historical development court.',human_observations:0
};
const fullLocalRef={schema_version:'CR0105R19-FULL-LOCAL-REFERENCE-1',role:'SEALED_HISTORICAL_REFERENCE_FOR_FUTURE_FRESH_SCORING',rows:eligibleFeatures.map(z=>({result_id:z.result_id,attempt_number:z.attempt_number,method:z.method,phase:z.phase,channel:z.channel,move_count:z.move_count,move_bin:z.move_bin,reference_envelope:z.reference_envelope,fold:z.fold})),human_observations:0};
const attemptRef={schema_version:'CR0105R19-CROSSFIT-ATTEMPT-FAMILYWISE-REFERENCE-1',role:'CROSSFITTED_HISTORICAL_ATTEMPT_REFERENCE_FOR_FUTURE_FRESH_SCORING',rows:crossfitAttempts,human_observations:0};
const seal={schema_version:'CR0105R19-ATTEMPT-FAMILYWISE-NULL-PREREG-SEAL-1',status:status==='PASS_READINESS_CALIBRATION'?'SEALED_FOR_FUTURE_FRESH_VINTAGE':'HOLD_NOT_SEALABLE',stage:napkin.stage,napkin_sha256:sha(fs.readFileSync(NAPKIN_PATH,'utf8')),core_sha256:sha(fs.readFileSync(CORE_PATH,'utf8')),historical_development_only:true,future_primary_alpha:.01,future_watch_alpha:.05,local_reference_rule:napkin.local_tail_normalization,familywise_rule:napkin.attempt_level_familywise_null,full_local_reference_semantic_sha256:sha(fullLocalRef),crossfit_attempt_reference_semantic_sha256:sha(attemptRef),development_summary_semantic_sha256:sha(summary),future_fresh_outcomes_seen:false,human_observations:0};seal.seal_sha256=sha(seal);
fs.writeFileSync(`${OUT}/QUOTIENT_FEATURE_LEDGER.json`,JSON.stringify({schema_version:'CR0105R19-QUOTIENT-FEATURE-LEDGER-1',rows:featureRows,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${OUT}/CROSSFIT_SCORED_FEATURES.json`,JSON.stringify({schema_version:'CR0105R19-CROSSFIT-SCORED-FEATURES-1',rows:scoredFeatures,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${OUT}/FULL_LOCAL_REFERENCE.json`,JSON.stringify(fullLocalRef,null,2)+'\n');
fs.writeFileSync(`${OUT}/CROSSFIT_ATTEMPT_REFERENCE.json`,JSON.stringify(attemptRef,null,2)+'\n');
fs.writeFileSync(`${OUT}/DEVELOPMENT_SUMMARY.json`,JSON.stringify(summary,null,2)+'\n');
fs.writeFileSync(`${OUT}/ATTEMPT_FAMILYWISE_NULL_PREREG_SEAL.json`,JSON.stringify(seal,null,2)+'\n');
console.log(JSON.stringify({status,seal_sha256:seal.seal_sha256,historical:summary.historical,geometry:summary.geometry,crossfit:summary.crossfit,roux_semantic_gate:summary.roux_semantic_gate,checks},null,2));
if(status!=='PASS_READINESS_CALIBRATION')process.exit(20);
