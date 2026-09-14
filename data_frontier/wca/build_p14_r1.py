#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import duckdb


def first_match(root: Path, stem: str) -> Path:
    matches = sorted(root.rglob(f"*{stem}*.tsv"))
    if not matches:
        raise FileNotFoundError(f"table not found: {stem}")
    exact = [p for p in matches if p.name.endswith(f"{stem}.tsv")]
    return exact[0] if exact else matches[0]


def qpath(p: Path) -> str:
    return str(p.resolve()).replace("'", "''")


def columns(con, view: str):
    return [r[0] for r in con.execute(f"DESCRIBE {view}").fetchall()]


def scalar(con, sql: str):
    return con.execute(sql).fetchone()[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--source-sha256", required=True)
    ap.add_argument("--api-json", required=True)
    args = ap.parse_args()

    root = Path(args.extract_dir)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    results_p = first_match(root, "results")
    attempts_p = first_match(root, "result_attempts")
    comps_p = first_match(root, "competitions")

    api = json.loads(Path(args.api_json).read_text(encoding="utf-8"))
    metadata_files = list(root.rglob("metadata.json"))
    metadata = json.loads(metadata_files[0].read_text(encoding="utf-8")) if metadata_files else {}

    con = duckdb.connect()
    con.execute("PRAGMA threads=4")
    con.execute("PRAGMA preserve_insertion_order=false")

    def make_view(name: str, path: Path):
        con.execute(
            f"""CREATE VIEW {name} AS
                SELECT * FROM read_csv_auto(
                    '{qpath(path)}',
                    delim='\\t',
                    header=true,
                    sample_size=200000,
                    ignore_errors=false
                )"""
        )

    make_view("results", results_p)
    make_view("result_attempts", attempts_p)
    make_view("competitions", comps_p)

    rc = columns(con, "results")
    ac = columns(con, "result_attempts")
    cc = columns(con, "competitions")
    required_results = {"id", "competition_id", "event_id", "round_type_id", "person_id"}
    required_attempts = {"result_id", "attempt_number", "value"}
    if not required_results.issubset(rc):
        raise RuntimeError(f"results schema mismatch: missing {sorted(required_results-set(rc))}; got={rc}")
    if not required_attempts.issubset(ac):
        raise RuntimeError(f"result_attempts schema mismatch: missing {sorted(required_attempts-set(ac))}; got={ac}")
    if "id" not in cc:
        raise RuntimeError(f"competitions schema mismatch: no id; got={cc}")

    if "start_date" in cc:
        comp_date = "CAST(c.start_date AS DATE)"
    elif {"year", "month", "day"}.issubset(cc):
        comp_date = "make_date(CAST(c.year AS INTEGER), CAST(c.month AS INTEGER), CAST(c.day AS INTEGER))"
    else:
        comp_date = "CAST(NULL AS DATE)"

    format_expr = "r.format_id" if "format_id" in rc else "CAST(NULL AS VARCHAR)"
    best_expr = "r.best" if "best" in rc else "CAST(NULL AS BIGINT)"
    avg_expr = "r.average" if "average" in rc else "CAST(NULL AS BIGINT)"
    status_case = """CASE
        WHEN a.value > 0 THEN 'VALID'
        WHEN a.value = -1 THEN 'DNF'
        WHEN a.value = -2 THEN 'DNS'
        WHEN a.value = 0 THEN 'NO_RESULT'
        ELSE 'UNEXPECTED_VALUE'
    END"""

    con.execute(f"""
        CREATE VIEW joined AS
        SELECT
          r.id AS result_id,
          r.competition_id,
          {comp_date} AS competition_date,
          r.event_id,
          r.round_type_id,
          {format_expr} AS format_id,
          CAST(r.person_id AS VARCHAR) AS wca_person_id,
          substr(sha256('CUBE-REV-WCA-v1:' || CAST(r.person_id AS VARCHAR)), 1, 24) AS competitor_key,
          a.attempt_number,
          CAST(a.value AS BIGINT) AS raw_value,
          {status_case} AS attempt_status,
          CASE WHEN r.event_id='333' AND a.value>0 THEN CAST(a.value AS BIGINT) ELSE NULL END AS solve_centiseconds,
          CASE WHEN r.event_id='333' AND a.value>0 THEN CAST(a.value AS DOUBLE)/100.0 ELSE NULL END AS solve_seconds,
          {best_expr} AS round_best_raw,
          {avg_expr} AS round_average_raw
        FROM result_attempts a
        JOIN results r ON a.result_id = r.id
        LEFT JOIN competitions c ON r.competition_id = c.id
    """)

    con.execute(f"""
        COPY (
          SELECT
            competitor_key, competition_id, competition_date, event_id, round_type_id,
            format_id, result_id, attempt_number, raw_value, attempt_status,
            solve_centiseconds, solve_seconds, round_best_raw, round_average_raw
          FROM joined
          WHERE event_id='333'
          ORDER BY competitor_key, competition_date NULLS LAST, competition_id, result_id, attempt_number
        ) TO '{qpath(out / 'wca_333_attempt_long.parquet')}'
        (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

    con.execute(f"""
        COPY (
          SELECT event_id, attempt_status, count(*) AS n
          FROM joined
          GROUP BY event_id, attempt_status
          ORDER BY event_id, attempt_status
        ) TO '{qpath(out / 'wca_event_attempt_status_census.csv')}'
        (HEADER, DELIMITER ',')
    """)

    con.execute(f"""
        COPY (
          SELECT
            competitor_key,
            min(competition_date) AS first_competition_date,
            max(competition_date) AS last_competition_date,
            count(DISTINCT competition_id) AS competitions,
            count(*) AS attempt_rows,
            sum(CASE WHEN attempt_status='VALID' THEN 1 ELSE 0 END) AS valid_attempts,
            sum(CASE WHEN attempt_status='DNF' THEN 1 ELSE 0 END) AS dnf_attempts,
            sum(CASE WHEN attempt_status='DNS' THEN 1 ELSE 0 END) AS dns_attempts,
            sum(CASE WHEN attempt_status='NO_RESULT' THEN 1 ELSE 0 END) AS no_result_rows
          FROM joined
          WHERE event_id='333'
          GROUP BY competitor_key
          ORDER BY competitor_key
        ) TO '{qpath(out / 'wca_333_competitor_longitudinal_index.parquet')}'
        (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

    counts = dict(con.execute("""
        SELECT attempt_status, count(*)
        FROM joined WHERE event_id='333'
        GROUP BY attempt_status
    """).fetchall())
    total_333 = scalar(con, "SELECT count(*) FROM joined WHERE event_id='333'")
    persons_333 = scalar(con, "SELECT count(DISTINCT competitor_key) FROM joined WHERE event_id='333'")
    comps_333 = scalar(con, "SELECT count(DISTINCT competition_id) FROM joined WHERE event_id='333'")
    min_date, max_date = con.execute(
        "SELECT min(competition_date), max(competition_date) FROM joined WHERE event_id='333'"
    ).fetchone()
    unexpected = counts.get("UNEXPECTED_VALUE", 0)

    schema = {
      "dataset": "CUBE-REV WCA 3x3 attempt-level longitudinal spine",
      "schema_version": "P14-R1.1",
      "primary_key_semantics": ["result_id", "attempt_number"],
      "identity_policy": {
        "competitor_key": "first 24 hex chars of SHA-256('CUBE-REV-WCA-v1:' + public WCA person_id)",
        "warning": "pseudonymous convenience key, not anonymization; source identifiers are public and recoverable from the WCA export",
        "release_table_drops_name": True
      },
      "attempt_value_semantics": {
        "positive": "valid event-dependent result; for event_id=333, centiseconds",
        "-1": "DNF",
        "-2": "DNS",
        "0": "NO_RESULT; preserved as a distinct source state, never imputed as DNF/DNS/valid",
        "other_nonpositive": "UNEXPECTED_VALUE -> preanalysis HOLD"
      },
      "columns": [
        "competitor_key", "competition_id", "competition_date", "event_id", "round_type_id",
        "format_id", "result_id", "attempt_number", "raw_value", "attempt_status",
        "solve_centiseconds", "solve_seconds", "round_best_raw", "round_average_raw"
      ]
    }
    (out / "schema.json").write_text(json.dumps(schema, indent=2, default=str), encoding="utf-8")

    manifest = {
      "stage": "CUBE-REV Generation III G3-P14-R1",
      "source": {
        "provider": "World Cube Association",
        "api_endpoint": "https://www.worldcubeassociation.org/api/v0/export/public",
        "api_export_date": api.get("export_date"),
        "api_export_version": api.get("export_version"),
        "tsv_url": api.get("tsv_url"),
        "tsv_filesize_bytes_reported": api.get("tsv_filesize_bytes"),
        "archive_sha256": args.source_sha256,
        "embedded_metadata": metadata,
        "files_used": {
          "results": results_p.name,
          "result_attempts": attempts_p.name,
          "competitions": comps_p.name
        }
      },
      "wca_333_census": {
        "attempt_rows": total_333,
        "competitors": persons_333,
        "competitions": comps_333,
        "date_min": str(min_date) if min_date is not None else None,
        "date_max": str(max_date) if max_date is not None else None,
        "status_counts": counts
      },
      "preanalysis_verdict": "PASS_SOURCE_SEMANTICS" if unexpected == 0 else "HOLD_UNEXPECTED_ATTEMPT_VALUES",
      "claims_not_authorized": [
        "causal cognitive mechanism",
        "clinical inference",
        "attempt-level within-solve cognitive state",
        "population representativeness outside WCA competitors"
      ]
    }
    (out / "p14_r1_manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

    notice = f"""# CUBE-REV P14-R1 derived-data notice

Source: World Cube Association Results Export v2.
Export date: {api.get('export_date')}
Format version: {api.get('export_version')}
Source archive SHA-256: `{args.source_sha256}`

This derived package does not include competitor names. `competitor_key` is a deterministic
pseudonymous convenience key derived from the public WCA person identifier; it is not an
anonymization guarantee.

Attempt-state semantics are preserved exactly:
- positive value: valid result (3x3 values are centiseconds)
- `-1`: DNF
- `-2`: DNS
- `0`: NO_RESULT
No one of these states is silently recoded into another.

Required WCA attribution for redistribution must accompany any public release.
"""
    (out / "NOTICE.md").write_text(notice, encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))


if __name__ == "__main__":
    main()
