#!/usr/bin/env python3
import json, math, hashlib, os
from pathlib import Path
from fractions import Fraction

ROOT=Path(os.environ.get('R112_ROOT','/tmp/r112')); ROOT.mkdir(parents=True,exist_ok=True)
BASE=Path('research/0.10.5-r1.12')

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def semsha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def rate(n,d): return n/d if d else 0.0

def fisher_two_sided(a,b,c,d):
    # Fixed-margin 2x2 Fisher exact, two-sided probability ordering.
    r1=a+b; r2=c+d; c1=a+c; n=r1+r2
    lo=max(0,c1-r2); hi=min(r1,c1)
    den=math.comb(n,c1)
    def prob(x): return math.comb(r1,x)*math.comb(r2,c1-x)/den
    p0=prob(a)
    return sum(prob(x) for x in range(lo,hi+1) if prob(x)<=p0+1e-15)

rules=load(BASE/'GENERATION_REVIEW_AUTHORITY_RULES.json')
g=load(BASE/'evidence-g2/ROUX_G2_GEOMETRY_AUDIT.json')
n=load(BASE/'evidence-g2/ROUX_G2_NULL_AUDIT.json')
d1=load(BASE/'evidence-destroy/ROUX_G2_COORDINATE_GAUGE_DESTROY_AUDIT.json')
gi=load(BASE/'evidence-gauge-identifiability/ROUX_G2_GAUGE_IDENTIFIABILITY_AUDIT.json')
r=load(BASE/'evidence-residual-gauge/ROUX_G2_RESIDUAL_GAUGE_AUDIT.json')

assert rules['nonnegotiable']['r112_g2_primary_can_be_released_by_posthoc_diagnostics'] is False
assert g['status']=='HOLD_ROUX_G2_GEOMETRY' and g['semantic_sha256']=='f1c19e8b960373e9968cab8b57c48a0ae4ed130d02d8d27704126462d40595e8'
assert n['status']=='HOLD_ROUX_G2_NULL_FOUNDRY'
assert d1['semantic_sha256']=='9f505ef602a68d0c62158bfc0f05f81b5da7dcdc7951b82b0048202b6ccb2611'
assert gi['semantic_sha256']=='c6c776bc5df6cecc394f6acc2f4dc687e2c958ac20b6dac73a9b93c8af2a3b9a'
assert r['semantic_sha256']=='bcc971b134682d9f3c1f9445cbb3e49af527fadabc2c31b788cfc44033843e8d'
assert all(x.get('post_result_gate_change') is False for x in [g,d1,gi,r])

eligible=gi['counts']['eligible']
prefix_unique=rate(gi['counts']['prefix_unique_pair'],eligible)
prefix_success=rate(gi['counts']['prefix_unique_pair_sb_success'],eligible)
sealed=gi['by_source']['SEALED_R111']; expansion=gi['by_source']['R112_EXPANSION']
sealed_success=rate(sealed['prefix_unique_pair_sb_success'],sealed['eligible'])
expansion_success=rate(expansion['prefix_unique_pair_sb_success'],expansion['eligible'])
dynamic_change=gi['rates']['dynamic_center_gauge_changed_fb_to_sb']
criteria={
  'prefix_unique_ge_0_95':prefix_unique>=.95,
  'prefix_sb_success_ge_0_90':prefix_success>=.90,
  'sealed_slice_ge_0_85':sealed_success>=.85,
  'expansion_slice_ge_0_85':expansion_success>=.85,
  'dynamic_center_gauge_change_ge_0_80':dynamic_change>=.80,
  'no_post_result_primary_change':True
}
g3_candidate=all(criteria.values())

fail=r['counts']['prefix_failure']; succ=r['counts']['prefix_success']
late=rate(r['counts']['failure_completion_any_later'],fail)
rot_fail=rate(r['counts']['failure_has_rotation_in_sb'],fail)
rot_succ=rate(r['counts']['success_has_rotation_in_sb'],succ)
rot_ratio=(rot_fail/rot_succ) if rot_succ else float('inf')
wide_fail=rate(r['counts']['failure_has_wide_slice_in_sb'],fail)
wide_succ=rate(r['counts']['success_has_wide_slice_in_sb'],succ)
wide_ratio=(wide_fail/wide_succ) if wide_succ else float('inf')
fisher_p=fisher_two_sided(r['counts']['failure_has_rotation_in_sb'], fail-r['counts']['failure_has_rotation_in_sb'], r['counts']['success_has_rotation_in_sb'], succ-r['counts']['success_has_rotation_in_sb'])
# Cross-product odds ratio, finite because all cells are nonzero.
rot_or=(r['counts']['failure_has_rotation_in_sb']*(succ-r['counts']['success_has_rotation_in_sb']))/((fail-r['counts']['failure_has_rotation_in_sb'])*r['counts']['success_has_rotation_in_sb'])
if late>=.50:
    residual_branch='NEXT_G3_MUST_COMBINE_PREFIX_GAUGE_WITH_PHASE_SPAN_REDESIGN'
elif late<=.20:
    residual_branch='NEXT_G3_SHOULD_RETAIN_FROZEN_SB_SPAN_AND_FOCUS_ON_GAUGE_TRANSPORT_OR_RESIDUAL_ROUTE_STRATA'
elif rot_ratio>=1.5:
    residual_branch='NEXT_G3_SHOULD_TEST_ROTATION_COVARIANT_GAUGE_TRANSPORT'
else:
    residual_branch='NEXT_G3_FIXED_PREFIX_GAUGE_WITH_EXPLICIT_RESIDUAL_STRATIFICATION'

review={
 'schema_version':'CR0105R112-GENERATION-REVIEW-CLOSURE-1',
 'stage':'CUBE-REV 0.10.5-R1.12 — Gauge Identifiability Court & Generation Review Closure',
 'generation_under_review':'ROUX-MEASUREMENT-G2',
 'status':'PASS_GENERATION_REVIEW_G2_REMANDED_G3_CANDIDATE_IDENTIFIED' if g3_candidate else 'PASS_GENERATION_REVIEW_G2_REMANDED_G3_UNRESOLVED',
 'primary_disposition':{
   'g2':'REMANDED_NOT_RELEASED',
   'reason':'Frozen G2 center-consistent operator admitted 10/130 ordinary-FB SB-search-eligible routes and failed geometry/null/resolution gates.',
   'geometry_status':g['status'],'null_status':n['status'],'future_roux_scoring_authority':False,
   'posthoc_diagnostics_can_repair_g2':False
 },
 'gauge_identifiability':{
   'eligible_n':eligible,
   'prefix_unique_pair_n':gi['counts']['prefix_unique_pair'],'prefix_unique_pair_rate':prefix_unique,
   'prefix_sb_success_n':gi['counts']['prefix_unique_pair_sb_success'],'prefix_sb_success_rate':prefix_success,
   'route_global_joint_solution_n':gi['counts']['route_global_joint_solution'],
   'prefix_success_equals_joint_solution_count':gi['counts']['prefix_unique_pair_sb_success']==gi['counts']['route_global_joint_solution'],
   'final_gauge_sb_success_n':gi['counts']['final_gauge_sb_success'],'final_gauge_sb_success_rate':gi['rates']['final_gauge_sb_success'],
   'sealed_slice_success_rate':sealed_success,'expansion_slice_success_rate':expansion_success,
   'dynamic_center_gauge_changed_fb_to_sb_rate':dynamic_change,
   'fb_center_gauge_differs_final_rate':gi['rates']['fb_center_gauge_differs_final'],
   'g3_candidate_criteria':criteria,'g3_candidate_identified':g3_candidate
 },
 'residual_court':{
   'failures_n':fail,'late_completion_any_later_n':r['counts']['failure_completion_any_later'],'late_completion_fraction':late,
   'late_completion_before_cmll_n':r['counts']['failure_completion_after_sb_before_cmll'],
   'first_block_breaks_n':r['counts']['failure_first_block_breaks_in_sb'],
   'rotation_in_sb_failure_rate':rot_fail,'rotation_in_sb_success_rate':rot_succ,'rotation_enrichment_ratio':rot_ratio,
   'rotation_odds_ratio':rot_or,'rotation_fisher_exact_two_sided_p':fisher_p,
   'wide_slice_failure_rate':wide_fail,'wide_slice_success_rate':wide_succ,'wide_slice_enrichment_ratio':wide_ratio,
   'adjudicated_next_design_branch':residual_branch,
   'statistics_role':'diagnostic only; n=10 residual failures and posthoc stratification prohibit confirmatory interpretation'
 },
 'inheritance_closure':{
   'RETAIN':[
     'state-certified first two-block completion within the frozen Roux SB span',
     'FB-prefix-only frame identification as a prospective measurement hypothesis, not as R1.12 authority',
     'Roux-only null architecture, nested outer-fold exclusion, alpha=0.01 and finite-resolution requirements',
     'ordinary-FB primary stratum with pseudo-FB/FBDR forked separately'
   ],
   'DOWNGRADE':[
     'fixed route-global gauge: strong diagnostic coverage (120/130) but residual rotation enrichment argues against assuming universal constancy',
     'final-state-derived gauge: 117/130 SB prediction and uses future information, therefore diagnostic only'
   ],
   'RETIRE':[
     'per-state center canonicalization as the persistent Roux route coordinate frame',
     'ROUX-MEASUREMENT-G2 center-consistent authority candidate',
     'R1.12 G2 feature/null bank for any future fresh scoring'
   ],
   'MUTATE':[
     'route frame -> FB-prefix-initialized gauge with prospectively specified rotation-covariant transport',
     'residual handling -> explicit route stratum/audit rather than posthoc endpoint substitution'
   ],
   'FORK':[
     'pseudo-FB/FBDR routes',
     'prefix-gauge residual routes with explicit SB rotations or first-block breakage'
   ],
   'RECOMBINE':[
     'R1.11 route-global quotient insight + R1.12 state-certified subphase completion + prefix-only identifiability',
     'rotation-token transport semantics + block-state objective geometry'
   ],
   'UNRESOLVED':[
     'causal source of the 10 prefix-gauge failures',
     'whether explicit rotation transport alone resolves those failures',
     'whether first-block breakage represents legitimate Roux substructure or annotation/operator mismatch',
     'whole-project CUBE-REV generation numbering'
   ]
 },
 'next_generation':{
   'label':'ROUX-MEASUREMENT-G3' if g3_candidate else 'UNRESOLVED',
   'version_candidate':'CUBE-REV 0.10.5-R1.13',
   'title_candidate':'Route-global Reconstruction Gauge, Rotation-covariant Prefix Frame & Rebuilt Roux Completion Null',
   'must_begin_with_new_NAPKIN':True,
   'may_reuse_r112_outcomes_as_confirmatory_evidence':False,
   'requires_rebuilt_features_and_null':True,
   'future_scoring_authority_at_transition':False
 },
 'authority':{
   'main_write':False,'public_runner_write':False,'collector_write':False,'human_recruitment':False,'human_observations':0,
   'cognitive_recovery_error_prevalence_claim':'PROHIBITED','causal_intentionality_claim':'PROHIBITED','full_wca_prevalence_claim':'PROHIBITED'
 },
 'source_semantic_sha256':{
   'g2_geometry':g['semantic_sha256'],'g2_null':n['semantic_sha256'],'joint_destroy':d1['semantic_sha256'],'gauge_identifiability':gi['semantic_sha256'],'residual':r['semantic_sha256']
 }
}
review['semantic_sha256']=semsha(review)
(Path(ROOT)/'GENERATION_REVIEW_CLOSURE.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'status':review['status'],'g2':review['primary_disposition']['g2'],'g3_candidate':g3_candidate,'prefix_success_rate':prefix_success,'sealed_slice':sealed_success,'expansion_slice':expansion_success,'rotation_enrichment_ratio':rot_ratio,'rotation_odds_ratio':rot_or,'rotation_fisher_p':fisher_p,'residual_branch':residual_branch,'semantic_sha256':review['semantic_sha256']},indent=2))
