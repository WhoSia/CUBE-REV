#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

ROOT=Path('.')
R=ROOT/'research/0.10.5-r1.15'
PARENT=ROOT/'research/0.10.5-r1.14/final/RAVEL_FINAL_SEAL.json'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    parent=load(PARENT)
    nap=load(R/'MANUSCRIPT_NAPKIN_AND_LIFECYCLE_FREEZE.json')
    adoption=load(R/'SKILL_WORKSHOP_2.4.1_CROSS_CHAT_ADOPTION.json')
    atlas=load(R/'CROSS_GENERATION_OBSERVATION_OPERATOR_ATLAS.json')
    claims=load(R/'CLAIM_AUTHORITY_LEDGER.json')
    ablate=load(R/'PROVENANCE_FAMILY_ABLATION_COURT.json')
    lit=load(R/'LITERATURE_GAP_COURT.json')
    source=load(R/'SOURCE_MAP_AND_CITATION_AUDIT.json')
    bundle=load(R/'MANUSCRIPT_BUNDLE_INDEX.json')
    ready=load(R/'MANUSCRIPT_READINESS_AND_DEBT.json')
    ko=(R/'SEMANTIC_MASTER_KO.md').read_text(encoding='utf-8')
    en=(R/'ABSTRACT_EN_DRAFT.md').read_text(encoding='utf-8')
    referee=(R/'HOSTILE_REFEREE_COURT.md').read_text(encoding='utf-8')

    claim_rows=claims['claims']
    ids={x['id'] for x in claim_rows}
    statuses={x['id']:x['authority'] for x in claim_rows}
    checks={
      'parent_is_g4_data_wait': parent['status']=='PASS_G4_ONTOLOGY_TRANSPORT_WITH_FRESH_AUTHORITY_DATA_WAIT',
      'parent_roux_authority_false': parent['authority']['roux_future_scoring_authority'] is False,
      'parent_fresh_zero': parent['freshness_baseline']['post_freeze_fresh_raw_routes']==0,
      'parent_fresh_threshold_20': parent['freshness_baseline']['minimum_post_freeze_fresh_raw_routes_for_authority']==20,
      'no_new_measurement_generation': nap['parent_final_seal']['measurement_generation']=='ROUX-MEASUREMENT-G4' and nap['parent_final_seal']['open_new_measurement_generation'] is False,
      'writing_not_evidence': nap['lifecycle']['writing_is_evidence'] is False and adoption['promoted_principles']['writing_as_epistemic_stress'].startswith('Draft argument'),
      'claim_ledger_has_c1_c10': all(f'C{i}_' in ' '.join(ids) for i in range(1,11)),
      'c9_cognitive_prevalence_prohibited': statuses.get('C9_COGNITIVE_PREVALENCE')=='PROHIBITED',
      'c10_firstness_hold': statuses.get('C10_WORLD_FIRST_NOVELTY')=='HOLD_LITERATURE_GAP_NOT_SYSTEMATICALLY_CLOSED',
      'operator_atlas_has_8_stages': len(atlas['operator_lineage'])==8,
      'family_ablation_all_four': len(ablate['families'])==4,
      'family_ablation_discloses_positive_endpoint_dependence': ablate['cross_family_conclusion']['positive_endpoint']=='MATERIALLY_DEPENDS_ON_F4_ROUX_G3_G4',
      'bounded_literature_not_systematic': lit['search_scope']['type'].startswith('bounded targeted'),
      'firstness_not_authorized': lit['gap_assessment']['strong_firstness_authorized'] is False,
      'internal_source_map_pass': source['citation_audit']['internal_numeric_claims_have_source_paths'] is True,
      'workflow_receipts_not_effect_evidence': source['citation_audit']['manuscript_may_cite_workflow_ids_as_scientific_support'] is False,
      'bundle_not_frozen': bundle['ready_for_freeze'] is False,
      'readiness_hold_preprint': ready['status']=='PASS_MANUSCRIPT_BRIDGE_HOLD_PREPRINT_FREEZE',
      'more_metric_iterations_should_not_continue_now': ready['should_continue_decision']['more_measurement_metric_iterations_now'] is False,
      'semantic_master_marks_not_evidence': 'evidence 아님' in ko,
      'english_abstract_marks_not_evidence': 'not evidence' in en.lower(),
      'referee_rejects_cognitive_prevalence_paper': 'FAILS_AS_COGNITIVE_PREVALENCE_PAPER' in referee,
      'semantic_master_prohibits_world_first': "'CUBE-REV가 세계 최초다.'" in ko,
      'abstract_does_not_claim_fresh_roux_authority': 'Genuinely post-freeze Roux validation remains pending' in en,
    }
    # Mainline thesis should survive single provenance-family ablation, though the positive endpoint may narrow.
    checks['central_thesis_survives_each_family_ablation']=all(v['central_thesis_survives'] for v in ablate['families'].values())

    # Audit only positive mainline English abstract text, not quoted prohibited examples in guard documents.
    banned=[
      r'we (?:measured|identified|estimated) cognitive recovery',
      r'cognitive error prevalence (?:was|is|equals)',
      r'first study to',
      r'world[- ]first',
      r'fresh replication',
    ]
    banned_hits=[]
    low=en.lower()
    for pat in banned:
      if re.search(pat,low): banned_hits.append(pat)
    checks['abstract_banned_claims_absent']=not banned_hits

    failed=[k for k,v in checks.items() if not v]
    status='PASS_ARGUMENT_COURT_MANUSCRIPT_BRIDGE' if not failed else 'HOLD_ARGUMENT_COURT'
    out={
      'schema_version':'CR0105R115-ARGUMENT-COURT-1',
      'status':status,
      'measurement_generation':'ROUX-MEASUREMENT-G4',
      'new_measurement_generation_opened':False,
      'checks':checks,
      'failed_checks':failed,
      'banned_abstract_hits':banned_hits,
      'artifact_sha256':{
        'manuscript_napkin':h(R/'MANUSCRIPT_NAPKIN_AND_LIFECYCLE_FREEZE.json'),
        'operator_atlas':h(R/'CROSS_GENERATION_OBSERVATION_OPERATOR_ATLAS.json'),
        'claim_ledger':h(R/'CLAIM_AUTHORITY_LEDGER.json'),
        'semantic_master_ko':h(R/'SEMANTIC_MASTER_KO.md'),
        'abstract_en':h(R/'ABSTRACT_EN_DRAFT.md'),
        'hostile_referee':h(R/'HOSTILE_REFEREE_COURT.md'),
        'provenance_ablation':h(R/'PROVENANCE_FAMILY_ABLATION_COURT.json'),
        'literature_gap':h(R/'LITERATURE_GAP_COURT.json'),
        'source_map':h(R/'SOURCE_MAP_AND_CITATION_AUDIT.json'),
        'readiness':h(R/'MANUSCRIPT_READINESS_AND_DEBT.json')
      },
      'court_disposition':{
        'paper_sized_claim':'PASS_MEASUREMENT_METHOD_SCOPE' if not failed else 'HOLD',
        'cognitive_prevalence_paper':'PROHIBITED',
        'preprint_freeze':'HOLD',
        'roux_fresh_authority':'HOLD_DATA_WAIT_0_OF_20'
      },
      'human_observations':0
    }
    out['semantic_sha256']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    dest=Path('/tmp/r115');dest.mkdir(parents=True,exist_ok=True)
    (dest/'ARGUMENT_COURT_AUDIT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':status,'failed':failed,'semantic_sha256':out['semantic_sha256']},indent=2))
    return 0 if not failed else 2

if __name__=='__main__': raise SystemExit(main())
