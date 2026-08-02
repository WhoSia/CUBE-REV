#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/0.8.14'
ERRATUM=ROOT/'research/CUBE_REV_0.8.13_ERRATUM_FROM_0.8.14.md'
def load(rel):return json.loads((ART/rel).read_text(encoding='utf-8'))
def erratum_valid():
    if not ERRATUM.is_file():return False
    text=ERRATUM.read_text(encoding='utf-8')
    required=['6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9','16217','c8cda746','supersedes','HOLD-LIVE-STORED-RAW-FACTORY-REPLAY']
    lower=text.lower();return all(token.lower() in lower for token in required)
def main():
    archival=load('archival_reconstruction_evidence.json');final=load('final_reconstruction_evidence.json');audit=load('live_evidence_lineage_audit.json');custody=load('custody/custody_replay_report.json');matrix=load('cross_device_browser_matrix.json');staging=load('staging_build_result.json')
    gates={
      'archival_live_submitted_byte_reconstruction':archival.get('result')=='PASS_ARCHIVAL_LIVE_SUBMITTED_BYTE_RECONSTRUCTION',
      'final_runtime_observation':str(final.get('result','')).startswith('PASS_FINAL_RUNTIME_'),
      'evidence_lineage_inconsistency_detected':audit.get('result')=='PASS_DETECTED_0_8_13_LIVE_EVIDENCE_LINEAGE_INCONSISTENCY_REQUIRES_ERRATUM',
      'evidence_lineage_reconciliation':erratum_valid(),
      'exact_stored_raw_custody_replay':str(custody.get('result','')).startswith('PASS_EXACT_STORED_RAW_CUSTODY_REPLAY'),
      'controlled_staging_browser_policy_matrix':matrix.get('result')=='PASS_CONTROLLED_STAGING_BROWSER_POLICY_MATRIX',
      'chromium_active_execution_automated':matrix.get('chromium_active_execution_certified_automated') is True,
      'firefox_fail_closed_policy':matrix.get('firefox_active_execution_certified') is False,
      'webkit_fail_closed_policy':matrix.get('webkit_active_execution_certified') is False,
      'active_profile_race_repetition':matrix.get('active_execution_passed_cells')==2 and matrix.get('active_race_iterations_passed')==8,
      'fail_closed_profile_count':matrix.get('fail_closed_passed_cells')==4,
      'physical_device_walkthrough':False,
      'owner_acceptance_walkthrough':False,
      'deterministic_staging_bundle':staging.get('result')=='PASS_DETERMINISTIC_STAGING_CANDIDATE_BUILD',
      'production_entry_untouched':staging.get('production_default_entry_modified') is False,
      'collector_untouched':staging.get('collector_modified') is False
    }
    blocking_names=['evidence_lineage_reconciliation','exact_stored_raw_custody_replay','controlled_staging_browser_policy_matrix','physical_device_walkthrough','owner_acceptance_walkthrough']
    blocking=[k for k in blocking_names if not gates[k]];nonblocking=[k for k,v in gates.items() if not v and k not in blocking];cutover='GO' if not blocking and all(gates.values()) else 'NO_GO'
    report={'schema_version':'CR0814-CONTROLLED-STAGING-CUTOVER-GATE-6','gates':gates,'blocking_gates':blocking,'nonblocking_failures':nonblocking,'staging_candidate_available':gates['deterministic_staging_bundle'],'supported_active_profiles':['chromium-desktop','chromium-android-emulation'],'fail_closed_profiles':['firefox-desktop','firefox-compact-viewport','webkit-desktop','webkit-iphone-emulation','unknown-engines'],'physical_device_certified':False,'production_cutover':cutover,'automatic_merge_authorized':False,'result':f'CONTROLLED_STAGING_CANDIDATE_PASS_PRODUCTION_CUTOVER_{cutover}'}
    (ART/'cutover_gate.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(f"CR0814_CUTOVER_GATE staging_candidate={str(gates['deterministic_staging_bundle']).lower()} production_cutover={cutover} blocking={','.join(blocking)}")
if __name__=='__main__':main()
