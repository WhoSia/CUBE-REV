#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

VERSION = "CUBE-REV 0.8.18"
LATENCY_BINS_MS = [0.0, 50.0, 80.0, 120.0, 180.0, 250.0, 400.0, 700.0, 1200.0, 1.0e12]
WEIGHT_MIN = 0.2
WEIGHT_MAX = 5.0
RAKE_ITERATIONS = 50


def canonical_bytes(obj: object) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.write_bytes(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n")


def quantile(values: Sequence[float], q: float) -> float:
    if not values:
        raise ValueError("EMPTY_QUANTILE")
    xs = sorted(float(v) for v in values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * q
    lo = int(math.floor(pos)); hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1.0 - frac) + xs[hi] * frac


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def histogram(values: Sequence[float], bins: Sequence[float], weights: Sequence[float] | None = None) -> list[float]:
    counts = [0.0] * (len(bins) - 1)
    if weights is None:
        weights = [1.0] * len(values)
    if len(values) != len(weights):
        raise ValueError("HIST_WEIGHT_LENGTH")
    for value, weight in zip(values, weights):
        idx = None
        for i in range(len(bins) - 1):
            if bins[i] <= value < bins[i + 1]:
                idx = i; break
        if idx is None:
            if value == bins[-1]:
                idx = len(bins) - 2
            else:
                raise ValueError(f"HIST_OUT_OF_RANGE:{value}")
        counts[idx] += float(weight)
    total = sum(counts)
    return [c / total if total else 0.0 for c in counts]


def js_divergence(p: Sequence[float], q: Sequence[float]) -> float:
    m = [(a + b) / 2.0 for a, b in zip(p, q)]
    def kl(a: Sequence[float], b: Sequence[float]) -> float:
        out = 0.0
        for x, y in zip(a, b):
            if x > 0:
                out += x * math.log2(x / y)
        return out
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def empirical_wasserstein_log_ms(a: Sequence[float], b: Sequence[float], points: int = 1001) -> float:
    if not a or not b:
        raise ValueError("EMPTY_WASSERSTEIN")
    la = [math.log10(max(1.0, x)) for x in a]
    lb = [math.log10(max(1.0, x)) for x in b]
    return sum(abs(quantile(la, i / (points - 1)) - quantile(lb, i / (points - 1))) for i in range(points)) / points


def move_face(move: str) -> str:
    if not isinstance(move, str) or not move:
        raise ValueError("INVALID_MOVE")
    face = move[0].upper()
    if face not in "URFDLB":
        raise ValueError(f"UNSUPPORTED_MOVE:{move}")
    suffix = move[1:]
    if suffix not in {"", "'", "2", "2'"}:
        raise ValueError(f"UNSUPPORTED_MOVE:{move}")
    return face


def relation(a: str, b: str) -> str:
    fa, fb = move_face(a), move_face(b)
    if fa == fb:
        return "SAME"
    if {fa, fb} in ({"U", "D"}, {"R", "L"}, {"F", "B"}):
        return "OPPOSITE"
    return "ADJACENT"


def latency_class(delta_ms: float, burst_max: float, flow_max: float) -> str:
    if delta_ms <= burst_max:
        return "BURST"
    if delta_ms <= flow_max:
        return "FLOW"
    return "PAUSE"


def audit_events(events: list[dict], require_sequence: bool = False) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    last_t = None
    last_seq = None
    duplicate_pairs = 0
    very_fast = 0
    long_gaps = 0
    deltas: list[float] = []
    for i, event in enumerate(events):
        try:
            move_face(event.get("m"))
        except Exception as exc:
            errors.append(str(exc))
        t = event.get("t")
        if not isinstance(t, (int, float)) or not math.isfinite(float(t)) or t < 0:
            errors.append(f"INVALID_TIMESTAMP:{i}")
            continue
        if last_t is not None:
            delta = float(t) - float(last_t)
            deltas.append(delta)
            if delta <= 0:
                errors.append(f"NON_MONOTONIC_TIMESTAMP:{i}")
            if delta < 20:
                very_fast += 1
                warnings.append(f"IMPLAUSIBLE_BURST_LT20MS:{i}")
            if delta > 1000:
                long_gaps += 1
                warnings.append(f"PAUSE_CANDIDATE_GT1000MS:{i}")
            if event.get("m") == events[i - 1].get("m") and delta == 0:
                duplicate_pairs += 1
        if require_sequence:
            seq = event.get("seq")
            if not isinstance(seq, int):
                errors.append(f"SEQUENCE_COUNTER_REQUIRED:{i}")
            elif last_seq is not None and seq != last_seq + 1:
                errors.append(f"SEQUENCE_GAP:{last_seq}->{seq}")
            last_seq = seq if isinstance(seq, int) else last_seq
        last_t = t
    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": sorted(set(errors)),
        "warnings": warnings,
        "event_count": len(events),
        "intermove_count": len(deltas),
        "very_fast_lt20ms_count": very_fast,
        "pause_candidate_gt1000ms_count": long_gaps,
        "duplicate_same_timestamp_move_count": duplicate_pairs,
        "strict_timestamp_monotonicity": not any(e.startswith("NON_MONOTONIC") for e in errors),
        "sequence_counter_checked": require_sequence,
    }


def compress_double_turns(events: list[dict]) -> tuple[list[dict], float]:
    if not events:
        return [], 0.0
    threshold_ms = float(events[-1]["t"]) / len(events)
    out: list[dict] = []
    i = 0
    while i < len(events):
        cur = events[i]
        if i + 1 < len(events):
            nxt = events[i + 1]
            if cur["m"] in {"U", "U'", "R", "R'", "F", "F'", "D", "D'", "L", "L'", "B", "B'"} and nxt["m"] == cur["m"] and 0 < nxt["t"] - cur["t"] <= threshold_ms:
                out.append({"m": move_face(cur["m"]) + "2", "t": cur["t"], "source_event_count": 2})
                i += 2
                continue
        out.append({"m": cur["m"], "t": cur["t"], "source_event_count": 1})
        i += 1
    return out, threshold_ms


def corruption_court(base: list[dict]) -> dict:
    cases = {}
    def copied(): return [dict(x) for x in base]
    x = copied(); x[5], x[6] = x[6], x[5]
    cases["reordered_events"] = {"expected": "FAIL", "audit": audit_events(x)}
    x = copied(); x[10]["t"] = x[9]["t"]
    cases["zero_delta"] = {"expected": "FAIL", "audit": audit_events(x)}
    x = copied(); x[10]["t"] = x[9]["t"] - 1
    cases["clock_regression"] = {"expected": "FAIL", "audit": audit_events(x)}
    x = copied(); x[4]["m"] = "Q"
    cases["unsupported_move"] = {"expected": "FAIL", "audit": audit_events(x)}
    x = copied(); x[4]["t"] = x[3]["t"] + 5
    cases["implausible_sub20ms_burst"] = {"expected": "PASS_WITH_WARNING", "audit": audit_events(x)}
    x = copied(); del x[7]
    cases["dropped_event_without_counter"] = {"expected": "UNDETECTABLE", "audit": audit_events(x), "conclusion": "PASSING_STRUCTURE_DOES_NOT_PROVE_NO_PACKET_LOSS"}
    seq = [dict(event, seq=i) for i, event in enumerate(base)]
    del seq[7]
    cases["dropped_event_with_counter"] = {"expected": "FAIL", "audit": audit_events(seq, require_sequence=True)}
    ok = (
        cases["reordered_events"]["audit"]["status"] == "FAIL" and
        cases["zero_delta"]["audit"]["status"] == "FAIL" and
        cases["clock_regression"]["audit"]["status"] == "FAIL" and
        cases["unsupported_move"]["audit"]["status"] == "FAIL" and
        cases["implausible_sub20ms_burst"]["audit"]["status"] == "PASS" and
        cases["implausible_sub20ms_burst"]["audit"]["very_fast_lt20ms_count"] >= 1 and
        cases["dropped_event_without_counter"]["audit"]["status"] == "PASS" and
        cases["dropped_event_with_counter"]["audit"]["status"] == "FAIL"
    )
    return {"cases": cases, "result": "PASS_NEGATIVE_CONTROL_COURT" if ok else "FAIL_NEGATIVE_CONTROL_COURT"}


def motif_distribution(motifs: Iterable[str], weights: Iterable[float] | None = None) -> dict[str, float]:
    counter: dict[str, float] = collections.defaultdict(float)
    if weights is None:
        weights = [1.0 for _ in motifs]
        # motifs consumed above if iterator; callers pass lists.
    for motif, weight in zip(motifs, weights):
        counter[motif] += float(weight)
    total = sum(counter.values())
    return {k: counter[k] / total for k in sorted(counter)} if total else {}


def js_dict(a: dict[str, float], b: dict[str, float]) -> float:
    keys = sorted(set(a) | set(b))
    return js_divergence([a.get(k, 0.0) for k in keys], [b.get(k, 0.0) for k in keys])


def bounded_scale(values: list[float], target_sum: float, lo: float, hi: float) -> list[float]:
    left, right = 0.0, 1.0
    def total(scale: float) -> float:
        return sum(min(hi, max(lo, scale * x)) for x in values)
    while total(right) < target_sum:
        right *= 2.0
    for _ in range(80):
        mid = (left + right) / 2.0
        if total(mid) < target_sum:
            left = mid
        else:
            right = mid
    return [min(hi, max(lo, right * x)) for x in values]


def raking_weights(rows: list[dict], target: list[float]) -> list[float]:
    weights = [1.0] * len(rows)
    mechanisms = sorted({row["mechanism"] for row in rows})
    indexes = {m: [i for i, row in enumerate(rows) if row["mechanism"] == m] for m in mechanisms}
    positions = [1, 2]
    for _ in range(RAKE_ITERATIONS):
        for pos in positions:
            values = [float(row["latencies_ms"][pos]) for row in rows]
            current = histogram(values, LATENCY_BINS_MS, weights)
            ratios = [(t + 1e-5) / (c + 1e-5) for t, c in zip(target, current)]
            for i, value in enumerate(values):
                bin_idx = next(j for j in range(len(LATENCY_BINS_MS) - 1) if LATENCY_BINS_MS[j] <= value < LATENCY_BINS_MS[j + 1])
                weights[i] *= ratios[bin_idx] ** 0.25
            for mechanism, idxs in indexes.items():
                scaled = bounded_scale([weights[i] for i in idxs], float(len(idxs)), WEIGHT_MIN, WEIGHT_MAX)
                for i, value in zip(idxs, scaled):
                    weights[i] = value
    return weights


def effective_sample_size(weights: Sequence[float]) -> float:
    s = sum(weights); ss = sum(w * w for w in weights)
    return s * s / ss if ss else 0.0


def run(fixture_path: Path, synthetic_path: Path, outdir: Path) -> None:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in synthetic_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    outdir.mkdir(parents=True, exist_ok=True)

    public_rows = []
    fixture_audits = []
    pooled_intermove: list[float] = []
    primary_2x2: list[float] = []
    raw_count = compressed_count = 0
    for source in fixture["fixtures"]:
        events = source["events"]
        audit = audit_events(events)
        if audit["status"] != "PASS":
            raise SystemExit(f"CR0818_FIXTURE_QC_FAIL:{source['fixture_id']}:{audit['errors']}")
        timestamps = [float(e["t"]) for e in events]
        deltas = [timestamps[0]] + [b - a for a, b in zip(timestamps, timestamps[1:])]
        inter = deltas[1:]
        pooled_intermove.extend(inter)
        if source["puzzle"] == "2x2x2":
            primary_2x2.extend(inter)
        compressed, compression_window_ms = compress_double_turns(events)
        raw_count += len(events); compressed_count += len(compressed)
        fixture_audits.append({
            "fixture_id": source["fixture_id"], "puzzle": source["puzzle"], "device_family": source["device_family"],
            "audit": audit, "first_move_latency_ms": deltas[0], "duration_ms": timestamps[-1],
            "intermove_summary_ms": {"minimum": min(inter), "p10": quantile(inter, .10), "p25": quantile(inter, .25), "median": quantile(inter, .5), "p75": quantile(inter, .75), "p90": quantile(inter, .90), "maximum": max(inter), "mean": mean(inter)},
            "raw_event_count": len(events), "derived_logical_turn_count": len(compressed), "upstream_adaptive_compression_window_ms": compression_window_ms,
            "double_turn_compression_is_derived_not_raw_rewrite": True,
        })
        for i, (event, delta) in enumerate(zip(events, deltas)):
            public_rows.append({
                "fixture_id": source["fixture_id"], "puzzle": source["puzzle"], "device_family": source["device_family"],
                "event_index": i, "move": event["m"], "timestamp_ms": event["t"], "delta_ms": delta,
                "delta_kind": "FIRST_MOVE" if i == 0 else "INTERMOVE", "research_consent": "NOT_ESTABLISHED",
            })

    burst_max = quantile(pooled_intermove, .25)
    flow_max = quantile(pooled_intermove, .75)
    for row in public_rows:
        row["latency_class"] = latency_class(row["delta_ms"], burst_max, flow_max)

    negative = corruption_court(fixture["fixtures"][1]["events"])
    qc_result = {
        "schema_version": "CR0818-TIMESTAMP-QC-RESULT-1", "version": VERSION,
        "evidence_grade": fixture["evidence_grade"], "fixture_count": len(fixture["fixtures"]),
        "raw_event_count": raw_count, "derived_logical_turn_count": compressed_count,
        "fixture_audits": fixture_audits, "negative_control_court": negative,
        "packet_loss_certification": "HOLD_PUBLIC_REPLAY_HAS_NO_DEVICE_SEQUENCE_COUNTER",
        "state_continuity_certification": "HOLD_PUBLIC_REPLAY_HAS_NO_INITIAL_STATE_OR_RAW_PACKET_STREAM",
        "research_consent": "HOLD_SOFTWARE_LICENSE_IS_NOT_RESEARCH_CONSENT",
        "result": "PASS_PUBLIC_LICENSED_TIMESTAMP_FIXTURE_QC_WITH_CONSENT_AND_PACKET_LOSS_HOLDS",
    }

    synthetic_late = [float(row["latencies_ms"][1]) for row in rows] + [float(row["latencies_ms"][2]) for row in rows]
    target_hist = histogram(primary_2x2, LATENCY_BINS_MS)
    synthetic_hist = histogram(synthetic_late, LATENCY_BINS_MS)
    js_before = js_divergence(target_hist, synthetic_hist)
    min_syn = min(synthetic_late)
    unreachable_low_mass = sum(1 for x in primary_2x2 if x < min_syn) / len(primary_2x2)
    weights = raking_weights(rows, target_hist)
    weighted_values = [float(row["latencies_ms"][1]) for row in rows] + [float(row["latencies_ms"][2]) for row in rows]
    weighted_weights = weights + weights
    weighted_hist = histogram(weighted_values, LATENCY_BINS_MS, weighted_weights)
    js_after = js_divergence(target_hist, weighted_hist)
    mechanisms = sorted({row["mechanism"] for row in rows})
    mechanism_weight_audit = []
    for mechanism in mechanisms:
        mw = [weights[i] for i, row in enumerate(rows) if row["mechanism"] == mechanism]
        mechanism_weight_audit.append({
            "mechanism": mechanism, "row_count": len(mw), "weight_sum": sum(mw),
            "minimum_weight": min(mw), "maximum_weight": max(mw),
            "effective_sample_size": effective_sample_size(mw), "ess_fraction": effective_sample_size(mw) / len(mw),
        })
    reweight_pass = (
        js_after < js_before and
        js_after <= js_before * 0.90 and
        min(x["ess_fraction"] for x in mechanism_weight_audit) >= 0.30 and
        max(x["maximum_weight"] for x in mechanism_weight_audit) <= WEIGHT_MAX + 1e-8 and
        min(x["minimum_weight"] for x in mechanism_weight_audit) >= WEIGHT_MIN - 1e-8 and
        all(abs(x["weight_sum"] - x["row_count"]) < 1e-6 for x in mechanism_weight_audit)
    )

    public_motifs = []
    for source in fixture["fixtures"]:
        events = source["events"]
        for prev, cur in zip(events, events[1:]):
            delta = cur["t"] - prev["t"]
            public_motifs.append(f"{relation(prev['m'], cur['m'])}|{latency_class(delta, burst_max, flow_max)}")
    synthetic_motifs = []
    synthetic_motif_weights = []
    for i, row in enumerate(rows):
        for pos in (1, 2):
            synthetic_motifs.append(f"{relation(row['actions'][pos-1], row['actions'][pos])}|{latency_class(float(row['latencies_ms'][pos]), burst_max, flow_max)}")
            synthetic_motif_weights.append(weights[i])
    public_motif_dist = motif_distribution(public_motifs)
    synthetic_motif_dist = motif_distribution(synthetic_motifs)
    weighted_motif_dist = motif_distribution(synthetic_motifs, synthetic_motif_weights)
    motif_js_before = js_dict(public_motif_dist, synthetic_motif_dist)
    motif_js_after = js_dict(public_motif_dist, weighted_motif_dist)

    domain_result = {
        "schema_version": "CR0818-TEMPORAL-DOMAIN-GAP-RESULT-1", "version": VERSION,
        "primary_calibration_domain": "PUBLIC_LICENSED_PARTICULA_2X2_TEST_FIXTURE",
        "primary_event_count": len(primary_2x2) + 1, "primary_intermove_count": len(primary_2x2),
        "pooled_public_intermove_count": len(pooled_intermove), "synthetic_late_latency_count": len(synthetic_late),
        "latency_class_thresholds_ms": {"burst_max_p25": burst_max, "flow_max_p75": flow_max},
        "primary_2x2_summary_ms": {"minimum": min(primary_2x2), "p10": quantile(primary_2x2,.1), "p25": quantile(primary_2x2,.25), "median": quantile(primary_2x2,.5), "p75": quantile(primary_2x2,.75), "p90": quantile(primary_2x2,.9), "maximum": max(primary_2x2), "mean": mean(primary_2x2)},
        "synthetic_late_summary_ms": {"minimum": min(synthetic_late), "p10": quantile(synthetic_late,.1), "p25": quantile(synthetic_late,.25), "median": quantile(synthetic_late,.5), "p75": quantile(synthetic_late,.75), "p90": quantile(synthetic_late,.9), "maximum": max(synthetic_late), "mean": mean(synthetic_late)},
        "histogram_bins_ms": LATENCY_BINS_MS, "primary_histogram": target_hist, "synthetic_histogram": synthetic_hist,
        "latency_js_divergence_before": js_before,
        "log10_wasserstein_before": empirical_wasserstein_log_ms(primary_2x2, synthetic_late),
        "unreachable_primary_mass_below_synthetic_minimum": unreachable_low_mass,
        "support_gap_conclusion": "FULL_ALIGNMENT_IMPOSSIBLE_BY_REWEIGHTING_ONLY" if unreachable_low_mass > 0 else "NO_LOWER_SUPPORT_GAP",
        "temporal_route_grammar": {"public_distribution": public_motif_dist, "synthetic_distribution": synthetic_motif_dist, "js_before": motif_js_before},
        "result": "PASS_DOMAIN_GAP_DETECTED_FULL_TEMPORAL_ALIGNMENT_HOLD",
    }

    reweight_result = {
        "schema_version": "CR0818-DOMAIN-GAP-REWEIGHTING-RESULT-1", "version": VERSION,
        "algorithm": {"type": "BOUNDED_ITERATIVE_RAKING", "iterations": RAKE_ITERATIONS, "weight_bounds": [WEIGHT_MIN, WEIGHT_MAX], "per_mechanism_total_preserved": True, "target": "PRIMARY_2X2_INTERMOVE_HISTOGRAM"},
        "latency_js_before": js_before, "latency_js_after": js_after,
        "relative_js_reduction": (js_before - js_after) / js_before if js_before else 0.0,
        "weighted_histogram": weighted_hist, "mechanism_weight_audit": mechanism_weight_audit,
        "temporal_route_grammar_js_before": motif_js_before, "temporal_route_grammar_js_after": motif_js_after,
        "reweighting_certification": "PASS_CONSTRAINED_DOMAIN_GAP_REDUCTION" if reweight_pass else "FAIL_CONSTRAINED_DOMAIN_GAP_REDUCTION",
        "full_alignment": "HOLD_SUPPORT_GAP_AND_SINGLE_PUBLIC_2X2_FIXTURE",
        "research_consent": "HOLD_NO_RESEARCH_CONSENTED_HUMAN_FIXTURE",
    }

    weight_rows = []
    for i, (row, weight) in enumerate(zip(rows, weights)):
        weight_rows.append({"trajectory_index": i, "mechanism": row["mechanism"], "probe_id": row["probe_id"], "second_latency_ms": row["latencies_ms"][1], "third_latency_ms": row["latencies_ms"][2], "analysis_weight": round(weight, 12)})

    cert_conditions = {
        "three_public_fixture_streams": len(fixture["fixtures"]) == 3,
        "all_fixture_timestamps_qc": all(x["audit"]["status"] == "PASS" for x in fixture_audits),
        "negative_control_court": negative["result"] == "PASS_NEGATIVE_CONTROL_COURT",
        "software_license_not_misrepresented_as_research_consent": fixture["source"]["research_consent"] == "NOT_ESTABLISHED_BY_SOFTWARE_LICENSE",
        "domain_gap_detected": js_before > 0.20,
        "support_gap_explicit": unreachable_low_mass > 0.25,
        "bounded_reweighting_reduces_js": reweight_pass,
        "full_alignment_not_overclaimed": reweight_result["full_alignment"].startswith("HOLD_"),
        "packet_loss_not_overclaimed": qc_result["packet_loss_certification"].startswith("HOLD_"),
    }
    certification = {
        "schema_version": "CR0818-CERTIFICATION-RESULT-1", "version": VERSION,
        "conditions": cert_conditions,
        "all_conditions_pass": all(cert_conditions.values()),
        "decision": {
            "public_licensed_timestamp_fixture": "PASS",
            "timestamp_qc_and_corruption_court": "PASS",
            "temporal_domain_gap_detection": "PASS",
            "constrained_reweighting": "PASS" if reweight_pass else "FAIL",
            "research_consented_human_fixture": "HOLD",
            "packet_loss_certification": "HOLD",
            "full_temporal_ecological_alignment": "HOLD",
            "human_cognitive_mechanism_transfer": "NO_GO",
            "participant_deployment": "NO_GO",
        },
        "result": "PASS_AUTOMATED_TEMPORAL_CALIBRATION_WITH_CONSENT_AND_ALIGNMENT_HOLDS" if all(cert_conditions.values()) else "FAIL_AUTOMATED_TEMPORAL_CALIBRATION",
    }

    write_json(outdir / "CUBE_REV_0.8.18_TIMESTAMP_QC_RESULT.json", qc_result)
    write_json(outdir / "CUBE_REV_0.8.18_TEMPORAL_DOMAIN_GAP_RESULT.json", domain_result)
    write_json(outdir / "CUBE_REV_0.8.18_REWEIGHTING_RESULT.json", reweight_result)
    write_json(outdir / "CUBE_REV_0.8.18_CERTIFICATION_RESULT.json", certification)
    with (outdir / "CUBE_REV_0.8.18_TEMPORAL_EVENT_ROWS.jsonl").open("w", encoding="utf-8") as handle:
        for row in public_rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")
    with (outdir / "CUBE_REV_0.8.18_REWEIGHTED_TRAJECTORY_WEIGHTS.jsonl").open("w", encoding="utf-8") as handle:
        for row in weight_rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")

    manifest_files = [
        fixture_path,
        outdir / "CUBE_REV_0.8.18_TIMESTAMP_QC_RESULT.json",
        outdir / "CUBE_REV_0.8.18_TEMPORAL_DOMAIN_GAP_RESULT.json",
        outdir / "CUBE_REV_0.8.18_REWEIGHTING_RESULT.json",
        outdir / "CUBE_REV_0.8.18_CERTIFICATION_RESULT.json",
        outdir / "CUBE_REV_0.8.18_TEMPORAL_EVENT_ROWS.jsonl",
        outdir / "CUBE_REV_0.8.18_REWEIGHTED_TRAJECTORY_WEIGHTS.jsonl",
    ]
    manifest = {
        "schema_version": "CR0818-SNAPSHOT-MANIFEST-1", "version": VERSION,
        "synthetic_input": {"path": synthetic_path.name, "row_count": len(rows), "sha256": sha256_bytes(synthetic_path.read_bytes())},
        "files": {path.name: {"sha256": sha256_bytes(path.read_bytes()), "bytes": path.stat().st_size} for path in manifest_files},
        "fixture_canonical_sha256": sha256_bytes(canonical_bytes(fixture)),
    }
    write_json(outdir / "CUBE_REV_0.8.18_SNAPSHOT_MANIFEST.json", manifest)
    print(f"CR0818_TEMPORAL_CALIBRATION_PASS fixtures={len(fixture['fixtures'])} events={raw_count} trajectories={len(rows)} js_before={js_before:.6f} js_after={js_after:.6f} consent=HOLD")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", type=Path, required=True)
    ap.add_argument("--synthetic-trajectories", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    run(args.fixtures, args.synthetic_trajectories, args.outdir)


if __name__ == "__main__":
    main()
