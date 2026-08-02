#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("cr0817_external_snapshot", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_SPEC_FAILED")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def gate(condition: bool, name: str) -> None:
    if not condition:
        raise AssertionError(f"CR0817_GATE_FAILED:{name}")
    print(f"PASS {name}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", type=Path, required=True)
    ap.add_argument("--artifact-dir", type=Path, required=True)
    ap.add_argument("--fixtures", type=Path, required=True)
    ap.add_argument("--probe-registry", type=Path, required=True)
    args = ap.parse_args()

    mod = load_module(args.analysis)
    fixture = json.loads(args.fixtures.read_text(encoding="utf-8"))
    registry = json.loads(args.probe_registry.read_text(encoding="utf-8"))
    result = json.loads((args.artifact_dir / "CUBE_REV_0.8.17_ECOLOGICAL_PROBE_TRANSFER_RESULT.json").read_text(encoding="utf-8"))
    manifest = json.loads((args.artifact_dir / "CUBE_REV_0.8.17_EXTERNAL_SNAPSHOT_MANIFEST.json").read_text(encoding="utf-8"))
    rows = [json.loads(x) for x in (args.artifact_dir / "CUBE_REV_0.8.17_ROUTE_GRAMMAR_ROWS.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]

    gates = 0
    def check(cond: bool, name: str) -> None:
        nonlocal gates
        gate(cond, name); gates += 1

    check(mod.normalize_token("U2'") == "U2" and mod.normalize_token("R3") == "R'" and mod.normalize_token("Rw") == "r", "notation_canonicalization")
    rejected = False
    try:
        mod.normalize_token("Q")
    except ValueError:
        rejected = True
    check(rejected, "unsupported_notation_rejected")
    check(len(fixture["routes"]) == 11 and sum(bool(x["official"]) for x in fixture["routes"]) == 10, "frozen_fixture_route_counts")
    wca = fixture["wca_anchor"]
    check(wca["export_format_version"] == "2.0.2" and wca["tsv_filename"] == "WCA_export_v2_214_20260802T000025Z.tsv.zip", "wca_version_pin")
    check(wca["full_archive_materialized"] is False and fixture["reconstruction_source"]["raw_html_materialized"] is False, "raw_custody_holds_explicit")
    check(result["stm_conformance"]["reported_route_count"] == 10 and result["stm_conformance"]["exact_match_count"] == 10 and not result["stm_conformance"]["mismatch_route_ids"], "reported_stm_exact_10_of_10")
    check(result["aggregate_route_grammar"]["action_token_count"] == 466 and result["aggregate_route_grammar"]["stage_count"] == 61, "aggregate_route_accounting")
    check(result["aggregate_route_grammar"]["in_solve_rotation_count"] == 26 and result["aggregate_route_grammar"]["wide_move_count"] == 42 and result["aggregate_route_grammar"]["slice_move_count"] == 14, "rotation_wide_slice_separation")
    audit = result["matched_scramble_audits"]
    check(len(audit) == 1 and audit[0]["same_reported_time"] and audit[0]["route_nonunique"] and audit[0]["action_token_lengths"] == [41, 45], "matched_scramble_route_nonuniqueness")
    check(abs(audit[0]["normalized_token_edit_distance"] - 0.466667) < 1e-9 and abs(audit[0]["token_lcs_ratio"] - 0.6) < 1e-9, "matched_scramble_route_distance")
    transfer = result["probe_transfer"]
    check(transfer["relation_bigram_coverage_all_windows"]["weighted_coverage"] >= 0.80 and transfer["relation_trigram_coverage_all_windows"]["weighted_coverage"] >= 0.60, "local_motif_support_thresholds")
    check(transfer["relation_bigram_coverage_all_windows"]["missing"] == ["OPPOSITE|OPPOSITE"] and transfer["relation_trigram_coverage_all_windows"]["missing"] == ["START|OPPOSITE|OPPOSITE"], "missing_motifs_preserved")
    check(transfer["js_divergence_bigram"] > 0.25 and transfer["js_divergence_trigram"] > 0.25, "distributional_misalignment_detected")
    decision = result["decision"]
    check(decision["local_motif_support"] == "PASS" and decision["distributional_ecological_alignment"] == "HOLD", "local_support_not_conflated_with_alignment")
    check(decision["timing_transfer"] == "HOLD" and decision["cognitive_mechanism_transfer"] == "NO_GO", "timing_and_cognition_not_overclaimed")
    check(len(rows) == 11 and all(set(x).isdisjoint({"solver_name", "wca_id", "person_name", "source_url"}) for x in rows), "aggregate_rows_deidentified")
    check(all(x["source_attribution_excluded_from_aggregate_features"] for x in rows), "source_identity_exclusion_marker")
    check(manifest["fixture_canonical_sha256"] == result["snapshot"]["fixture_sha256"] and manifest["route_count"] == 11, "manifest_result_binding")
    check(manifest["raw_source_bytes_custodied"] is False and manifest["snapshot_grade"] == "VERSIONED_CANONICAL_TRANSCRIPTION_FIXTURE", "snapshot_grade_honest")
    check(registry["family_count"] == 6 and len(registry["families"]) == 6, "parent_probe_registry_bound")
    check(result["epistemic_boundary"]["population_representative"] is False and result["epistemic_boundary"]["named_solver_trait_inference"] is False, "population_and_named_trait_claims_prohibited")
    source_urls = [x["source_url"] for x in fixture["routes"]]
    check(len(set(source_urls)) == 11 and all(re.fullmatch(r"https://reco\.nz/solve/\d+", u) for u in source_urls), "source_url_attribution_integrity")

    print(f"CR0817_EXTERNAL_TRAJECTORY_SNAPSHOT_PASS {gates}/{gates}")


if __name__ == "__main__":
    main()
