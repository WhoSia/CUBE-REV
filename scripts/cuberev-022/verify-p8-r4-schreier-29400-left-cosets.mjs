/**
 * CUBE-REV 0.22 P8-R4: complete 29,400-left-coset Schreier action on exact Rubik DR subgroup.
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
const actualScramble=tokenize(ledger.normal_scramble),certificates=[];
for(const row of ledger.eo_dr_pairs){
 if(row.id==='riabov_other_2')continue;
 const source=[...tokenize(row.eo_prefix),...tokenize(row.dr_extension)];
 const original=stickerAfter([...actualScramble,...source]);
 const axes=Object.keys(ROT).filter(a=>dr(phaseState(original,a)));assert.equal(axes.length,1);
 const axis=axes[0],sourceState=phaseState(original,axis),idx=getId(enc(sourceState));
 const d=dist[idx],inverseWord=[];
 let cur=idx;
 while(cur!==0){
  const a=DR[via[cur]];
  inverseWord.push(INVERSE[a]);cur=parents[cur];
 }
 assert.equal(inverseWord.length,d);
 let physical=sourceState;
 for(const t of inverseWord)physical=compose(physical,FACE[t]);
 assert(H.has(enc(physical)),'Path does not physically reach H');
 const realSuffix=inverseWord.map(t=>MAP[axis].frame_to_original[t[0]]+t.slice(1));
 const actualEnd=phaseState(stickerAfter([...actualScramble,...source,...realSuffix]),axis);
 assert.equal(key(actualEnd),key(physical));
 certificates.push({id:row.id,axis,source_parse:row.declared_mode,exact_DR_to_HTR_HTM:d,
  canonical_shortest_contact_suffix:inverseWord.join(' '),
  actual_face_shortest_contact_suffix:realSuffix.join(' '),
  source_physical_hash:crypto.createHash('sha256').update(key(sourceState)).digest('hex'),
  end_in_verified_HTR_group:true,
  full_original_sticker_crosschecked:true});
}
assert.equal(certificates.length,5);
assert.equal(certificates.find(x=>x.id==='miao_main').exact_DR_to_HTR_HTM,5);
assert.equal(certificates.find(x=>x.id==='riabov_main').exact_DR_to_HTR_HTM,5);
assert.equal(certificates.find(x=>x.id==='miao_alternative_from_same_eo').exact_DR_to_HTR_HTM,7);
assert.equal(certificates.find(x=>x.id==='riabov_other_1').exact_DR_to_HTR_HTM,7);
const r3=certificates.find(x=>x.id==='riabov_other_3');
assert(r3.exact_DR_to_HTR_HTM>=9&&r3.exact_DR_to_HTR_HTM<=13);
const result={
 marker:'CUBE_REV_022_P8_R4_ACTUAL_FULL_DR_GROUP_29400_LEFT_COSET_SCHREIER_BFS',
 source_condition:'P7 source grades remain; Riabov Other cases conditional',
 HTR_actual_subgroup_size:H.size,
 DR_group_order:19508428800,
 independent_index_quotient:19508428800/H.size,
 corner_H_orbits:cornerOrbits,edge_H_orbits:edgeOrbits,
 orbit_occupancy_bucket_count:idBuckets.size,
 residual_coset_classes_per_bucket:6,
 left_coset_count:reps.length,
 graph_directed_generator_edges:reps.length*DR.length,
 max_bucket_size:maxBucket,
 representative_independence_checks:covariance,
 subgroup_membership_checks:memberCheckCount,
 graph_distance_histogram:hist,
 maximum_HTR_contact_distance_over_DR_cosets:hist.length-1,
 source_certs:certificates,
 source_Riabov_other3_H_contact_exact:r3.exact_DR_to_HTR_HTM,
 source_Riabov_other3_previously_closed_interval:[9,13],
 original_full_cube_verified:true,
 no_assertion_of_identity_solved_distance_from_cosets:true,
 no_unrestricted_FMC_global_optimality:true,
 historic_human_search_mechanism_unidentified:true
};
console.log(JSON.stringify(result,null,2));
