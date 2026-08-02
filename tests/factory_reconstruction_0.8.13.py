from __future__ import annotations
import csv
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('cr0813_factory',ROOT/'factory/cognitive_snapshot_adapter_0_8_13.py')
MOD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MOD)
source=ROOT/'artifacts/0.8.13/live_synthetic_snapshot.json'
if not source.exists():
    raise SystemExit('SYNTHETIC_SNAPSHOT_MISSING')
with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'out';manifest=MOD.adapt(source,out)
    assert manifest['analysis_eligible'] is True
    assert manifest['blocking_qc_count']==0
    with (out/'trial_table.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==28
    assert [int(r['position']) for r in rows]==list(range(1,29))
    assert (out/'raw'/source.name).read_bytes()==source.read_bytes()
    tampered=json.loads(source.read_text())
    tampered['responses'][2]['position']=9
    bad=Path(td)/'bad.json';bad.write_text(json.dumps(tampered))
    try:
        MOD.adapt(bad,Path(td)/'bad-out')
    except MOD.FactoryError as exc:
        assert 'BLOCKING_QC' in str(exc)
    else:
        raise AssertionError('TAMPERED_SNAPSHOT_ACCEPTED')
print('CR0813_FACTORY_ADAPTER_TEST_PASS rows=28 tamper_rejected=true')
