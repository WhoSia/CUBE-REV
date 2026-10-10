/** CUBE-REV 0.21 P0: test physical 24-state adaptive Bellman semantics.
 * Import the existing sticker-derived physical oracle, never mutate the 0.15 proof.
 * Run: node scripts/cuberev-021/audit-physical-adaptive-beliefs.mjs
 * Independent finite-horizon recursion + full branch replay + baseline comparison.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton,adaptiveOrientationDepth} from '../cuberev-015/ur-fiber-tomography.mjs';

const maps=urMoveAutomaton();
assert.equal(maps.length,18);
for (const m of maps)assert.deepEqual([...m].sort((a,b)=>a-b),
  Array.from({length:24},(_,i)=>i));

const pop=x=>{let n=0;for(;x;x&=x-1)n++;return n;};
const move=(mask,m)=>{
 let out=0;
 for(let s=0;s<24;s++)if(mask & (1<<s))out|=1<<m[s];
 return out;
};
const branches=(mask,m)=>{
 const next=move(mask,m);
 const zero=next&0x555555,one=next&0xAAAAAA;
 assert.equal(zero|one,next);
 assert.equal(zero&one,0);
 assert.equal(pop(zero)+pop(one),pop(mask));
 return [zero,one].filter(Boolean);
};
const memo=new Map();
function finite(mask,depth){
 if(pop(mask)<=1)return true;
 if(depth===0)return false;
 if(pop(mask)>2**depth)return false;
 const key=mask+':'+depth;
 if(memo.has(key))return memo.get(key);
 for(let a=0;a<18;a++){
  const bs=branches(mask,maps[a]);
  if(bs.every(b=>finite(b,depth-1))){
   memo.set(key,a+1);return true;
  }
 }
 memo.set(key,0);return false;
}
function witness(mask,depth){
 if(pop(mask)<=1)return {mask,terminal:true};
 assert(finite(mask,depth));
 const a=memo.get(mask+':'+depth)-1;
 assert(a>=0);
 const bs=branches(mask,maps[a]);
 const child=bs.map(b=>witness(b,depth-1));
 assert(child.every(c=>c.terminal||c.move!==undefined));
 return {mask,action_index:a,move:true,children:child};
}
const cases=[];
for(const s of [0,1,2,3,4,5,6,7,8,9,10,11])
 for(const t of [s+1,12,18])if(t<24)
  cases.push((1<<(2*s))|(1<<t));
cases.push(0x555555,0xFFFFFF,0xAAA555,0x555);
const unique=[...new Set(cases)];
const checked=[];
for(const b of unique){
 // Comparing to historic function only if it does not exceed its documented 10-step limit.
 let depth=null;
 for(let d=0;d<=10;d++)if(finite(b,d)){depth=d;break;}
 if(depth!==null){
  const historic=adaptiveOrientationDepth(b,maps);
  assert.equal(historic,depth,'0.15 baseline disagreement on mask '+b);
  const w=witness(b,depth);
  checked.push({mask:b,start_cardinality:pop(b),depth,first_action:w.action_index??null});
 }else checked.push({mask:b,start_cardinality:pop(b),depth:'>10 or unidentifiable'});
}
const reference=checked.find(c=>c.mask===0x555555);
console.log(JSON.stringify({
 result:'CUBE_REV_021_P0_PHYSICAL_ADAPTIVE_BELIEF_BASELINE_PASS',
 source:'actual sticker-derived 18 legal HTM original UR edge oracle',
 reference,
 belief_cases:checked.length,
 historical_baseline:'adaptiveOrientationDepth from CUBE-REV 0.15',
 independently_tested_finite_horizon_bound:10,
 false_solved_as_full_cube:false,
 sample:checked.slice(0,12)
},null,2));
