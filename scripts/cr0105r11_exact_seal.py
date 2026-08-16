#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path

EXPECTED_BYTES=2588604
EXPECTED_SHA256='e6e66bb489fc0c814a431c7d24c3d067363162393317e773abdec1377877d7cf'
EXPECTED_BLOB='344faeb45d0046a52b24fad91a5bcbcb46784b71'
EXPECTED_VERSION="const VERSION = '0.7.12';"
CACHE_KEY='0712-camera-neutral-bypass-hotfix-1'
ZOOM_ANCHOR=f'<script src="./js/camera-zoom-controller.js?v={CACHE_KEY}"></script>'
MARKER='CR0105R1-NATURALISTIC-TELEMETRY-INTEGRATION'
SCRIPT=f'<script src="./js/naturalistic-telemetry-v0105-r1.js?v={CACHE_KEY}"></script><!-- {MARKER} -->'
LOG_ANCHOR="function logSessionEvent(type,extra={}){\n  if(!session)return null;"
LOG_HOOK="function logSessionEvent(type,extra={}){\n  // CR0105R1 additive telemetry decorator; no puzzle/camera mutation.\n  if(String(type).startsWith('camera_')&&globalThis.CubeRevNaturalisticTelemetry0105R1){\n    extra=globalThis.CubeRevNaturalisticTelemetry0105R1.decorateCameraPayload(type,extra,()=>camera,CubeRevCameraOrbit);\n  }\n  if(!session)return null;"

def sha256(b): return hashlib.sha256(b).hexdigest()
def git_blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def fail(msg): raise SystemExit('CR0105R11_FAIL: '+msg)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--artifact-dir',required=True); a=ap.parse_args()
    root=Path(a.root).resolve(); art=Path(a.artifact_dir).resolve(); art.mkdir(parents=True,exist_ok=True)
    src=(root/'index.html').read_bytes()
    source={'bytes':len(src),'sha256':sha256(src),'git_blob_sha1':git_blob(src)}
    if source['bytes']!=EXPECTED_BYTES: fail(f"source byte length {source['bytes']} != {EXPECTED_BYTES}")
    if source['sha256']!=EXPECTED_SHA256: fail(f"source sha256 {source['sha256']} != {EXPECTED_SHA256}")
    if source['git_blob_sha1']!=EXPECTED_BLOB: fail(f"source blob {source['git_blob_sha1']} != {EXPECTED_BLOB}")
    text=src.decode('utf-8')
    if EXPECTED_VERSION not in text: fail('VERSION anchor missing')
    if text.count(ZOOM_ANCHOR)!=1: fail(f'zoom anchor count {text.count(ZOOM_ANCHOR)}')
    if text.count(LOG_ANCHOR)!=1: fail(f'logger anchor count {text.count(LOG_ANCHOR)}')
    if MARKER in text: fail('source unexpectedly already patched')
    shutil.copyfile(root/'index.html',art/'index.source.html')
    tel_src=root/'js/naturalistic-telemetry-v0105-r1.js'
    if not tel_src.is_file(): fail('telemetry module missing')
    tel=tel_src.read_bytes(); shutil.copyfile(tel_src,art/'naturalistic-telemetry-v0105-r1.js')
    patched=text.replace(ZOOM_ANCHOR,ZOOM_ANCHOR+'\n'+SCRIPT,1).replace(LOG_ANCHOR,LOG_HOOK,1).encode('utf-8')
    (root/'index.html').write_bytes(patched); (art/'index.patched.html').write_bytes(patched)
    reread=(root/'index.html').read_bytes()
    if reread!=patched: fail('post-write byte mismatch')
    ptxt=reread.decode('utf-8')
    if ptxt.count(MARKER)!=1 or ptxt.count('CubeRevNaturalisticTelemetry0105R1.decorateCameraPayload')!=1: fail('patch markers not singleton')
    if ptxt.count(f'?v={CACHE_KEY}') < 1 or '?v=0105r1' in ptxt: fail('cache-key parity violation')
    receipt={
      'schema_version':'CR0105R11-EXACT-SOURCE-PATCH-2','status':'PASS',
      'source_expected':{'bytes':EXPECTED_BYTES,'sha256':EXPECTED_SHA256,'git_blob_sha1':EXPECTED_BLOB},
      'source_observed':source,
      'telemetry':{'bytes':len(tel),'sha256':sha256(tel),'git_blob_sha1':git_blob(tel)},
      'patched':{'bytes':len(reread),'sha256':sha256(reread),'git_blob_sha1':git_blob(reread),'additive_bytes':len(reread)-len(src)},
      'cache_key':CACHE_KEY,
      'checks':{
        'source_exact_byte_length':True,'source_exact_sha256':True,'source_exact_git_blob':True,
        'source_version_anchor':True,'zoom_anchor_singleton':True,'logger_anchor_singleton':True,
        'source_unpatched_before_execution':True,'post_write_byte_identity':True,'patch_marker_singleton':True,
        'logger_hook_singleton':True,'source_backup_exact':(art/'index.source.html').read_bytes()==src,
        'release_cache_key_preserved':True
      },
      'human_observations':0,'production_mutated':False
    }
    (art/'PATCH_EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    (art/'EXACT_SOURCE_BINDING.json').write_text(json.dumps({'schema_version':'CR0105R11-SOURCE-BINDING-1','repository':'WhoSia/CUBE-REV','base_main_commit':'52fc4a04c922ea0d39dd29cdf1ac6ebed5a196a1','index':source,'status':'PASS'},indent=2),encoding='utf-8')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__': main()
