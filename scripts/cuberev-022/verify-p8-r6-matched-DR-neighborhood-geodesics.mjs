/**
 * CUBE-REV 0.22 P8-R6: exactly matched DR one-step interventions on sourced Miao EO branch endpoints.
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

const scramble=tokenize(ledger.normal_scramble);
const fixture=JSON.parse(fs.readFileSync('data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json','utf8'));
const subjects=['miao_main','miao_alternative_from_same_eo'].map(id=>{
 const source=ledger.eo_dr_pairs.find(x=>x.id===id),known=fixture.rows.find(x=>x.id===id);
 assert(source&&known&&source.declared_mode==='CONTIGUOUS_NORMAL_SIDE_PREFIX');
 const authored=[...tokenize(source.eo_prefix),...tokenize(source.dr_extension)];
 const cube=stickerAfter([...scramble,...authored]);
 assert.deepEqual(Object.keys(ROT).filter(a=>dr(phaseState(cube,a))),['FB']);
 const state=phaseState(cube,'FB');
 const oldSuffix=tokenize(known.canonical_phase2_word);
 assert.equal(oldSuffix.length,known.exact_minimum_DR_to_solved);
 assert.equal(known.axis,'FB');
 assert(solvedUpToRotation(stickerAfter([...scramble,...authored,...tokenize(known.actual_phase2_word)])));
 return {id,source,authored,state,known,oldSuffix};
});
assert.deepEqual(subjects[0].authored.slice(0,4),subjects[1].authored.slice(0,4));
const baseFull=[9,12],baseCost=[19,23];
assert.equal(subjects[0].known.exact_minimum_DR_to_solved,9);
assert.equal(subjects[1].known.exact_minimum_DR_to_solved,12);
const firstOptimalMoves=subjects.map(x=>x.oldSuffix[0]);
const HMAX=10,visitationBudget=6000000;
const opposite={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
const observations=[];
for(let a=0;a<DR.length;a++){
 const word=DR[a],pair={matched_canonical_DR_intervention:word,arms:[]};
 for(let arm=0;arm<2;arm++){
  const q=subjects[arm],base=baseFull[arm],child=compose(q.state,FACE[word]);
  assert(dr(child),'genuine DR group closure');
  const real=MAP.FB.frame_to_original[word[0]]+word.slice(1);
  const sticker=phaseState(stickerAfter([...scramble,...q.authored,real]),'FB');
  assert.equal(key(sticker),key(child),'Actual authored prefix and synthetic intervention must match full original sticker oracle');
  const c=rank(child.cp),e=rank(child.ep.slice(0,8)),s=rank(child.ep.slice(8).map(x=>x-8));
  const hc=corner.dist[c*E4+s],he=edge.dist[e*E4+s],h=Math.max(hc,he);
  const lower=Math.max(base-1,h),upper=base+1;
  assert(lower<=upper);
  const armRec={
   id:q.id,source_status:'SOURCE_AUTHORED_PREFIX_PLUS_SYNTHETIC_MATCHED_ONE_MOVE',
   historical_source_cannot_be_extended_to_this_word:true,
   literal_authored_prefix_HTM:q.authored.length,
   canonical_one_move:word,actual_one_move:real,
   original_full_cubie_SHA256:crypto.createHash('sha256').update(key(child)).digest('hex'),
   projected_corner_ESlice_exact_lower:hc,projected_UDedge_ESlice_exact_lower:he,
   admissible_max_joint_lower:h,
   triangle_geodesic_lower:base-1,
   original_18_HTM_distance_certified_interval:[base-1,base+1],
   DR_geodesic_search_started_at:lower,
   DR_geodesic_search_upper:upper,
   new_literal_plus_one_prefix_raw_HTM:q.authored.length+1
  };
  let proof=null,spent=0,attempts=[],resourceHold=false;
  if(lower===upper){proof={exact:lower,warrant:'MATCHED_LIPSCHITZ_PLUS_PDB_LOWER_AND_UPPER'};}
  else if(word===q.oldSuffix[0]){proof={exact:base-1,warrant:'EXACT_FIRST_MOVE_ON_PREVIOUSLY_CERTIFIED_SHORTEST_GEODESIC'};}
  if(!proof){
   const path=[];
   function dfs(cc,ee,ss,g,depthLimit,lastFace){
    if(++spent>visitationBudget){resourceHold=true;return false;}
    if(g+Math.max(corner.dist[cc*E4+ss],edge.dist[ee*E4+ss])>depthLimit)return false;
    if(cc===0&&ee===0&&ss===0){proof={exact:g,warrant:'IDA_EXHAUSTIVE_PREVIOUS_DEPTHS'};proof.word=path.slice(0,g).join(' ');return true;}
    if(g===depthLimit)return false;
    for(let i=0;i<DR.length;i++){
     const face=DR[i][0];
     if(lastFace!==null&&(face===lastFace||(opposite[lastFace]===face&&face<lastFace)))continue;
     path[g]=DR[i];
     if(dfs(TC[cc*M+i],TE[ee*M+i],TS[ss*M+i],g+1,depthLimit,face))return true;
     if(resourceHold)return false;
    }
    return false;
   }
   for(let bound=lower;bound<=upper;bound++){
    const prior=spent,ok=dfs(c,e,s,0,bound,null);
    attempts.push({bound,nodes:spent-prior,closed:!resourceHold,has_solution:ok});
    if(ok||resourceHold)break;
   }
  }
  const best=proof?.exact??null;
  if(best!==null) {
   assert(best>=base-1&&best<=base+1);
   const exactSuffix=proof.word?tokenize(proof.word):
     (word===q.oldSuffix[0]?q.oldSuffix.slice(1):
      null);
   if(exactSuffix){
    assert.equal(exactSuffix.length,best);
    const actual=exactSuffix.map(w=>MAP.FB.frame_to_original[w[0]]+w.slice(1));
    assert(solvedUpToRotation(stickerAfter([...scramble,...q.authored,real,...actual])));
    armRec.valid_original_54_sticker_shortest_physical_witness=actual.join(' ');
   } else if(proof.warrant.includes('LIPSCHITZ')) {
    armRec.valid_original_54_sticker_shortest_physical_witness=null;
    armRec.solution_existence_entailed_by_neighbor_metric_proof=true;
   }
  }
  armRec.exact_DR10_geodesic_after_synthetic_move=best;
  armRec.exact_DR10_certificate=proof?.warrant??'RESOURCE_HOLD_TRIANGLE_AND_PDB_BOUNDS';
  armRec.search_nodes=spent;armRec.search_attempts=attempts;armRec.hit_resource_cap=resourceHold;
  armRec.DR10_exact_or_interval=best===null?[lower,upper]:[best,best];
  armRec.DR10_total_authored_plus_synthetic_plus_solve_exact_or_interval=[q.authored.length+1+(best??lower),q.authored.length+1+(best??upper)];
  pair.arms.push(armRec);
 }
 const x=pair.arms[0],y=pair.arms[1];
 const geodesicInterval=[y.DR10_exact_or_interval[0]-x.DR10_exact_or_interval[1],y.DR10_exact_or_interval[1]-x.DR10_exact_or_interval[0]];
 const costInterval=[
  y.DR10_total_authored_plus_synthetic_plus_solve_exact_or_interval[0]-x.DR10_total_authored_plus_synthetic_plus_solve_exact_or_interval[1],
  y.DR10_total_authored_plus_synthetic_plus_solve_exact_or_interval[1]-x.DR10_total_authored_plus_synthetic_plus_solve_exact_or_interval[0]];
 pair.matched_DR10_total_difference_interval_alternative_minus_main=costInterval;
 pair.matched_18_all_HTM_total_difference_provable=[2,6];
 pair.projection_ranks_alternative_easier=(y.admissible_max_joint_lower<x.admissible_max_joint_lower);
 pair.reversal_proven_under_DR10=(pair.projection_ranks_alternative_easier&&geodesicInterval[0]>0);
 pair.reversal_proven_under_all18_from_triangle=(pair.projection_ranks_alternative_easier&& (baseFull[1]-1)>(baseFull[0]+1));
 assert(pair.matched_18_all_HTM_total_difference_provable[0]>=2);
 assert(costInterval[0]>=2,'all matched source-branched perturbations preserve strict dominance under DR group');
 observations.push(pair);
}
const exactPairs=observations.filter(p=>p.arms.every(x=>x.exact_DR10_geodesic_after_synthetic_move!==null));
const reversals=observations.filter(x=>x.reversal_proven_under_DR10);
const result={
 marker:'CUBE_REV_022_P8_R6_SOURCE_ANCHORED_MATCHED_DR_PHYSICAL_NEIGHBORHOOD',
 mode:'Two actual human authored Miao EO/DR branches, then synthetically perturb each endpoint with the SAME one of ten legal canonical DR-preserving face moves',
 declared_source_not_historical_human_consideration:true,
 common_actual_EO:'L2 F\u0027 L D',
 original_source_DR_costs:[9,12],
 original_source_18_HTM_costs:[9,12],
 original_total_actions:[19,23],
 neighborhood_generator_actions:DR,
 matched_one_step_pair_count:observations.length,
 actual_synthetic_physical_states_examined:observations.length*2,
 exact_DR_geodesic_matched_pairs:exactPairs.length,
 PDB_reverse_ranking_matched_pairs:observations.filter(x=>x.projection_ranks_alternative_easier).length,
 DR_cost_reverse_ranking_proved_matched_pairs:reversals.length,
 exact_DR_geodesic_cost_gap_distribution:exactPairs.map(x=>({move:x.matched_canonical_DR_intervention,interval:x.matched_DR10_total_difference_interval_alternative_minus_main})),
 all18_cost_robust_bound:'For each of the ten matched legal one-step DR interventions, by 1-Lipschitz all-18 geodesic, updated whole-prefix completion alternative minus main lies in [2,6] raw actions regardless of any still uncomputed neighbor exact all-18 distances.',
 all18_exact_neighbor_values_NOT_calculated:true,
 statistical_sample_claim_NO:'These are the ten full legal one-step DR generator interventions, not independent human observations or a random sample of cubes.',
 matched_interventions:observations,
 neither_PDB_residual_nor_corner_mask_identified_as_unique_causal_mechanism:true,
 follow_on_zero_history_human_process_claim:true
};
console.log(JSON.stringify(result,null,2));
