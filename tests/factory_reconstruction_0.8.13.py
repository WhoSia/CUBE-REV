from __future__ import annotations
import csv
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('cr0813_factory',ROOT/'factory/cognitive_snapshot_adapter_0_8_13.py')
if SPEC is None or SPEC.loader is None:
    raise SystemExit('FACTORY_MODULE_SPEC_UNAVAILABLE')
MOD=importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name]=MOD
SPEC.loader.exec_module(MOD)
source=ROOT/'artifacts/0.8.13/live_synthetic_snapshot.json'
if not source.exists():
    raise SystemExit('SYNTHETIC_SNAPSHOT_MISSING')

def canonical(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf-8')

def make_wrapper(snapshot):
    identity=MOD.transport_identity(snapshot)
    return {
        'project':'CUBE-REV','version':'0.7.12','session_id':identity['session_id'],
        'original_scientific_session_id':identity['original_scientific_session_id'],
        'transport_session_policy':identity['transport_session_policy'],
        'generated_at':snapshot['scientific_completed_at'],
        'trials':[
            {
                'trial_index':r['position'],'trial_id':f"CR0813-COMPAT-{r['position']:02d}",
                'condition_id':snapshot['mode_id'],'stimulus_id':r['stimulus_id'],
                'response':{'choice_display':r['choice_display'],'choice_code':r['choice_code'],'latency_ms':r['latency_ms'],'recorded_at':r['recorded_at']},
                'status':'completed','source_schema':snapshot['schema_version'],'scientific_revision':snapshot['scientific_revision']
            } for r in snapshot['responses']
        ],
        'data_submission':{
            'status':'engineering_synthetic_live_cert','synthetic_live_cert':True,'exclude_from_human_cohort':True,
            'app_payload_version':snapshot['version'],'app_payload_schema':snapshot['schema_version'],
            'collector_compatibility_schema':'CR0813-COLLECTOR-COMPATIBILITY-ENVELOPE-1',
            'compatibility_trial_policy':'LOSSLESS_OPAQUE_RESPONSE_PROJECTION_V1',
            'original_scientific_session_id':identity['original_scientific_session_id'],
            'transport_session_id':identity['session_id'],
            'transport_session_policy':identity['transport_session_policy'],
            'immutable_snapshot_sha256':hashlib.sha256(canonical(snapshot)).hexdigest()
        },
        'cognitive_snapshot':snapshot
    }

def must_reject(value,path,label):
    path.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    try:
        MOD.adapt(path,path.parent/(label+'-out'))
    except MOD.FactoryError as exc:
        assert 'BLOCKING_QC' in str(exc) or 'COLLECTOR_ENVELOPE' in str(exc)
    else:
        raise AssertionError(label+'_ACCEPTED')

snapshot=json.loads(source.read_text(encoding='utf-8'))
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    inner_out=td/'inner-out';inner_manifest=MOD.adapt(source,inner_out)
    assert inner_manifest['analysis_eligible'] is True
    assert inner_manifest['blocking_qc_count']==0
    assert inner_manifest['source']['root_kind']=='inner_scientific_snapshot'
    with (inner_out/'trial_table.csv').open(encoding='utf-8-sig',newline='') as f:
        inner_rows=list(csv.DictReader(f))
    assert len(inner_rows)==28
    assert [int(r['position']) for r in inner_rows]==list(range(1,29))
    assert all(r['choice_code'].startswith('CR9C-') for r in inner_rows)
    assert (inner_out/'raw'/source.name).read_bytes()==source.read_bytes()

    wrapper=make_wrapper(snapshot)
    identity=MOD.transport_identity(snapshot)
    wrapper_path=td/'collector-wrapper.json'
    wrapper_bytes=json.dumps(wrapper,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    wrapper_path.write_bytes(wrapper_bytes)
    wrapper_out=td/'wrapper-out';wrapper_manifest=MOD.adapt(wrapper_path,wrapper_out)
    assert wrapper_manifest['analysis_eligible'] is True
    assert wrapper_manifest['blocking_qc_count']==0
    assert wrapper_manifest['source']['root_kind']=='collector_compatibility_envelope'
    envelope_info=wrapper_manifest['source']['collector_envelope']
    assert envelope_info['trial_count']==28
    assert envelope_info['exclude_from_human_cohort'] is True
    assert envelope_info['session_id']==identity['session_id']
    assert envelope_info['scientific_session_id']==snapshot['session_id']
    assert envelope_info['transport_session_policy']==identity['transport_session_policy']
    assert (wrapper_out/'raw'/wrapper_path.name).read_bytes()==wrapper_bytes
    with (wrapper_out/'trial_table.csv').open(encoding='utf-8-sig',newline='') as f:
        wrapper_rows=list(csv.DictReader(f))
    assert wrapper_rows==inner_rows
    with (wrapper_out/'session_table.csv').open(encoding='utf-8-sig',newline='') as f:
        session_row=list(csv.DictReader(f))[0]
    assert session_row['scientific_session_id']==snapshot['session_id']
    assert session_row['transport_session_id']==identity['session_id']

    bad_inner=json.loads(source.read_text())
    bad_inner['responses'][2]['position']=9
    must_reject(bad_inner,td/'bad-inner.json','TAMPERED_INNER_POSITION')

    bad_projection=json.loads(json.dumps(wrapper))
    bad_projection['trials'][4]['response']['choice_code']='CR9C-0000000000000000'
    must_reject(bad_projection,td/'bad-projection.json','TAMPERED_COMPAT_PROJECTION')

    bad_session=json.loads(json.dumps(wrapper))
    bad_session['session_id']='CR-20260802110001-0813a0b0c0d1'
    must_reject(bad_session,td/'bad-session.json','MISMATCHED_TRANSPORT_SESSION')

    bad_original=json.loads(json.dumps(wrapper))
    bad_original['original_scientific_session_id']='CR088-FORGED-SCIENTIFIC-SESSION'
    must_reject(bad_original,td/'bad-original.json','MISMATCHED_SCIENTIFIC_SESSION')

    bad_policy=json.loads(json.dumps(wrapper))
    bad_policy['transport_session_policy']='IDENTITY_SESSION_V1' if identity['transport_session_policy']!='IDENTITY_SESSION_V1' else 'DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1'
    must_reject(bad_policy,td/'bad-policy.json','MISMATCHED_TRANSPORT_POLICY')

print(f"CR0813_FACTORY_ADAPTER_TEST_PASS inner_rows=28 wrapper_rows=28 tamper_cases=5 bridge={identity['transport_session_policy']}")
