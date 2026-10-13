// CUBE-REV 0.25 P0-R4. Independently check the five original full
// 54-sticker physical legal move witnesses for continuous 5-PDB share upper8.
// Independent of Go physical move kernel. Not a global full-cube optimum proof.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {solvedStickerCube,applyAlgorithm,toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const cert=JSON.parse(readFileSync(new URL('../../data/cuberev-025/p0_r4_five_real_cubie_projected_words_cap8.json',import.meta.url),'utf8'));
assert.equal(cert.face_order,'URFDLB');
assert.deepEqual(cert.common_cap,[0,1,1,2,2,2]);
assert.equal(cert.patterns.length,5);
const order='E0,E1,E2,C0,C1';
assert.equal(cert.patterns.map(x=>x.name).join(','),order);
const markerIds=new Set(), cap=[0,0,0,0,0,0];
function wordCounts(word){
 let c=[0,0,0,0,0,0];
 for(const x of word.trim().split(/\s+/)){
  assert(ACTIONS.includes(x),'nonlegal real original 18HTM word token '+x);
  const i=cert.face_order.indexOf(x[0]);
  assert(i>=0);c[i]++;
 }
 return c;
}
function originalCubieAfter(word){
 const c=solvedStickerCube();applyAlgorithm(c,cert.scramble+' '+word);
 return toCubieState(c);
}
for(const p of cert.patterns){
 let counts=wordCounts(p.word);
 assert.deepEqual(counts,p.counts,'face cost count of '+p.name);
 for(let face=0;face<6;face++){
   cap[face]=Math.max(cap[face],counts[face]);
   assert(counts[face]<=cert.common_cap[face],'source capped face budget exceeded: '+p.name);
 }
 const s=originalCubieAfter(p.word);
 assert(!cubieSolved(s),'projected marker word accidentally full solves original source (must reassess scope): '+p.name);
 for(const id of p.ids){
   const markerKey=p.type+id;
   assert(!markerIds.has(markerKey),'source marker repeated '+markerKey); markerIds.add(markerKey);
   if(p.type==='edge'){
     assert.equal(s.ep[id],id,'original real edge identity '+id);
     assert.equal(s.eo[id],0,'original real edge flip '+id);
   }else if(p.type==='corner'){
     assert.equal(s.cp[id],id,'original real corner identity '+id);
     assert.equal(s.co[id],0,'original real corner twist '+id);
   }else throw Error('not a genuine corner/edge marker');
 }
 console.log('P0R4_INDEPENDENT_ORIGINAL_54STICKER_REAL_PROJECTED_WORD '+p.name+' COUNTS '+JSON.stringify(counts)+' LEGAL_18HTM 1 ALL_SOURCE_MARKED_PIECES_SOLVED 1');
}
assert.equal(markerIds.size,20,'original all 20 distinct cubies partition');
assert.deepEqual(cap,cert.common_cap);
assert.equal(cap.reduce((a,b)=>a+b,0),8);
const full=originalCubieAfter(cert.source_complete_18_witness);
assert(cubieSolved(full),'inherited real WCA full 18 HTM witness must be truly solved');
console.log('P0R4_INDEPENDENT_54_STICKER_FIVE_REAL_PHYSICAL_PROJECTION_CERTIFICATE PASS WHOLE_ORIGINAL_20_CUBIES_PARTITIONED 1 CONTINUOUS_FIVE_PDB_COST_SHARE_UPPER_8 1 DOES_NOT_SHOW_WHOLE_CUBE_SHORTEST_LEQ_8 1 ORIGINAL_FULL_18HTM_STILL_SOLVES 1');
