/**
 * CUBE-REV 0.21 P2 — genuine shared Rubik edge transport and front-sticker visual access.
 * Both edge identities move on ONE legal cube, with occupied-slot exclusion.
 * The tag-window pilot and the ordinary-colour front-camera pilot are different experiments.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS, FACE_EDGE_IDS} from '../cuberev-013/cross4-pdb.mjs';
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';

const maps=urMoveAutomaton();
const all=Array.from({length:12},(_,i)=>i);
const F=new Set(FACE_EDGE_IDS.F);
const act=(token)=>{const i=ACTIONS.indexOf(token);assert(i>=0);return i;};
const key=(p,q)=>p+','+q;
const sourceStates=[];
for(let p=0;p<12;p++)for(let q=0;q<12;q++)if(p!==q)sourceStates.push([2*p,2*q]);
assert.equal(sourceStates.length,132);

// Independent full-sticker and reduced two-edge transport checks.
for(const a of ACTIONS){
 const cube=solvedStickerCube();applyMoveToken(cube,a);
 const {ep,eo}=toCubieState(cube);
 for(const target of [0,1]){
  const p=ep.indexOf(target);
  assert.equal(maps[act(a)][2*target],2*p+eo[p]);
 }
}
const seen=new Map([[key(0,2),{distance:0,word:[]}]]);
const queue=[[0,2]];let qi=0;
while(qi<queue.length){
 const [p,q]=queue[qi++],here=seen.get(key(p,q));
 for(let a=0;a<18;a++){
  const pn=maps[a][p],qn=maps[a][q];
  assert.notEqual(pn>>1,qn>>1);
  const k=key(pn,qn);
  if(!seen.has(k)){
   const w=[...here.word,ACTIONS[a]];
   seen.set(k,{distance:here.distance+1,word:w});
   queue.push([pn,qn]);
  }
 }
}
assert.equal(seen.size,12*11*4,'all 528 physically attainable oriented distinct placements');
const depths=[...seen.values()].map(x=>x.distance);
for(const [p,q] of sourceStates){
 const path=seen.get(key(p,q))?.word;
 assert(path!==undefined,'orientation-zero pair has legal real-cube witness');
 const cube=solvedStickerCube();
 for(const token of path)applyMoveToken(cube,token);
 const s=toCubieState(cube);
 for(const [target,expected] of [[0,p],[1,q]]){
  const i=s.ep.indexOf(target);
  assert.equal(2*i+s.eo[i],expected,'real sticker-generated legal witness');
 }
}
// Joint observations are the labelled visibility of EACH tracked edge at the front window.
// This sensor requires visibly labelled target pieces and is not the natural untagged F image.
const tagObs=([s,t])=>Number(F.has(s>>1))*2+Number(F.has(t>>1));
function transport(st,a){return [maps[a][st[0]],maps[a][st[1]]];}
const count=(states)=>states.reduce((acc,s)=>(acc[tagObs(s)]++,acc),[0,0,0,0]);
const before=count(sourceStates);
const afterF=count(sourceStates.map(s=>transport(s,act('F'))));
assert.deepEqual(before,[56,32,32,12]);
assert.deepEqual(afterF,[56,32,32,12]);
const naiveIndependentCounts=[64,32,32,16];
assert.equal(before.reduce((x,y)=>x+y),132);

// Physical eight-HTM positive preset witness for BOTH labelled edge starting locations.
const witness=["L'",'U2','R2','D2',"L'",'R','D','L2'];
let each=Array.from({length:12},(_,i)=>2*i);
const oneHist=Array(12).fill(''),oneRanks=[];
for(const move of witness){
 const a=act(move);
 each=each.map(p=>maps[a][p]);
 for(let i=0;i<12;i++)oneHist[i]+=Number(F.has(each[i]>>1));
 oneRanks.push(new Set(oneHist).size);
}
assert.equal(new Set(oneHist).size,12);
assert.deepEqual(oneRanks,[2,4,6,7,9,10,11,12]);
let pairs=sourceStates.map(s=>[...s]);
const pairHist=sourceStates.map(()=>''),pairRanks=[];
for(const move of witness){
 const a=act(move);
 pairs=pairs.map(p=>transport(p,a));
 for(let i=0;i<132;i++)pairHist[i]+=String(tagObs(pairs[i]));
 pairRanks.push(new Set(pairHist).size);
}
assert.equal(new Set(pairHist).size,132);

// Observed labelwise source sets obey exact exclusion, not independent 12 x 12 product.
let intersectionAudits=0;
for(let n=0;n<=witness.length;n++){
 const candidates=new Map();
 for(let i=0;i<132;i++){
  const joint=pairHist[i].slice(0,n);
  if(!candidates.has(joint))candidates.set(joint,[]);
  candidates.get(joint).push(i);
 }
 for(const [joint,ixs] of candidates){
  const A=new Set(ixs.map(i=>sourceStates[i][0]>>1));
  const B=new Set(ixs.map(i=>sourceStates[i][1]>>1));
  const overlap=[...A].filter(x=>B.has(x)).length;
  const admissible=A.size*B.size-overlap;
  assert.equal(ixs.length,admissible,'same-action independent tag histories + diagonal exclusion');
  intersectionAudits++;
 }
}

// Ordinary untagged sticker camera: no privileged piece ID, just nine visible facelet colours.
const photo=cube=>cube.filter(s=>s.n[0]===0&&s.n[1]===0&&s.n[2]===1)
 .sort((x,y)=>x.p[0]-y.p[0]||x.p[1]-y.p[1]||x.p[2]-y.p[2])
 .map(s=>s.c).join('');
function prepared(scramble){
 const cube=solvedStickerCube();
 if(scramble)applyMoveToken(cube,scramble);
 return cube;
}
const four=[prepared(null),prepared('B'),prepared("B'"),prepared('B2')];
const initialPhotos=four.map(photo);assert.equal(new Set(initialPhotos).size,1);
const actionDisclosure={};
for(const token of ACTIONS){
 const newPhotos=four.map(c=>{
  const next=c.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));
  applyMoveToken(next,token);return photo(next);
 });
 actionDisclosure[token]=new Set(newPhotos).size;
}
assert.equal(actionDisclosure.U,4);
assert.equal(actionDisclosure["U'"],4);
assert.equal(actionDisclosure.B,1);
assert.equal(actionDisclosure.F,1);
const nearInvisibleOneTurn=ACTIONS.filter(a=>actionDisclosure[a]===1);
const fullRevealOneTurn=ACTIONS.filter(a=>actionDisclosure[a]===4);

console.log(JSON.stringify({
 result:'CUBE_REV_021_P2_SHARED_EDGE_AND_NATIVE_STICKER_FRONT_CAMERA_PASS',
 exact_scope:'actual 18 sticker-derived 3x3 face moves; original two labelled UR/UF cubies with zero initial intrinsic flips; 132 ordered distinct source slots',
 physically_reachable_two_edge_oriented_states:seen.size,
 max_shortest_face_turn_witness_depth_for_oriented_pair_states:Math.max(...depths),
 zero_initial_orientation_distinct_pair_sources:sourceStates.length,
 physical_full_sticker_replay_of_all_132_start_states:true,
 marked_F_window_experiment:{
  sensor:'two removable marker IDs visible on front-face edge stickers; DIFFERENT FROM normal colours',
  one_view_joint_counts_00_01_10_11:before,
  impossible_independent_product_counts_00_01_10_11:naiveIndependentCounts,
  explanation:'same cube has no two labelled edges in the same slot',
  eight_turn_positive_witness:witness,
  one_edge_rank_prefix:oneRanks,
  joint_132_source_rank_prefix:pairRanks,
  one_edge_final_histories:oneHist,
  source_support_product_exclusion_checks:intersectionAudits
 },
 untagged_real_sticker_F_front_view:{
  hidden_scramble_options:['solved','B',"B'",'B2'],
  all_four_initial_nine_colour_F_photos_identical:true,
  one_turn_F_camera_rank_by_HTM:actionDisclosure,
  one_turn_actions_revealing_all_four:fullRevealOneTurn,
  one_turn_actions_leaving_all_four_indistinguishable:nearInvisibleOneTurn
 },
 claim_limits:'No human decisions measured. 8-turn two-marker witness is an upper bound, not proven optimum. Sticker-only face camera is a different observation ontology. Two edge labels are not the full cube state.'
},null,2));
