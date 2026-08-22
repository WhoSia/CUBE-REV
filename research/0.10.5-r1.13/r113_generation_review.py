#!/usr/bin/env python3
import json,hashlib,os,pathlib,datetime
ROOT=pathlib.Path(os.environ.get('R113_REPO_ROOT','.')).resolve()
OUT=pathlib.Path(os.environ.get('R113_ROOT','/tmp/r113'));OUT.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads((ROOT/p).read_text())
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
F=load(pathlib.Path('research/0.10.5-r1.13/evidence-development/ROTATION_GAUGE_TRANSPORT_FIXTURE.json'))
G=load(pathlib.Path('research/0.10.5-r1.13/evidence-development/ROUX_G3_GEOMETRY_AUDIT.json'))
N=load(pathlib.Path('research/0.10.5-r1.13/evidence-development/ROUX_G3_NULL_AUDIT.json'))
D=load(pathlib.Path('research/0.10.5-r1.13/evidence-rotation-destroy/ROTATION_MECHANISM_DESTROY_AUDIT.json'))
L=load(pathlib.Path('research/0.10.5-r1.13/evidence-rotation-localization/ROTATION_ROUTE_LOCALIZATION_AUDIT.json'))
B=load(pathlib.Path('research/0.10.5-r1.13/evidence-break-restore/RESIDUAL_BREAK_RESTORE_AUDIT.json'))
C=load(pathlib.Path('research/0.10.5-r1.13/evidence-move-cocycle/MOVE_COCYCLE_GAUGE_DIAGNOSTIC.json'))
stat_checks={k:v for k,v in N['checks'].items() if k!='geometry_pass'}
stat_stack_without_geometry=all(stat_checks.values())
component_pass={
 'rotation_algebra':F['status']=='PASS_ROTATION_GAUGE_ALGEBRA' and all(F['checks'].values()),
 'prefix_identification':G['rates']['prefix_unique_rate']>=.95,
 'overall_sb_completion':G['rates']['sb_completion_rate']>=.90,
 'no_rotation_sb_completion':G['rates']['no_rotation_sb_completion_rate']>=.90,
 'rotation_present_gate':G['rates']['rotation_present_sb_completion_rate']>=.75,
 'null_stack_conditioned_on_admitted_geometry':stat_stack_without_geometry,
 'finite_1pct_resolution':N['finite_sample_primary_resolution']['primary_1pct_resolvable'],
 'move_cocycle_candidate':C['rates']['cocycle_completion']>=.90
}
review={
 'schema_version':'CR0105R113-GENERATION-REVIEW-1',
 'stage':'CUBE-REV 0.10.5-R1.13 — Route-global Reconstruction Gauge, Rotation-covariant Prefix Frame & Rebuilt Roux Completion Null',
 'generation_under_review':'ROUX-MEASUREMENT-G3',
 'status':'PASS_GENERATION_REVIEW_G3_REMANDED_COMPONENTS_VALIDATED_G4_CANONICAL_ROUX_CANDIDATE_IDENTIFIED',
 'primary_disposition':{
   'g3':'REMANDED_NOT_RELEASED',
   'reason':'Frozen rotation-present geometry gate failed at 3/6=0.50 versus required 0.75. Posthoc diagnostics cannot remove or relax that gate.',
   'geometry_status':G['status'],'null_status':N['status'],'future_roux_scoring_authority':False,
   'posthoc_diagnostics_can_repair_g3':False
 },
 'validated_or_surviving_components':{
   'rotation_transport_algebra':component_pass['rotation_algebra'],
   'prefix_unique_rate':G['rates']['prefix_unique_rate'],
   'overall_sb_completion_rate':G['rates']['sb_completion_rate'],
   'no_rotation_sb_completion_rate':G['rates']['no_rotation_sb_completion_rate'],
   'cmll_consistency_rate':G['rates']['cmll_consistency_rate'],
   'lse_consistency_rate':G['rates']['lse_consistency_rate'],
   'admitted_attempts':G['counts']['g3_admitted'],
   'null_stack_pass_if_geometry_gate_externalized':stat_stack_without_geometry,
   'loo_watch_rate':N['loo_pseudofresh']['watch_rate'],
   'nested_watch_rate':N['nested_no_test_fold_leak']['watch_rate'],
   'crossfit_loo_pearson':N['transport']['pearson_crossfit_vs_loo'],
   'crossfit_loo_p99_abs_diff':N['transport']['abs_difference']['p99'],
   'primary_1pct_resolution':component_pass['finite_1pct_resolution']
 },
 'falsified_or_remanded_hypotheses':{
   'rotation_presence_as_residual_mechanism':{
      'frozen_gate_pass':component_pass['rotation_present_gate'],
      'rotation_present_completion_rate':G['rates']['rotation_present_sb_completion_rate'],
      'fixed_success_rotation':D['rates']['rotation_fixed_success'],
      'forward_success_rotation':D['rates']['rotation_forward_success'],
      'inverse_success_rotation':D['rates']['rotation_inverse_success'],
      'fixed_forward_outcome_agreement_rotation':D['rates']['rotation_fixed_forward_same']
   },
   'pure_rotation_algebra_failure':False,
   'reason_pure_rotation_not_failure':f"{L['counts']['rotation_events_block_status_invariant']}/{L['counts']['rotation_events']} explicit rotation events preserved tracked block status under transported gauge.",
   'wide_slice_as_hidden_coordinate_gauge':{
      'candidate_pass':component_pass['move_cocycle_candidate'],
      'move_cocycle_completion_rate':C['rates']['cocycle_completion'],
      'g3_successes_lost':C['counts']['cocycle_loses_g3_successes'],
      'g3_failures_rescued':C['counts']['cocycle_rescues_g3_failures']
   }
 },
 'residual_court':{
   'residual_n':B['counts']['residual'],
   'residual_with_rotation_n':B['counts']['residual_rotation'],
   'residual_first_block_break_n':B['counts']['residual_first_block_break'],
   'first_block_restored_after_break_n':B['counts']['residual_first_block_restored_after_break'],
   'both_complete_any_later_n':B['counts']['residual_both_complete_any_later'],
   'both_complete_before_cmll_n':B['counts']['residual_both_complete_before_cmll'],
   'both_complete_before_lse_n':B['counts']['residual_both_complete_before_lse'],
   'interpretation':'Residual routes are not explained by explicit rotation transport alone. Many violate the tracked first-block persistence assumption, and a general center-cocycle treatment of wide/slice moves is strongly rejected.'
 },
 'inheritance_closure':{
   'RETAIN':[
     'FB-prefix-only unique gauge initialization',
     'explicit whole-cube rotation transport table derived by asymmetric-state invariance',
     'state-certified in-span two-block completion operator',
     'Roux-only LOO/crossfit/nested attempt-level familywise null architecture',
     'alpha=0.01 and total admitted N>=100 finite-resolution gate'
   ],
   'DOWNGRADE':[
     'rotation presence as an explanatory residual mechanism; R1.13 targeted gate failed',
     'fixed versus forward transport comparison; both score 120/130 but select disjoint outcomes on all six rotation routes'
   ],
   'RETIRE':[
     'inverse rotation transport',
     'general move-level center cocycle for wide/slice moves',
     'R1.13 development feature/null bank for future confirmatory scoring'
   ],
   'MUTATE':[
     'Roux ontology -> prospectively separate canonical first-block-preserving SB from block-disruptive/noncanonical-or-reconstruction-inconsistent residual routes',
     'authority court -> require fresh routes after the next ontology freeze rather than reclassifying R1.13 routes in-place'
   ],
   'FORK':[
     'canonical first-block-preserving Roux SB',
     'first-block-disruptive residual reconstructions',
     'pseudo-FB/FBDR and syntactically invalid reconstruction records'
   ],
   'RECOMBINE':[
     'G3 explicit-rotation gauge algebra + canonical Roux block-preservation ontology + rebuilt null stack'
   ],
   'UNRESOLVED':[
     'whether first-block-disruptive residuals are legitimate advanced Roux variants, reconstruction notation inconsistencies, or route errors',
     'whether a distinct subgoal ontology is needed for block-disruptive variants',
     'whole-project CUBE-REV generation numbering'
   ]
 },
 'next_generation':{
   'label':'ROUX-MEASUREMENT-G4',
   'version_candidate':'CUBE-REV 0.10.5-R1.14',
   'title_candidate':'Canonical Roux Block-preservation Ontology, Residual Reconstruction-consistency Fork & Fresh-route Gauge Authority Court',
   'must_begin_with_new_NAPKIN':True,
   'r113_routes_may_be_confirmatory':False,
   'fresh_routes_required_for_authority':True,
   'future_scoring_authority_at_transition':False
 },
 'authority':{
   'roux_future_scoring_authority':False,'main_write':False,'public_runner_write':False,'collector_write':False,
   'human_recruitment':False,'human_observations':0,
   'cognitive_recovery_error_prevalence_claim':'PROHIBITED','causal_intentionality_claim':'PROHIBITED','full_wca_prevalence_claim':'PROHIBITED'
 },
 'source_semantic_sha256':{
   'rotation_fixture':F['semantic_sha256'],'g3_geometry':G['semantic_sha256'],'g3_null':N['semantic_sha256'],
   'rotation_destroy':D['semantic_sha256'],'rotation_localization':L['semantic_sha256'],'break_restore':B['semantic_sha256'],'move_cocycle':C['semantic_sha256']
 }
}
review['semantic_sha256']=sha(review)
(OUT/'GENERATION_REVIEW_CLOSURE.json').write_text(json.dumps(review,indent=2)+'\n')
print(json.dumps({'status':review['status'],'primary':review['primary_disposition'],'components':review['validated_or_surviving_components'],'next':review['next_generation'],'semantic_sha256':review['semantic_sha256']},indent=2))
