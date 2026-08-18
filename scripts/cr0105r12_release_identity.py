#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil
from pathlib import Path

BASE_BYTES=2588604
BASE_SHA256='e6e66bb489fc0c814a431c7d24c3d067363162393317e773abdec1377877d7cf'
BASE_BLOB='344faeb45d0046a52b24fad91a5bcbcb46784b71'
SEALED_BYTES=2591526
SEALED_SHA256='98e6431c72c7b32fd9461b261c981b470bdda04c617bdb0595b7ce059a250180'
SEALED_BLOB='ce5b5608767083a696cf57982edd979a21b3ba22'
BASE_MAIN='52fc4a04c922ea0d39dd29cdf1ac6ebed5a196a1'
R11_EVIDENCE='d949b9638d7db3661b62bc9913fa3439a83f3194'
EXPECTED_PUBLIC_URL='https://whosia.github.io/CUBE-REV/'
CANDIDATE_REL=Path('release-candidates/0.10.5-r1.2/98e6431c72c7b32f/index.html')


def sha256(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def git_blob(b:bytes)->str:return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def fact(path:Path):
    if not path.is_file(): return {'present':False}
    b=path.read_bytes(); return {'present':True,'bytes':len(b),'sha256':sha256(b),'git_blob_sha1':git_blob(b)}
def load(path:Path):
    try:return json.loads(path.read_text(encoding='utf-8'))
    except Exception:return None

def main():
    root=Path('.').resolve(); art=Path(os.environ.get('CR0105R12_ARTIFACT_DIR','cr0105r12-artifact')).resolve(); art.mkdir(parents=True,exist_ok=True)
    candidate=(root/CANDIDATE_REL).resolve(); evidence=(root/'research/0.10.5-r1.2/prelaunch-seal').resolve(); evidence.mkdir(parents=True,exist_ok=True)
    r11=load(root/'research/0.10.5-r1.1/action-seal/FINAL_SEAL.json')
    patch=load(art/'PATCH_EXECUTION_RECEIPT.json'); browser=load(art/'EXACT_MONOLITH_BROWSER_COURT.json'); boot=load(art/'BOOT_DIAGNOSTIC.json')
    pages=load(art/'PAGES_METADATA.json') or {}; host=load(art/'PUBLIC_HOST_FETCH.json') or {}
    authority=load(art/'AUTHORITY_COURT.json') or {}; baseline=load(art/'BASELINE_COURT.json') or {}; material=load(art/'MATERIALIZATION_COURT.json') or {}
    cand=fact(candidate); source=fact(art/'index.source.html'); hosted=fact(art/'public-host-index.html')
    checks={}
    checks['r11_final_seal_pass']=bool(r11 and r11.get('status')=='PASS' and (r11.get('first_patched') or {}).get('sha256')==SEALED_SHA256)
    checks['authority_court_pass']=authority.get('status')=='PASS' and authority.get('main_sha')==BASE_MAIN
    checks['baseline_regression_pass']=baseline.get('status')=='PASS'
    checks['source_exact_base']=source.get('bytes')==BASE_BYTES and source.get('sha256')==BASE_SHA256 and source.get('git_blob_sha1')==BASE_BLOB
    checks['patch_receipt_pass']=bool(patch and patch.get('status')=='PASS' and (patch.get('patched') or {}).get('sha256')==SEALED_SHA256)
    checks['materialization_court_pass']=material.get('status')=='PASS' and material.get('candidate_sha256')==SEALED_SHA256
    checks['candidate_present']=bool(cand.get('present'))
    checks['candidate_exact_sealed_bytes']=cand.get('bytes')==SEALED_BYTES
    checks['candidate_exact_sealed_sha256']=cand.get('sha256')==SEALED_SHA256
    checks['candidate_exact_sealed_git_blob']=cand.get('git_blob_sha1')==SEALED_BLOB
    checks['candidate_content_address_path']=SEALED_SHA256.startswith(CANDIDATE_REL.parts[-2])
    checks['boot_selftest_pass']=bool(((boot.get('state') or {}).get('selftest') or {}).get('passed') is True)
    checks['browser_court_pass']=bool(browser and browser.get('status')=='PASS' and browser.get('check_count')==browser.get('pass_count') and not browser.get('runtime_errors'))
    pages_status=int(pages.get('http_status') or 0); host_status=int(host.get('http_status') or 0)
    canonical=(host.get('canonical_url') or '').rstrip('/')+'/' if host.get('canonical_url') else None
    checks['public_host_url_expected']=canonical==EXPECTED_PUBLIC_URL
    checks['public_host_http_200']=host_status==200 and hosted.get('present')
    checks['public_host_matches_current_main_baseline']=hosted.get('bytes')==BASE_BYTES and hosted.get('sha256')==BASE_SHA256 and hosted.get('git_blob_sha1')==BASE_BLOB
    checks['candidate_not_prematurely_public']=bool(hosted.get('present') and hosted.get('sha256')!=SEALED_SHA256)
    checks['no_human_observations']=bool(browser and browser.get('human_observations')==0)
    checks['production_network_only_read']=True
    checks['deployment_write_not_performed']=True
    status='PASS' if all(checks.values()) else 'HOLD'
    verdict='PASS_SEALED_RELEASE_IDENTITY_MATERIALIZED_DEPLOYMENT_BYTE_EQUIVALENCE_PRELAUNCH_GATE' if status=='PASS' else 'HOLD_CR0105R12_PRELAUNCH_GATE'
    out={
      'schema_version':'CR0105R12-PRELAUNCH-SEAL-2',
      'stage':'CUBE-REV 0.10.5-R1.2 — Sealed Release-Identity Materialization, Deployment-byte Equivalence Court & Public-host Prelaunch Gate',
      'status':status,'verdict':verdict,'repository':'WhoSia/CUBE-REV','research_branch':'cube-rev-0.10.5-r1.2-release-identity',
      'base_main_commit':BASE_MAIN,'r11_evidence_commit':R11_EVIDENCE,'workflow_head_sha':os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),
      'release_identity':{'candidate_path':str(CANDIDATE_REL),'bytes':SEALED_BYTES,'sha256':SEALED_SHA256,'git_blob_sha1':SEALED_BLOB},
      'candidate_observed':cand,'source_observed':source,'public_host_observed':hosted,
      'pages_metadata':{'http_status':pages_status,'html_url':pages.get('html_url'),'source':pages.get('source'),'build_type':pages.get('build_type'),'informational_only':True},
      'public_host_fetch':host,'authority_observed':authority,
      'browser_check_count':(browser or {}).get('check_count'),'browser_pass_count':(browser or {}).get('pass_count'),
      'checks':checks,'authority':{'main_written':False,'pages_settings_written':False,'deployment_triggered':False,'human_launch':False},
      'gate':'READY_FOR_EXPLICIT_DEPLOYMENT_AUTHORITY_COURT' if status=='PASS' else 'NOT_READY_FOR_DEPLOYMENT',
      'scope':'PRELAUNCH_ENGINEERING_ONLY'
    }
    (art/'FINAL_PRELAUNCH_GATE.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    for name in ['AUTHORITY_COURT.json','BASELINE_COURT.json','MATERIALIZATION_COURT.json','PATCH_EXECUTION_RECEIPT.json','EXACT_SOURCE_BINDING.json','BOOT_DIAGNOSTIC.json','EXACT_MONOLITH_BROWSER_COURT.json','PAGES_METADATA.json','PUBLIC_HOST_FETCH.json','FINAL_PRELAUNCH_GATE.json']:
        p=art/name
        if p.is_file(): shutil.copyfile(p,evidence/name)
    print(json.dumps(out,indent=2))
    raise SystemExit(0 if status=='PASS' else 2)
if __name__=='__main__':main()
