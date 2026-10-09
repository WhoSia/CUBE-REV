/** 0.18 evidence court: compare the historical hand-coded P6 ring oracle
 * against the current real sticker-derived UR-edge physical automaton.
 * This is intentionally a failed transport witness + repaired physical PASS.
 * No historical human data or solver trust required.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const old=JSON.parse(fs.readFileSync(new URL('../../docs/0.18/P0_34_WORD_PHYSICAL_UPPER_WITNESS.json',import.meta.url),'utf8'));
const fixed=JSON.parse(fs.readFileSync(new URL('../../docs/0.18/P0_REPAIRED_37_WORD_PHYSICAL_WITNESS.json',import.meta.url),'utf8'));
assert.equal(old.status,'REJECTED_PHYSICAL_UPPER_WITNESS');
assert.equal(old.words.length,34);assert.equal(fixed.words.length,37);
const real=urMoveAutomaton();assert.equal(real.length,18);
const oldAlpha=[...('URFDLB')].flatMap(f=>[f,f+"'",f+'2']);
const ring=[[0,1,2,3],[0,8,4,11],[1,8,5,9],
 [4,5,6,7],[2,9,6,10],[3,10,7,11]];
const prior=oldAlpha.map((_,a)=>{
 const face=Math.floor(a/3);
 let k=[1,-1,2][a%3];if(face===1)k=-k;
 const map=[];
 for(let state=0;state<24;state++){
  let p=state>>1,fl=state&1;
  let at=ring[face].indexOf(p);
  if(at>=0){p=ring[face][(at+k+4)%4];
   if((face===2||face===5)&&a%3!==2)fl^=1}
  map.push(2*p+fl);
 }
 return map;
});
const distance=oldAlpha.map((word,i)=>{
 const realMap=real[ACTIONS.indexOf(word)],oldMap=prior[i];
 assert(realMap && oldMap);
 return {word,disagreements:oldMap.filter((x,j)=>x!==realMap[j]).length};
});
const different=distance.filter(x=>x.disagreements);
const phys=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const bases=phys.bases;assert.equal(bases.length,1192);
function coverage(words,model,alpha){
 let all=new Array(1192).fill(false);
 for(const word of words){
  const idx=word.map(tok=>alpha.indexOf(tok));
  assert.equal(idx.length,4);assert(idx.every(i=>i>=0));
  let st=Array.from({length:12},(_,i)=>2*i),hist=Array(12).fill(0);
  for(let t=0;t<4;t++){
   st=st.map(x=>model[idx[t]][x]);
   for(let p=0;p<12;p++)hist[p]|=(st[p]&1)<<t;
  }
  for(let i=0;i<1192;i++){
   let mask=bases[i],bits=0,ok=true;
   for(let p=0;p<12;p++)if(mask&(1<<p)){
    const v=1<<hist[p];
    if(bits&v){ok=false;break}
    bits|=v;
   }
   if(ok)all[i]=true;
  }
 }
 return bases.filter((_,i)=>!all[i]).sort((a,b)=>a-b);
}
const dIndex=ACTIONS.indexOf('D'),dpIndex=ACTIONS.indexOf("D'");
assert(dIndex>=0&&dpIndex>=0);
assert.deepEqual(prior[oldAlpha.indexOf('D')],real[dpIndex],
 'Old D must equal true sticker-derived D-prime as a 24-state map');
assert.deepEqual(prior[oldAlpha.indexOf("D'")],real[dIndex],
 'Old D-prime must equal true sticker-derived D');
for(const word of oldAlpha){
 if(word==='D'||word==="D'")continue;
 assert.deepEqual(prior[oldAlpha.indexOf(word)],real[ACTIONS.indexOf(word)]);
}
const correctedWords=old.words.map(word=>word.map(tok=>
 tok==='D'?"D'":tok==="D'"?'D':tok));
const convertedMissing=coverage(correctedWords,real,ACTIONS);
assert.deepEqual(convertedMissing,[],
 'Alphabet D/D-prime translation must preserve all 1192 P6 source-cover witnesses');
console.log('CUBE_REV_018_P6_D_DIRECTION_RELABEL_EQUIVALENCE_PASS',
 JSON.stringify({changedActionSymbols:['D',"D'"],stateMismatchesPerSymbol:8,
 correctedWordCount:correctedWords.length,coveredSourceBases:1192}));
const oldLegacyMissing=coverage(old.words,prior,oldAlpha);
const oldPhysicalMissing=coverage(old.words,real,ACTIONS);
const repairedPhysicalMissing=coverage(fixed.words,real,ACTIONS);
assert.deepEqual(oldLegacyMissing,[]);
assert.deepEqual(oldPhysicalMissing,[740,1082,2105,2154]);
assert.deepEqual(repairedPhysicalMissing,[]);
assert(different.length>0);
console.log('CUBE_REV_018_P6_LEGACY_ORACLE_EQUIVALENCE_FAILURE_CERT_PASS',
 JSON.stringify({differentMoves:different.length,mismatches:distance,
  oldLegacyCovered:1192,oldPhysicalCovered:1188,
  missedOriginalBases:oldPhysicalMissing}));
console.log('CUBE_REV_018_REPAIRED_37_PHYSICAL_1192_COVER_PASS');
