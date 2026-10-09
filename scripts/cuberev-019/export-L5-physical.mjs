/** CUBE-REV 0.19: independent exhaustive five-HTM orientation-history court.
 * Physically sticker-derived 18×24 edge action map; 12 initially flip-zero starts.
 * 18^5 words -> deduplicated observable partitions. No guessed abstract transition table.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
const source=process.argv[2], target=process.argv[3];
assert(source&&target,'Usage: node export-L5-physical.mjs physical.json partitions.tsv');
const raw=fs.readFileSync(source); const d=JSON.parse(raw);
assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),'9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1');
assert.equal(d.bases.length,1192);
const maps=urMoveAutomaton(); assert.equal(maps.length,18);
const partitions=new Map(), H=18**5;
for(let z=0;z<H;z++){
 let x=z,word=[];
 for(let i=0;i<5;i++){word.push(x%18);x=Math.floor(x/18);}
 const state=Array.from({length:12},(_,i)=>2*i),code=new Uint8Array(12);
 for(let i=0;i<5;i++){
  const map=maps[word[i]];
  for(let p=0;p<12;p++){state[p]=map[state[p]];code[p]|=(state[p]&1)<<i;}
 }
 const groups=new Map();
 for(let p=0;p<12;p++)groups.set(code[p],(groups.get(code[p])||0)|(1<<p));
 const blocks=[...groups.values()].sort((a,b)=>a-b),key=blocks.join(',');
 if(!partitions.has(key))partitions.set(key,word.join(' ')+'|'+blocks.join(' '));
}
assert.equal(partitions.size,14938,'Changed physical partition count: STOP');
fs.writeFileSync(target,[...partitions.values()].join('\n')+'\n');
console.log('CUBE_REV_019_PHYSICAL_L5_1889568_WORDS_14938_PARTITIONS_PASS',JSON.stringify({literal:H,partitions:partitions.size,sha256:crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex')}));
