#!/usr/bin/env python3
"""CUBE-REV 0.21 P5: evidence-grade audit, NOT independent semantic re-reading of third-party pages.

Inputs contain compact original paraphrases and public source URLs, not full reproductions.
Do not confuse retrospectively written order with unedited timestamped observed actions.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

SEED = Path(__file__).resolve().parents[2] / "data" / "cuberev-021" / "p5_fmc_existing_search_event_seed.json"
ALLOWED_BASIS = {"AUTHOR_RETROSPECTIVE_STATEMENT"}
ALLOWED_TIME_KINDS = {
    "self_report_approx_elapsed_min", "self_report_elapsed_min", "self_report_relative_to_end"
}
OBSERVED_AND_CERTIFIED_BY_VIDEO = {"VIDEO_OBSERVED", "FRAME_VERIFIED", "SENSOR_TIMESTAMP_VERIFIED"}
REPORTED_REVISIT_KINDS = {"REVISIT_INVERSE", "REVISIT_PRIOR_CANDIDATE_POOL", "LATE_REVISIT"}
REPORTED_ALTERNATIVE_KINDS = {
    "REPORTED_BRANCH_ENUMERATION", "ALTERNATIVE_CONTINUATION_TEST",
    "CANDIDATE_INDEX_CHOSEN"
}
if len(sys.argv) > 2:
    raise SystemExit("usage: verify-p5-fmc-process-evidence.py [receipt-path]")
raw = SEED.read_bytes()
dataset = json.loads(raw)
assert dataset["schema"] == "cuberev-021-p5-fmc-retrospective-process-v1"
assert dataset["source_acquisition"].endswith("NO_PRIVATE .VFMC FILE")
assert all(dataset["assertions"].values())
episodes = dataset["episodes"]
assert len(episodes) == 6
assert len({ep["id"] for ep in episodes}) == 6
assert len({ep["author"] for ep in episodes}) == 5
total_events = []
for ep in episodes:
    assert ep["source_url"].startswith("https://")
    assert ep["source_type"] in {
        "public_author_retrospective_writeup",
        "public_archived_personal_working_note"
    }
    assert ep["chronology_grade"] == "AUTHOR_REPORTED_PARTIAL_ORDER_ONLY"
    assert "No machine-time-verified" in ep["notes"]
    evs = ep["events"]
    assert len(evs) >= 3
    assert [e["sequence_index"] for e in evs] == list(range(1, len(evs) + 1))
    assert len({e["event_id"] for e in evs}) == len(evs)
    assert all(e["basis"] in ALLOWED_BASIS for e in evs)
    assert not any(e["basis"] in OBSERVED_AND_CERTIFIED_BY_VIDEO for e in evs)
    for event in evs:
        assert event["kind"] and event["author_paraphrase_ko"]
        assert len(event["author_paraphrase_ko"]) <= 250
        if "time_anchor" in event:
            a = event["time_anchor"]
            assert a["kind"] in ALLOWED_TIME_KINDS
            assert a.get("minutes", a.get("minutes_before_end")) is not None
            if "minutes" in a:
                assert 0 <= a["minutes"] <= 60
        if "candidate_quantity" in event:
            q = event["candidate_quantity"]
            assert q["kind"] in {"more_than", "at_least", "exact_reported", "author_reported_ordinal"}
            assert isinstance(q["n"], int) and q["n"] > 0
            assert q["unit"] in {
                "EO_candidates_written", "branch_variants_written", "new_NISS_EO_candidates",
                "EO_candidate_test_index"
            }
            # Never derive number of tested candidates from a written-pool size!
            assert not (q["unit"] == "EO_candidates_written" and event["kind"] == "CANDIDATE_INDEX_CHOSEN")
    total_events.extend(evs)
assert len(total_events) == 29
assert len({e["event_id"] for e in total_events}) == 29
categories = Counter(e["kind"] for e in total_events)
by_ep = {ep["id"]: len(ep["events"]) for ep in episodes}
assert by_ep == {
 "WHEELER_SEFMC2026_A1": 10,
 "QURAISHI_FMCWORLD2026_A3": 6,
 "DONG_FMCWORLD2026_A1": 3,
 "DONG_FMCWORLD2026_A2": 3,
 "PIETRUSIAK_WARSZAWA2026_F2": 3,
 "GUIDO_ARCHIVE_REWRITE_24": 4
}
revisits = sum(categories.get(k, 0) for k in REPORTED_REVISIT_KINDS)
alternative_explicit = sum(categories.get(k, 0) for k in REPORTED_ALTERNATIVE_KINDS)
assert revisits == 3
assert alternative_explicit == 3
time_anchors = [e for e in total_events if "time_anchor" in e]
assert len(time_anchors) == 7
quantities = [e["candidate_quantity"] for e in total_events if "candidate_quantity" in e]
assert len(quantities) == 4
assert any(q["n"] == 42 and q["unit"] == "EO_candidates_written" for q in quantities)
assert any(q["n"] == 38 and q["unit"] == "EO_candidate_test_index" for q in quantities)
assert any(q["n"] == 2 and q["unit"] == "new_NISS_EO_candidates" for q in quantities)
assert categories["DEFERRED_UNEVALUATED"] == 1
assert categories["OTHER_AUTHOR_POSTHOC_NOTE"] == 1

w = next(ep for ep in episodes if ep["id"] == "WHEELER_SEFMC2026_A1")
w_times = [e["time_anchor"]["minutes"] for e in w["events"]
           if e.get("time_anchor", {}).get("kind", "").startswith("self_report_")
           and "minutes" in e["time_anchor"]]
assert w_times == [30, 55, 56, 57.5, 59.95]
assert all(a < b for a, b in zip(w_times, w_times[1:]))
assert not any("time_anchor" in e for ep in episodes if ep["id"].startswith("GUIDO")
               for e in ep["events"])

receipt = {
 "marker": "CUBE_REV_021_P5_EXISTING_FMC_PROCESS_EVIDENCE_BOUNDARY_PASS",
 "research_status": "RETROSPECTIVE_TEXT_EVENT_EXTRACTION_PASS__DIRECT_PROCESS_OBSERVATION_HOLD",
 "seed_sha256": hashlib.sha256(raw).hexdigest(),
 "episodes": len(episodes),
 "unique_named_authors": len({ep["author"] for ep in episodes}),
 "events": len(total_events),
 "events_by_episode": by_ep,
 "explicitly_reported_revisits": revisits,
 "explicitly_reported_alternative_selection_or_comparison_events": alternative_explicit,
 "time_anchors_self_report_only": len(time_anchors),
 "independently_verified_event_time_anchors": 0,
 "public_vfmc_user_session_files_acquired": 0,
 "raw_video_frames_examined": 0,
 "human_experimental_participants_recruited": 0,
 "events_directly_verified_from_unedited_performance": 0,
 "reported_quantity_records": quantities,
 "unevaluated_cubie_candidate_events_kept_distinct_from_failed_candidate_events": categories["DEFERRED_UNEVALUATED"],
 "other_author_posthoc_revision_excluded_from_original_author_cognition": categories["OTHER_AUTHOR_POSTHOC_NOTE"],
 "event_kind_counts": dict(sorted(categories.items())),
 "methodology": "Verify evidence-grade schema and known manually audited counts; no automated remote source-content validation; paraphrased historical authors' reports, not certified live behavioral traces."
}
output = (json.dumps(receipt, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()
if len(sys.argv) == 2:
    Path(sys.argv[1]).write_bytes(output)
sys.stdout.buffer.write(output)
