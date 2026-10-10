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
const HALF='U2 R2 F2 D2 L2 B2'.split(' ');
const DR='U U2 U\u0027 D D2 D\u0027 R2 L2 F2 B2'.split(' ');
assert.equal(DR.length,10);
for(const t of DR)assert(dr(compose(solved,FACE[t])));
for(const a of Object.keys(ROT))assert.equal(key(phaseState(stickerAfter([]),a)),key(solved));
for(const a of Object.keys(ROT))for(const t of ACTIONS){
 const f=MAP[a].original_to_frame[t[0]]+t.slice(1);
 assert.equal(key(phaseState(stickerAfter([t]),a)),key(FACE[f]),'axis conjugacy check '+a+'/'+t);
}

assert.equal(ACTIONS.length,18);
const acts=ACTIONS,move=acts.map(x=>FACE[x]),names=acts.map(x=>x[0]),
 opposite={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
const chars=acts.map((_,i)=>String.fromCharCode(65+i)),inverse={};
for(let i=0;i<acts.length;i++){
 const t=acts[i],s=t.endsWith("'")?t[0]:t.endsWith('2')?t:t[0]+"'";
 inverse[chars[i]]=chars[acts.indexOf(s)];
 assert(inverse[chars[i]]);
}
function encode(s){
 return String.fromCharCode(...s.cp.map(x=>65+x),...s.co.map(x=>65+x),
 ...s.ep.map(x=>65+x),...s.eo.map(x=>65+x));
}
function advance(k,m){
 const v=new Array(40);
 for(let i=0;i<8;i++){
  v[i]=k.charCodeAt(m.cp[i]);v[8+i]=65+(k.charCodeAt(8+m.cp[i])-65+m.co[i])%3;
 }
 for(let i=0;i<12;i++){
  v[16+i]=k.charCodeAt(16+m.ep[i]);
  v[28+i]=65+((k.charCodeAt(28+m.ep[i])-65)^m.eo[i]);
 }
 return String.fromCharCode(...v);
}
function decodeWord(s){return Array.from(s,x=>acts[x.charCodeAt(0)-65]);}
function invertWord(s){return Array.from(s).reverse().map(x=>inverse[x]).join('');}
function adjacentNormalized(word){
 const result=[],e=x=>x.endsWith('2')?2:x.endsWith("'")?3:1;
 for(const x of word){
  const p=result.at(-1);
  if(!p||p[0]!==x[0]){result.push(x);continue;}
  const r=(e(p)+e(x))%4;result.pop();
  if(r)result.push(x[0]+(r===1?'':r===2?'2':"'"));
 }
 return result;
}
const OPPOSITE_CANONICAL=true;
function bfs(source,maxDepth,name){
 const visited=new Map([[source,'']]);
 let frontier=[source],hist=[1],transitions=0;
 for(let depth=1;depth<=maxDepth;depth++){
  const next=[];
  for(const key of frontier){
   const w=visited.get(key);
   const last=w.length?names[w.charCodeAt(w.length-1)-65]:null;
   for(let a=0;a<18;a++){
    const face=names[a];
    if(last!==null&&(face===last||(OPPOSITE_CANONICAL&&opposite[last]===face&&face<last)))continue;
    transitions++;
    const n=advance(key,move[a]);
    if(visited.has(n))continue;
    visited.set(n,w+chars[a]);next.push(n);
   }
  }
  hist.push(next.length);frontier=next;
 }
 return {visited,frontier,hist,transitions,name};
}
const root=encode(solved),G=bfs(root,5,'reverse_from_solved_18_face_htm');
assert(G.hist[0]===1);
assert.equal(G.hist.reduce((a,b)=>a+b,0),G.visited.size);
assert(G.hist[1]===18);
function inspect(source,side,label) {
 let best=null,intersectionChecks=0;
 for(const [key,fw] of side.visited){
  const bw=G.visited.get(key);
  intersectionChecks++;
  if(bw===undefined)continue;
  const total=fw.length+bw.length;
  if(!best||total<best.length){
   best={length:total,forward:fw,backward:bw,
    continuationChars:fw+invertWord(bw)};
  }
 }
 return {best,intersectionChecks};
}

const scrape=tokenize(ledger.normal_scramble);
const T=JSON.parse(fs.readFileSync('data/cuberev-023/p1_certified_matched_tie_DR_witnesses.json','utf8'));
assert.equal(T.schema,'cuberev-023-p1-physically-certified-two-action-matched-tie-witness-v1');
assert.equal(T.pairs.length,2);
const expectedWords=['D B2',"D' F2"];
assert.deepEqual(T.pairs.map(x=>x.word),expectedWords);
const rows=[];
for(const pair of T.pairs){
 assert.equal(pair.arms.length,2);
 const word=tokenize(pair.word);
 const actualSynthetic=word.map(t=>MAP.FB.frame_to_original[t[0]]+t.slice(1));
 for(const arm of pair.arms){
  const authored=ledger.eo_dr_pairs.find(x=>x.id===arm.id);
  assert(authored&&authored.declared_mode==='CONTIGUOUS_NORMAL_SIDE_PREFIX');
  const written=[...tokenize(authored.eo_prefix),...tokenize(authored.dr_extension)];
  const physical=stickerAfter([...scrape,...written,...actualSynthetic]),state=toCubieState(physical);
  assert(dr(phaseState(physical,'FB')));
  const oldRestricted=tokenize(arm.suffix);
  assert.equal(oldRestricted.length,arm.exact);
  const oldSolution=[...written,...actualSynthetic,...oldRestricted];
  assert(solvedUpToRotation(stickerAfter([...scrape,...oldSolution])),'P1 certified sourced literal+synthetic+restricted suffix must solve original cube');
  const front=bfs(encode(state),5,'source_and_synthetic_'+arm.id+'_'+pair.word);
  assert.deepEqual(front.hist,G.hist);
  const scanned=inspect(null,front,arm.id);
  const best=scanned.best;
  let minimum=null,word18=null,certificate=null;
  if(best){
   minimum=best.length;
   assert(minimum<=10,'G radius five plus source radius five must never exceed ten');
   word18=decodeWord(best.continuationChars);
   assert(solvedUpToRotation(stickerAfter([...scrape,...written,...actualSynthetic,...word18])));
   certificate='EXACT_FULL_18_MITM_RADIUS_5_PLUS_RADIUS_5';
  }else{
   assert.equal(arm.exact,11,'Only main DR11 can be closed as exact11 by MITM exclusion <=10');
   minimum=11;word18=oldRestricted;
   certificate='FULL_18_RADIUS10_EXCLUSION_PLUS_P1_ORIGINAL_STICKER_REPLAY_11_UPPER';
  }
  assert(minimum<=arm.exact);
  const joint=[...written,...actualSynthetic,...word18];
  const normalized=adjacentNormalized(joint);
  assert(solvedUpToRotation(stickerAfter([...scrape,...normalized])));
  const entry={matched_synthetic_canonical_FB_move:pair.word,source_id:arm.id,
   human_source_literal_prefix_HTM:written.length,
   source_grade:'AUTHORED_RETROSPECTIVE_PLUS_MODEL_GENERATED_NOT_HUMAN_OBSERVED',
   synthetic_actions_original_face_word:actualSynthetic.join(' '),
   restricted_DR_proven_exact_suffix:arm.exact,
   exact_all18_post_synthetic_suffix:minimum,
   all18_complete_full_cube_distance_warrant:certificate,
   real_post_authored_prefix_full_cube_state_SHA256:crypto.createHash('sha256').update(key(state)).digest('hex'),
   goal_radius5_state_count:G.visited.size,source_radius5_state_count:front.visited.size,
   all18_complete_witness_original_face_word:word18.join(' '),
   full_original_scramble_solution_raw_word:joint.join(' '),
   raw_authored_prefix_plus_two_synthetic_plus_exact_solve_HTM:joint.length,
   normalized_full_solution_HTM:normalized.length,
   normalized_word_preserves_full_literal_authored_prefix:written.every((x,i)=>normalized[i]===x),
   physically_solves_original_54_sticker_scramble:true};
  rows.push(entry);
 }
}
const pairs=T.pairs.map(p=>{
 const a=rows.filter(x=>x.matched_synthetic_canonical_FB_move===p.word);
 assert.equal(a.length,2);
 return {matched_intervention:p.word,
  exact_all18_continuation_main:a[0].exact_all18_post_synthetic_suffix,
  exact_all18_continuation_alt:a[1].exact_all18_post_synthetic_suffix,
  main_stage_raw_completion_total:a[0].raw_authored_prefix_plus_two_synthetic_plus_exact_solve_HTM,
  alt_stage_raw_completion_total:a[1].raw_authored_prefix_plus_two_synthetic_plus_exact_solve_HTM,
  exact_all18_stage_raw_cost_gap_alt_minus_main:a[1].raw_authored_prefix_plus_two_synthetic_plus_exact_solve_HTM-a[0].raw_authored_prefix_plus_two_synthetic_plus_exact_solve_HTM,
  original_10_action_DR_grammar_tie_proven:true};
});
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P1_FULL_18_HTM_TIE_FALSIFICATION_ON_TWO_SOURCE_MATCHED_DR_WITNESSES',
 original_physical_scramble:ledger.normal_scramble,
 all18_goal_ball_layer_histogram:G.hist,
 source_state_and_human_word_count:rows.length,
 exact_18_HTM_shortest_continuation_proven_for_all:true,
 different_human_authored_alternatives_only_main_and_alt_miao:true,
 P1_two_DR_preserving_matched_ties_rechecked_under_all18:2,
 actual_all18_tie_count:pairs.filter(x=>x.exact_all18_stage_raw_cost_gap_alt_minus_main===0).length,
 actual_all18_advantage_count:pairs.filter(x=>x.exact_all18_stage_raw_cost_gap_alt_minus_main>0).length,
 invalidated_DR_only_tie_under_all18_count:pairs.filter(x=>x.exact_all18_stage_raw_cost_gap_alt_minus_main!==0).length,
 all18_pair_adjudications:pairs,
 entire_original_54_sticker_source_specific_witnesses:rows,
 human_process_choice_untested:true,
 no_global_FMC_prefix_free_optimality_claim:true
},null,2));
