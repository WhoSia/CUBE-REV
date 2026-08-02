#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/0.8.14'

def load(p:Path):return json.loads(p.read_text(encoding='utf-8'))
def main():
    committed=load(ROOT/'research/CUBE_REV_0.8.13_LIVE_COLLECTOR_EVIDENCE.json')
    archival=load(ROOT/'research/CUBE_REV_0.8.14_ARCHIVAL_LIVE_WORKFLOW_EVIDENCE.json')
    live_recon=load(ART/'archival_reconstruction_evidence.json')
    final_recon=load(ART/'final_reconstruction_evidence.json')
    cenv=committed['collector_envelope'];csnap=committed['snapshot'];aenv=archival['collector_envelope'];asnap=archival['snapshot']
    checks={
      'archival_runtime_reconstruction_matches_preserved_workflow_artifact':(
        live_recon['observed']['envelope_sha256']==aenv['sha256'] and
        live_recon['observed']['bytes']==aenv['bytes'] and
        live_recon['observed']['checksum_fnv1a32']==aenv['checksum_fnv1a32'] and
        live_recon['observed']['snapshot_raw_sha256']==asnap['sha256']),
      'committed_0_8_13_envelope_matches_final_runtime_counterfactual':(
        cenv['sha256']==final_recon['observed']['envelope_sha256'] and
        cenv['bytes']==final_recon['observed']['bytes'] and
        cenv['checksum_fnv1a32']==final_recon['observed']['checksum_fnv1a32']),
      'committed_0_8_13_envelope_matches_archival_live_submission':(
        cenv['sha256']==aenv['sha256'] and cenv['bytes']==aenv['bytes'] and cenv['checksum_fnv1a32']==aenv['checksum_fnv1a32']),
      'committed_snapshot_hash_matches_archival_raw_snapshot':csnap['sha256']==asnap['sha256'],
      'committed_snapshot_hash_matches_final_embedded_snapshot':csnap['sha256']==final_recon['observed']['embedded_snapshot_sha256'],
      'committed_receipts_match_archival_receipts':[x.get('receipt_code') for x in committed['deliveries']]==[x.get('receipt_code') for x in archival['receipts']]
    }
    if not checks['archival_runtime_reconstruction_matches_preserved_workflow_artifact']:raise RuntimeError('ARCHIVAL_RECONSTRUCTION_DOES_NOT_MATCH_ARTIFACT')
    if not checks['committed_0_8_13_envelope_matches_final_runtime_counterfactual']:raise RuntimeError('COMMITTED_VALUES_NOT_EXPLAINED_BY_FINAL_RUNTIME')
    if checks['committed_0_8_13_envelope_matches_archival_live_submission']:raise RuntimeError('EXPECTED_ARCHIVAL_DIVERGENCE_NOT_FOUND')
    report={
      'schema_version':'CR0814-LIVE-EVIDENCE-LINEAGE-AUDIT-1',
      'checks':checks,
      'archival_live_workflow':{'run':archival['source_workflow_run'],'head_sha':archival['source_head_sha'],'artifact_id':archival['source_artifact_id'],'envelope':aenv,'snapshot':asnap,'receipt_codes':[x['receipt_code'] for x in archival['receipts']]},
      'committed_0_8_13_record':{'envelope':cenv,'snapshot':csnap,'receipt_codes':[x.get('receipt_code') for x in committed['deliveries']]},
      'final_runtime_counterfactual':final_recon['observed'],
      'finding':'0.8.13 committed evidence combines post-live final-runtime-derived payload identities with receipt claims not present in the preserved live workflow artifact',
      'retained_claims':['live_endpoint_health','valid_post_acceptance','duplicate_receipt_for_same_session_filename'],
      'revoked_or_unproven_claims':['committed_envelope_was_the_payload_in_preserved_live_workflow','stored_raw_equals_committed_envelope','committed_receipt_codes_are_proven_by_preserved_artifact','exact_stored_raw_factory_replay'],
      'result':'PASS_DETECTED_EVIDENCE_LINEAGE_MIXING_REQUIRES_0_8_13_ERRATUM'
    }
    (ART/'live_evidence_lineage_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('CR0814_LIVE_EVIDENCE_LINEAGE_AUDIT_PASS lineage_mixing_detected=true erratum_required=true')
if __name__=='__main__':main()
