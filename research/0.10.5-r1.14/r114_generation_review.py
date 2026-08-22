#!/usr/bin/env python3
import json,hashlib,os,datetime
from pathlib import Path
OUT=Path(os.environ.get('R114_REVIEW_ROOT','/tmp/r114review'));OUT.mkdir(parents=True,exist_ok=True)
def load(p): return json.load(open(p,encoding='utf-8'))
def sha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
dev=load('research/0.10.5-r1.14/evidence-ontology/G4_ONTOLOGY_AUDIT.json')
ref=load('research/0.10.5-r1.14/evidence-reference/G4_REFERENCE_NULL_AUDIT.json')
seal=load('research/0.10.5-r1.14/evidence-reference/G4_REFERENCE_BANK_SEAL.json')
acq=load('research/0.10.5-r1.14/evidence-external-acquisition/G4_SECOND_LIVE_READ_AUDIT.json')
pre=load('research/0.10.5-r1.14/evidence-preexisting-unseen/G4_EXTERNAL_SCORE_AUDIT.json')
pre_attempts=load('research/0.10.5-r1.14/evidence-preexisting-unseen/G4_EXTERNAL_ATTEMPT_SCORES.json')['rows']
pre_features=load('research/0.10.5-r1.14/evidence-preexisting-unseen/G4_EXTERNAL_SCORED_FEATURES.json')['rows']
review_freeze=load('research/0.10.5-r1.14/G4_GENERATION_REVIEW_FREEZE.json')
sup=load('research/0.10.5-r1.14/PREEXISTING_COURT_R1_SUPERSESSION.json')
assert dev['status']=='PASS_G4_DEVELOPMENT_ONTOLOGY'
assert ref['status']=='PASS_G4_CANONICAL_REFERENCE_NULL'
assert seal['status']=='PASS_REFERENCE_BANK_SEALED_BEFORE_FRESH_OUTCOMES'
assert acq['status']=='PASS_SECOND_LIVE_READ_AND_MEMBERSHIP_FREEZE'
assert pre['status']=='PASS_PREEXISTING_UNSEEN_ONTOLOGY_TRANSPORT'
assert pre['future_roux_scoring_authority'] is False
assert sup['scientific_result_authority'] is False
assert review_freeze['status']=='FROZEN_BEFORE_PREEXISTING_UNSEEN_OUTCOMES_ARE_INSPECTED'
# Diagnostic-only: localize preexisting familywise tail without changing any gate.
tails=[a for a in pre_attempts if a.get('familywise_p') is not None and a['familywise_p']<=0.01]
feat_by={}
for z in pre_features:
    k=f"{z['result_id']}:{z['attempt_number']}"
    feat_by.setdefault(k,[]).append(z)
tail_rows=[]
for a in sorted(tails,key=lambda x:(x['familywise_p'],-x['attempt_statistic'])):
    ff=sorted(feat_by.get(a['key'],[]),key=lambda z:z.get('local_score',-1),reverse=True)
    top=ff[0] if ff else None
    tail_rows.append({'key':a['key'],'reco_id':a.get('reco_id'),'familywise_p':a['familywise_p'],'attempt_statistic':a['attempt_statistic'],'top_feature':None if top is None else {'phase':top.get('phase'),'channel':top.get('channel'),'move_count':top.get('move_count'),'move_bin':top.get('move_bin'),'observed_amplitude':top.get('observed_amplitude'),'local_level':top.get('local_level'),'local_n':top.get('local_n'),'local_p':top.get('local_p'),'local_score':top.get('local_score')}})
tail={'schema_version':'CR0105R114-PREEXISTING-TAIL-DIAGNOSTIC-1','status':'POSTHOC_DIAGNOSTIC_ONLY_NO_GATE_CHANGE','preexisting_attempts_n':len(pre_attempts),'primary_tail_n':len(tails),'primary_tail_rate':len(tails)/max(1,len(pre_attempts)),'rows':tail_rows,'gate_changed':False,'authority_effect':'NONE','human_observations':0};tail['semantic_sha256']=sha(tail)
(OUT/'PREEXISTING_TAIL_DIAGNOSTIC.json').write_text(json.dumps(tail,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
fresh_raw=acq['post_freeze_fresh']['raw_route_n']; fresh_min=acq['post_freeze_fresh']['minimum_raw_for_authority']
data_wait=fresh_raw<fresh_min
fresh_receipt={'schema_version':'CR0105R114-FRESH-AUTHORITY-DATA-WAIT-1','generation':'ROUX-MEASUREMENT-G4','status':'HOLD_DATA_WAIT' if data_wait else 'FRESH_COURT_REQUIRED','baseline_id_set_sha256':acq['baseline']['id_set_sha256'],'reference_seal_sha256':seal['seal_sha256'],'second_live_read_timestamp':acq['retrieval']['retrieved_at_utc'],'post_freeze_fresh_index_n':acq['post_freeze_fresh']['eligible_index_n'],'post_freeze_fresh_raw_route_n':fresh_raw,'minimum_raw_required':fresh_min,'substitution_with_preexisting_routes':'PROHIBITED','fresh_authority_released':False,'reason':'No post-freeze fresh Roux routes were available at the sealed second live read.' if fresh_raw==0 else 'Post-freeze fresh Roux routes were below the frozen minimum authority sample size.','human_observations':0};fresh_receipt['seal_sha256']=sha(fresh_receipt)
(OUT/'FRESH_AUTHORITY_DATA_WAIT.json').write_text(json.dumps(fresh_receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if pre['status']=='PASS_PREEXISTING_UNSEEN_ONTOLOGY_TRANSPORT' and data_wait:
    disposition='VALIDATED_FOR_PREEXISTING_UNSEEN_ONTOLOGY_TRANSPORT_AUTHORITY_DATA_WAIT';authority=False
elif pre['status']!='PASS_PREEXISTING_UNSEEN_ONTOLOGY_TRANSPORT':
    disposition='REMANDED_EXTERNAL_ONTOLOGY_TRANSPORT_FAILURE';authority=False
else:
    disposition='UNRESOLVED_FRESH_COURT_REQUIRED';authority=False
review={'schema_version':'CR0105R114-G4-GENERATION-REVIEW-1','stage':'CUBE-REV 0.10.5-R1.14 — Canonical Roux Block-preservation Ontology, Residual Reconstruction-consistency Fork & Fresh-route Gauge Authority Court','generation':'ROUX-MEASUREMENT-G4','status':'PASS_GENERATION_REVIEW_CLOSURE','generation_disposition':disposition,'evidence_chain':{'development_ontology':dev['status'],'development_canonical_n':dev['counts']['canonical'],'reference_null':ref['status'],'reference_attempt_n':ref['counts']['reference_attempts'],'reference_seal_sha256':seal['seal_sha256'],'preexisting_unseen_transport':pre['status'],'preexisting_raw_n':pre['counts']['raw_routes'],'preexisting_canonical_n':pre['counts']['canonical'],'preexisting_canonical_rate_given_eligible':pre['rates']['canonical_given_eligible'],'preexisting_fallback_rate':pre['rates']['local_reference_fallback'],'fresh_raw_n':fresh_raw,'fresh_minimum_required':fresh_min,'fresh_status':fresh_receipt['status'],'r1_operational_supersession_preserved':True},'inheritance':{'RETAIN':['G4 CANONICAL_FB_PRESERVING state ontology','BLOCK_DISRUPTIVE_RESIDUAL and FB_PRESERVED_NO_COMPLETION_RESIDUAL as observable forks','prefix-only gauge identification with explicit x/y/z transport','114-attempt canonical reference bank and its frozen local/familywise null','1% add-one resolution and no-alpha-relaxation','freshness baseline and post-freeze-only authority rule'],'DOWNGRADE':['preexisting unseen familywise tail is transport-diagnostic only and cannot be interpreted as cognitive anomaly prevalence'],'RETIRE':['superseded preexisting court R1 output caused by omitted pre-recorded helper repair'],'MUTATE':[],'FORK':['future genuinely post-freeze fresh authority lane remains separate from baseline-present unseen lane'],'RECOMBINE':['G4 ontology plus frozen reference scorer is technically ready for a future post-freeze fresh court without reopening development definitions'],'UNRESOLVED':['fresh authority because post-freeze fresh Roux N=0','official-attempt duplicate exclusion for future fresh records when linkage is not yet available']},'authority':{'roux_future_scoring_authority':authority,'preexisting_unseen_can_release':False,'fresh_data_wait':data_wait,'cognitive_recovery_or_error_claim':'PROHIBITED','causal_intentional_strategy_claim':'PROHIBITED','full_WCA_prevalence':'PROHIBITED','human_recruitment':'DEFERRED_BY_RESEARCH_DESIGN','human_observations':0},'next_generation':{'open_new_generation_now':False,'reason':'Data wait is not a measurement-generation failure. Keep G4 frozen until genuinely post-freeze fresh Roux evidence exists; meanwhile manuscript/observation-operator synthesis may proceed on a separate writing branch.'},'post_result_gate_change':False,'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};review['semantic_sha256']=sha(review)
(OUT/'G4_GENERATION_REVIEW.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'disposition':disposition,'preexisting_status':pre['status'],'preexisting_canonical_n':pre['counts']['canonical'],'preexisting_canonical_rate':pre['rates']['canonical_given_eligible'],'tail_n':len(tails),'fresh_raw_n':fresh_raw,'fresh_status':fresh_receipt['status'],'authority':authority,'review_sha256':review['semantic_sha256']},indent=2))
