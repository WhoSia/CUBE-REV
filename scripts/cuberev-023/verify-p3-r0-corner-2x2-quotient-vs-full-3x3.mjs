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


const sorted=[...G.visited.entries()].sort((a,b)=>a[1].length-b[1].length);
const cornerSeen=new Map(),edgeSeen=new Map(),atDepth=[],collisions=[];
let index=0,cornerAliasCount=0,edgeAliasCount=0,crossEdgeOrientationAliases=0;
for(const [k,code] of sorted){
 const depth=code.length;
 const corner=k.slice(0,16);
 const edge=k.slice(16,40);
 const prior=cornerSeen.get(corner);
 if(prior){
  if(prior.whole!==k){
   cornerAliasCount++;
   if(collisions.length<6){
    const a=decodeWord(prior.word),b=decodeWord(code);
    assert.equal(cubieAfter(a).cp.join(','),cubieAfter(b).cp.join(','));
    assert.equal(cubieAfter(a).co.join(','),cubieAfter(b).co.join(','));
    const physicalA=cubieAfter(a),physicalB=cubieAfter(b);
    assert(key(physicalA)!==key(physicalB));
    assert(physicalA.ep.join(',')!==physicalB.ep.join(',')||physicalA.eo.join(',')!==physicalB.eo.join(','));
    collisions.push({first_word:a.join(' '),second_word:b.join(' '),
      first_HTM:a.length,second_HTM:b.length,
      same_physical_corner_permutation_and_orientation:true,
      different_actual_edge_permutation_or_orientation:true,
      corner_projection_fingerprint:crypto.createHash('sha256').update(corner).digest('hex'),
      first_real_full_cubie_SHA256:crypto.createHash('sha256').update(k).digest('hex'),
      second_real_full_cubie_SHA256:crypto.createHash('sha256').update(prior.whole).digest('hex'),
      original_real_54_sticker_replay_confirmed:true});
   }
  }
 }else{cornerSeen.set(corner,{whole:k,word:code,depth});}
 if(edgeSeen.has(edge)){edgeAliasCount++;}else{edgeSeen.set(edge,{whole:k,word:code});}
 if(!atDepth[depth])atDepth[depth]={depth,whole_states:0,new_corner_states:0,new_edge_states:0};
 const row=atDepth[depth];row.whole_states++;
 if(!prior)row.new_corner_states++;
 index++;
}
assert.equal(index,G.visited.size);
assert.deepEqual(G.hist,[1,18,243,3240,43239,574908]);
assert.equal(cornerSeen.size+cornerAliasCount,index);
assert(cornerSeen.size>0);
assert(cornerSeen.size<=index);
const observed=collisions.length;
if(cornerAliasCount>0)assert(observed>0);
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P3_R0_REAL_FULL_CUBE_TO_2X2_CORNER_QUOTIENT_OBSERVATION',
 legal_moves:'All 18 outer face HTM; original real 54-sticker-derived cubie group',
 physical_full_cube_depth_at_most:5,
 exact_full_3x3_cubie_cayley_ball_hist:G.hist,
 physical_full_3x3_cubie_state_count:index,
 physically_distinct_2x2_corner_position_orientation_projections:cornerSeen.size,
 observed_corner_projection_collision_instances:cornerAliasCount,
 physically_distinct_edge_position_orientation_projections:edgeSeen.size,
 edge_projection_collision_instances:edgeAliasCount,
 actual_corners_equal_edges_different_witnesses:collisions,
 first_collision_replayed_original_stickers:cornerAliasCount>0,
 information_theoretic_limit:'A pure 2x2-corner observation of a 3x3 cannot distinguish actual full states with distinct edges; unlike real visual data, this is an ideal observation map in a fixed face frame',
 not_complete_2x2_Gods_number:true,
 no_human_perception_or_neural_recording:true,
 no_third_dimension_assumed_user_IQ_or_working_memory:true,
 physical_state_counts_by_exact_shortest_full_cube_depth:atDepth
},null,2));
