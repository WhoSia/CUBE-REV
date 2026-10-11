/** CUBE-REV 0.23 P3-R2B public AGGREGATE-ONLY transport/audit gate.
 * Does NOT fetch or expose the authorized private 451-reconstruction archive.
 * Verifies internally auditable aggregate arithmetic; independent recomputation
 * of the underlying 451 source trajectories requires local private ZIP custody.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
const p=JSON.parse(fs.readFileSync('data/cuberev-023/p3_r2b_private451_new_corner_state_conditional_support_aggregate.json','utf8'));
assert.equal(p.schema,'cuberev-023-p3-r2b-private451-exploratory-aggregate-v1');
assert.equal(p.private_archive_sha256,'fb88827cce327d0021a0741e47dfa09670651083b8baaaa46cccc9051d73568e');
assert.deepEqual([p.original_records,p.identical_reconstructed_content_duplicate_eliminated,p.remaining_distinct_reconstructed_solve_contents,p.retrospective_reconstruction_next_actions],[452,1,451,25272]);
assert.equal(Object.values(p.types).reduce((a,b)=>a+b,0),25272);
assert.equal(p.explicit_method_family_tagged_record_count,20);
const rows=p.all_actions,only=p.face_turn_only;
assert.equal(rows.length,5);assert.equal(only.length,5);
assert.deepEqual(rows.map(x=>x.keys_with_both_same_full_and_different_full_contrasts),[181,120,43,9,0]);
assert.deepEqual(only.map(x=>x.keys_with_both_same_full_and_different_full_contrasts),[164,73,15,1,0]);
assert.deepEqual(rows.map(x=>[x.same_exact_full_state_cross_source_pairs,x.different_exact_full_state_cross_source_pairs]),[[7851,86453],[733,5611],[258,1951],[105,352],[59,43]]);
assert.deepEqual(only.map(x=>[x.same_exact_full_state_cross_source_pairs,x.different_exact_full_state_cross_source_pairs]),[[6078,27988],[589,1817],[202,597],[70,182],[45,29]]);
assert(rows.every((r,i)=>r.cross_source_qualifying_observation_keys>=r.keys_with_both_same_full_and_different_full_contrasts));
assert(rows.every((r,i)=>r.different_next_action_when_same_full<=r.same_exact_full_state_cross_source_pairs && r.different_next_action_when_different_full<=r.different_exact_full_state_cross_source_pairs));
assert(only.every((r,i)=>r.different_next_action_when_same_full<=r.same_exact_full_state_cross_source_pairs && r.different_next_action_when_different_full<=r.different_exact_full_state_cross_source_pairs));
assert(rows.at(-1).descriptive_common_key_balanced_delta_different_minus_same===null);
assert(p.independent_heldout===false&&p.causal_brain_barrier_inference===false);
assert(p.transport_of_P3_R1A_62_state_uniform_policy_to_real_people===false);
const theoretical={cohort:62,adaptive:[1,12,42,58,62,62,62],fixed:[1,12,38,50,62,62,62],query_is:'IDEAL_NINE_FACELETS_ONE_FACE',task:'3x3 exact FULL cube'};
assert(theoretical.adaptive[2]>theoretical.fixed[2]&&theoretical.adaptive[3]>theoretical.fixed[3]);
assert(p.corner_projection.includes('NOT the old FC3')&&p.stage_proxy.includes('not mental stage'));
const observations={theoretical_62_real_3x3_full_sticker_face_oracle:theoretical,
 human_archival_451_ideal_CP_CO_corner_state_observation:'COMPLETE_8_CORNERS_ABSTRACT_CUBIE_STATE_NOT_HUMAN_RECORDED_9_STICKER_VISION',
 physical_operator_identity_between_theory_and_human_data:false,
 empirical_exact_human_eye_scan_count_observed:false,
 historical_human_3x3_cross_source_full_vs_corner_action_support_layers:rows,
 exclusive_face_turn_sensitivity_supported_keys:only.map(x=>x.keys_with_both_same_full_and_different_full_contrasts),
 extreme_matched_history_support_after_3_moves:0,
 matched_effect_estimate_at_strictest_level:'UNDEFINED_SUPPORT_FAILURE',
 source_pairs_are_not_independent_participants:true,
 psychometric_reaction_time_neural_evidence_present:false,
 private_original_reconstruction_data_in_public_artifact:false,
 human_real_Mstar_frontier_identified:false,
 source_archive_rerun_requires_access_to_PRIVATE_sha_verified_zip:true};
console.log(JSON.stringify({marker:'CUBE_REV_023_P3_R2B_SOURCE_GRADED_HUMAN_TO_PHYSICAL_FRONTIER_TRANSPORT_GATE_PASS',...observations},null,2));
