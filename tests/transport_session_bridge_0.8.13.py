from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('cr0813_factory_bridge',ROOT/'factory/cognitive_snapshot_adapter_0_8_13.py')
if SPEC is None or SPEC.loader is None:
    raise SystemExit('FACTORY_MODULE_SPEC_UNAVAILABLE')
MOD=importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name]=MOD
SPEC.loader.exec_module(MOD)

path=ROOT/'artifacts/0.8.13/native_snapshot.json'
if not path.exists():
    raise SystemExit('NATIVE_SNAPSHOT_MISSING')
root=json.loads(path.read_text(encoding='utf-8'))
snapshot=root.get('cognitive_snapshot')
if not isinstance(snapshot,dict):
    raise SystemExit('NATIVE_ENVELOPE_INNER_SNAPSHOT_MISSING')
expected=MOD.transport_identity(snapshot)
actual={
    'session_id':root.get('session_id'),
    'original_scientific_session_id':root.get('original_scientific_session_id'),
    'transport_session_policy':root.get('transport_session_policy'),
}
seed=f"{snapshot.get('session_id')}|{snapshot.get('participant_token') or ''}|{snapshot.get('sequence_id') or ''}"
report={
    'schema_version':'CR0813-TRANSPORT-BRIDGE-PARITY-1',
    'scientific_session_id':snapshot.get('session_id'),
    'started_at':snapshot.get('started_at'),
    'scientific_completed_at':snapshot.get('scientific_completed_at'),
    'participant_token':snapshot.get('participant_token'),
    'sequence_id':snapshot.get('sequence_id'),
    'seed':seed,
    'checksum_a':MOD.checksum_text(seed+'|A'),
    'checksum_b':MOD.checksum_text(seed+'|B'),
    'actual':actual,
    'expected':expected,
    'passed':actual==expected,
}
out=ROOT/'artifacts/0.8.13/transport_session_bridge_parity.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('CR0813_TRANSPORT_BRIDGE_PARITY '+json.dumps(report,ensure_ascii=False,separators=(',',':')))
if actual!=expected:
    raise SystemExit('TRANSPORT_BRIDGE_PARITY_MISMATCH')
