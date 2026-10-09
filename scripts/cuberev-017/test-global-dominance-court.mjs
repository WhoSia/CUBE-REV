/** CUBE-REV 0.17: derive an M*-sound ALL-k coverage-dominance quotient.
 * Unlike the P7 168-word near-tight cut, THIS replacement is valid for
 * arbitrary k, including k=25: if C(u) subset C(v), replace u by v.
 * Full action grammar: 18 literal HTM words of exactly four turns,
 * source: frozen physical 0.15 known-flip-zero edge automaton.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
const maps=urMoveAutomaton();
assert.equal(maps.length,18);
const allGroups=[
 new Set([1,5,8,9]),new Set([3,7,10,11]),new Set([0,2,4,6])
];
const five=[[0,2,3],[2,0,3],[1,2,2],[2,1,2],[2,2,1]];
const masks=[],sizes=[];
function subsets(k,start=0,s=0){
 if(k===0){
  const c=allGroups.map(g=>[...g].filter(v=>s&(1<<v)).length);
  const n=c.reduce((a,b)=>a+b,0);
  const ok=n===3||(n===4&&c.filter(x=>x>0).length>=2)
   ||(n===5&&five.some(t=>t.every((v,i)=>c[i]>=v)));
  if(ok){masks.push(s);sizes.push(n);}
  return;
 }
 for(let i=start;i<=12-k;i++)subsets(k-1,i+1,s|(1<<i));
}
for(let k=3;k<=5;k++)subsets(k);
assert.deepEqual([3,4,5].map(k=>sizes.filter(n=>n===k).length),
 [220,492,480]);
const partitionMap=new Map(),S=Array.from({length:12},(_,i)=>2*i);
for(let a=0;a<18;a++)for(let b=0;b<18;b++)
for(let c=0;c<18;c++)for(let d=0;d<18;d++){
 const signature=new Array(12).fill(0);
 let states=S.slice();
 for(const [i,move] of [a,b,c,d].entries()){
  states=states.map(x=>maps[move][x]);
  for(let p=0;p<12;p++)signature[p]|=(states[p]&1)<<i;
 }
 const groups=new Map();
 for(let p=0;p<12;p++)groups.set(signature[p],
    (groups.get(signature[p])||0)|(1<<p));
 const blocks=[...groups.values()].sort((x,y)=>x-y);
 const key=blocks.join(',');
 if(!partitionMap.has(key))partitionMap.set(key,{blocks,word:[a,b,c,d]});
}
assert.equal(partitionMap.size,1913);
const ptypes=[...partitionMap.values()];
const coverage=ptypes.map(({blocks})=>{
 let value=0n;
 for(let i=0;i<masks.length;i++){
  if(blocks.every(g=>((g&masks[i]).toString(2).replaceAll('0','').length)<=1))
   value|=1n<<BigInt(i);
 }
 return value;
});
const uniq=[...new Set(coverage.map(v=>v.toString(16)))].map(h=>BigInt('0x'+h));
assert.equal(uniq.length,1477);
const pop=x=>x.toString(2).replaceAll('0','').length;
uniq.sort((a,b)=>pop(b)-pop(a));
const max=[];
for(const mask of uniq){
 if(!max.some(other=>(mask&~other)===0n))max.push(mask);
}
assert.equal(max.length,1323);
const union=max.reduce((a,b)=>a|b,0n);
assert.equal(pop(union),1192);
console.log('CUBE_REV_017_GLOBAL_MSTAR_ALL_K_DOMINANCE_PASS');
console.log(JSON.stringify({originalWords:18**4,partitionTypes:partitionMap.size,
 admissibleBases:masks.length,coverageTypes:uniq.length,
 inclusionMaximal: max.length,validForK25:true}));
