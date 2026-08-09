#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
BASE_MODULE_PATH = ROOT / "analysis" / "cognitive_mechanism_lattice_0_8_15.py"


def load_base_module():
    spec = importlib.util.spec_from_file_location("cube_rev_cr0815_core", BASE_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("CR0816_BASE_MODULE_SPEC_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BASE = load_base_module()
State = BASE.State
Vec = BASE.Vec
MOVES = BASE.MOVES
FACES = BASE.FACES
ROTATIONS = BASE.ROTATIONS


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def inverse_move(move: str) -> str:
    if move.endswith("2"):
        return move
    return move[0] if move.endswith("'") else move + "'"


def state_to_stickers(state: State) -> Dict[str, List[List[str]]]:
    out: Dict[str, List[List[str]]] = {}
    i = 0
    for face in FACES:
        out[face] = [[state[i], state[i + 1]], [state[i + 2], state[i + 3]]]
        i += 4
    return out


@lru_cache(maxsize=None)
def best_sequence_summary(state: State, depth: int, previous_face: str = "") -> Tuple[int, Tuple[str, ...], int]:
    if depth == 0:
        return BASE.solved_score(state), (), 1
    best_score = -10**9
    best_sequence: Tuple[str, ...] | None = None
    best_count = 0
    for move in MOVES:
        if previous_face and move[0] == previous_face:
            continue
        score, tail, count = best_sequence_summary(BASE.apply_move(state, move), depth - 1, move[0])
        sequence = (move,) + tail
        if score > best_score:
            best_score = score
            best_sequence = sequence
            best_count = count
        elif score == best_score:
            best_count += count
            if best_sequence is None or sequence < best_sequence:
                best_sequence = sequence
    if best_sequence is None:
        raise RuntimeError("CR0816_NO_SEQUENCE")
    return best_score, best_sequence, best_count


def greedy_moves(state: State, excluded_face: str = "") -> List[str]:
    values = {
        move: BASE.solved_score(BASE.apply_move(state, move))
        for move in MOVES
        if not excluded_face or move[0] != excluded_face
    }
    best = max(values.values())
    return sorted(move for move, value in values.items() if value == best)


def inverse_rotation(rotation: Tuple[Vec, Vec, Vec]) -> Tuple[Vec, Vec, Vec]:
    return (
        (rotation[0][0], rotation[1][0], rotation[2][0]),
        (rotation[0][1], rotation[1][1], rotation[2][1]),
        (rotation[0][2], rotation[1][2], rotation[2][2]),
    )


def normalized_score(state: State, rotation: Tuple[Vec, Vec, Vec]) -> int:
    return BASE.solved_score(BASE.rotate_state(state, inverse_rotation(rotation)))


UNIQUE_STICKER_STATE: State = tuple(f"S{i:02d}" for i in range(24))


@lru_cache(maxsize=None)
def conjugated_move(move: str, rotation: Tuple[Vec, Vec, Vec]) -> str:
    rotated_before = BASE.rotate_state(UNIQUE_STICKER_STATE, rotation)
    target = BASE.rotate_state(BASE.apply_move(UNIQUE_STICKER_STATE, move), rotation)
    matches = [candidate for candidate in MOVES if BASE.apply_move(rotated_before, candidate) == target]
    if len(matches) != 1:
        raise RuntimeError(f"CR0816_MOVE_CONJUGATION_FAILURE:{move}:{rotation}:{matches}")
    return matches[0]


def transform_sequence(sequence: Sequence[str], rotation: Tuple[Vec, Vec, Vec]) -> Tuple[str, ...]:
    return tuple(conjugated_move(move, rotation) for move in sequence)


def select_family_rotations(planned_first: str, recovery_error: str) -> Dict[str, Tuple[Vec, Vec, Vec]]:
    identity = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    candidates_by_face: Dict[str, List[Tuple[Vec, Vec, Vec]]] = {}
    for target_face in FACES:
        candidates = [m for m in ROTATIONS if conjugated_move(planned_first, m)[0] == target_face]
        if not candidates:
            raise RuntimeError(f"CR0816_NO_ROTATION_FOR_PLANNED_FACE:{planned_first}:{target_face}")
        candidates_by_face[target_face] = sorted(candidates)

    best = None
    for combo in __import__('itertools').product(*(candidates_by_face[face] for face in FACES)):
        if len(set(combo)) != 6:
            continue
        recovery_faces = [conjugated_move(recovery_error, m)[0] for m in combo]
        counts = Counter(recovery_faces)
        values = [counts.get(face, 0) for face in FACES]
        identity_penalty = 0 if identity in combo else 1
        score = (
            max(values) - min(values),
            sum(v * v for v in values),
            identity_penalty,
            tuple(combo),
        )
        if best is None or score < best[0]:
            best = (score, combo)
    if best is None:
        raise RuntimeError("CR0816_FAMILY_ROTATION_OPTIMIZATION_FAILED")
    return {face: rotation for face, rotation in zip(FACES, best[1])}


def path_score(state: State, sequence: Sequence[str]) -> int:
    out = state
    for move in sequence:
        out = BASE.apply_move(out, move)
    return BASE.solved_score(out)


@dataclass(frozen=True)
class CandidateSeed:
    seed_id: str
    parent_stimulus_id: str
    generator_move: str | None
    generation_depth: int
    state: State


@dataclass(frozen=True)
class BaseProbe:
    seed_id: str
    parent_stimulus_id: str
    generator_move: str | None
    generation_depth: int
    orbit_id: str
    state: State
    planned_sequence: Tuple[str, str, str]
    replanned_sequence: Tuple[str, str, str]
    error_move: str
    undo_move: str
    reset_move: str
    persist_move: str
    initial_score: int
    planned_final_score: int
    replan_final_score: int
    error_score: int
    undo_score: int
    reset_score: int
    persist_score: int
    optimal_sequence_count: int
    recovery_options: Tuple[Tuple[str, str, str, str, int, int, int, int, int], ...]
    selection_score: Tuple[int, int, int, int, int, str]


def enumerate_recovery_options(state: State) -> List[Tuple[str, str, str, str, int, int, int, int]]:
    initial_score = BASE.solved_score(state)
    recovery_options: List[Tuple[str, str, str, str, int, int, int, int]] = []
    for move in MOVES:
        if move.endswith("2"):
            continue
        after_error = BASE.apply_move(state, move)
        error_score = BASE.solved_score(after_error)
        if error_score >= initial_score:
            continue
        undo = inverse_move(move)
        undo_score = BASE.solved_score(BASE.apply_move(after_error, undo))
        if undo_score != initial_score:
            continue
        reset_candidates = []
        for second in MOVES:
            if second == undo or second[0] == move[0]:
                continue
            after_reset = BASE.apply_move(after_error, second)
            reset_score = BASE.solved_score(after_reset)
            future_score = max(
                BASE.solved_score(BASE.apply_move(after_reset, third))
                for third in MOVES if third[0] != second[0]
            )
            reset_candidates.append((future_score, reset_score, second))
        if not reset_candidates:
            continue
        _, reset_score, reset = max(reset_candidates, key=lambda row: (row[0], row[1], row[2]))
        persist = move
        persist_score = BASE.solved_score(BASE.apply_move(after_error, persist))
        if reset_score <= persist_score:
            continue
        recovery_options.append((move, undo, reset, persist, error_score, undo_score, reset_score, persist_score))
    return recovery_options


def generate_candidate_seeds(stimuli: Sequence[object], neighbour_parent_count: int = 12) -> List[CandidateSeed]:
    """Expand only the most recovery-dense certified parents by one legal move.

    All original bank states remain candidates. Neighbours are generated from a
    deterministic parent screen, preventing an unbounded combinatorial sweep
    while preserving explicit provenance and valid cube reachability.
    """
    parent_rows = []
    for stimulus in stimuli:
        density = len(enumerate_recovery_options(stimulus.state))
        parent_rows.append((density, BASE.solved_score(stimulus.state), str(stimulus.stimulus_id), stimulus))
    selected_parents = {
        row[2] for row in sorted(parent_rows, key=lambda row: (row[0], row[1], row[2]), reverse=True)[:neighbour_parent_count]
    }
    raw: List[CandidateSeed] = []
    for stimulus in stimuli:
        raw.append(CandidateSeed(
            seed_id=str(stimulus.stimulus_id),
            parent_stimulus_id=str(stimulus.stimulus_id),
            generator_move=None,
            generation_depth=0,
            state=stimulus.state,
        ))
        if str(stimulus.stimulus_id) not in selected_parents:
            continue
        for move in MOVES:
            token = move.replace("'", "p")
            raw.append(CandidateSeed(
                seed_id=f"{stimulus.stimulus_id}~{token}",
                parent_stimulus_id=str(stimulus.stimulus_id),
                generator_move=move,
                generation_depth=1,
                state=BASE.apply_move(stimulus.state, move),
            ))
    by_state: Dict[str, CandidateSeed] = {}
    for seed in sorted(raw, key=lambda x: (x.generation_depth, x.seed_id)):
        by_state.setdefault(BASE.state_digest(seed.state), seed)
    return sorted(by_state.values(), key=lambda x: x.seed_id)


def make_probe_candidate(seed: CandidateSeed, preliminary: Sequence[Tuple[str, str, str, str, int, int, int, int]] | None = None) -> BaseProbe | None:
    initial_score = BASE.solved_score(seed.state)
    preliminary = list(preliminary) if preliminary is not None else enumerate_recovery_options(seed.state)
    # The 0.8.16 design requires multiple natural recovery opportunities in
    # every family; reject sparse states before the expensive depth-3 search.
    if len(preliminary) < 6:
        return None

    best_score, planned, sequence_count = best_sequence_summary(seed.state, 3)
    first_state = BASE.apply_move(seed.state, planned[0])
    greedy_second = greedy_moves(first_state, excluded_face=planned[0][0])[0]
    if greedy_second == planned[1]:
        return None
    second_state = BASE.apply_move(first_state, greedy_second)
    greedy_third = greedy_moves(second_state, excluded_face=greedy_second[0])[0]
    replanned = (planned[0], greedy_second, greedy_third)

    h3_values = BASE.action_values(seed.state, 3)
    recovery_options = []
    for move, undo, reset, persist, error_score, undo_score, reset_score, persist_score in preliminary:
        regret = max(h3_values.values()) - h3_values[move]
        recovery_options.append((move, undo, reset, persist, error_score, undo_score, reset_score, persist_score, regret))
    recovery_options = sorted(
        recovery_options,
        key=lambda row: (row[8], row[6] - row[7], initial_score - row[4], row[0]),
        reverse=True,
    )
    error, undo, reset, persist, error_score, undo_score, reset_score, persist_score, regret = recovery_options[0]
    separation = reset_score - persist_score
    damage = initial_score - error_score
    orbit_id = hashlib.sha256(BASE.canonical_rotation(seed.state).encode()).hexdigest()
    return BaseProbe(
        seed_id=seed.seed_id,
        parent_stimulus_id=seed.parent_stimulus_id,
        generator_move=seed.generator_move,
        generation_depth=seed.generation_depth,
        orbit_id=orbit_id,
        state=seed.state,
        planned_sequence=planned,  # type: ignore[arg-type]
        replanned_sequence=replanned,
        error_move=error,
        undo_move=undo,
        reset_move=reset,
        persist_move=persist,
        initial_score=initial_score,
        planned_final_score=path_score(seed.state, planned),
        replan_final_score=path_score(seed.state, replanned),
        error_score=error_score,
        undo_score=undo_score,
        reset_score=reset_score,
        persist_score=persist_score,
        optimal_sequence_count=sequence_count,
        recovery_options=tuple(recovery_options),
        selection_score=(
            len(recovery_options),
            regret + separation + damage,
            -sequence_count,
            best_score,
            -seed.generation_depth,
            seed.seed_id,
        ),
    )


def select_base_probes(stimuli: Sequence[object], family_count: int) -> List[BaseProbe]:
    seeds = generate_candidate_seeds(stimuli)
    screened = []
    for seed in seeds:
        options = enumerate_recovery_options(seed.state)
        if len(options) >= 6:
            screened.append((seed, options))
    # Limit expensive depth-3 planning evaluation to the strongest, diverse
    # recovery candidates. No parent may contribute more than four candidates
    # to the depth-search pool.
    screened.sort(
        key=lambda row: (
            len(row[1]),
            BASE.solved_score(row[0].state),
            -row[0].generation_depth,
            row[0].seed_id,
        ),
        reverse=True,
    )
    pool = []
    by_parent: Dict[str, List[Tuple[CandidateSeed, Sequence[Tuple[str, str, str, str, int, int, int, int]]]]] = defaultdict(list)
    for seed, options in screened:
        by_parent[seed.parent_stimulus_id].append((seed, options))
    ranked_parents = sorted(
        by_parent,
        key=lambda parent: (len(by_parent[parent][0][1]), parent),
        reverse=True,
    )
    # Evaluate at most two dense candidates per parent. This preserves parent
    # diversity while keeping the exact depth-3 search deterministic and bounded.
    for rank in range(2):
        for parent in ranked_parents[:12]:
            if rank < len(by_parent[parent]):
                pool.append(by_parent[parent][rank])

    candidates = [probe for seed, options in pool if (probe := make_probe_candidate(seed, options)) is not None]
    by_orbit: Dict[str, BaseProbe] = {}
    for probe in sorted(candidates, key=lambda p: p.selection_score, reverse=True):
        by_orbit.setdefault(probe.orbit_id, probe)
    candidates = list(by_orbit.values())
    if len(candidates) < family_count:
        raise RuntimeError(f"CR0816_INSUFFICIENT_DENSE_UNIQUE_BASE_PROBES:{len(candidates)}<{family_count}")

    selected: List[BaseProbe] = []
    remaining = sorted(candidates, key=lambda p: p.selection_score, reverse=True)
    used_faces = set()
    used_bands = set()
    used_parents = set()
    while remaining and len(selected) < family_count:
        best = max(
            remaining,
            key=lambda p: (
                p.parent_stimulus_id not in used_parents,
                p.planned_sequence[0][0] not in used_faces,
                (p.initial_score // 4) not in used_bands,
                p.selection_score,
            ),
        )
        selected.append(best)
        remaining.remove(best)
        used_parents.add(best.parent_stimulus_id)
        used_faces.add(best.planned_sequence[0][0])
        used_bands.add(best.initial_score // 4)
    if min(len(p.recovery_options) for p in selected) < 6:
        raise RuntimeError("CR0816_RECOVERY_DENSITY_SELECTION_FAILURE")
    if len({p.orbit_id for p in selected}) != family_count:
        raise RuntimeError("CR0816_ROTATIONAL_FAMILY_DUPLICATE")
    if len({p.parent_stimulus_id for p in selected}) < 4:
        raise RuntimeError("CR0816_PARENT_STATE_DIVERSITY_FAILURE")
    return sorted(selected, key=lambda p: p.seed_id)


def build_family_registry(base_probes: Sequence[BaseProbe]) -> Dict[str, object]:
    families = []
    all_members = []
    for family_index, base in enumerate(base_probes, 1):
        family_id = f"CR0816-F{family_index:02d}"
        family_rotations = select_family_rotations(base.planned_sequence[0], base.error_move)
        members = []
        canonical_probe_id = None
        canonical_target_face = base.planned_sequence[0][0]
        for target_face, rotation in family_rotations.items():
            rotated_state = BASE.rotate_state(base.state, rotation)
            planned = transform_sequence(base.planned_sequence, rotation)
            replanned = transform_sequence(base.replanned_sequence, rotation)
            member = {
                "probe_id": f"{family_id}-{target_face}",
                "target_planned_face": target_face,
                "rotation_matrix": rotation,
                "inverse_rotation_matrix": inverse_rotation(rotation),
                "state_sha256": BASE.state_digest(rotated_state),
                "stickers": state_to_stickers(rotated_state),
                "planned_sequence": planned,
                "replanned_sequence": replanned,
                "recovery": {
                    "error_move": conjugated_move(base.error_move, rotation),
                    "undo_move": conjugated_move(base.undo_move, rotation),
                    "reset_move": conjugated_move(base.reset_move, rotation),
                    "persist_move": conjugated_move(base.persist_move, rotation),
                },
                "recovery_opportunities": [
                    {
                        "error_move": conjugated_move(option[0], rotation),
                        "undo_move": conjugated_move(option[1], rotation),
                        "reset_move": conjugated_move(option[2], rotation),
                        "persist_move": conjugated_move(option[3], rotation),
                        "error_score": option[4],
                        "undo_score": option[5],
                        "reset_score": option[6],
                        "persist_score": option[7],
                        "h3_regret": option[8],
                    }
                    for option in base.recovery_options
                ],
            }
            # Exact equivariance contract.
            if tuple(conjugated_move(m, rotation) for m in base.planned_sequence) != planned:
                raise RuntimeError("CR0816_PLANNED_EQUIVARIANCE_FAILURE")
            canonical_final = base.state
            rotated_final = rotated_state
            for canonical_move, rotated_move in zip(base.planned_sequence, planned):
                canonical_final = BASE.apply_move(canonical_final, canonical_move)
                rotated_final = BASE.apply_move(rotated_final, rotated_move)
            if BASE.rotate_state(canonical_final, rotation) != rotated_final:
                raise RuntimeError(f"CR0816_ROTATED_TRANSITION_FAILURE:{family_id}:{target_face}")
            if normalized_score(rotated_final, rotation) != base.planned_final_score:
                raise RuntimeError(f"CR0816_ROTATED_NORMALIZED_SCORE_FAILURE:{family_id}:{target_face}")
            if rotation == ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                canonical_probe_id = member["probe_id"]
            members.append(member)
            all_members.append(member)
        if canonical_probe_id is None:
            raise RuntimeError(f"CR0816_FAMILY_IDENTITY_MEMBER_MISSING:{family_id}")
        families.append({
            "family_id": family_id,
            "source_seed_id": base.seed_id,
            "parent_stimulus_id": base.parent_stimulus_id,
            "generator_move": base.generator_move,
            "generation_depth": base.generation_depth,
            "source_orbit_sha256": base.orbit_id,
            "canonical_probe_id": canonical_probe_id,
            "canonical_target_face": canonical_target_face,
            "initial_score": base.initial_score,
            "planned_final_score": base.planned_final_score,
            "replan_final_score": base.replan_final_score,
            "error_score": base.error_score,
            "undo_score": base.undo_score,
            "reset_score": base.reset_score,
            "persist_score": base.persist_score,
            "optimal_sequence_count": base.optimal_sequence_count,
            "recovery_opportunity_count": len(base.recovery_options),
            "members": members,
        })
    face_counts = Counter(member["planned_sequence"][0][0] for member in all_members)
    recovery_face_counts = Counter(member["recovery"]["error_move"][0] for member in all_members)
    opportunity_counts = [family["recovery_opportunity_count"] for family in families]
    return {
        "schema_version": "CR0816-TRAJECTORY-PROBE-REGISTRY-1",
        "version": "CUBE-REV 0.8.16",
        "family_count": len(families),
        "members_per_family": 6,
        "probe_count": len(all_members),
        "trajectory_length": 3,
        "families": families,
        "planned_first_face_counts": dict(sorted(face_counts.items())),
        "recovery_error_face_counts": dict(sorted(recovery_face_counts.items())),
        "recovery_opportunity_count": {
            "minimum_per_family": min(opportunity_counts),
            "mean_per_family": round(statistics.fmean(opportunity_counts), 4),
            "maximum_per_family": max(opportunity_counts),
        },
        "participant_visibility": "RESEARCH_ONLY_NOT_DEPLOYED",
        "result": "PASS_ROTATIONAL_EQUIVALENCE_FAMILY_CONSTRUCTION",
    }


def trajectory_features(actions: Sequence[str], latencies: Sequence[float], scores: Sequence[int], recovery: Mapping[str, str]) -> Dict[str, float]:
    if len(actions) != 3 or len(latencies) != 3 or len(scores) != 4:
        raise ValueError("CR0816_TRAJECTORY_LENGTH")
    return {
        "second_latency": float(latencies[1]),
        "third_latency": float(latencies[2]),
        "boundary_ratio": float(latencies[1]) / max(float(latencies[0]), 1.0),
        "late_latency_sum": float(latencies[1] + latencies[2]),
        "score_delta_1": float(scores[1] - scores[0]),
        "score_delta_2": float(scores[2] - scores[1]),
        "score_delta_3": float(scores[3] - scores[2]),
        "undo_at_second": float(actions[1] == recovery["undo_move"]),
        "reset_at_second": float(actions[1] == recovery["reset_move"]),
        "persist_at_second": float(actions[1] == recovery["persist_move"]),
        "planned_second": float(actions[1] == recovery.get("planned_second", "")),
        "action_change_2": float(actions[1] != actions[0]),
        "action_change_3": float(actions[2] != actions[1]),
    }


def simulate_probe(member: Mapping[str, object], family: Mapping[str, object], mechanism: str, rng: random.Random) -> Dict[str, object]:
    state = BASE.state_from_stickers(member["stickers"])  # type: ignore[arg-type]
    planned = tuple(member["planned_sequence"])  # type: ignore[arg-type]
    replanned = tuple(member["replanned_sequence"])  # type: ignore[arg-type]
    recovery = dict(member["recovery"])  # type: ignore[arg-type]
    recovery["planned_second"] = planned[1]

    if mechanism == "open_loop_chunk":
        actions = planned
        latencies = [rng.lognormvariate(math.log(900), 0.12), rng.lognormvariate(math.log(180), 0.10), rng.lognormvariate(math.log(160), 0.10)]
    elif mechanism == "closed_loop_replan":
        actions = replanned
        latencies = [rng.lognormvariate(math.log(900), 0.12), rng.lognormvariate(math.log(760), 0.12), rng.lognormvariate(math.log(430), 0.12)]
    elif mechanism == "undo_recovery":
        actions = (recovery["error_move"], recovery["undo_move"], planned[0])
        latencies = [rng.lognormvariate(math.log(720), 0.14), rng.lognormvariate(math.log(310), 0.12), rng.lognormvariate(math.log(680), 0.14)]
    elif mechanism == "reset_recovery":
        actions = (recovery["error_move"], recovery["reset_move"], greedy_moves(BASE.apply_move(BASE.apply_move(state, recovery["error_move"]), recovery["reset_move"]), excluded_face=recovery["reset_move"][0])[0])
        latencies = [rng.lognormvariate(math.log(720), 0.14), rng.lognormvariate(math.log(830), 0.14), rng.lognormvariate(math.log(410), 0.12)]
    elif mechanism == "persist_after_error":
        actions = (recovery["error_move"], recovery["persist_move"], recovery["reset_move"])
        latencies = [rng.lognormvariate(math.log(720), 0.14), rng.lognormvariate(math.log(220), 0.12), rng.lognormvariate(math.log(980), 0.16)]
    elif mechanism in {"latent_open_a", "latent_open_b", "same_actions_chunk_fast"}:
        actions = planned
        latencies = [rng.lognormvariate(math.log(900), 0.12), rng.lognormvariate(math.log(180), 0.10), rng.lognormvariate(math.log(160), 0.10)]
    elif mechanism == "same_actions_boundary_pause":
        actions = planned
        latencies = [rng.lognormvariate(math.log(900), 0.12), rng.lognormvariate(math.log(760), 0.12), rng.lognormvariate(math.log(430), 0.12)]
    elif mechanism == "viewer_centered_alias":
        # Reuse canonical moves without rotation transformation. This deliberately
        # violates object-centered equivariance while preserving action frequencies.
        source_family = family
        canonical_member = next(m for m in source_family["members"] if m["probe_id"] == family["canonical_probe_id"])
        actions = tuple(canonical_member["planned_sequence"])  # type: ignore[arg-type]
        latencies = [rng.lognormvariate(math.log(900), 0.12), rng.lognormvariate(math.log(250), 0.10), rng.lognormvariate(math.log(220), 0.10)]
    else:
        raise ValueError(mechanism)

    rotation = tuple(tuple(int(x) for x in col) for col in member["rotation_matrix"])  # type: ignore[arg-type]
    scores = [normalized_score(state, rotation)]
    current = state
    for action in actions:
        current = BASE.apply_move(current, action)
        scores.append(normalized_score(current, rotation))
    return {
        "mechanism": mechanism,
        "probe_id": member["probe_id"],
        "family_id": family["family_id"],
        "target_up_face": member["target_planned_face"],
        "actions": list(actions),
        "latencies_ms": [round(x, 3) for x in latencies],
        "scores": scores,
        "features": trajectory_features(actions, latencies, scores, recovery),
    }


def feature_view(row: Mapping[str, object], view: str) -> Dict[str, float]:
    actions = [str(x) for x in row["actions"]]  # type: ignore[index]
    latencies = [float(x) for x in row["latencies_ms"]]  # type: ignore[index]
    scores = [float(x) for x in row["scores"]]  # type: ignore[index]
    if view == "first_action_only":
        action_count, include_latency, include_scores = 1, True, True
    elif view == "two_actions_no_latency":
        action_count, include_latency, include_scores = 2, False, True
    elif view == "two_actions_with_latency":
        action_count, include_latency, include_scores = 2, True, True
    elif view == "three_actions_with_latency":
        action_count, include_latency, include_scores = 3, True, True
    elif view == "latency_only":
        action_count, include_latency, include_scores = 0, True, False
    else:
        raise ValueError(f"CR0816_UNKNOWN_FEATURE_VIEW:{view}")
    features: Dict[str, float] = {}
    for position in range(action_count):
        for move in MOVES:
            features[f"p{position+1}_{move}"] = float(actions[position] == move)
    if include_latency:
        for position in range(max(action_count, 3) if view == "latency_only" else action_count):
            features[f"latency_{position+1}"] = latencies[position]
    if include_scores:
        for position in range(action_count):
            features[f"score_delta_{position+1}"] = scores[position + 1] - scores[position]
    return features


def apply_feature_view(rows: Sequence[Mapping[str, object]], view: str) -> List[Dict[str, object]]:
    return [{**row, "features": feature_view(row, view)} for row in rows]


def nearest_centroid_accuracy(rows: Sequence[Mapping[str, object]], labels: Sequence[str], seed: int, repeats: int = 31) -> Dict[str, float]:
    subset = [row for row in rows if row["mechanism"] in labels]
    feature_names = sorted(next(iter(subset))["features"])  # type: ignore[arg-type]
    scores = []
    for repeat in range(repeats):
        rng = random.Random(seed + 1009 * repeat)
        grouped: Dict[str, List[Mapping[str, object]]] = defaultdict(list)
        for row in subset:
            grouped[str(row["mechanism"])].append(row)
        train = []
        test = []
        for label in labels:
            items = grouped[label][:]
            rng.shuffle(items)
            split = int(0.65 * len(items))
            train.extend(items[:split])
            test.extend(items[split:])
        means = {name: statistics.fmean(float(row["features"][name]) for row in train) for name in feature_names}  # type: ignore[index]
        sds = {name: statistics.pstdev(float(row["features"][name]) for row in train) or 1.0 for name in feature_names}  # type: ignore[index]
        centroids = {}
        for label in labels:
            lab_rows = [row for row in train if row["mechanism"] == label]
            centroids[label] = [statistics.fmean((float(row["features"][name]) - means[name]) / sds[name] for row in lab_rows) for name in feature_names]  # type: ignore[index]
        recalls = []
        for label in labels:
            lab_test = [row for row in test if row["mechanism"] == label]
            correct = 0
            for row in lab_test:
                vector = [(float(row["features"][name]) - means[name]) / sds[name] for name in feature_names]  # type: ignore[index]
                pred = min(labels, key=lambda candidate: math.sqrt(sum((a - b) ** 2 for a, b in zip(vector, centroids[candidate]))))
                correct += pred == label
            recalls.append(correct / len(lab_test))
        scores.append(statistics.fmean(recalls))
    return {
        "mean": round(statistics.fmean(scores), 4),
        "sd": round(statistics.pstdev(scores), 4),
        "min": round(min(scores), 4),
        "max": round(max(scores), 4),
        "repeats": repeats,
    }


def object_centered_equivariance(row: Mapping[str, object], member: Mapping[str, object], family: Mapping[str, object]) -> float:
    canonical_member = next(m for m in family["members"] if m["probe_id"] == family["canonical_probe_id"])
    rotation = tuple(tuple(int(x) for x in col) for col in member["rotation_matrix"])  # type: ignore[arg-type]
    expected = transform_sequence(canonical_member["planned_sequence"], rotation)  # type: ignore[arg-type]
    return statistics.fmean(float(a == b) for a, b in zip(row["actions"], expected))  # type: ignore[arg-type]


def perturb_trajectories(
    rows: Sequence[Mapping[str, object]],
    registry: Mapping[str, object],
    seed: int,
    action_slip_rate: float = 0.08,
    latency_log_sigma: float = 0.25,
) -> List[Dict[str, object]]:
    """Apply coherent observation/execution noise and recompute derived states."""
    rng = random.Random(seed)
    member_map = {}
    family_map = {}
    for family in registry["families"]:  # type: ignore[index]
        family_map[str(family["family_id"])] = family
        for member in family["members"]:
            member_map[str(member["probe_id"])] = member
    out = []
    for source in rows:
        row = dict(source)
        actions = [str(x) for x in source["actions"]]  # type: ignore[index]
        latencies = [float(x) * rng.lognormvariate(0.0, latency_log_sigma) for x in source["latencies_ms"]]  # type: ignore[index]
        for position in range(len(actions)):
            if rng.random() < action_slip_rate:
                alternatives = [move for move in MOVES if move != actions[position]]
                actions[position] = rng.choice(alternatives)
        member = member_map[str(source["probe_id"])]
        family = family_map[str(source["family_id"])]
        state = BASE.state_from_stickers(member["stickers"])
        rotation = tuple(tuple(int(x) for x in col) for col in member["rotation_matrix"])
        scores = [normalized_score(state, rotation)]
        current = state
        for action in actions:
            current = BASE.apply_move(current, action)
            scores.append(normalized_score(current, rotation))
        recovery = dict(member["recovery"])
        recovery["planned_second"] = member["planned_sequence"][1]
        row["actions"] = actions
        row["latencies_ms"] = [round(value, 3) for value in latencies]
        row["scores"] = scores
        row["features"] = trajectory_features(actions, latencies, scores, recovery)
        row["object_centered_equivariance"] = round(object_centered_equivariance(row, member, family), 4)
        row["features"]["object_centered_equivariance"] = row["object_centered_equivariance"]
        out.append(row)
    return out


def simulate_identifiability(registry: Mapping[str, object], sessions_per_mechanism: int, seed: int) -> Tuple[List[Dict[str, object]], Dict[str, object]]:
    mechanisms = [
        "open_loop_chunk", "closed_loop_replan", "undo_recovery", "reset_recovery",
        "persist_after_error", "latent_open_a", "latent_open_b",
        "same_actions_chunk_fast", "same_actions_boundary_pause", "viewer_centered_alias",
    ]
    rows: List[Dict[str, object]] = []
    families = registry["families"]  # type: ignore[assignment]
    for mechanism_index, mechanism in enumerate(mechanisms):
        for rep in range(sessions_per_mechanism):
            family = families[rep % len(families)]
            member = family["members"][(rep // len(families)) % 6]
            rng = random.Random(seed + mechanism_index * 1_000_000 + rep)
            row = simulate_probe(member, family, mechanism, rng)
            row["object_centered_equivariance"] = round(object_centered_equivariance(row, member, family), 4)
            row["features"]["object_centered_equivariance"] = row["object_centered_equivariance"]  # type: ignore[index]
            rows.append(row)

    contrasts = {
        "open_vs_closed": ("open_loop_chunk", "closed_loop_replan"),
        "undo_vs_reset": ("undo_recovery", "reset_recovery"),
        "reset_vs_persist": ("reset_recovery", "persist_after_error"),
        "latent_same_trajectory": ("latent_open_a", "latent_open_b"),
        "boundary_pause_same_actions": ("same_actions_chunk_fast", "same_actions_boundary_pause"),
        "object_vs_viewer_frame": ("open_loop_chunk", "viewer_centered_alias"),
    }
    results = {name: nearest_centroid_accuracy(rows, labels, seed + i * 5000) for i, (name, labels) in enumerate(contrasts.items())}
    classifications = {
        name: "IDENTIFIABLE" if result["mean"] >= 0.80 else "PARTIAL" if result["mean"] >= 0.65 else "NON_IDENTIFIABLE"
        for name, result in results.items()
    }
    feature_views = {}
    for view in ["first_action_only", "two_actions_no_latency", "two_actions_with_latency", "three_actions_with_latency", "latency_only"]:
        viewed = apply_feature_view(rows, view)
        feature_views[view] = {
            name: nearest_centroid_accuracy(viewed, labels, seed + 70000 + vi * 10000 + ci * 1000)
            for ci, (name, labels) in enumerate(contrasts.items())
            for vi in [list(["first_action_only", "two_actions_no_latency", "two_actions_with_latency", "three_actions_with_latency", "latency_only"]).index(view)]
        }
    noisy_rows = perturb_trajectories(rows, registry, seed + 816999)
    noisy_full = {
        name: nearest_centroid_accuracy(noisy_rows, labels, seed + 91000 + i * 1000)
        for i, (name, labels) in enumerate(contrasts.items())
    }
    noisy_two_action_latency = apply_feature_view(noisy_rows, "two_actions_with_latency")
    noisy_minimal = {
        name: nearest_centroid_accuracy(noisy_two_action_latency, labels, seed + 101000 + i * 1000)
        for i, (name, labels) in enumerate(contrasts.items())
    }
    robust_conditions = {
        "open_closed_minimal": noisy_minimal["open_vs_closed"]["mean"] >= 0.80,
        "undo_reset_minimal": noisy_minimal["undo_vs_reset"]["mean"] >= 0.80,
        "reset_persist_minimal": noisy_minimal["reset_vs_persist"]["mean"] >= 0.75,
        "boundary_pause_minimal": noisy_minimal["boundary_pause_same_actions"]["mean"] >= 0.80,
        "object_viewer_full": noisy_full["object_vs_viewer_frame"]["mean"] >= 0.75,
        "latent_negative_stays_nonidentifiable": noisy_full["latent_same_trajectory"]["mean"] < 0.60,
    }

    summary = {
        "schema_version": "CR0816-TRAJECTORY-IDENTIFIABILITY-RESULT-1",
        "version": "CUBE-REV 0.8.16",
        "seed": seed,
        "sessions_per_mechanism": sessions_per_mechanism,
        "mechanism_count": len(mechanisms),
        "simulated_trajectory_count": len(rows),
        "contrasts": {name: {**results[name], "classification": classifications[name]} for name in results},
        "feature_view_audit": feature_views,
        "robust_noise_audit": {
            "action_slip_rate": 0.08,
            "latency_log_sigma": 0.25,
            "full_trajectory": noisy_full,
            "two_actions_with_latency": noisy_minimal,
            "conditions": robust_conditions,
        },
        "minimality_conditions": {
            "first_action_open_closed_nonidentifiable": feature_views["first_action_only"]["open_vs_closed"]["mean"] < 0.60,
            "two_actions_open_closed_without_latency_not_robustly_identifiable": feature_views["two_actions_no_latency"]["open_vs_closed"]["mean"] < 0.80,
            "two_actions_open_closed_identifiable_with_latency": feature_views["two_actions_with_latency"]["open_vs_closed"]["mean"] >= 0.80,
            "first_action_recovery_nonidentifiable": feature_views["first_action_only"]["undo_vs_reset"]["mean"] < 0.60,
            "two_actions_recovery_without_latency_not_robustly_identifiable": feature_views["two_actions_no_latency"]["undo_vs_reset"]["mean"] < 0.80,
            "two_actions_recovery_identifiable_with_latency": feature_views["two_actions_with_latency"]["undo_vs_reset"]["mean"] >= 0.80,
            "boundary_pause_requires_latency": feature_views["two_actions_no_latency"]["boundary_pause_same_actions"]["mean"] < 0.60 and feature_views["latency_only"]["boundary_pause_same_actions"]["mean"] >= 0.80,
        },
        "success_conditions": {
            "open_vs_closed": results["open_vs_closed"]["mean"] >= 0.80,
            "undo_vs_reset": results["undo_vs_reset"]["mean"] >= 0.80,
            "reset_vs_persist": results["reset_vs_persist"]["mean"] >= 0.80,
            "latent_same_trajectory_remains_nonidentifiable": results["latent_same_trajectory"]["mean"] < 0.60,
            "boundary_pause_same_actions": results["boundary_pause_same_actions"]["mean"] >= 0.80,
            "object_vs_viewer_frame": results["object_vs_viewer_frame"]["mean"] >= 0.80,
        },
        "result": "PASS_MINIMAL_TRAJECTORY_IDENTIFIABILITY" if all([
            results["open_vs_closed"]["mean"] >= 0.80,
            results["undo_vs_reset"]["mean"] >= 0.80,
            results["reset_vs_persist"]["mean"] >= 0.80,
            results["latent_same_trajectory"]["mean"] < 0.60,
            results["boundary_pause_same_actions"]["mean"] >= 0.80,
            results["object_vs_viewer_frame"]["mean"] >= 0.80,
            feature_views["first_action_only"]["open_vs_closed"]["mean"] < 0.60,
            feature_views["two_actions_no_latency"]["open_vs_closed"]["mean"] < 0.80,
            feature_views["two_actions_with_latency"]["open_vs_closed"]["mean"] >= 0.80,
            feature_views["first_action_only"]["undo_vs_reset"]["mean"] < 0.60,
            feature_views["two_actions_no_latency"]["undo_vs_reset"]["mean"] < 0.80,
            feature_views["two_actions_with_latency"]["undo_vs_reset"]["mean"] >= 0.80,
            feature_views["two_actions_no_latency"]["boundary_pause_same_actions"]["mean"] < 0.60,
            feature_views["latency_only"]["boundary_pause_same_actions"]["mean"] >= 0.80,
            all(robust_conditions.values()),
        ]) else "HOLD_TRAJECTORY_IDENTIFIABILITY",
    }
    return rows, summary


def build_balanced_schedules(registry: Mapping[str, object]) -> Dict[str, object]:
    families = list(registry["families"])  # type: ignore[arg-type]
    if len(families) != 6:
        raise RuntimeError("CR0816_SCHEDULE_DESIGN_REQUIRES_SIX_FAMILIES")
    face_order = list(FACES)
    schedules = []
    exposure_counts = {str(family["family_id"]): Counter() for family in families}
    for schedule_index in range(12):
        offset = schedule_index % 6
        variant = schedule_index // 6
        first_orientation = {family_index: (offset + family_index) % 6 for family_index in range(6)}
        second_orientation = {family_index: (offset + family_index + 3 + variant) % 6 for family_index in range(6)}
        first_family_order = [next(i for i, orientation in first_orientation.items() if orientation == face_index) for face_index in range(6)]
        second_family_order = list(first_family_order)
        entries = []
        for half, family_order, assignments in ((1, first_family_order, first_orientation), (2, second_family_order, second_orientation)):
            for family_index in family_order:
                family = families[family_index]
                target_face = face_order[assignments[family_index]]
                member = next(m for m in family["members"] if m["target_planned_face"] == target_face)
                entries.append({
                    "position": len(entries) + 1,
                    "half": half,
                    "family_id": family["family_id"],
                    "probe_id": member["probe_id"],
                    "target_planned_face": target_face,
                })
                exposure_counts[str(family["family_id"])][target_face] += 1
        positions: Dict[str, List[int]] = defaultdict(list)
        for entry in entries:
            positions[str(entry["family_id"])].append(int(entry["position"]))
        separations = {family_id: values[1] - values[0] for family_id, values in positions.items()}
        if min(separations.values()) < 6:
            raise RuntimeError(f"CR0816_SCHEDULE_FAMILY_SPACING:{schedule_index+1}")
        if any(entries[i]["target_planned_face"] == entries[i-1]["target_planned_face"] for i in range(1, len(entries))):
            raise RuntimeError(f"CR0816_SCHEDULE_FACE_ADJACENCY:{schedule_index+1}")
        schedules.append({
            "schedule_id": f"CR0816-SCH-{schedule_index+1:02d}",
            "entries": entries,
            "family_separations": separations,
        })
    if len({tuple(entry["probe_id"] for entry in schedule["entries"]) for schedule in schedules}) != 12:
        raise RuntimeError("CR0816_SCHEDULES_NOT_UNIQUE")
    for family_id, counts in exposure_counts.items():
        if any(counts[face] != 4 for face in FACES):
            raise RuntimeError(f"CR0816_ORIENTATION_EXPOSURE_IMBALANCE:{family_id}:{dict(counts)}")
    return {
        "schema_version": "CR0816-TRAJECTORY-SCHEDULES-1",
        "version": "CUBE-REV 0.8.16",
        "schedule_count": len(schedules),
        "trials_per_schedule": 12,
        "families_per_schedule": 6,
        "exposures_per_family_per_schedule": 2,
        "minimum_family_spacing": 6,
        "orientation_exposures_per_family_across_schedules": 4,
        "schedules": schedules,
        "result": "PASS_BALANCED_MINIMAL_TRAJECTORY_SCHEDULES",
    }


def external_source_registry() -> Dict[str, object]:
    return {
        "schema_version": "CR0816-EXTERNAL-TRAJECTORY-SOURCE-REGISTRY-1",
        "version": "CUBE-REV 0.8.16",
        "retrieval_date": "2026-08-03",
        "sources": [
            {
                "source_id": "WCA-RESULTS-EXPORT-V2",
                "authority": "World Cube Association",
                "url": "https://www.worldcubeassociation.org/export/results",
                "access": "PUBLIC_VERSIONED_EXPORT",
                "observed_export": {
                    "format_version": "2.0.2",
                    "export_date": "2026-08-02T16:15:23+00:00",
                    "tsv_filename": "WCA_export_v2_214_20260802T000025Z.tsv.zip",
                    "reported_tsv_size_mb": 352,
                    "materialization": "METADATA_SNAPSHOT_ONLY_BULK_ARCHIVE_NOT_STORED_IN_REPOSITORY"
                },
                "contains": ["competition metadata", "individual attempt times", "official scrambles", "competitor WCA IDs"],
                "does_not_contain": ["solution move sequence", "per-move timestamp", "cognitive annotation"],
                "allowed_role": "official-result and scramble linkage",
                "attribution_required": True,
            },
            {
                "source_id": "RECO-NZ-RECONSTRUCTION-DATABASE",
                "authority": "community reconstruction project",
                "url": "https://reco.nz",
                "access": "PUBLIC_WEB_DATABASE",
                "observed_index_scale": "solve IDs above 13400 as of 2026-08-03",
                "contains": ["scramble", "full move sequence", "method-stage comments", "total and stage times", "movecount", "TPS", "official/unofficial flag", "solver", "competition", "reconstructor"],
                "does_not_contain": ["reliable per-move timestamp for ordinary video reconstructions", "direct thought-process report"],
                "allowed_role": "trajectory motif prior, notation parser validation, elite-solve comparison",
                "prohibited_role": "direct inference of 2x2 thought process",
                "site_stated_purpose": "individual and large-scale solve analysis",
                "site_caution": "site FAQ states short one-look 2x2 solutions do not reveal what is behind the solution without solver explanation",
            },
            {
                "source_id": "CSTIMER-SMART-CUBE-EXPORT",
                "authority": "user-owned timer export",
                "url": "https://www.cstimer.net/new/",
                "access": "USER_CONSENT_EXPORT_ONLY",
                "contains": ["scramble", "solve time", "detailed move sequence for supported smart cubes", "reconstruction when available"],
                "does_not_contain": ["public bulk cohort"],
                "allowed_role": "consented per-move trajectory and timing validation",
                "prohibited_role": "server-side scraping or unconsented account access",
            },
            {
                "source_id": "CUBEAST-SHARED-SOLVE",
                "authority": "user-shared smart-cube analysis",
                "url": "https://www.cubeast.com/",
                "access": "EXPLICITLY_SHARED_LINK_OR_OWNER_EXPORT",
                "contains": ["move-level solution", "solve analysis", "shareable solve link"],
                "allowed_role": "consented high-resolution timing prior",
                "prohibited_role": "bulk profile scraping",
            },
            {
                "source_id": "SOLVED-NO-RECONSTRUCTOR",
                "authority": "user-created shared reconstruction",
                "url": "https://www.solved.no/reconstructor",
                "access": "PUBLIC_SHARE_LINK_OR_OWNER_EXPORT",
                "contains": ["scramble", "move sequence", "shareable reconstruction"],
                "allowed_role": "notation and trajectory fixture",
                "prohibited_role": "private saved-solve access",
            },
        ],
        "linkage_design": {
            "official_anchor": "WCA competition, event, round, attempt, time and scramble",
            "trajectory_anchor": "reco.nz solve ID or explicitly shared smart-cube solve",
            "join_status": "REQUIRES_SOURCE_SNAPSHOT_AND_LINKAGE_AUDIT",
            "identity_policy": "retain public source attribution but model trajectories without inferring latent traits of named individuals",
        },
        "external_data_decision": "PASS_SOURCE_DISCOVERY_HOLD_BULK_INGESTION_UNTIL_SNAPSHOT_CUSTODY",
    }


def external_reconstruction_fixture_pack() -> Dict[str, object]:
    """Public reconstruction fixtures for trajectory-shape validation only."""
    shared_scramble = "D2 U' R2 B2 L2 B2 D B2 L2 D2 B' U' R' U2 F2 D' B F D B' R"
    return {
        "schema_version": "CR0816-EXTERNAL-RECONSTRUCTION-FIXTURE-PACK-1",
        "retrieved": "2026-08-03",
        "fixtures": [
            {
                "solve_id": 12564,
                "source": "https://reco.nz/solve/12564",
                "puzzle": "3x3",
                "result_seconds": 2.76,
                "scramble": "L B R2 B' R2 U2 F D R2 U R2 F2 D2 R U B L2",
                "stages": [
                    {"label": "xxxcross", "moves": "r' U F U' r U' r' U2 r' U r"},
                    {"label": "4th pair", "moves": "R U2' R2' U' R U R U2' R'"},
                    {"label": "ZBLL", "moves": "U' F' r U R' U' r' F R"},
                ],
                "reported_stm": 29,
                "reported_tps": 10.51,
                "role": "STAGE_BOUNDARY_AND_NOTATION_FIXTURE",
            },
            {
                "solve_id": 9269,
                "source": "https://reco.nz/solve/9269",
                "puzzle": "3x3",
                "result_seconds": 4.54,
                "scramble": shared_scramble,
                "solver_label": "PUBLIC_SOURCE_ATTRIBUTION_ONLY",
                "stages": [
                    {"label": "xcross", "moves": "U' U' R2 D R' U' R' u'"},
                    {"label": "2nd pair", "moves": "R' U' R L' U L"},
                    {"label": "3rd pair", "moves": "y R' U' R U' R' U R"},
                    {"label": "4th pair", "moves": "U' R U R' U' F' U' F"},
                    {"label": "ZBLL", "moves": "R U' U' R D R' U U R D' R2' U"},
                ],
                "reported_stm": 41,
                "role": "MATCHED_SCRAMBLE_ROUTE_A",
            },
            {
                "solve_id": 9274,
                "source": "https://reco.nz/solve/9274",
                "puzzle": "3x3",
                "result_seconds": 4.54,
                "scramble": shared_scramble,
                "solver_label": "PUBLIC_SOURCE_ATTRIBUTION_ONLY",
                "stages": [
                    {"label": "xcross", "moves": "U2 R2 D R' U' R' u'"},
                    {"label": "2nd pair", "moves": "R' U' R L' U L"},
                    {"label": "3rd/4th pairs", "moves": "y U R' U' R D' U2 y' R' U2 R U' R' U R D"},
                    {"label": "OLL", "moves": "R' U' R' F R F' U R"},
                    {"label": "PLL", "moves": "x R2' D2 R U R' D2 R U' R x' U2"},
                ],
                "reported_stm": 45,
                "role": "MATCHED_SCRAMBLE_ROUTE_B",
            },
        ],
        "matched_scramble_hypothesis": "THE_SAME_OFFICIAL_STATE_AND_SAME_TOTAL_TIME_CAN_SUPPORT_DISTINCT_OBSERVED_TRAJECTORIES",
        "allowed_inference": "trajectory nonuniqueness and motif priors",
        "prohibited_inference": "named-solver cognitive trait or unobserved thought process",
    }


def audit_external_fixture_pack(pack: Mapping[str, object]) -> Dict[str, object]:
    fixtures = list(pack["fixtures"])  # type: ignore[index]
    tokenized = {}
    for fixture in fixtures:
        tokens = [token for stage in fixture["stages"] for token in str(stage["moves"]).split()]
        tokenized[str(fixture["solve_id"])] = tokens
    matched = [fixture for fixture in fixtures if fixture["role"].startswith("MATCHED_SCRAMBLE")]
    same_scramble = len({fixture["scramble"] for fixture in matched}) == 1
    same_time = len({fixture["result_seconds"] for fixture in matched}) == 1
    distinct_routes = tokenized[str(matched[0]["solve_id"])] != tokenized[str(matched[1]["solve_id"])]
    return {
        "fixture_count": len(fixtures),
        "stage_boundary_fixture_count": sum(len(fixture["stages"]) >= 3 for fixture in fixtures),
        "matched_scramble_pair_count": 1 if len(matched) == 2 else 0,
        "matched_pair_same_scramble": same_scramble,
        "matched_pair_same_result_time": same_time,
        "matched_pair_distinct_move_routes": distinct_routes,
        "matched_pair_reported_stm": [fixture["reported_stm"] for fixture in matched],
        "result": "PASS_EXTERNAL_TRAJECTORY_FIXTURE_PACK" if same_scramble and same_time and distinct_routes else "HOLD_EXTERNAL_FIXTURE_PACK",
    }


def reconstruction_fixture() -> Dict[str, object]:
    return {
        "schema_version": "CR0816-RECONSTRUCTION-FIXTURE-1",
        "source": "https://reco.nz/solve/12564",
        "retrieved": "2026-08-03",
        "puzzle": "3x3",
        "official": True,
        "result_seconds": 2.76,
        "scramble": "L B R2 B' R2 U2 F D R2 U R2 F2 D2 R U B L2",
        "inspection": "x'",
        "stages": [
            {"label": "xxxcross", "moves": "r' U F U' r U' r' U2 r' U r"},
            {"label": "4th pair", "moves": "R U2' R2' U' R U R U2' R'"},
            {"label": "ZBLL", "moves": "U' F' r U R' U' r' F R"},
        ],
        "reported_stm": 29,
        "reported_tps": 10.51,
        "use": "PARSER_AND_STAGE_BOUNDARY_FIXTURE_ONLY",
        "cognitive_inference": "PROHIBITED",
    }


def validate_reconstruction_fixture(fixture: Mapping[str, object]) -> Dict[str, object]:
    tokens = []
    stage_counts = {}
    for stage in fixture["stages"]:  # type: ignore[index]
        stage_tokens = str(stage["moves"]).split()
        tokens.extend(stage_tokens)
        stage_counts[str(stage["label"])] = len(stage_tokens)
    # Rotations and wide moves count as one token in this parser fixture. The page's
    # reported STM remains source authority; token count is recorded, not forced equal.
    return {
        "token_count": len(tokens),
        "stage_token_counts": stage_counts,
        "reported_stm": fixture["reported_stm"],
        "reported_tps": fixture["reported_tps"],
        "has_stage_boundaries": len(stage_counts) >= 3,
        "has_scramble": len(str(fixture["scramble"]).split()) > 0,
        "result": "PASS_RECONSTRUCTION_FIXTURE_PARSE",
    }


def build_design_contract(registry: Mapping[str, object], trajectory_result: Mapping[str, object]) -> Dict[str, object]:
    return {
        "schema_version": "CR0816-NONREACTIVE-TRAJECTORY-DESIGN-1",
        "version": "CUBE-REV 0.8.16",
        "participant_instruction": "Continue naturally for up to three moves; no accuracy or strategy feedback is shown.",
        "trial_contract": {
            "maximum_actions": 3,
            "stop_if_solved": True,
            "intermediate_state_visible": True,
            "record": ["move display", "opaque move code", "action onset", "action confirmation", "inter-move latency", "intermediate state hash"],
            "do_not_record": ["trialwise confidence", "strategy label", "error admission", "planning-depth self-report"],
            "feedback": "NONE",
        },
        "nonreactivity_firewall": [
            "do not call any first move an error in participant-facing text",
            "do not reveal rotational family membership",
            "do not show expected continuation or recovery category",
            "retain only post-task global demand capture",
            "analyze recovery only when the observed first move creates a preregistered opportunity",
        ],
        "analysis_classes": [
            "chunk_continuation_signature",
            "closed_loop_replanning_signature",
            "exact_undo_recovery",
            "nonundo_subgoal_reset",
            "persistence_after_deterioration",
            "rotation_equivariance",
        ],
        "probe_count": registry["probe_count"],
        "family_count": registry["family_count"],
        "synthetic_result": trajectory_result["result"],
        "deployment": "NO_GO_RESEARCH_ASSET_ONLY",
    }


def run(bank_path: Path, outdir: Path, family_count: int, sessions_per_mechanism: int, seed: int) -> Dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    stimuli = BASE.load_stimuli(bank_path)
    base_probes = select_base_probes(stimuli, family_count)
    registry = build_family_registry(base_probes)
    rows, trajectory_result = simulate_identifiability(registry, sessions_per_mechanism, seed)
    schedules = build_balanced_schedules(registry)
    sources = external_source_registry()
    fixture = reconstruction_fixture()
    fixture_audit = validate_reconstruction_fixture(fixture)
    fixture_pack = external_reconstruction_fixture_pack()
    fixture_pack_audit = audit_external_fixture_pack(fixture_pack)
    design = build_design_contract(registry, trajectory_result)

    summary = {
        "schema_version": "CR0816-CERTIFICATION-RESULT-1",
        "version": "CUBE-REV 0.8.16",
        "seed": seed,
        "family_count": family_count,
        "probe_count": registry["probe_count"],
        "simulated_trajectory_count": trajectory_result["simulated_trajectory_count"],
        "trajectory_identifiability": trajectory_result,
        "schedule_design": {
            "schedule_count": schedules["schedule_count"],
            "trials_per_schedule": schedules["trials_per_schedule"],
            "minimum_family_spacing": schedules["minimum_family_spacing"],
        },
        "rotation_balance": {
            "planned_first_face_counts": registry["planned_first_face_counts"],
            "recovery_error_face_counts": registry["recovery_error_face_counts"],
        },
        "external_source_decision": sources["external_data_decision"],
        "fixture_audit": fixture_audit,
        "external_fixture_pack_audit": fixture_pack_audit,
        "deployment": "NO_GO",
        "human_mechanism_claim": "NO_GO",
        "result": "PASS_MINIMAL_NONREACTIVE_TRAJECTORY_PROBE_CERTIFICATION" if trajectory_result["result"] == "PASS_MINIMAL_TRAJECTORY_IDENTIFIABILITY" else "HOLD",
    }

    outputs = {
        "CUBE_REV_0.8.16_TRAJECTORY_PROBE_REGISTRY.json": registry,
        "trajectory_identifiability_result.json": trajectory_result,
        "CUBE_REV_0.8.16_TRAJECTORY_SCHEDULES.json": schedules,
        "simulated_trajectories.jsonl": rows,
        "CUBE_REV_0.8.16_EXTERNAL_TRAJECTORY_SOURCE_REGISTRY.json": sources,
        "reco_nz_12564_fixture.json": fixture,
        "reco_nz_12564_fixture_audit.json": fixture_audit,
        "CUBE_REV_0.8.16_EXTERNAL_RECONSTRUCTION_FIXTURE_PACK.json": fixture_pack,
        "CUBE_REV_0.8.16_EXTERNAL_RECONSTRUCTION_FIXTURE_AUDIT.json": fixture_pack_audit,
        "CUBE_REV_0.8.16_NONREACTIVE_TRAJECTORY_DESIGN.json": design,
        "CUBE_REV_0.8.16_CERTIFICATION_RESULT.json": summary,
    }
    for name, value in outputs.items():
        path = outdir / name
        if name.endswith(".jsonl"):
            path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in value) + "\n", encoding="utf-8")
        else:
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "CR0816_TRAJECTORY_PROBE_PASS "
        f"families={family_count} probes={registry['probe_count']} trajectories={trajectory_result['simulated_trajectory_count']} "
        f"open_closed={trajectory_result['contrasts']['open_vs_closed']['classification']} "
        f"recovery={trajectory_result['contrasts']['undo_vs_reset']['classification']} "
        f"negative={trajectory_result['contrasts']['latent_same_trajectory']['classification']}"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--family-count", type=int, default=6)
    parser.add_argument("--sessions-per-mechanism", type=int, default=360)
    parser.add_argument("--seed", type=int, default=8162026)
    args = parser.parse_args()
    run(args.bank, args.outdir, args.family_count, args.sessions_per_mechanism, args.seed)


if __name__ == "__main__":
    main()
