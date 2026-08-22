import fs from 'node:fs';
import { sha } from './r19_quotient_core.mjs';

const OUT=process.env.R19_NESTED_ROOT||'/tmp/r19nested';fs.mkdirSync(OUT,{recursive:true});
const FEATURES_PATH='research/0.10.5-r1.9/evidence-familywise-development/QUOTIENT_FEATURE_LEDGER.json';
const ATTEMPT_PATH='research/0.10.5-r1.9/evidence-familywise-development/CROSSFIT_ATTEMPT_REFERENCE.json';
const OLD_SEAL_PATH='research/0.10.5-r1.9/evidence-familywise-development/ATTEMPT_FAMILYWISE_NULL_PREREG_SEAL.json';
const FULL_LOCAL_PATH='research/0.10.5-r1.9/evidence-familywise-development/FULL_LOCAL_REFERENCE.json';
const NAPKIN_PATH='research/0.10.5-r1.9/NAPKIN_INTENT_AND_PREREGISTRATION.json';
const features=JSON.parse(fs.readFileSync(FEATURES_PATH,'utf8')).rows;
const attempts0=JSON.parse(fs.readFileSync(ATTEMPT_PATH,'utf8')).rows;
const oldSeal=JSON.parse(fs.readFileSync(OLD_SEAL_PATH,'utf8'));
const napkin=JSON.parse(fs.readFileSync(NAPKIN_PATH,'utf8'));
function keyOf(r){return `${r.result_id}:${r.attempt_number}`;}
function featureCountBin(n){return n<=8?'1-8':n<=12?'9-12':n<=16?'13-16':'17+';}
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
function localScore(trainRows,z){const ref=refCandidates(trainRows,z);if(!ref.n)return null;const ge=ref.rows.filter(r=>r.reference_envelope>=z.observed_amplitude-1e-12).length,p=(1+ge)/(ref.n+1);return {p,score:-Math.log10(p),level:ref.level,n:ref.n};}
function scoreAttemptSet(targetFold,trainExcludedFolds){
  const train=features.filter(z=>!trainExcludedFolds.has(z.fold));
  const held=features.filter(z=>z.fold===targetFold),by=new Map();let fallback=0;
  for(const z of held){const s=localScore(train,z);if(!s){fallback++;continue;}const k=keyOf(z);if(!by.has(k))by.set(k,[]);by.get(k).push(s.score);}
  const base=attempts0.filter(a=>a.fold===targetFold&&a.feature_n>0);return {fallback,rows:base.map(a=>{const v=by.get(keyOf(a))||[];return {...a,feature_count_bin:featureCountBin(v.length),scored_feature_n:v.length,attempt_statistic:v.length?Math.max(...v):null};})};
}
function familyRef(rows,a){
  const candidates=rows.filter(r=>r.attempt_statistic!==null);
  const levels=[
    ['METHOD_COUNT',candidates.filter(r=>r.method===a.method&&r.feature_count_bin===a.feature_count_bin),300],
    ['COUNT',candidates.filter(r=>r.feature_count_bin===a.feature_count_bin),300],
    ['METHOD',candidates.filter(r=>r.method===a.method),300],
    ['GLOBAL',candidates,1000],
  ];
  for(const [level,x,min] of levels)if(x.length>=min)return {level,rows:x,n:x.length};return {level:'HOLD_FAMILY_REFERENCE_SUPPORT',rows:[],n:0};
}
const nestedRows=[],outerSummary=[];let totalLocalFallback=0,minFamilyN=Infinity;
for(let f=0;f<5;f++){
  // Test fold f is scored against all other folds.
  const test=scoreAttemptSet(f,new Set([f]));totalLocalFallback+=test.fallback;
  // Familywise reference scores are constructed without any feature from test fold f.
  const familyRows=[];
  for(let g=0;g<5;g++)if(g!==f){const refScore=scoreAttemptSet(g,new Set([f,g]));totalLocalFallback+=refScore.fallback;for(const r of refScore.rows)familyRows.push({...r,reference_for_outer_fold:f,inner_holdout_fold:g});}
  let ok=0,p01=0,p05=0;const levels={};
  for(const a of test.rows){if(a.attempt_statistic===null){nestedRows.push({...a,outer_fold:f,familywise_ok:false});continue;}const ref=familyRef(familyRows,a);minFamilyN=Math.min(minFamilyN,ref.n||Infinity);if(!ref.n){nestedRows.push({...a,outer_fold:f,familywise_ok:false,familywise_level:ref.level});continue;}const ge=ref.rows.filter(r=>r.attempt_statistic>=a.attempt_statistic-1e-12).length,p=(1+ge)/(ref.n+1);levels[ref.level]=(levels[ref.level]||0)+1;ok++;if(p<=.01)p01++;if(p<=.05)p05++;nestedRows.push({...a,outer_fold:f,familywise_ok:true,familywise_level:ref.level,familywise_n:ref.n,familywise_p:p});}
  outerSummary.push({fold:f,n:test.rows.length,familywise_ok_n:ok,primary_rate:p01/Math.max(1,ok),watch_rate:p05/Math.max(1,ok),familywise_levels:levels,family_reference_attempts:familyRows.filter(r=>r.attempt_statistic!==null).length});
}
const okRows=nestedRows.filter(r=>r.familywise_ok),primary=okRows.filter(r=>r.familywise_p<=.01).length/Math.max(1,okRows.length),watch=okRows.filter(r=>r.familywise_p<=.05).length/Math.max(1,okRows.length);
const checks={nested_familywise_attempts_ge_1200:okRows.length>=1200,primary_health_band:primary>=.003&&primary<=.02,watch_health_band:watch>=.025&&watch<=.08,min_family_reference_n_ge_1000:minFamilyN>=1000,outer_test_fold_excluded_from_local_and_family_reference:true,future_fresh_outcomes_seen_false:oldSeal.future_fresh_outcomes_seen===false};
const status=Object.values(checks).every(Boolean)?'PASS_NESTED_NO_LEAK_READINESS':'HOLD_NESTED_CALIBRATION';
const audit={schema_version:'CR0105R19-NESTED-NO-LEAK-FAMILYWISE-AUDIT-1',status,role:'HISTORICAL_CALIBRATION_HEALTH_WITH_OUTER_TEST_FOLD_EXCLUDED_FROM_ALL_REFERENCE_CONSTRUCTION',old_seal_sha256:oldSeal.seal_sha256,nested_attempts:okRows.length,primary_alpha:.01,primary_empirical_exceedance:primary,watch_alpha:.05,watch_empirical_exceedance:watch,min_family_reference_n:minFamilyN,total_local_fallback_events:totalLocalFallback,outer_folds:outerSummary,checks,dependency_rule:'For outer test fold f, test local reference uses folds != f. Every familywise-reference attempt in inner fold g is itself scored using only folds != f and != g. Thus no feature from outer test fold f can affect either its local score or the familywise reference scores against which it is compared.',human_observations:0};
const seal={schema_version:'CR0105R19-ATTEMPT-FAMILYWISE-NULL-PREREG-SEAL-2',status:status==='PASS_NESTED_NO_LEAK_READINESS'?'SEALED_FOR_FUTURE_FRESH_VINTAGE_R2_NO_TEST_FOLD_LEAK':'HOLD_NOT_SEALABLE',supersedes_seal_sha256:oldSeal.seal_sha256,supersession_reason:'RAVEL found indirect outer-fold influence in the R1 crossfit health court: scores in other folds could have used the target fold as local training data. R2 validates calibration with the entire outer test fold excluded from local and familywise-reference score construction. No fresh-vintage outcomes had been read.',napkin_sha256:sha(fs.readFileSync(NAPKIN_PATH,'utf8')),full_local_reference_file_sha256:sha(fs.readFileSync(FULL_LOCAL_PATH,'utf8')),historical_crossfit_attempt_reference_file_sha256:sha(fs.readFileSync(ATTEMPT_PATH,'utf8')),nested_audit_semantic_sha256:sha(audit),future_scoring_rule:oldSeal.familywise_rule,future_primary_alpha:.01,future_watch_alpha:.05,future_fresh_outcomes_seen:false,human_observations:0};seal.seal_sha256=sha(seal);
fs.writeFileSync(`${OUT}/NESTED_NO_LEAK_ATTEMPT_ROWS.json`,JSON.stringify({schema_version:'CR0105R19-NESTED-NO-LEAK-ATTEMPT-ROWS-1',rows:nestedRows,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${OUT}/NESTED_NO_LEAK_AUDIT.json`,JSON.stringify(audit,null,2)+'\n');
fs.writeFileSync(`${OUT}/ATTEMPT_FAMILYWISE_NULL_PREREG_SEAL_R2.json`,JSON.stringify(seal,null,2)+'\n');
console.log(JSON.stringify({status,old_seal:oldSeal.seal_sha256,new_seal:seal.seal_sha256,nested_attempts:okRows.length,primary_empirical_exceedance:primary,watch_empirical_exceedance:watch,min_family_reference_n:minFamilyN,outer_folds:outerSummary,checks},null,2));
if(status!=='PASS_NESTED_NO_LEAK_READINESS')process.exit(20);
