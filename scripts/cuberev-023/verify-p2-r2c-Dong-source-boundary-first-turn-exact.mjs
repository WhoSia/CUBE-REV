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



const prereg=JSON.parse(fs.readFileSync('data/cuberev-023/p2_r2c_Dong_source_boundary_geodesic_prereg.json','utf8'));
const old=JSON.parse(fs.readFileSync('data/cuberev-023/p2_r2_guarded_signature_independent_source_prereg.json','utf8'));
assert.equal(prereg.schema,'cuberev-023-p2-r2c-independent-Dong-authored-boundary-shortest-suffix-v1');
const real=old.independent_source;
const scramble=tokenize(real.scramble);
const human=tokenize(real.source_EO+' '+real.source_DR);
const published=tokenize(real.submitted_full_22);
assert.equal(human.length,10);
assert.equal(published.length,22);
assert.deepEqual(published.slice(0,10),human);
assert.equal(human.at(-1),'D');
assert(solvedUpToRotation(stickerAfter([...scramble,...published])));
const sourceStickers=stickerAfter([...scramble,...human]);
assert.deepEqual(Object.keys(ROT).filter(a=>dr(phaseState(sourceStickers,a))),['LR']);
const originalBound=12;
assert.equal(published.length-human.length,originalBound);
const witnessTests=[];
for(const first of prereg.physically_exhaustive_test_alphabet){
 const extended=stickerAfter([...scramble,...human,first]);
 const dest=encode(toCubieState(extended));
 const F=bfs(dest,5,'Dong_matched_original_face_boundary_move_'+first);
 assert.deepEqual(F.hist,G.hist);
 const shorter=inspect(dest,F,'test_child_'+first);
 // Given independently exact d18(source)=12, one actual legal face turn can decrease it
 // to 11 at most. A child with d<=10 contradicts full 18-HTM group metric.
 assert.equal(shorter.best,null,'Unexpected <=10 after one action from exact source distance12');
 let oneBridge=0,attained=false,suffix11=null;
 outer:for(const [gk,gw] of G.visited){
  if(gw.length!==5)continue;
  for(let a=0;a<18;a++){
   oneBridge++;
   const intermediate=advance(gk,move[a]),fw=F.visited.get(intermediate);
   if(fw===undefined)continue;
   const words=fw+inverse[chars[a]]+invertWord(gw);
   const candidate=decodeWord(words);
   assert.equal(candidate.length,11,'Shortest source12 implies 11 from child if hit');
   suffix11=candidate;attained=true;break outer;
  }
 }
 if(!attained)assert.equal(oneBridge,574908*18,'Must exhaust all depth11 routes before exclusion');
 const row={
  first_additional_original_face_turn:first,
  physical_full_cube_original_parent_sha256:crypto.createHash('sha256').update(encode(toCubieState(sourceStickers))).digest('hex'),
  physically_supported_exact_12_turn_continuation_starting_this_face:attained,
  eleven_turn_whole_cube_midpoint_tests:oneBridge,
  original_DR_source_literal_prefix_len:human.length,
  initial_source_shortest_all18_distance_imported_exact:originalBound,
  child_bfs_original_full_cubie_histogram:F.hist,
  exact_11_turn_child_solution_if_attained:attained?null:null
 };
 if(attained){
  const word=[...human,first,...suffix11];
  assert.equal(word.length,22);
  assert(solvedUpToRotation(stickerAfter([...scramble,...word])),'Original source physical replay after face cancel failed');
  const normalized=adjacentNormalized(word);
  assert(solvedUpToRotation(stickerAfter([...scramble,...normalized])));
  assert(normalized.length<22,'Same-face author/suffix boundary should be reducible');
  row.exact_11_turn_child_solution_if_attained=suffix11.join(' ');
  row.physical_complete_22_raw_word=word.join(' ');
  row.physical_adjacent_normalized_solution=normalized.join(' ');
  row.normalized_finished_HTM=normalized.length;
  row.boundary_savings_HTM=22-normalized.length;
  row.authored_literal_prefix_retained_after_normalization=human.every((t,i)=>normalized[i]===t);
 } else {
  row.exclusion_claim='No shortest12 (regardless of remaining moves) can begin with this original-face turn, from exhaustive source-child radius5/goal radius5 + 1 bridge';
 }
 witnessTests.push(row);
}
assert.equal(witnessTests.length,3);
const possible=witnessTests.filter(x=>x.physically_supported_exact_12_turn_continuation_starting_this_face);
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P2_R2C_INDEPENDENT_HUMAN_DONG_OPTIMAL_BOUNDARY_TURN_COURT',
 source_url:real.original_reconstruction_url,independent_author:real.author,
 real_DR_source_full_54_sticker_verified:true,
 original_human_complete_22_solved_exact:true,
 imported_actual_source_prefix_18HTM_exact_postcost:originalBound,
 authored_last_real_face:'D',
 exactly_three_boundary_merge_eligible_first_moves:['D','D2',"D'"],
 exact_shortest_postprefix_paths_tested_at_first_step:true,
 independent_exhaustive_full_cube_11_turn_bridge_searches:true,
 shortest12_cancellation_first_moves_physically_possible:possible.map(x=>x.first_additional_original_face_turn),
 final_normalized_source_conditioned_cancellation_witnesses:possible.map(x=>({move:x.first_additional_original_face_turn,normalized_HTM:x.normalized_finished_HTM,physically_solved:true})),
 potential_shorter_than_human_recorded_22_minimum_constructed:possible.length>0?Math.min(...possible.map(x=>x.normalized_finished_HTM)):null,
 if_no_moves_possible_all_12turn_shortest_continuations_are_reduced_at_human_prefix_boundary:possible.length===0,
 no_global_unrestricted_FMC_OPTIMALITY_INFERENCE:true,
 unobserved_human_mental_choice_NOT_IDENTIFIED:true,
 exact_three_face_turn_tests:witnessTests
},null,2));
