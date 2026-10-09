/** Independent physical oracle replay of any solver-found k25 word dictionary.
 * Consumes ONLY the four HTM word tokens; ignores solver coverage bitsets.
 * No model can be called a witness without passing all 1192 real cube bases.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const witness=process.argv[2];
if(!witness||!fs.existsSync(witness)){
 console.log('MSTAR25_INDEPENDENT_REPLAY_NOT_APPLICABLE_NO_SAT_WITNESS');
 process.exit(0);
}
const data=JSON.parse(fs.readFileSync(witness));
const words=data.four_turn_words ?? data.words;
assert(Array.isArray(words) && words.length>=1);
assert(words.length<=(data.k??25));
const moves=urMoveAutomaton();
assert.equal(moves.length,18);
const allGroups=[new Set([1,5,8,9]),new Set([3,7,10,11]),new Set([0,2,4,6])];
const five=[[0,2,3],[2,0,3],[1,2,2],[2,1,2],[2,2,1]];
const bases=[];
function list(k,start=0,s=0){
 if(!k){
  const c=allGroups.map(g=>[...g].filter(x=>s&(1<<x)).length);
  const n=c.reduce((a,b)=>a+b,0);
  if(n===3||(n===4&&c.filter(x=>x>0).length>=2)
      ||(n===5&&five.some(t=>t.every((v,i)=>c[i]>=v))))bases.push(s);
  return;
 }
 for(let i=start;i<=12-k;i++)list(k-1,i+1,s|(1<<i));
}
for(let k=3;k<=5;k++)list(k);
assert.equal(bases.length,1192);
const covered=new Array(1192).fill(false);
for(const word of words){
 assert.equal(word.length,4);
 const token=word.map(t=>ACTIONS.indexOf(t));
 assert(token.every(t=>t>=0&&t<18));
 const state=Array.from({length:12},(_,i)=>2*i);
 const codes=new Array(12).fill(0);
 for(let t=0;t<4;t++){
  for(let i=0;i<12;i++){
   state[i]=moves[token[t]][state[i]];
   codes[i]|=(state[i]&1)<<t;
  }
 }
 for(let i=0;i<1192;i++){
  const orig=bases[i],seen=new Set();let ok=true;
  for(let p=0;p<12;p++)if(orig&(1<<p)){
   if(seen.has(codes[p])){ok=false;break}
   seen.add(codes[p]);
  }
  if(ok)covered[i]=true;
 }
}
const missing=bases.filter((_,i)=>!covered[i]);
if(missing.length){
 console.error('MSTAR25_PHYSICAL_REPLAY_FAILED',JSON.stringify(missing));
 process.exit(1);
}
console.log('MSTAR_REAL_HTM_WORD_WITNESS_FULL_1192_PASS',words.length);
