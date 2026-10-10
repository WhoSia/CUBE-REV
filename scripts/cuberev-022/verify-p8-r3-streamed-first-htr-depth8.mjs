/**
 * CUBE-REV 0.22 P8-R3: source-anchored exact 8-turn first HTR contact through streaming physical quotient.
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
const start=enc(solved);
const groupDist=new Map([[start,0]]), groupParents=new Map(), queue=[start], hist=[1];
let head=0;
while(head<queue.length) {
 const current=queue[head++],d=groupDist.get(current);
 for(const t of HALF){
  const m=FACE[t];let next='';
  for(let i=0;i<8;i++)next+=current[m.cp[i]];
  for(let i=0;i<12;i++)next+=current[8+m.ep[i]];
  if(groupDist.has(next))continue;
  groupDist.set(next,d+1);groupParents.set(next,[current,t]);queue.push(next);
  hist[d+1]=(hist[d+1]??0)+1;
  if(queue.length>663552)throw Error('HTR_SUBGROUP_OVERSHOT');
 }
}
assert.equal(groupDist.size,663552);
assert.equal(hist.length-1,15); // BFS levels are contiguous; no spread over 663552 values
assert.equal(hist.reduce((a,b)=>a+b,0),663552);
function checksum(s){return crypto.createHash('sha256').update(key(s)).digest('hex');}
function htrDistance(s){return dr(s)?groupDist.get(enc(s)):undefined;}
function exactReturnFromHTR(s){
 const path=[];let state=enc(s);
 assert(groupDist.has(state),'HTR state not in exact subgroup');
 while(state!==start){
  const parent=groupParents.get(state);
  assert(parent,'Subgroup BFS parent missing');
  path.push(parent[1]);state=parent[0];
 }
 assert.equal(path.length,groupDist.get(enc(s)),'Shortest HTR suffix does not match BFS certificate');
 let c=s;for(const t of path)c=compose(c,FACE[t]);
 assert.equal(key(c),key(solved),'Actual half-turns must solve canonical cube');
 return path;
}

const scramble=tokenize(ledger.normal_scramble);
const record=ledger.eo_dr_pairs.find(x=>x.id==='riabov_other_3');
assert(record && record.declared_mode==='ASSUMED_CONTIGUOUS_NORMAL_SIDE_FOR_TEST_ONLY');
const prefix=[...tokenize(record.eo_prefix),...tokenize(record.dr_extension)];
const axis='LR',startCube=phaseState(stickerAfter([...scramble,...prefix]),axis);
assert(dr(startCube));
assert(!groupDist.has(enc(startCube)));
const letters=DR.map((_,i)=>String.fromCharCode(65+i));
const fromLetter=Object.fromEntries(letters.map((x,i)=>[x,DR[i]]));
const quarters=new Set(["U","U'","D","D'"]);
const qIdx=DR.flatMap((t,i)=>quarters.has(t)?[i]:[]);
assert.equal(qIdx.length,4);
function stateFromKey(k) {
 assert.equal(k.length,20);
 return {cp:Array.from(k.slice(0,8),x=>x.charCodeAt(0)-65),
 co:Array(8).fill(0),ep:Array.from(k.slice(8),x=>x.charCodeAt(0)-65),
 eo:Array(12).fill(0)};
}
function moveKey(k,move) {
 const m=FACE[move],a=k.slice(0,8),b=k.slice(8);
 let out='';
 for(let i=0;i<8;i++)out+=a[m.cp[i]];
 for(let i=0;i<12;i++)out+=b[m.ep[i]];
 return out;
}
// Backward HTR subgroup is itself a 663552-target set; a shortest last step
// cannot be a half turn, because every half turn is in H. This halves memory
// and cuts the final contact tests from 10*|frontier| to 4*|frontier|.
let front=new Map([[enc(startCube),'']]);
const layers=[{depth:0,unique_full_states:1,HTR_hits:0}];
for(let d=1;d<=7;d++){
 const next=new Map();let contacts=0;
 for(const [key,word] of front)for(let i=0;i<DR.length;i++){
  const nxt=moveKey(key,DR[i]);
  if(!next.has(nxt)) next.set(nxt,word+letters[i]);
 }
 for(const key of next.keys())if(groupDist.has(key))contacts++;
 layers.push({depth:d,unique_full_states:next.size,HTR_hits:contacts});
 front=next;
}
assert.deepEqual(layers.map(x=>x.unique_full_states),[1,10,74,524,3589,23508,146571,883454]);
assert(layers.every(x=>x.HTR_hits===0));
const contactHTR=new Map();let tests=0,returnCostMin=Infinity,best=null;
for(const [key,word] of front){
 for(const i of qIdx){
  const out=moveKey(key,DR[i]);tests++;
  const tail=groupDist.get(out);
  if(tail===undefined)continue;
  if(!contactHTR.has(out))contactHTR.set(out,{word:word+letters[i],HTR_to_solved_half_turns:tail});
  const cost=8+tail;
  if(cost>=returnCostMin)continue;
  returnCostMin=cost;
  best={word:word+letters[i],out,HTR_to_solved_half_turns:tail};
 }
}
assert.equal(tests,4*883454);
let witness=null;
if(best){
 const canonicalMoves=[...best.word].map(x=>fromLetter[x]);
 let s=startCube;for(const t of canonicalMoves)s=compose(s,FACE[t]);
 assert.equal(enc(s),best.out);
 const halfMoves=exactReturnFromHTR(s);
 const actualFromCanonical=t=>MAP[axis].frame_to_original[t[0]]+t.slice(1);
 const realMoves=canonicalMoves.map(actualFromCanonical),realHalf=halfMoves.map(actualFromCanonical);
 const solution=[...prefix,...realMoves,...realHalf];
 assert(solvedUpToRotation(stickerAfter([...scramble,...solution])));
 witness={
  canonical_DR_to_HTR_word:canonicalMoves.join(' '),
  actual_DR_to_HTR_word:realMoves.join(' '),
  actual_HTR_to_solved_word:realHalf.join(' '),
  complete_original_face_word:solution.join(' '),
  authored_prefix_turns:prefix.length,
  DR_to_HTR_turns:canonicalMoves.length,
  HTR_to_solved_half_turns:halfMoves.length,
  whole_solution_HTM:solution.length,
  endpoint_sha256:checksum(s),
  verified_original_full_54_sticker_solution:true
 };
}
const out={
 marker:'CUBE_REV_022_P8_R3_LR_SOURCE_OTHER3_EIGHT_TURN_QUOTIENT_CONTACT_CENSUS',
 source_id:record.id,
 source_parse_status:'CONDITIONAL_ON_CONTIGUOUS_NORMAL_SIDE',
 full_cube_axis:axis,
 valid_declared_DR_state:true,
 stable_7_depth_baseline_exact:layers,
 frozen_DR_10_action_alphabet:DR,
 terminal_quarter_turns_only:qIdx.map(i=>DR[i]),
 justification_for_last_step_pruning:'A half turn is an element of H. Therefore if g*t in H and t in H, g in H. No first arrival to H can finish with a half turn.',
 source_state_full_cubie_sha256:checksum(startCube),
 eighth_layer_full_states_NOT_materialized:true,
 seventh_layer_unique_full_states:front.size,
 quarter_only_eighth_layer_raw_membership_tests:tests,
 eighth_layer_unique_HTR_endpoints_contacted:contactHTR.size,
 strict_exact_minimum_DR_to_HTR:best?8:null,
 DR_to_HTR_minimum_if_no_hit:'AT_LEAST_9',
 optimal_bounded_8_depth_two_phase_from_source:witness,
 bounded_target_HTR_subgroup_exact_elements:groupDist.size,
 untouched_19_turn_source_submission_not_assumed_as_literal_DR_suffix:true,
 no_claim_of_global_FMC_minimality:true,
 source_reconstruction_not_realtime_human_process:true
};
console.log(JSON.stringify(out,null,2));
