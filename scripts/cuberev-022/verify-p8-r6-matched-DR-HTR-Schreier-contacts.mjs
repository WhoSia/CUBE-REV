/**
 * CUBE-REV 0.22 P8-R6: source-faithful matched DR one-step HTR quotient interventions with source provenance.
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

const START=enc(solved),H=new Set([START]),queueH=[START];
function applyEnc(st,m){let t='';for(let i=0;i<8;i++)t+=st[m.cp[i]];for(let i=0;i<12;i++)t+=st[8+m.ep[i]];return t;}
for(let at=0;at<queueH.length;at++){
 const x=queueH[at];
 for(const word of HALF){
  const y=applyEnc(x,FACE[word]);if(H.has(y))continue;
  H.add(y);queueH.push(y);
 }
 if(queueH.length>663552)throw Error('HTR_SUBGROUP_OVERRUN');
}
assert.equal(H.size,663552);
const orbit=(count,getMove)=>{
 const seen=new Set(),all=[];
 for(let k=0;k<count;k++){
  if(seen.has(k))continue;
  const q=[k];seen.add(k);
  for(let p=0;p<q.length;p++)for(const w of HALF){
   const nxt=getMove(FACE[w])[q[p]];
   if(!seen.has(nxt)){seen.add(nxt);q.push(nxt);}
  }
  q.sort((a,b)=>a-b);all.push(q);
 }
 return all.sort((a,b)=>a[0]-b[0]);
};
const cornerOrbits=orbit(8,m=>m.cp),edgeOrbits=orbit(12,m=>m.ep);
assert.equal(cornerOrbits.length,2,'HTR corner 4+4 orbit partition');
assert(cornerOrbits.every(x=>x.length===4));
assert.deepEqual(edgeOrbits.map(x=>x.length),[4,4,4]);
const cornerSet=new Set(cornerOrbits[0]),edgeSet=new Set(edgeOrbits.find(x=>x[0]<8));
assert.equal(edgeSet.size,4);
function bucket(st){
 let c=0,e=0;for(let i=0;i<8;i++){
  if(cornerSet.has(st.charCodeAt(i)-65))c|=1<<i;
  if(edgeSet.has(st.charCodeAt(8+i)-65))e|=1<<i;
 }
 return c*256+e;
}
function ratioInH(candidate,rep){
 const h=new Array(20);
 for(let i=0;i<8;i++)h[rep.charCodeAt(i)-65]=candidate[i];
 for(let i=0;i<12;i++)h[8+rep.charCodeAt(8+i)-65]=candidate[8+i];
 assert(h.every(x=>x!==undefined));
 return H.has(h.join(''));
}
const reps=[START],idBuckets=new Map([[bucket(START),[0]]]),dist=[0],parents=[-1],via=[-1];
const EDGES=new Uint16Array(29400*DR.length);
let memberCheckCount=0,maxBucket=1;
function getId(candidate) {
 const k=bucket(candidate),ids=idBuckets.get(k)||[];
 for(const idx of ids){memberCheckCount++;if(ratioInH(candidate,reps[idx]))return idx;}
 const next=reps.length;
 if(next>=29400)throw Error('G_H_LEFT_COSET_EXCEEDED_29400');
 ids.push(next);idBuckets.set(k,ids);reps.push(candidate);
 maxBucket=Math.max(maxBucket,ids.length);
 return next;
}
const hist=[1];
for(let at=0;at<reps.length;at++){
 const representative=reps[at],d=dist[at];
 for(let a=0;a<DR.length;a++){
  const next=applyEnc(representative,FACE[DR[a]]);
  const idx=getId(next);
  EDGES[at*DR.length+a]=idx;
  if(idx>=dist.length){
   dist[idx]=d+1;parents[idx]=at;via[idx]=a;
   hist[d+1]=(hist[d+1]||0)+1;
  }
 }
}
assert.equal(reps.length,29400,'Exact Schreier left coset index');
assert.equal(idBuckets.size,4900,'70 corner orbit masks x 70 UD edge orbit masks');
assert.equal(maxBucket,6);
assert([...idBuckets.values()].every(v=>v.length===6),'Six residual coset states in each occupancy bucket');
assert.equal(hist.reduce((a,b)=>a+b,0),29400);
const INVERSE={"U":"U'","U'":"U","D":"D'","D'":"D","U2":"U2","D2":"D2","R2":"R2","L2":"L2","F2":"F2","B2":"B2"};
for(let id=0;id<reps.length;id++)for(let a=0;a<DR.length;a++){
 const next=EDGES[id*DR.length+a],other=DR.indexOf(INVERSE[DR[a]]);
 assert.equal(EDGES[next*DR.length+other],id,'Schreier inverse action broken');
 assert(Math.abs(dist[id]-dist[next])<=1,'Distance Lipschitz violation');
}
const redundantCheck=1000;
const hSample=queueH.filter((_,i)=>i%Math.floor(queueH.length/redundantCheck)===0).slice(0,redundantCheck);
function leftMultiply(h,rep){
 // The physical permutation after left h then right rep equals h[rep[i]].
 let out='';for(let i=0;i<8;i++)out+=h[rep.charCodeAt(i)-65];
 for(let i=0;i<12;i++)out+=h[8+rep.charCodeAt(8+i)-65];return out;
}
let covariance=0;
for(let ci=0;ci<Math.min(500,reps.length);ci++){
 const id=(ci*59)%reps.length,h=hSample[(ci*31)%hSample.length];
 const alt=leftMultiply(h,reps[id]);
 assert.equal(getId(alt),id,'Left coset h*g agreement');
 const a=ci%DR.length;
 assert.equal(getId(applyEnc(alt,FACE[DR[a]])),EDGES[id*DR.length+a],'Schreier rep-independence');
 covariance++;
}
assert.equal(reps.length,29400);

const scramble=tokenize(ledger.normal_scramble);
const sourceNames=['miao_main','miao_alternative_from_same_eo'];
const base=sourceNames.map(id=>{
 const row=ledger.eo_dr_pairs.find(x=>x.id===id);
 assert(row&&row.declared_mode==='CONTIGUOUS_NORMAL_SIDE_PREFIX');
 const prefix=[...tokenize(row.eo_prefix),...tokenize(row.dr_extension)];
 const real=stickerAfter([...scramble,...prefix]);
 assert.deepEqual(Object.keys(ROT).filter(x=>dr(phaseState(real,x))),['FB']);
 const s=phaseState(real,'FB'),groupCoset=getId(enc(s));
 return {id,row,prefix,state:s,baseHtr:dist[groupCoset],baseIndex:groupCoset};
});
assert.deepEqual(base.map(x=>x.baseHtr),[5,7]);
const records=[];
for(const m of DR){
 const o={matched_canonical_DR_action:m,arms:[]};
 for(const subject of base){
  const realMove=MAP.FB.frame_to_original[m[0]]+m.slice(1);
  const next=compose(subject.state,FACE[m]);
  assert(dr(next));
  const actual=phaseState(stickerAfter([...scramble,...subject.prefix,realMove]),'FB');
  assert.equal(key(next),key(actual),'every synthetic state must be original full-sticker replayed');
  const idx=getId(enc(next)),h=dist[idx];
  assert(Math.abs(h-subject.baseHtr)<=1,'HTR exact quotient distance must be 1-Lipschitz');
  const expectedTransition=EDGES[subject.baseIndex*DR.length+DR.indexOf(m)];
  assert.equal(idx,expectedTransition,'actual right action must equal Schreier graph');
  o.arms.push({id:subject.id,authored_prefix_HTM:subject.prefix.length,
   synthetic_not_authored_by_human:true,
   canonical_matched_action:m,original_face_action:realMove,
   exact_HTR_distance:h,
   original_source_exact_HTR_distance:subject.baseHtr,
   subgroup_coset_vertex_id:idx,
   real_full_sticker_replay_verified:true});
 }
 o.exact_HTR_distance_advantage_alt_minus_main=o.arms[1].exact_HTR_distance-o.arms[0].exact_HTR_distance;
 records.push(o);
}
const gaps=records.map(x=>x.exact_HTR_distance_advantage_alt_minus_main);
assert.equal(records.length,10);
assert.equal(reps.length,29400);
console.log(JSON.stringify({
 marker:'CUBE_REV_022_P8_R6_MATCHED_SOURCE_DR_FULL_SCHREIER_HTR_CONTACT_NEIGHBORS',
 original_real_DR_group_cardinality:19508428800,
 HTR_subgroup_physical_cardinality:H.size,
 complete_left_coset_count:reps.length,
 exact_10DR_generator_transition_count:EDGES.length,
 base_real_source_HTR_costs:base.map(x=>x.baseHtr),
 same_physical_intervention_on_two_source_reconstructed_FB_DR_endpoints:true,
 all_matched_physical_state_replays_verified:true,
 synthetic_neighbor_not_human_observed:true,
 matched_pairs:records,
 exact_HTR_gap_summary:{min:Math.min(...gaps),max:Math.max(...gaps),
  strictly_alt_worse:records.filter(x=>x.exact_HTR_distance_advantage_alt_minus_main>0).length,
  equal:records.filter(x=>x.exact_HTR_distance_advantage_alt_minus_main===0).length},
 subgroup_quotient_is_NOT_solved_distance_proof:true,
 no_human_choice_mechanism_IDENTIFIED:true
},null,2));
