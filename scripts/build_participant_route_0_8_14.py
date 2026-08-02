#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'participant-cognitive-mode-0.8.13.html'
TARGET=ROOT/'participant-cognitive-mode-0.8.14.html'
UNSUPPORTED=ROOT/'unsupported-browser-0.8.14.html'
MANIFEST=ROOT/'artifacts/0.8.14/participant_route_build_manifest.json'

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def main()->None:
    source=SOURCE.read_text(encoding='utf-8')
    required=['<title>CUBE-REV 0.8.13</title>','<body>','CUBE-REV 0.8.13']
    for token in required:
        if token not in source:raise RuntimeError(f'PARENT_ROUTE_TOKEN_MISSING:{token}')
    gate="""<script id=\"cr0814-browser-gate\">(function(){'use strict';const ua=navigator.userAgent;const firefox=/Firefox\\//.test(ua);const ios=/(iPhone|iPad|iPod)/.test(ua);const chromium=/(Chrome|Chromium|Edg|OPR)\\//.test(ua);const desktopWebKit=/AppleWebKit\\//.test(ua)&&!ios&&!chromium&&!firefox;const reason=firefox?'FIREFOX_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED':desktopWebKit?'DESKTOP_WEBKIT_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED':null;const gate={schema_version:'CR0814-BROWSER-CAPABILITY-GATE-2',release_version:'CUBE-REV 0.8.14',scientific_runtime_version:'CUBE-REV 0.8.13',engine_policy:reason?`FAIL_CLOSED_${reason}`:'ACTIVE_ALLOWED',status:reason?'REDIRECTING_TO_UNSUPPORTED':'ACTIVE_ALLOWED',reason,user_agent:ua};window.CUBE_REV_0814_BROWSER_GATE=Object.freeze(gate);if(reason)location.replace(`unsupported-browser-0.8.14.html?reason=${encodeURIComponent(reason)}`);})();</script>"""
    target=source.replace('<title>CUBE-REV 0.8.13</title>','<title>CUBE-REV 0.8.14 — Controlled Staging</title>',1)
    target=target.replace('<body>','<body>'+gate,1)
    target=target.replace('<p class="small">CUBE-REV 0.8.13</p>','<p class="small">CUBE-REV 0.8.14 · Controlled staging · scientific runtime 0.8.13</p>')
    target=target.replace('<main>','<main><p id="stagingBanner" class="small warning">CUBE-REV 0.8.14 controlled staging — production 기본 진입점이 아닙니다.</p>',1)
    unsupported="""<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>CUBE-REV 0.8.14 — 지원 확인 필요</title><style>body{margin:0;background:#f5f7fa;font-family:system-ui,-apple-system,\"Noto Sans KR\",sans-serif;color:#17191d}main{max-width:720px;margin:8vh auto;padding:24px}.card{background:#fff;border:1px solid #d9dee7;border-radius:18px;padding:28px}.small{font-size:13px;color:#68707b}.warning{color:#8a4b00}</style></head><body><main><section class=\"card\"><h1>이 브라우저에서는 과제를 시작하지 않았습니다</h1><p id=\"reasonText\" class=\"warning\">여러 창 저장 일관성이 현재 staging 인증에서 안전하게 확인되지 않았습니다.</p><p>Chrome 또는 Edge 계열 브라우저를 사용해 주세요. iPhone·iPad의 Safari는 자동화된 staging 범위에 포함되지만 실제 기기 인증은 아직 완료되지 않았습니다. 기존 응답과 저장 상태는 변경하지 않았습니다.</p><p id=\"reasonCode\" class=\"small\">CUBE-REV 0.8.14 · FAIL-CLOSED-CROSS-TAB-COHERENCE</p></section></main><script>(function(){'use strict';const raw=new URLSearchParams(location.search).get('reason')||'UNSUPPORTED_BROWSER_POLICY';const allowed=new Set(['FIREFOX_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED','DESKTOP_WEBKIT_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED']);const reason=allowed.has(raw)?raw:'UNSUPPORTED_BROWSER_POLICY';const descriptions={FIREFOX_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED:'Firefox의 여러 창 저장 일관성은 현재 staging 인증에서 안전하게 확인되지 않았습니다.',DESKTOP_WEBKIT_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED:'desktop WebKit 계열의 여러 창 저장 일관성은 현재 staging 인증에서 안전하게 확인되지 않았습니다.',UNSUPPORTED_BROWSER_POLICY:'이 브라우저의 여러 창 저장 일관성은 현재 staging 인증 범위에 포함되지 않았습니다.'};document.getElementById('reasonText').textContent=descriptions[reason];document.getElementById('reasonCode').textContent=`CUBE-REV 0.8.14 · FAIL-CLOSED-${reason}`;window.CUBE_REV_0814_BROWSER_GATE=Object.freeze({schema_version:'CR0814-BROWSER-CAPABILITY-GATE-2',release_version:'CUBE-REV 0.8.14',status:'BLOCKED',reason,state_mutation_authorized:false});})();</script></body></html>"""
    TARGET.write_text(target,encoding='utf-8');UNSUPPORTED.write_text(unsupported,encoding='utf-8')
    MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    manifest={'schema_version':'CR0814-PARTICIPANT-ROUTE-BUILD-2','source_path':SOURCE.name,'source_sha256':sha(SOURCE.read_bytes()),'target_path':TARGET.name,'target_sha256':sha(TARGET.read_bytes()),'unsupported_path':UNSUPPORTED.name,'unsupported_sha256':sha(UNSUPPORTED.read_bytes()),'visible_release_version':'CUBE-REV 0.8.14','scientific_runtime_version':'CUBE-REV 0.8.13','browser_policy':{'chromium_desktop_and_mobile':'ACTIVE_AUTOMATED','ios_webkit_emulation':'ACTIVE_AUTOMATED','firefox':'FAIL_CLOSED_BEFORE_SESSION_BOOT','desktop_webkit':'FAIL_CLOSED_BEFORE_SESSION_BOOT'},'physical_device_certified':False,'production_default_entry_modified':False,'result':'PASS_DETERMINISTIC_STAGING_ROUTE_BUILD'}
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"CR0814_PARTICIPANT_ROUTE_BUILD_PASS target={manifest['target_sha256']} unsupported={manifest['unsupported_sha256']} firefox=FAIL_CLOSED desktop_webkit=FAIL_CLOSED")
if __name__=='__main__':main()
