#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, shutil, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/0.8.14/staging_candidate'
ZIP=ROOT/'artifacts/0.8.14/CUBE-REV_0.8.14_CONTROLLED_STAGING_CANDIDATE.zip'
BASE_COMMIT='6c127f86704b29ed4d884acc19a28407578753c2'
CORE=[
 'participant-cognitive-mode-0.8.14.html','unsupported-browser-0.8.14.html','collector-config.js','js/collector-client.js',
 'js/active-session-cas-0.8.13.js','js/participant-cognitive-mode-0.8.13.js','js/public-asset-verifier-0.8.13.js','js/asset-pins-0.8.13.js',
 'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json','cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json',
 'research/CUBE_REV_0.8.13_ASSET_MANIFEST.json','research/CUBE_REV_0.8.13_DECISION_PACKET.json','research/CUBE_REV_0.8.13_VALIDATION_REPORT.md','research/CUBE_REV_0.8.13_RUNBOOK.md',
 'factory/cognitive_snapshot_adapter_0_8_13.py','factory/archival_live_bridge_0_8_14.py',
 'artifacts/0.8.14/participant_route_build_manifest.json'
]

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def canonical(v)->str:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def main()->None:
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    files=[]
    for rel in CORE:
        src=ROOT/rel
        if not src.is_file():raise FileNotFoundError(rel)
        target_rel='index.html' if rel=='participant-cognitive-mode-0.8.14.html' else rel
        if rel=='artifacts/0.8.14/participant_route_build_manifest.json':target_rel='research/CUBE_REV_0.8.14_PARTICIPANT_ROUTE_BUILD_MANIFEST.json'
        dst=OUT/target_rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
        data=dst.read_bytes();files.append({'source_path':rel,'staging_path':target_rel,'bytes':len(data),'sha256':sha(data)})
    provenance={
      'schema_version':'CR0814-CONTROLLED-STAGING-PROVENANCE-2','project':'CUBE-REV','research_version':'0.8.14',
      'source_branch':'cube-rev-0.8.14-custody-device-staging','parent_certified_commit':BASE_COMMIT,
      'production_default_entry_modified':False,'collector_config_modified':False,'collector_client_modified':False,
      'candidate_entry':'index.html','candidate_release_version':'CUBE-REV 0.8.14','candidate_scientific_runtime_version':'CUBE-REV 0.8.13',
      'browser_policy':{'chromium':'ACTIVE_CERTIFIED_AUTOMATED','webkit':'ACTIVE_CERTIFIED_AUTOMATED','firefox':'FAIL_CLOSED_PENDING_CROSS_TAB_STORAGE_COHERENCE'},
      'deployment_authorized':False,'rollback_target':BASE_COMMIT,'files':sorted(files,key=lambda x:x['staging_path'])
    }
    core=dict(provenance);provenance['candidate_fingerprint_sha256']=sha(canonical(core).encode())
    (OUT/'STAGING_PROVENANCE.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf-8')
    rollback={'schema_version':'CR0814-STAGING-ROLLBACK-PLAN-2','rollback_target_commit':BASE_COMMIT,'rollback_action':'remove_staging_route_or_restore_parent_branch_bytes','production_index_untouched':True,'collector_untouched':True,'automatic_cutover_forbidden':True,'firefox_fail_closed_route':'unsupported-browser-0.8.14.html'}
    (OUT/'ROLLBACK_PLAN.json').write_text(json.dumps(rollback,indent=2),encoding='utf-8')
    ZIP.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(OUT.rglob('*')):
            if not p.is_file():continue
            info=zipfile.ZipInfo(p.relative_to(OUT).as_posix(),date_time=(2026,8,2,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes())
    result={'schema_version':'CR0814-STAGING-BUILD-RESULT-2','candidate_fingerprint_sha256':provenance['candidate_fingerprint_sha256'],'zip_sha256':sha(ZIP.read_bytes()),'zip_bytes':ZIP.stat().st_size,'file_count':len([p for p in OUT.rglob('*') if p.is_file()]),'production_default_entry_modified':False,'collector_modified':False,'firefox_policy':'FAIL_CLOSED','result':'PASS_DETERMINISTIC_STAGING_CANDIDATE_BUILD'}
    (ROOT/'artifacts/0.8.14/staging_build_result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(f"CR0814_STAGING_BUILD_PASS files={result['file_count']} zip_sha256={result['zip_sha256']} fingerprint={result['candidate_fingerprint_sha256']} firefox=FAIL_CLOSED")
if __name__=='__main__':main()
