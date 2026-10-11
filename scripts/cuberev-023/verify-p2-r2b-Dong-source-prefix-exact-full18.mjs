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


const prereg=JSON.parse(fs.readFileSync('data/cuberev-023/p2_r2b_Dong_whole18_prefix_optimality_prereg.json','utf8'));
const upstream=JSON.parse(fs.readFileSync('data/cuberev-023/p2_r2_guarded_signature_independent_source_prereg.json','utf8'));
assert.equal(prereg.schema,'cuberev-023-p2-r2b-Dong-source-conditioned-whole18-exact-opportunity-v1');
const origin=upstream.independent_source;
const scramble=tokenize(origin.scramble);
const written=tokenize(origin.source_EO+' '+origin.source_DR);
const submitted=tokenize(origin.submitted_full_22);
assert.equal(written.length,10);assert.equal(submitted.length,22);
assert.deepEqual(submitted.slice(0,10),written);
const humanRemainder=submitted.slice(10);
assert.equal(humanRemainder.length,12);
assert(solvedUpToRotation(stickerAfter([...scramble,...submitted])));
const targetStickers=stickerAfter([...scramble,...written]);
const axes=Object.keys(ROT).filter(a=>dr(phaseState(targetStickers,a)));
assert.deepEqual(axes,['LR']);
const source=encode(toCubieState(targetStickers));
const F=bfs(source,5,'Dong_actual_authored_LR_DR_full18_radius5');
assert.deepEqual(F.hist,G.hist);
const c=inspect(source,F,'dong_real_human_EO_DR_word');
let exact=null,constructed=null,route=null,oneEdgeQueries=0,oneEdgeExhausted=false;
if(c.best!==null){
 exact=c.best.length;
 constructed=decodeWord(c.best.continuationChars);
 route='FULL_CUBIE_18_HTM_MEET_IN_MIDDLE_EXACT_5_5';
}else{
 outer:for(const [goalState,goalWord] of G.visited){
  if(goalWord.length!==5)continue;
  for(let a=0;a<18;a++){
   oneEdgeQueries++;
   const dest=advance(goalState,move[a]);
   const fromSource=F.visited.get(dest);
   if(fromSource===undefined)continue;
   const charsWord=fromSource+inverse[chars[a]]+invertWord(goalWord);
   const candidate=decodeWord(charsWord);
   assert(candidate.length<=11);
   exact=candidate.length;
   constructed=candidate;
   route='FULL_CUBIE_18_HTM_INDEPENDENT_5_ONE_5_BRIDGE';
   break outer;
  }
 }
 if(exact===null){
  assert.equal(oneEdgeQueries,574908*18,'Need complete 11-turn exclusion before declaring exact 12');
  oneEdgeExhausted=true;
  exact=12;
  constructed=humanRemainder;
  route='EXHAUSTIVE_NO_18_HTM_PATH_LE_11_AND_AUTHENTIC_HUMAN_12_UPPER_STICKER_REPLAY';
 }
}
assert(exact>=0&&exact<=12);
assert.equal(constructed.length,exact);
const reconstructed=[...written,...constructed];
const entire=[...scramble,...reconstructed];
assert(solvedUpToRotation(stickerAfter(entire)),'Constructed all18 shortest source-preserving witness not physically solved');
const reduced=adjacentNormalized(reconstructed);
assert(solvedUpToRotation(stickerAfter([...scramble,...reduced])));
const origReduced=adjacentNormalized(submitted);
assert(solvedUpToRotation(stickerAfter([...scramble,...origReduced])));
const beforeFullHumanEnds=written.every((t,i)=>t===origReduced[i]);
const beforeFullConstructEnds=written.every((t,i)=>t===reduced[i]);
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P2_R2B_DONG_INDEPENDENT_SOURCE_ALL18_EXACT_FIXED_PREFIX_OPPORTUNITY',
 preregistered_before_result:true,
 independent_source:origin.original_reconstruction_url,
 author:origin.author,
 competition:origin.event,attempt:origin.attempt,
 source_EO_DR_literal_original_actions:written.join(' '),
 source_original_prefix_HTM:written.length,
 verified_physical_DR_axes:axes,
 original_22_HTM_public_result_solves_original_cube:true,
 human_published_full_word_HTM:submitted.length,
 human_published_remaining_after_authored_DR:humanRemainder.length,
 entire_source_18_HTM_goal_ball_cardinalities:G.hist,
 independently_reconstructed_source_full_cubie_radius5_cardinalities:F.hist,
 complete_intersection_check_for_paths_at_most_10:true,
 one_bridge_checked_directed_goal_depth5_turns:oneEdgeQueries,
 all_lengths_at_most_11_excluded_when_distance12:oneEdgeExhausted,
 exact_shortest_all18_post_actual_human_source_prefix:exact,
 source_prefix_plus_exact_shortest_raw_total_HTM:written.length+exact,
 difference_human_published_22_minus_computed_source_prefix_minimum:submitted.length-(written.length+exact),
 shortest_solve_witness_source_prefix_plus_all18:reconstructed.join(' '),
 witness_physically_solves_original_54_sticker_cube:true,
 witness_adjacent_face_normalized_length:reduced.length,
 human_published_reduced_length:origReduced.length,
 human_actual_full_word_preserves_authored_first10_after_normalization:beforeFullHumanEnds,
 geodesic_candidate_preserves_authored_first10_after_normalization:beforeFullConstructEnds,
 reconstructed_geodesic_warrant:route,
 source_notes_backup_parenthesis_UNRESOLVED:true,
 human_historical_choice_trajectory_NOT_IDENTIFIED:true,
 bounded_this_original_literal_prefix_only:true,
 global_FMC_NISS_insertion_optimum_NOT_PROVEN:true
},null,2));
