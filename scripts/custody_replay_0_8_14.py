#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

EXPECTED_SHA='6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3'
EXPECTED_BYTES=21227
EXPECTED_FILE='CR-20260802110000-0813a0b0c0d0.json'

def sha256(data: bytes)->str:return hashlib.sha256(data).hexdigest()
def fnv1a32(text: str)->str:
    h=0x811C9DC5
    for ch in text:
        h^=ord(ch);h=(h*0x01000193)&0xffffffff
    return f'{h:08x}'

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--raw',type=Path,default=Path('custody')/EXPECTED_FILE)
    ap.add_argument('--reconstructed',type=Path,default=Path('artifacts/0.8.14/reconstructed_live_envelope.json'))
    ap.add_argument('--outdir',type=Path,default=Path('artifacts/0.8.14/custody'))
    args=ap.parse_args();args.outdir.mkdir(parents=True,exist_ok=True)
    report={'schema_version':'CR0814-STORED-RAW-CUSTODY-REPLAY-1','expected_file_name':EXPECTED_FILE,'expected_sha256':EXPECTED_SHA,'expected_bytes':EXPECTED_BYTES,'raw_path':str(args.raw),'direct_drive_raw_available':args.raw.is_file()}
    if not args.raw.is_file():
        reconstructed=args.reconstructed.read_bytes()
        report.update({'reconstructed_submitted_bytes_available':True,'reconstructed_sha256':sha256(reconstructed),'reconstructed_bytes':len(reconstructed),'reconstructed_checksum_fnv1a32':fnv1a32(reconstructed.decode('utf-8')),'factory_on_exact_stored_raw_executed':False,'result':'HOLD_DIRECT_DRIVE_RAW_UNAVAILABLE_PASS_SUBMITTED_BYTE_RECONSTRUCTION'})
        if report['reconstructed_sha256']!=EXPECTED_SHA or len(reconstructed)!=EXPECTED_BYTES:raise RuntimeError('RECONSTRUCTED_IDENTITY_MISMATCH')
        (args.outdir/'custody_replay_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print('CR0814_STORED_RAW_CUSTODY_HOLD direct_drive_raw_available=false submitted_byte_reconstruction=true')
        return 0
    raw=args.raw.read_bytes();report.update({'observed_sha256':sha256(raw),'observed_bytes':len(raw),'observed_checksum_fnv1a32':fnv1a32(raw.decode('utf-8'))})
    if report['observed_sha256']!=EXPECTED_SHA or len(raw)!=EXPECTED_BYTES:
        report.update({'factory_on_exact_stored_raw_executed':False,'result':'FAIL_STORED_RAW_IDENTITY_MISMATCH'});(args.outdir/'custody_replay_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');raise RuntimeError('STORED_RAW_IDENTITY_MISMATCH')
    factory_out=args.outdir/'factory';subprocess.run([sys.executable,'factory/cognitive_snapshot_adapter_0_8_13.py',str(args.raw),'--outdir',str(factory_out)],check=True)
    manifest=json.loads((factory_out/'analysis_manifest.json').read_text(encoding='utf-8'))
    report.update({'factory_on_exact_stored_raw_executed':True,'analysis_eligible':manifest.get('analysis_eligible'),'blocking_qc_count':manifest.get('blocking_qc_count'),'result':'PASS_EXACT_STORED_RAW_CUSTODY_REPLAY'})
    (args.outdir/'custody_replay_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f"CR0814_STORED_RAW_CUSTODY_PASS sha256={report['observed_sha256']} analysis_eligible={report['analysis_eligible']}")
    return 0
if __name__=='__main__':raise SystemExit(main())
