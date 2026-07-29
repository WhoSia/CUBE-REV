#!/usr/bin/env python3
"""Create non-overwriting Pass A and Pass B annotation packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

LABELS = [
    "REPLAY",
    "GEODESIC_PLANNING",
    "ALGORITHMIC_CHUNK",
    "LOCAL_SEARCH",
    "FRAME_REPAIR",
    "INPUT_RECOVERY",
    "PERIODIC_POLICY",
    "DISENGAGEMENT",
    "OTHER_OR_MIXED",
]


def packet_id(session_id: str, trial_id: str) -> str:
    raw = f"{session_id}:{trial_id}".encode()
    return "CR07A-" + hashlib.sha256(raw).hexdigest()[:16]


def build(session: dict) -> tuple[list[dict], list[dict]]:
    first, second = [], []
    for trial in session.get("trials", []):
        pid = packet_id(str(session.get("session_id")), str(trial.get("trial_id")))
        trace = {
            "accepted_moves": trial.get("accepted_moves", []),
            "events": trial.get("events", []),
            "timing": trial.get("timing"),
            "status": trial.get("status"),
        }
        common = {
            "packet_id": pid,
            "labels": LABELS,
            "annotation": {
                "label": None,
                "episode_start_event_id": None,
                "episode_end_event_id": None,
                "confidence": None,
                "notes": None,
            },
        }
        first.append({
            **common,
            "pass": "A_BLINDED_TRACE",
            "blinding": {
                "participant_token_hidden": True,
                "condition_hidden": True,
                "history_visibility_hidden": True,
                "probe_response_hidden": True,
            },
            "trace": trace,
        })
        second.append({
            **json.loads(json.dumps(common)),
            "pass": "B_CONTEXT_AND_ALTERNATIVES",
            "requires_completed_pass_a": True,
            "trace": trace,
            "context": {
                "condition": trial.get("condition"),
                "assigned_history_label": trial.get("assigned_history_label"),
                "calibration_assignment": trial.get("calibration_assignment"),
                "probe_policy": trial.get("probe_policy"),
                "strategy_probe": trial.get("strategy_probe"),
            },
            "pass_a_reference": {"packet_id": pid, "annotation_sha256": None},
        })
    return first, second


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    session = json.loads(args.session_json.read_text(encoding="utf-8"))
    pass_a, pass_b = build(session)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "pass_a_blinded.json").write_text(
        json.dumps(pass_a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.output / "pass_b_context.json").write_text(
        json.dumps(pass_b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"pass_a": len(pass_a), "pass_b": len(pass_b), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
