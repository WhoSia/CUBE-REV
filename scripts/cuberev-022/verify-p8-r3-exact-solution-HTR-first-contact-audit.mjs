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


const source=JSON.parse(fs.readFileSync('data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json','utf8'));
assert.equal(source.schema,'cuberev-022-p8-r3-verified-physical-phase2-source-prefix-fixtures-v1');
assert.equal(source.rows.length,5);
const scramble=tokenize(ledger.normal_scramble),rows=[];
for(const p of source.rows){
 const c=ledger.eo_dr_pairs.find(x=>x.id===p.id);assert(c);
 const authored=[...tokenize(c.eo_prefix),...tokenize(c.dr_extension)];
 const physical=tokenize(p.actual_phase2_word),canonical=tokenize(p.canonical_phase2_word);
 assert.equal(canonical.length,p.exact_minimum_DR_to_solved);
 assert.equal(physical.length,canonical.length);
 const original=stickerAfter([...scramble,...authored]);
 const axis=p.axis;
 let current=phaseState(original,axis);
 assert(dr(current));
 assert.equal(checksum(current),p.source_DR_endpoint_SHA256);
 let exactEarly=groupDist.has(enc(current))?[0]:[];
 for(let i=0;i<canonical.length;i++){
  current=compose(current,FACE[canonical[i]]);
  assert(dr(current),'continuation leaves the fixed source DR group');
  const originalStickers=stickerAfter([...scramble,...authored,...physical.slice(0,i+1)]);
  assert.equal(key(current),key(phaseState(originalStickers,axis)),'real sticker versus group mismatch at prefix turn '+(i+1));
  if(groupDist.has(enc(current)))exactEarly.push(i+1);
 }
 assert(cubieSolved(current));
 assert(solvedUpToRotation(stickerAfter([...scramble,...authored,...physical])));
 const first=exactEarly.length?exactEarly[0]:null;
 if(p.id==='riabov_other_3')assert(first===null||first>=9);
 rows.push({id:p.id,axis,source_status:c.declared_mode,source_DR_to_solved_exact_length:p.exact_minimum_DR_to_solved,
  full_authored_prefix_plus_physical_suffix_raw_turns:authored.length+physical.length,
  full_cubie_member_HTR_at_continuation_depths:exactEarly,
  first_HTR_contact_on_this_optimal_solving_word:first,
  shortest_HTR_contact_distance_not_necessarily_same_as_this_path:first,
  full_source_specific_actual_cube_replay:true});
}
const special=rows.find(x=>x.id==='riabov_other_3');
const report={
 marker:'CUBE_REV_022_P8_R3_MINIMAL_PHASE2_SOLUTION_H_GROUP_FIRST_CONTACT_PHYSICAL_AUDIT',
 physical_group:'663552 full HTR genuine actual half-turn whole-cube states',
 actual_source_ledgers:'P7 original human authored retrospective reconstructions; Riabov Other #1/#3 conditional parses',
 source_separate_replay_count:rows.length,
 source_specific_exact_solved_state_paths:rows,
 riabov_other_3_first_contact_according_to_witness:special.first_HTR_contact_on_this_optimal_solving_word,
 hard_lower_bound_for_riabov_other_3_HTR_any_path:9,
 valid_upper_bound_for_riabov_other_3_HTR_any_path:special.first_HTR_contact_on_this_optimal_solving_word,
 no_global_FMC_optimality_claim:true
};
console.log(JSON.stringify(report,null,2));
