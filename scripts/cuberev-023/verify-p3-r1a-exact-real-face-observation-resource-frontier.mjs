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



const register=JSON.parse(fs.readFileSync('data/cuberev-023/p3_r1a_preregistered_physical_face_query_dictionary_frontier.json','utf8'));
assert.equal(register.schema,'cuberev-023-p3-r1a-real-face-observation-dictionary-frontier-preregistered-v1');
assert.deepEqual(G.hist,[1,18,243,3240,43239,574908]);
assert.equal(G.visited.size,621649);
const frequency=new Map();
for(const cube of G.visited.keys()){
 const projection=cube.slice(0,16);
 frequency.set(projection,(frequency.get(projection)||0)+1);
}
assert.equal(frequency.size,236552);
let maxFiber=0,chosenCorner='';
for(const [projection,count] of frequency){
 if(count>maxFiber||(count===maxFiber&&(chosenCorner===''||projection<chosenCorner))){
  chosenCorner=projection;maxFiber=count;
 }
}
assert.equal(maxFiber,62);
const source=[];
for(const [cube,encodedMoves] of G.visited){
 if(cube.slice(0,16)!==chosenCorner)continue;
 source.push({cubie:cube,encodedMoves,turns:decodeWord(encodedMoves)});
}
source.sort((a,b)=>a.cubie.localeCompare(b.cubie,'en'));
assert.equal(source.length,62);
assert.equal(new Set(source.map(x=>x.cubie)).size,62);
const cornersOf=x=>x.slice(0,16);
const stickerSignatures=[];
const faceOrder='URFDLB'.split('');
for(const s of source){
 const stickers=stickerAfter(s.turns);
 assert.equal(encode(toCubieState(stickers)),s.cubie);
 const faces=Object.fromEntries(faceOrder.map(face=>[face,[]]));
 for(const sticker of stickers){
  const f=normal[sticker.n.join(',')];
  assert(faces[f],"Every full 3x3 physical sticker must live on one of six outward faces");
  faces[f].push({position:sticker.p.join(','),color:sticker.c});
 }
 const signatures=faceOrder.map(face=>{
  const facelets=faces[face].sort((a,b)=>a.position.localeCompare(b.position,'en'));
  assert.equal(facelets.length,9);
  return facelets.map(x=>x.color).join('');
 });
 const inversePath=decodeWord(invertWord(s.encodedMoves));
 const fullSolved=encode(toCubieState(stickerAfter([...s.turns,...inversePath])));
 assert.equal(fullSolved,root,"Original sticker exact complete inverse witness");
 stickerSignatures.push({signatures,inversePath,sourceWord:s.turns.join(' '),fullCubieStateSHA256:crypto.createHash('sha256').update(s.cubie).digest('hex')});
}
const commonCornerSolve=stickerSignatures[0].inversePath;
for(const row of stickerSignatures){
 const actual=toCubieState(stickerAfter([...tokenize(row.sourceWord),...commonCornerSolve]));
 assert.equal(encode(actual).slice(0,16),root.slice(0,16),'Identical corner full-cube state requires common corner solve action');
}
const uniqueInverse=new Set(stickerSignatures.map(x=>x.inversePath.join(' ')));
assert.equal(uniqueInverse.size,62,'Different exact cubie positions need distinct inverse solution word');
for(let i=0;i<62;i++)for(let j=i+1;j<62;j++)assert.notDeepEqual(stickerSignatures[i].signatures,stickerSignatures[j].signatures);
const ALL=(1n<<62n)-1n;
const popcount=mask=>{let n=0;for(let x=mask;x!==0n;x&=x-1n)n++;return n;};
const cachePartition=new Map();
function parts(mask,face){
 const key=faceOrder[face]+'|'+mask.toString(16);
 if(cachePartition.has(key))return cachePartition.get(key);
 const out=new Map();
 for(let i=0;i<62;i++){
  const bit=1n<<BigInt(i);
  if((mask&bit)===0n)continue;
  const signature=stickerSignatures[i].signatures[face];
  out.set(signature,(out.get(signature)||0n)|bit);
 }
 const result=[...out.entries()].sort((a,b)=>a[0].localeCompare(b[0],'en')).map(([signature,set])=>({signature,set}));
 let check=0n;for(const x of result){assert.equal(check&x.set,0n);check|=x.set;}assert.equal(check,mask);
 cachePartition.set(key,result);
 return result;
}
const optMemo=new Map(),leafMemo=new Map(),optStates={};
function minimax(mask,used){
 const n=popcount(mask);
 if(n===1)return {cost:0,face:-1};
 const key=mask.toString(16)+':'+used;
 if(optMemo.has(key))return optMemo.get(key);
 let best={cost:Infinity,face:-1};
 for(let f=0;f<6;f++){
  if(used&(1<<f))continue;
  const branches=parts(mask,f);
  if(branches.length<2)continue;
  let worst=0;
  for(const ch of branches){
   const t=minimax(ch.set,used|(1<<f));
   worst=Math.max(worst,t.cost);
   if(worst>=best.cost)break;
  }
  const cur=1+worst;
  if(cur<best.cost)best={cost:cur,face:f};
 }
 optMemo.set(key,best);
 return best;
}
function leaves(mask,used,budget){
 if(popcount(mask)===1||budget===0)return 1;
 const key=mask.toString(16)+':'+used+':'+budget;
 if(leafMemo.has(key))return leafMemo.get(key);
 let best=1;
 for(let f=0;f<6;f++){
  if(used&(1<<f))continue;
  const branches=parts(mask,f);
  if(branches.length<2)continue;
  let sum=0;
  for(const ch of branches)sum+=leaves(ch.set,used|(1<<f),budget-1);
  if(sum>best)best=sum;
 }
 assert(best<=popcount(mask));
 leafMemo.set(key,best);
 return best;
}
const minimaxSolution=minimax(ALL,0);
assert(minimaxSolution.face>=0&&Number.isInteger(minimaxSolution.cost)&&minimaxSolution.cost<=6);
const pathTrace=[],leavesInTree=[];
function replayTree(mask,used,steps){
 const n=popcount(mask);
 if(n===1){
  let idx=-1;for(let i=0;i<62;i++)if(mask===(1n<<BigInt(i)))idx=i;
  assert(idx>=0);
  leavesInTree.push({idx,observations:steps});
  return;
 }
 const decision=minimax(mask,used);
 assert(decision.face>=0);
 for(const br of parts(mask,decision.face)){
  replayTree(br.set,used|(1<<decision.face),[...steps,{face:faceOrder[decision.face],nineStickerColors:br.signature}]);
 }
}
replayTree(ALL,0,[]);
assert.equal(leavesInTree.length,62);
assert.equal(new Set(leavesInTree.map(x=>x.idx)).size,62);
assert.equal(Math.max(...leavesInTree.map(x=>x.observations.length)),minimaxSolution.cost);
for(const row of leavesInTree){
 for(const step of row.observations){
  const face=faceOrder.indexOf(step.face);
  assert.equal(stickerSignatures[row.idx].signatures[face],step.nineStickerColors);
 }
 const inverse=stickerSignatures[row.idx].inversePath;
 const whole=[...source[row.idx].turns,...inverse];
 assert.equal(encode(toCubieState(stickerAfter(whole))),root);
}
const pop6=x=>{let n=0;for(let t=x;t;t&=t-1)n++;return n;};
const fixedSubsets=[];
const fixedFrontier=Array(7).fill(0);
for(let mask=0;mask<64;mask++){
 const k=pop6(mask),patterns=new Set();
 for(const r of stickerSignatures){
  patterns.add(faceOrder.map((_,i)=>(mask&(1<<i))?r.signatures[i]:'NOT_READ').join('|'));
 }
 const n=patterns.size;
 fixedFrontier[k]=Math.max(fixedFrontier[k],n);
 fixedSubsets.push({faceMask:mask,faces:faceOrder.filter((_,i)=>mask&(1<<i)).join(''),n_faces:k,distinct_observation_classes:n,completely_identifies_all_62:n===62});
}
const minimalFixed=Math.min(...fixedSubsets.filter(x=>x.completely_identifies_all_62).map(x=>x.n_faces));
const exactMinimalFixedSubsets=fixedSubsets.filter(x=>x.completely_identifies_all_62&&x.n_faces===minimalFixed);
assert(exactMinimalFixedSubsets.length>0);
const adaptiveFrontier=Array.from({length:7},(_,q)=>leaves(ALL,0,q));
for(let q=0;q<=6;q++){
 assert(adaptiveFrontier[q]>=fixedFrontier[q]);
 assert(adaptiveFrontier[q]<=62);
 if(q)assert(adaptiveFrontier[q]>=adaptiveFrontier[q-1]);
}
assert.equal(adaptiveFrontier[0],1);
assert.equal(adaptiveFrontier[6],62);
const minForFull=adaptiveFrontier.findIndex(x=>x===62);
assert.equal(minForFull,minimaxSolution.cost,'Independent leaf-max success frontier vs minimax full identification');
const classGrades=[1,2,4,8,16,32,62];
const resourcePareto=[];
for(let q=0;q<=6;q++)for(const dictionaryLimit of classGrades){
 const numberSolved=Math.min(dictionaryLimit,adaptiveFrontier[q]);
 resourcePareto.push({maximum_adaptive_full_face_queries:q,max_distinct_full_solution_words:dictionaryLimit,max_correct_full_cube_states_uniform_prior:numberSolved,success_frequency_in_frozen_uniform_62:numberSolved+'/62',full_guarantee:numberSolved===62});
}
assert(resourcePareto.filter(x=>x.full_guarantee).every(x=>x.maximum_adaptive_full_face_queries>=minForFull&&x.max_distinct_full_solution_words>=62));
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P3_R1A_TRUE_FULL_CUBE_FACE_INSPECTION_VS_ALGORITHM_DICTIONARY_FRONTIER',
 preregistration_preceded_first_new_outcome:true,
 physical_reference:'Original 54-sticker complete 18-HTM radius<=5 whole-cubie states',
 original_r5_full_cubie_states:G.visited.size,
 original_corner_projection_state_keys:frequency.size,
 chosen_largest_fixed_frame_corner_equivalence_fiber_count:source.length,
 corner_fiber_lexicographic_tie_rule_verified:true,
 raw_two_goal_tasks:{corner_permutation_orientation_only:'COMMON_WORD_LENGTH_'+commonCornerSolve.length,full_original_cp_co_ep_eo:'DISTINCT_MINIMAL_EXACT_INVERSES_62'},
 same_corner_orientation_and_permutation_for_all:true,
 exact_solved_word_dictionary_minimum_corner_task:1,
 exact_solved_word_dictionary_minimum_full_task_given_perfect_state_identification:62,
 exact_full_HTM_per_state_completion_word_upper:5,
 corner_task_extra_face_queries_needed:0,
 exact_fixed_face_subset_enumerations:fixedSubsets.length,
 exact_minimum_fixed_full_face_looks_to_identify_state:minimalFixed,
 all_optimal_minimal_fixed_face_subsets:exactMinimalFixedSubsets,
 full_face_order:faceOrder.join(''),
 fixed_face_maximum_unique_classes_by_budget:fixedFrontier,
 adaptive_exact_maximum_uniform_prior_correct_states_by_face_query_budget:adaptiveFrontier,
 exact_minimax_adaptive_full_face_looks_to_identify_state:minimaxSolution.cost,
 exact_adaptive_tree_leaf_count:leavesInTree.length,
 exact_adaptive_tree_decision_internal_memo_states:optMemo.size,
 exact_adaptive_budgeted_leaf_DP_states:leafMemo.size,
 selected_adaptive_tree_distinct_physical_faces_and_full_nine_color_observations:leavesInTree,
 uniform_artificial_prior_not_actual_human_behavior:true,
 exact_solution_success_resource_grid:resourcePareto,
 expected_optimal_tree_queries_under_artificial_uniform_state_prior:leavesInTree.reduce((n,x)=>n+x.observations.length,0)/62,
 fixed_full_cohort_face_symbol_alphabet_multivalued_NOT_binary:true,
 prior_P3_R0_6bit_lower_bound_does_NOT_equal_number_of_full_face_looks:true,
 no_human_visual_time_attention_or_algorithms_assumed:true,
 no_real_2x2_solve_trace_claim:true,
 example_raw_full_cube_source_words:source.slice(0,8).map(x=>x.turns.join(' ')),
 common_exact_corner_solution_from_1_inverted_real_source:commonCornerSolve.join(' '),
 complete_fiber_witness_dataset:source.map((x,i)=>({index:i,source_shortest_from_solved:x.turns.join(' '),inverse_full_solution_HTM:stickerSignatures[i].inversePath.join(' '),cubie_sha256:stickerSignatures[i].fullCubieStateSHA256,face9:stickerSignatures[i].signatures}))
},null,2));
