import fs from 'node:fs';
import { sha, upperQuantile, mean } from '../0.10.5-r1.9/r19_quotient_core.mjs';

const OUT=process.env.R110_LOCAL_ROOT||'/tmp/r110local';fs.mkdirSync(OUT,{recursive:true});
const NAPKIN=JSON.parse(fs.readFileSync('research/0.10.5-r1.10/NAPKIN_INTENT_AND_PREREGISTRATION.json','utf8'));
const ALLF=JSON.parse(fs.readFileSync('research/0.10.5-r1.9/evidence-familywise-development/QUOTIENT_FEATURE_LEDGER.json','utf8')).rows;
const ALLA=JSON.parse(fs.readFileSync('research/0.10.5-r1.9/evidence-familywise-development/CROSSFIT_ATTEMPT_REFERENCE.json','utf8')).rows.filter(x=>x.attempt_statistic!==null);
const METHODS=new Set(['CFOP','ZB']);
const F=ALLF.filter(x=>METHODS.has(x.method));
const A=ALLA.filter(x=>METHODS.has(x.method));
function key(r){return `${r.result_id}:${r.attempt_number}`;}
function bin(n){return n<=8?'1-8':n<=12?'9-12':n<=16?'13-16':'17+';}
function pearson(rows,a='crossfit_stat',b='loo_stat'){
  if(rows.length<2)return null;const x=rows.map(r=>r[a]),y=rows.map(r=>r[b]),mx=mean(x),my=mean(y);let num=0,dx=0,dy=0;
  for(let i=0;i<x.length;i++){num+=(x[i]-mx)*(y[i]-my);dx+=(x[i]-mx)**2;dy+=(y[i]-my)**2;}return dx&&dy?num/Math.sqrt(dx*dy):null;
}
function localReference(rows,z){
  const ch=rows.filter(r=>r.channel===z.channel);
  const levels=[
    ['METHOD_PHASE_CHANNEL_BIN',ch.filter(r=>r.method===z.method&&r.phase===z.phase&&r.move_bin===z.move_bin),120],
    ['PHASE_CHANNEL_BIN',ch.filter(r=>r.phase===z.phase&&r.move_bin===z.move_bin),160],
    ['METHOD_PHASE_CHANNEL',ch.filter(r=>r.method===z.method&&r.phase===z.phase),120],
    ['PHASE_CHANNEL',ch.filter(r=>r.phase===z.phase),200],
    ['LAYERED_GLOBAL_CHANNEL',ch,500],
  ];
  for(const [level,x,min] of levels)if(x.length>=min)return {level,rows:x,n:x.length,min};return null;
}
function localScore(rows,z,excludeOwn=false){
  const ref0=localReference(rows,z);if(!ref0)return null;
  const ref=excludeOwn?ref0.rows.filter(r=>key(r)!==key(z)):ref0.rows;
  if(ref.length<ref0.min)return null;
  const ge=ref.filter(r=>r.reference_envelope>=z.observed_amplitude-1e-12).length,p=(1+ge)/(ref.length+1);
  return {p,score:-Math.log10(p),level:ref0.level,n:ref.length};
}
function scoreAttemptRows(train,held,excludeOwn=false){
  const by=new Map();let fallback=0,scored=0;
  for(const z of held){const s=localScore(train,z,excludeOwn);if(!s){fallback++;continue;}scored++;const k=key(z);if(!by.has(k))by.set(k,[]);by.get(k).push(s.score);}
  return {by,fallback,scored};
}
function familyRef(rows,a,binField='feature_count_bin'){
  const candidates=rows.filter(r=>r.attempt_statistic!==null);
  const b=a[binField];
  const levels=[
    ['METHOD_COUNT',candidates.filter(r=>r.method===a.method&&r[binField]===b),300],
    ['COUNT',candidates.filter(r=>r[binField]===b),300],
    ['METHOD',candidates.filter(r=>r.method===a.method),300],
    ['LAYERED_GLOBAL',candidates,1000],
  ];
  for(const [level,x,min] of levels)if(x.length>=min)return {level,rows:x,n:x.length,min};return null;
}

// LOO full-history bank: future-score scale by construction.
const looScore=scoreAttemptRows(F,F,true);const loo=[];
for(const a of A){const v=looScore.by.get(key(a))||[];loo.push({...a,loo_feature_n:v.length,loo_feature_count_bin:bin(v.length),attempt_statistic:v.length?Math.max(...v):null});}
const looOk=loo.filter(x=>x.attempt_statistic!==null);
let looP01=0,looP05=0,looFamilyOk=0;const looLevels={};
for(const a of looOk){const candidates=looOk.filter(r=>key(r)!==key(a));const proxy={...a,feature_count_bin:a.loo_feature_count_bin};const ref=familyRef(candidates,proxy,'feature_count_bin');if(!ref)continue;const ge=ref.rows.filter(r=>r.attempt_statistic>=a.attempt_statistic-1e-12).length,p=(1+ge)/(ref.n+1);a.loo_familywise_level=ref.level;a.loo_familywise_n=ref.n;a.loo_familywise_p=p;looLevels[ref.level]=(looLevels[ref.level]||0)+1;looFamilyOk++;if(p<=.01)looP01++;if(p<=.05)looP05++;}
const looPrimary=looP01/Math.max(1,looFamilyOk),looWatch=looP05/Math.max(1,looFamilyOk);

// Fivefold family-isolated attempt scores for scale transport.
function scoreFold(targetFold,excluded){
  const train=F.filter(z=>!excluded.has(z.fold)),held=F.filter(z=>z.fold===targetFold);const s=scoreAttemptRows(train,held,false);const rows=A.filter(a=>a.fold===targetFold).map(a=>{const v=s.by.get(key(a))||[];return {...a,feature_count_bin:bin(v.length),scored_feature_n:v.length,attempt_statistic:v.length?Math.max(...v):null};});return {...s,rows};
}
const fivefold=[];let fivefoldFallback=0;for(let f=0;f<5;f++){const s=scoreFold(f,new Set([f]));fivefoldFallback+=s.fallback;fivefold.push(...s.rows);}
const looMap=new Map(looOk.map(r=>[key(r),r]));const transport=[];
for(const c of fivefold){const l=looMap.get(key(c));if(c.attempt_statistic===null||!l)continue;transport.push({key:key(c),method:c.method,fold:c.fold,feature_count_bin:c.feature_count_bin,crossfit_stat:c.attempt_statistic,loo_stat:l.attempt_statistic,abs_diff:Math.abs(c.attempt_statistic-l.attempt_statistic)});}
const corr=pearson(transport),diffs=transport.map(x=>x.abs_diff),p99=upperQuantile(diffs,.99);

// Nested no-outer-test-fold-leak calibration, family-isolated.
const nestedRows=[],outer=[];let nestedFallback=0;
for(let f=0;f<5;f++){
  const test=scoreFold(f,new Set([f]));nestedFallback+=test.fallback;
  const family=[];
  for(let g=0;g<5;g++)if(g!==f){const s=scoreFold(g,new Set([f,g]));nestedFallback+=s.fallback;family.push(...s.rows.map(r=>({...r,reference_for_outer_fold:f,inner_fold:g})));}
  let ok=0,p01=0,p05=0;const levels={};
  for(const a of test.rows){if(a.attempt_statistic===null){nestedRows.push({...a,outer_fold:f,familywise_ok:false});continue;}const ref=familyRef(family,a);if(!ref){nestedRows.push({...a,outer_fold:f,familywise_ok:false,familywise_level:'HOLD_FAMILY_REFERENCE_SUPPORT'});continue;}const ge=ref.rows.filter(r=>r.attempt_statistic>=a.attempt_statistic-1e-12).length,p=(1+ge)/(ref.n+1);ok++;if(p<=.01)p01++;if(p<=.05)p05++;levels[ref.level]=(levels[ref.level]||0)+1;nestedRows.push({...a,outer_fold:f,familywise_ok:true,familywise_level:ref.level,familywise_n:ref.n,familywise_p:p});}
  outer.push({fold:f,n:test.rows.length,familywise_ok_n:ok,primary_rate:p01/Math.max(1,ok),watch_rate:p05/Math.max(1,ok),levels,family_reference_attempts:family.filter(r=>r.attempt_statistic!==null).length});
}
const nestedOk=nestedRows.filter(r=>r.familywise_ok),nestedPrimary=nestedOk.filter(r=>r.familywise_p<=.01).length/Math.max(1,nestedOk.length),nestedWatch=nestedOk.filter(r=>r.familywise_p<=.05).length/Math.max(1,nestedOk.length);
const methods=Object.fromEntries([...METHODS].map(m=>[m,{attempts:A.filter(x=>x.method===m).length,features:F.filter(x=>x.method===m).length,transport_correlation:pearson(transport.filter(x=>x.method===m))}]));
const checks={
  napkin_frozen:NAPKIN.frozen_before_r110_execution===true,
  no_roux_in_layered_features:F.every(x=>METHODS.has(x.method)),
  no_roux_in_layered_attempts:A.every(x=>METHODS.has(x.method)),
  layered_attempts_ge_1200:A.length>=1200,
  loo_familywise_attempts_ge_1200:looFamilyOk>=1200,
  loo_local_fallback_rate_le_0_05:looScore.fallback/Math.max(1,F.length)<=.05,
  loo_primary_health:looPrimary>=.003&&looPrimary<=.02,
  loo_watch_health:looWatch>=.025&&looWatch<=.08,
  nested_familywise_attempts_ge_1200:nestedOk.length>=1200,
  nested_primary_health:nestedPrimary>=.003&&nestedPrimary<=.02,
  nested_watch_health:nestedWatch>=.025&&nestedWatch<=.08,
  transport_pair_n_ge_1200:transport.length>=1200,
  crossfit_loo_pearson_ge_0_95:corr!==null&&corr>=.95,
  crossfit_loo_abs_diff_p99_le_0_50:p99!==null&&p99<=.50,
};
const status=Object.values(checks).every(Boolean)?'PASS_LAYERED_FUTURE_SCORE_TRANSPORT':'HOLD_LAYERED_FUTURE_SCORE_TRANSPORT';
const bank={schema_version:'CR0105R110-LAYERED-LOO-ATTEMPT-BANK-1',status:'HISTORICAL_CALIBRATION_BANK',method_family:'LAYERED',methods:['CFOP','ZB'],future_role:'FROZEN_REFERENCE_ONLY_IF_R110_TRANSPORT_PASS',rows:looOk,human_observations:0};
const result={schema_version:'CR0105R110-METHOD-STRATIFIED-TRANSPORT-1',status,method_family:'LAYERED',methods:['CFOP','ZB'],r19_metric_reused:true,r19_roux_excluded:true,counts:{features:F.length,attempts:A.length,loo_familywise_attempts:looFamilyOk,nested_familywise_attempts:nestedOk.length,transport_pairs:transport.length},method_diagnostics:methods,loo_pseudofresh:{primary_alpha:.01,primary_rate:looPrimary,watch_alpha:.05,watch_rate:looWatch,levels:looLevels,local_fallback_n:looScore.fallback,local_fallback_rate:looScore.fallback/Math.max(1,F.length)},nested_no_test_fold_leak:{primary_rate:nestedPrimary,watch_rate:nestedWatch,outer_folds:outer,total_local_fallback_events:nestedFallback},transport:{pearson_crossfit_vs_loo:corr,abs_difference:{p50:upperQuantile(diffs,.5),p90:upperQuantile(diffs,.9),p99,max:diffs.length?Math.max(...diffs):null}},checks,future_scoring_rule:'If and only if this artifact PASSes and a later authority seal releases it: score a genuinely fresh CFOP/ZB attempt against the full sealed LAYERED local reference, take the attempt maximum, and compute an add-one upper-tail familywise p against the frozen LAYERED LOO attempt-statistic bank using the highest supported within-LAYERED conditioning level.',fresh_outcomes_seen:false,human_observations:0};
const seal={schema_version:'CR0105R110-LAYERED-TRANSPORT-SEAL-1',status:status==='PASS_LAYERED_FUTURE_SCORE_TRANSPORT'?'SEALABLE_LAYERED_FUTURE_SCORER':'HOLD_NOT_SEALABLE',napkin_sha256:sha(fs.readFileSync('research/0.10.5-r1.10/NAPKIN_INTENT_AND_PREREGISTRATION.json','utf8')),r19_feature_ledger_sha256:sha(fs.readFileSync('research/0.10.5-r1.9/evidence-familywise-development/QUOTIENT_FEATURE_LEDGER.json','utf8')),method_family:'LAYERED',methods:['CFOP','ZB'],metric_changed:false,roux_reference_contamination:false,loo_bank_semantic_sha256:sha(bank),transport_result_semantic_sha256:sha(result),future_fresh_outcomes_seen:false,human_observations:0};seal.seal_sha256=sha(seal);
fs.writeFileSync(`${OUT}/LAYERED_LOO_ATTEMPT_BANK.json`,JSON.stringify(bank,null,2)+'\n');
fs.writeFileSync(`${OUT}/METHOD_STRATIFIED_TRANSPORT.json`,JSON.stringify(result,null,2)+'\n');
fs.writeFileSync(`${OUT}/LAYERED_TRANSPORT_SEAL.json`,JSON.stringify(seal,null,2)+'\n');
console.log(JSON.stringify({status,seal:seal.seal_sha256,counts:result.counts,loo_pseudofresh:result.loo_pseudofresh,nested:result.nested_no_test_fold_leak,transport:result.transport,checks},null,2));
