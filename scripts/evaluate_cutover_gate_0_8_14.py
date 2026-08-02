#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/0.8.14'

def load(rel):return json.loads((ART/rel).read_text(encoding='utf-8'))
def main():
    reconstruction=load('reconstruction_evidence.json')
    custody=load('custody/custody_replay_report.json')
    matrix=load('cross_device_browser_matrix.json')
    staging=load('staging_build_result.json')
    gates={
      'submitted_byte_reconstruction':reconstruction.get('exact_submitted_bytes_reconstructed') is True,
      'exact_stored_raw_custody_replay':custody.get('result')=='PASS_EXACT_STORED_RAW_CUSTODY_REPLAY',
      'automated_cross_engine_device_matrix':matrix.get('result')=='PASS_AUTOMATED_CROSS_ENGINE_DEVICE_EMULATION',
      'physical_device_walkthrough':False,
      'owner_acceptance_walkthrough':False,
      'deterministic_staging_bundle':staging.get('result')=='PASS_DETERMINISTIC_STAGING_CANDIDATE_BUILD',
      'production_entry_untouched':staging.get('production_default_entry_modified') is False,
      'collector_untouched':staging.get('collector_modified') is False
    }
    blocking=[k for k in ['exact_stored_raw_custody_replay','physical_device_walkthrough','owner_acceptance_walkthrough'] if not gates[k]]
    nonblocking=[k for k,v in gates.items() if not v and k not in blocking]
    cutover='GO' if not blocking and all(gates.values()) else 'NO_GO'
    report={'schema_version':'CR0814-CONTROLLED-STAGING-CUTOVER-GATE-1','gates':gates,'blocking_gates':blocking,'nonblocking_failures':nonblocking,'staging_candidate_available':gates['deterministic_staging_bundle'],'production_cutover':cutover,'automatic_merge_authorized':False,'result':f'CONTROLLED_STAGING_CANDIDATE_PASS_PRODUCTION_CUTOVER_{cutover}'}
    (ART/'cutover_gate.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f"CR0814_CUTOVER_GATE staging_candidate={str(gates['deterministic_staging_bundle']).lower()} production_cutover={cutover} blocking={','.join(blocking)}")
if __name__=='__main__':main()
