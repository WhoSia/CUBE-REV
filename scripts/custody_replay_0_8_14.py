#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

EXPECTED_FILE='CR-20260802110000-0813a0b0c0d0.json'
COMMITTED_LEDGER_CLAIM={'sha256':'6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3','bytes':21227,'checksum':'f795cd8e'}
def sha256(data: bytes)->str:return hashlib.sha256(data).hexdigest()
def fnv1a32(text: str)->str:
    h=0x811C9DC5
    for ch in text:h^=ord(ch);h=(h*0x01000193)&0xffffffff
    return f'{h:08x}'
def fingerprint(p:Path):
    data=p.read_bytes();return {'sha256':sha256(data),'bytes':len(data),'checksum':fnv1a32(data.decode('utf-8'))}

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=Path('custody')/EXPECTED_FILE);ap.add_argument('--archival-reconstructed',type=Path,default=Path('artifacts/0.8.14/archival_live_envelope.json'));ap.add_argument('--final-reconstructed',type=Path,default=Path('artifacts/0.8.14/final_runtime_envelope.json'));ap.add_argument('--archival-evidence',type=Path,default=Path('artifacts/0.8.14/archival_reconstruction_evidence.json'));ap.add_argument('--final-evidence',type=Path,default=Path('artifacts/0.8.14/final_reconstruction_evidence.json'));ap.add_argument('--outdir',type=Path,default=Path('artifacts/0.8.14/custody'));args=ap.parse_args();args.outdir.mkdir(parents=True,exist_ok=True)
    ae=json.loads(args.archival_evidence.read_text(encoding='utf-8'));fe=json.loads(args.final_evidence.read_text(encoding='utf-8'))
    reconstructed={'archival_live_submission':fingerprint(args.archival_reconstructed),'final_runtime_observation':fingerprint(args.final_reconstructed),'committed_0_8_13_ledger_claim':COMMITTED_LEDGER_CLAIM}
    if reconstructed['archival_live_submission']!={k:ae['observed'][{'sha256':'envelope_sha256','bytes':'bytes','checksum':'checksum_fnv1a32'}[k]] for k in ['sha256','bytes','checksum']}:raise RuntimeError('ARCHIVAL_EVIDENCE_FILE_MISMATCH')
    if reconstructed['final_runtime_observation']!={k:fe['observed'][{'sha256':'envelope_sha256','bytes':'bytes','checksum':'checksum_fnv1a32'}[k]] for k in ['sha256','bytes','checksum']}:raise RuntimeError('FINAL_EVIDENCE_FILE_MISMATCH')
    report={'schema_version':'CR0814-STORED-RAW-CUSTODY-REPLAY-3','expected_file_name':EXPECTED_FILE,'stored_raw_identity_prior_to_retrieval':'UNKNOWN_BECAUSE_COLLECTOR_DEDUPLICATES_BY_SESSION_FILENAME','candidate_fingerprints':reconstructed,'raw_path':str(args.raw),'direct_drive_raw_available':args.raw.is_file()}
    if not args.raw.is_file():
        report.update({'factory_on_exact_stored_raw_executed':False,'stored_raw_matches':[],'result':'HOLD_DIRECT_STORED_RAW_UNAVAILABLE_THREE_IDENTITY_CANDIDATES_RECORDED'})
        (args.outdir/'custody_replay_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('CR0814_STORED_RAW_CUSTODY_HOLD direct_raw=false candidates=archival,final_observed,committed_ledger');return 0
    raw=args.raw.read_bytes();observed={'sha256':sha256(raw),'bytes':len(raw),'checksum':fnv1a32(raw.decode('utf-8'))};matches=[name for name,v in reconstructed.items() if v==observed];report.update({'observed':observed,'stored_raw_matches':matches})
    factory_out=args.outdir/'factory';subprocess.run([sys.executable,'factory/cognitive_snapshot_adapter_0_8_13.py',str(args.raw),'--outdir',str(factory_out)],check=True)
    manifest=json.loads((factory_out/'analysis_manifest.json').read_text(encoding='utf-8'));report.update({'factory_on_exact_stored_raw_executed':True,'analysis_eligible':manifest.get('analysis_eligible'),'blocking_qc_count':manifest.get('blocking_qc_count'),'result':'PASS_EXACT_STORED_RAW_CUSTODY_REPLAY_KNOWN_IDENTITY' if matches else 'PASS_EXACT_STORED_RAW_CUSTODY_REPLAY_PREVIOUSLY_UNKNOWN_IDENTITY'})
    (args.outdir/'custody_replay_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(f"CR0814_STORED_RAW_CUSTODY_PASS sha256={observed['sha256']} matches={','.join(matches) or 'unknown'} analysis_eligible={report['analysis_eligible']}");return 0
if __name__=='__main__':raise SystemExit(main())
