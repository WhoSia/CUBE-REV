/**
 * CUBE-REV 0.22 P1: exact source-specific two-hypothesis belief quotient.
 * Imported maps are 18 original physical HTM sticker-cube permutations.
 * Congruence preserves silent/read action, binary observation label,
 * reached pair class and terminal identification. NOT full 12-source memory.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const moves=urMoveAutomaton();
assert.equal(moves.length,18);
const all=Array.from({length:24},(_,i)=>i);
for(const a of moves)assert.deepEqual([...a].sort((x,y)=>x-y),all);
const pairMask=(i,j)=>(1<<i)|(1<<j);
const states=[],lookup=new Map();
for(let u=0;u<24;u++)for(let v=u+1;v<24;v++){
  const i=states.length,mask=pairMask(u,v);
  states.push({u,v,mask});lookup.set(mask,i);
}
assert.equal(states.length,276);
const roots=states.map((s,i)=>s.u%2===0&&s.v%2===0?i:-1).filter(i=>i>=0);
assert.equal(roots.length,66);
const transitions=states.map(s=>moves.map(a=>{
  const u=a[s.u],v=a[s.v],to=lookup.get(pairMask(u,v));
  assert(Number.isInteger(to));
  const p=u&1,q=v&1;
  return {to,split:p!==q,knownBit:p===q?p:null};
}));
const reachable=new Set(roots),todo=[...reachable];
for(let i=0;i<todo.length;i++){
 for(const t of transitions[todo[i]])if(!reachable.has(t.to)){
  reachable.add(t.to);todo.push(t.to);
 }
}
const ids=[...reachable].sort((a,b)=>a-b);
const ix=new Map(ids.map((id,i)=>[id,i]));
for(const id of ids)for(const t of transitions[id])assert(ix.has(t.to));
const inSameSlot=states.map((s,i)=>Math.floor(s.u/2)===Math.floor(s.v/2)?i:-1).filter(x=>x>=0);
assert.equal(inSameSlot.length,12);
assert(inSameSlot.every(i=>!reachable.has(i)));
function canonical(keys){
  const d=new Map(),out=[];
  for(const k of keys){if(!d.has(k))d.set(k,d.size);out.push(d.get(k));}
  return {labels:out,count:d.size};
}
function refine(current){
  const keys=ids.map((id,i)=>{
    const signature=transitions[id].map(t=>{
      const c=current[ix.get(t.to)];
      return [c,t.split?'SPLIT':('SAME_BIT_'+t.knownBit+'_CLASS_'+c)];
    });
    // single bit-inspection costs 1 query, silent costs 0 queries;
    // both pay 1 HTM turn, and have action-labelled class transitions.
    return JSON.stringify([current[i],signature]);
  });
  return canonical(keys);
}
const levels=[{depth:0,labels:ids.map(()=>0),count:1}];
for(let depth=1;depth<35;depth++){
  const next=refine(levels.at(-1).labels);
  assert(next.count>=levels.at(-1).count);
  levels.push({depth,...next});
  if(next.count===levels.at(-2).count)break;
}
assert(levels.at(-1).count===levels.at(-2).count);
const final=levels.at(-1),minClasses=final.count;
for(let a=0;a<ids.length;a++)for(let b=a+1;b<ids.length;b++){
  if(final.labels[a]!==final.labels[b])continue;
  for(let m=0;m<18;m++){
    const A=transitions[ids[a]][m],B=transitions[ids[b]][m];
    assert.equal(A.split,B.split);
    if(!A.split)assert.equal(A.knownBit,B.knownBit);
    assert.equal(final.labels[ix.get(A.to)],final.labels[ix.get(B.to)]);
  }
}
const counts=levels.map(l=>({
  depth:l.depth,
  reachable_pair_classes:l.count,
  distinct_classes_among_initial_66:new Set(roots.map(id=>l.labels[ix.get(id)])).size
}));
const r0=lookup.get(pairMask(0,2)),r1=lookup.get(pairMask(0,6));
assert(roots.includes(r0)&&roots.includes(r1));
const splittingAction=p=>ACTIONS.filter((_,a)=>transitions[p][a].split);
assert.deepEqual(splittingAction(r0),['F',"F'"]);
assert.deepEqual(splittingAction(r1),['B',"B'"]);
function firstDifferent(a,b){
 for(const l of levels)if(l.labels[ix.get(a)]!==l.labels[ix.get(b)])return l.depth;
 return null;
}
assert.equal(firstDifferent(r0,r1),1);
const splitProfiles=new Map();
for(const id of roots){
 const profile=splittingAction(id).join('|');
 splitProfiles.set(profile,(splitProfiles.get(profile)||0)+1);
}
const histogram=Object.fromEntries([...splitProfiles].map(([k,v])=>[k||'NO_ONE_TURN_SPLIT',v]));
assert.deepEqual(histogram,{'F|F\'':16,'F|F\'|B|B\'':16,'B|B\'':16,'NO_ONE_TURN_SPLIT':18});
const unequalAtTwo=[];
for(let i=0;i<roots.length;i++)for(let j=i+1;j<roots.length;j++){
 const a=roots[i],b=roots[j];
 if(firstDifferent(a,b)===2&&unequalAtTwo.length<6){
  unequalAtTwo.push({first_slots:[states[a].u/2,states[a].v/2],
   second_slots:[states[b].u/2,states[b].v/2]});
 }
}
// Independently exhaust all short literal observation protocols, not using
// partition-refinement labels. An early READ may already identify and terminate;
// SILENT then READ is a different legal protocol with only one paid bit read.
const directOneReadTrace=(p,a)=>{
 const x=moves[a][p.u]&1,y=moves[a][p.v]&1;
 return x!==y?'0:GOAL|1:GOAL':(String(x)+':PAIR');
};
const directTwoReadTrace=(p,a,b)=>{
 let x=moves[a][p.u],y=moves[a][p.v];
 if((x&1)!==(y&1))return '0:GOAL|1:GOAL';
 const first=x&1;
 x=moves[b][x];y=moves[b][y];
 if((x&1)!==(y&1))return first+'0:GOAL|'+first+'1:GOAL';
 return first+String(x&1)+':PAIR';
};
const directSilentThenReadTrace=(p,a,b)=>{
 const x=moves[b][moves[a][p.u]]&1,y=moves[b][moves[a][p.v]]&1;
 return x!==y?'0:GOAL|1:GOAL':(String(x)+':PAIR');
};
const earlySignatures=new Map(),allSignatures=new Map();
for(const id of ids){
 const p=states[id],early=[],complete=[];
 for(let a=0;a<18;a++){
  const first=directOneReadTrace(p,a);
  early.push(first);complete.push(first);
  for(let b=0;b<18;b++){
   const e=directTwoReadTrace(p,a,b);
   early.push(e);complete.push(e);
   complete.push(directSilentThenReadTrace(p,a,b));
  }
 }
 const kEarly=early.join(';'),kAll=complete.join(';');
 if(!earlySignatures.has(kEarly))earlySignatures.set(kEarly,[]);
 earlySignatures.get(kEarly).push(id);
 if(!allSignatures.has(kAll))allSignatures.set(kAll,[]);
 allSignatures.get(kAll).push(id);
}
const readEachTurnClasses=earlySignatures.size;
const allProtocolsClasses=allSignatures.size;
assert.equal(readEachTurnClasses,139);
assert.equal(allProtocolsClasses,264);
const firstSilentWitness=(()=>{
 for(const block of earlySignatures.values()){
  if(block.length<2)continue;
  for(let i=0;i<block.length;i++)for(let j=i+1;j<block.length;j++){
   const P=states[block[i]],Q=states[block[j]];
   for(let a=0;a<18;a++)for(let b=0;b<18;b++){
    const x=directSilentThenReadTrace(P,a,b);
    const y=directSilentThenReadTrace(Q,a,b);
    if(x!==y)return {
      belief1_physical_edge_states:[P.u,P.v],
      belief2_physical_edge_states:[Q.u,Q.v],
      legal_silent_then_read_turns:[ACTIONS[a],ACTIONS[b]],
      first_trace:x,second_trace:y,
      certified_read_every_turn_experiments_up_to_two_indistinguishable:true
    };
   }
  }
 }
 return null;
})();
assert(firstSilentWitness);
let oneActionSeparated=0,twoActionsNeeded=0;
for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){
 const P=states[ids[i]],Q=states[ids[j]];
 let distinct=false,depth=0;
 for(let a=0;a<18;a++)if(directOneReadTrace(P,a)!==directOneReadTrace(Q,a)){
  distinct=true;depth=1;break;
 }
 if(!distinct){
  outer:for(let a=0;a<18;a++)for(let b=0;b<18;b++){
   if(directTwoReadTrace(P,a,b)!==directTwoReadTrace(Q,a,b) ||
      directSilentThenReadTrace(P,a,b)!==directSilentThenReadTrace(Q,a,b)){
     distinct=true;depth=2;break outer;
   }
  }
 }
 assert(distinct,'every pair of distinct reachable two-source beliefs admits <=2 legal turn observational protocol distinguishing them');
 if(depth===1)oneActionSeparated++;else twoActionsNeeded++;
}
assert.equal(oneActionSeparated+twoActionsNeeded,264*263/2);
const minimumFixedWidthStateBits=Math.ceil(Math.log2(ids.length+1));
assert.equal(minimumFixedWidthStateBits,9); // 264 nonterminal + 1 terminal.

const output={
 marker:'CUBE_REV_022_P1_PHYSICAL_TWO_SOURCE_ACTION_LABELLED_QUOTIENT_PASS',
 model:'original legal 18 HTM sticker-derived Rubik action permutations; binary intrinsic orientation read after turn',
 goal:'separate two unknown initially distinct-slot tagged edge source hypotheses; singleton recognition terminal',
 interface:'each physical face turn supports SILENT or READ; READ reports actual bit and/or terminal separation; costs are fixed 1 turn and optional 1 read',
 states:{all_unordered_24_edge_state_pairs:276,initial_zero_flip_two_slot_pairs:66,
  reachable_pair_states_under_common_legal_action_words:ids.length,
  original_same_slot_opposite_flip_pairs_proven_unreachable:12},
 labelled_congruence:{
  quotient_class_counts_by_refinement:counts,
  stabilization_round:levels.at(-1).depth,
  stable_minimum_number_of_classes_for_defined_action_observation_interface:minClasses,
  physical_labelled_transition_bisimulation_explicitly_checked:true,
  direct_short_experiment_certificate:{
    one_turn_read_protocols:18,
    two_turn_read_each_turn_protocols:324,
    two_turn_silent_then_read_protocols:324,
    read_after_every_turn_short_protocol_classes:readEachTurnClasses,
    read_or_silent_short_protocol_classes:allProtocolsClasses,
    extra_required_silent_then_read_witness:firstSilentWitness,
    fully_distinct_reachable_belief_transcript_signatures:allProtocolsClasses,
    distinct_pair_belief_comparisons_separated_by_one_action:oneActionSeparated,
    additional_pair_belief_comparisons_requiring_two_action_experiment:twoActionsNeeded,
    full_unordered_264_state_pair_comparisons:264*263/2,
    exact_logical_fixed_width_bits_for_264_nonterminal_and_one_terminal:minimumFixedWidthStateBits
  },
  initial_equal_cost_but_incompatible_first_action_pairs:[[0,1],[0,3]],
  separation_depth_of_p0_scalar_equivalence_counterexample:firstDifferent(r0,r1),
  initial_action_split_profile_histogram:histogram,
  two_step_new_separation_examples:unequalAtTwo
 },
 proof:'finite monotone partition refinement from indiscriminate nonterminal pairs; stable partition is the largest action-labelled congruence preserving read outputs, silent transitions and termination; any strictly larger merge differs at a shortest finite refined distinguishing experiment',
 previous_generation_iii_authority:'G3-P23,P26,P27,P29 formal quotient/sufficiency already proven; P1 contributes this actual legal-cube reachable-pair quotient instance',
 boundaries:'the quotient preserves the pair-task cost/observation interface, NOT necessarily initial-source naming or all priors; minimum memory for all 12-source original controller NOT proved; no human video or new participants'
};
console.log(JSON.stringify(output,null,2));
