#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil, sys
from pathlib import Path

EXPECTED_BYTES = 2588604
EXPECTED_SHA256 = 'e6e66bb489fc0c814a431c7d24c3d067363162393317e773abdec1377877d7cf'
EXPECTED_BLOB = '344faeb45d0046a52b24fad91a5bcbcb46784b71'
PASS_VERDICT = 'PASS_EXACT_MONOLITH_BYTE_RECOVERY_SOURCE_BOUND_PATCH_BINARY_IDENTICAL_WHOLE_PAGE_SEAL'
FAIL_VERDICT = 'HOLD_CR0105R11_EXACT_MONOLITH_SEAL'


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob(b: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def file_fact(path: Path):
    if not path.is_file():
        return {'present': False}
    b = path.read_bytes()
    return {
        'present': True,
        'bytes': len(b),
        'sha256': sha256(b),
        'git_blob_sha1': git_blob(b),
    }


def main() -> int:
    art = Path(os.environ.get('CR0105R11_ARTIFACT_DIR', 'cr0105r11-artifact')).resolve()
    out = Path(os.environ.get('CR0105R11_EVIDENCE_DIR', 'research/0.10.5-r1.1/action-seal')).resolve()
    out.mkdir(parents=True, exist_ok=True)

    source_path = art / 'index.source.html'
    first_path = art / 'index.patched.first.html'
    second_path = art / 'rebuild2' / 'index.patched.html'
    source = file_fact(source_path)
    first = file_fact(first_path)
    second = file_fact(second_path)

    patch = read_json(art / 'PATCH_EXECUTION_RECEIPT.json')
    rebuild = read_json(art / 'DETERMINISTIC_REBUILD.json')
    browser = read_json(art / 'EXACT_MONOLITH_BROWSER_COURT.json')
    boot = read_json(art / 'BOOT_DIAGNOSTIC.json')
    baseline = read_json(art / 'BASELINE_VALIDATION.json')

    checks = {}
    checks['source_present'] = bool(source.get('present'))
    checks['source_exact_bytes'] = source.get('bytes') == EXPECTED_BYTES
    checks['source_exact_sha256'] = source.get('sha256') == EXPECTED_SHA256
    checks['source_exact_git_blob'] = source.get('git_blob_sha1') == EXPECTED_BLOB
    checks['patch_receipt_pass'] = bool(patch and patch.get('status') == 'PASS')
    checks['baseline_validation_pass'] = bool(baseline and baseline.get('status') == 'PASS')
    checks['first_patch_present'] = bool(first.get('present'))
    checks['second_patch_present'] = bool(second.get('present'))
    checks['patched_byte_identical'] = bool(first.get('present') and second.get('present') and first == second)
    checks['deterministic_rebuild_receipt_pass'] = bool(rebuild and rebuild.get('status') == 'PASS' and rebuild.get('byte_identical') is True)
    boot_state = (boot or {}).get('state') or {}
    boot_selftest = boot_state.get('selftest') or {}
    checks['boot_selftest_pass'] = bool(boot_selftest.get('passed') is True)
    checks['boot_no_pageerror'] = bool(boot is not None and not boot.get('pageerror'))
    checks['browser_court_pass'] = bool(browser and browser.get('status') == 'PASS')
    checks['browser_all_checks_pass'] = bool(browser and browser.get('check_count') == browser.get('pass_count') and not browser.get('runtime_errors'))
    checks['engineering_only_no_human'] = bool(browser and browser.get('human_observations') == 0)
    checks['production_network_not_performed'] = bool(browser and browser.get('production_network_performed') is False)
    checks['production_mutated_false'] = bool(patch and patch.get('production_mutated') is False)

    status = 'PASS' if all(checks.values()) else 'HOLD'
    final = {
        'schema_version': 'CR0105R11-FINAL-SEAL-1',
        'stage': 'CUBE-REV 0.10.5-R1.1 — Exact-Monolith Byte Recovery, Source-Bound Patch Execution & Binary-identical Whole-page Release Seal',
        'status': status,
        'verdict': PASS_VERDICT if status == 'PASS' else FAIL_VERDICT,
        'repository': 'WhoSia/CUBE-REV',
        'research_branch': 'cube-rev-0.10.5-r1.1-exact-monolith-seal',
        'base_main_commit': '52fc4a04c922ea0d39dd29cdf1ac6ebed5a196a1',
        'workflow_head_sha': os.environ.get('GITHUB_SHA'),
        'workflow_run_id': os.environ.get('GITHUB_RUN_ID'),
        'source': source,
        'first_patched': first,
        'second_patched': second,
        'patched_additive_bytes': (first.get('bytes') - EXPECTED_BYTES) if first.get('present') else None,
        'checks': checks,
        'browser_check_count': (browser or {}).get('check_count'),
        'browser_pass_count': (browser or {}).get('pass_count'),
        'human_observations': 0,
        'main_or_pages_mutated': False,
        'release_scope': 'RESEARCH_BRANCH_ENGINEERING_SEAL_ONLY',
        'human_launch': 'NO_GO' if status != 'PASS' else 'ELIGIBLE_FOR_NEXT_RELEASE-IDENTITY_COURT; NOT_AUTO_LAUNCHED',
    }
    (art / 'FINAL_SEAL.json').write_text(json.dumps(final, indent=2), encoding='utf-8')

    selected = [
        'BASELINE_VALIDATION.json',
        'PATCH_EXECUTION_RECEIPT.json',
        'EXACT_SOURCE_BINDING.json',
        'DETERMINISTIC_REBUILD.json',
        'BOOT_DIAGNOSTIC.json',
        'EXACT_MONOLITH_BROWSER_COURT.json',
        'GITHUB_ACTION_PROVENANCE.txt',
        'FINAL_SEAL.json',
    ]
    for name in selected:
        src = art / name
        if src.is_file():
            shutil.copyfile(src, out / name)

    print(json.dumps(final, indent=2), flush=True)
    return 0 if status == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())
