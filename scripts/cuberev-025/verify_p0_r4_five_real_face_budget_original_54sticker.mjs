// CUBE-REV 0.25 P0-R4 standalone original 54-sticker physical
// verification of five projected words for the exact continuous
// face-uniform five-PDB cost share =7; cap8 historic witness also checked.
// This independent Node implementation is NOT an unrestricted 3x3 geodesic.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {solvedStickerCube,applyAlgorithm,toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
function load(name){
 return JSON.parse(readFileSync(new URL('../../data/cuberev-025/'+name,import.meta.url),'utf8'));
}
function wordCounts(word,faceOrder){
 let c=[0,0,0,0,0,0];
 for(const x of word.trim().split(/\s+/)){
  assert(ACTIONS.includes(x),'illegal 18HTM token '+x);
  const i=faceOrder.indexOf(x[0]);assert(i>=0);c[i]++;
 }
 return c;
}
function physicallyApply(original,word){
 const c=solvedStickerCube();
 applyAlgorithm(c,original+' '+word);
 return toCubieState(c);
}
for(const budget of [7,8]){
 const cert=load('p0_r4_five_real_cubie_projected_words_cap'+budget+'.json');
 assert.equal(cert.face_order,'URFDLB');
 assert.equal(cert.patterns.map(x=>x.name).join(','),'E0,E1,E2,C0,C1');
 assert.equal(cert.patterns.length,5);
 assert.equal(cert.common_cap.reduce((a,b)=>a+b,0),budget);
 let markerIds=new Set(),actualCap=Array(6).fill(0);
 for(const p of cert.patterns){
  const cnt=wordCounts(p.word,cert.face_order);
  assert.deepEqual(cnt,p.counts,'source marker face count '+p.name);
  for(let f=0;f<6;f++){
   actualCap[f]=Math.max(actualCap[f],cnt[f]);
   assert(cnt[f]<=cert.common_cap[f],'real physical face-cap violation '+p.name);
  }
  const s=physicallyApply(cert.scramble,p.word);
  assert(!cubieSolved(s),'projected certificate word unexpectedly completely solves source');
  for(const id of p.ids){
   let label=p.type+':'+id;
   assert(!markerIds.has(label),'non-disjoint physical cubie projection '+label);markerIds.add(label);
   if(p.type==='edge'){
    assert.equal(s.ep[id],id,'real original edge position '+id);
    assert.equal(s.eo[id],0,'real original edge flip '+id);
   }else if(p.type==='corner'){
    assert.equal(s.cp[id],id,'real original corner position '+id);
    assert.equal(s.co[id],0,'real original corner twist '+id);
   }else throw Error('unknown marked physical cubie type');
  }
  console.log('P0R4_NODE_ORIGINAL_54STICKER_PROJECTED_SOLVE_CERTIFIED cap='+budget+' pattern='+p.name+' word='+p.word+' counts='+JSON.stringify(cnt)+' validHTM=1');
 }
 assert.equal(markerIds.size,20);
 assert.deepEqual(actualCap,cert.common_cap);
 assert(cubieSolved(physicallyApply(cert.scramble,cert.source_complete_18_witness)));
 console.log('P0R4_NODE_INDEPENDENT_ORIGINAL_54_FACELET_FIVE_CUBIE_CERTIFICATE cap='+budget+' complete_marked_cubies=20 true_original_sticker_physics=1 five_cost_share_continuous_upper='+budget+' original_18HTM_complete_witness=1 no_whole_cube_lower_upgrade=1');
}
console.log('P0R4_CONTINUOUS_FIVE_PDB_FACE_COST_EXACT_OPTIMUM_7_CROSSKERNEL_PASS source_WCA_original=1 physical_Go_and_independent_Node_certificates=1 invariant=d18_global_14_to_18');
