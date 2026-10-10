/**
 * CUBE-REV 0.22 P2 — counterexample-first belief-as-model-object audit.
 * Uses original 18 legal sticker-derived Rubik HTM turns.
 * Distinguishes full 12-source optimal policy DAGs (chosen tie-break),
 * cost regime and query-cap effects, support/cardinality compression failures,
 * and joint physical-state / observation-channel uncertainty.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const MAP=urMoveAutomaton(),EVEN=0x555555,FULL=(1<<24)-1,ODD=FULL^EVEN;
assert.equal(MAP.length,18);
for(const map of MAP)assert.deepEqual([...map].sort((a,b)=>a-b),Array.from({length:24},(_,i)=>i));
const size=m=>{let z=0;while(m){m&=m-1;z++;}return z;};
const bit=x=>x&1;
const movecache=new Map();
const push=(mask,action)=>{
  const k=mask+':'+action;if(movecache.has(k))return movecache.get(k);
  let b=mask,x=0;
  while(b){const lo=b&-b,idx=31-Math.clz32(lo);x|=1<<MAP[action][idx];b-=lo;}
  movecache.set(k,x);return x;
};
const optimise=(price,queryCap=null)=>{
  const memo=new Map(),cap=queryCap===null?7:queryCap;
  const better=(candidate,best)=>{
    if(!best)return true;
    const c=candidate.T+price*candidate.Q,d=best.T+price*best.Q;
    if(c!==d)return c<d;
    if(candidate.Q!==best.Q)return candidate.Q<best.Q;
    if(candidate.T!==best.T)return candidate.T<best.T;
    if(candidate.a!==best.a)return candidate.a<best.a;
    return candidate.mode<best.mode;
  };
  function solve(mask,h,k){
    if(size(mask)===1)return {T:0,Q:0,a:null,mode:'TERMINAL'};
    if(h===0||k===0||size(mask)>2**Math.min(h,k))return null;
    const key=mask+':'+h+':'+k;
    if(memo.has(key))return memo.get(key);
    const m=size(mask);let best=null;
    for(let a=0;a<18;a++){
      const next=push(mask,a);
      const x=next&EVEN,y=next&ODD;
      if(x&&y&&k>0){
        const l=solve(x,h-1,k-1),r=solve(y,h-1,k-1);
        if(l&&r){
          const o={T:m+l.T+r.T,Q:m+l.Q+r.Q,a,mode:'READ'};
          if(better(o,best))best=o;
        }
      }
      if(h>1){
        const v=solve(next,h-1,k);
        if(v){
          const o={T:m+v.T,Q:v.Q,a,mode:'SILENT'};
          if(better(o,best))best=o;
        }
      }
    }
    memo.set(key,best);return best;
  }
  const root=solve(EVEN,7,cap);assert(root);
  const internalStates=new Set(),sigAnon=new Set(),sigOrigin=new Set(),allW=[];
  const remaining=set=>Object.fromEntries([...set].map(([k,v])=>[k,v]));
  function trace(mask,h,k,orig,actions=[],observed=''){
    assert(orig.size===size(mask));
    const physicalStates=new Set(orig.values());
    assert([...physicalStates].reduce((x,s)=>x|1<<s,0)===mask);
    if(size(mask)===1){
      const slot=[...orig.keys()][0];
      const anon='DONE';
      const named='DONE_SOURCE_'+slot;
      sigAnon.add(anon);sigOrigin.add(named);
      allW.push({source_slot:slot,actions,observed,turns:actions.length,reads:observed.length});
      return {anon,named};
    }
    const policy=solve(mask,h,k);assert(policy&&policy.a!==null);
    const key=mask+':'+h+':'+k;
    internalStates.add(key);
    const acted=new Map([...orig].map(([i,s])=>[i,MAP[policy.a][s]]));
    const newmask=push(mask,policy.a);
    const name=ACTIONS[policy.a];
    let out;
    if(policy.mode==='SILENT'){
      const nxt=trace(newmask,h-1,k,acted,[...actions,{turn:name,query:false}],observed);
      out={anon:JSON.stringify([name,'S',nxt.anon]),named:JSON.stringify([name,'S',nxt.named])};
    } else {
      const parts=[new Map(),new Map()];
      for(const [i,s] of acted)parts[bit(s)].set(i,s);
      assert(parts[0].size&&parts[1].size);
      const ch=parts.map((group,b)=>trace(newmask&(b?ODD:EVEN),h-1,k-1,group,
        [...actions,{turn:name,query:true,bit:b}],observed+b));
      out={anon:JSON.stringify([name,'R',ch[0].anon,ch[1].anon]),
        named:JSON.stringify([name,'R',ch[0].named,ch[1].named])};
    }
    sigAnon.add(out.anon);sigOrigin.add(out.named);
    return out;
  }
  trace(EVEN,7,cap,new Map(Array.from({length:12},(_,i)=>[i,2*i])));
  assert.equal(allW.length,12);
  assert.equal(new Set(allW.map(w=>w.source_slot)).size,12);
  const T=allW.reduce((s,w)=>s+w.turns,0),Q=allW.reduce((s,w)=>s+w.reads,0);
  assert.equal(T,root.T);assert.equal(Q,root.Q);
  assert(allW.every(w=>w.turns<=7&&w.reads<=cap));
  const codeStrings=allW.map(w=>w.observed);
  for(let i=0;i<12;i++)for(let j=i+1;j<12;j++){
    assert(!codeStrings[i].startsWith(codeStrings[j]));
    assert(!codeStrings[j].startsWith(codeStrings[i]));
  }
  return {price,queryCap:queryCap??'UNCAPPED',total_T:T,total_Q:Q,
    mean_T:T/12,mean_Q:Q/12,max_turn:Math.max(...allW.map(w=>w.turns)),
    max_reads:Math.max(...allW.map(w=>w.reads)),dp_states:memo.size,
    chosen_policy:{distinct_belief_budget_nodes:internalStates.size,
      anonymous_termination_minimal_structural_policy_nodes:sigAnon.size,
      source_named_terminal_structural_policy_nodes:sigOrigin.size,
      leaf_worlds:allW.length,
      action_word_signatures_included:true,
      not_minimum_over_all_equally_optimal_policies:true},
    first_action:ACTIONS[root.a],first_mode:root.mode,
    first_three_witnesses:allW.slice(0,3),all_source_witnesses:allW};
};
const policies=[optimise(0),optimise(1),optimise(3),optimise(4),
                optimise(0,4),optimise(4,4)];
assert.deepEqual([policies[0].total_T,policies[0].total_Q],[71,45]);
assert.deepEqual([policies[1].total_T,policies[1].total_Q],[71,45]);
assert.deepEqual([policies[2].total_T,policies[2].total_Q],[74,44]);
assert.deepEqual([policies[3].total_T,policies[3].total_Q],[74,44]);
assert.deepEqual([policies[4].total_T,policies[4].total_Q],[74,44]);
assert.deepEqual([policies[5].total_T,policies[5].total_Q],[74,44]);
assert.equal(policies[0].max_reads,5);
assert.equal(policies[4].max_reads,4);
const shift=(policies[0].first_action!==policies[3].first_action||
             policies[0].first_mode!==policies[3].first_mode||
             JSON.stringify(policies[0].all_source_witnesses)!==JSON.stringify(policies[3].all_source_witnesses));
assert(shift,'price must change chosen policy in full original 12 source problem');
// Explore ALL PHYSICAL ACTIONS AND OPTIONAL OBSERVATIONS at the root for the
// first <=3 moves ONLY. This deliberately does not claim an exhaustive
// all-policy horizon-seven belief reachability census.
const prefixes=[new Set([EVEN])];
for(let depth=1;depth<=3;depth++){
 const nxt=new Set();
 for(const mask of prefixes.at(-1)){
   if(size(mask)===1)continue;
   for(let a=0;a<18;a++){
     const t=push(mask,a);
     nxt.add(t);
     if(t&EVEN)nxt.add(t&EVEN);
     if(t&ODD)nxt.add(t&ODD);
   }
 }
 prefixes.push(nxt);
}
const prefixProfile=prefixes.map((s,d)=>{
 const sizes={};
 for(const mask of s)sizes[size(mask)]=(sizes[size(mask)]||0)+1;
 return {depth:d,distinct_reachable_current_physical_support_masks:s.size,by_candidate_count:sizes};
});
// Check h as an independent resource: the same physical belief of original
// slot pair {0,2} is not one-turn identifiable but is two-turn identifiable.
const p02=(1<<0)|(1<<4);
assert(MAP.every((_,a)=>bit(MAP[a][0])===bit(MAP[a][4])));
assert(MAP.some((_,a)=>MAP.some((_,b)=>bit(MAP[b][MAP[a][0]])!==bit(MAP[b][MAP[a][4]]))));
const fIndex=ACTIONS.indexOf('F');
assert(fIndex>=0&&bit(MAP[fIndex][0])!==bit(MAP[fIndex][2]));
// In a deliberately extended *uncertain sensor polarity* model, two joint
// distributions over (physical s, latent calibration c) induce the SAME
// physical marginal but different F-observation informativeness.
// Joint A: calibration c=0 always; joint B: calibration is correlated with s
// to exactly cancel the F output (y = O(F(s)) XOR c = 0 always).
const hypothesisStates=[0,2],sourceProb=[0.5,0.5];
const yBits=hypothesisStates.map(s=>bit(MAP[fIndex][s]));
const jointA=hypothesisStates.map((s,i)=>({s,c:0,p:sourceProb[i]}));
const jointB=hypothesisStates.map((s,i)=>({s,c:yBits[i],p:sourceProb[i]}));
const aggregate=(joints)=>{
 const marg=new Map(),outcome=[0,0],conditional=[[],[]];
 for(const j of joints){
  marg.set(j.s,(marg.get(j.s)||0)+j.p);
  const y=bit(MAP[fIndex][j.s])^j.c;
  outcome[y]+=j.p;conditional[y].push(j.s);
 }
 return {physical_state_marginal:Object.fromEntries(marg),
         bit_outcome_probabilities:outcome,
         physical_slots_identified_by_one_read:conditional.filter(x=>x.length===1).length};
};
const aa=aggregate(jointA),bb=aggregate(jointB);
assert.deepEqual(aa.physical_state_marginal,bb.physical_state_marginal);
assert.deepEqual(aa.bit_outcome_probabilities,[.5,.5]);
assert.deepEqual(bb.bit_outcome_probabilities,[1,0]);
const historicalLabelNeed={same_marginal_physical_belief_cannot_report_historical_origin_in_general:true,
  same_belief_different_observation_models_reject_ordinary_state_only_belief:true,
  extended_information_state_must_include:'joint belief on latent physical configuration AND uncertain calibration/model parameter; known action history/source-label inverse if original-source naming is terminal goal'};
const result={
 marker:'CUBE_REV_022_P2_COST_DEPENDENT_OPTIMAL_POLICY_AND_BELIEF_MODEL_ATTACK_PASS',
 ontology:'fixed ideal tagged-edge physical model vs extended uncertain-sensor mathematical counterexample; no empirical human perception measured',
 p8_original_uniform_physical_cost_frontier_rederived:true,
 policies:policies.map(({all_source_witnesses,...z})=>z),
 objective_distinction:'all scalar results have worst turn<=7; hard query cap=4 differs from uncapped, P8 price transition λ=3',
 selected_policy_reconstruction_caveat:'Chosen tie-broken policy DAG counts are exact for those concrete policies, NOT a proof of globally minimum reachable control memory over all optimal policies',
 all_action_three_move_reachability_prefix:prefixProfile,
 incomplete_reachability_notice:'three-move all-action prefix only; complete original 7-turn reachable belief arena NOT enumerated',
 fixed_same_belief_different_remaining_budget:{initial_slots:[0,2],one_turn_read_separation_possible:false,two_turn_read_separation_possible:true},
 joint_sensor_channel_counterexample:{action:'F',original_physical_edge_states:hypothesisStates,
  fixed_physical_state_marginal:aa.physical_state_marginal,
  joint_prior_A_known_polarity_zero:jointA,joint_prior_B_latent_correlated_polarity:jointB,
  model_A:aa,model_B:bb,conclusion:'Marginal posterior on physical state is not generally sufficient once observation law contains unmodeled uncertain latent parameters'},
 historical_origin_and_model_belief_limit:historicalLabelNeed,
 revised_information_state_proposal:{
   mathematical_minimality_NOT_established:true,
   posterior_over_augmented_latents:'P(physical state, camera/sensor calibration, notation reference frame, uncertain transition law | observed history)',
   task_context:'terminal goal, loss, prior, phase-specific admissible actions, remaining actual time and sensor budget, query and move cost regime',
   path_provenance:'known cumulative permutation or source-label map for retrospective source naming',
   human_warning:'psychological belief is NOT identified from final cube or FMC reconstruction; cognitive effort, memory, uncertainty and unrecorded alternatives remain unobserved',
   classical_alternative:'predictive state of future action-conditioned observation probabilities (PSR) instead of requiring human probability-vector representation',
   required_test:'two histories with same proposed statistic must have identical conditional distributions for every admitted future controlled experiment AND compatible goal/loss'
 },
 source_precedents:{g3:'P23,P26,P27,P29',literature:[
 'https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf',
 'https://www.jmlr.org/beta/papers/v23/20-1152.html',
 'https://ojs.aaai.org/index.php/AAAI/article/view/8264'
 ]},
 no_claims:'No globally minimum full 12-source FSC memory established, no human cost measurement, no naturally occurring hidden camera calibration, no new participant/video work'
};
console.log(JSON.stringify(result,null,2));
