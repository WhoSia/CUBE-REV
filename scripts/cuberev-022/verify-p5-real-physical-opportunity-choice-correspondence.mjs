/**
 * CUBE-REV 0.22 P5 — actual Rubik 18-HTM counterfactual feasible first moves,
 * Bellman root-action conditional cost and limited-consideration identified sets.
 *
 * IMPORTANT: PHYSICAL ideal tagged-edge oracle ≠ actual FMC human policy.
 * Menus are hypothetical mathematical consideration sets, NOT reconstructed
 * from WCA or authored FMC retrospective data.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const MAP=urMoveAutomaton(),EVEN=0x555555,FULL=(1<<24)-1,ODD=FULL^EVEN;
assert.equal(MAP.length,18);
assert.equal(ACTIONS.length,18);
for(const a of MAP)assert.deepEqual([...a].sort((x,y)=>x-y),Array.from({length:24},(_,i)=>i));
const size=m=>{let n=0;for(;m;m&=m-1)n++;return n;};
const trans=new Map();
const move=(mask,a)=>{
 const key=mask+':'+a;
 if(trans.has(key))return trans.get(key);
 let out=0;
 for(let m=mask;m;){
  const bit=m&-m;const idx=31-Math.clz32(bit);
  out|=(1<<MAP[a][idx]);m-=bit;
 }
 trans.set(key,out);return out;
};
function exactCourt({h,k,lambda}){
 const memo=new Map();
 const compare=(x,y)=>{
   const sx=x.T+lambda*x.Q,sy=y.T+lambda*y.Q;
   if(sx!==sy)return sx-sy;
   if(x.Q!==y.Q)return x.Q-y.Q;
   return x.T-y.T;
 };
 const choose=(offers)=>{
   if(offers.length===0)return null;
   return offers.reduce((best,now)=>compare(now,best)<0?now:best);
 };
 function offers(mask,turns,reads,root=false){
  if(size(mask)===1)return [];
  if(turns<1||reads<0||size(mask)>2**Math.min(turns,reads))return [];
  const m=size(mask),out=[];
  for(let a=0;a<18;a++){
   const next=move(mask,a),lo=next&EVEN,hi=next&ODD;
   // The only observation option requiring a paid read is one with a
   // real split. Non-splitting reads can be omitted at equal/lower cost.
   if(reads>0&&lo&&hi){
    const l=solve(lo,turns-1,reads-1),r=solve(hi,turns-1,reads-1);
    if(l&&r)out.push({a,action:ACTIONS[a],mode:'READ',
      T:m+l.T+r.T,Q:m+l.Q+r.Q});
   }
   if(turns>1){
    const s=solve(next,turns-1,reads);
    if(s)out.push({a,action:ACTIONS[a],mode:'SILENT',
      T:m+s.T,Q:s.Q});
   }
  }
  return out;
 }
 function solve(mask,turns,reads){
  if(size(mask)===1)return {T:0,Q:0};
  if(turns===0||reads===0||size(mask)>2**Math.min(turns,reads))return null;
  const key=mask+':'+turns+':'+reads;
  if(memo.has(key))return memo.get(key);
  const out=choose(offers(mask,turns,reads));
  memo.set(key,out);return out;
 }
 const optimal=solve(EVEN,h,k);
 const modes=offers(EVEN,h,k).map(o=>({
   ...o,total_weighted:Tscore(o),expected_cost:Tscore(o)/12,
   expected_turns:o.T/12,expected_reads:o.Q/12
 }));
 function Tscore(z){return z.T+lambda*z.Q;}
 const byAction=ACTIONS.map((action,a)=>{
   const cs=modes.filter(z=>z.a===a);
   const best=choose(cs);
   return {action,feasible:cs.length>0,
     modes:cs.map(z=>({mode:z.mode,T:z.T,Q:z.Q,weighted:z.total_weighted})),
     ...(best?{best_mode:best.mode,T:best.T,Q:best.Q,weighted:Tscore(best)}:{})};
 });
 const feasible=byAction.filter(x=>x.feasible);
 const minimum=optimal?Tscore(optimal):null;
 const rootOpt=feasible.filter(x=>x.weighted===minimum);
 const better=(target)=>feasible.filter(x=>x.weighted<target.weighted);
 const noBetter=(target)=>feasible.filter(x=>x.action!==target.action&&x.weighted>=target.weighted);
 const observableMenuCourt=target=>{
   const excluded=better(target);
   const optional=noBetter(target);
   const competitor=optional.find(x=>x.action!==target.action);
   assert(competitor,'At least one weakly worse root alternative needed for choice nonidentification');
   const num=2**optional.length;
   // All considered subsets consistent with choosing target under
   // cost-minimizing weak preference and arbitrary tie-breaking.
   // All strictly better actions are ruled out, but non-considered is
   // an assumed latent decision set, not evidence in real humans.
   return {chosen_root_action:target.action,
      physical_costed_criterion:'Minimum expected physical turn + lambda*read cost with a fixed frozen ideal observation oracle',
      strictly_better_physically_feasible_actions_that_must_be_EXCLUDED_from_menu:excluded.map(x=>x.action),
      no_better_other_physically_feasible_actions:optional.map(x=>x.action),
      exactly_consistent_consideration_menus: num,
      tight_considered_move_count_bounds:[1,1+optional.length],
      witness_minimal_menu:[target.action],
      witness_larger_menu:[target.action,competitor.action],
      same_possible_chosen_physical_action_under_distinct_menus:true,
      conditional_assumptions:'Choose a cost-minimal action in latent considered menu; agent knows exact future oracle-optimized continuation cost for each menu item; tie-breaking unrestricted.',
      NOT_evidence_of_actual_human_restricted_attention:true};
 };
 const optimalConsideration=optimal?observableMenuCourt(rootOpt[0]):null;
 const closestSubopt=feasible.filter(x=>x.weighted>minimum)
  .sort((a,b)=>a.weighted-b.weighted||a.action.localeCompare(b.action))[0]??null;
 const suboptimalConsideration=closestSubopt?observableMenuCourt(closestSubopt):null;
 // A hypothetical unobserved considered menu produces the same optimal first
 // action despite containing a different set; no hidden psychology imputed.
 if(optimal)assert(rootOpt.length>0);
 const firstStageRegret=closestSubopt?(closestSubopt.weighted-minimum)/12:null;
 return {
  task:{max_turns:h,max_reads:k,lambda,source_count:12,source_uniform:true},
  feasible_complete_identification:!!optimal,
  ...(optimal?{
    root_physical_optimum:{aggregate_T:optimal.T,aggregate_Q:optimal.Q,
      total_weighted:minimum,mean_cost:minimum/12},
    feasible_root_face_turns:feasible.length,
    infeasible_root_face_turns:byAction.filter(x=>!x.feasible).map(x=>x.action),
    full_physical_root_optimal_action_names:rootOpt.map(x=>x.action),
    modes_feasible_for_full_identification:modes.length,
    distinct_root_cost_tiers:new Set(feasible.map(x=>x.weighted)).size,
    root_cost_by_legal_face_turn:byAction,
    sharp_root_choice_correspondence_under_HYPOTHETICAL_consideration:optimalConsideration,
    closest_feasible_strictly_suboptimal_first_action_correspondence:suboptimalConsideration,
    nearest_suboptimal_regret_in_EXPECTED_PHYSICAL_COST_not_human_cost:firstStageRegret
  }:{}),
  exact_Bellman_belief_resource_states:memo.size,
  no_claim_about_population_human_ability:true};
}

const cases=[
  {h:7,k:7,lambda:0},
  {h:7,k:7,lambda:4},
  {h:7,k:4,lambda:0},
  {h:7,k:4,lambda:4},
  {h:6,k:4,lambda:0},
  {h:7,k:3,lambda:0}
];
const court=cases.map(exactCourt);
assert.deepEqual([court[0].root_physical_optimum.aggregate_T,
  court[0].root_physical_optimum.aggregate_Q],[71,45]);
assert.deepEqual([court[1].root_physical_optimum.aggregate_T,
  court[1].root_physical_optimum.aggregate_Q],[74,44]);
assert.deepEqual([court[2].root_physical_optimum.aggregate_T,
  court[2].root_physical_optimum.aggregate_Q],[74,44]);
assert(!court[4].feasible_complete_identification);
assert(!court[5].feasible_complete_identification);
const pi=court[2].root_physical_optimum;
assert.equal(pi.aggregate_T,74);
assert.equal(pi.aggregate_Q,44);
assert(court[2].sharp_root_choice_correspondence_under_HYPOTHETICAL_consideration.exactly_consistent_consideration_menus>=2);
const src=JSON.parse(fs.readFileSync('data/cuberev-022/p3_fmc_matched_scramble_author_evidence.json','utf8'));
assert(src.schema==='cuberev-022-p3-fmc-matched-scramble-retrospective-v1');
assert(src.controls.unreported_candidate_counts_are_unknown_not_zero);
assert(src.competitors.length===2);
assert(src.competitors.every(x=>x.attempts.length===3));
const A=src.competitors.find(x=>x.id==='2018RIAB01'),B=src.competitors.find(x=>x.id==='2014MIAO02');
assert(A&&B);
for(let i=0;i<3;i++){
 assert(A.attempts[i].official_scramble===B.attempts[i].official_scramble);
 assert(A.attempts[i].solution_htm===B.attempts[i].solution_htm);
}
const w=A.attempts[2].written_EO_candidates_about,
 e=A.attempts[2].checked_EO_candidates_about;
assert(w===70&&e===30);
const sharp=(W,E)=>({
 intersection_min:0,intersection_max:Math.min(W,E),
 written_not_evaluated_min:Math.max(0,W-E),
 written_not_evaluated_max:W,
 true_full_feasible_opportunity_denominator:'UNKNOWN',
 true_cognitive_evaluation_set:'NOT_OBSERVED_IN_FULL'});
const fmc={
 matched_author_ids:[A.id,B.id],
 matched_scrambles:3,attempts:6,independent_people:2,
 same_final_lengths:[19,19,23],
 Riabov_attempt3_authored_approximate_report:{written_about:w,checked_about:e},
 conditional_on_EXACT_w_e_not_source_warranted:sharp(w,e),
 hypothetical_margin_10_per_count_lower_written_unchecked:Math.max(0,(w-10)-(e+10)),
 same_final_move_word_is_not_unique_inverse_map_to_process:true,
 process_evidence_grade:'RETROSPECTIVE_SOURCE_TEXT_NOT_REALTIME_SEARCH_LOG',
 cause_from_endpoint:'NOT_IDENTIFIED',
 actual_human_opportunity_set:'NOT_IDENTIFIED',
 no_fake_converted_cube_edge_oracle_to_FMC_EO_search:true
};
const result={
 marker:'CUBE_REV_022_P5_REAL_PHYSICAL_FIRST_ACTION_OPPORTUNITY_AND_FMC_CHOICE_CORRESPONDENCE_PASS',
 proof_scope:'exact genuine HTM moves plus hypothetical cost-rational considered-menu identified set, distinct from actual FMC human cognitive evidence',
 original_physical_rubik_model:'single tagged UR edge, 12 known initial-zero-flip source slots, 18 genuine face HTM moves, optional intrinsic post-turn 1-bit query',
 rooted_resource_opportunity_frontiers:court,
 retrospective_matched_fmc_source_audit:fmc,
 theorem_choice_correspondence:'For finite opportunity menu A with action a observed under weak rationality on chosen cost c, feasible latent considered sets are exactly {a} union arbitrary subsets of {b in A excluding a: c(b)>=c(a)}. All strictly cheaper actions must be excluded. If tie-breaking unspecified, compatible menu count = 2^(#weakly-worse alternatives). This is a mathematical identification theorem conditional on rationality, not observed mental process.',
 theorem_restricted_model_transfer:'Rubik tagged-edge oracle and full-cube FMC EO/DR search have DIFFERENT states, information access, costs and objective; no numeric move regret or menu count is attributed to FMC solvers.',
 directions_evaluation:{
  preserve_exact_math_and_executable_reproduction:true,
  preserve_sparse_human_observations_and_source_grades:true,
  falsify_inapplicable_cognitive_transfer:true,
  do_not_invent_scalar_cognitive_gap:true,
  no_new_human_recruitment_video_or_VFMC:true,
  next_requirements:'Physical full-cube FMC candidate grammar and source-attested opportunity denominator are separate future conditions, not solved by a tagged-edge first-move menu.'
 }
};
console.log(JSON.stringify(result,null,2));
