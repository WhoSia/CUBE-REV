#!/usr/bin/env python3
"""Bridge the pinned pre-transport 0.8.13 live envelope into the final Factory contract.

The source bytes are never modified. Only the single preserved engineering
live-probe identity is accepted. A derived JSON adds identity-session metadata
that was semantically implicit at the time, while a provenance report binds
source and derived hashes.
"""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path

SOURCE_SHA='6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9'
SOURCE_BYTES=16217
SOURCE_FNV='c8cda746'
SESSION='CR-20260802110000-0813a0b0c0d0'
POLICY='IDENTITY_SESSION_V1'

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def fnv(text:str)->str:
    h=0x811C9DC5
    for ch in text:h^=ord(ch);h=(h*0x01000193)&0xffffffff
    return f'{h:08x}'
def canonical(v)->bytes:return json.dumps(v,ensure_ascii=False,separators=(',',':')).encode('utf-8')
def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--derived',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
    raw=a.source.read_bytes();text=raw.decode('utf-8');identity={'sha256':sha(raw),'bytes':len(raw),'checksum_fnv1a32':fnv(text)}
    if identity!={'sha256':SOURCE_SHA,'bytes':SOURCE_BYTES,'checksum_fnv1a32':SOURCE_FNV}:raise RuntimeError(f'ARCHIVAL_SOURCE_IDENTITY_MISMATCH:{identity}')
    root=json.loads(text);snap=root.get('cognitive_snapshot');ds=root.get('data_submission')
    if not isinstance(snap,dict) or not isinstance(ds,dict):raise RuntimeError('ARCHIVAL_STRUCTURE_INVALID')
    if root.get('project')!='CUBE-REV' or root.get('version')!='0.7.12':raise RuntimeError('ARCHIVAL_COLLECTOR_IDENTITY_INVALID')
    if root.get('session_id')!=SESSION or snap.get('session_id')!=SESSION:raise RuntimeError('ARCHIVAL_SESSION_IDENTITY_INVALID')
    if root.get('original_scientific_session_id') is not None or root.get('transport_session_policy') is not None:raise RuntimeError('ARCHIVAL_ALREADY_BRIDGED')
    if any(ds.get(k) is not None for k in ['original_scientific_session_id','transport_session_id','transport_session_policy']):raise RuntimeError('ARCHIVAL_DATA_SUBMISSION_ALREADY_BRIDGED')
    derived=copy.deepcopy(root);derived['original_scientific_session_id']=SESSION;derived['transport_session_policy']=POLICY
    derived_ds=derived['data_submission'];derived_ds['original_scientific_session_id']=SESSION;derived_ds['transport_session_id']=SESSION;derived_ds['transport_session_policy']=POLICY
    derived_raw=canonical(derived);a.derived.parent.mkdir(parents=True,exist_ok=True);a.report.parent.mkdir(parents=True,exist_ok=True);a.derived.write_bytes(derived_raw)
    report={'schema_version':'CR0814-ARCHIVAL-LIVE-FACTORY-BRIDGE-1','bridge_policy':'ADD_EXPLICIT_IDENTITY_SESSION_METADATA_WITHOUT_SCIENTIFIC_MUTATION','source':{'path':str(a.source),**identity},'derived':{'path':str(a.derived),'sha256':sha(derived_raw),'bytes':len(derived_raw),'checksum_fnv1a32':fnv(derived_raw.decode('utf-8'))},'added_fields':{'original_scientific_session_id':SESSION,'transport_session_policy':POLICY,'data_submission.original_scientific_session_id':SESSION,'data_submission.transport_session_id':SESSION,'data_submission.transport_session_policy':POLICY},'source_snapshot_sha256':sha(canonical(snap)),'derived_snapshot_sha256':sha(canonical(derived['cognitive_snapshot'])),'scientific_snapshot_unchanged':canonical(snap)==canonical(derived['cognitive_snapshot']),'result':'PASS_PINNED_ARCHIVAL_LIVE_FACTORY_BRIDGE'}
    if not report['scientific_snapshot_unchanged']:raise RuntimeError('SCIENTIFIC_SNAPSHOT_MUTATED')
    a.report.write_text(json.dumps(report,indent=2),encoding='utf-8');print(f"CR0814_ARCHIVAL_FACTORY_BRIDGE_PASS source={identity['sha256']} derived={report['derived']['sha256']} scientific_unchanged=true");return 0
if __name__=='__main__':raise SystemExit(main())
