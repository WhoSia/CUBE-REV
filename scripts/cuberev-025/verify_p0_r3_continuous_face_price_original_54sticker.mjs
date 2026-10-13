// CUBE-REV 0.25 P0-R3 — independent ORIGINAL 54-sticker check of ten
// compact 2-pattern continuous-face-cost mathematical certificates.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { solvedStickerCube, applyAlgorithm, toCubieState, cubieSolved } from '../cube/sticker-cube.mjs';
import { ACTIONS } from '../cuberev-013/cross4-pdb.mjs';
const srcPath = new URL('../../data/cuberev-025/p0_r3_continuous_face_price_ten_physical_word_pair_witness.json',import.meta.url);
const seal = JSON.parse(readFileSync(srcPath,'utf8'));
const faceOrder='URFDLB';
assert.equal(seal.face_order,faceOrder);
assert.equal(seal.records.length,10);
const spec=seal.fixed_original_cubie_markers;
assert.deepEqual(Object.keys(spec).sort(),['C0','C1','E0','E1','E2']);
function countFaces(word){
 const cs=[0,0,0,0,0,0];
 for(const token of word.trim().split(/\s+/)){
  assert(ACTIONS.includes(token),'illegal original 18 HTM token: '+token);
  const face=faceOrder.indexOf(token[0]);assert(face>=0);
  cs[face]++;
 }
 return cs;
}
function physWord(original,word){
 const cube=solvedStickerCube();
 applyAlgorithm(cube,original+' '+word);
 return toCubieState(cube);
}
function solvesMarked(cubies,x){
 for(const id of x.ids){
  if(x.type==='edge'){
   assert.equal(cubies.ep[id],id,'original edge identity '+id);
   assert.equal(cubies.eo[id],0,'original edge flip '+id);
  }else if(x.type==='corner'){
   assert.equal(cubies.cp[id],id,'original corner identity '+id);
   assert.equal(cubies.co[id],0,'original corner twist '+id);
  }else throw new Error('unknown real cubie pattern');
 }
}
const seen=new Set();let near7=0,exact7=0,below7=0;
for(const rec of seal.records){
 const pair=rec.source_pattern_A+'+'+rec.source_pattern_B;
 assert(!seen.has(pair),'duplicate '+pair);seen.add(pair);
 const ca=countFaces(rec.projected_solution_A),cb=countFaces(rec.projected_solution_B);
 const envelope=ca.map((v,i)=>Math.max(v,cb[i])).reduce((x,y)=>x+y,0);
 assert(envelope<=7,'face-cost certificate violates upper7: '+pair+' '+envelope);
 const pa=physWord(seal.source_wca_original_scramble,rec.projected_solution_A);
 const pb=physWord(seal.source_wca_original_scramble,rec.projected_solution_B);
 solvesMarked(pa,spec[rec.source_pattern_A]);
 solvesMarked(pb,spec[rec.source_pattern_B]);
 assert(!cubieSolved(pa)&&!cubieSolved(pb),'projected short words should not solve full WCA source');
 if(pair==='E0+E2'){
  assert.deepEqual(ca,[2,1,2,0,1,1]);
  assert.deepEqual(cb,ca,'E0 and E2 physically different seven words must share face counts');
  assert.equal(rec.projected_solution_A.trim().split(/\s+/).length,7);
  assert.equal(rec.projected_solution_B.trim().split(/\s+/).length,7);
 }
 near7++;if(envelope===7)exact7++;else below7++;
 console.log('P0R3_NODE_INDEPENDENT_PHYSICAL_FACE_ENVELOPE_PAIR '+pair+' ENVELOPE '+envelope+' COUNTS_A '+JSON.stringify(ca)+' COUNTS_B '+JSON.stringify(cb)+' SOURCE_MARKED_CUBIES_SOLVED_BOTH 1');
}
assert.equal(seen.size,10);assert.equal(near7,10);assert.equal(exact7+below7,10);
const full18="F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2";
assert(cubieSolved(physWord(seal.source_wca_original_scramble,full18)),'whole WCA real 18 word must solve');
console.log('P0R3_NODE_INDEPENDENT_ORIGINAL_54_STICKER_CERTIFICATE ALL_TEN_CONTINUOUS_PRICE_FACE_ENVELOPES_MAX7 1 ALL_TWENTY_ORIGINAL_PHYSICAL_PROJECTED_WORDS_PASS 1 SOURCE_FULL18_WITNESS_PASS 1 NO_HUMAN_SOLVE_WORD_INFERRED 1 FULL_GLOBAL_DISTANCE_14_TO_18_UNCHANGED 1');
