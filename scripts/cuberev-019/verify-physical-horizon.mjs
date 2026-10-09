/** CUBE-REV 0.19: physical sticker-derived finite invariants that imply the analytic L<=3 impossibility theorem.
 * Mathematically, each incremental orientation bit is a transported 4-slot cut.
 * All F/B family moves preserve F/B/N initial partition; see docs/0.19/P1.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const maps=urMoveAutomaton(); assert.equal(maps.length,18);
const F=new Set([1,5,8,9]),B=new Set([3,7,10,11]);
const N=new Set([...Array(12).keys()].filter(x=>!F.has(x)&&!B.has(x)));
const flip=new Set(['F',"F'",'B',"B'"]);
for(let a=0;a<18;a++){
 const token=ACTIONS[a],m=maps[a];
 assert.equal(m.length,24);assert.equal(new Set(m).size,24);
 const support=new Set();
 for(let p=0;p<12;p++){
  if(m[2*p]&1)support.add(p);
  assert.equal(m[2*p+1],m[2*p]^1);
 }
 const expected=token[0]==='F'&&flip.has(token)?F:token[0]==='B'&&flip.has(token)?B:new Set();
 assert.equal(support.size,expected.size,token);
 for(const p of expected)assert(support.has(p),token);
 if(token[0]==='F'||token[0]==='B'){
  for(const group of [F,B,N]){
   const next=new Set([...group].map(p=>Math.floor(m[2*p]/2)));
   assert.equal(next.size,group.size,token);
   for(const p of group)assert(next.has(p),token);
  }
 }
}
function rank(word){
 const s=Array.from({length:12},(_,i)=>2*i),hist=Array(12).fill(0);
 for(let t=0;t<word.length;t++)for(let i=0;i<12;i++){
  s[i]=maps[word[t]][s[i]]; hist[i]|=(s[i]&1)<<t;
 }
 return new Set(hist).size;
}
const actual=[];
for(let length=0;length<=3;length++){
 let mx=0;
 for(let n=0;n<18**length;n++){
  const word=[];let k=n;
  for(let t=0;t<length;t++){word.push(k%18);k=Math.floor(k/18);}
  const q=word.filter(i=>flip.has(ACTIONS[i])).length;
  const z=rank(word);
  assert(z<=2**q);
  if(word.every(i=>'FB'.includes(ACTIONS[i][0])))assert(z<=3);
  mx=Math.max(mx,z);
 }
 actual.push(mx);
}
assert.deepEqual(actual,[1,2,3,4]);
console.log('CUBE_REV_019_EARLIEST_PHYSICAL_FIVE_STATE_OBSERVABILITY_HORIZON_4_PASS',JSON.stringify({maxRankForHorizon0to3:actual,F:[...F],B:[...B],N:[...N]}));
