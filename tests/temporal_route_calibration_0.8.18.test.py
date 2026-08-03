#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import tempfile
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("cr0818", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("CR0818_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", type=Path, required=True)
    ap.add_argument("--fixtures", type=Path, required=True)
    ap.add_argument("--synthetic-trajectories", type=Path, required=True)
    ap.add_argument("--artifact-dir", type=Path, required=True)
    args = ap.parse_args()
    m = load_module(args.analysis)
    fixture = json.loads(args.fixtures.read_text())
    art = args.artifact_dir
    qc = json.loads((art / "CUBE_REV_0.8.18_TIMESTAMP_QC_RESULT.json").read_text())
    gap = json.loads((art / "CUBE_REV_0.8.18_TEMPORAL_DOMAIN_GAP_RESULT.json").read_text())
    rw = json.loads((art / "CUBE_REV_0.8.18_REWEIGHTING_RESULT.json").read_text())
    cert = json.loads((art / "CUBE_REV_0.8.18_CERTIFICATION_RESULT.json").read_text())
    manifest = json.loads((art / "CUBE_REV_0.8.18_SNAPSHOT_MANIFEST.json").read_text())
    passed = 0

    assert fixture["source"]["repository"] == "SpeedcuberOSS/speedcuber-timer"
    assert fixture["source"]["commit"] == "7c9d9a798b0396d35d635c929051041f18c84687"
    assert fixture["source"]["license"] == "MPL-2.0"
    passed += 1

    assert fixture["evidence_grade"] == "PUBLICLY_LICENSED_SOFTWARE_TEST_FIXTURE_NOT_RESEARCH_CONSENT"
    assert fixture["source"]["research_consent"] == "NOT_ESTABLISHED_BY_SOFTWARE_LICENSE"
    passed += 1

    assert len(fixture["fixtures"]) == 3
    assert [x["event_count"] for x in fixture["fixtures"]] == [66, 29, 69]
    assert [x["duration_ms"] for x in fixture["fixtures"]] == [14362, 7217, 11653]
    passed += 1

    for source in fixture["fixtures"]:
        assert m.audit_events(source["events"])["status"] == "PASS"
        expected = m.sha256_bytes(m.canonical_bytes(source["events"]))
        assert expected == source["canonical_events_sha256"]
    passed += 1

    assert qc["raw_event_count"] == 164
    assert qc["derived_logical_turn_count"] == 143
    assert [x["derived_logical_turn_count"] for x in qc["fixture_audits"]] == [61, 22, 60]
    passed += 1

    for audit in qc["fixture_audits"]:
        expected_window = audit["duration_ms"] / audit["raw_event_count"]
        assert math.isclose(audit["upstream_adaptive_compression_window_ms"], expected_window, rel_tol=0, abs_tol=1e-12)
        assert audit["double_turn_compression_is_derived_not_raw_rewrite"] is True
    passed += 1

    court = qc["negative_control_court"]
    assert court["result"] == "PASS_NEGATIVE_CONTROL_COURT"
    passed += 1

    for name in ["reordered_events", "zero_delta", "clock_regression", "unsupported_move", "dropped_event_with_counter"]:
        assert court["cases"][name]["audit"]["status"] == "FAIL"
    passed += 1

    assert court["cases"]["implausible_sub20ms_burst"]["audit"]["status"] == "PASS"
    assert court["cases"]["implausible_sub20ms_burst"]["audit"]["very_fast_lt20ms_count"] >= 1
    passed += 1

    assert court["cases"]["dropped_event_without_counter"]["audit"]["status"] == "PASS"
    assert court["cases"]["dropped_event_without_counter"]["conclusion"] == "PASSING_STRUCTURE_DOES_NOT_PROVE_NO_PACKET_LOSS"
    passed += 1

    assert qc["packet_loss_certification"].startswith("HOLD_")
    assert qc["state_continuity_certification"].startswith("HOLD_")
    passed += 1

    assert qc["research_consent"] == "HOLD_SOFTWARE_LICENSE_IS_NOT_RESEARCH_CONSENT"
    passed += 1

    assert gap["primary_calibration_domain"] == "PUBLIC_LICENSED_PARTICULA_2X2_TEST_FIXTURE"
    assert gap["primary_intermove_count"] == 28
    assert gap["pooled_public_intermove_count"] == 161
    passed += 1

    assert gap["latency_js_divergence_before"] > 0.25
    assert gap["log10_wasserstein_before"] > 0.20
    passed += 1

    assert gap["unreachable_primary_mass_below_synthetic_minimum"] > 0.35
    assert gap["support_gap_conclusion"] == "FULL_ALIGNMENT_IMPOSSIBLE_BY_REWEIGHTING_ONLY"
    passed += 1

    thresholds = gap["latency_class_thresholds_ms"]
    assert thresholds["burst_max_p25"] == 89.0
    assert thresholds["flow_max_p75"] == 221.0
    passed += 1

    assert rw["reweighting_certification"] == "PASS_CONSTRAINED_DOMAIN_GAP_REDUCTION"
    assert rw["latency_js_after"] < rw["latency_js_before"] * 0.90
    passed += 1

    assert rw["algorithm"]["per_mechanism_total_preserved"] is True
    assert rw["algorithm"]["weight_bounds"] == [0.2, 5.0]
    passed += 1

    assert len(rw["mechanism_weight_audit"]) == 10
    for row in rw["mechanism_weight_audit"]:
        assert abs(row["weight_sum"] - row["row_count"]) < 1e-6
        assert row["minimum_weight"] >= 0.2 - 1e-9
        assert row["maximum_weight"] <= 5.0 + 1e-9
        assert row["ess_fraction"] >= 0.30
    passed += 1

    assert rw["temporal_route_grammar_js_after"] < rw["temporal_route_grammar_js_before"]
    passed += 1

    assert rw["full_alignment"].startswith("HOLD_")
    assert rw["research_consent"].startswith("HOLD_")
    passed += 1

    assert cert["all_conditions_pass"] is True
    assert all(cert["conditions"].values())
    passed += 1

    decision = cert["decision"]
    assert decision["public_licensed_timestamp_fixture"] == "PASS"
    assert decision["timestamp_qc_and_corruption_court"] == "PASS"
    assert decision["temporal_domain_gap_detection"] == "PASS"
    assert decision["constrained_reweighting"] == "PASS"
    passed += 1

    assert decision["research_consented_human_fixture"] == "HOLD"
    assert decision["packet_loss_certification"] == "HOLD"
    assert decision["full_temporal_ecological_alignment"] == "HOLD"
    passed += 1

    assert decision["human_cognitive_mechanism_transfer"] == "NO_GO"
    assert decision["participant_deployment"] == "NO_GO"
    passed += 1

    assert manifest["synthetic_input"]["row_count"] == 3600
    assert manifest["fixture_canonical_sha256"] == m.sha256_bytes(m.canonical_bytes(fixture))
    passed += 1

    for name, record in manifest["files"].items():
        path = args.fixtures if name == args.fixtures.name else art / name
        assert path.exists(), name
        assert m.sha256_bytes(path.read_bytes()) == record["sha256"]
        assert path.stat().st_size == record["bytes"]
    passed += 1

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        m.run(args.fixtures, args.synthetic_trajectories, out)
        for name in [
            "CUBE_REV_0.8.18_TIMESTAMP_QC_RESULT.json",
            "CUBE_REV_0.8.18_TEMPORAL_DOMAIN_GAP_RESULT.json",
            "CUBE_REV_0.8.18_REWEIGHTING_RESULT.json",
            "CUBE_REV_0.8.18_CERTIFICATION_RESULT.json",
            "CUBE_REV_0.8.18_TEMPORAL_EVENT_ROWS.jsonl",
            "CUBE_REV_0.8.18_REWEIGHTED_TRAJECTORY_WEIGHTS.jsonl",
            "CUBE_REV_0.8.18_SNAPSHOT_MANIFEST.json",
        ]:
            assert (out / name).read_bytes() == (art / name).read_bytes(), name
    passed += 1

    assert passed == 28
    print(f"CR0818_TEMPORAL_ROUTE_CALIBRATION_PASS {passed}/28")


if __name__ == "__main__":
    main()
