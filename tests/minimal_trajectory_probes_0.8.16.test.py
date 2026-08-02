#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "minimal_trajectory_probes_0_8_16.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cr0816", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("CR0816_TEST_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact-dir", type=Path, required=True)
    ap.add_argument("--bank", type=Path, required=True)
    args = ap.parse_args()
    m = load_module()
    art = args.artifact_dir
    registry = json.loads((art / "CUBE_REV_0.8.16_TRAJECTORY_PROBE_REGISTRY.json").read_text())
    schedules = json.loads((art / "CUBE_REV_0.8.16_TRAJECTORY_SCHEDULES.json").read_text())
    result = json.loads((art / "trajectory_identifiability_result.json").read_text())
    cert = json.loads((art / "CUBE_REV_0.8.16_CERTIFICATION_RESULT.json").read_text())
    sources = json.loads((art / "CUBE_REV_0.8.16_EXTERNAL_TRAJECTORY_SOURCE_REGISTRY.json").read_text())
    pack = json.loads((art / "CUBE_REV_0.8.16_EXTERNAL_RECONSTRUCTION_FIXTURE_PACK.json").read_text())
    pack_audit = json.loads((art / "CUBE_REV_0.8.16_EXTERNAL_RECONSTRUCTION_FIXTURE_AUDIT.json").read_text())
    design = json.loads((art / "CUBE_REV_0.8.16_NONREACTIVE_TRAJECTORY_DESIGN.json").read_text())
    linkage = json.loads((art / "CUBE_REV_0.8.16_EXTERNAL_LINKAGE_DRYRUN.json").read_text())
    bank = json.loads(args.bank.read_text())
    bank_state = {row["stimulus_id"]: m.BASE.state_from_stickers(row["stickers"]) for row in bank["stimuli"]}

    passed = 0
    # 1. Exact move conjugation under all proper cube rotations.
    for rotation in m.ROTATIONS:
        for move in m.MOVES:
            transformed = m.conjugated_move(move, rotation)
            lhs = m.BASE.rotate_state(m.BASE.apply_move(m.UNIQUE_STICKER_STATE, move), rotation)
            rhs = m.BASE.apply_move(m.BASE.rotate_state(m.UNIQUE_STICKER_STATE, rotation), transformed)
            assert lhs == rhs
    passed += 1

    # 2. Six unique families and 36 probes.
    assert registry["family_count"] == 6 and registry["probe_count"] == 36
    assert len({family["source_orbit_sha256"] for family in registry["families"]}) == 6
    passed += 1

    # 3. Exact parent/generator provenance for every generated seed.
    for family in registry["families"]:
        parent = bank_state[family["parent_stimulus_id"]]
        expected = parent if family["generator_move"] is None else m.BASE.apply_move(parent, family["generator_move"])
        canonical = next(member for member in family["members"] if member["probe_id"] == family["canonical_probe_id"])
        assert m.BASE.state_from_stickers(canonical["stickers"]) == expected
        assert family["generation_depth"] in {0, 1}
        assert (family["generator_move"] is None) == (family["generation_depth"] == 0)
    passed += 1

    # 4. Dense recovery opportunities.
    counts = [family["recovery_opportunity_count"] for family in registry["families"]]
    assert min(counts) >= 6
    assert registry["recovery_opportunity_count"]["minimum_per_family"] == min(counts)
    passed += 1

    # 5. Planned and recovery face balance.
    assert registry["planned_first_face_counts"] == {face: 6 for face in sorted(m.FACES)}
    assert registry["recovery_error_face_counts"] == {face: 6 for face in sorted(m.FACES)}
    passed += 1

    # 6. Every rotated planned path is transition-equivariant.
    for family in registry["families"]:
        canonical = next(member for member in family["members"] if member["probe_id"] == family["canonical_probe_id"])
        canonical_state = m.BASE.state_from_stickers(canonical["stickers"])
        for member in family["members"]:
            rotation = tuple(tuple(x for x in col) for col in member["rotation_matrix"])
            rotated_state = m.BASE.state_from_stickers(member["stickers"])
            expected_actions = m.transform_sequence(canonical["planned_sequence"], rotation)
            assert tuple(member["planned_sequence"]) == expected_actions
            a, b = canonical_state, rotated_state
            for ca, rb in zip(canonical["planned_sequence"], member["planned_sequence"]):
                a = m.BASE.apply_move(a, ca); b = m.BASE.apply_move(b, rb)
            assert m.BASE.rotate_state(a, rotation) == b
    passed += 1

    # 7. Balanced minimal schedules.
    assert schedules["schedule_count"] == 12 and schedules["trials_per_schedule"] == 12
    assert schedules["minimum_family_spacing"] == 6
    exposure = {family["family_id"]: Counter() for family in registry["families"]}
    for schedule in schedules["schedules"]:
        assert len(schedule["entries"]) == 12
        for entry in schedule["entries"]:
            exposure[entry["family_id"]][entry["target_planned_face"]] += 1
        assert min(schedule["family_separations"].values()) >= 6
    assert all(all(counter[face] == 4 for face in m.FACES) for counter in exposure.values())
    passed += 1

    # 8. Full positive controls and negative control.
    assert result["contrasts"]["open_vs_closed"]["mean"] >= 0.80
    assert result["contrasts"]["undo_vs_reset"]["mean"] >= 0.80
    assert result["contrasts"]["reset_vs_persist"]["mean"] >= 0.80
    assert result["contrasts"]["latent_same_trajectory"]["mean"] < 0.60
    passed += 1

    # 9. First action remains insufficient.
    views = result["feature_view_audit"]
    assert views["first_action_only"]["open_vs_closed"]["mean"] < 0.60
    assert views["first_action_only"]["undo_vs_reset"]["mean"] < 0.60
    passed += 1

    # 10. Second action plus latency is the robust minimum in this synthetic design.
    assert views["two_actions_no_latency"]["open_vs_closed"]["mean"] < 0.80
    assert views["two_actions_no_latency"]["undo_vs_reset"]["mean"] < 0.80
    assert views["two_actions_with_latency"]["open_vs_closed"]["mean"] >= 0.80
    assert views["two_actions_with_latency"]["undo_vs_reset"]["mean"] >= 0.80
    passed += 1

    # 11. Chunk-boundary pause requires timing rather than action identity.
    assert views["two_actions_no_latency"]["boundary_pause_same_actions"]["mean"] < 0.60
    assert views["latency_only"]["boundary_pause_same_actions"]["mean"] >= 0.80
    passed += 1

    # 12. Noise stress retains positives and refuses the latent negative.
    robust = result["robust_noise_audit"]
    assert all(robust["conditions"].values())
    assert robust["two_actions_with_latency"]["latent_same_trajectory"]["mean"] < 0.60
    passed += 1

    # 13. External source registry assigns non-overlapping roles.
    by_id = {row["source_id"]: row for row in sources["sources"]}
    assert by_id["WCA-RESULTS-EXPORT-V2"]["does_not_contain"] == ["solution move sequence", "per-move timestamp", "cognitive annotation"]
    assert by_id["RECO-NZ-RECONSTRUCTION-DATABASE"]["prohibited_role"] == "direct inference of 2x2 thought process"
    assert by_id["CSTIMER-SMART-CUBE-EXPORT"]["access"] == "USER_CONSENT_EXPORT_ONLY"
    passed += 1

    # 14. Current WCA export metadata snapshot is explicit and not mistaken for trajectory data.
    wca = by_id["WCA-RESULTS-EXPORT-V2"]["observed_export"]
    assert wca["format_version"] == "2.0.2"
    assert wca["tsv_filename"] == "WCA_export_v2_214_20260802T000025Z.tsv.zip"
    assert wca["materialization"].startswith("METADATA_SNAPSHOT_ONLY")
    passed += 1

    # 15. Public matched-scramble reconstructions demonstrate trajectory nonuniqueness.
    assert pack_audit["result"] == "PASS_EXTERNAL_TRAJECTORY_FIXTURE_PACK"
    assert pack_audit["matched_pair_same_scramble"] is True
    assert pack_audit["matched_pair_same_result_time"] is True
    assert pack_audit["matched_pair_distinct_move_routes"] is True
    assert pack["prohibited_inference"] == "named-solver cognitive trait or unobserved thought process"
    passed += 1

    # 16. External linkage contract distinguishes exact, ambiguous, and unlinked cases.
    assert linkage["result"] == "PASS_LINKAGE_ADJUDICATION_CONTRACT"
    assert linkage["exact_case"]["status"] == "EXACT_UNIQUE"
    assert linkage["ambiguous_case"]["status"] == "AMBIGUOUS_MULTIPLE"
    assert linkage["negative_case"]["status"] == "UNLINKED"
    assert linkage["bulk_execution"].startswith("HOLD_")
    passed += 1

    # 17. Participant-facing nonreactivity firewall.
    assert design["trial_contract"]["maximum_actions"] == 3
    assert "trialwise confidence" in design["trial_contract"]["do_not_record"]
    assert design["feedback"] if "feedback" in design else design["trial_contract"]["feedback"] == "NONE"
    assert design["deployment"] == "NO_GO_RESEARCH_ASSET_ONLY"
    passed += 1

    # 18. Certification remains research-only.
    assert result["result"] == "PASS_MINIMAL_TRAJECTORY_IDENTIFIABILITY"
    assert cert["result"] == "PASS_MINIMAL_NONREACTIVE_TRAJECTORY_PROBE_CERTIFICATION"
    assert cert["deployment"] == "NO_GO" and cert["human_mechanism_claim"] == "NO_GO"
    passed += 1

    assert passed == 18
    print(f"CR0816_MINIMAL_TRAJECTORY_PASS {passed}/18")


if __name__ == "__main__":
    main()
