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
    gate="""<script id=\"cr0814-browser-gate\">(function(){'use strict';const firefox=/Firefox\\//.test(navigator.userAgent);const gate={schema_version:'CR0814-BROWSER-CAPABILITY-GATE-1',release_version:'CUBE-REV 0.8.14',scientific_runtime_version:'CUBE-REV 0.8.13',engine_policy:firefox?'FIREFOX_FAIL_CLOSED_PENDING_CROSS_TAB_STORAGE_COHERENCE':'ACTIVE_ALLOWED',status:firefox?'REDIRECTING_TO_UNSUPPORTED':'ACTIVE_ALLOWED',user_agent:navigator.userAgent};window.CUBE_REV_0814_BROWSER_GATE=Object.freeze(gate);if(firefox)location.replace('unsupported-browser-0.8.14.html?reason=firefox-cross-tab-coherence');})();</script>"""
    target=source.replace('<title>CUBE-REV 0.8.13</title>','<title>CUBE-REV 0.8.14 — Controlled Staging</title>',1)
    target=target.replace('<body>','<body>'+gate,1)
    target=target.replace('<p class="small">CUBE-REV 0.8.13</p>','<p class="small">CUBE-REV 0.8.14 · Controlled staging · scientific runtime 0.8.13</p>')
    target=target.replace('<main>','<main><p id="stagingBanner" class="small warning">CUBE-REV 0.8.14 controlled staging — production 기본 진입점이 아닙니다.</p>',1)
    unsupported="""<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>CUBE-REV 0.8.14 — 지원 확인 필요</title><style>body{margin:0;background:#f5f7fa;font-family:system-ui,-apple-system,\"Noto Sans KR\",sans-serif;color:#17191d}main{max-width:720px;margin:8vh auto;padding:24px}.card{background:#fff;border:1px solid #d9dee7;border-radius:18px;padding:28px}.small{font-size:13px;color:#68707b}.warning{color:#8a4b00}</style></head><body><main><section class=\"card\"><h1>이 브라우저에서는 과제를 시작하지 않았습니다</h1><p class=\"warning\">Firefox의 여러 창 저장 일관성은 현재 staging 인증에서 안전하게 확인되지 않았습니다.</p><p>Chrome, Edge 또는 Safari 계열 브라우저에서 다시 열어 주세요. 기존 응답과 저장 상태는 변경하지 않았습니다.</p><p class=\"small\">CUBE-REV 0.8.14 · FAIL-CLOSED-FIREFOX-CROSS-TAB-COHERENCE</p></section></main><script>window.CUBE_REV_0814_BROWSER_GATE=Object.freeze({schema_version:'CR0814-BROWSER-CAPABILITY-GATE-1',release_version:'CUBE-REV 0.8.14',status:'BLOCKED',reason:'FIREFOX_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED',state_mutation_authorized:false});</script></body></html>"""
    TARGET.write_text(target,encoding='utf-8');UNSUPPORTED.write_text(unsupported,encoding='utf-8')
    MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    manifest={'schema_version':'CR0814-PARTICIPANT-ROUTE-BUILD-1','source_path':SOURCE.name,'source_sha256':sha(SOURCE.read_bytes()),'target_path':TARGET.name,'target_sha256':sha(TARGET.read_bytes()),'unsupported_path':UNSUPPORTED.name,'unsupported_sha256':sha(UNSUPPORTED.read_bytes()),'visible_release_version':'CUBE-REV 0.8.14','scientific_runtime_version':'CUBE-REV 0.8.13','firefox_policy':'FAIL_CLOSED_BEFORE_SESSION_BOOT','production_default_entry_modified':False,'result':'PASS_DETERMINISTIC_STAGING_ROUTE_BUILD'}
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"CR0814_PARTICIPANT_ROUTE_BUILD_PASS target={manifest['target_sha256']} unsupported={manifest['unsupported_sha256']} firefox=FAIL_CLOSED")
if __name__=='__main__':main()
