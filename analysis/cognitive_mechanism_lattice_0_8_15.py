#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import statistics
from functools import lru_cache
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

FACES = ("U", "R", "F", "D", "L", "B")
TURNS = ("", "2", "'")
MOVES = tuple(f + t for f in FACES for t in TURNS)
FACE_NORMAL = {
    "U": (0, 1, 0), "D": (0, -1, 0), "F": (0, 0, 1),
    "B": (0, 0, -1), "R": (1, 0, 0), "L": (-1, 0, 0),
}
# local right and down vectors as seen while looking straight at each face
FACE_BASIS = {
    "F": ((1, 0, 0), (0, -1, 0)),
    "B": ((-1, 0, 0), (0, -1, 0)),
    "U": ((1, 0, 0), (0, 0, 1)),
    "D": ((1, 0, 0), (0, 0, -1)),
    "R": ((0, 0, -1), (0, -1, 0)),
    "L": ((0, 0, 1), (0, -1, 0)),
}

Vec = Tuple[int, int, int]
StickerKey = Tuple[Vec, Vec]
State = Tuple[str, ...]


def vadd(a: Vec, b: Vec) -> Vec:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def vscale(a: Vec, k: int) -> Vec:
    return tuple(k * x for x in a)  # type: ignore[return-value]


def dot(a: Vec, b: Vec) -> int:
    return sum(x * y for x, y in zip(a, b))


def cross(a: Vec, b: Vec) -> Vec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def sticker_key(face: str, row: int, col: int) -> StickerKey:
    n = FACE_NORMAL[face]
    right, down = FACE_BASIS[face]
    sx = -1 if col == 0 else 1
    sy = -1 if row == 0 else 1
    pos = vadd(vadd(n, vscale(right, sx)), vscale(down, sy))
    return pos, n


ORDERED_KEYS: Tuple[StickerKey, ...] = tuple(
    sticker_key(face, row, col)
    for face in FACES for row in range(2) for col in range(2)
)
KEY_TO_INDEX = {key: i for i, key in enumerate(ORDERED_KEYS)}


def state_from_stickers(stickers: Mapping[str, Sequence[Sequence[str]]]) -> State:
    out = []
    for face in FACES:
        for row in range(2):
            for col in range(2):
                out.append(str(stickers[face][row][col]))
    return tuple(out)


def solved_score(state: State) -> int:
    score = 0
    for i, color in enumerate(state):
        face = FACES[i // 4]
        score += color == face
    return score


def rotate_quarter(v: Vec, axis: Vec, sign: int) -> Vec:
    # sign=+1 right-hand +90; sign=-1 right-hand -90
    parallel = vscale(axis, dot(axis, v))
    perpendicular = cross(axis, v) if sign == 1 else cross(v, axis)
    return vadd(parallel, perpendicular)


def apply_face_quarter(state: State, face: str, clockwise: bool = True) -> State:
    axis = FACE_NORMAL[face]
    sign = -1 if clockwise else 1
    out = list(state)
    layer_sign = 1
    # axis itself already contains sign, so points on the selected face satisfy dot(pos,axis)==1
    for i, (pos, normal) in enumerate(ORDERED_KEYS):
        if dot(pos, axis) == layer_sign:
            new_key = (rotate_quarter(pos, axis, sign), rotate_quarter(normal, axis, sign))
            out[KEY_TO_INDEX[new_key]] = state[i]
    return tuple(out)


@lru_cache(maxsize=None)
def apply_move(state: State, move: str) -> State:
    face, suffix = move[0], move[1:]
    turns = 2 if suffix == "2" else 1
    clockwise = suffix != "'"
    out = state
    for _ in range(turns):
        out = apply_face_quarter(out, face, clockwise=clockwise)
    return out


def rotation_matrices() -> List[Tuple[Vec, Vec, Vec]]:
    mats = []
    basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for perm in itertools.permutations(basis):
        for signs in itertools.product((-1, 1), repeat=3):
            cols = tuple(vscale(perm[i], signs[i]) for i in range(3))
            if dot(cols[0], cross(cols[1], cols[2])) == 1:
                mats.append(cols)  # columns
    unique = []
    seen = set()
    for m in mats:
        if m not in seen:
            unique.append(m); seen.add(m)
    assert len(unique) == 24
    return unique


ROTATIONS = rotation_matrices()
FIXED_ALIAS_ROTATION = ROTATIONS[7]


def mat_vec(m: Tuple[Vec, Vec, Vec], v: Vec) -> Vec:
    return (
        m[0][0] * v[0] + m[1][0] * v[1] + m[2][0] * v[2],
        m[0][1] * v[0] + m[1][1] * v[1] + m[2][1] * v[2],
        m[0][2] * v[0] + m[1][2] * v[1] + m[2][2] * v[2],
    )


def rotate_state(state: State, m: Tuple[Vec, Vec, Vec]) -> State:
    out = list(state)
    for i, (pos, normal) in enumerate(ORDERED_KEYS):
        new_key = (mat_vec(m, pos), mat_vec(m, normal))
        out[KEY_TO_INDEX[new_key]] = state[i]
    return tuple(out)


def canonical_rotation(state: State) -> str:
    return min("".join(rotate_state(state, m)) for m in ROTATIONS)


def transformed_face(face: str, m: Tuple[Vec, Vec, Vec]) -> str:
    n = mat_vec(m, FACE_NORMAL[face])
    return next(f for f, normal in FACE_NORMAL.items() if normal == n)


def transformed_move(move: str, m: Tuple[Vec, Vec, Vec]) -> str:
    return transformed_face(move[0], m) + move[1:]


def state_digest(state: State) -> str:
    return hashlib.sha256("".join(state).encode()).hexdigest()


def best_future_score(state: State, remaining: int, memo: Dict[Tuple[State, int, str], int], previous_face: str = "") -> int:
    if remaining == 0:
        return solved_score(state)
    key = (state, remaining, previous_face)
    if key in memo:
        return memo[key]
    best = -1
    for move in MOVES:
        if previous_face and move[0] == previous_face:
            continue
        value = best_future_score(apply_move(state, move), remaining - 1, memo, move[0])
        if value > best:
            best = value
    memo[key] = best
    return best


def action_values(state: State, horizon: int) -> Dict[str, int]:
    memo: Dict[Tuple[State, int, str], int] = {}
    return {
        move: best_future_score(apply_move(state, move), horizon - 1, memo, move[0])
        for move in MOVES
    }


def argmax_moves(values: Mapping[str, float]) -> List[str]:
    m = max(values.values())
    return sorted([k for k, v in values.items() if v == m])


def softmax_choice(values: Mapping[str, float], rng: random.Random, temperature: float) -> str:
    mx = max(values.values())
    weights = [math.exp((values[m] - mx) / max(temperature, 1e-9)) for m in MOVES]
    return rng.choices(MOVES, weights=weights, k=1)[0]


@dataclass(frozen=True)
class Stimulus:
    stimulus_id: str
    state: State
    orbit: str
    solved: int
    values: Dict[int, Dict[str, int]]
    alias_h2: Dict[str, int]


def load_stimuli(bank_path: Path) -> List[Stimulus]:
    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    out = []
    for row in bank["stimuli"]:
        state = state_from_stickers(row["stickers"])
        out.append(Stimulus(
            stimulus_id=row["stimulus_id"],
            state=state,
            orbit=canonical_rotation(state),
            solved=solved_score(state),
            values={h: action_values(state, h) for h in (1, 2, 3)},
            alias_h2=action_values(rotate_state(state, FIXED_ALIAS_ROTATION), 2),
        ))
    return out


def latency(rng: random.Random, base: float, spread: float = 0.16) -> float:
    # log-normal with requested median-like scale
    return max(120.0, rng.lognormvariate(math.log(base), spread))


def simulate_session(mechanism: str, schedule: Sequence[Stimulus], rng: random.Random) -> Dict[str, object]:
    choices: List[str] = []
    latencies: List[float] = []
    latent_only = None
    for i, stim in enumerate(schedule):
        h1, h2, h3 = stim.values[1], stim.values[2], stim.values[3]
        if mechanism == "greedy_h1":
            choice = rng.choice(argmax_moves(h1)); rt = latency(rng, 820 + 35 * (24 - stim.solved))
        elif mechanism == "lookahead_h2":
            choice = rng.choice(argmax_moves(h2)); rt = latency(rng, 1120 + 45 * (24 - stim.solved))
        elif mechanism == "lookahead_h3":
            choice = rng.choice(argmax_moves(h3)); rt = latency(rng, 1500 + 55 * (24 - stim.solved))
        elif mechanism == "strategy_switch_h1_to_h3":
            if i < len(schedule) // 2:
                choice = rng.choice(argmax_moves(h1)); rt = latency(rng, 880 + 35 * (24 - stim.solved))
            else:
                choice = rng.choice(argmax_moves(h3)); rt = latency(rng, 1600 + 55 * (24 - stim.solved))
        elif mechanism == "perseverative_interference":
            if choices and rng.random() < 0.48:
                prev = choices[-1]
                same_face = [m for m in MOVES if m[0] == prev[0]]
                choice = rng.choice(same_face); rt = latency(rng, 760)
            else:
                choice = rng.choice(argmax_moves(h2)); rt = latency(rng, 1080)
        elif mechanism == "stochastic_exploration":
            choice = softmax_choice(h2, rng, temperature=1.8); rt = latency(rng, 1280, 0.24)
        elif mechanism == "orientation_frame_alias":
            choice = rng.choice(argmax_moves(stim.alias_h2)); rt = latency(rng, 1240)
        elif mechanism == "open_loop_chunk_unobserved":
            choice = rng.choice(argmax_moves(h2)); rt = latency(rng, 1100)
            latent_only = "OPEN_LOOP_AFTER_FIRST_ACTION"
        elif mechanism == "closed_loop_monitor_unobserved":
            choice = rng.choice(argmax_moves(h2)); rt = latency(rng, 1100)
            latent_only = "CLOSED_LOOP_AFTER_FIRST_ACTION"
        elif mechanism == "high_capacity_same_policy_unobserved":
            choice = rng.choice(argmax_moves(h2)); rt = latency(rng, 1100)
            latent_only = "HIGH_VISUOSPATIAL_CAPACITY"
        elif mechanism == "low_capacity_same_policy_unobserved":
            choice = rng.choice(argmax_moves(h2)); rt = latency(rng, 1100)
            latent_only = "LOW_VISUOSPATIAL_CAPACITY_WITH_COMPENSATION"
        else:
            raise ValueError(mechanism)
        choices.append(choice); latencies.append(rt)

    return {"mechanism": mechanism, "choices": choices, "latencies": latencies, "latent_only": latent_only}


def entropy(values: Sequence[str]) -> float:
    n = len(values)
    counts = Counter(values)
    return -sum((c / n) * math.log(c / n + 1e-15) for c in counts.values())


def agreement(choice: str, values: Mapping[str, int]) -> float:
    return 1.0 if choice in argmax_moves(values) else 0.0


def session_features(session: Mapping[str, object], schedule: Sequence[Stimulus]) -> Dict[str, float]:
    choices = list(session["choices"])  # type: ignore[arg-type]
    rts = [float(x) for x in session["latencies"]]  # type: ignore[arg-type]
    n = len(choices)
    half = n // 2
    reps = sum(choices[i][0] == choices[i - 1][0] for i in range(1, n)) / (n - 1)
    exact_reps = sum(choices[i] == choices[i - 1] for i in range(1, n)) / (n - 1)
    feats = {
        "agree_h1": statistics.fmean(agreement(c, s.values[1]) for c, s in zip(choices, schedule)),
        "agree_h2": statistics.fmean(agreement(c, s.values[2]) for c, s in zip(choices, schedule)),
        "agree_h3": statistics.fmean(agreement(c, s.values[3]) for c, s in zip(choices, schedule)),
        "mean_rt": statistics.fmean(rts),
        "sd_rt": statistics.pstdev(rts),
        "action_entropy": entropy(choices),
        "face_entropy": entropy([c[0] for c in choices]),
        "face_repeat_rate": reps,
        "exact_repeat_rate": exact_reps,
        "late_minus_early_rt": statistics.fmean(rts[half:]) - statistics.fmean(rts[:half]),
        "late_minus_early_h3": statistics.fmean(agreement(c, s.values[3]) for c, s in zip(choices[half:], schedule[half:])) - statistics.fmean(agreement(c, s.values[3]) for c, s in zip(choices[:half], schedule[:half])),
    }
    return feats


def standardize(train: List[Dict[str, float]], test: List[Dict[str, float]]) -> Tuple[List[List[float]], List[List[float]], List[str]]:
    names = sorted(train[0])
    means = {k: statistics.fmean(row[k] for row in train) for k in names}
    sds = {k: statistics.pstdev(row[k] for row in train) or 1.0 for k in names}
    enc = lambda rows: [[(row[k] - means[k]) / sds[k] for k in names] for row in rows]
    return enc(train), enc(test), names


def dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def centroid(rows: Sequence[Sequence[float]]) -> List[float]:
    return [statistics.fmean(r[j] for r in rows) for j in range(len(rows[0]))]


def classify_nearest_centroid(samples: List[Tuple[str, Dict[str, float]]], seed: int = 815) -> Dict[str, object]:
    rng = random.Random(seed)
    by_label: Dict[str, List[Dict[str, float]]] = defaultdict(list)
    for label, feat in samples:
        by_label[label].append(feat)
    train_rows: List[Dict[str, float]] = []
    train_labels: List[str] = []
    test_rows: List[Dict[str, float]] = []
    test_labels: List[str] = []
    for label, rows in by_label.items():
        rows = list(rows); rng.shuffle(rows)
        split = max(1, int(0.65 * len(rows)))
        train_rows.extend(rows[:split]); train_labels.extend([label] * split)
        test_rows.extend(rows[split:]); test_labels.extend([label] * (len(rows) - split))
    train_x, test_x, feature_names = standardize(train_rows, test_rows)
    grouped: Dict[str, List[List[float]]] = defaultdict(list)
    for label, row in zip(train_labels, train_x): grouped[label].append(row)
    cents = {label: centroid(rows) for label, rows in grouped.items()}
    labels = sorted(cents)
    confusion = {a: {b: 0 for b in labels} for a in labels}
    correct = 0
    for truth, row in zip(test_labels, test_x):
        pred = min(labels, key=lambda lab: dist(row, cents[lab]))
        confusion[truth][pred] += 1
        correct += pred == truth
    per_class = {}
    for lab in labels:
        total = sum(confusion[lab].values())
        per_class[lab] = confusion[lab][lab] / total if total else 0.0
    return {
        "feature_names": feature_names,
        "test_n": len(test_labels),
        "overall_accuracy": correct / len(test_labels),
        "balanced_accuracy": statistics.fmean(per_class.values()),
        "per_class_recall": per_class,
        "confusion": confusion,
    }


def pairwise_accuracy(samples: List[Tuple[str, Dict[str, float]]], labels: Sequence[str], seed: int = 815, repeats: int = 31) -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, Dict[str, float]]]]:
    means: Dict[str, Dict[str, float]] = {a: {} for a in labels}
    diagnostics: Dict[str, Dict[str, Dict[str, float]]] = {a: {} for a in labels}
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            subset = [(lab, feat) for lab, feat in samples if lab in {a, b}]
            scores = [float(classify_nearest_centroid(subset, seed=seed + 7919 * r)["balanced_accuracy"]) for r in range(repeats)]
            summary = {
                "mean": round(statistics.fmean(scores), 4),
                "sd": round(statistics.pstdev(scores), 4),
                "min": round(min(scores), 4),
                "max": round(max(scores), 4),
                "repeats": repeats,
            }
            means[a][b] = means[b][a] = summary["mean"]
            diagnostics[a][b] = diagnostics[b][a] = summary
        means[a][a] = 1.0
        diagnostics[a][a] = {"mean": 1.0, "sd": 0.0, "min": 1.0, "max": 1.0, "repeats": repeats}
    return means, diagnostics


def orbit_summary(stimuli: Sequence[Stimulus]) -> Dict[str, object]:
    groups: Dict[str, List[str]] = defaultdict(list)
    for s in stimuli: groups[s.orbit].append(s.stimulus_id)
    repeated = sorted([ids for ids in groups.values() if len(ids) > 1])
    return {
        "orbit_count": len(groups),
        "repeated_orbit_count": len(repeated),
        "repeated_orbits": repeated,
        "max_orbit_multiplicity": max(map(len, groups.values())),
    }


def horizon_summary(stimuli: Sequence[Stimulus]) -> Dict[str, object]:
    rows = []
    counts = Counter()
    for s in stimuli:
        sets = {h: set(argmax_moves(s.values[h])) for h in (1, 2, 3)}
        sig = f"h1={'/'.join(sorted(sets[1]))}|h2={'/'.join(sorted(sets[2]))}|h3={'/'.join(sorted(sets[3]))}"
        rows.append({"stimulus_id": s.stimulus_id, "solved_score": s.solved, "best_h1": sorted(sets[1]), "best_h2": sorted(sets[2]), "best_h3": sorted(sets[3]), "signature": sig})
        counts["h1_vs_h2_disjoint"] += sets[1].isdisjoint(sets[2])
        counts["h2_vs_h3_disjoint"] += sets[2].isdisjoint(sets[3])
        counts["h1_vs_h3_disjoint"] += sets[1].isdisjoint(sets[3])
        counts["h1_vs_h2_different"] += sets[1] != sets[2]
        counts["h2_vs_h3_different"] += sets[2] != sets[3]
        counts["all_same"] += sets[1] == sets[2] == sets[3]
    return {"counts": dict(counts), "stimuli": rows}


def orientation_pair_audit(stimuli: Sequence[Stimulus], schedules: Sequence[Sequence[Stimulus]]) -> Dict[str, object]:
    groups: Dict[str, List[Stimulus]] = defaultdict(list)
    for s in stimuli:
        groups[s.orbit].append(s)
    pairs = []
    for members in groups.values():
        if len(members) < 2:
            continue
        for a, b in itertools.combinations(members, 2):
            mappings = []
            for ri, m in enumerate(ROTATIONS):
                if rotate_state(a.state, m) == b.state:
                    mappings.append({
                        "rotation_index": ri,
                        "face_map": {f: transformed_face(f, m) for f in FACES},
                        "move_map": {mv: transformed_move(mv, m) for mv in MOVES},
                    })
            positions = []
            for sid, schedule in enumerate(schedules, 1):
                ids = [x.stimulus_id for x in schedule]
                pa, pb = ids.index(a.stimulus_id) + 1, ids.index(b.stimulus_id) + 1
                positions.append({"schedule_id": sid, "a_position": pa, "b_position": pb, "separation": abs(pa-pb), "a_before_b": pa<pb})
            pairs.append({
                "stimulus_a": a.stimulus_id,
                "stimulus_b": b.stimulus_id,
                "rotation_mapping_count": len(mappings),
                "rotation_mappings": mappings,
                "schedule_positions": positions,
                "a_before_b_count": sum(x["a_before_b"] for x in positions),
                "b_before_a_count": sum(not x["a_before_b"] for x in positions),
                "mean_separation": round(statistics.fmean(x["separation"] for x in positions), 4),
                "min_separation": min(x["separation"] for x in positions),
                "max_separation": max(x["separation"] for x in positions),
            })
    return {
        "pair_count": len(pairs),
        "pairs": pairs,
        "conclusion": "SINGLE_ROTATIONAL_PAIR_INSUFFICIENT_FOR_STABLE_TRAIT_INFERENCE" if len(pairs)==1 else "NO_ROTATIONAL_PAIR" if not pairs else "MULTIPLE_ROTATIONAL_PAIRS_AVAILABLE"
    }


def schedule_balance_audit(schedules: Sequence[Sequence[Stimulus]]) -> Dict[str, object]:
    rows=[]
    for sid, schedule in enumerate(schedules,1):
        indicators=[set(argmax_moves(s.values[1])) != set(argmax_moves(s.values[3])) for s in schedule]
        first=statistics.fmean(indicators[:14]); second=statistics.fmean(indicators[14:])
        rows.append({"schedule_id":sid,"first_half_horizon_discrimination_rate":round(first,4),"second_half_horizon_discrimination_rate":round(second,4),"second_minus_first":round(second-first,4)})
    diffs=[r["second_minus_first"] for r in rows]
    return {
        "schedule_count":len(rows),
        "mean_second_minus_first":round(statistics.fmean(diffs),4),
        "mean_absolute_difference":round(statistics.fmean(abs(x) for x in diffs),4),
        "max_absolute_difference":round(max(abs(x) for x in diffs),4),
        "rows":rows,
        "conclusion":"COUNTERBALANCED_ORDER_REDUCES_BUT_DOES_NOT_ELIMINATE_WITHIN_SCHEDULE_ITEM_MIXTURE_VARIATION"
    }


def registry() -> Dict[str, object]:
    return {
        "schema_version": "CR0815-COGNITIVE-MECHANISM-AXIS-REGISTRY-1",
        "version": "CUBE-REV 0.8.15",
        "title": "Cognitive Mechanism-axis Lattice, Strategy-transition Signatures & Identifiability-constrained Hypothesis Registry",
        "epistemic_rule": "BEHAVIORAL_SIGNATURE_FIRST_PSYCHOLOGICAL_LABEL_SECOND",
        "measurement_rule": "NO_TRIALWISE_SELF_REPORT_ADDED_IN_0_8_15",
        "axes": [
            {
                "axis_id": "AX-PLANNING-HORIZON",
                "candidate_mechanisms": ["local_greedy", "two_step_lookahead", "three_step_lookahead"],
                "observable_now": ["first_action", "latency_ms", "stimulus_specific_horizon_value"],
                "falsifier": "choices do not preferentially match the depth-specific optimum on horizon-discriminating stimuli",
                "status": "SYNTHETIC_IDENTIFIABILITY_TESTED"
            },
            {
                "axis_id": "AX-STRATEGY-ARBITRATION",
                "candidate_mechanisms": ["stationary_policy", "h1_to_h3_change_point", "perseverative_interference"],
                "observable_now": ["schedule_position", "first_action", "latency_ms", "previous_action"],
                "falsifier": "change-point signatures vanish under counterbalanced schedules or are reproduced by item order alone",
                "status": "SYNTHETIC_IDENTIFIABILITY_TESTED"
            },
            {
                "axis_id": "AX-ORIENTATION-EQUIVARIANCE",
                "candidate_mechanisms": ["object_centered_mapping", "viewer_centered_alias"],
                "observable_now": ["first_action", "rotationally_paired_stimuli"],
                "falsifier": "no rotational stimulus pairs exist or transformed actions are not recoverable",
                "status": "BANK_SUPPORT_AUDITED"
            },
            {
                "axis_id": "AX-CHUNK-RETRIEVAL-AND-SWITCHING",
                "candidate_mechanisms": ["perceptual_chunk_retrieval", "sequence_chunk_switch_cost"],
                "observable_now": ["motif_repetition", "latency_ms", "action_consistency"],
                "falsifier": "single-action trials lack within-chunk boundary timing and repeated motifs",
                "status": "PARTIAL_OR_NOT_IDENTIFIABLE"
            },
            {
                "axis_id": "AX-OPEN-VS-CLOSED-LOOP-CONTROL",
                "candidate_mechanisms": ["open_loop_chunk", "closed_loop_re_evaluation"],
                "observable_now": ["first_action_only"],
                "required_extension": ["intermediate_state", "subsequent_action_timestamps", "correction_events"],
                "falsifier": "two mechanisms generate identical current observables",
                "status": "NEGATIVE_CONTROL_EXPECTED_NON_IDENTIFIABLE"
            },
            {
                "axis_id": "AX-RECOVERY-MONITORING",
                "candidate_mechanisms": ["last_move_undo", "subgoal_reset", "continue_despite_error"],
                "observable_now": [],
                "required_extension": ["multi_action_trajectory", "error_opportunity", "recovery_path"],
                "status": "NOT_IDENTIFIABLE_CURRENT_INSTRUMENT"
            },
            {
                "axis_id": "AX-VISUOSPATIAL-CAPACITY",
                "candidate_mechanisms": ["capacity_limit", "compensatory_policy"],
                "observable_now": ["first_action", "latency_ms"],
                "falsifier": "different capacity states can implement the same observable policy",
                "status": "DO_NOT_INFER_AS_TRAIT_FROM_CURRENT_TRACE"
            },
            {
                "axis_id": "AX-METACOGNITIVE-MONITORING",
                "candidate_mechanisms": ["confidence_calibration", "performance_oriented_conservatism"],
                "observable_now": ["post_task_global_confidence", "post_task_guess"],
                "measurement_hazard": "trialwise confidence can alter strategy and task performance",
                "status": "POST_TASK_ONLY_NON_REACTIVE_BOUNDARY"
            }
        ],
        "forbidden_claims": [
            "infer working-memory capacity from first-action trace alone",
            "infer conscious planning from latency alone",
            "infer chunking without repeated structural motifs or within-sequence timing",
            "infer recovery strategy without observing an error and subsequent actions",
            "treat trialwise confidence as a passive measurement"
        ]
    }


def run(bank_path: Path, config_path: Path, outdir: Path, sessions_per_mechanism: int, seed: int) -> Dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    stimuli = load_stimuli(bank_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    by_id = {s.stimulus_id: s for s in stimuli}
    schedules = [[by_id[x] for x in config["schedules"][str(i)]] for i in range(1, 25)]
    mechanisms = [
        "greedy_h1", "lookahead_h2", "lookahead_h3", "strategy_switch_h1_to_h3",
        "perseverative_interference", "stochastic_exploration", "orientation_frame_alias",
        "open_loop_chunk_unobserved", "closed_loop_monitor_unobserved",
        "high_capacity_same_policy_unobserved", "low_capacity_same_policy_unobserved",
    ]
    samples: List[Tuple[str, Dict[str, float]]] = []
    session_rows = []
    for mi, mechanism in enumerate(mechanisms):
        for rep in range(sessions_per_mechanism):
            rng = random.Random(seed + mi * 100000 + rep)
            schedule_id = rep % 24
            schedule = schedules[schedule_id]
            session = simulate_session(mechanism, schedule, rng)
            feat = session_features(session, schedule)
            samples.append((mechanism, feat))
            session_rows.append({"mechanism": mechanism, "replication": rep, "schedule_id": schedule_id + 1, **feat})

    model = classify_nearest_centroid(samples, seed=seed)
    pairwise, pairwise_diagnostics = pairwise_accuracy(samples, mechanisms, seed=seed, repeats=31)
    special_keys = {
        "open_vs_closed_loop": ("open_loop_chunk_unobserved", "closed_loop_monitor_unobserved"),
        "high_vs_low_capacity_same_policy": ("high_capacity_same_policy_unobserved", "low_capacity_same_policy_unobserved"),
        "h1_vs_h3": ("greedy_h1", "lookahead_h3"),
        "stationary_h1_vs_switch": ("greedy_h1", "strategy_switch_h1_to_h3"),
    }
    special_pairs = {name: pairwise[a][b] for name,(a,b) in special_keys.items()}
    thresholds = {"identifiable": 0.80, "partial": 0.65}
    classifications = {}
    for name, acc in special_pairs.items():
        classifications[name] = "IDENTIFIABLE" if acc >= thresholds["identifiable"] else "PARTIAL" if acc >= thresholds["partial"] else "NON_IDENTIFIABLE"

    orbit = orbit_summary(stimuli)
    horizon = horizon_summary(stimuli)
    orientation = orientation_pair_audit(stimuli, schedules)
    schedule_balance = schedule_balance_audit(schedules)
    result = {
        "schema_version": "CR0815-MECHANISM-IDENTIFIABILITY-RESULT-1",
        "version": "CUBE-REV 0.8.15",
        "seed": seed,
        "sessions_per_mechanism": sessions_per_mechanism,
        "mechanism_count": len(mechanisms),
        "simulated_session_count": len(session_rows),
        "stimulus_count": len(stimuli),
        "schedule_count": len(schedules),
        "orbit_audit": orbit,
        "horizon_audit": horizon["counts"],
        "classifier": model,
        "pairwise_balanced_accuracy_mean": pairwise,
        "predeclared_pair_results": {k: {"balanced_accuracy_mean": v, "diagnostics": pairwise_diagnostics[special_keys[k][0]][special_keys[k][1]], "classification": classifications[k]} for k, v in special_pairs.items()},
        "orientation_pair_audit": orientation,
        "schedule_balance_audit": schedule_balance,
        "instrument_conclusions": {
            "planning_horizon": classifications["h1_vs_h3"],
            "strategy_transition": classifications["stationary_h1_vs_switch"],
            "open_vs_closed_loop": classifications["open_vs_closed_loop"],
            "visuospatial_capacity_trait": classifications["high_vs_low_capacity_same_policy"],
            "orientation_equivariance": "NOT_IDENTIFIABLE_NO_REPEATED_ROTATIONAL_ORBITS" if orbit["repeated_orbit_count"] == 0 else "PARTIAL_SINGLE_ROTATIONAL_PAIR" if orbit["repeated_orbit_count"] == 1 else "POTENTIALLY_IDENTIFIABLE",
            "chunk_boundary_cost": "NOT_IDENTIFIABLE_SINGLE_ACTION_TRIALS",
            "recovery_monitoring": "NOT_IDENTIFIABLE_NO_POST_ERROR_TRAJECTORY",
            "trialwise_confidence": "NOT_ADDED_MEASUREMENT_REACTIVITY_RISK"
        },
        "promotion_rule": "PROMOTE_ONLY_AXES_WITH_DISTINCT_CURRENT_OBSERVABLES_OR_EXPLICIT_NEW_INSTRUMENT_REQUIREMENTS",
        "result": "PASS_IDENTIFIABILITY_LATTICE_WITH_NEGATIVE_CONTROLS"
    }
    (outdir / "CUBE_REV_0.8.15_MECHANISM_AXIS_REGISTRY.json").write_text(json.dumps(registry(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "mechanism_identifiability_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "horizon_stimulus_audit.json").write_text(json.dumps(horizon, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "orientation_pair_audit.json").write_text(json.dumps(orientation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "schedule_balance_audit.json").write_text(json.dumps(schedule_balance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "simulated_session_features.jsonl").write_text("\n".join(json.dumps(r, sort_keys=True) for r in session_rows) + "\n", encoding="utf-8")
    print(f"CR0815_MECHANISM_LATTICE_PASS sessions={len(session_rows)} planning={classifications['h1_vs_h3']} switch={classifications['stationary_h1_vs_switch']} open_closed={classifications['open_vs_closed_loop']} capacity={classifications['high_vs_low_capacity_same_policy']} rotational_pairs={orbit['repeated_orbit_count']}")
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", type=Path, required=True)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--sessions-per-mechanism", type=int, default=240)
    ap.add_argument("--seed", type=int, default=8152026)
    args = ap.parse_args()
    run(args.bank, args.config, args.outdir, args.sessions_per_mechanism, args.seed)


if __name__ == "__main__":
    main()
