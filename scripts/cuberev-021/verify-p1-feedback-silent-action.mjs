/**
 * CUBE-REV 0.21 P1 — physical feedback/value-of-silent-actions court.
 * Reuse the original 0.15 sticker-derived 18 x 24 oracle unmodified.
 * Scope: single tracked UR edge orientation, 12 start slots (initial flip zero).
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton,adaptiveOrientationDepth} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const moves=urMoveAutomaton(), zero=0x555555,one=0xAAAAAA;
assert.equal(moves.length,18);
const ai=name=>{const i=ACTIONS.indexOf(name); assert(i>=0); return i;};
const bitcount=x=>{let n=0;for(;x;x&=x-1)n++;return n;};
const moveMemo=new Map(), branchMemo=new Map();
function move(mask,a){
 const key=mask+':'+a;if(moveMemo.has(key))return moveMemo.get(key);
 let m=mask,res=0;while(m){const b=m&-m,i=31-Math.clz32(b);res|=1<<moves[a][i];m^=b;}
 moveMemo.set(key,res);return res;
}
function branches(mask,a){
 const key=mask+':'+a;if(branchMemo.has(key))return branchMemo.get(key);
 const next=move(mask,a),xs=[next&zero,next&one].filter(Boolean);
 assert.equal(xs.reduce((v,x)=>v|x,0),next);
 assert.equal(xs.reduce((v,x)=>v+bitcount(x),0),bitcount(mask));
 branchMemo.set(key,xs);return xs;
}
const winning=new Map(),cost=new Map();
function win(mask,d){
 if(bitcount(mask)<2)return true;
 if(d===0||bitcount(mask)>2**d)return false;
 const key=mask+':'+d;
 if(winning.has(key))return winning.get(key);
 for(let a=0;a<18;a++)if(branches(mask,a).every(b=>win(b,d-1))){
  winning.set(key,true);return true;
 }
 winning.set(key,false);return false;
}
function depth(mask){
 for(let d=0;d<=10;d++)if(win(mask,d))return d;
 throw Error('not solved within 10, unsupported claim');
}
function bestExpectedSum(mask,d){
 if(bitcount(mask)<2)return {sum:0,action:null};
 if(d===0||bitcount(mask)>2**d)return {sum:Infinity,action:null};
 const key=mask+':'+d;if(cost.has(key))return cost.get(key);
 let best={sum:Infinity,action:null};
 for(let a=0;a<18;a++){
  const sums=branches(mask,a).map(b=>bestExpectedSum(b,d-1).sum);
  const s=bitcount(mask)+sums.reduce((x,y)=>x+y,0);
  if(s<best.sum)best={sum:s,action:a};
 }
 cost.set(key,best);return best;
}
const D=depth(zero);
assert.equal(D,7);
assert.equal(adaptiveOrientationDepth(zero,moves),7);
const firstActionCosts=ACTIONS.map((name,a)=>({
 action:name,first_branch_sizes:branches(zero,a).map(bitcount),
 worst_depth:1+Math.max(...branches(zero,a).map(depth))
}));
assert.deepEqual(firstActionCosts.filter(c=>c.worst_depth===7).map(x=>x.action),['F',"F'",'B',"B'"]);
const total=bestExpectedSum(zero,7).sum;
assert.equal(total,71,'optimal uniform-prior length sum under deadline 7');
for(const d of [8,9,10])assert.equal(bestExpectedSum(zero,d).sum,71);

const policy=[];
for(let start=0;start<12;start++){
 let mask=zero,cur=2*start,d=7;
 const actions=[],observations=[];
 while(bitcount(mask)>1){
  const {action}=bestExpectedSum(mask,d);
  assert(action!==null);const child=branches(mask,action);
  cur=moves[action][cur];
  const z=cur%2;
  const next=child.find(b=>(b&(1<<cur))!==0);
  assert(next!==undefined);
  mask=next;actions.push(ACTIONS[action]);observations.push(z);d--;
 }
 assert.equal(mask,1<<cur);
 policy.push({initial_slot:start,depth:actions.length,actions,observations,terminal_coordinate:cur});
}
assert.equal(policy.reduce((sum,t)=>sum+t.depth,0),71);
assert.equal(Math.max(...policy.map(t=>t.depth)),7);

const word=['F','B','U','R2','F',"B'",'U','F','B'];
const states=Array.from({length:12},(_,i)=>2*i),codes=Array(12).fill('');
const prefix_rank=[],earliestStop=Array(12).fill(null);
for(let t=0;t<word.length;t++){
 const a=ai(word[t]);
 for(let i=0;i<12;i++){states[i]=moves[a][states[i]];codes[i]+=String(states[i]%2);}
 prefix_rank.push(new Set(codes).size);
 for(let i=0;i<12;i++)if(earliestStop[i]===null&&codes.filter(s=>s===codes[i]).length===1)earliestStop[i]=t+1;
}
assert.deepEqual(prefix_rank,[2,3,3,3,6,9,9,11,12]);
assert.equal(new Set(codes).size,12);
assert.equal(earliestStop.reduce((a,b)=>a+b,0),84);
assert.equal(Math.max(...earliestStop),9);

const Fzero=branches(zero,ai('F'))[0];
const silent=branches(Fzero,ai('B'))[0];
assert.equal(bitcount(silent),4);
assert.equal(silent,0x1111);
assert(branches(silent,ai('U')).length===1);
for(let a=0;a<18;a++)assert.equal(branches(silent,a).length,1,
 'All physical single-turn options must yield zero immediate orientation discrimination');
assert.equal(depth(silent),5);
const afterU=branches(silent,ai('U'))[0];
assert.deepEqual(branches(afterU,ai('F')).map(bitcount),[3,1]);

function greedy(initialSlot){
 let mask=zero,cur=2*initialSlot;
 for(let t=0;t<20;t++){
  if(bitcount(mask)===1)return {resolved:true,turns:t};
  let best=Infinity,aopt=-1;
  for(let a=0;a<18;a++){
   const worst=Math.max(...branches(mask,a).map(bitcount));
   if(worst<best){best=worst;aopt=a;}
  }
  cur=moves[aopt][cur];
  const child=branches(mask,aopt).find(b=>(b&(1<<cur))!==0);
  assert(child!==undefined);mask=child;
 }
 return {resolved:bitcount(mask)===1,turns:20,remaining:bitcount(mask)};
}
const greedyOutcomes=Array.from({length:12},(_,s)=>({slot:s,...greedy(s)}));
assert(greedyOutcomes.some(t=>!t.resolved));
const receipt={
 theorem_scope:'actual 18 3x3 HTM sticker-derived 24-state single UR edge, initial 12 orientation-zero positions',
 result:'CUBE_REV_021_P1_PHYSICAL_FEEDBACK_AND_SILENT_ACTION_PASS',
 historical_fixed_minimum_9:'inherited 0.19 P5 full length-8 lower-bound finite court, NOT recertified here',
 fixed_nine_turn_witness:word,
 fixed_witness_prefix_ranks:prefix_rank,
 fixed_witness_earliest_stop_turns:earliestStop,
 fixed_witness_mean_earliest_stop_uniform:84/12,
 adaptive_minimax_worst_depth:D,
 admissible_first_actions_first_step:firstActionCosts.filter(x=>x.worst_depth===D),
 other_first_actions_have_depth_8:firstActionCosts.filter(x=>x.worst_depth!==D).length===14,
 adaptive_expected_minimizing_total_turns_under_worst_7:total,
 adaptive_mean_turns_uniform:total/12,
 adaptive_policy_12_traces:policy,
 silent_transport:{
  transcript_prefix:['F:0','B:0'], belief_mask_hex:'0x'+silent.toString(16),
  belief_cardinality:bitcount(silent),all_18_immediate_moves_uninformative:true,
  remaining_exact_depth:depth(silent), U_next_cardinality:branches(silent,ai('U')).map(bitcount),
  F_after_U_cardinalities:branches(afterU,ai('F')).map(bitcount)
 },
 greedy_scope:'only a specific immediate-worst-cardinality heuristic with registry-order tie-breaking; NOT all greedy policies or humans',
 greedy_20_turn_probe:greedyOutcomes,
 warning:'9 versus 7 compares worst-case turns of ONE fixed word versus ONE feedback policy on SAME 12-source B. The old M*(5)=8 is a distinct preset dictionary cardinality. Expected turn figures explicitly assume uniform initial slot prior; no human participant data.'
};
console.log(JSON.stringify(receipt,null,2));
