/**
 * CUBE-REV 0.22 P8-R3: source-anchored full 18 HTM face-turn meet-in-middle exact depth at most ten.
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

const scramble=tokenize(ledger.normal_scramble);
const fixtures=JSON.parse(fs.readFileSync('data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json','utf8'));
const study=['riabov_other_1','riabov_other_3'];
const sources=new Map();
for(const id of study){
 const row=ledger.eo_dr_pairs.find(z=>z.id===id),prior=fixtures.rows.find(z=>z.id===id);
 assert(row&&prior&&row.declared_mode==='ASSUMED_CONTIGUOUS_NORMAL_SIDE_FOR_TEST_ONLY');
 const authored=[...tokenize(row.eo_prefix),...tokenize(row.dr_extension)];
 const stickers=stickerAfter([...scramble,...authored]);
 const axes=Object.keys(ROT).filter(x=>dr(phaseState(stickers,x)));
 assert.deepEqual(axes,[prior.axis]);
 const front=bfs(encode(toCubieState(stickers)),5,'full_source_18_'+id);
 assert.deepEqual(front.hist,G.hist);
 const earlier=tokenize(prior.actual_phase2_word);
 assert.equal(earlier.length,13);
 assert(solvedUpToRotation(stickerAfter([...scramble,...authored,...earlier])));
 sources.set(id,{row,prior,authored,front,found:null,oneStepTests:0,twoStepTests:0});
}
function fullWitness(id,fromSource,bridge,goalWord) {
 const p=sources.get(id);
 const mid=fromSource+invertWord(bridge)+invertWord(goalWord);
 const continuation=decodeWord(mid);
 assert.equal(continuation.length,12);
 const whole=[...p.authored,...continuation];
 const normalized=adjacentNormalized(whole);
 assert(solvedUpToRotation(stickerAfter([...scramble,...whole])));
 assert(solvedUpToRotation(stickerAfter([...scramble,...normalized])));
 return {exact_suffix_length:12,raw_authored_prefix_plus_suffix_HTM:whole.length,
  suffix:continuation.join(' '),
  full_raw_physical_word:whole.join(' '),
  normalized_full_word:normalized.join(' '),
  normalized_full_HTM:normalized.length,
  literal_source_prefix_preserved_after_normalization:p.authored.every((x,i)=>normalized[i]===x),
  replay_solved_full_original_stickers:true,
  source_half_radius:fromSource.length,goal_half_radius:goalWord.length,bridge_length:bridge.length};
}
for(const [id,p] of sources) {
 for(const k of p.front.visited.keys())assert(!G.visited.has(k),'An <=10 full-HTM completion was missed in prior R4');
}
let goalLayer=0;
for(const [k,w] of G.visited){
 if(w.length!==5)continue;
 goalLayer++;
 for(let a=0;a<18;a++){
  const one=advance(k,move[a]);
  for(const p of sources.values()){
   p.oneStepTests++;
   assert(!p.front.visited.has(one),'An <=11 general completion existed');
  }
 }
}
assert.equal(goalLayer,574908);
for(const p of sources.values())assert.equal(p.oneStepTests,574908*18);
let twoTests=0,goalNodes=0;
search:for(const [goalState,goalWord] of G.visited) {
 if(goalWord.length!==5)continue;
 goalNodes++;
 for(let a=0;a<18;a++){
  const once=advance(goalState,move[a]);
  for(let b=0;b<18;b++){
   const twice=advance(once,move[b]),mid=chars[a]+chars[b];
   twoTests++;
   for(const [id,p] of sources){
    if(p.found)continue;
    p.twoStepTests++;
    const fw=p.front.visited.get(twice);
    if(fw!==undefined)p.found=fullWitness(id,fw,mid,goalWord);
   }
   if([...sources.values()].every(x=>!!x.found))break search;
  }
 }
}
const outcomes=[];
for(const [id,p] of sources){
 const exact=p.found?12:13;
 if(!p.found)assert.equal(goalNodes,574908,'Cannot claim no depth12 without exhaustive join');
 const fallback=tokenize(p.prior.actual_phase2_word);
 assert.equal(fallback.length,13);
 const oldWhole=[...p.authored,...fallback];
 assert(solvedUpToRotation(stickerAfter([...scramble,...oldWhole])));
 const actual=p.found??{
  exact_suffix_length:13,
  suffix:fallback.join(' '),
  full_raw_physical_word:oldWhole.join(' '),
  normalized_full_word:adjacentNormalized(oldWhole).join(' '),
  normalized_full_HTM:adjacentNormalized(oldWhole).length,
  literal_source_prefix_preserved_after_normalization:p.authored.every((x,i)=>adjacentNormalized(oldWhole)[i]===x),
  replay_solved_full_original_stickers:true,
  imported_independently_verified_P8_R3_upper:true};
 outcomes.push({id,source_parse_condition:p.row.declared_mode,
  original_prefix_moves:p.authored.length,
  exact_all18_HTM_post_prefix:exact,
  full_original_prefix_plus_exact_completion_RAW_HTM:p.authored.length+exact,
  no_depth_at_most_10:true,no_depth_11:true,
  depth11_edge_checks:p.oneStepTests,depth12_two_edge_checks:p.twoStepTests,
  entire_depth12_join_examined_if_no_found:p.found===null?goalNodes===574908:null,
  exact_physical_witness:actual});
}
console.log(JSON.stringify({
 marker:'CUBE_REV_022_P8_R5_RIABOV_EXACT_GENERAL18_LENGTH12_JOIN',
 original_goal_radius5_total:G.visited.size,
 original_goal_radius5_layer:goalLayer,
 depth12_goal_layer_visited:goalNodes,
 two_middle_edge_evaluations:twoTests,
 all_18_outer_face_turns_permitted:true,
 source_pair_parsing_only_conditional:true,
 proofs:outcomes,
 human_candidate_choice_NOT_identified:true,
 global_FMC_optimum_NOT_evaluated:true
},null,2));
