#!/usr/bin/env python3
import json
from pathlib import Path

SRC=Path('research/0.10.5-r1.4/live-canary/LIVE_COLLECTOR_CANARY.json')
OUT=Path('research/0.10.5-r1.4/final/RAVEL_FINAL_SEAL.json')
x=json.loads(SRC.read_text(encoding='utf-8'))
a=x['first_tab']; b=x['second_tab_mutated_duplicate']
fresh=x['fresh_drive_lookup']['payload']; cached=x['duplicate_cached_receipt']['payload']; prior=x['known_prior_canary_lookup']['payload']
a_ds=a['session']['data_submission']; b_ds=b['session']['data_submission']
a_ck=a_ds.get('checksum_fnv1a32'); b_ck=b_ds.get('checksum_fnv1a32')

mechanics={
 'public_release_bound': x.get('expected_main')=='19f7b83aceba3a3d0cec94a3c10b1b80af85fafd' and x.get('expected_public_sha256')=='98e6431c72c7b32fd9461b261c981b470bdda04c617bdb0595b7ce059a250180',
 'live_health_exact': x['checks'].get('health_exact') is True and x['checks'].get('independent_health_exact') is True,
 'first_canary_stored_and_verified': x['checks'].get('first_submit_stored') is True and x['checks'].get('first_receipt_checksum_verified') is True,
 'inflight_duplicate_collapsed': x['checks'].get('concurrent_submit_collapsed') is True,
 'mutated_payload_distinct': x['checks'].get('payloads_intentionally_different') is True,
 'client_observed_integrity_rejection': x['checks'].get('mutated_duplicate_rejected_by_client') is True,
 'fresh_drive_lookup_original_exact': fresh.get('status')=='stored' and fresh.get('checksum_fnv1a32')==a_ck,
 'prior_r2_canary_recovered': prior.get('status')=='stored',
 'stale_version_fail_closed': x['checks'].get('stale_version_health_fail_closed') is True,
 'synthetic_markers_present': x['checks'].get('synthetic_markers_present') is True,
 'no_page_errors': x['checks'].get('no_page_errors') is True,
}
race={
 'duplicate_cached_ack_exists': cached.get('ok') is True and cached.get('status')=='duplicate',
 'duplicate_cached_ack_nonce_matches_retry': cached.get('submission_nonce')==b_ds.get('submission_nonce'),
 'duplicate_cached_ack_session_matches': cached.get('session_id')==x.get('session_id'),
 'duplicate_cached_ack_checksum_matches_retry_B': cached.get('checksum_fnv1a32')==b_ck,
 'actual_drive_checksum_matches_original_A': fresh.get('checksum_fnv1a32')==a_ck,
 'retry_B_differs_from_original_A': bool(a_ck and b_ck and a_ck!=b_ck),
 'cached_ack_checksum_differs_from_actual_stored': cached.get('checksum_fnv1a32')!=fresh.get('checksum_fnv1a32'),
}
client_acceptance_predicate = (
 cached.get('ok') is True and cached.get('status') in ('stored','duplicate') and
 cached.get('submission_nonce')==b_ds.get('submission_nonce') and
 cached.get('session_id')==x.get('session_id') and
 str(cached.get('checksum_fnv1a32','')).lower()==str(b_ck or '').lower()
)
mechanics_pass=all(mechanics.values())
race_confirmed=all(race.values()) and client_acceptance_predicate
status='HOLD' if mechanics_pass and race_confirmed else 'FAIL'
verdict='HOLD_HUMAN_LAUNCH_LIVE_DUPLICATE_RECEIPT_STORED_BYTE_BINDING_RACE' if status=='HOLD' else 'FAIL_R14_FINALIZATION_EVIDENCE_INCOMPLETE'
out={
 'schema_version':'CR0105R14-RAVEL-FINAL-SEAL-1',
 'stage':'CUBE-REV 0.10.5-R1.4 — Live Collector Receipt Canary, Public-session End-to-end Provenance & Blinded Human-launch Gate',
 'status':status,'verdict':verdict,
 'engineering_infrastructure':'PASS' if mechanics_pass else 'FAIL',
 'human_launch_gate':'HOLD', 'human_launch':False, 'human_observations':0,
 'main_commit':'19f7b83aceba3a3d0cec94a3c10b1b80af85fafd',
 'public_sha256':'98e6431c72c7b32fd9461b261c981b470bdda04c617bdb0595b7ce059a250180',
 'collector_deployment_id':x['independent_health']['payload'].get('deployment_id'),
 'r3_session_id':x.get('session_id'),
 'known_prior_r2_session_id':x.get('known_prior_canary_session'),
 'verified_synthetic_sessions':[s for s in [x.get('known_prior_canary_session'),x.get('session_id')] if s],
 'synthetic_record_count_statement':'AT_LEAST_2_VERIFIED_R14_SYNTHETIC_RECORDS; DO_NOT INTERPRET AS HUMAN DATA',
 'stored_original':{'checksum_fnv1a32':a_ck,'receipt_code':fresh.get('receipt_code'),'file_name':fresh.get('file_name')},
 'mutated_retry':{'checksum_fnv1a32':b_ck,'submission_nonce':b_ds.get('submission_nonce'),'client_rejected':bool(b.get('submit_error'))},
 'cached_duplicate_ack':{'checksum_fnv1a32':cached.get('checksum_fnv1a32'),'submission_nonce':cached.get('submission_nonce'),'status':cached.get('status'),'confirmation_source':cached.get('confirmation_source')},
 'fresh_drive_lookup':{'checksum_fnv1a32':fresh.get('checksum_fnv1a32'),'status':fresh.get('status'),'confirmation_source':fresh.get('confirmation_source')},
 'mechanics_checks':mechanics,'race_checks':race,
 'client_acceptance_predicate_on_cached_duplicate':client_acceptance_predicate,
 'race_confirmed':race_confirmed,
 'interpretation':'The observed client rejection in R3 is timing-contingent. The later cached duplicate ACK is self-consistent with retry B but not with the immutable stored file A, so a different poll ordering can satisfy the current client acceptance predicate for bytes that were not stored.',
 'required_repair':'For status=duplicate, success must be bound to the checksum of the immutable stored file, not merely the retry payload. A client-side repair can require a fresh-nonce stored-file lookup before accepting duplicate; a server-side repair can return the existing stored-file checksum in duplicate ACKs.',
 'next_gate':'REPAIR_REQUIRED_BEFORE_HUMAN_LAUNCH'
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
if status=='FAIL': raise SystemExit(2)
