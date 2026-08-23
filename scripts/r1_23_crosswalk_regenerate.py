#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import statistics
import urllib.request
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation, ROUND_FLOOR
from pathlib import Path

PIN = "e5a6bb14961b5b26c882f9fb3bf13d61d9eba890"
REPO = "2017YANR02/cuberoot.me"
RECONS_URL = f"https://raw.githubusercontent.com/{REPO}/{PIN}/data/recon_backup/recons_backup.json"
ATTEMPTS_URL = f"https://raw.githubusercontent.com/{REPO}/{PIN}/data/recon_backup/wca_attempts.json"
EXPECTED = {
    "recons_backup.json": {"bytes": 2089782, "blob_sha1": "681adbeba019ef1fc657d6927287fd00dbca6c87"},
    "wca_attempts.json": {"bytes": 110301, "blob_sha1": "78949e0be591c8d99dfa5e5e5754b76eb4013df9"},
}
OUT = Path("r1_23_output")
OUT.mkdir(exist_ok=True)

EVENT_MAP_SOURCE = {
    "3x3": "333", "2x2": "222", "OH": "333oh",
    "3BLD": "333bf", "4BLD": "444bf", "5BLD": "555bf",
    "5x5": "555", "6x6": "666", "7x7": "777",
    "Pyraminx": "pyram", "Skewb": "skewb", "SQ1": "sq1",
    "Megaminx": "minx", "Clock": "clock",
}
EVENT_MAP_REPAIRED = {**EVENT_MAP_SOURCE, "4x4": "444"}
ROUND_MAP_SOURCE = {
    "R1": ["1", "d"], "R2": ["2", "e"],
    "R3": ["3", "g"], "Fi": ["f", "c", "b"],
}
RAW_ROUNDS = {"0", "1", "2", "3", "f", "d", "e", "g", "c", "b", "h"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CUBE-REV-R1.23/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def to_int(v):
    try:
        if v is None or v == "": return None
        return int(v)
    except Exception:
        return None


def raw_time_to_cs(v):
    if v is None or v == "": return None
    try:
        d = Decimal(str(v))
        if not d.is_finite() or d < 0: return None
        return int((d * Decimal(100)).to_integral_value(rounding=ROUND_FLOOR))
    except (InvalidOperation, ValueError, TypeError):
        return None


def repaired_round_candidates(rnd):
    if rnd is None: return []
    s = str(rnd).strip()
    if s in RAW_ROUNDS:
        return [s]
    if s in ROUND_MAP_SOURCE:
        return ROUND_MAP_SOURCE[s][:]
    return []


def flatten_legacy_r(sidecar):
    rows = []
    for comp_id, comp_data in sidecar.items():
        if not isinstance(comp_data, dict): continue
        for person_id, person_data in comp_data.items():
            if not isinstance(person_data, dict): continue
            for er, entry in person_data.items():
                if not isinstance(entry, dict): continue
                rmap = entry.get("r") or {}
                for k, rid in rmap.items():
                    sn = to_int(k)
                    attempts = entry.get("a") or []
                    val = attempts[sn-1] if sn and 1 <= sn <= len(attempts) else None
                    rows.append({
                        "competition_id": comp_id, "person_id": person_id,
                        "event_round": er, "attempt_index": sn,
                        "recon_id": to_int(rid), "wca_attempt_value": val,
                    })
    return rows


def build_source_faithful_index(recons):
    # Exact behavior of pinned build_wca_attempts.ts recon_index construction.
    idx = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for r in recons:
        comp = r.get("compWcaId") or ""
        person = r.get("personId") or ""
        event = r.get("event") or ""
        rnd = r.get("round") or ""
        sn = r.get("solveNum")
        rid = r.get("id")
        if not comp or not person: continue
        wca_event = EVENT_MAP_SOURCE.get(str(event))
        rts = ROUND_MAP_SOURCE.get(str(rnd), [])
        if not wca_event or not rts or not sn or not rid: continue
        for rt in rts:
            idx[comp][person][f"{wca_event}_{rt}"][str(sn)] = rid
    return idx


def materialize_faithful(idx, sidecar):
    rows = []
    for comp, persons in sidecar.items():
        for person, pdata in (persons or {}).items():
            for er, entry in (pdata or {}).items():
                ri = idx.get(comp, {}).get(person, {}).get(er, {})
                for sn_s, rid in ri.items():
                    sn = to_int(sn_s)
                    a = (entry or {}).get("a") or []
                    if sn and 1 <= sn <= len(a):
                        rows.append((comp, person, er, sn, to_int(rid), a[sn-1]))
    return rows


def main():
    recons_b = fetch(RECONS_URL)
    attempts_b = fetch(ATTEMPTS_URL)
    byte_audit = {}
    for name, data in [("recons_backup.json", recons_b), ("wca_attempts.json", attempts_b)]:
        exp = EXPECTED[name]
        byte_audit[name] = {
            "bytes": len(data), "expected_bytes": exp["bytes"],
            "git_blob_sha1": git_blob_sha1(data), "expected_git_blob_sha1": exp["blob_sha1"],
            "byte_count_pass": len(data) == exp["bytes"],
            "blob_sha1_pass": git_blob_sha1(data) == exp["blob_sha1"],
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    if not all(x["byte_count_pass"] and x["blob_sha1_pass"] for x in byte_audit.values()):
        raise SystemExit("Pinned-byte verification failed")

    recons = json.loads(recons_b)
    sidecar = json.loads(attempts_b)
    by_id = {to_int(r.get("id")): r for r in recons if to_int(r.get("id")) is not None}

    # Fresh source-faithful build, deliberately not inheriting old sidecar r values.
    faithful_idx = build_source_faithful_index(recons)
    faithful_rows = materialize_faithful(faithful_idx, sidecar)
    faithful_ids = {x[4] for x in faithful_rows}

    legacy = flatten_legacy_r(sidecar)
    legacy_by_attempt = defaultdict(list)
    for x in legacy:
        legacy_by_attempt[(x["competition_id"], x["person_id"], x["event_round"], x["attempt_index"])].append(x["recon_id"])

    repaired_rows = []
    exact_attempt_to_recons = defaultdict(list)
    status_counts = Counter()
    official_status_counts = Counter()
    event_counts_exact = Counter()
    round_counts = Counter(str(r.get("round")) for r in recons if r.get("round") not in (None, ""))
    wca_round_counts = Counter(str(r.get("round")) for r in recons if r.get("official") == "wca" and r.get("round") not in (None, ""))

    for r in recons:
        rid = to_int(r.get("id"))
        official = r.get("official") or ""
        comp = r.get("compWcaId") or ""
        person = r.get("personId") or ""
        event = r.get("event") or ""
        rnd = r.get("round")
        sn = to_int(r.get("solveNum"))
        raw_cs = raw_time_to_cs(r.get("rawTime"))
        wca_event = EVENT_MAP_REPAIRED.get(str(event))
        round_candidates = repaired_round_candidates(rnd)
        base = {
            "recon_id": rid, "official": official, "event": event,
            "compWcaId": comp, "personId": person, "round": rnd,
            "solveNum": sn, "method": r.get("method") or "",
            "rawTime": r.get("rawTime"), "raw_time_cs_floor": raw_cs,
            "source_faithful_regenerated": rid in faithful_ids,
        }

        if not rid:
            status = "KEY_INCOMPLETE_ID"; candidates = []
        elif not comp or not person or not sn:
            status = "KEY_INCOMPLETE_COMP_PERSON_SOLVENUM"; candidates = []
        elif not wca_event:
            status = "EVENT_UNSUPPORTED"; candidates = []
        elif not round_candidates:
            status = "ROUND_TOKEN_UNMAPPED"; candidates = []
        elif comp not in sidecar:
            status = "SIDECAR_COMP_MISSING"; candidates = []
        elif person not in (sidecar.get(comp) or {}):
            status = "SIDECAR_PERSON_MISSING"; candidates = []
        else:
            candidates = []
            pdata = sidecar[comp][person]
            for rt in round_candidates:
                er = f"{wca_event}_{rt}"
                entry = pdata.get(er)
                if not entry: continue
                a = entry.get("a") or []
                if sn < 1 or sn > len(a):
                    candidates.append((er, None, "OUT_OF_RANGE")); continue
                wv = a[sn-1]
                if wv == 0:
                    candidates.append((er, wv, "ZERO_PLACEHOLDER")); continue
                if raw_cs is None or wv < 0:
                    candidates.append((er, wv, "POSITION_ONLY")); continue
                candidates.append((er, wv, "VALUE_MATCH" if wv == raw_cs else "VALUE_MISMATCH"))

            vm = [c for c in candidates if c[2] == "VALUE_MATCH"]
            pos = [c for c in candidates if c[1] not in (None, 0)]
            if len(vm) == 1:
                status = "EXACT_REPAIRED_VALUE_VERIFIED"
            elif len(vm) > 1:
                status = "ROUND_CANDIDATE_COLLISION_VALUE_MATCH"
            elif len(pos) == 1 and pos[0][2] == "POSITION_ONLY":
                status = "POSITION_LINK_VALUE_NOT_TESTABLE"
            elif len(pos) == 1:
                status = "POSITION_LINK_VALUE_MISMATCH"
            elif len(pos) > 1:
                status = "ROUND_CANDIDATE_AMBIGUOUS"
            else:
                status = "SIDECAR_EVENT_ROUND_ATTEMPT_MISSING"

        status_counts[status] += 1
        if official == "wca": official_status_counts[status] += 1
        exact = [c for c in candidates if c[2] == "VALUE_MATCH"] if candidates else []
        chosen = exact[0] if len(exact) == 1 else None
        attempt_key = None
        if chosen:
            attempt_key = (comp, person, chosen[0], sn)
            exact_attempt_to_recons[attempt_key].append(rid)
            event_counts_exact[event] += 1
        legacy_same = legacy_by_attempt.get(attempt_key, []) if attempt_key else []
        if rid in legacy_same:
            legacy_shadow = "LEGACY_SAME_ATTEMPT_SAME_RECON"
        elif any(rid == x["recon_id"] for x in legacy):
            legacy_shadow = "LEGACY_RECON_PRESENT_OTHER_OR_UNRESOLVED_ATTEMPT"
        else:
            legacy_shadow = "NO_LEGACY_R"
        repaired_rows.append({
            **base, "status": status,
            "candidate_count": len(candidates) if candidates else 0,
            "candidate_event_rounds": "|".join(str(c[0]) for c in candidates) if candidates else "",
            "candidate_wca_values": "|".join(str(c[1]) for c in candidates) if candidates else "",
            "candidate_value_states": "|".join(str(c[2]) for c in candidates) if candidates else "",
            "chosen_event_round": chosen[0] if chosen else "",
            "chosen_wca_value": chosen[1] if chosen else "",
            "attempt_key": "|".join(map(str, attempt_key)) if attempt_key else "",
            "legacy_shadow": legacy_shadow,
        })

    # Referential-integrity and revision-cluster adjudication.
    collisions = {"|".join(map(str, k)): v for k, v in exact_attempt_to_recons.items() if len(v) > 1}
    exact_unique_attempts = len(exact_attempt_to_recons)
    exact_recon_rows = sum(len(v) for v in exact_attempt_to_recons.values())

    # Source-local attempt denominator: nonzero attempt slots only. Negative WCA outcomes are real slots.
    denominator = []
    exact_keys = set(exact_attempt_to_recons)
    for comp, persons in sidecar.items():
        for person, pdata in (persons or {}).items():
            for er, entry in (pdata or {}).items():
                a = entry.get("a") or []
                event_id, _, round_id = er.rpartition("_")
                for i, val in enumerate(a, 1):
                    if val == 0: continue
                    k = (comp, person, er, i)
                    denominator.append({
                        "competition_id": comp, "person_id": person, "event_round": er,
                        "event_id": event_id, "round_type_id": round_id,
                        "attempt_index": i, "wca_attempt_value": val,
                        "valid_positive_time": int(isinstance(val, (int, float)) and val > 0),
                        "repaired_exact_link": int(k in exact_keys),
                        "n_recon_versions": len(exact_attempt_to_recons.get(k, [])),
                    })

    # Legacy audit against repaired/current snapshot.
    legacy_audit = []
    for x in legacy:
        rid = x["recon_id"]
        k = (x["competition_id"], x["person_id"], x["event_round"], x["attempt_index"])
        rr = by_id.get(rid)
        repaired_same = rid in exact_attempt_to_recons.get(k, [])
        if rr is None:
            state = "LEGACY_ORPHAN_RECON_MISSING"
        elif repaired_same:
            state = "LEGACY_RECOVERED_BY_REPAIRED_COMPILER"
        elif rid in faithful_ids:
            state = "LEGACY_REGENERATED_SOURCE_FAITHFUL_OTHER_CHECK_NEEDED"
        else:
            state = "LEGACY_STALE_OR_SCHEMA_DRIFT"
        legacy_audit.append({**x, "recon_present": rr is not None, "audit_state": state,
                             "current_round": rr.get("round") if rr else None,
                             "current_event": rr.get("event") if rr else None,
                             "current_official": rr.get("official") if rr else None})

    def write_csv(path, rows):
        if not rows: return
        fields = list(rows[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

    write_csv(OUT / "CUBE_REV_0.10.5-R1.23_REGENERATED_CROSSWALK.csv", repaired_rows)
    write_csv(OUT / "CUBE_REV_0.10.5-R1.23_SOURCE_LOCAL_ATTEMPT_DENOMINATOR.csv", denominator)
    write_csv(OUT / "CUBE_REV_0.10.5-R1.23_LEGACY_R_AUDIT.csv", legacy_audit)

    # Stratum diagnostics for positivity.
    strata = defaultdict(lambda: [0, 0])
    solver = defaultdict(lambda: [0, 0])
    for d in denominator:
        key = (d["event_id"], d["round_type_id"], d["attempt_index"])
        strata[key][0] += 1; strata[key][1] += d["repaired_exact_link"]
        solver[d["person_id"]][0] += 1; solver[d["person_id"]][1] += d["repaired_exact_link"]
    stratum_rows = [{"event_id":k[0], "round_type_id":k[1], "attempt_index":k[2],
                     "denominator_n":v[0], "linked_n":v[1], "link_rate":v[1]/v[0]}
                    for k,v in sorted(strata.items())]
    solver_rows = [{"person_id":k, "denominator_n":v[0], "linked_n":v[1], "link_rate":v[1]/v[0]}
                   for k,v in sorted(solver.items())]
    write_csv(OUT / "CUBE_REV_0.10.5-R1.23_POSITIVITY_STRATA.csv", stratum_rows)
    write_csv(OUT / "CUBE_REV_0.10.5-R1.23_SOLVER_LINKAGE_STRATA.csv", solver_rows)

    positive_strata = [r for r in stratum_rows if r["linked_n"] > 0]
    zero_strata = [r for r in stratum_rows if r["linked_n"] == 0]
    mixed_strata = [r for r in stratum_rows if 0 < r["linked_n"] < r["denominator_n"]]
    all_link_strata = [r for r in stratum_rows if r["linked_n"] == r["denominator_n"]]

    wca_rows = [r for r in repaired_rows if r["official"] == "wca"]
    wca_exact = [r for r in wca_rows if r["status"] == "EXACT_REPAIRED_VALUE_VERIFIED"]
    all_exact = [r for r in repaired_rows if r["status"] == "EXACT_REPAIRED_VALUE_VERIFIED"]

    summary = {
        "schema_version": "CUBE-REV-R1.23-REGENERATION-1",
        "pinned_commit": PIN,
        "byte_audit": byte_audit,
        "snapshot": {
            "recon_records": len(recons),
            "wca_classified": sum(r.get("official") == "wca" for r in recons),
            "legacy_r_mappings": len(legacy),
        },
        "source_faithful_fresh_regeneration": {
            "mapping_rows": len(faithful_rows),
            "distinct_recon_ids": len(faithful_ids),
            "meaning": "fresh-from-current-snapshot result using pinned builder EVENT_MAP/ROUND_MAP, without inheriting old r cache",
        },
        "repaired_regeneration": {
            "all_exact_recon_rows": len(all_exact),
            "wca_exact_recon_rows": len(wca_exact),
            "exact_unique_attempts": exact_unique_attempts,
            "attempts_with_multiple_recon_versions": len(collisions),
            "status_counts_all": dict(status_counts),
            "status_counts_wca": dict(official_status_counts),
            "event_counts_exact": dict(event_counts_exact),
        },
        "round_vocabulary": {
            "all": dict(round_counts),
            "wca": dict(wca_round_counts),
            "builder_expected_labels": list(ROUND_MAP_SOURCE),
            "raw_wca_ids_accepted_by_repair": sorted(RAW_ROUNDS),
        },
        "legacy_audit_counts": dict(Counter(x["audit_state"] for x in legacy_audit)),
        "source_local_denominator": {
            "nonzero_attempt_slots": len(denominator),
            "linked_attempt_slots": sum(d["repaired_exact_link"] for d in denominator),
            "attempt_link_rate": (sum(d["repaired_exact_link"] for d in denominator) / len(denominator)) if denominator else None,
            "strata_total": len(stratum_rows),
            "strata_with_any_link": len(positive_strata),
            "strata_zero_link": len(zero_strata),
            "strata_mixed": len(mixed_strata),
            "strata_all_linked": len(all_link_strata),
        },
        "authority": {
            "selection_probability_target": "P(exact repaired reconstruction link | source-local sidecar attempt slot covariates)",
            "causal": False,
            "population_wca_generalization": False,
            "model_gate": "POSITIVITY_DIAGNOSTICS_REQUIRED_POST_ARTIFACT",
        },
    }
    (OUT / "CUBE_REV_0.10.5-R1.23_REGENERATION_SUMMARY.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "CUBE_REV_0.10.5-R1.23_COLLISION_CLUSTERS.json").write_text(json.dumps(collisions, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "CUBE_REV_0.10.5-R1.23_BYTE_AUDIT.json").write_text(json.dumps(byte_audit, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False))

if __name__ == "__main__":
    main()
