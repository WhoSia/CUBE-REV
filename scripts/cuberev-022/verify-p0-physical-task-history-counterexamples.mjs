/**
 * CUBE-REV 0.22 P0: Exact physical one-bit decision-state abstraction court.
 * Legacy G3-P23/P26/P27/P29 quotient and belief×path laws explicitly inherited.
 * Verifies in genuine original sticker-derived 18-move 24-state tagged UR edge:
 * (1) candidate COUNT is not a sufficient 1-turn decision state;
 * (2) scalar optimal COST is not an action-labelled behavioural congruence;
 * (3) posterior SUPPORT alone fails to determine Bayesian optimal action when
 *     priors differ, using one real physically solvable 3-source example.
 * Nothing here measures any person's actual perception or cognition.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const maps=urMoveAutomaton();
assert.equal(maps.length,18);
const ZERO=Array.from({length:12},(_,i)=>2*i);
const split=(a,x,y)=>((maps[a][x]^maps[a][y])&1)!==0;
const splitActions=(x,y)=>ACTIONS.filter((_,a)=>split(a,x,y));
const pairProfiles=[];
for(let i=0;i<12;i++)for(let j=i+1;j<12;j++){
 const acts=splitActions(2*i,2*j);
 pairProfiles.push({slots:[i,j],split_action_count:acts.length,actions:acts});
}
assert.equal(pairProfiles.length,66);
const oneStep=pairProfiles.filter(x=>x.split_action_count>0);
const twoSteps=pairProfiles.filter(x=>x.split_action_count===0);
assert(oneStep.length>0 && twoSteps.length>0);
for(const p of twoSteps){
 const [u,v]=p.slots.map(i=>2*i);
 assert(maps.some((_,a)=>maps.some((_,b)=>split(b,maps[a][u],maps[a][v]))));
}
const profileGroups=new Map();
for(const p of pairProfiles){
 const code=p.actions.join(',');
 if(!profileGroups.has(code))profileGroups.set(code,[]);
 profileGroups.get(code).push(p.slots);
}
const firstPair=pairProfiles.find(p=>p.split_action_count>0);
const secondPair=pairProfiles.find(p=>p.split_action_count>0 &&
 p.actions.join(',')!==firstPair.actions.join(','));
assert(firstPair&&secondPair);
const separatingAction=firstPair.actions.find(a=>!secondPair.actions.includes(a));
const witnessPair=separatingAction?{first:firstPair,second:secondPair,first_only_action:separatingAction}:
 (()=>{const x=secondPair.actions.find(a=>!firstPair.actions.includes(a));assert(x);return {first:secondPair,second:firstPair,first_only_action:x};})();
assert(witnessPair.first.split_action_count&&witnessPair.second.split_action_count);
assert(!witnessPair.second.actions.includes(witnessPair.first_only_action));

const plans=[];
for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)for(let k=j+1;k<12;k++){
 const slots=[i,j,k],states=slots.map(p=>2*p);
 const alternatives=[];
 for(let t=0;t<3;t++){
  const choices=[];
  for(let a=0;a<18;a++){
   const outputs=states.map(s=>maps[a][s]&1);
   if(outputs.filter(b=>b===outputs[t]).length!==1)continue;
   const others=[0,1,2].filter(x=>x!==t);
   const updated=others.map(x=>maps[a][states[x]]);
   const ending=maps.findIndex((_,b)=>split(b,updated[0],updated[1]));
   if(ending>=0)choices.push({first_turn:ACTIONS[a],second_turn_if_two_left:ACTIONS[ending],
     first_action_index:a,second_action_index:ending,isolated_initial_slot:slots[t],
     remaining_initial_slots:others.map(x=>slots[x])});
  }
  if(choices.length)alternatives.push({t,choices});
 }
 if(alternatives.length>=2)plans.push({slots,alternatives});
}
assert(plans.length>0);
const selected=plans[0],planA=selected.alternatives[0].choices[0],
 planB=selected.alternatives[1].choices[0];
assert.notEqual(planA.isolated_initial_slot,planB.isolated_initial_slot);
// Probability measure A: 0.9 on the first singled source; 0.05 on each other;
// measure B: 0.9 on second singled source. Both have *identical support*.
const makeWeights=focus=>selected.slots.map(i=>i===focus?0.9:0.05);
const wa=makeWeights(planA.isolated_initial_slot),wb=makeWeights(planB.isolated_initial_slot);
const expectedTime=(weights,firstAction)=>{
 const outputs=selected.slots.map(slot=>maps[firstAction][2*slot]&1);
 const prob0=weights.reduce((s,p,i)=>s+(outputs[i]===0?p:0),0);
 const prob1=1-prob0;
 // Leaf after one read iff exactly one source in the observed outcome group.
 const leafContribution=[0,1].reduce((s,o)=>{
  const idx=outputs.map((v,i)=>v===o?i:null).filter(i=>i!==null);
  return s+(idx.length===1?0:weights.reduce((s,p,i)=>s+(outputs[i]===o?p:0),0));
 },0);
 return 1+leafContribution; // lower bound: each non-singleton after first turn needs ≥1 more
};
const outputGrade=(a)=>selected.slots.map(i=>maps[a][2*i]&1).join('');
// Exhaustive first-action lower-bound argument, physically authenticated action splits:
// to get E[T]<=1.1 from a 0.9-heavy hypothesis, it MUST be a singleton
// in the first observed branch (otherwise E[T]>=1.9). Both plans achieve
// EXACT 1.1 as remaining pair can be split by a legal second turn.
for(const [w,focus,witness] of [[wa,planA.isolated_initial_slot,planA],[wb,planB.isolated_initial_slot,planB]]){
 const a=witness.first_action_index;
 assert.equal(expectedTime(w,a),1.1);
 assert.equal(selected.slots[outputGrade(a).split('').indexOf(String(maps[a][2*focus]&1))],focus);
 for(let other=0;other<18;other++){
  if(other===a)continue;
  const vals=selected.slots.map(s=>maps[other][2*s]&1);
  if(vals.filter(v=>v===vals[selected.slots.indexOf(focus)]).length===1)continue;
  assert(expectedTime(w,other)>=1.9-1e-10);
 }
}
const oneHotActionsFor=(target)=>{
 const i=selected.slots.indexOf(target);
 return ACTIONS.filter((_,a)=>{
  const outs=selected.slots.map(slot=>maps[a][2*slot]&1);
  if(outs.filter(b=>b===outs[i]).length!==1)return false;
  const otherStates=selected.slots.filter(slot=>slot!==target).map(slot=>maps[a][2*slot]);
  return maps.some((_,b)=>split(b,otherStates[0],otherStates[1]));
 });
};
const optimalClassesA=oneHotActionsFor(planA.isolated_initial_slot);
const optimalClassesB=oneHotActionsFor(planB.isolated_initial_slot);
assert(optimalClassesA.length>0&&optimalClassesB.length>0);
assert(optimalClassesA.every(a=>!optimalClassesB.includes(a)));
// For three states in 2-turn binary identification, first split MUST have
// singleton branch and its complement pair must be separable in 1 extra turn.
// We verified existence for both focused choices.
const tuple={
 marker:'CUBE_REV_022_P0_PHYSICAL_TASK_RELATIVE_DECISION_SUFFICIENCY_COUNTEREXAMPLES_PASS',
 model:'original 18 legal HTM sticker-derived maps, tagged edge 24 states, intrinsic post-turn orientation bit, initial flip-zero 12 slots',
 legacy_theorem_boundary:'G3-P23-P29 dynamic quotient and belief×path semantics are prior results, NOT new 0.22 discoveries',
 pairwise:{
  total_distinct_two_slot_zero_flip_beliefs:66,
  separable_by_one_real_turn_and_one_read:oneStep.length,
  requiring_at_least_two_real_turns_before_a_read_can_separate:twoSteps.length,
  distinct_one_turn_action_labelled_split_profiles:profileGroups.size,
  same_scalar_cost_but_incompatible_action_labelled_observation_protocol:witnessPair,
  previous_P8_counterexample_0_1_one_turn:splitActions(0,2).length>0,
  previous_P8_counterexample_0_2_one_turn:splitActions(0,4).length>0
 },
 nonuniform_bayesian:{
  same_candidate_support_initial_slots:selected.slots,
  prior_A:wa,
  prior_B:wb,
  prior_A_optimal_one_turn_isolated_source:planA.isolated_initial_slot,
  prior_B_optimal_one_turn_isolated_source:planB.isolated_initial_slot,
  same_optimal_cost_E_turns_for_both:1.1,
  known_solvable_two_turn_policies:{A:planA,B:planB},
  optimal_one_step_action_sets:{A:optimalClassesA,B:optimalClassesB},
  intersection_of_optimal_action_sets:optimalClassesA.filter(x=>optimalClassesB.includes(x)),
  one_turn_lower_bound_for_nonisolating_heavy_hypothesis_Eturns:1.9,
  caveat:'Different assumed priors across tasks, not two posteriors derived from one fixed uniform prior; no claim about human strategy preference.'
 },
 theorem:'For known reversible physical transitions and noiseless measured output, weighted current posterior plus remaining turn/query budgets is sufficient to propagate future Bayesian experiments; cardinality and unweighted support are not sufficient for all objectives/priors.',
 right_congruence_warning:'Equality of one scalar optimal residual cost is weaker than equal action-labelled observation transition signatures. Any quotient intended for reuse under actions must be checked for transition and observation stability, not just value.',
 no_claims:'No minimal reachable belief-controller quotient proved. No measured human cost, no actual full-cube or FMC visual observation.'
};
assert(tuple.pairwise.previous_P8_counterexample_0_1_one_turn===true);
assert(tuple.pairwise.previous_P8_counterexample_0_2_one_turn===false);
console.log(JSON.stringify(tuple,null,2));
