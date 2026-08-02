#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

EXPECTED_FILE='CR-20260802110000-0813a0b0c0d0.json'
KNOWN_CANDIDATES={
 'archival_live_submission':{'sha256':'6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9','bytes':16217,'checksum':'c8cda746'},
 'final_runtime_counterfactual':{'sha256':'6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3','bytes':21227,'checksum':'f795cd8e'}
}

def sha256(data: bytes)->str:return hashlib.sha256(data).hexdigest()
def fnv1a32(text: str)->str:
    h=0x811C9DC5
    for ch in text:h^=ord(ch);h=(h*0x01000193)&0xffffffff
    return f'{h:08x}'
def classify(fp,bytes_,checksum):
    return [name for name,v in KNOWN_CANDIDATES.items() if (fp,bytes_,checksum)==(v['sha256'],v['bytes'],v['checksum'])]

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=Path('custody')/EXPECTED_FILE);ap.add_argument('--archival-reconstructed',type=Path,default=Path('artifacts/0.8.14/archival_live_envelope.json'));ap.add_argument('--final-reconstructed',type=Path,default=Path('artifacts/0.8.14/final_runtime_envelope.json'));ap.add_argument('--outdir',type=Path,default=Path('artifacts/0.8.14/custody'));args=ap.parse_args();args.outdir.mkdir(parents=True,exist_ok=True)
    reconstructed={}
    for name,p in [('archival_live_submission',args.archival_reconstructed),('final_runtime_counterfactual',args.final_reconstructed)]:
        data=p.read_bytes();obs={'sha256':sha256(data),'bytes':len(data),'checksum':fnv1a32(data.decode('utf-8'))};reconstructed[name]=obs
        if obs!=KNOWN_CANDIDATES[name]:raise RuntimeError(f'RECONSTRUCTION_IDENTITY_MISMATCH:{name}:{obs}')
    report={'schema_version':'CR0814-STORED-RAW-CUSTODY-REPLAY-2','expected_file_name':EXPECTED_FILE,'stored_raw_identity_prior_to_retrieval':'UNKNOWN_BECAUSE_COLLECTOR_DEDUPLICATES_BY_SESSION_FILENAME','known_candidate_fingerprints':KNOWN_CANDIDATES,'reconstructed_candidates':reconstructed,'raw_path':str(args.raw),'direct_drive_raw_available':args.raw.is_file()}
    if not args.raw.is_file():
        report.update({'factory_on_exact_stored_raw_executed':False,'stored_raw_matches':[],'result':'HOLD_DIRECT_STORED_RAW_UNAVAILABLE_TWO_RUNTIME_CANDIDATES_RECONSTRUCTED'})
        (args.outdir/'custody_replay_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('CR0814_STORED_RAW_CUSTODY_HOLD direct_raw=false archival_and_final_candidates=true');return 0
    raw=args.raw.read_bytes();fp=sha256(raw);checksum=fnv1a32(raw.decode('utf-8'));matches=classify(fp,len(raw),checksum);report.update({'observed_sha256':fp,'observed_bytes':len(raw),'observed_checksum_fnv1a32':checksum,'stored_raw_matches':matches})
    factory_out=args.outdir/'factory';subprocess.run([sys.executable,'factory/cognitive_snapshot_adapter_0_8_13.py',str(args.raw),'--outdir',str(factory_out)],check=True)
    manifest=json.loads((factory_out/'analysis_manifest.json').read_text(encoding='utf-8'));report.update({'factory_on_exact_stored_raw_executed':True,'analysis_eligible':manifest.get('analysis_eligible'),'blocking_qc_count':manifest.get('blocking_qc_count'),'result':'PASS_EXACT_STORED_RAW_CUSTODY_REPLAY_KNOWN_CANDIDATE' if matches else 'PASS_EXACT_STORED_RAW_CUSTODY_REPLAY_PREVIOUSLY_UNKNOWN_IDENTITY'})
    (args.outdir/'custody_replay_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(f"CR0814_STORED_RAW_CUSTODY_PASS sha256={fp} matches={','.join(matches) or 'unknown'} analysis_eligible={report['analysis_eligible']}");return 0
if __name__=='__main__':raise SystemExit(main())
