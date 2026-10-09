/** CUBE-REV 0.19 P5 — fixed-word nine-turn witness and exact adaptive horizon.
 * Independently replay with the sticker-derived physical 18-action UR-edge oracle.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
import fs from 'node:fs';
import crypto from 'node:crypto';
const maps=urMoveAutomaton();
const raw=fs.readFileSync(new URL('../../docs/0.18/P0_60_POSITIVE_DUAL_WEIGHTS.json',import.meta.url));
// The original requirement list is reconstructed by the frozen physical source exporter.
// For one-word coverage, full 12-state injectivity implies every subset is identified.
assert.equal(maps.length,18);
assert(maps.every(m=>m.length===24&&new Set(m).size===24));
const F=new Set([1,5,8,9]), B=new Set([3,7,10,11]);
const N=new Set([...Array(12).keys()].filter(p=>!F.has(p)&&!B.has(p)));
for(let a=0;a<18;a++){
 const tok=ACTIONS[a],groups=[F,B,N], support=new Set();
 for(let p=0;p<12;p++){
  assert.equal(maps[a][2*p+1],maps[a][2*p]^1);
  if(maps[a][2*p]&1)support.add(p);
 }
 const expected=(tok==='F'||tok==="F'")?F:(tok==='B'||tok==="B'")?B:new Set();
 assert.equal(support.size,expected.size);
 for(const p of expected)assert(support.has(p));
 if('FB'.includes(tok[0])){
  for(const group of groups){
   const moved=new Set([...group].map(p=>Math.floor(maps[a][2*p]/2)));
   assert.equal(moved.size,group.size);
   for(const p of group)assert(moved.has(p));
  }
 }
}
// Each flip-producing action tests exactly FOUR of the original 12 slots.
// Twelve distinct binary codes of length 4 require at least 19 total ones;
// any four transported flip cuts provide exactly 16 ones.
const popBits=v=>{let z=0;while(v){v&=v-1;z++;}return z};
assert.equal([...Array(16).keys()].map(popBits).sort((x,y)=>x-y).slice(0,12).reduce((x,y)=>x+y,0),19);
console.log('CUBE_REV_019_Q_AT_MOST4_WEIGHT_BARRIER_AND_FB_CONFINEMENT_PASS');
const W=['F','B','U','R2','F',"B'",'U','F','B'];
let states=Array.from({length:12},(_,i)=>2*i),history=Array(12).fill(0);
const prefixes=[];
for(let t=0;t<W.length;t++){
  const ix=ACTIONS.indexOf(W[t]);assert(ix>=0);
  states=states.map(s=>maps[ix][s]);
  history=history.map((h,i)=>h|((states[i]&1)<<t));
  prefixes.push(new Set(history).size);
}
assert.deepEqual(prefixes,[2,3,3,3,6,9,9,11,12]);
assert.equal(new Set(history).size,12);
console.log('CUBE_REV_019_FIXED_NINE_TURN_12_STATE_INJECTIVE_PASS',JSON.stringify({words:W,codes:history,prefixRanks:prefixes}));
const even=0x555555,full=(1<<24)-1;
const initial=even;
function popcount(v){let z=0;while(v){v&=v-1;z++;}return z}
const successor=new Map();
function moveBelief(mask,a){
 const key=mask*18+a;
 if(successor.has(key))return successor.get(key);
 let nxt=0;
 while(mask){const low=mask&-mask;const idx=31-Math.clz32(low);nxt|=1<<maps[a][idx];mask&=mask-1}
 successor.set(key,nxt);return nxt;
}
const memo=new Map();
function solve(mask,horizon){
 if(popcount(mask)<=1)return [];
 if(horizon<=0||popcount(mask)>2**horizon)return null;
 const key=mask+':'+horizon;
 if(memo.has(key))return memo.get(key);
 const choices=[];
 for(let a=0;a<18;a++){
  const s=moveBelief(mask,a),zero=s&even,one=s&(full^even);
  if(Math.max(popcount(zero),popcount(one))>2**(horizon-1))continue;
  choices.push([Math.abs(popcount(zero)-popcount(one)),a,zero,one]);
 }
 choices.sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
 for(const [,a,z,o] of choices){
  const left=z?solve(z,horizon-1):[];
  if(left===null)continue;
  const right=o?solve(o,horizon-1):[];
  if(right!==null){
   const ans=[a,left,right];memo.set(key,ans);return ans;
  }
 }
 memo.set(key,null);return null;
}
assert.equal(solve(initial,6),null,'An adaptive six-step strategy unexpectedly exists');
const losingMemo=memo.size;
const policy=solve(initial,7);
assert(policy!==null,'Seven-step adaptive policy lost');
const depths=[];
function audit(node,originals,physical,depth){
 if(node.length===0){
  assert.equal(originals.length,1,'Non-singleton terminal belief');
  depths.push(depth);return;
 }
 assert(depth<7);
 const [a,left,right]=node;
 const ch=[[],[]], st=[[],[]];
 for(let k=0;k<originals.length;k++){
  const next=maps[a][physical[k]],label=next&1;
  ch[label].push(originals[k]);st[label].push(next);
 }
 if(ch[0].length)audit(left,ch[0],st[0],depth+1);
 if(ch[1].length)audit(right,ch[1],st[1],depth+1);
}
audit(policy,Array.from({length:12},(_,i)=>i),Array.from({length:12},(_,i)=>2*i),0);
assert.equal(depths.length,12);
assert.equal(Math.max(...depths),7);
assert.equal(depths.reduce((a,b)=>a+b,0),71);
console.log('CUBE_REV_019_EXACT_ADAPTIVE_MINIMAX_DEPTH7_PASS',
 JSON.stringify({horizon6Unwinnable:true,memoStatesForHorizon6:losingMemo,
  totalMemoStates:memo.size,horizon7Worst:7,policyLeafDepths:depths,
  uniformPolicyMeanActions:'71/12',policy}));
