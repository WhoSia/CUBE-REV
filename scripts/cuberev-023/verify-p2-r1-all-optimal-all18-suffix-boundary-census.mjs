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


const source=tokenize(ledger.normal_scramble);
const input=JSON.parse(fs.readFileSync('data/cuberev-023/p2_P1_all18_four_word_authority_fixture.json','utf8'));
assert.equal(input.rows.length,4);
const ipow=x=>x.endsWith('2')?2:x.endsWith("'")?3:1;
const mkTok=(f,p)=>f+(p===1?'':p===2?'2':p===3?"'":'');
function reduceHTM(word) {
 const stack=[];
 for(const x of word){
  const y=stack.at(-1);
  if(!y||y[0]!==x[0]){stack.push(x);continue;}
  stack.pop();
  const z=(ipow(x)+ipow(y))%4;
  if(z)stack.push(mkTok(x[0],z));
 }
 return stack;
}
const invertToken=x=>x.endsWith('2')?x:x.endsWith("'")?x[0]:x[0]+"'";
const invMove=acts.map(x=>move[acts.indexOf(invertToken(x))]);
const goalDistance=new Map([...G.visited].map(([k,w])=>[k,w.length]));
assert.equal(G.hist.join(','),'1,18,243,3240,43239,574908');
const sourceGoalDistances=new Map([[root,0]]);
const goalCounts=new Map([[root,1n]]);
for(let depth=0;depth<5;depth++){
 for(const [k,w] of G.visited){
  if(w.length!==depth)continue;
  const count=goalCounts.get(k);
  assert(count!==undefined);
  for(let a=0;a<18;a++){
   const next=advance(k,move[a]);
   if(goalDistance.get(next)!==depth+1)continue;
   goalCounts.set(next,(goalCounts.get(next)||0n)+count);
  }
 }
}
assert.equal(goalCounts.size,G.visited.size);
const proof=[];
for(const item of input.rows){
 const author=ledger.eo_dr_pairs.find(x=>x.id===item.source_id);
 assert(author);
 const written=tokenize(author.eo_prefix+' '+author.dr_extension);
 const synth=tokenize(item.synthetic_original_face_word);
 const fixed=[...written,...synth];
 const s=encode(toCubieState(stickerAfter([...source,...fixed])));
 const remaining=item.post_intervention_all18_exact_length;
 assert([10,11].includes(remaining));
 assert.equal(written.length+synth.length+remaining,23);
 const sf=bfs(s,5,'source_'+item.source_id+'_'+item.synthetic_FBDR_actions);
 assert.deepEqual(sf.hist,G.hist);
 // Establish EXACT distance by the same independent physical midpoint exclusion.
 const intersection=inspect(null,sf,item.source_id).best;
 if(remaining===11)assert.equal(intersection,null,'No full-cubie <=10 solution for an 11-turn exact source');
 else assert(intersection&&intersection.length===10);
 const good=[new Map(),new Map(),new Map(),new Map(),new Map(),new Map()];
 let midpointCount=0,terminalBridges=0;
 for(const [k,w] of sf.visited){
  if(w.length!==5)continue;
  let c=0n,completing=null;
  if(remaining===10){
   if(goalDistance.get(k)===5){
    c=goalCounts.get(k);
    completing=invertWord(G.visited.get(k));
   }
  }else{
   for(let a=0;a<18;a++){
    const newKey=advance(k,move[a]);
    if(goalDistance.get(newKey)!==5)continue;
    c+=goalCounts.get(newKey);
    if(completing===null)completing=chars[a]+invertWord(G.visited.get(newKey));
    terminalBridges++;
   }
  }
  if(c>0n){
   good[5].set(k,{count:c,suffix:completing});
   midpointCount++;
  }
 }
 assert(midpointCount>0);
 let backwardsEdges=0;
 for(let depth=5;depth>0;depth--){
  for(const [k,entry] of good[depth]){
   for(let a=0;a<18;a++){
    const pred=advance(k,invMove[a]);
    const w=sf.visited.get(pred);
    if(w===undefined||w.length!==depth-1)continue;
    const old=good[depth-1].get(pred);
    const newCount=(old?.count??0n)+entry.count;
    const newSuffix=old?.suffix??(chars[a]+entry.suffix);
    good[depth-1].set(pred,{count:newCount,suffix:newSuffix});
    backwardsEdges++;
   }
  }
 }
 assert.equal(good[0].size,1);
 const total=good[0].get(s).count;
 let histogram=new Map(),samples=new Map(),groupPrefixPairCounts=new Map();
 let legalPrefixes=0,oneWords=new Set(),observedTwo=new Set();
 for(let a=0;a<18;a++){
  const t1=advance(s,move[a]);
  for(let b=0;b<18;b++){
   const t2=advance(t1,move[b]);
   if(sf.visited.get(t2)?.length!==2)continue;
   const entry=good[2].get(t2);
   if(!entry)continue;
   const firstTwo=acts[a]+' '+acts[b];
   legalPrefixes++;
   oneWords.add(acts[a]);observedTwo.add(firstTwo);
   const fullSuffix=decodeWord(chars[a]+chars[b]+entry.suffix);
   assert.equal(fullSuffix.length,remaining);
   const raw=[...fixed,...fullSuffix];
   assert.equal(raw.length,23);
   const reduced=reduceHTM(raw);
   const saved=23-reduced.length;
   const previouslyLower=item.source_id==='miao_main'?19:23;
   assert(reduced.length>=previouslyLower,'Contradicts R4 exact source-authored stage geodesic');
   assert(reduced.slice(0,written.length).every((t,i)=>t===written[i]),'Source literal prefix was unexpectedly modified');
   const size=entry.count;
   histogram.set(saved,(histogram.get(saved)||0n)+size);
   const category=samples.get(saved);
   if(!category)samples.set(saved,{first_two:firstTwo,complete_post_synthetic_optimal_suffix:fullSuffix.join(' '),complete_normalized_word:reduced.join(' '),normalized_length:reduced.length,original_stickers_replayed:false});
   groupPrefixPairCounts.set(firstTwo,size.toString());
  }
 }
 const sum=[...histogram.values()].reduce((x,y)=>x+y,0n);
 assert.equal(sum,total,'All shortest path first two actions must partition complete counted optimal suffix DAG');
 // Physical independent replay for EACH observed class + imported previous P1 witness.
 for(const sample of samples.values()){
  const complete=[...source,...tokenize(sample.complete_normalized_word)];
  assert(solvedUpToRotation(stickerAfter(complete)),'Boundary class witness must solve original full sticker cube');
  sample.original_stickers_replayed=true;
 }
 const imported=tokenize(item.full_18_exact_shortest_suffix);
 assert.equal(imported.length,remaining);
 assert(solvedUpToRotation(stickerAfter([...source,...fixed,...imported])));
 const originalNorm=reduceHTM([...fixed,...imported]);
 const importedSavings=23-originalNorm.length;
 assert(histogram.has(importedSavings));
 // Independent second proof: enumerate EVERY whole-word optimal 18-HTM path,
 // not merely one witness per shortest-state or first-two face-turn class.
 // For these four source-bound states the proven exact total is tiny (<=5000).
 assert(total<=5000n,'P2-R1 complete physical replay bound must not silently truncate');
 const allWordKeys=new Set(),allWordCounts=new Map(),allWordExamples=[];
 function finishGoal(k,depth,codes){
  if(depth===0){
   assert.equal(k,root);
   assert.equal(codes.length,remaining);
   const word=decodeWord(codes);
   const phrase=word.join(' ');
   assert(!allWordKeys.has(phrase),'Duplicate optimal suffix word counted through graph');
   allWordKeys.add(phrase);
   const full=[...fixed,...word],reduced=reduceHTM(full);
   assert(solvedUpToRotation(stickerAfter([...source,...full])));
   assert(solvedUpToRotation(stickerAfter([...source,...reduced])));
   assert(reduced.slice(0,written.length).every((t,i)=>t===written[i]));
   const saved=23-reduced.length;
   allWordCounts.set(saved,(allWordCounts.get(saved)||0n)+1n);
   allWordExamples.push({
    shortest_suffix:phrase,
    first_two:word.slice(0,2).join(' '),
    boundary_savings_HTM:saved,
    normalized_final_word_length:reduced.length,
    original_54_sticker_solved:true
   });
   return;
  }
  for(let j=0;j<18;j++){
   const next=advance(k,move[j]);
   if(goalDistance.get(next)===depth-1)finishGoal(next,depth-1,codes+chars[j]);
  }
 }
 function followSource(k,depth,codes){
  if(depth===5){
   if(remaining===10){
    if(goalDistance.get(k)===5)finishGoal(k,5,codes);
   }else{
    for(let j=0;j<18;j++){
     const next=advance(k,move[j]);
     if(goalDistance.get(next)===5)finishGoal(next,5,codes+chars[j]);
    }
   }
   return;
  }
  for(let j=0;j<18;j++){
   const next=advance(k,move[j]);
   if(good[depth+1].has(next))followSource(next,depth+1,codes+chars[j]);
  }
 }
 followSource(s,0,'');
 assert.equal(BigInt(allWordKeys.size),total,'Independent explicit optimal word enumeration disagrees with DAG count');
 for(const [saved,count] of histogram)assert.equal(allWordCounts.get(saved),count,'Explicit original-sticker replay class counts disagree with DP');
 assert.equal(allWordExamples.length,allWordKeys.size);
 const possible=[...histogram.keys()].sort((a,b)=>a-b);
 const allCounts=Object.fromEntries(possible.map(x=>[String(x),histogram.get(x).toString()]));
 const exactClassFreq=Object.fromEntries(possible.map(x=>[String(x),Number(histogram.get(x)>0n)]));
 proof.push({
  source_id:item.source_id,synthetic_canonical_FB_word:item.synthetic_FBDR_actions,
  original_synthetic_physical_word:item.synthetic_original_face_word,
  exact_full_18_shortest_post_intervention_length:remaining,
  authentic_source_full_prefix_actions:written.length,
  physical_root_Cubie_SHA256:crypto.createHash('sha256').update(s).digest('hex'),
  source_radius5_unique_physical_states:sf.visited.size,
  goal_radius5_unique_physical_states:G.visited.size,
  admissible_midpoints_at_exact_five:midpointCount,admissible_final_one_move_goalBridges:terminalBridges,
  good_shortest_completion_DAG_state_counts:good.map(m=>m.size),
  source_backwards_optimal_DAG_edges:backwardsEdges,
  distinct_first_one_moves_in_an_optimal_suffix:[...oneWords].sort(),
  distinct_first_two_words_in_an_optimal_suffix_count:observedTwo.size,
  exact_optimal_all18_suffix_word_COUNT:total.toString(),
  independent_complete_suffix_word_enumeration_verified:true,
  all_shortest_suffix_words_physically_replayed_on_original_54_stickers:true,
  all_optimal_suffix_words_with_boundary_savings:allWordExamples,
  geodesic_first_two_partition_verified:true,
  optimal_suffix_word_counts_by_final_adjacent_face_savings:allCounts,
  actual_possible_final_adjacent_face_savings:possible,
  exact_normalized_witness_length_range:[23-Math.max(...possible),23-Math.min(...possible)],
  physically_replayed_representative_per_savings_class:Object.fromEntries([...samples.entries()].map(([x,y])=>[String(x),y])),
  source_literal_preserved_in_every_sample:true,
  observed_previous_P1_witness_savings:importedSavings,
  this_result_only_source_conditional_synthetic_NOT_HUMAN_OBSERVED:true
 });
}
const pairs=["D B2","D' F2"].map(name=>{
 const a=proof.filter(x=>x.synthetic_canonical_FB_word===name);
 assert.equal(a.length,2);
 const totals=a.map(x=>x.exact_optimal_all18_suffix_word_COUNT);
 const savingsSets=a.map(x=>x.actual_possible_final_adjacent_face_savings);
 const aa=a[0],bb=a[1];
 return {
  matched_synthetic_word:name,
  main_exact_minimal_post_intervention_suffix_count:totals[0],
  alternative_exact_minimal_post_intervention_suffix_count:totals[1],
  main_all_optimal_suffix_boundary_savings:savingsSets[0],
  alt_all_optimal_suffix_boundary_savings:savingsSets[1],
  all_suffix_final_witness_lengths_main:aa.exact_normalized_witness_length_range,
  all_suffix_final_witness_lengths_alt:bb.exact_normalized_witness_length_range,
  source_literal_prefix_conditioned_global_exact_optimum:[19,23],
  source_specific_human_choice_not_observed:true
 };
});
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P2_R1_ALL_OPTIMAL_18_HTM_SUFFIX_BOUNDARY_CENSUS',
 scientific_goal:'Count all distinct shortest legal 18 HTM suffix move WORDS of each physically actual P1 branch state, not only one BFS-selected witness. Classify complete final adjacent-face cancellation outcomes and physically replay one witness of every class.',
 independent_all18_backward_exact_goal_radius5:G.hist,
 no_greedy_suffix_selection_and_no_shortest_path_omission:true,
 ordered_full_face_turn_graph_both_commuting_orders_included_in_suffix_DAG:true,
 all_shortest_suffixes_counted_as_distinct_legal_HTM_words_not_distinct_endpoints:true,
 every_single_geodesic_suffix_word_independently_enumerated_and_physically_replayed:true,
 physical_full_54_sticker_replay_per_class:true,
 exact_original_prefix_preserving_19_vs_23_bound_still_enforced:true,
 human_cognition_not_identified:true,
 results:proof,
 matched_original_authored_branch_pairs:pairs
},null,2));
