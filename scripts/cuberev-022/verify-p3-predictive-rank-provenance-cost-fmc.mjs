/**
 * CUBE-REV 0.22 P3 — exact real-Rubik predictive tests, original-source
 * aliasing, resource-cost policy switches & existing FMC matched-case court.
 * Genuine moves imported from original sticker Rubik oracle, NO new human data.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const moves=urMoveAutomaton();
const N=24,prime=1000003;
assert.equal(moves.length,18);
for(const q of moves)assert.deepEqual([...q].sort((a,b)=>a-b),Array.from({length:N},(_,i)=>i));
function power(a,k){let out=1;for(;k;k=Math.floor(k/2),a=a*a%prime)if(k%2)out=out*a%prime;return out;}
class ExactModRank {
 constructor(){this.basis=new Map();this.witnesses=[];}
 add(bits,meta){
  const v=bits.map(x=>((x%prime)+prime)%prime);
  for(let col=0;col<N;col++){
   if(!v[col])continue;
   const pivot=this.basis.get(col);
   if(pivot){const z=v[col];for(let j=col;j<N;j++)v[j]=(v[j]-z*pivot[j]%prime+prime)%prime;}
   else {
    const inverse=power(v[col],prime-2);
    for(let j=col;j<N;j++)v[j]=v[j]*inverse%prime;
    this.basis.set(col,v);
    this.witnesses.push(meta);
    return true;
   }
  }
  return false;
 }
 get rank(){return this.basis.size;}
}
const full=new ExactModRank(),lastOnly=new ExactModRank();
const allStates=Array.from({length:N},(_,i)=>i);
full.add(Array(N).fill(1),{protocol:'NORMALIZATION',word:[],output:'ANY'});
lastOnly.add(Array(N).fill(1),{protocol:'NORMALIZATION',word:[],output:'ANY'});
const predictionLevels=[{turns:0,all_read_transcript_rank:1,final_read_only_rank:1,all_read_pure_state_class_count:1}];
const signatures=Array(N).fill('');
let frontier=[{word:[],transported:allStates,bits:allStates.map(_=>'')}];
for(let d=1;d<=3;d++){
 const next=[];
 for(const prev of frontier)for(let a=0;a<18;a++){
  const transported=prev.transported.map(s=>moves[a][s]);
  const bits=transported.map((s,i)=>prev.bits[i]+(s&1));
  const word=[...prev.word,ACTIONS[a]];
  const transcripts=[...new Set(bits)].sort();
  for(const pattern of transcripts){
   const row=bits.map(b=>b===pattern?1:0);
   full.add(row,{word,observed_entire_bit_transcript:pattern});
  }
  const patterns=new Set(transported.map(s=>s&1));
  for(const b of patterns){
   const row=transported.map(s=>(s&1)===b?1:0);
   lastOnly.add(row,{word,observed_final_bit:b});
  }
  for(let i=0;i<N;i++)signatures[i]+='|'+bits[i];
  if(d<3)next.push({word,transported,bits});
 }
 const cls=new Set(signatures).size;
 predictionLevels.push({turns:d,all_read_transcript_rank:full.rank,
   final_read_only_rank:lastOnly.rank,all_read_pure_state_class_count:cls});
 frontier=next;
}
assert(predictionLevels[0].all_read_transcript_rank===1);
assert(predictionLevels.every(z=>z.all_read_transcript_rank<=24));
assert(predictionLevels.every(z=>z.final_read_only_rank<=24));
// A rank-24 mod-p witness is also full rank over Q, hence any real-valued
// posterior over the 24 physical edge states is identified from those
// selected controlled future event probabilities at the tested horizon.
// EXACT all-horizons algebraic upper bound for the last-bit-only interface.
// Each real legal edge move has T_w(2p+b) = 2 slot_w(p) + (b XOR flip_w(p)).
// Thus for any fixed word w, final-bit-0 event indicator r_w satisfies
// r_w(2p)+r_w(2p+1)=1 for EACH p. All such rows live in a
// 13-dimensional linear subspace: one common pair sum plus 12 differences.
// Independent actual physical tests reach rank 13 by depth two, certifying
// rank EXACTLY 13 for the ENTIRE infinite family of legal words.
for(let a=0;a<18;a++)for(let slot=0;slot<12;slot++){
 assert.equal((moves[a][2*slot]&1)^(moves[a][2*slot+1]&1),1);
}
assert.equal(predictionLevels[2].final_read_only_rank,13);
for(const level of predictionLevels)assert(level.final_read_only_rank<=13);
const lastBitAnyLengthExactRank=13;
// Mixtures at the two different slots, each with unknown orientation uniformly.
// For EVERY legal action word, final bit is still 1/2 each, because the
// physical moves preserve a XOR with the initial orientation bit.
const mixtures=[
 {tag:'PHYSICAL_SLOT_0_EITHER_FLIP',states:[0,1],weights:[.5,.5]},
 {tag:'PHYSICAL_SLOT_1_EITHER_FLIP',states:[2,3],weights:[.5,.5]}
];
let distinctFullTwoStep=null;
const transcriptDist=(states,word)=>{
 let current=[...states],transcripts=states.map(()=>'');
 for(const a of word){
  current=current.map(s=>moves[a][s]);
  transcripts=transcripts.map((v,i)=>v+(current[i]&1));
 }
 const out={};
 for(const v of transcripts)out[v]=(out[v]??0)+.5;
 return out;
};
for(let a=0;a<18&&!distinctFullTwoStep;a++)for(let b=0;b<18;b++){
 const X=transcriptDist(mixtures[0].states,[a,b]);
 const Y=transcriptDist(mixtures[1].states,[a,b]);
 if(JSON.stringify(Object.entries(X).sort())!==JSON.stringify(Object.entries(Y).sort())){
  distinctFullTwoStep={word:[ACTIONS[a],ACTIONS[b]],first_mixture_bit_history_distribution:X,
   second_mixture_bit_history_distribution:Y};
  break;
 }
}
assert(distinctFullTwoStep);
for(let a=0;a<18;a++)for(let b=0;b<18;b++){
 const v0=mixtures.map(m=>m.states.map(s=>moves[b][moves[a][s]]&1));
 assert(v0.every(pair=>pair[0]!==pair[1]));
}

const rank24Depth=predictionLevels.find(x=>x.all_read_transcript_rank===24)?.turns??null;
const finalRank24Depth=predictionLevels.find(x=>x.final_read_only_rank===24)?.turns??null;
const rankWitnesses=full.witnesses.slice(0,24);
const protocolCount=rankWitnesses.filter(x=>x.word.length).length;
if(rank24Depth!==null)assert.equal(full.rank,24);

// Construct two histories from SAME initial 2-source prior, with same CURRENT
// singleton physical posterior but distinct labels of the original source.
const original=[0,2];
let splitWord=null;
outer:for(let a=0;a<18;a++)for(let b=0;b<18;b++){
 const p=original.map(s=>moves[b][moves[a][s]]&1);
 if(p[0]!==p[1]){splitWord=[a,b];break outer;}
}
assert(splitWord);
const after=original.map(s=>moves[splitWord[1]][moves[splitWord[0]][s]]);
assert.notEqual(after[0]&1,after[1]&1);
function shortestTransport(from,to){
 if(from===to)return [];
 const q=[{s:from,w:[]}],seen=new Set([from]);
 for(let i=0;i<q.length;i++){
  for(let a=0;a<18;a++){
   const t=moves[a][q[i].s];
   if(seen.has(t))continue;
   const word=[...q[i].w,a];
   if(t===to)return word;
   seen.add(t);q.push({s:t,w:word});
  }
 }
 throw Error('REAL_RUBIK_EDGE_TRANSITIVITY_BREAK');
}
const histories=original.map((start,i)=>{
 const word=shortestTransport(after[i],0);
 let cur=after[i];for(const a of word)cur=moves[a][cur];
 assert.equal(cur,0);
 return {
  original_initial_slot:i,
  initial_physical_state:start,
  common_first_two_moves:splitWord.map(a=>ACTIONS[a]),
  read_after_second_move:true,
  distinguishing_second_read_bit:after[i]&1,
  subsequent_silent_moves:word.map(a=>ACTIONS[a]),
  final_physical_edge_state:cur,
  final_physical_posterior:{0:1},
  original_source_label:i
 };
});
assert(histories[0].distinguishing_second_read_bit!==histories[1].distinguishing_second_read_bit);
assert.equal(histories[0].final_physical_edge_state,histories[1].final_physical_edge_state);
assert.notEqual(histories[0].original_source_label,histories[1].original_source_label);

// Exact time-dependent physical decision, SAME initial three-source posterior.
// Both stages are real HTM turns; query after every turn at no extra fee.
const triple=[0,2,6],priors=[1/3,1/3,1/3];
const plansForCosts=(firstCost,secondCost)=>{
 const plans=[];
 for(let a=0;a<18;a++){
  const bits=triple.map(s=>moves[a][s]&1);
  for(const observedBit of [0,1]){
   const ids=triple.map((s,i)=>bits[i]===observedBit?i:-1).filter(i=>i>=0);
   if(ids.length===3){break;}
  }
  const groups=[0,1].map(b=>triple.map((s,i)=>bits[i]===b?i:-1).filter(x=>x>=0));
  if(groups.some(x=>x.length===0)||groups.some(x=>x.length===3))continue;
  if(groups.filter(x=>x.length===2).length!==1)continue;
  const remain=groups.find(x=>x.length===2);
  const post=remain.map(i=>moves[a][triple[i]]);
  const nextCandidates=[];
  for(let b=0;b<18;b++)if((moves[b][post[0]]&1)!==(moves[b][post[1]]&1)){
   nextCandidates.push({second:ACTIONS[b],cost:secondCost(b)});
  }
  if(!nextCandidates.length)continue;
  nextCandidates.sort((x,y)=>x.cost-y.cost||x.second.localeCompare(y.second));
  plans.push({first:ACTIONS[a],firstIdx:a,second:nextCandidates[0].second,
    first_stage_cost:firstCost(a),continuation_probability:2/3,
    expected_cost:firstCost(a)+(2/3)*nextCandidates[0].cost});
 }
 assert(plans.length>0);
 plans.sort((x,y)=>x.expected_cost-y.expected_cost||x.first.localeCompare(y.first));
 return {optimum:plans[0].expected_cost,
   all_optimal_first_moves:plans.filter(x=>Math.abs(x.expected_cost-plans[0].expected_cost)<1e-9).map(x=>x.first),
   winning_example:plans[0],feasible_first_moves:plans.length};
};
const isF=a=>ACTIONS[a]==='F'||ACTIONS[a]==="F'";
const isB=a=>ACTIONS[a]==='B'||ACTIONS[a]==="B'";
const scheduleF=plansForCosts(a=>isF(a)?1:isB(a)?4:10,_=>1);
const scheduleB=plansForCosts(a=>isB(a)?1:isF(a)?4:10,_=>1);
assert(scheduleF.all_optimal_first_moves.every(x=>x==='F'||x==="F'"));
assert(scheduleB.all_optimal_first_moves.every(x=>x==='B'||x==="B'"));
assert(scheduleF.all_optimal_first_moves.length===2);
assert(scheduleB.all_optimal_first_moves.length===2);
assert.equal(scheduleF.feasible_first_moves,scheduleB.feasible_first_moves);
assert(Math.abs(scheduleF.optimum-5/3)<1e-10);
assert(Math.abs(scheduleB.optimum-5/3)<1e-10);

// New matched real historic FMC case evidence, reported-source only.
// Identical three official scrambles 2026 FMC World; NO psychological inference.
const evPath='data/cuberev-022/p3_fmc_matched_scramble_author_evidence.json';
const records=JSON.parse(fs.readFileSync(evPath,'utf8'));
assert.equal(records.schema,'cuberev-022-p3-fmc-matched-scramble-retrospective-v1');
assert.equal(records.competitors.length,2);
const byId=new Map(records.competitors.map(c=>[c.id,c]));
const yr=byId.get('2018RIAB01'),qm=byId.get('2014MIAO02');
assert(yr&&qm);
for(let i=0;i<3;i++){
 assert.equal(yr.attempts[i].attempt,i+1);
 assert.equal(qm.attempts[i].attempt,i+1);
 assert.equal(yr.attempts[i].official_scramble,qm.attempts[i].official_scramble);
 assert.equal(yr.attempts[i].solution_htm,qm.attempts[i].solution_htm);
}
assert.deepEqual(yr.attempts.map(x=>x.solution_htm),[19,19,23]);
assert.deepEqual(qm.attempts.map(x=>x.solution_htm),[19,19,23]);
assert.equal(yr.attempts[2].written_EO_candidates_about,70);
assert.equal(yr.attempts[2].checked_EO_candidates_about,30);
assert(yr.attempts[2].written_EO_candidates_about>yr.attempts[2].checked_EO_candidates_about);
assert(qm.attempts[2].self_report_limited_search_under_result_pressure);
assert(records.controls.no_hidden_choices_imputed&&records.controls.no_retrospective_psychological_causality_claims);
const matched=yr.attempts.map((x,i)=>({attempt:i+1,both_HTM:x.solution_htm,
  identical_scramble_verified_from_both_authors:true,
  first_author_reported_EOs_checked_about:x.checked_EO_candidates_about,
  first_author_EO_written_about:x.written_EO_candidates_about??null,
  second_author_reported_EO_checked:qm.attempts[i].checked_EO_candidates_about??null,
  second_author_process_warrant:qm.attempts[i].author_report_process_kind,
  self_report_not_measured_cognitive_latents:true}));
const receipt={
 marker:'CUBE_REV_022_P3_REAL_PHYSICAL_PREDICTIVE_STATE_AND_FMC_COGNITIVE_BARRIER_COURT_PASS',
 original_sticker_derived_cube:true,
 predictive_linear_tests:{
  state_coordinates:24,
  field_prime:prime,
  max_test_word_depth:3,
  levels:predictionLevels,
  first_depth_full_rank_all_read:rank24Depth,
  first_depth_full_rank_final_only:finalRank24Depth,
  final_bit_only_exact_rank_for_arbitrarily_long_legal_words:lastBitAnyLengthExactRank,
  proof_of_all_horizons_rank13:'Each terminal one-bit experiment has across original opposite-flip source states at any slot a pair of complementary indicators; hence all rows satisfy a shared per-slot pair-sum and span dimension <=13. 13 independent actual legal tests are found at depth 2.',
  exact_mixture_indistinguishability:{
   distinct_physical_mixtures_with_uniform_hidden_flip:mixtures,
   all_legal_words_terminal_bit_distribution_for_each_mixture:{0:0.5,1:0.5},
   full_two_turn_history_separating_witness:distinctFullTwoStep,
   inference:'Final one-bit observations never reveal the physical slot if the initial flip is uniformly unknown, but ordered multi-time correlations can reveal it.'
  },
  independent_test_rows_for_rank_certificate:rankWitnesses,
  sufficient_distribution_identification_if_rank24:'Full mod-prime rank => nonzero integer minor => rank24 over real numbers. Prediction vector of these 24 tests uniquely determines arbitrary distribution on 24 physical states, under frozen known sensor/moves.',
  nonfull_rank_caveat:'Rank below 24 mod-p only certifies a lower rank bound unless rational rank upper bound independently verified.'
 },
 historical_original_source_decoding:{
  prior:'Uniform over two distinct original flip-zero edge slots 0 and 1',
  physical_hypotheses:[0,2],
  both_read_after_same_two_legal_turns:true,
  posterior_becomes_singleton_after_second_observation:true,
  both_end_in_same_physical_singleton_even_with_shared_original_prior:true,
  distinct_original_source_labels_require_history_or_provenance:true,
  histories
 },
 nonstationary_cost_control:{
  same_physical_initial_prior_on_slots:[0,1,3],
  same_prior_weights:[1/3,1/3,1/3],
  horizon:2,
  model:'stage-one named face-turn cost varies exogenously; stage-two any legal face turn cost 1; query after each turn; this is a mathematical schedule not empirical human motor cost',
  cheap_F_schedule:scheduleF,
  cheap_B_schedule:scheduleB,
  disjoint_first_action_sets:true
 },
 fmc_source_graded_match:{
  two_actual_named_authors:2,
  real_attempts:6,
  matched_official_scrambles:3,
  identical_solution_lengths_all_three_attempts:true,
  matched,
  retrospective_coverage_vs_hidden_cognitive_state:'Written-vs-checked pools and self-reported pressure are distinct; identical 19/19/23 outcomes do not identify internal search policy, latent costs or actual subjective beliefs.',
  source_pages:records.competitors.map(x=>x.source_url),
  evidence_grade:'AUTHORED_RETROSPECTIVE_WRITEUPS_NOT_RAW_TIMESTAMPED_ACTION_LOG',
  no_videos_or_new_participants:true
 },
 theorem_scope:'Predictions identify a model-conditioned physical mixture when the finite test family has full rank, but task-relative original-source naming and nonstationary cost policy require provenance/context; actual FMC cognition is not measured by these norms.',
 no_claims:'No universal smaller-than-physical predictive state under any observation model, no optimal full 12-source controller memory size, no human belief posterior identification, no video label'
};
console.log(JSON.stringify(receipt,null,2));
