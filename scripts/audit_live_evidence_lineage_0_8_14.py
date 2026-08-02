#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/0.8.14'
def load(p:Path):return json.loads(p.read_text(encoding='utf-8'))
def same_envelope(a,b):return a['sha256']==b['envelope_sha256'] and a['bytes']==b['bytes'] and a['checksum_fnv1a32']==b['checksum_fnv1a32']
def main():
    committed=load(ROOT/'research/CUBE_REV_0.8.13_LIVE_COLLECTOR_EVIDENCE.json')
    archival=load(ROOT/'research/CUBE_REV_0.8.14_ARCHIVAL_LIVE_WORKFLOW_EVIDENCE.json')
    live_recon=load(ART/'archival_reconstruction_evidence.json');final_recon=load(ART/'final_reconstruction_evidence.json')
    cenv=committed['collector_envelope'];csnap=committed['snapshot'];aenv=archival['collector_envelope'];asnap=archival['snapshot'];lo=live_recon['observed'];fo=final_recon['observed']
    checks={
      'archival_reconstruction_matches_preserved_workflow_artifact':same_envelope(aenv,lo) and lo['snapshot_raw_sha256']==asnap['sha256'],
      'committed_envelope_matches_archival_live_submission':same_envelope(cenv,lo),
      'committed_envelope_matches_final_head_observation':same_envelope(cenv,fo),
      'committed_snapshot_hash_matches_archival_raw_snapshot':csnap['sha256']==asnap['sha256'],
      'committed_snapshot_hash_matches_final_embedded_snapshot':csnap['sha256']==fo['embedded_snapshot_sha256'],
      'committed_receipts_match_archival_receipts':[x.get('receipt_code') for x in committed['deliveries']]==[x.get('receipt_code') for x in archival['receipts']]
    }
    if not checks['archival_reconstruction_matches_preserved_workflow_artifact']:raise RuntimeError('ARCHIVAL_RECONSTRUCTION_DOES_NOT_MATCH_ARTIFACT')
    if checks['committed_envelope_matches_archival_live_submission']:raise RuntimeError('EXPECTED_ARCHIVAL_DIVERGENCE_NOT_FOUND')
    explanation='UNEXPLAINED_BY_ARCHIVAL_LIVE_COMMIT_AND_FINAL_0_8_13_HEAD'
    if checks['committed_envelope_matches_final_head_observation']:explanation='MATCHES_FINAL_0_8_13_HEAD_ONLY'
    report={
      'schema_version':'CR0814-LIVE-EVIDENCE-LINEAGE-AUDIT-2','checks':checks,
      'archival_live_workflow':{'run':archival['source_workflow_run'],'head_sha':archival['source_head_sha'],'artifact_id':archival['source_artifact_id'],'envelope':aenv,'snapshot':asnap,'receipt_codes':[x['receipt_code'] for x in archival['receipts']]},
      'committed_0_8_13_record':{'envelope':cenv,'snapshot':csnap,'receipt_codes':[x.get('receipt_code') for x in committed['deliveries']]},
      'final_0_8_13_head_observation':fo,'committed_identity_explanation':explanation,
      'finding':'The committed 0.8.13 live evidence record is not the preserved live workflow artifact. Its payload identity is also not reproduced by the final 0.8.13 head, and its receipt codes differ from the preserved artifact.',
      'retained_claims':['live_endpoint_health','valid_posts_reached_receipt_v2','two_duplicate_receipts_reference_same_session_filename'],
      'revoked_or_unproven_claims':['committed_envelope_was_the_preserved_live_submission','stored_raw_equals_any_reconstructed_candidate','committed_receipt_codes_are_proven_by_preserved_artifact','exact_stored_raw_factory_replay'],
      'required_correction':['publish_0_8_13_erratum','identify_or_retract_unexplained_committed_payload_identity','retrieve_exact_stored_raw_or_keep_custody_hold'],
      'result':'PASS_DETECTED_0_8_13_LIVE_EVIDENCE_LINEAGE_INCONSISTENCY_REQUIRES_ERRATUM'
    }
    (ART/'live_evidence_lineage_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f"CR0814_LIVE_EVIDENCE_LINEAGE_AUDIT_PASS inconsistency=true committed_identity={explanation} erratum_required=true")
if __name__=='__main__':main()
