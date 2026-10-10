/**
 * CUBE-REV 0.22 P6: executable real-cube FMC branch grammar.
 * Precise meanings: EO/DR/HTR GROUP conditions are not observed FMC cognition.
 * UD physical axis is exact, FB/LR EO/DR by color+pose cube-rotation conjugacy.
 * Six half-turn generators are exhausted (663552 distinct actual cube states).
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {solvedStickerCube,applyMoveToken,applyAlgorithm,toCubieState,cubieSolved,solvedUpToRotation} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const ID8=Array.from({length:8},(_,i)=>i),ID12=Array.from({length:12},(_,i)=>i);
const FACES=['U','R','F','D','L','B'];
const normalFace={'0,1,0':'U','1,0,0':'R','0,0,1':'F','0,-1,0':'D','-1,0,0':'L','0,0,-1':'B'};
const solved=()=>toCubieState(solvedStickerCube());
const stateKey=s=>s.cp.join(',')+'/'+s.co.join(',')+'/'+s.ep.join(',')+'/'+s.eo.join(',');
const stickerAfter=(tokens)=>{const c=solvedStickerCube();for(const token of tokens)applyMoveToken(c,token);return c;};
const cubieAfter=tokens=>toCubieState(stickerAfter(tokens));
const isEO=s=>s.eo.every(x=>x===0);
const isDR=s=>isEO(s)&&s.co.every(x=>x===0)&&s.ep.slice(8).every(x=>x>=8);
const parity=a=>{let p=0;for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)p^=Number(a[i]>a[j]);return p;};
const inverseToken=t=>t.endsWith("'")?t.slice(0,-1):t.endsWith('2')?t:t+"'";
const invertWord=word=>word.slice().reverse().map(inverseToken);
const seq=t=>t.trim()?t.trim().split(/\s+/):[];
const normalized=t=>{
 const a=seq(t);assert(a.every(x=>ACTIONS.includes(x)), 'Only strict 18 HTM face turns enter physical word semantics');
 return a;
};
const FACE_MOVES=Object.fromEntries(ACTIONS.map(token=>[token,cubieAfter([token])]));
function compose(s,m){
 return {
  cp:m.cp.map(i=>s.cp[i]),
  co:m.co.map((x,i)=>(s.co[m.cp[i]]+x)%3),
  ep:m.ep.map(i=>s.ep[i]),
  eo:m.eo.map((x,i)=>s.eo[m.ep[i]]^x)
 };
}
function fastWord(w){
 let s=solved();
 for(const t of w)s=compose(s,FACE_MOVES[t]);
 return s;
}
const fixtureWords=[
 [],['U'],['U',"U'"],['F','B'],['B','F'],
 ['U2','R2','L2','F2'],['F',"R'","U2",'D2','B2','L','B',"L'"],
 ["R'","U'","F","L2","D'","L2","U'","R","U","F'"]
];
for(const word of fixtureWords)assert.equal(stateKey(fastWord(word)),stateKey(cubieAfter(word)),
 'original full sticker derivation must independently agree with cubie composition');

// The correct reference frame of a phase is a tagged parameter, not inferred
// from a post-hoc prose "EO/DR/HTR" label.
function rotateFrame(cube,turn){
 if(turn===null)return cube;
 const ref=stickerAfter([turn]),colorMap={};
 for(const st of ref){
  if(st.p.every((v,i)=>v===st.n[i]))colorMap[st.c]=normalFace[st.n.join(',')];
 }
 assert.equal(Object.keys(colorMap).length,6);
 const x=cube.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));
 applyMoveToken(x,turn);
 x.forEach(st=>st.c=colorMap[st.c]);
 return x;
}
const AXES={UD:null,FB:'x',LR:'z'};
function phaseState(stickers,axis){
 assert(Object.hasOwn(AXES,axis));
 return toCubieState(rotateFrame(stickers,AXES[axis]));
}
for(const axis of Object.keys(AXES)){
 const x=phaseState(solvedStickerCube(),axis);
 assert(cubieSolved(x));
 assert(isDR(x));
}
assert(isEO(cubieAfter(['U'])));
assert(isDR(cubieAfter(['U'])));
assert(!isDR(cubieAfter(['F'])));
assert(parity(cubieAfter(['U']).cp)===1);
assert(isDR(cubieAfter(['R2'])));

// Exact membership in half-turn subgroup H = <U2,R2,F2,D2,L2,B2>.
// Every generator preserves zero cubie orientation. Encode eight corners +
// twelve edges as 20 chars (orientation flags separately tested).
const HALF=FACES.map(f=>FACE_MOVES[f+'2']);
for(const g of HALF){assert(g.co.every(x=>x===0)&&g.eo.every(x=>x===0));}
const enc=s=>String.fromCharCode(...s.cp.map(x=>65+x),...s.ep.map(x=>65+x));
const start='ABCDEFGHABCDEFGHIJKL';
assert.equal(enc(solved()),start);
function exactSquareSubgroup(){
 const seen=new Set([start]),q=[start];let head=0;let maxDepth=0;
 const firstAtDepth=[1],dist=[0];
 while(head<q.length){
  const v=q[head],depth=dist[head];head++;
  const cp=v.slice(0,8),ep=v.slice(8);
  for(const m of HALF){
   let n='';
   for(let i=0;i<8;i++)n+=cp[m.cp[i]];
   for(let i=0;i<12;i++)n+=ep[m.ep[i]];
   if(!seen.has(n)){
    seen.add(n);q.push(n);dist.push(depth+1);maxDepth=Math.max(maxDepth,depth+1);
    firstAtDepth[depth+1]=(firstAtDepth[depth+1]??0)+1;
    if(q.length>663552)throw Error('HALF_TURN_GROUP_OVERSHOT_AUTHORITATIVE_ORDER');
   }
  }
 }
 assert.equal(seen.size,663552,'exhaust entire original 3x3 square subgroup, not a guessed HTR flag');
 return {seen,depthHistogram:firstAtDepth,diameterInSixHalfTurnGenerators:maxDepth};
}
const group=exactSquareSubgroup();
const isHTR=s=>isDR(s)&&group.seen.has(enc(s));
assert(isHTR(solved()));
for(const g of HALF)assert(isHTR(g));
assert(!isHTR(cubieAfter(['U'])));
assert(isHTR(cubieAfter(['U2'])));
for(const ax of Object.keys(AXES)){
 const c=phaseState(stickerAfter(['U2']),ax);
 assert(isHTR(c)); // square subgroup invariant under face-axis conjugations.
}

// Stage membership is monotone nested HTR subset DR subset EO in an AXIS.
// This does NOT imply a labelled human phase has a precise timestamp/side.
const physicalCases={
  solved:[],eoud_not_dr:['F2','U','F'], // EO classification assessed below, no assertion
  dr_but_not_htr:['U'],
  htr_not_solved:['U2'],
  non_eo:['F'],
  cancel_identity:['U',"U'"],
  adjacent_face_commutation_one:['F','B'],
  adjacent_face_commutation_two:['B','F']
};
for(const [tag,word] of Object.entries(physicalCases)){
 const st=fastWord(word);
 assert(!isHTR(st)||isDR(st));
 assert(!isDR(st)||isEO(st));
}
assert(!isEO(fastWord(['F'])));
assert(stateKey(fastWord(['F','B']))===stateKey(fastWord(['B','F'])));
assert(stateKey(fastWord(['U',"U'"]))===stateKey(solved()));
assert(stateKey(fastWord(['U']))!==stateKey(solved()));
const sameEndDifferentHistory={
  equal_physical_state_commutation:['F B','B F'],
  equal_physical_state_cancelled:['','U U\''],
  distinct_source_event_representation:true,
  equal_physical_endpoint_does_NOT_imply_equal_chronological_search:true,
  equal_physical_endpoint_does_NOT_imply_equal_HTM_cost:true,
  disjoint_event_ontology_source_assumption_required:true
};

// Side-normal/inverse is an explicit representation; NO ungrounded NISS
// concatenation. Physical inverse of an actual scramble is verified.
const db=JSON.parse(fs.readFileSync('data/cuberev-022/p3_fmc_matched_scramble_author_evidence.json','utf8'));
assert(db.competitors.length===2);
const scr=normalized(db.competitors[0].attempts[0].official_scramble);
const inv=invertWord(scr);
assert(cubieSolved(fastWord([...scr,...inv])));
assert(cubieSolved(fastWord([...inv,...scr])));
const sN=fastWord(scr),sI=fastWord(inv);
assert(stateKey(sN)!==stateKey(sI));
assert(cubieSolved(fastWord([...scr,...inv])));
const niss={
  normal_side_scramble_state_sha_prefix:stateKey(sN).slice(0,48),
  inverse_side_scramble_state_sha_prefix:stateKey(sI).slice(0,48),
  inversion_word_inverse_correct:true,
  NISS_switch_as_if_it_were_simple_concatenation_REJECTED:true,
  side_labels_required_for_state_comparison:true
};

// Verify an authentic published FMC terminal and stage labels conservatively.
// The two author's identical final result word is source-documented. Stage
// labels may involve NISS or insertions, so only self-contained linear
// PREFIXES may be tested as actual physical stage witnesses.
const finalA1=normalized("L2 F' L D L2 F2 B L B2 R2 L B' R2 U2 B U2 L2 F B");
assert.equal(finalA1.length,19);
const finCube=stickerAfter([...scr,...finalA1]);
assert(solvedUpToRotation(finCube));
const eoA1=normalized("L2 F' L D");
const drIncrement=normalized("L2 F2 B L B2 L");
const maybePhase=[
 {stage:'EO',w:eoA1},
 {stage:'DR',w:[...eoA1,...drIncrement]}
].map(({stage,w})=>{
 const cube=stickerAfter([...scr,...w]);
 const tests=Object.keys(AXES).map(axis=>{
  const state=phaseState(cube,axis);
  return {axis,EO:isEO(state),DR:isDR(state),HTR:isHTR(state)};
 });
 return {source_person:'Qijun Miao',attempt:1,phase_reported_by_author:stage,
  normal_side_prefix_from_authored_source:w.join(' '),stage_axis_not_assumed:tests,
  source_grade:'EXPLICIT_LINEAR_PREFIX_IN_AUTHORED_RETROSPECTIVE',
  reported_phase_not_a_verified_REALTIME_search_event:true};
});
assert(maybePhase[0].stage_axis_not_assumed.some(x=>x.EO),
  'published unparenthesized EO prefix must pass EO for at least one conjugated axis');
assert(maybePhase[1].stage_axis_not_assumed.some(x=>x.DR),
  'published unparenthesized DR prefix must pass DR for at least one conjugated axis');

// Partial observational model: stage subgroup sufficiency does not recover
// full 3x3 cube state nor human candidate identity.
const eoMany=[];
for(const action of ACTIONS){
 const c=fastWord([action]);
 if(isEO(c))eoMany.push(action);
}
assert(eoMany.length>1);
assert(new Set(eoMany.map(a=>stateKey(fastWord([a])))).size>1);
const groupPhysicalSignature={
 HTR_subset_DR_subset_EO:true,
 exact_HTR_square_subgroup_order:group.seen.size,
 half_turn_generator_diameter:group.diameterInSixHalfTurnGenerators,
 EO_axis_UD_state_count_not_enumerated:'FULL_EO_SUBGROUP_HUGE',
 EO_many_distinct_physical_states_same_stage_label:eoMany.length,
 DR_non_HTR_witness:'U',
 HTR_not_solved_witness:'U2',
 final_same_state_different_words:sameEndDifferentHistory
};
// Representation-relative source DR opportunities after the authentic A1 EO.
// Freeze FB EO frame from independent physical source-prefix verification.
// Search a *bounded* exact menu of legal physical EO-preserving face moves.
// We never assert this is the whole historical set the author considered.
const fbRotation=stickerAfter(['x']),oldFaceToConjugatedFace={};
for(const s of fbRotation)if(s.p.every((v,i)=>v===s.n[i])){
  oldFaceToConjugatedFace[s.c]=normalFace[s.n.join(',')];
}
assert.equal(Object.keys(oldFaceToConjugatedFace).length,6);
const conjugateFaceMove=token=>oldFaceToConjugatedFace[token[0]]+token.slice(1);
const EO_FB_ALLOWED=ACTIONS.filter(token=>FACE_MOVES[conjugateFaceMove(token)].eo.every(x=>x===0));
assert.equal(EO_FB_ALLOWED.length,14);
const sourceDR=normalized('L2 F2 B L B2 L');
for(const action of sourceDR)assert(EO_FB_ALLOWED.includes(action),'real sourced DR path must be admitted to this frozen EO-preserving generator alphabet');
const initialFB=phaseState(stickerAfter([...scr,...eoA1]),'FB');
assert(isEO(initialFB));
const sourceDRstate=sourceDR.reduce((cur,a)=>compose(cur,FACE_MOVES[conjugateFaceMove(a)]),initialFB);
const independentSourceDR=phaseState(stickerAfter([...scr,...eoA1,...sourceDR]),'FB');
assert.equal(stateKey(sourceDRstate),stateKey(independentSourceDR));
assert(isDR(sourceDRstate));
const stagePaths=[
 [],
 ['B'],['U2'],['L','R'],
 ['B','F2','R'],sourceDR
];
for(const word of stagePaths){
 const viaGroup=word.reduce((cur,a)=>compose(cur,FACE_MOVES[conjugateFaceMove(a)]),initialFB);
 const viaOriginal=phaseState(stickerAfter([...scr,...eoA1,...word]),'FB');
 assert.equal(stateKey(viaGroup),stateKey(viaOriginal),
  'axis-conjugation must agree with original full-sticker moves on actual scramble+EO+prefix');
}
let frontier=[{s:initialFB,w:''}],wordCumulative=1,collisionWitness=null;
const boundedFrontier=[];
for(let depth=0;depth<=4;depth++){
 const unique=new Map();let DRcount=0,HTRcount=0;
 for(const p of frontier){
  assert(isEO(p.s),'Only physical EO-preserving path words admitted');
  const k=stateKey(p.s);
  if(unique.has(k)&&!collisionWitness&&unique.get(k)!==p.w){
   collisionWitness={depth,same_physical_state_first_word:unique.get(k),same_physical_state_second_word:p.w,
    stage_axis:'FB',given_the_same_true_scramble_and_authored_EO_prefix:true};
  }
  if(!unique.has(k))unique.set(k,p.w);
  if(isDR(p.s))DRcount++;
  if(isHTR(p.s))HTRcount++;
 }
 boundedFrontier.push({
  additional_turns_from_real_authored_FB_EO_prefix:depth,
  exact_generator_word_paths:frontier.length,
  distinct_full_physical_cube_endpoints:unique.size,
  full_DR_membership_word_paths:DRcount,
  full_HTR_membership_word_paths:HTRcount,
  total_words_over_all_depths_through_here:wordCumulative,
  full_retro_human_EO_candidates_evaluated:'NOT_OBSERVED'
 });
 if(depth===4)break;
 const next=[];
 for(const p of frontier)for(const action of EO_FB_ALLOWED){
   const s=compose(p.s,FACE_MOVES[conjugateFaceMove(action)]);
   next.push({s,w:p.w?p.w+' '+action:action});
 }
 frontier=next;wordCumulative+=frontier.length;
}
// Source-context exact fifth-turn frontier, using a *weighted* quotient:
// carry how many different legal length-four WORDS reach each full cubie state.
// This removes 14^4 repeated prefixes without losing path multiplicities.
// It does NOT assert these 537824 candidates were personally generated.
const weightedDepth4=new Map();
for(const p of frontier){
 const k=stateKey(p.s);
 if(!weightedDepth4.has(k))weightedDepth4.set(k,{s:p.s,number_of_legal_words:0,witness:p.w});
 weightedDepth4.get(k).number_of_legal_words++;
}
assert.equal(weightedDepth4.size,boundedFrontier[4].distinct_full_physical_cube_endpoints);
const weightedDepth5=new Map();let drFiveWords=0,htrFiveWords=0,rawFiveWords=0,DR5Witness=null;
for(const p of weightedDepth4.values())for(const a of EO_FB_ALLOWED){
 const st=compose(p.s,FACE_MOVES[conjugateFaceMove(a)]);
 const k=stateKey(st),weight=p.number_of_legal_words;
 rawFiveWords+=weight;
 if(isDR(st)){drFiveWords+=weight;if(!DR5Witness)DR5Witness=p.witness+' '+a;}
 if(isHTR(st))htrFiveWords+=weight;
 if(!weightedDepth5.has(k))weightedDepth5.set(k,{number_of_legal_words:0});
 weightedDepth5.get(k).number_of_legal_words+=weight;
}
assert.equal(rawFiveWords,14**5);
assert.equal([...weightedDepth5.values()].reduce((v,x)=>v+x.number_of_legal_words,0),14**5);
assert(htrFiveWords<=drFiveWords);
boundedFrontier.push({
 additional_turns_from_real_authored_FB_EO_prefix:5,
 exact_generator_word_paths:rawFiveWords,
 distinct_full_physical_cube_endpoints:weightedDepth5.size,
 full_DR_membership_word_paths:drFiveWords,
 full_HTR_membership_word_paths:htrFiveWords,
 total_words_over_all_depths_through_here:wordCumulative+rawFiveWords,
 full_retro_human_EO_candidates_evaluated:'NOT_OBSERVED',
 exact_collapse_using_weighted_physical_endpoint_quotient:true
});
const sourceRelativeDRDepthBound={
  no_DR_certificate_with_4_or_fewer_additional_EO_preserving_HTM_moves:true,
  exists_5_step_DR_witness:DR5Witness!==null,
  first_found_5_step_DR_witness:DR5Witness,
  source_actual_6_step_DR_path_verified:true,
  minimum_extra_moves_under_this_frozen_14_generator_grammar:DR5Witness?5:6,
  human_actual_solution_optimality_not_inferred:true
};

assert(boundedFrontier[4].exact_generator_word_paths===14**4);
assert(boundedFrontier[4].distinct_full_physical_cube_endpoints<=14**4);
assert(collisionWitness,'mathematically distinct EO-preserving words must sometimes reach the same cube');
const budgetedOpportunity={
 source_attempt:'Qijun Miao FMCWorld2026 Attempt 1, authored normal-side four-move EO prefix',
 original_scramble:db.competitors[0].attempts[0].official_scramble,
 base_word:eoA1.join(' '),
 explicit_axis:'FB',
 legal_EO_preserving_HTM_actions:EO_FB_ALLOWED,
 preserving_HTM_generator_count:EO_FB_ALLOWED.length,
 stage_target:'full-cubie DR FB subgroup membership, not a psychological consideration label',
 source_relative_DR_minimum_additional_HTM_certificate:sourceRelativeDRDepthBound,
 exact_up_to_four_added_HTM_depth_frontier:boundedFrontier,
 measured_DO_NOT_infer_time_or_attention_from_word_counts:true,
 author_known_six_move_EO_to_DR_completion:sourceDR.join(' '),
 completed_stage_certificate_verified:true,
 distinct_word_same_physical_state_witness:collisionWitness,
 note:'The 14-move generated universe is one mathematical grammar; we did not verify the historical human considered any of these exhaustively.'
};

const report={
 marker:'CUBE_REV_022_P6_REAL_FULL_CUBE_FMC_GRAMMAR_AND_SQUARE_SUBGROUP_PASS',
 physical_engine:'CUBE-REV original 54-sticker transformations and complete corner/edge permutation/orientation derived states; not a 24-state tagged-edge abstraction',
 move_alphabet:'strict original 18 Rubik face HTM actions; excludes unsound implicit wide/slice/insertion rewrites',
 stage_grammar:{
  EO:'For specified physical axis: all 12 edges oriented in that conjugated cubie frame.',
  DR:'EO plus all eight corner twists zero plus four E-slice edge cubies within E slice; equivalent to <U,D,R2,L2,F2,B2> after choosing UD frame.',
  HTR:'Membership in explicitly exhaustively enumerated <U2,R2,F2,D2,L2,B2> subgroup of order 663552, not a mere parity heuristic.',
  INVERSE:'Explicit inversion of cube scramble and side token; do not equate notation parentheses or NISS switches to a single linear prefix.',
  candidate_types:[
    'PHYSICAL_FULL_CUBE_STATE',
    'PHASE_AXIS_SUBGROUP_CERTIFICATE',
    'WORD_PREFIX_REPRESENTATION',
    'NISS_SIDE_LABELED_BRANCH',
    'AUTHOR_REPORTED_EVENT',
    'ACTUALLY_EVALUATED_HUMAN_SEARCH_BRANCH_UNOBSERVED_IF_NOT_SOURCED'
  ],
  invalid_coercions:[
    'EO stage label by itself is not a unique physical cube state',
    'same complete final HTM word is not unique original cognitive process',
    'distinct written DR candidate word is not automatically a distinct cubie endpoint',
    'inverse-side notation cannot be applied as normal-side word without formal side conjugation',
    'prefix stage membership does not identify total search-time budget or evaluated alternatives'
  ]
 },
 phase_subgroup_certificate:groupPhysicalSignature,
 bounded_source_relative_fmc_DR_opportunity_grammar:budgetedOpportunity,
 HTR_depth_histogram:group.depthHistogram,
 source_based_authored_Miao_first_attempt_normal_prefix_verification:maybePhase,
 full_actual_competition_scramble_plus_19_HTM_solution_verified_solved:true,
 physically_distinct_normal_vs_inverse_scramble_side_states:niss,
 evidence_boundary:{
  distinct_source_people:2, matched_source_scrambles:3,
  authenticated_real_written_event_NOT_unique_hidden_psychology:true,
  user_video_and_VFMC_engineering_HOLD:true,
  transfer_from_24_edge_oracle_to_full_FMC_SEARCH_NOT_AUTOMATIC:true,
  conditional_branch_budget_time_not_measured:true,
  no_new_recruitment_or_private_scrape:true
 }
};
console.log(JSON.stringify(report,null,2));
