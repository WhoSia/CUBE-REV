#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


def normalize_scramble(value: str) -> str:
    return " ".join(str(value).replace("\n", " ").split())


def scramble_sha256(value: str) -> str:
    return hashlib.sha256(normalize_scramble(value).encode("utf-8")).hexdigest()


def result_centiseconds(seconds: float) -> int:
    return int(round(float(seconds) * 100))


@dataclass(frozen=True)
class AttemptAnchor:
    competition_id: str
    event_id: str
    round_type_id: str
    attempt_number: int
    result_centiseconds: int
    scramble: str
    date: str
    public_person_key: str | None = None

    @property
    def scramble_sha256(self) -> str:
        return scramble_sha256(self.scramble)


@dataclass(frozen=True)
class ReconstructionAnchor:
    source_id: str
    puzzle: str
    result_centiseconds: int
    scramble: str
    date: str
    competition_label: str | None = None
    public_solver_label: str | None = None

    @property
    def scramble_sha256(self) -> str:
        return scramble_sha256(self.scramble)


def normalize_wca_attempt(row: Mapping[str, object]) -> AttemptAnchor:
    return AttemptAnchor(
        competition_id=str(row["competition_id"]),
        event_id=str(row["event_id"]),
        round_type_id=str(row["round_type_id"]),
        attempt_number=int(row["attempt_number"]),
        result_centiseconds=int(row["result_centiseconds"]),
        scramble=normalize_scramble(str(row["scramble"])),
        date=str(row["date"]),
        public_person_key=None if row.get("public_person_key") is None else str(row["public_person_key"]),
    )


def normalize_reconstruction(row: Mapping[str, object]) -> ReconstructionAnchor:
    return ReconstructionAnchor(
        source_id=str(row["source_id"]),
        puzzle=str(row["puzzle"]),
        result_centiseconds=int(row.get("result_centiseconds", result_centiseconds(float(row["result_seconds"])))),
        scramble=normalize_scramble(str(row["scramble"])),
        date=str(row["date"]),
        competition_label=None if row.get("competition_label") is None else str(row["competition_label"]),
        public_solver_label=None if row.get("public_solver_label") is None else str(row["public_solver_label"]),
    )


def linkage_candidates(reconstruction: ReconstructionAnchor, attempts: Sequence[AttemptAnchor]) -> list[AttemptAnchor]:
    event_map = {"2x2": "222", "3x3": "333", "4x4": "444", "5x5": "555", "OH": "333oh"}
    event_id = event_map.get(reconstruction.puzzle, reconstruction.puzzle)
    return [
        attempt for attempt in attempts
        if attempt.event_id == event_id
        and attempt.result_centiseconds == reconstruction.result_centiseconds
        and attempt.scramble_sha256 == reconstruction.scramble_sha256
        and attempt.date == reconstruction.date
    ]


def adjudicate_linkage(reconstruction: ReconstructionAnchor, attempts: Sequence[AttemptAnchor]) -> dict[str, object]:
    candidates = linkage_candidates(reconstruction, attempts)
    if len(candidates) == 1:
        attempt = candidates[0]
        return {
            "source_id": reconstruction.source_id,
            "status": "EXACT_UNIQUE",
            "candidate_count": 1,
            "attempt_anchor": {
                "competition_id": attempt.competition_id,
                "event_id": attempt.event_id,
                "round_type_id": attempt.round_type_id,
                "attempt_number": attempt.attempt_number,
                "result_centiseconds": attempt.result_centiseconds,
                "scramble_sha256": attempt.scramble_sha256,
                "date": attempt.date,
            },
            "identity_use": "PUBLIC_ATTRIBUTION_AND_LINKAGE_ONLY",
            "cognitive_trait_inference": "PROHIBITED",
        }
    if len(candidates) > 1:
        return {
            "source_id": reconstruction.source_id,
            "status": "AMBIGUOUS_MULTIPLE",
            "candidate_count": len(candidates),
            "cognitive_trait_inference": "PROHIBITED",
        }
    return {
        "source_id": reconstruction.source_id,
        "status": "UNLINKED",
        "candidate_count": 0,
        "cognitive_trait_inference": "PROHIBITED",
    }


def dryrun_contract() -> dict[str, object]:
    scramble = "D2 U' R2 B2 L2 B2 D B2 L2 D2 B' U' R' U2 F2 D' B F D B' R"
    attempts = [
        AttemptAnchor("WC2023", "333", "f", 4, 454, scramble, "2023-08-19", "PUBLIC-A"),
        AttemptAnchor("WC2023", "333", "f", 5, 548, "R U R'", "2023-08-19", "PUBLIC-B"),
    ]
    reconstruction = ReconstructionAnchor("reco.nz/solve/9269", "3x3", 454, scramble, "2023-08-19", "Rubik's WCA World Championship 2023")
    exact = adjudicate_linkage(reconstruction, attempts)
    ambiguous = adjudicate_linkage(reconstruction, attempts + [AttemptAnchor("WC2023", "333", "f", 1, 454, scramble, "2023-08-19", "PUBLIC-C")])
    unlinked = adjudicate_linkage(
        ReconstructionAnchor("negative/wrong-scramble", "3x3", 454, "U R F", "2023-08-19"),
        attempts,
    )
    return {
        "schema_version": "CR0816-EXTERNAL-TRAJECTORY-LINKAGE-DRYRUN-1",
        "version": "CUBE-REV 0.8.16",
        "required_exact_fields": ["event", "result_centiseconds", "scramble_sha256", "date"],
        "recommended_disambiguators": ["competition_id", "round_type_id", "attempt_number", "public_person_key"],
        "exact_case": exact,
        "ambiguous_case": ambiguous,
        "negative_case": unlinked,
        "bulk_execution": "HOLD_WCA_ARCHIVE_NOT_MATERIALIZED",
        "result": "PASS_LINKAGE_ADJUDICATION_CONTRACT" if exact["status"] == "EXACT_UNIQUE" and ambiguous["status"] == "AMBIGUOUS_MULTIPLE" and unlinked["status"] == "UNLINKED" else "HOLD",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    data = dryrun_contract()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CR0816_EXTERNAL_LINKAGE_PASS status={data['result']}")


if __name__ == "__main__":
    main()
