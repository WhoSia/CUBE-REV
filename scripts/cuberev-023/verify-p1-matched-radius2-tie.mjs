/**
 * CUBE-REV 0.23 P1: pre-registered two-step matched source branches, exact tie-exclusion within 10 DR legal actions.
 * This is exact finite physical search, not a reconstruction of human thought.
 * Assumption: fixed physical DR axis, DR-preserving 10-face-turn alphabet,
 * then exactly six physical half-turn moves. Bound D=7 applies to DR stage only.
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

const M=DR.length,N=40320,E4=24,K=N*E4,UNVIS=255;
const perm=n=>Array.from({length:n},(_,i)=>i);
function rank(p){let v=0;for(let i=0;i<p.length;i++){let d=0;for(let j=i+1;j<p.length;j++)d+=+(p[j]<p[i]);v=v*(p.length-i)+d;}return v;}
function unrank(v,n){const d=new Array(n);for(let i=n-1;i>=0;i--){d[i]=v%(n-i);v=Math.floor(v/(n-i));}assert.equal(v,0);const pool=perm(n);return d.map(x=>pool.splice(x,1)[0]);}
for(const n of [4,8])for(const i of [0,1,15,(n===4?23:40319)])assert.equal(rank(unrank(i,n)),i);
const TC=new Uint16Array(N*M),TE=new Uint16Array(N*M),TS=new Uint8Array(E4*M);
for(let id=0;id<N;id++){
 const p=unrank(id,8);
 for(let a=0;a<M;a++){const m=FACE[DR[a]];TC[id*M+a]=rank(m.cp.map(i=>p[i]));TE[id*M+a]=rank(m.ep.slice(0,8).map(i=>p[i]));}
}
for(let id=0;id<E4;id++){
 const p=unrank(id,4);
 for(let a=0;a<M;a++){const m=FACE[DR[a]];TS[id*M+a]=rank(m.ep.slice(8).map(i=>p[i-8]));}
}
function reverseBFS(P,name) {
 const dist=new Uint8Array(K);dist.fill(UNVIS);
 const queue=new Int32Array(K),hist=[];
 let head=0,tail=1;dist[0]=0;queue[0]=0;
 while(head<tail){
  const state=queue[head++],depth=dist[state],p=(state/E4)|0,e=state%E4;
  hist[depth]=(hist[depth]||0)+1;
  for(let a=0;a<M;a++){
   const nxt=P[p*M+a]*E4+TS[e*M+a];
   if(dist[nxt]!==UNVIS)continue;
   dist[nxt]=depth+1;queue[tail++]=nxt;
  }
 }
 assert.equal(tail,K,name+'-PDB must cover all 967680 valid projected states');
 return {name,dist,maximumDepth:hist.length-1,depthHistogram:hist};
}
const corner=reverseBFS(TC,'corners_x_Eslice'),edge=reverseBFS(TE,'UDedges_x_Eslice');


const P=JSON.parse(fs.readFileSync('data/cuberev-023/p1_matched_radius2_preregistration.json','utf8'));
const P0=JSON.parse(fs.readFileSync('data/cuberev-023/p0_source_evidence_contract.json','utf8'));
assert.equal(P.schema,'cuberev-023-p1-preregistered-matched-radius2-v1');
assert.equal(P0.schema,'cuberev-023-p0-source-evidence-contract-v1');
assert.deepEqual(P.intervention_alphabet,DR);
const f=JSON.parse(fs.readFileSync('data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json','utf8'));
const scramble=tokenize(ledger.normal_scramble);
const ids=['miao_main','miao_alternative_from_same_eo'];
const starts=ids.map(id=>{
 const q=ledger.eo_dr_pairs.find(x=>x.id===id),pr=f.rows.find(x=>x.id===id);
 assert(q&&pr&&pr.axis==='FB'&&q.declared_mode==='CONTIGUOUS_NORMAL_SIDE_PREFIX');
 const prefix=[...tokenize(q.eo_prefix),...tokenize(q.dr_extension)];
 const cube=stickerAfter([...scramble,...prefix]);
 assert.deepEqual(Object.keys(ROT).filter(a=>dr(phaseState(cube,a))),['FB']);
 const s=phaseState(cube,'FB');
 const baseDistance=pr.exact_minimum_DR_to_solved;
 assert(baseDistance===(id==='miao_main'?9:12));
 assert(solvedUpToRotation(stickerAfter([...scramble,...prefix,...tokenize(pr.actual_phase2_word)])));
 return {id,prefix,state:s,baseDistance,certifiedOriginalSuffix:tokenize(pr.canonical_phase2_word)};
});
const invert=x=>x.endsWith('2')?x:x.endsWith("'")?x[0]:x[0]+"'";
const opposite={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
const signedWord=x=>x.map(t=>MAP.FB.frame_to_original[t[0]]+t.slice(1));
const maxNodesPerState=P.resource_budget.per_unique_endpoint_IDA_nodes;
const aggregateCap=P.resource_budget.max_aggregate_IDA_nodes;
const cache=[new Map(),new Map()];
let allNodes=0,computationalHolds=0,actualReplays=0;
function solve10(state,arm,intervention) {
 const k=key(state);
 if(cache[arm].has(k))return {...cache[arm].get(k),cacheHit:true};
 const original=starts[arm],baseD=original.baseDistance;
 const firstTriangle=Math.max(0,baseD-2),upper=baseD+2;
 const c0=rank(state.cp),e0=rank(state.ep.slice(0,8)),s0=rank(state.ep.slice(8).map(x=>x-8));
 const hCorner=corner.dist[c0*E4+s0],hUD=edge.dist[e0*E4+s0],h=Math.max(hCorner,hUD);
 const low=Math.max(firstTriangle,h);
 const provenUpper=[...intervention].reverse().map(invert).concat(original.certifiedOriginalSuffix);
 assert.equal(provenUpper.length,upper);
 const upperReal=[...original.prefix,...signedWord([...intervention,...provenUpper])];
 assert(solvedUpToRotation(stickerAfter([...scramble,...upperReal])),'simple inverse + known original solve upper bound must always solve');
 actualReplays++;
 const path=[],attempts=[];let nodes=0,found=null,exhausted=true;
 // State of this true original cube in the canonical FB frame is a valid DR cubie.
 function dfs(c,e,s,d,limit,last) {
  if(++nodes>maxNodesPerState||allNodes++>aggregateCap){exhausted=false;return false;}
  if(d+Math.max(corner.dist[c*E4+s],edge.dist[e*E4+s])>limit)return false;
  if(c===0&&e===0&&s===0){found=path.slice(0,d);return true;}
  if(d>=limit)return false;
  const ic=c*M,ie=e*M,is=s*M;
  for(let j=0;j<DR.length;j++){
   const face=DR[j][0];
   if(last&&(face===last||(opposite[last]===face&&face<last)))continue;
   path[d]=DR[j];
   if(dfs(TC[ic+j],TE[ie+j],TS[is+j],d+1,limit,face))return true;
   if(!exhausted)return false;
  }
  return false;
 }
 let exact=null;
 if(low===upper){
  exact=upper;found=provenUpper; // admissible bound certifies this physically replayed upper solution
  attempts.push({bound:upper,proof:'EXACT_PDB_LOWER_EQUALS_ACTUAL_FULL_STICKER_UPPER'});
 }else{
  for(let depth=low;depth<=upper;depth++){
   const before=nodes,foundThis=dfs(c0,e0,s0,0,depth,null);
   attempts.push({depth,nodes:nodes-before,complete:exhausted,solution:foundThis});
   if(foundThis){exact=depth;break}
   if(!exhausted)break;
  }
 }
 let actualSuffix=null;
 if(exact!==null){
  assert(found&&found.length===exact);
  const fullOriginal=[...original.prefix,...intervention,...found];
  assert(solvedUpToRotation(stickerAfter([...scramble,...original.prefix,...signedWord([...intervention,...found])])),'exact newly computed witness physically solves original scramble');
  actualSuffix=signedWord(found).join(' ');actualReplays++;
 }
 const proof={
  full_state_sha256:crypto.createHash('sha256').update(k).digest('hex'),
  source_id:original.id,source_original_prefix_HTM:original.prefix.length,
  initial_admissible_lower_bound:low,reverse_projection_corner_ES:hCorner,reverse_projection_UD_ES:hUD,
  original_source_geodesic:baseD,upper_bound_from_inverse_intervention_and_original_solution:upper,
  exact_10_DR_solved_distance:exact,certificate:exact===null?'COMPUTE_HOLD':'EXACT_IDA_OR_MATCHED_LOWER_UPPER',
  resource_hold:!exhausted,physical_replay_completed:exact!==null,
  shortest_actual_original_face_suffix:actualSuffix,
  tested_search_levels:attempts,IDA_nodes:nodes
 };
 cache[arm].set(k,proof);if(!exhausted)computationalHolds++;
 return proof;
}
const radiusOne=new Map(Object.entries(P.inherited_radius1_exact_DR_costs));
assert.equal(radiusOne.size,10);
const possibleFirst=new Set(P.necessary_condition_for_raw_tie.complete_candidate_first_move_actions);
const possible=[];
let ordered=0,noncritical=0,reducedOrIdentity=0;
const actionProducts=new Map(),wordCounts=new Map();
const root=key(solved);
const oneMove=new Set(DR.map(x=>key(compose(solved,FACE[x]))));
for(const first of DR)for(const second of DR){
 ordered++;
 const rel=compose(compose(solved,FACE[first]),FACE[second]),k=key(rel);
 if(!actionProducts.has(k))actionProducts.set(k,[first,second]);
 wordCounts.set(k,(wordCounts.get(k)||0)+1);
 if(k===root||oneMove.has(k))reducedOrIdentity++;
 const [main1,alt1]=radiusOne.get(first);
 if(possibleFirst.has(first)){
  assert.equal(main1,10);assert.equal(alt1,11);
  possible.push([first,second,k]);
 }else{
  // Necessity is not statistical filtering; triangle equality rules out tie after another turn.
  assert(main1!==10||alt1!==11);
  const afterSecondMinAlt=alt1-1,afterSecondMaxMain=main1+1;
  assert(1+afterSecondMinAlt-afterSecondMaxMain>0,'Unfiltered candidate could tie');
  noncritical++;
 }
}
assert.equal(ordered,100);
assert.equal(noncritical,70);
assert.equal(possible.length,30);
// Genuine radius-two sphere is the 74 new group states outside identity and 10 one-move states.
const genuinelyNew=[...actionProducts.keys()].filter(x=>x!==root&&!oneMove.has(x));
assert.equal(actionProducts.size,74,'Exactly-two-token physical images');
assert.equal(genuinelyNew.length,67,'Actual new physical geodesic distance-two states');
assert.equal(1+oneMove.size+genuinelyNew.length,78,'Closed physical ball radius at most two');
let matchedPhysicalPairs=[],possibleTies=[],pairHolds=[];
for(const [first,second,relativeKey] of possible){
 const intervention=[first,second],entry={word:intervention.join(' '),physical_relative_action_hash:crypto.createHash('sha256').update(relativeKey).digest('hex'),arms:[]};
 for(let arm=0;arm<2;arm++){
  const original=starts[arm];
  const child=compose(compose(original.state,FACE[first]),FACE[second]);
  assert(dr(child),'Every two-action synthetic state stays in true DR subgroup');
  const actual=phaseState(stickerAfter([...scramble,...signedWord([...original.prefix,...intervention])]),'FB');
  assert.equal(key(actual),key(child),'Source original sticker vs cubie action');
  actualReplays++;
  const solved=solve10(child,arm,intervention);
  entry.arms.push(solved);
 }
 if(entry.arms.every(x=>x.exact_10_DR_solved_distance!==null)){
  const costGap=1+entry.arms[1].exact_10_DR_solved_distance-entry.arms[0].exact_10_DR_solved_distance;
  entry.exact_source_raw_cost_difference_alt_minus_main=costGap;
  if(costGap===0)possibleTies.push(entry.word);
  assert(costGap>=0,'Two same legal physical moves must have nonnegative gap from original 4-minus-2r bound');
 }else{
  entry.exact_source_raw_cost_difference_alt_minus_main=null;
  pairHolds.push(entry.word);
 }
 matchedPhysicalPairs.push(entry);
}
const tieVerdict=possibleTies.length?'PHYSICAL_TIE_WITNESSED':pairHolds.length?'COMPUTE_HOLD_NO_EXCLUSION':'NO_RADIUS_TWO_RAW_TIE_IN_DR_GRAMMAR';
const maxNodes=[...cache[0].values(),...cache[1].values()].reduce((m,x)=>Math.max(m,x.IDA_nodes),0);
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P1_PREREG_SOURCE_MATCHED_2STEP_EXACT_DR_TIE_COURT',
 predeclared_protocol:'data/cuberev-023/p1_matched_radius2_preregistration.json',
 original_authored_miao_states_verified:true,
 all_ordered_two_action_words:ordered,
 unique_actual_action_endpoints:[...actionProducts.keys()].length,
 unique_new_geodesic_distance_two_actions:genuinelyNew.length,
 complete_ball_radius_two_states:1+oneMove.size+genuinelyNew.length,
 normalized_to_identity_or_one_turn_words:reducedOrIdentity,
 exact_full_alphabet_first_move_tie_exclusion_count:noncritical,
 necessary_first_step_set:[...possibleFirst],
 selected_conditionally_possible_ordered_words:possible.length,
 selected_source_full_cubie_pairs:matchedPhysicalPairs.length,
 actual_sticker_replays:actualReplays,
 // The following two detailed counters are written explicitly below for strict reproducibility.
 unique_children_with_exact_per_arm:[...[0,1].map(i=>[...cache[i].values()].filter(x=>x.exact_10_DR_solved_distance!==null).length)],
 unique_children_resource_HOLD_per_arm:[...[0,1].map(i=>[...cache[i].values()].filter(x=>x.resource_hold).length)],
 visits_total:allNodes,maximum_nodes_one_child:maxNodes,
 early_tie_candidates:possibleTies,unresolved_possible_tie_words:pairHolds,
 strict_exact_DR_matched_radius2_tie_verdict:tieVerdict,
 all18_match_pair_cost_gap_only_analytic_interval:[0,8],
 all18_exact_radius2_children_NOT_COMPUTED:true,
 human_consideration_of_any_synthetic_word_NOT_OBSERVED:true,
 pairs:matchedPhysicalPairs
},null,2));
