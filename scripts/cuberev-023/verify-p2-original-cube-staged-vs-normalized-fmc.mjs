/**
 * CUBE-REV 0.23 P2. Independent source-relative boundary rewrite accounting.
 * No P1 search engine imported. Input: four exact all-18 P1 sealed witnesses.
 * Replays original 54-sticker Rubik cube and audits every adjacent-face reduction.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {solvedStickerCube, applyMoveToken, toCubieState, solvedUpToRotation} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const source=JSON.parse(fs.readFileSync('data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json','utf8'));
const input=JSON.parse(fs.readFileSync('data/cuberev-023/p2_P1_all18_four_word_authority_fixture.json','utf8'));
assert.equal(input.schema,'cuberev-023-p2-independent-P1-all18-witness-source-replay-v1');
assert.equal(input.original_scramble,source.normal_scramble);
const tokenize=s=>s.trim().split(/\s+/).filter(Boolean);
const allMoveOK=w=>assert(w.every(x=>ACTIONS.includes(x)), 'All written moves must be actual legal 18 HTM tokens');
const cubeAfter=w=>{const x=solvedStickerCube();for(const t of w)applyMoveToken(x,t);return x;};
const signature=st=>{const s=toCubieState(st);return [...s.cp,...s.co,...s.ep,...s.eo].join(',');};
const hash=w=>crypto.createHash('sha256').update(signature(cubeAfter(w))).digest('hex');
const solved=tokenize(source.normal_scramble);allMoveOK(solved);
const power=x=>x.endsWith('2')?2:x.endsWith("'")?3:1;
const token=(face,p)=>face+(p===1?'':p===2?'2':p===3?"'":'');
const reduceTagged=parts=>{
  const stack=[],changes=[];
  for(const part of parts)for(let i=0;i<part.tokens.length;i++){
    const x=part.tokens[i];const t={move:x,source:part.kind,source_pos:i+1,origin:[{kind:part.kind,index:i+1,word:x}]};
    const prev=stack.at(-1);
    if(!prev||prev.move[0]!==x[0]){stack.push(t);continue;}
    stack.pop();const c=(power(prev.move)+power(x))%4;
    const next=c===0?null:token(x[0],c);
    const before=[prev.move,x];
    const prevTag=new Set(prev.origin.map(z=>z.kind)),nextTag=new Set(t.origin.map(z=>z.kind));
    changes.push({
      no:changes.length+1,before,
      after:next,
      length_saved:next===null?2:1,
      left_provenance:[...prevTag],right_provenance:[...nextTag],
      contact:prev.origin.some(z=>z.kind!==t.source)?'CROSS_OR_COMPOSITE':'INTRA_SINGLE_SOURCE',
      original_source_position_left:prev.origin,
      original_source_position_right:t.origin
    });
    if(next)stack.push({...t,move:next,origin:[...prev.origin,...t.origin]});
  }
  return {tokens:stack.map(x=>x.move),changes,saved:changes.reduce((n,c)=>n+c.length_saved,0)};
};
const stages=['AUTHOR','INTERVENTION','SUFFIX'];
const results=[];
for(const item of input.rows){
 const authored=source.eo_dr_pairs.find(x=>x.id===item.source_id);
 assert(authored&&authored.declared_mode==='CONTIGUOUS_NORMAL_SIDE_PREFIX');
 const p=tokenize(authored.eo_prefix+' '+authored.dr_extension);
 const intervention=tokenize(item.synthetic_original_face_word),suffix=tokenize(item.full_18_exact_shortest_suffix);
 const originalScramble=tokenize(source.normal_scramble);
 [p,intervention,suffix].forEach(allMoveOK);
 assert.equal(intervention.length,2);
 assert.equal(suffix.length,item.post_intervention_all18_exact_length);
 const components=[
  {kind:'AUTHOR',tokens:p},
  {kind:'INTERVENTION',tokens:intervention},
  {kind:'SUFFIX',tokens:suffix}
 ];
 const whole=[...p,...intervention,...suffix];
 assert.equal(whole.length,item.raw_actions);
 assert(solvedUpToRotation(cubeAfter([...originalScramble,...whole])));
 const combined=reduceTagged(components);
 assert.equal(combined.tokens.length,item.adjacent_reduced_actions);
 assert(solvedUpToRotation(cubeAfter([...originalScramble,...combined.tokens])));
 assert.equal(hash(whole),hash(combined.tokens),'Reducing a whole real source solution cannot change its full-cube permutation/orientations');
 const independentPerStage=components.map(x=>reduceTagged([x]));
 const preConcat=independentPerStage.flatMap(z=>z.tokens);
 const across=reduceTagged(independentPerStage.map((z,i)=>({kind:stages[i],tokens:z.tokens})));
 assert.deepEqual(across.tokens,combined.tokens,'Independent per-stage normalization + boundary-only reduction must reach same final word');
 const savedWithin=independentPerStage.reduce((n,x)=>n+x.saved,0),savedAtBoundary=across.saved;
 assert.equal(savedWithin+savedAtBoundary,combined.saved);
 const stageBoundarySource=reduceTagged(components.slice(0,2));
 assert.equal(stageBoundarySource.tokens.length,p.length+2);
 const allChangeDetails=combined.changes.map(x=>({...x,stages_at_transition:x.left_provenance.concat(x.right_provenance)}));
 const sourceUntouched=combined.tokens.slice(0,p.length).every((t,i)=>t===p[i]);
 assert.equal(sourceUntouched,item.authored_prefix_remains_literal);
 const exactUnrestrictedDistanceFromLiteralAuthoredSource=item.source_id==='miao_main'?9:12;
 const exactSourcePrefixConditionedNormalizedGlobalWithinPrefix=p.length+exactUnrestrictedDistanceFromLiteralAuthoredSource;
 // Frozen P8-R4/P8-R5 whole-cubie exact d18 from the original authored prefix;
 // any full word retaining the entire literal prefix must require >= d18 further HTM moves.
 assert(combined.tokens.length>=exactSourcePrefixConditionedNormalizedGlobalWithinPrefix);
 const attainsLiteralPrefixConditionedOptimum=combined.tokens.length===exactSourcePrefixConditionedNormalizedGlobalWithinPrefix;
 const gapAboveLiteralPrefixConditionedOptimum=combined.tokens.length-exactSourcePrefixConditionedNormalizedGlobalWithinPrefix;
 const reducedWholeIsSubmitted=combined.tokens.join(' ')===source.submitted_final_19;
 const row={
  source_id:item.source_id,source_grade:'HUMAN_RETROSPECTIVE_PREFIX_ONLY',
  synthetic_FB_axis_word:item.synthetic_FBDR_actions,
  original_synthetic_face_word:item.synthetic_original_face_word,
  original_source_prefix_HTM:p.length,synthetic_action_HTM:2,certified_exact_all18_suffix_HTM:suffix.length,
  exact_literal_source_prefix_preserving_optimum_all18_HTM:exactSourcePrefixConditionedNormalizedGlobalWithinPrefix,
  this_reduced_witness_attains_literal_prefix_conditioned_optimum:attainsLiteralPrefixConditionedOptimum,
  this_reduced_witness_excess_over_literal_prefix_optimum_HTM:gapAboveLiteralPrefixConditionedOptimum,
  raw_stage_cost_HTM:whole.length,
  independent_stage_savings_HTM:savedWithin,
  cross_stage_boundary_savings_HTM:savedAtBoundary,
  normalized_submitted_form_witness_HTM:combined.tokens.length,
  total_adjacent_rewrite_savings_HTM:combined.saved,
  rewrites:allChangeDetails,
  fully_unchanged_human_source_prefix:sourceUntouched,
  is_exactly_human_published_final_word:reducedWholeIsSubmitted,
  original_complete_word:whole.join(' '),
  reduced_complete_word:combined.tokens.join(' '),
  fully_physically_original_scramble_solved:true,
  same_full_cubie_state_after_rewrites:true,
  distinct_source_grades:{author_prefix:'HUMAN_AUTHORED_RETROSPECTIVE',intervention:'SYNTHETIC_MODEL_ACTION',suffix:'EXACT_COMPUTER_CERTIFIED_ALL_18_COMPLETION'}
 };
 results.push(row);
}
assert.deepEqual(results.map(x=>x.raw_stage_cost_HTM),[23,23,23,23]);
assert.deepEqual(results.map(x=>x.normalized_submitted_form_witness_HTM),[19,23,21,23]);
assert.deepEqual(results.map(x=>x.cross_stage_boundary_savings_HTM),[4,0,2,0]);
assert.deepEqual(results.map(x=>x.exact_literal_source_prefix_preserving_optimum_all18_HTM),[19,23,19,23]);
assert.deepEqual(results.map(x=>x.this_reduced_witness_attains_literal_prefix_conditioned_optimum),[true,true,false,true]);
assert.deepEqual(results.map(x=>x.this_reduced_witness_excess_over_literal_prefix_optimum_HTM),[0,0,2,0]);
assert(results.every(x=>x.independent_stage_savings_HTM===0));
assert(results.every(x=>x.fully_unchanged_human_source_prefix));
const paired=['D B2',"D' F2"].map(word=>{
 const two=results.filter(x=>x.synthetic_FB_axis_word===word);
 assert.equal(two.length,2);
 return {
  intervention:word,
  raw_stage_gap_alt_minus_main:two[1].raw_stage_cost_HTM-two[0].raw_stage_cost_HTM,
  canonical_final_witness_gap_alt_minus_main:two[1].normalized_submitted_form_witness_HTM-two[0].normalized_submitted_form_witness_HTM,
  boundary_saving_advantage_main:two[0].cross_stage_boundary_savings_HTM-two[1].cross_stage_boundary_savings_HTM,
  source_prefix_both_preserved:two.every(x=>x.fully_unchanged_human_source_prefix),
  both_physically_solved:two.every(x=>x.fully_physically_original_scramble_solved),
  claim_grade:'CONSTRUCTIVE_COMPLETE_SOLUTION_WITNESSES_ONLY_NOT_GLOBAL_OPTIMALITY'
 };
});
assert.deepEqual(paired.map(x=>x.canonical_final_witness_gap_alt_minus_main),[4,2]);
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P2_ORIGINAL_CUBE_BOUNDARY_REWRITE_AND_STAGE_COST_SPLIT',
 proof_condition:'Independent replay of original authored FMC words, two synthetic legal physical turns, four certified all18 suffixes, 54 sticker normalizations',
 source_original_scramble:source.normal_scramble,
 all_four_physical_replays_pass:true,
 all_source_literal_prefixes_preserved:true,
 all_four_individual_components_have_zero_internal_adjacent_savings:true,
 observed_rewrite_intervention_suffix_boundary_only:true,
 final_normalized_lengths_are_constructions_NOT_exact_global_minima:true,
 authors_computed_or_chosen_synthetic_actions_NOT_observed:true,
 original_human_cognition_NOT_identified:true,
 full_18_post_intervention_geodesic_minima_imported_from_P1_PROVEN:true,
 source_literal_prefix_conditioned_exact_final_word_optima_from_frozen_R4_R5:[19,23],
 four_witness_source_prefix_exact_optimum_attainment:[true,true,false,true],
 second_main_21_HTM_is_provably_not_optimal_even_under_its_original_ten_turn_prefix:true,
 paired_contrasts:paired,
 complete_physical_four_way_rewrite_evidence:results
},null,2));
