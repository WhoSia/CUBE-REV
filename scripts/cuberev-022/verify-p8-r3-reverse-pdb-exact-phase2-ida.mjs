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
const permitted=new Set(['miao_main','riabov_main','miao_alternative_from_same_eo','riabov_other_1','riabov_other_3']);
const upperCaps={miao_main:11,riabov_main:11,miao_alternative_from_same_eo:12,riabov_other_1:16,riabov_other_3:20};
const face=DR.map(x=>x[0]),opposite={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
const solveCache=new Map(),reports=[];
for(const row of ledger.eo_dr_pairs.filter(x=>permitted.has(x.id))){
 const authored=[...tokenize(row.eo_prefix),...tokenize(row.dr_extension)];
 const original=stickerAfter([...scramble,...authored]);
 const axes=Object.keys(ROT).filter(a=>dr(phaseState(original,a)));
 assert.equal(axes.length,1);
 const axis=axes[0],s=phaseState(original,axis),str=key(s);
 let proof=solveCache.get(str);
 if(!proof){
  const c0=rank(s.cp),e0=rank(s.ep.slice(0,8)),t0=rank(s.ep.slice(8).map(x=>x-8));
  const h=(c,e,t)=>Math.max(corner.dist[c*E4+t],edge.dist[e*E4+t]);
  const rootLower=h(c0,e0,t0);
  assert(rootLower!==UNVIS);
  const CAP=20000000,cap=upperCaps[row.id],path=[],bounds=[];
  let visited=0,stopped=false,found=null;
  function dfs(c,e,t,depth,limit,last){
   if(visited++>=CAP){stopped=true;return false;}
   if(depth+h(c,e,t)>limit)return false;
   if(c===0&&e===0&&t===0){found=path.slice(0,depth);return true;}
   if(depth>=limit)return false;
   const ic=c*M,ie=e*M,it=t*M;
   for(let a=0;a<M;a++){
    const f=face[a];
    if(last!==null&&(f===last||(opposite[last]===f&&f<last)))continue;
    path[depth]=a;
    if(dfs(TC[ic+a],TE[ie+a],TS[it+a],depth+1,limit,f))return true;
    if(stopped)return false;
   }
   return false;
  }
  let optimum=null;
  for(let bound=rootLower;bound<=cap;bound++){
   const prev=visited,ok=dfs(c0,e0,t0,0,bound,null);
   bounds.push({depth:bound,nodes:visited-prev,outcome:ok?'FOUND':stopped?'RESOURCE_LIMIT':'EXHAUSTED'});
   if(ok){optimum=bound;break;}
   if(stopped)break;
  }
  const canonical=found?.map(a=>DR[a])??null;
  const physical=canonical?.map(m=>MAP[axis].frame_to_original[m[0]]+m.slice(1))??null;
  const completed=physical?[...authored,...physical]:null;
  if(completed)assert(solvedUpToRotation(stickerAfter([...scramble,...completed])));
  proof={
   initial_admissible_lower_bound:rootLower,
   exact_minimum_DR_preserving_continuation_to_solved:optimum,
   bounded_exhaustion_warrant:optimum===null?'HOLD':bounds.filter(b=>b.depth<optimum).every(b=>b.outcome==='EXHAUSTED')?'PASS':'FAIL',
   effort_nodes:visited,resource_cap_reached:stopped,attempts:bounds,
   optimal_canonical_DR_phase_word:canonical?.join(' ')??null,
   actual_legal_face_turns:physical?.join(' ')??null,
   full_source_prefix_plus_continuation_solution:completed?.join(' ')??null,
   complete_original_full_sticker_solves:completed!==null
  };
  solveCache.set(str,proof);
 }
 // A reused physical-state certificate never supplies the earlier author's literal prefix.
 // Reconstruct and independently replay each person's own authentic source word.
 const reusedSuffix=proof.actual_legal_face_turns?tokenize(proof.actual_legal_face_turns):null;
 const sourceSpecificSolution=reusedSuffix?[...authored,...reusedSuffix]:null;
 if(sourceSpecificSolution)assert(solvedUpToRotation(stickerAfter([...scramble,...sourceSpecificSolution])));
 const joinMayMerge=!!(reusedSuffix?.length&&authored.at(-1)[0]===reusedSuffix[0][0]);
 reports.push({id:row.id,source_parse:row.declared_mode,axis,source_prefix_HTM:authored.length,
  source_DR_hash:crypto.createHash('sha256').update(str).digest('hex'),
  ...proof,
  full_source_prefix_plus_continuation_solution:sourceSpecificSolution?.join(' ')??null,
  complete_original_full_sticker_solves:sourceSpecificSolution!==null,
  prefix_continuation_boundary_has_adjacent_same_face:joinMayMerge,
  raw_action_count_not_necessarily_normalized_FMC_HTM:joinMayMerge,
  exact_total_HTM_restricted:proof.exact_minimum_DR_preserving_continuation_to_solved===null?null:authored.length+proof.exact_minimum_DR_preserving_continuation_to_solved});
}
assert.equal(reports.length,5);
const a=reports.find(x=>x.id==='miao_main'),b=reports.find(x=>x.id==='riabov_main'),c=reports.find(x=>x.id==='miao_alternative_from_same_eo');
assert.equal(a.source_DR_hash,b.source_DR_hash);
assert.equal(a.exact_minimum_DR_preserving_continuation_to_solved,b.exact_minimum_DR_preserving_continuation_to_solved);
console.log(JSON.stringify({
 marker:'CUBE_REV_022_P8_R3_DUAL_BACKWARD_PROJECTION_PDB_SOURCE_PHASE2_EXACT_IDA',
 actual_cube_model:'Original full-sticker, only ten real DR-preserving HTM moves with individually fixed tested phase axis',
 dual_backward_PDB:[{name:corner.name,size:K,diameter:corner.maximumDepth,hist:corner.depthHistogram},{name:edge.name,size:K,diameter:edge.maximumDepth,hist:edge.depthHistogram}],
 mathematical_warrant:'Both PDBs are exact reverse shortest projected distances; max is an admissible heuristic; iterative deepening exhausts all smaller lengths if not resource-capped. Adjacent same face turns shorten, reversed opposite-face turns commute and can be normalized.',
 resource_ceiling_per_physical_endpoint:20000000,
 results:reports,
 same_EO_two_authored_alternatives_conditional_dominance:(a.exact_total_HTM_restricted!==null&&c.exact_total_HTM_restricted!==null)?{main:a.exact_total_HTM_restricted,alternative:c.exact_total_HTM_restricted,main_strictly_better:a.exact_total_HTM_restricted<c.exact_total_HTM_restricted}:null,
 entire_unrestricted_FMC_minimum_NOT_proven:true,
 riabov_other_parsing_still_conditional:true,
 human_actual_search_trace_NOT_identified:true
},null,2));
