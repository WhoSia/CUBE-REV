/**
 * CUBE-REV 0.22 P8-R3: reverse projection BFS and source-to-solved optimal DR-grammar IDA*.
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
const fixed=JSON.parse(fs.readFileSync('data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json','utf8'));
const ids=['miao_main','miao_alternative_from_same_eo'];
const source=ids.map(id=>{
 const r=ledger.eo_dr_pairs.find(x=>x.id===id),known=fixed.rows.find(x=>x.id===id);
 assert.equal(r.declared_mode,'CONTIGUOUS_NORMAL_SIDE_PREFIX');
 const authored=[...tokenize(r.eo_prefix),...tokenize(r.dr_extension)];
 const real=stickerAfter([...scramble,...authored]);
 const axes=Object.keys(ROT).filter(a=>dr(phaseState(real,a)));assert.deepEqual(axes,['FB']);
 const s=phaseState(real,'FB');
 const c=rank(s.cp),e=rank(s.ep.slice(0,8)),t=rank(s.ep.slice(8).map(x=>x-8));
 const hC=corner.dist[c*E4+t],hE=edge.dist[e*E4+t],h=Math.max(hC,hE);
 assert.equal(known.exact_minimum_DR_to_solved,tokenize(known.actual_phase2_word).length);
 assert(h<=known.exact_minimum_DR_to_solved);
 const cornerOrbit=new Set([0,2,5,7]),edgeOrbit=new Set([0,2,4,6]);
 const mask=(p,orbit)=>p.reduce((bits,value,i)=>bits|(orbit.has(value)?(1<<i):0),0);
 return {
  id,source_line:r.source_lines,authored_EO:tokenize(r.eo_prefix),authored_DR:tokenize(r.dr_extension),
  literal_prefix_HTM:authored.length,
  full_physical_SHA256:crypto.createHash('sha256').update(key(s)).digest('hex'),
  verified_axis:'FB',
  corner_4of8_H_orbit_occupancy_mask:mask(s.cp,cornerOrbit),
  edge_4of8_H_orbit_occupancy_mask:mask(s.ep.slice(0,8),edgeOrbit),
  PDB_corner_E_projection_lower_bound:hC,
  PDB_UDedge_E_projection_lower_bound:hE,
  max_of_two_admissible_lower_bounds:h,
  exact_restricted_DR_solution_HTM:known.exact_minimum_DR_to_solved,
  full_joint_cubie_abstraction_gap:known.exact_minimum_DR_to_solved-h,
  corner_position_perm:s.cp,
  edge_position_perm:s.ep,
  real_full_scramble_physically_solvable_by_fixture:solvedUpToRotation(stickerAfter([...scramble,...authored,...tokenize(known.actual_phase2_word)]))
 };
});
assert(source.every(x=>x.real_full_scramble_physically_solvable_by_fixture));
const [a,b]=source;
const w1=[...a.authored_EO,...a.authored_DR],w2=[...b.authored_EO,...b.authored_DR];
let common=0;while(common<Math.min(w1.length,w2.length)&&w1[common]===w2[common])common++;
assert.equal(common,6);
assert.deepEqual(a.authored_EO,b.authored_EO);
assert.notEqual(a.full_physical_SHA256,b.full_physical_SHA256);
const nChanges=(x,y)=>x.reduce((n,v,i)=>n+(v!==y[i]?1:0),0);
console.log(JSON.stringify({
 marker:'CUBE_REV_022_P8_R5_MIAO_SAME_EO_BRANCH_PHYSICAL_PROJECTION_CROSS_EXAM',
 source_status:'Two actual written same-EO DR alternatives, both source-linear; not proof of temporal consideration order',
 independently_observed_source_claim:'Miao reconstruction attempt1 line45 says extend from the EO; source page publicly reports alternative and main',
 literal_identical_EO_turns:a.authored_EO.join(' '),
 longest_common_actual_authored_prefix_HTM:common,
 first_diverging_HTM_position_1indexed:common+1,
 first_diverging_moves:[w1[common],w2[common]],
 verified_source_states:source,
 full_state_coordinate_disagreement:{corner_position_slots:nChanges(a.corner_position_perm,b.corner_position_perm),edge_position_slots:nChanges(a.edge_position_perm,b.edge_position_perm)},
 main_vs_alt_restricted_suffix_optimal_cost_difference:b.exact_restricted_DR_solution_HTM-a.exact_restricted_DR_solution_HTM,
 main_vs_alt_authored_DR_length_difference:b.authored_DR.length-a.authored_DR.length,
 exact_total_cost_difference:(b.literal_prefix_HTM+b.exact_restricted_DR_solution_HTM)-(a.literal_prefix_HTM+a.exact_restricted_DR_solution_HTM),
 proven_all18_caveat:'The physical metrics calculated here concern 10-generator DR subgroup projections; all-18 optimal costs are independently established in R4 Actions #38079967359',
 caution:'Projection gap is an exact residual relative to a chosen admissible heuristic, NOT a unique causal mediator, neural mechanism, or information metric',
 human_search_timeline_unobserved:true
},null,2));
