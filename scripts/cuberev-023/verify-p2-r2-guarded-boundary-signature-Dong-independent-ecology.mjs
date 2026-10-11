/**
 * CUBE-REV 0.22 0.23 P1: falsify matched two-turn DR tie under full 18 legal HTM solved geodesics.
 * This is exact finite physical search, not a reconstruction of human thought.
 * Assumption: fixed physical DR axis, DR-preserving 10-face-turn alphabet,
 * then exact HTR Cayley BFS. Query only 4 non-HTR quarter turns in last layer.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {solvedStickerCube, applyMoveToken, toCubieState, solvedUpToRotation} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const ledger=JSON.parse(fs.readFileSync('data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json','utf8'));
assert.equal(ledger.schema,'cuberev-022-p7-fmc-authored-physical-candidate-ledger-v1');
const tokenize=s=>{const a=s.trim().split(/\s+/).filter(Boolean);assert(a.every(t=>ACTIONS.includes(t)));return a;};
const stickerAfter=word=>{const x=solvedStickerCube();for(const t of word)applyMoveToken(x,t);return x;};
const cubieAfter=w=>toCubieState(stickerAfter(w));
const key=s=>s.cp.join(',')+'/'+s.co.join(',')+'/'+s.ep.join(',')+'/'+s.eo.join(',');
const enc=s=>String.fromCharCode(...s.cp.map(x=>65+x),...s.ep.map(x=>65+x));
const solved=cubieAfter([]);
const FACE=Object.fromEntries(ACTIONS.map(t=>[t,cubieAfter([t])]));
const compose=(s,m)=>({
 cp:m.cp.map(i=>s.cp[i]),
 co:m.co.map((x,i)=>(s.co[m.cp[i]]+x)%3),
 ep:m.ep.map(i=>s.ep[i]),
 eo:m.eo.map((x,i)=>s.eo[m.ep[i]]^x)
});
const normal={'0,1,0':'U','1,0,0':'R','0,0,1':'F','0,-1,0':'D','-1,0,0':'L','0,0,-1':'B'};
const ROT={UD:null,FB:'x',LR:'z'};
function frameMap(rot) {
 if(!rot)return {original_to_frame:Object.fromEntries('URFDLB'.split('').map(x=>[x,x])),frame_to_original:Object.fromEntries('URFDLB'.split('').map(x=>[x,x]))};
 const c=stickerAfter([rot]), oldToFrame={};
 for(const s of c)if(s.p.every((v,i)=>v===s.n[i])) oldToFrame[s.c]=normal[s.n.join(',')];
 assert.equal(Object.keys(oldToFrame).length,6);
 return {original_to_frame:oldToFrame,frame_to_original:Object.fromEntries(Object.entries(oldToFrame).map(([k,v])=>[v,k]))};
}
const MAP=Object.fromEntries(Object.keys(ROT).map(a=>[a,frameMap(ROT[a])]));
function phaseState(originalStickers,axis) {
 const rot=ROT[axis];assert(Object.hasOwn(ROT,axis));
 if(!rot)return toCubieState(originalStickers);
 const x=originalStickers.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));
 applyMoveToken(x,rot);for(const s of x)s.c=MAP[axis].original_to_frame[s.c];
 return toCubieState(x);
}
const eo=s=>s.eo.every(v=>v===0);
const dr=s=>eo(s)&&s.co.every(v=>v===0)&&s.ep.slice(8).every(v=>v>=8);

const P=JSON.parse(fs.readFileSync('data/cuberev-023/p2_r2_guarded_signature_independent_source_prereg.json','utf8'));
const W=JSON.parse(fs.readFileSync('data/cuberev-023/p2_r2_frozen_all_eight_full18_optimal_suffix_words.json','utf8'));
assert.equal(P.schema,'cuberev-023-p2-r2-guarded-two-token-predictor-v1');
assert.equal(W.schema,'cuberev-023-p2-r2-frozen-P2R1-eight-exact-geodesic-suffixes-v1');
const turnPower=t=>t.endsWith('2')?2:t.endsWith("'")?3:1;
const mk=(f,p)=>f+(p===1?'':p===2?'2':p===3?"'":'');
const inverse=t=>t.endsWith('2')?t:t.endsWith("'")?t[0]:t[0]+"'";
const invWord=word=>word.slice().reverse().map(inverse);
function reduceWithTags(parts){
 const stack=[],events=[];
 for(const part of parts){
  for(let j=0;j<part.moves.length;j++){
   const t=part.moves[j],prior=stack.at(-1);
   if(!prior||prior.move[0]!==t[0]){stack.push({move:t,origins:[{kind:part.grade,index:j} ]});continue;}
   stack.pop();
   const power=(turnPower(prior.move)+turnPower(t))%4,after=power?mk(t[0],power):null;
   events.push({before:[prior.move,t],after,save:after?1:2,provenance:[...new Set([...prior.origins.map(x=>x.kind),part.grade])]});
   if(after)stack.push({move:after,origins:[...prior.origins,{kind:part.grade,index:j}]});
  }
 }
 return {stack,events,word:stack.map(x=>x.move),saved:events.reduce((s,x)=>s+x.save,0)};
}
function audit(A,I,S,needGeodesic){
 const a=tokenize(A),i=tokenize(I),s=tokenize(S);
 const parts=[{grade:'AUTHORED_HUMAN_SOURCE',moves:a},{grade:'SYNTHETIC_INTERVENTION',moves:i},{grade:'COMPUTED_SUFFIX',moves:s}];
 const exact=reduceWithTags(parts);
 const initial=reduceWithTags(parts.slice(0,2));
 const firstTwo=reduceWithTags([{grade:'AUTHORED_HUMAN_SOURCE',moves:a},{grade:'SYNTHETIC_INTERVENTION',moves:i},{grade:'COMPUTED_SUFFIX',moves:s.slice(0,2)}]);
 const boundarySavedAtFirstTwo=(a.length+i.length+Math.min(s.length,2))-firstTwo.word.length;
 // Only if top token originates in second suffix move, that token (if internally reduced
 // shortest S with no same-face adjacency) cannot merge with the third suffix token,
 // so the prefix boundary has become protected by a fully reduced suffix barrier.
 const tail=firstTwo.stack.at(-1);
 const guard=tail&&tail.origins.some(z=>z.kind==='COMPUTED_SUFFIX'&&z.index===1);
 const geodesicReduced=s.every((t,j)=>!j||s[j-1][0]!==t[0]);
 if(needGeodesic)assert(geodesicReduced,'Actual shortest physical path contains a mergeable same-face adjacent pair');
 // A shortest HTM suffix cannot contain adjacent same-face turns.
 // Its first surviving frontier suffix token is thus a permanent stack barrier:
 // the next suffix turn is on a different face, so later source-boundary rewrites cease.
 // Record the MINIMUM number of suffix tokens needed before this is a theorem.
 let earliestSealingPrefix=null,earliestSealedSavings=null;
 if(geodesicReduced){
  for(let k=1;k<=s.length;k++){
   const partial=reduceWithTags([
    {grade:'AUTHORED_HUMAN_SOURCE',moves:a},
    {grade:'SYNTHETIC_INTERVENTION',moves:i},
    {grade:'COMPUTED_SUFFIX',moves:s.slice(0,k)}
   ]);
   const top=partial.stack.at(-1);
   if(top&&top.origins.some(x=>x.kind==='COMPUTED_SUFFIX'&&x.index===k-1)){
    earliestSealingPrefix=k;
    earliestSealedSavings=a.length+i.length+k-partial.word.length;
    assert.equal(earliestSealedSavings,exact.saved,'Source-tail barrier local theorem falsified');
    break;
   }
  }
  if(earliestSealingPrefix===null){
   earliestSealingPrefix=s.length;earliestSealedSavings=exact.saved;
  }
 }
 const call=(guard&&geodesicReduced)?'EXACT_SEALED_BY_SECOND_SUFFIX_TOKEN':'ABSTAIN_AUTHOR_INTERFACE_MAY_EXPOSE';
 if(call.startsWith('EXACT'))assert.equal(boundarySavedAtFirstTwo,exact.saved,'Guarded local prediction falsified');
 return {actual_raw_word:parts.flatMap(x=>x.moves).join(' '),
  actual_whole_reduced_word:exact.word.join(' '),raw_actions:a.length+i.length+s.length,
  final_reduced_actions:exact.word.length,actual_adjacent_saved_actions:exact.saved,
  suffix_first_two:s.slice(0,2).join(' '),
  early_two_token_saved:boundarySavedAtFirstTwo,
  predictor_claim:call,
  guaranteed_exact_value:call.startsWith('EXACT')?boundarySavedAtFirstTwo:null,
  exact_minimal_boundary_opportunity_sealing_horizon_HTM:earliestSealingPrefix,
  predicted_entire_savings_from_first_sealed_suffix_prefix:earliestSealedSavings,
  all_saved_boundary_events:exact.events,
  author_full_literal_prefix_preserved:exact.word.slice(0,a.length).every((t,j)=>t===a[j]),
  full_suffix_internally_adjacent_reduced:geodesicReduced};
}
const data=[];
for(const row of W.rows){
 const author=ledger.eo_dr_pairs.find(x=>x.id===row.source_id);
 assert(author&&author.declared_mode==='CONTIGUOUS_NORMAL_SIDE_PREFIX');
 const a=author.eo_prefix+' '+author.dr_extension;
 const i=row.synthetic_original_face_word;
 assert.equal(row.all_certified_optimal_suffixes.length,Number(row.full_r1_shortest_word_total));
 for(const w of row.all_certified_optimal_suffixes){
  const probe=audit(a,i,w.word,true);
  assert.equal(probe.actual_adjacent_saved_actions,w.boundary_savings_HTM);
  assert.equal(probe.final_reduced_actions,w.normalized_final_word_length);
  assert.equal(tokenize(w.word).length,row.exact_18HTM_shortest_suffix_length);
  assert(probe.author_full_literal_prefix_preserved);
  assert(solvedUpToRotation(stickerAfter([...tokenize(ledger.normal_scramble),...tokenize(probe.actual_whole_reduced_word)])));
  data.push({source_id:row.source_id,intervention:row.synthetic_FBDR_actions,shortest_suffix:w.word,...probe,
    physically_original_54_sticker_replayed:true,source_grade:'ACTUAL_HUMAN_SOURCE_PLUS_SYNTHETIC_AND_CERTIFIED_EXACT_SUFFIX'});
 }
}
assert.equal(data.length,8);
const exact=data.filter(x=>x.predictor_claim.startsWith('EXACT'));
const abstain=data.filter(x=>x.predictor_claim.startsWith('ABSTAIN'));
assert.equal(exact.length+abstain.length,8);
const sealingHorizonCensus=Object.fromEntries([...new Set(data.map(x=>x.exact_minimal_boundary_opportunity_sealing_horizon_HTM))].sort((a,b)=>a-b).map(k=>[String(k),data.filter(x=>x.exact_minimal_boundary_opportunity_sealing_horizon_HTM===k).length]));
assert.deepEqual(sealingHorizonCensus,{'1':2,'2':2,'3':4});
assert(data.every(x=>x.predicted_entire_savings_from_first_sealed_suffix_prefix===x.actual_adjacent_saved_actions));
const t=P.independent_source;
const src=tokenize(t.source_EO+' '+t.source_DR),submission=tokenize(t.submitted_full_22),scramble=tokenize(t.scramble);
assert.equal(src.length,10);
assert.equal(submission.length,22);
assert.deepEqual(submission.slice(0,10),src,'New independent human author reconstructed EO+DR prefix must match their published solution');
assert(solvedUpToRotation(stickerAfter([...scramble,...submission])),'Independent Dong public submitted FMC solution did NOT solve exact original scramble');
const axes=Object.keys(ROT).filter(a=>dr(phaseState(stickerAfter([...scramble,...src]),a)));
assert(axes.length>0,'Independent Dong source prefix not valid DR in any real physical axis: CROSS_ECOLOGY_HOLD');
const T=submission.slice(src.length);
assert.equal(T.length,12);
const baseAudit=reduceWithTags([{grade:'AUTHORED_HUMAN_SOURCE',moves:src},{grade:'AUTHORED_HUMAN_SUBMISSION_SUFFIX',moves:T}]);
assert.equal(baseAudit.word.length,22);
assert.equal(baseAudit.saved,0);
assert(baseAudit.word.every((x,i)=>x===submission[i]));
const originalSolved=key(cubieAfter([...scramble,...submission]));
const allInterventions=[];
for(const x of ACTIONS)for(const y of ACTIONS){
 const I=[x,y],S=[...invWord(I),...T];
 const test=audit(src.join(' '),I.join(' '),S.join(' '),false);
 const whole=tokenize(test.actual_whole_reduced_word);
 assert.equal(test.final_reduced_actions,22);
 assert.deepEqual(whole,submission,'Legal synthetic inverse pairs must cancel back to actual original human submitted solution');
 assert(solvedUpToRotation(stickerAfter([...scramble,...tokenize(test.actual_raw_word)])));
 assert(solvedUpToRotation(stickerAfter([...scramble,...whole])));
 assert.equal(key(cubieAfter([...scramble,...whole])),originalSolved);
 allInterventions.push({I:I.join(' '),prefixFirstTwo:test.suffix_first_two,raw:test.raw_actions,normalized:test.final_reduced_actions,save:test.actual_adjacent_saved_actions,predictor:test.predictor_claim});
}
assert.equal(allInterventions.length,324);
assert(allInterventions.every(x=>x.raw===26&&x.normalized===22&&x.save===4));
const classifier=[
 ...new Set(allInterventions.map(x=>x.predictor))
];
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P2_R2_GUARDED_TWO_TOKEN_PREDICTOR_INDEPENDENT_DONG_SOURCE',
 registered_before_outcome:P.schema,
 external_source_url:t.original_reconstruction_url,
 original_independent_scramble:t.scramble,
 independent_author:t.author,
 independent_original_prefix10_is_literal_subword_of_actual22:true,
 independent_original_submitted_FMC_solution_verified:true,
 independent_full_cube_DR_axes:axes,
 source_backup_NISS_parentheses_not_falsely_parsed:true,
 P2R1_shortest_actual_full18_word_count:data.length,
 two_token_exact_safe_claim_count:exact.length,
 two_token_guarded_abstention_count:abstain.length,
 two_token_exact_prediction_mistakes:0,
 exact_physical_source_boundary_sealing_horizon_census:sealingHorizonCensus,
 all_eight_actual_HTM_geodesic_suffixes_sealed_by_at_most_three_tokens:true,
 earliest_sealing_prefix_was_measured_from_each_original_authored_source_and_synthetic_intervention:true,
 all_eight_original_full_sticker_checks:true,
 independent_original_face_synthetic_inverse_pair_count:allInterventions.length,
 independent_real_original_scramble_full_cube_replays_verified:true,
 all_324_synthetic_distinct_human_observations:false,
 all_324_are_geodesic_suffixes:false,
 alternate_source_raw_word_26_reduces_to_original_human22_in_all324:true,
 independent_synthetic_guard_claim_types:classifier,
 author_stage_preservation_original_reported_solution:true,
 human_decision_process_inference_NOT_IDENTIFIED:true,
 P2R1_predicted_cases:data,
 independent_Dong_negative_control:{
  source: t.original_reconstruction_url,
  human_recorded_EO_DR:src.join(' '),
  exact_human_submitted_solution:submission.join(' '),
  verified_DR_axes:axes,
  actual_human_continuation:T.join(' '),
  exact_original_submitted_solution_HTM:22,
  synthetic_reversible_insertions_tested:allInterventions.length,
  first_eight_counterfactuals:allInterventions.slice(0,8)
 }
},null,2));
