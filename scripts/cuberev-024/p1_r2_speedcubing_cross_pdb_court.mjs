// CUBE-REV 0.24 P1-R2: REAL official WCA 3x3 scramble -> exact CFOP-cross
// four-edge HTM optimal planning, all 6 possible reference colors.
// This measures machine-computed physical possibilities, NOT a human's
// inspection, choices, TPS, regrips, or observed solve stage.
import assert from 'node:assert/strict';
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';
import {buildCrossPDB,indexOfFourEdges,FACE_EDGE_IDS,ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const casebook=[
  {id:'WCA_SeoulSummer2026_333_Final_A_1',
    source:'https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles',
    scramble:"R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2"},
  {id:'WCA_SeoulSummer2026_333_First_A_1',
    source:'https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles',
    scramble:"L2 F2 U F2 R2 U B2 R2 D U F L U F' R2 B R' D B'"},
  {id:'WCA_SeoulWinter2026_333_Final_A_1',
    source:'https://www.worldcubeassociation.org/competitions/SeoulWinter2026/scrambles',
    scramble:"F2 D' F2 U' R2 B2 R2 D' B2 R' D' F' D R' U' F2 U L' D2 U"}
];
function originalState(tokens){
  const cube=solvedStickerCube();
  for(const t of tokens){
    assert(ACTIONS.includes(t),'Only official exact original outer-face HTM tokens');
    applyMoveToken(cube,t);
  }
  return cube;
}
const moves=ACTIONS.map(token=>{
  const c=solvedStickerCube();applyMoveToken(c,token);
  return toCubieState(c);
});
function compose(s,m){
  const x=moves[ACTIONS.indexOf(m)];assert(x,'legal HTM token required');return {cp:x.cp.map(i=>s.cp[i]),
    co:x.co.map((v,i)=>(s.co[x.cp[i]]+v)%3),
    ep:x.ep.map(i=>s.ep[i]),eo:x.eo.map((v,i)=>s.eo[x.ep[i]]^v)};
}
const pdb=Object.fromEntries('URFDLB'.split('').map(face=>[face,buildCrossPDB(face)]));
for(const face of 'URFDLB')assert.equal(pdb[face].reachable,190080);
function d(s,face){return pdb[face].distances[indexOfFourEdges(s.ep,s.eo,FACE_EDGE_IDS[face])]}
function crossPlan(state,face){
  const input=d(state,face);
  let cur=state;const path=[],shortestFirst=[],progress=[];
  for(const token of ACTIONS){
    const next=compose(state,token),v=d(next,face);
    if(v===input-1)shortestFirst.push(token);
  }
  while(d(cur,face)>0){
    const now=d(cur,face);
    const chosen=ACTIONS.find(t=>d(compose(cur,t),face)===now-1);
    assert(chosen,'exact cross PDB must have every predecessor');
    path.push(chosen);cur=compose(cur,chosen);
    progress.push(d(cur,face));
  }
  assert.equal(path.length,input);
  assert.equal(d(cur,face),0);
  return {optimalCrossHTM:input,crossWord:path.join(' '),shortestFirstMoves:shortestFirst,
    afterMoveCrossRemaining:progress,
    fullCubeSolvedByCrossOnly:cur.cp.every((v,i)=>v===i)&&cur.ep.every((v,i)=>v===i)&&cur.co.every(x=>x===0)&&cur.eo.every(x=>x===0)};
}
const results=[];
for(const {id,source,scramble} of casebook){
  const tokens=scramble.split(/\s+/);
  const c=originalState(tokens),state=toCubieState(c),rows={};
  for(const face of 'URFDLB'){
    const output=crossPlan(state,face);
    const replay=originalState([...tokens,...output.crossWord.split(/\s+/).filter(Boolean)]);
    assert.equal(d(toCubieState(replay),face),0,'physically replayed original cross must be solved');
    rows[face]=output;
  }
  const minimum=Math.min(...Object.values(rows).map(x=>x.optimalCrossHTM));
  results.push({id,source,official_333_scramble:scramble,
    crossFaceResults:rows,
    minCrossFaceHTM:minimum,
    allOptimalCrossReferenceFaces:Object.keys(rows).filter(face=>rows[face].optimalCrossHTM===minimum),
    officialHumanSolutionObserved:false,
    speedcubing_stage_evidence:'ACTUAL_COMPETITION_SCRAMBLE_ONLY, MACHINE_SYNTHETIC_CROSS_PLANS'});
}
console.log(JSON.stringify({
  marker:'CUBE_REV_024_P1_R2_ACTUAL_SPEEDCUBING_CROSS_PDB_STAGE_COURT',
  official_wca_scramble_examples:results.length,
  CFOP_cross_four_edge_exact_PDB_states_per_reference_face:190080,
  all_six_face_reference_targets:'URFDLB',
  sourceRights:'Official publicly listed competition scramble text only; no new video or solver identity/trajectory acquisition',
  result:results,
  no_human_behavior_claim:true,
  no_unrestricted_full_cube_speed_optimization_claim:true
},null,2));
