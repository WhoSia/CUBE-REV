/** Reconstruct independent 34-word P6 cube witness and map each
 * word's actual physical coverage to an inclusion-maximal M-star column.
 * The 34 seed is a genuine cube upper bound, NOT an assumed solver result.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const physical=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const source=JSON.parse(fs.readFileSync(new URL(
 '../../docs/0.18/P0_34_WORD_PHYSICAL_UPPER_WITNESS.json',import.meta.url),'utf8'));
assert.equal(physical.counts.maximal,1323);
assert.equal(source.words.length,34);
const moves=urMoveAutomaton(),bases=physical.bases;
const columns=physical.candidates.map(x=>BigInt('0x'+x.mask));
const chosen=[];
for(const word of source.words){
 const indices=word.map(w=>ACTIONS.indexOf(w));
 assert(indices.length===4&&indices.every(i=>i>=0));
 const states=Array.from({length:12},(_,i)=>2*i),codes=new Array(12).fill(0);
 for(let t=0;t<4;t++)for(let i=0;i<12;i++){
  states[i]=moves[indices[t]][states[i]];
  codes[i]|=(states[i]&1)<<t;
 }
 let bitset=0n;
 for(const [i,mask] of bases.entries()){
  let seen=0,ok=true;
  for(let p=0;p<12;p++)if(mask&(1<<p)){
   const bit=1<<codes[p];
   if(seen&bit){ok=false;break}
   seen|=bit;
  }
  if(ok)bitset|=1n<<BigInt(i);
 }
 const options=columns.map((m,i)=>({m,i})).filter(z=>(bitset&~z.m)===0n);
 assert(options.length>0);
 const best=options.sort((a,b)=>Number((b.m&~bitset).toString(2).replaceAll('0','').length-(a.m&~bitset).toString(2).replaceAll('0','').length))[0];
 chosen.push(best.i);
}
const unique=[...new Set(chosen)];
let union=0n;for(let i of unique)union|=columns[i];
assert.equal(union.toString(2).replaceAll('0','').length,1192);
const out={schema:'cube-rev.018.physical-34-hint-v1',
 candidates:unique,originalCount:34,newCount:unique.length,
 physicalAll1192Verified:true,
 initialHTMWords:source.words};
if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(out)+'\n');
console.log('MSTAR34_SEEDED_REAL_CUBE_PHYSICAL_COVER_PASS',
 JSON.stringify({original34:source.words.length,maximalRepresentativeCount:unique.length,
 allCovered:true}));
