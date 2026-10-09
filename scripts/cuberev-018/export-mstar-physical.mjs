/** CUBE-REV 0.18. Build exact public-only SAT input from the physical
 * 18-HTM UR-edge oracle, never from a guessed abstract automaton table.
 * Writes only /tmp artifacts in CI, never git writeback or human data.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const maps=urMoveAutomaton(), source=JSON.parse(fs.readFileSync(
  new URL('../../docs/0.18/P0_60_POSITIVE_DUAL_WEIGHTS.json',import.meta.url),'utf8'));
assert.equal(maps.length,18);
const weights=new Map(source.pairs);
assert.equal(weights.size,60);
assert.equal([...weights.values()].reduce((a,b)=>a+b,0),476);
const groups=[new Set([1,5,8,9]),new Set([3,7,10,11]),new Set([0,2,4,6])];
const templates=[[0,2,3],[2,0,3],[1,2,2],[2,1,2],[2,2,1]];
const bases=[],sizes=[];
function visit(k,start=0,mask=0){
 if(k===0){
  const counts=groups.map(g=>[...g].filter(x=>mask&(1<<x)).length);
  const n=counts.reduce((a,b)=>a+b,0);
  const ok=n===3||(n===4&&counts.filter(x=>x).length>=2)||
   (n===5&&templates.some(t=>t.every((v,i)=>counts[i]>=v)));
  if(ok){bases.push(mask);sizes.push(n)};return;
 }
 for(let i=start;i<=12-k;i++)visit(k-1,i+1,mask|(1<<i));
}
for(let k=3;k<=5;k++)visit(k);
assert.deepEqual([3,4,5].map(k=>sizes.filter(x=>x===k).length),[220,492,480]);
assert.equal(bases.length,1192);
for(const m of weights.keys())assert(bases.includes(m));
const partitions=new Map(),S=Array.from({length:12},(_,i)=>2*i);
for(let a=0;a<18;a++)for(let b=0;b<18;b++)
for(let c=0;c<18;c++)for(let d=0;d<18;d++){
 const sign=new Array(12).fill(0);let states=S.slice();
 for(const [i,m] of [a,b,c,d].entries()){
  states=states.map(x=>maps[m][x]);
  for(let p=0;p<12;p++)sign[p]|=(states[p]&1)<<i;
 }
 const partition=new Map();
 for(let p=0;p<12;p++)partition.set(sign[p],(partition.get(sign[p])||0)|(1<<p));
 const blocks=[...partition.values()].sort((x,y)=>x-y);
 const key=blocks.join(',');
 if(!partitions.has(key))partitions.set(key,{blocks,actions:[a,b,c,d]});
}
assert.equal(partitions.size,1913);
const coverage=new Map(),dualHistogram=new Map();
for(const {blocks,actions} of partitions.values()){
 let bitset=0n,mass=0;
 for(const [i,m] of bases.entries()){
  if(blocks.every(block=>{const z=block&m;return (z&(z-1))===0})){
   bitset|=1n<<BigInt(i);mass+=weights.get(m)??0;
  }
 }
 assert(mass<=20);
 dualHistogram.set(mass,(dualHistogram.get(mass)??0)+1);
 const key=bitset.toString(16);
 if(!coverage.has(key))coverage.set(key,{mask:bitset,mass,actions});
}
assert.equal(coverage.size,1477);
const pop=x=>x.toString(2).replaceAll('0','').length;
const sorted=[...coverage.values()].sort((x,y)=>pop(y.mask)-pop(x.mask));
const maximal=[];
for(const candidate of sorted){
 if(!maximal.some(z=>(candidate.mask&~z.mask)===0n))maximal.push(candidate);
}
assert.equal(maximal.length,1323);
assert.equal(pop(maximal.reduce((x,y)=>x|y.mask,0n)),1192);
const hist=Object.fromEntries([...new Set(maximal.map(x=>x.mass))].sort((a,b)=>a-b)
 .map(m=>[m,maximal.filter(x=>x.mass===m).length]));
assert.deepEqual(hist,{'0':727,'4':340,'8':76,'12':12,'16':6,'20':162});
const heavy=source.pairs.filter(([m,w])=>w===20).map(([m])=>m);
assert.equal(heavy.length,10);
const input={
 schema:'cube-rev.018.cube-physical-mstar-maximal-v1',
 original:'3x3 Rubik edge 18 legal HTM moves; physical frozen sticker-derived oracle',
 observations:'UR edge initial flip0; four intrinsic orientation-bit outputs, one after each action',
 counts:{literal:18**4,partitions:partitions.size,coverageTypes:coverage.size,maximal:maximal.length,bases:bases.length},
 bases,dual:source.pairs,heavy,dualHistogram:Object.fromEntries(dualHistogram),
 candidates:maximal.map(z=>({
  mask:z.mask.toString(16),mass:z.mass,
  actions:z.actions,word:z.actions.map(i=>ACTIONS[i])
 }))
};
const output=process.argv[2];
if(output){fs.writeFileSync(output,JSON.stringify(input)+'\n');
 console.log('CUBE_REV_018_PHYSICAL_MSTAR_INSTANCE_EMITTED',output)}
console.log('CUBE_REV_018_PHYSICAL_1323_DUAL_AUDIT_PASS',JSON.stringify({
 ...input.counts,heavyCount:heavy.length,positiveCandidates:maximal.filter(x=>x.mass>0).length,
 maximalHistogram:hist}));
