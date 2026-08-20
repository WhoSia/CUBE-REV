import fs from 'node:fs';
import crypto from 'node:crypto';
import { sha, upperQuantile, mean } from '../0.10.5-r1.9/r19_quotient_core.mjs';

const ROOT=process.env.R111_ROOT||'/tmp/r111';fs.mkdirSync(ROOT,{recursive:true});
const G=JSON.parse(fs.readFileSync(`${ROOT}/ROUX_BLOCK_INTERNAL_GEOMETRY_AUDIT.json`,'utf8'));
const F=JSON.parse(fs.readFileSync(`${ROOT}/ROUX_FEATURE_LEDGER.json`,'utf8')).rows;
const key=r=>`${r.result_id}:${r.attempt_number}`;
const featureBin=n=>n<=4?'1-4':n<=8?'5-8':n<=12?'9-12':'13+';
const bins=['1-4','5-8','9-12','13+'];
function tail(ref,x){const ge=ref.filter(r=>r.observed_amplitude>=x.observed_amplitude-1e-12).length;const p=(1+ge)/(ref.length+1);return {p,score:-Math.log10(p),n:ref.length};}
function localRef(train,z){
  const levels=[
    ['PHASE_CHANNEL_BIN',train.filter(r=>r.phase===z.phase&&r.channel===z.channel&&r.move_bin===z.move_bin),25],
    ['PHASE_CHANNEL',train.filter(r=>r.phase===z.phase&&r.channel===z.channel),40],
    ['CHANNEL',train.filter(r=>r.channel===z.channel),100]
  ];
  for(const [level,rows,min] of levels)if(rows.length>=min)return {level,rows,n:rows.length,required:min};
  return null;
}
function scoreFeatures(target,train){let fallback=0;const out=[];for(const z of target){const r=localRef(train,z);if(!r){fallback++;continue;}const t=tail(r,z);out.push({...z,local_level:r.level,local_n:r.n,local_p:t.p,local_score:t.score});}return {rows:out,fallback};}
function attemptsFromFeatures(rows){const by=new Map();for(const z of rows){const k=key(z);if(!by.has(k))by.set(k,[]);by.get(k).push(z);}return [...by.entries()].map(([k,z])=>({key:k,result_id:z[0].result_id,attempt_number:z[0].attempt_number,reco_id:z[0].reco_id,source:z[0].source,fold:z[0].fold,scored_feature_n:z.length,feature_count_bin:featureBin(z.length),attempt_statistic:Math.max(...z.map(x=>x.local_score))}));}
function familyRef(rows,a,excludeSelf=true){let c=rows.filter(r=>r.attempt_statistic!==null);if(excludeSelf)c=c.filter(r=>r.key!==a.key);const b=c.filter(r=>r.feature_count_bin===a.feature_count_bin);if(b.length>=25)return {level:'FEATURE_COUNT_BIN',rows:b,n:b.length,required:25};if(c.length>=60)return {level:'ROUX_GLOBAL',rows:c,n:c.length,required:60};return null;}
function familyP(ref,a){const ge=ref.rows.filter(r=>r.attempt_statistic>=a.attempt_statistic-1e-12).length;return (1+ge)/(ref.n+1);}
// Leave-one-attempt-out future-scale bank.
let looFallback=0;const looFeatureRows=[];
for(const z of F){const train=F.filter(r=>key(r)!==key(z));const s=scoreFeatures([z],train);looFallback+=s.fallback;looFeatureRows.push(...s.rows);}
const loo=attemptsFromFeatures(looFeatureRows);
let looOk=0,looWatch=0,looPrimary=0;const looLevels={};
const looAdjudicated=loo.map(a=>{const r=familyRef(loo,a,true);if(!r)return {...a,familywise_ok:false};const p=familyP(r,a);looOk++;if(p<=.05)looWatch++;if(p<=.01)looPrimary++;looLevels[r.level]=(looLevels[r.level]||0)+1;return {...a,familywise_ok:true,familywise_level:r.level,familywise_n:r.n,familywise_p:p};});
// Five-fold crossfit bank for transport comparison.
let crossFallback=0;const crossFeatures=[];
for(let f=0;f<5;f++){const target=F.filter(z=>z.fold===f),train=F.filter(z=>z.fold!==f);const s=scoreFeatures(target,train);crossFallback+=s.fallback;crossFeatures.push(...s.rows);}
const cross=attemptsFromFeatures(crossFeatures);
// Fully nested no-outer-test-fold-leak familywise calibration.
const nestedRows=[],outer=[];let nestedFallback=0;
for(let f=0;f<5;f++){
  const testS=scoreFeatures(F.filter(z=>z.fold===f),F.filter(z=>z.fold!==f));nestedFallback+=testS.fallback;const testA=attemptsFromFeatures(testS.rows);
  const refs=[];
  for(let g=0;g<5;g++)if(g!==f){const innerS=scoreFeatures(F.filter(z=>z.fold===g),F.filter(z=>z.fold!==f&&z.fold!==g));nestedFallback+=innerS.fallback;for(const a of attemptsFromFeatures(innerS.rows))refs.push({...a,reference_for_outer_fold:f,inner_fold:g});}
  let ok=0,w=0,p1=0;const levels={};
  for(const a of testA){const r=familyRef(refs,a,false);if(!r){nestedRows.push({...a,outer_fold:f,familywise_ok:false});continue;}const p=familyP(r,a);ok++;if(p<=.05)w++;if(p<=.01)p1++;levels[r.level]=(levels[r.level]||0)+1;nestedRows.push({...a,outer_fold:f,familywise_ok:true,familywise_level:r.level,familywise_n:r.n,familywise_p:p});}
  outer.push({fold:f,test_attempts:testA.length,familywise_ok_n:ok,watch_rate:w/Math.max(1,ok),primary_rate:p1/Math.max(1,ok),levels,reference_attempts:refs.length});
}
const nestedOk=nestedRows.filter(r=>r.familywise_ok),nestedWatch=nestedOk.filter(r=>r.familywise_p<=.05).length/Math.max(1,nestedOk.length),nestedPrimary=nestedOk.filter(r=>r.familywise_p<=.01).length/Math.max(1,nestedOk.length);
// Crossfit versus LOO future-scale transport.
const cm=new Map(cross.map(a=>[a.key,a])),pairs=[];for(const a of loo){const b=cm.get(a.key);if(b)pairs.push({key:a.key,fold:a.fold,feature_count_bin:a.feature_count_bin,crossfit_stat:b.attempt_statistic,loo_stat:a.attempt_statistic,abs_diff:Math.abs(b.attempt_statistic-a.attempt_statistic)});}
function corr(rows){if(rows.length<2)return null;const x=rows.map(r=>r.crossfit_stat),y=rows.map(r=>r.loo_stat),mx=mean(x),my=mean(y);let n=0,dx=0,dy=0;for(let i=0;i<x.length;i++){n+=(x[i]-mx)*(y[i]-my);dx+=(x[i]-mx)**2;dy+=(y[i]-my)**2;}return dx&&dy?n/Math.sqrt(dx*dy):null;}
const diffs=pairs.map(r=>r.abs_diff),pearson=corr(pairs),p99=diffs.length?upperQuantile(diffs,.99):null;
// Explicit finite-sample resolution court for a future genuinely fresh attempt.
const fullBank=loo.filter(a=>a.attempt_statistic!==null),globalN=fullBank.length;
const futurePaths={};let primaryResolution=true;
for(const b of bins){const n=fullBank.filter(a=>a.feature_count_bin===b).length;let level,refN;if(n>=25){level='FEATURE_COUNT_BIN';refN=n;}else if(globalN>=60){level='ROUX_GLOBAL';refN=globalN;}else{level='UNSUPPORTED';refN=0;}const minP=refN?1/(refN+1):null,ok=refN>=99;futurePaths[b]={level,reference_n:refN,minimum_add_one_p:minP,primary_1pct_resolvable:ok};if(!ok)primaryResolution=false;}
const localFallbackRate=looFallback/Math.max(1,F.length);
const engineeringChecks={
  familywise_attempts_ge_75:looOk>=75,
  nested_familywise_attempts_ge_75:nestedOk.length>=75,
  local_fallback_rate_le_0_10:localFallbackRate<=.10,
  nested_watch_health:nestedWatch>=.015&&nestedWatch<=.12,
  transport_pairs_ge_75:pairs.length>=75,
  crossfit_loo_pearson_ge_0_90:pearson!==null&&pearson>=.90,
  crossfit_loo_abs_diff_p99_le_0_75:p99!==null&&p99<=.75,
  nested_outer_fold_excluded_from_local_and_family_reference:true,
  roux_only_features:F.every(z=>z.method==='Roux')
};
const engineeringPass=Object.values(engineeringChecks).every(Boolean);
const framePass=G.status==='PASS_ROUX_BLOCK_INTERNAL_FRAME_GEOMETRY';
const futureAuthority=framePass&&engineeringPass&&primaryResolution;
let status;if(futureAuthority)status='PASS_ROUX_FUTURE_SCORE_AUTHORITY';else if(framePass&&engineeringPass&&!primaryResolution)status='PASS_ROUX_NULL_FOUNDRY_HOLD_PRIMARY_RESOLUTION';else status='HOLD_ROUX_NULL_FOUNDRY';
const audit={schema_version:'CR0105R111-ROUX-METHOD-SPECIFIC-NULL-FOUNDRY-1',status,geometry_status:G.status,counts:{features:F.length,loo_attempts:loo.length,loo_familywise_ok:looOk,crossfit_attempts:cross.length,nested_familywise_ok:nestedOk.length,transport_pairs:pairs.length},local_reference:{loo_fallback_n:looFallback,loo_fallback_rate:localFallbackRate,crossfit_fallback_n:crossFallback,nested_fallback_events:nestedFallback},loo_pseudofresh:{primary_alpha:.01,primary_rate:looPrimary/Math.max(1,looOk),watch_alpha:.05,watch_rate:looWatch/Math.max(1,looOk),levels:looLevels},nested_no_test_fold_leak:{primary_alpha:.01,primary_rate:nestedPrimary,watch_alpha:.05,watch_rate:nestedWatch,outer_folds:outer},transport:{pearson_crossfit_vs_loo:pearson,abs_difference:{p50:diffs.length?upperQuantile(diffs,.5):null,p90:diffs.length?upperQuantile(diffs,.9):null,p99,max:diffs.length?Math.max(...diffs):null}},finite_sample_primary_resolution:{global_bank_n:globalN,required_reference_n:99,paths:futurePaths,pass:primaryResolution},engineering_checks:engineeringChecks,engineering_pass:engineeringPass,frame_geometry_pass:framePass,future_roux_scoring_authority:futureAuthority,fresh_outcomes_seen:false,historical_role:'DEVELOPMENT_AND_CALIBRATION_ONLY',human_observations:0};
audit.semantic_sha256=sha(audit);
const seal={schema_version:'CR0105R111-ROUX-FUTURE-AUTHORITY-SEAL-1',status:futureAuthority?'RELEASED_FOR_LATER_GENUINELY_FRESH_ROUX':'HOLD_ROUX_FUTURE_AUTHORITY',geometry_semantic_sha256:G.semantic_sha256,null_foundry_semantic_sha256:audit.semantic_sha256,engineering_pass:engineeringPass,primary_1pct_resolution_pass:primaryResolution,future_roux_scoring_authority:futureAuthority,fresh_network_read_in_r111:false,fresh_scoring_in_r111:false,layered_cfop_zb_authority_modified:false,human_observations:0};seal.seal_sha256=sha(seal);
fs.writeFileSync(`${ROOT}/ROUX_NULL_FOUNDRY_AUDIT.json`,JSON.stringify(audit,null,2)+'\n');
fs.writeFileSync(`${ROOT}/ROUX_LOO_ATTEMPT_BANK.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-LOO-ATTEMPT-BANK-1',rows:looAdjudicated,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${ROOT}/ROUX_CROSSFIT_ATTEMPT_BANK.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-CROSSFIT-ATTEMPT-BANK-1',rows:cross,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${ROOT}/ROUX_NESTED_FAMILYWISE_ROWS.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-NESTED-FAMILYWISE-ROWS-1',rows:nestedRows,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${ROOT}/ROUX_TRANSPORT_PAIRS.json`,JSON.stringify({schema_version:'CR0105R111-ROUX-TRANSPORT-PAIRS-1',rows:pairs,human_observations:0},null,2)+'\n');
fs.writeFileSync(`${ROOT}/ROUX_FUTURE_AUTHORITY_SEAL.json`,JSON.stringify(seal,null,2)+'\n');
console.log(JSON.stringify({status,geometry_status:G.status,engineering_pass:engineeringPass,primary_resolution_pass:primaryResolution,future_authority:futureAuthority,nested_watch:nestedWatch,transport_pearson:pearson,transport_p99:p99,loo_attempts:loo.length,nested_attempts:nestedOk.length,future_paths:futurePaths,seal:seal.seal_sha256},null,2));
