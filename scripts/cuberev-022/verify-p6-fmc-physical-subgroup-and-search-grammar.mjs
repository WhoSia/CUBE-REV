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
