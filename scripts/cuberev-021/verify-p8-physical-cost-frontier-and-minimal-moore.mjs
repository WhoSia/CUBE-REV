/** CUBE-REV 0.21 P8 — physical, sticker-derived exact cost Pareto frontier
 *
 * 12 unknown initial flip-zero slots for a tagged UR edge, legal 18 HTM Rubik
 * turns, intrinsic orientation-bit sensor optionally queried after each turn.
 *
 * Distinguish: (i) worst turns <=7, no hard query cap, charge query cost;
 *             (ii) worst turns <=7 AND worst queries <=4.
 *
 * Every Bellman score below is sum over individual uniform-prior sources
 * (integer leaf lengths), NOT a human physical/survey or FMC observation.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const MAPS=urMoveAutomaton(),EVEN=0x555555,ODD=((1<<24)-1)^EVEN,START=EVEN;
assert.equal(MAPS.length,18);
assert.equal(ACTIONS.length,18);
for(const map of MAPS)assert.deepEqual([...map].sort((a,b)=>a-b),Array.from({length:24},(_,i)=>i));

const transitions=new Map();
const step=(mask,a)=>{
 const k=mask+','+a;
 if(transitions.has(k))return transitions.get(k);
 let b=mask,out=0;
 while(b){const x=b&-b,source=31-Math.clz32(x);b^=x;out|=1<<MAPS[a][source];}
 transitions.set(k,out);return out;
};
const count=m=>{let n=0;while(m){n++;m&=m-1;}return n;};
function exactPolicy({p,q=1,turnCap=7,queryCap=null}){
 assert(Number.isInteger(p)&&p>=0&&Number.isInteger(q)&&q>0);
 const memo=new Map();
 function solve(mask,h,k){
  const m=count(mask);
  if(m===1)return {T:0,Q:0,action:null,mode:'done'};
  if(h===0||k===0||m>2**Math.min(h,k))return null;
  const key=mask+','+h+','+k;
  if(memo.has(key))return memo.get(key);
  let best=null, bestScore=Infinity;
  const offer=(action,mode,T,Q)=>{
   const score=q*T+p*Q;
   if(score<bestScore || (score===bestScore&&best&&(Q<best.Q||(Q===best.Q&&T<best.T)))){
    best={T,Q,action,mode};bestScore=score;
   }
  };
  for(let a=0;a<18;a++){
   const after=step(mask,a),left=after&EVEN,right=after&ODD;
   // Query a bit when it *actually* splits candidates.
   if(left&&right){
    const x=solve(left,h-1,k-1);
    if(x){
     const y=solve(right,h-1,k-1);
     if(y)offer(a,'read',m+x.T+y.T,m+x.Q+y.Q);
    }
   }
   // Under h<=k a query is cost-free in cardinality of future reads only
   // when p=0; for positive p a silent option is always needed.
   const z=solve(after,h-1,k);
   if(z)offer(a,'silent',m+z.T,z.Q);
  }
  memo.set(key,best);return best;
 }
 const horizon=turnCap,observations=queryCap===null?turnCap:queryCap;
 const root=solve(START,horizon,observations);
 assert(root,'no fully identifying physical policy with these resources');
 function replay(slot){
  let mask=START,physical=2*slot,h=horizon,k=observations;
  const steps=[],readBits=[];
  while(count(mask)>1){
   const choice=solve(mask,h,k);
   assert(choice&&choice.action!==null);
   const action=choice.action;
   physical=MAPS[action][physical];
   const next=step(mask,action),isRead=choice.mode==='read';
   if(isRead){
    const bit=physical&1;
    mask=next&(bit?ODD:EVEN);
    readBits.push(bit);
    k--;
   }else mask=next;
   steps.push({turn:ACTIONS[action],read:isRead,observed_bit:isRead?physical&1:null});
   h--;
   assert(h>=0&&k>=0&&(mask&(1<<physical))!==0);
  }
  assert.equal(mask,1<<physical);
  return {initial_slot:slot,steps,read_bits:readBits.join(''),turns:steps.length,reads:readBits.length,final_tracked_edge_state:physical};
 }
 const witnesses=Array.from({length:12},(_,i)=>replay(i));
 assert.equal(new Set(witnesses.map(w=>w.read_bits)).size,12);
 for(let i=0;i<witnesses.length;i++)for(let j=i+1;j<witnesses.length;j++){
  assert(!witnesses[i].read_bits.startsWith(witnesses[j].read_bits));
  assert(!witnesses[j].read_bits.startsWith(witnesses[i].read_bits));
 }
 const T=witnesses.reduce((s,w)=>s+w.turns,0);
 const Q=witnesses.reduce((s,w)=>s+w.reads,0);
 assert.equal(T,root.T);assert.equal(Q,root.Q);
 assert(witnesses.every(w=>w.turns<=turnCap));
 if(queryCap!==null)assert(witnesses.every(w=>w.reads<=queryCap));
 const kraft=witnesses.reduce((s,w)=>s+2**(-w.reads),0);
 assert.equal(kraft,1);
 return {p,q,queryCap,turnCap,T,Q,weighted_integer_root:q*T+p*Q,
  recursion_states:memo.size, move_belief_cache:transitions.size,
  worst_turns:Math.max(...witnesses.map(w=>w.turns)),
  worst_reads:Math.max(...witnesses.map(w=>w.reads)),
  turn_depth_distribution:Object.fromEntries([...new Set(witnesses.map(w=>w.turns))].sort((a,b)=>a-b).map(n=>[n,witnesses.filter(w=>w.turns===n).length])),
  read_depth_distribution:Object.fromEntries([...new Set(witnesses.map(w=>w.reads))].sort((a,b)=>a-b).map(n=>[n,witnesses.filter(w=>w.reads===n).length])),
  kraft_sum:kraft,witnesses};
}
// Primary exact 7-turn Bellman duals: lambda=0 and lambda=3 and lambda=4.
const turnFirst=exactPolicy({p:0});
const dualTie=exactPolicy({p:3});
const queryFirst=exactPolicy({p:4});
const hardCap=exactPolicy({p:0,queryCap:4});
const hardCapLarge=exactPolicy({p:100,queryCap:4});
assert.deepEqual([turnFirst.T,turnFirst.Q],[71,45]);
assert.deepEqual([dualTie.T,dualTie.Q],[74,44]);
assert.deepEqual([queryFirst.T,queryFirst.Q],[74,44]);
assert.deepEqual([hardCap.T,hardCap.Q],[74,44]);
assert.deepEqual([hardCapLarge.T,hardCapLarge.Q],[74,44]);
assert.equal(turnFirst.worst_reads,5,'T-minimizer uses 5 queries on some states and is NOT hard-cap4 feasible');
assert.equal(queryFirst.worst_reads,4);
assert.equal(hardCap.worst_reads,4);
assert.equal(71+3*45,206);assert.equal(74+3*44,206);
// For every feasible policy under 7-turn horizon, exact scalar DP supplies
//  T>=71 and T+3Q>=206. Uniform prefix code entails Q>=ceil(12log2 12)=44.
// Hence Q>=45 policies are dominated by (71,45); Q=44 implies T>=74.
// Thus EXACT global Pareto frontier contains precisely these two vertices.
assert.equal(Math.ceil(12*Math.log2(12)),44);

// Machine minimization: full 24 Moore states, observable intrinsic bit.
// Profiles at depth d consist of output and actions leading to profiles d-1.
// This checks right-distinguishability under <=2 actions, NOT one fixed word.
const label0=Array.from({length:24},(_,i)=>i%2);
function refine(old){
 const keys=new Map(),labels=[];
 for(let s=0;s<24;s++){
  const sig=JSON.stringify([old[s],...MAPS.map(m=>old[m[s]])]);
  if(!keys.has(sig))keys.set(sig,keys.size);
  labels.push(keys.get(sig));
 }
 return labels;
}
const countClasses=labels=>new Set(labels).size;
const label1=refine(label0),label2=refine(label1);
assert.deepEqual([countClasses(label0),countClasses(label1),countClasses(label2)],[2,6,24]);
const depths={0:0,1:0,2:0};
for(let i=0;i<24;i++)for(let j=i+1;j<24;j++){
 const d=label0[i]!==label0[j]?0:label1[i]!==label1[j]?1:2;
 assert(d===2?label2[i]!==label2[j]:true);
 depths[d]++;
}
assert.deepEqual(depths,{'0':144,'1':96,'2':36});
const separableOneTurn=(i,j)=>MAPS.some(a=>(a[i]&1)!==(a[j]&1));
assert(separableOneTurn(0,2),'original even-state slots 0 and 1 separable by a move');
assert(!separableOneTurn(0,4),'original even-state slots 0 and 2 NOT separable by ANY single move');
const distinguishingAction=ACTIONS.find((_,a)=>(MAPS[a][0]&1)!==(MAPS[a][2]&1));
assert(['F',"F'"].includes(distinguishingAction));

// Bellman sufficiency: deterministic state permutations + uniform initial
// posterior mean current belief carries all conditional future possibilities;
// h and query cap (if any) complete the finite resource-bounded controller state.
// It is not asserted that the resulting entire belief automaton is minimal.
console.log(JSON.stringify({
 marker:'CUBE_REV_021_P8_EXACT_REAL_RUBIK_COST_PARETO_AND_MOORE_MINIMIZATION_PASS',
 verified_instance:'original full-sticker-induced UR tagged edge; 12 initially flip-zero sources, 18 HTM face actions and optional 1-bit orientation read',
 assumption:'uniform prior on the 12 physical initial slots; deterministic/noiseless sensor; one query max after each legal physical turn; complete identification by at most 7 turns',
 objective_without_query_cap:'min expected HTM turns + lambda * expected number of bit-read operations',
 root_integer_dual_lower_bounds:{T_at_least:71,Q_at_least_via_binary_entropy:44,T_plus_3Q_at_least:206},
 exact_mean_cost_pareto_uncapped_7_turns:[{T:71,Q:45},{T:74,Q:44}],
 exact_scalar_switch:{lambda_less_than_3:[71,45],lambda_equal_3:'both optimal',lambda_greater_than_3:[74,44]},
 hard_7_turn_4_query_cap_optimum:{T:74,Q:44,policy_feasible_with_max_turns:7,max_reads_per_source:4},
 previous_p7_constructive_policy:{T:80,Q:44,dominated_in_mean_by_P8:true,still_valid_in_p7_worst_case:true},
 read_cap_warning:'T=71,Q=45 uses five reads for some sources and violates max-four-query cap',
 moore_24_state_output_minimization:{original_states:24,zero_action_classes:2,one_action_response_classes:6,two_action_response_classes:24,shortest_pair_distinguish_depth_counts:depths,full_machine_minimal_under_all_action_words:true},
 belief_cardinality_insufficient_counterexample:{same_size:2,horizon:1,source_even_slots_0_1_distinguishable:true,source_even_slots_0_2_distinguishable:false,one_turn_separating_action:distinguishingAction},
 controller_state_sufficiency:'posterior current belief 24-bit mask + remaining move and query budget; with any fixed prior replace uniform count by posterior weights',
 no_claims:'no theorem identifying minimum policy-controller memory size; no human cognition/cost coefficients inferred; not an ordinary untagged sticker photograph or complete FMC search',
 scalar_objectives:[
  {p:0,q:1,T:turnFirst.T,Q:turnFirst.Q,dp_states:turnFirst.recursion_states,read_dist:turnFirst.read_depth_distribution},
  {p:3,q:1,T:dualTie.T,Q:dualTie.Q,dp_states:dualTie.recursion_states,read_dist:dualTie.read_depth_distribution},
  {p:4,q:1,T:queryFirst.T,Q:queryFirst.Q,dp_states:queryFirst.recursion_states},
  {p:0,q:1,queryCap:4,T:hardCap.T,Q:hardCap.Q,dp_states:hardCap.recursion_states},
  {p:100,q:1,queryCap:4,T:hardCapLarge.T,Q:hardCapLarge.Q,dp_states:hardCapLarge.recursion_states}
 ],
 witnesses:{turn_first:turnFirst.witnesses,query_first:queryFirst.witnesses,strict_cap7_4:hardCap.witnesses},
 kraft_certificates:{turn_first:turnFirst.kraft_sum,query_first:queryFirst.kraft_sum},
 all_physical_witnesses_replayed:true
},null,2));
