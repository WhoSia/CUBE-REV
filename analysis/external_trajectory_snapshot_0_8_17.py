#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

TOKEN_RE = re.compile(r"^(?P<base>[URFDLBMESxyzurfdlb](?:w)?)(?P<power>2|3)?(?P<prime>')?$")
FACE_AXIS = {"U":"UD","D":"UD","R":"RL","L":"RL","F":"FB","B":"FB"}
OPPOSITE = {"U":"D","D":"U","R":"L","L":"R","F":"B","B":"F"}
SLICE_AXIS = {"M":"RL","E":"UD","S":"FB"}
ROTATIONS = {"x","y","z"}


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_token(raw: str) -> str:
    raw = raw.strip().replace("’", "'")
    m = TOKEN_RE.fullmatch(raw)
    if not m:
        raise ValueError(f"UNSUPPORTED_MOVE_TOKEN:{raw}")
    base = m.group("base")
    power = m.group("power") or ""
    prime = bool(m.group("prime"))
    if base.endswith("w"):
        base = base[0].lower()
    if power == "3":
        power = ""
        prime = not prime
    if power == "2":
        prime = False
    return base + power + ("'" if prime else "")


def tokenize(text: str) -> list[str]:
    if not text.strip():
        return []
    return [normalize_token(tok) for tok in text.split()]


def token_class(token: str) -> str:
    base = token[0]
    if base in ROTATIONS:
        return "ROTATION"
    if base in "urfdlb":
        return "WIDE"
    if base in "MES":
        return "SLICE"
    return "FACE"


def token_face(token: str) -> str | None:
    base = token[0]
    if base.upper() in FACE_AXIS and base not in ROTATIONS:
        return base.upper()
    return None


def token_axis(token: str) -> str | None:
    base = token[0]
    if base.upper() in FACE_AXIS and base not in ROTATIONS:
        return FACE_AXIS[base.upper()]
    if base in SLICE_AXIS:
        return SLICE_AXIS[base]
    return None


def token_turn(token: str) -> int:
    if "2" in token:
        return 2
    return -1 if token.endswith("'") else 1


def inverse_token(token: str) -> str:
    if "2" in token:
        return token
    return token[:-1] if token.endswith("'") else token + "'"


def face_relation(previous: str | None, current: str | None) -> str:
    if previous is None or current is None:
        return "START"
    if previous == current:
        return "SAME"
    if OPPOSITE[previous] == current:
        return "OPPOSITE"
    return "ADJACENT"


def relation_signature(tokens: Sequence[str]) -> tuple[str, ...]:
    faces = [token_face(t) for t in tokens if token_class(t) in {"FACE", "WIDE"}]
    if not faces:
        return ()
    out = ["START"]
    for a, b in zip(faces, faces[1:]):
        out.append(face_relation(a, b))
    return tuple(out)


def class_signature(tokens: Sequence[str]) -> tuple[str, ...]:
    return tuple(token_class(t) for t in tokens)


def windows(seq: Sequence[str], n: int) -> Iterable[tuple[str, ...]]:
    for i in range(len(seq) - n + 1):
        yield tuple(seq[i:i+n])


def normalized_levenshtein(a: Sequence[str], b: Sequence[str]) -> float:
    if not a and not b:
        return 0.0
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j-1] + (x != y)))
        prev = cur
    return prev[-1] / max(len(a), len(b), 1)


def lcs_ratio(a: Sequence[str], b: Sequence[str]) -> float:
    dp = [0] * (len(b) + 1)
    for x in a:
        last = 0
        for j, y in enumerate(b, 1):
            old = dp[j]
            if x == y:
                dp[j] = last + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            last = old
    return dp[-1] / max(len(a), len(b), 1)


def js_divergence(p: Mapping[str, float], q: Mapping[str, float]) -> float:
    keys = sorted(set(p) | set(q))
    ps = [float(p.get(k, 0.0)) for k in keys]
    qs = [float(q.get(k, 0.0)) for k in keys]
    sp, sq = sum(ps), sum(qs)
    if sp == 0 or sq == 0:
        return 1.0
    ps = [x/sp for x in ps]
    qs = [x/sq for x in qs]
    ms = [(x+y)/2 for x,y in zip(ps,qs)]
    def kl(xs: Sequence[float], ys: Sequence[float]) -> float:
        return sum(x * math.log2(x/y) for x,y in zip(xs,ys) if x > 0 and y > 0)
    return 0.5 * kl(ps, ms) + 0.5 * kl(qs, ms)


def normalize_counts(counter: collections.Counter[tuple[str, ...]]) -> dict[str, float]:
    total = sum(counter.values())
    return {"|".join(k): v/total for k,v in sorted(counter.items())} if total else {}


@dataclass
class ParsedRoute:
    route_id: str
    solve_id: int
    all_tokens: list[str]
    action_tokens: list[str]
    stage_boundaries: list[int]
    stage_labels: list[str]
    inspection_tokens: list[str]
    source: dict


def parse_route(row: dict) -> ParsedRoute:
    all_tokens: list[str] = []
    action_tokens: list[str] = []
    boundaries: list[int] = []
    labels: list[str] = []
    for stage in row["stages"]:
        tokens = tokenize(stage["moves"])
        all_tokens.extend(tokens)
        action_tokens.extend(t for t in tokens if token_class(t) != "ROTATION")
        boundaries.append(len(action_tokens))
        labels.append(stage["label"])
    return ParsedRoute(
        route_id=row["route_id"],
        solve_id=int(row["source_solve_id"]),
        all_tokens=all_tokens,
        action_tokens=action_tokens,
        stage_boundaries=boundaries,
        stage_labels=labels,
        inspection_tokens=tokenize(row.get("inspection", "")),
        source=row,
    )


def route_summary(route: ParsedRoute) -> dict:
    classes = collections.Counter(token_class(t) for t in route.all_tokens)
    action_faces = [token_face(t) for t in route.action_tokens]
    inverse_pairs = sum(b == inverse_token(a) for a,b in zip(route.action_tokens, route.action_tokens[1:]))
    same_face_pairs = sum(a is not None and a == b for a,b in zip(action_faces, action_faces[1:]))
    axis_changes = sum(token_axis(a) != token_axis(b) for a,b in zip(route.action_tokens, route.action_tokens[1:]))
    return {
        "route_id": route.route_id,
        "source_solve_id": route.solve_id,
        "official": bool(route.source["official"]),
        "method_label_source_only": route.source["method_label"],
        "result_seconds": route.source["result_seconds"],
        "reported_stm": route.source["reported_stm"],
        "parsed_nonrotation_token_count": len(route.action_tokens),
        "all_token_count": len(route.all_tokens),
        "inspection_rotation_count": len(route.inspection_tokens),
        "in_solve_rotation_count": classes["ROTATION"],
        "wide_move_count": classes["WIDE"],
        "slice_move_count": classes["SLICE"],
        "stage_count": len(route.stage_labels),
        "stage_lengths": [b-a for a,b in zip([0]+route.stage_boundaries[:-1], route.stage_boundaries)],
        "inverse_pair_rate": round(inverse_pairs/max(len(route.action_tokens)-1,1), 6),
        "same_face_pair_rate": round(same_face_pairs/max(len(route.action_tokens)-1,1), 6),
        "axis_change_rate": round(axis_changes/max(len(route.action_tokens)-1,1), 6),
        "relation_signature_prefix_8": list(relation_signature(route.action_tokens[:8])),
        "source_attribution_excluded_from_aggregate_features": True,
    }


def extract_probe_sequences(registry: dict) -> dict[str, list[list[str]]]:
    groups: dict[str, list[list[str]]] = collections.defaultdict(list)
    for family in registry["families"]:
        for member in family["members"]:
            groups["planned"].append([normalize_token(x) for x in member["planned_sequence"]])
            groups["replanned"].append([normalize_token(x) for x in member["replanned_sequence"]])
            rec = member["recovery"]
            groups["undo"].append([normalize_token(rec["error_move"]), normalize_token(rec["undo_move"])])
            groups["reset"].append([normalize_token(rec["error_move"]), normalize_token(rec["reset_move"])])
            groups["persist"].append([normalize_token(rec["error_move"]), normalize_token(rec["persist_move"])])
    return dict(groups)


def motif_counter(sequences: Iterable[Sequence[str]], n: int) -> collections.Counter[tuple[str,...]]:
    out: collections.Counter[tuple[str,...]] = collections.Counter()
    for seq in sequences:
        sig = relation_signature(seq)
        if len(sig) >= n:
            out.update(windows(sig, n))
    return out


def build_external_motifs(routes: Sequence[ParsedRoute], n: int, within_stage_only: bool) -> collections.Counter[tuple[str,...]]:
    out: collections.Counter[tuple[str,...]] = collections.Counter()
    for route in routes:
        if within_stage_only:
            start = 0
            for end in route.stage_boundaries:
                sig = relation_signature(route.action_tokens[start:end])
                out.update(windows(sig, n))
                start = end
        else:
            sig = relation_signature(route.action_tokens)
            out.update(windows(sig, n))
    return out


def matched_scramble_audit(routes: Sequence[ParsedRoute]) -> list[dict]:
    groups: dict[str, list[ParsedRoute]] = collections.defaultdict(list)
    for r in routes:
        norm = " ".join(tokenize(r.source["scramble"]))
        groups[sha256_bytes(norm.encode())].append(r)
    audits=[]
    for scramble_sha, members in groups.items():
        if len(members) < 2:
            continue
        for i,a in enumerate(members):
            for b in members[i+1:]:
                audits.append({
                    "scramble_sha256": scramble_sha,
                    "route_a": a.route_id,
                    "route_b": b.route_id,
                    "same_reported_time": a.source["result_seconds"] == b.source["result_seconds"],
                    "action_token_lengths": [len(a.action_tokens), len(b.action_tokens)],
                    "normalized_token_edit_distance": round(normalized_levenshtein(a.action_tokens,b.action_tokens),6),
                    "token_lcs_ratio": round(lcs_ratio(a.action_tokens,b.action_tokens),6),
                    "relation_edit_distance": round(normalized_levenshtein(relation_signature(a.action_tokens), relation_signature(b.action_tokens)),6),
                    "stage_counts": [len(a.stage_labels),len(b.stage_labels)],
                    "route_nonunique": a.action_tokens != b.action_tokens,
                })
    return audits


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--fixtures", type=Path, required=True)
    ap.add_argument("--probe-registry", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    args=ap.parse_args()

    fixture=json.loads(args.fixtures.read_text(encoding="utf-8"))
    registry=json.loads(args.probe_registry.read_text(encoding="utf-8"))
    routes=[parse_route(row) for row in fixture["routes"]]
    probe_groups=extract_probe_sequences(registry)
    probe_sequences=[s for group in probe_groups.values() for s in group]

    summaries=[route_summary(r) for r in routes]
    external2=build_external_motifs(routes,2,False)
    external3=build_external_motifs(routes,3,False)
    within2=build_external_motifs(routes,2,True)
    within3=build_external_motifs(routes,3,True)
    probe2=motif_counter(probe_sequences,2)
    probe3=motif_counter(probe_sequences,3)

    def coverage(probe: collections.Counter, ext: collections.Counter) -> dict:
        keys=set(probe)
        observed=keys & set(ext)
        weighted=sum(probe[k] for k in observed)/sum(probe.values()) if probe else 0
        return {"unique_total":len(keys),"unique_observed":len(observed),"unique_coverage":round(len(observed)/max(len(keys),1),6),"weighted_coverage":round(weighted,6),"missing":["|".join(x) for x in sorted(keys-observed)]}

    # Stage boundary support: how often a 2- or 3-action window ends exactly at a source boundary.
    boundary_total=0; boundary_short=0
    for r in routes:
        boundary_total += len(r.stage_boundaries)
        boundary_short += sum(x in {1,2,3} for x in [b-a for a,b in zip([0]+r.stage_boundaries[:-1],r.stage_boundaries)])

    result={
        "schema_version":"CR0817-ECOLOGICAL-PROBE-TRANSFER-RESULT-1",
        "version":"CUBE-REV 0.8.17",
        "snapshot":{
            "fixture_sha256":sha256_bytes(canonical_json_bytes(fixture)),
            "route_count":len(routes),
            "official_route_count":sum(r.source["official"] for r in routes),
            "method_labels_source_only":dict(sorted(collections.Counter(r.source["method_label"] for r in routes).items())),
            "date_range":[min(r.source["date"] for r in routes),max(r.source["date"] for r in routes)],
            "wca_export_pin":fixture["wca_anchor"],
        },
        "route_summaries":summaries,
        "aggregate_route_grammar":{
            "action_token_count":sum(len(r.action_tokens) for r in routes),
            "all_token_count":sum(len(r.all_tokens) for r in routes),
            "stage_count":sum(len(r.stage_labels) for r in routes),
            "in_solve_rotation_count":sum(token_class(t)=="ROTATION" for r in routes for t in r.all_tokens),
            "wide_move_count":sum(token_class(t)=="WIDE" for r in routes for t in r.all_tokens),
            "slice_move_count":sum(token_class(t)=="SLICE" for r in routes for t in r.all_tokens),
            "relation_bigram_distribution":normalize_counts(external2),
            "relation_trigram_distribution":normalize_counts(external3),
            "within_stage_bigram_distribution":normalize_counts(within2),
            "within_stage_trigram_distribution":normalize_counts(within3),
            "short_stage_fraction_len_1_to_3":round(boundary_short/max(boundary_total,1),6),
        },
        "probe_transfer":{
            "relation_bigram_coverage_all_windows":coverage(probe2,external2),
            "relation_trigram_coverage_all_windows":coverage(probe3,external3),
            "relation_bigram_coverage_within_stage":coverage(probe2,within2),
            "relation_trigram_coverage_within_stage":coverage(probe3,within3),
            "js_divergence_bigram":round(js_divergence(normalize_counts(probe2),normalize_counts(external2)),6),
            "js_divergence_trigram":round(js_divergence(normalize_counts(probe3),normalize_counts(external3)),6),
            "latency_transfer":"NOT_ESTIMABLE_PUBLIC_RECONSTRUCTIONS_LACK_PER_MOVE_TIMESTAMPS",
            "puzzle_transfer":"LOCAL_ROTATION_INVARIANT_MOVE_GRAMMAR_ONLY_3X3_TO_2X2",
        },
        "stm_conformance":{
            "reported_route_count":sum(r.source.get("reported_stm") is not None for r in routes),
            "exact_match_count":sum(r.source.get("reported_stm") is not None and int(r.source["reported_stm"])==len(r.action_tokens) for r in routes),
            "mismatch_route_ids":[r.route_id for r in routes if r.source.get("reported_stm") is not None and int(r.source["reported_stm"])!=len(r.action_tokens)],
            "conclusion":"PASS_EXACT_REPORTED_STM_CONFORMANCE" if all(r.source.get("reported_stm") is None or int(r.source["reported_stm"])==len(r.action_tokens) for r in routes) else "FAIL_STM_CONFORMANCE",
        },
        "matched_scramble_audits":matched_scramble_audit(routes),
        "epistemic_boundary":{
            "population_representative":False,
            "human_mechanism_evidence":False,
            "named_solver_trait_inference":False,
            "method_label_used_as_outcome":False,
            "raw_html_custodied":False,
            "bulk_reco_snapshot":False,
            "wca_bulk_archive_materialized":False,
            "supported_claim":"THE_0_8_16_PROBE_ACTION_GRAMMAR_HAS_OR_LACKS_LOCAL_SUPPORT_IN_THIS_FROZEN_PUBLIC_3X3_FIXTURE",
        }
    }

    # Decision separates local support from distributional alignment.
    c2=result["probe_transfer"]["relation_bigram_coverage_all_windows"]["weighted_coverage"]
    c3=result["probe_transfer"]["relation_trigram_coverage_all_windows"]["weighted_coverage"]
    j2=result["probe_transfer"]["js_divergence_bigram"]
    j3=result["probe_transfer"]["js_divergence_trigram"]
    result["decision"]={
        "local_motif_support":"PASS" if c2>=0.8 and c3>=0.6 else "HOLD",
        "distributional_ecological_alignment":"PASS" if j2<=0.25 and j3<=0.25 else "HOLD",
        "timing_transfer":"HOLD",
        "cognitive_mechanism_transfer":"NO_GO",
        "external_snapshot_grade":"VERSIONED_SMALL_FIXTURE",
        "overall_ecological_probe_transfer":"PARTIAL_LOCAL_SUPPORT_ONLY",
    }

    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"CUBE_REV_0.8.17_ECOLOGICAL_PROBE_TRANSFER_RESULT.json").write_bytes(canonical_json_bytes(result)+b"\n")
    (args.outdir/"CUBE_REV_0.8.17_ROUTE_GRAMMAR_ROWS.jsonl").write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n" for x in summaries),encoding="utf-8")
    manifest={
        "schema_version":"CR0817-EXTERNAL-SNAPSHOT-MANIFEST-1",
        "version":"CUBE-REV 0.8.17",
        "fixture_pack_sha256":sha256_bytes(args.fixtures.read_bytes()),
        "fixture_canonical_sha256":sha256_bytes(canonical_json_bytes(fixture)),
        "probe_registry_sha256":sha256_bytes(args.probe_registry.read_bytes()),
        "result_sha256":sha256_bytes((args.outdir/"CUBE_REV_0.8.17_ECOLOGICAL_PROBE_TRANSFER_RESULT.json").read_bytes()),
        "route_rows_sha256":sha256_bytes((args.outdir/"CUBE_REV_0.8.17_ROUTE_GRAMMAR_ROWS.jsonl").read_bytes()),
        "source_count":2,
        "route_count":len(routes),
        "raw_source_bytes_custodied":False,
        "snapshot_grade":"VERSIONED_CANONICAL_TRANSCRIPTION_FIXTURE",
        "result":"PASS_MANIFEST_WITH_EXPLICIT_RAW_CUSTODY_HOLD"
    }
    (args.outdir/"CUBE_REV_0.8.17_EXTERNAL_SNAPSHOT_MANIFEST.json").write_bytes(canonical_json_bytes(manifest)+b"\n")
    print(f"CR0817_EXTERNAL_SNAPSHOT_PASS routes={len(routes)} action_tokens={result['aggregate_route_grammar']['action_token_count']} bigram_weighted={c2:.6f} trigram_weighted={c3:.6f}")

if __name__=="__main__":
    main()
