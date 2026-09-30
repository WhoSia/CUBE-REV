#!/usr/bin/env python3
import argparse, hashlib, json, sqlite3
from pathlib import Path

def tables(conn):
    return {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}

def cols(conn, table):
    return {r[1] for r in conn.execute(f"pragma table_info({table})")}

def rows_by_id(conn, table):
    if table not in tables(conn):
        return {}
    cs = cols(conn, table)
    if "id" not in cs:
        return {}
    return {r["id"]: dict(r) for r in conn.execute(f"select * from {table}")}

def pick(row, *names):
    if not row:
        return None
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--out", required=True)
    ap.add_argument("--only-333", action="store_true")
    args = ap.parse_args()

    db_path = Path(args.db)
    raw_sha256 = hashlib.sha256(db_path.read_bytes()).hexdigest()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ts = tables(conn)
    if "solves" not in ts:
        raise SystemExit("CUBESOLVES_SCHEMA_NO_SOLVES")

    averages = rows_by_id(conn, "averages")
    solvers = rows_by_id(conn, "solvers")
    competitions = rows_by_id(conn, "competitions")
    puzzles = rows_by_id(conn, "puzzles")
    reconstructors = rows_by_id(conn, "reconstructors")

    step_map = {}
    if "steps" in ts:
        sc = cols(conn, "steps")
        needed = {"solve_id","position_in_solve","moves","explanation"}
        if needed.issubset(sc):
            for row in conn.execute("select * from steps order by solve_id, position_in_solve, id"):
                step_map.setdefault(row["solve_id"], []).append({
                    "moves": row["moves"] or "",
                    "explanation": row["explanation"] or "",
                    "position_in_solve": row["position_in_solve"],
                })

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0

    with out_path.open("w", encoding="utf-8") as out:
        for solve in conn.execute("select * from solves order by id"):
            s = dict(solve)
            avg = averages.get(s.get("average_id"), {})

            solver_id = pick(s, "solver_id") or pick(avg, "solver_id")
            competition_id = pick(s, "competition_id") or pick(avg, "competition_id")
            puzzle_id = pick(s, "puzzle_id") or pick(avg, "puzzle_id")

            solver = solvers.get(solver_id, {})
            competition = competitions.get(competition_id, {})
            puzzle = puzzles.get(puzzle_id, {})

            puzzle_name = pick(puzzle, "name") or pick(s, "puzzle") or ""
            if args.only_333:
                p = str(puzzle_name).lower().replace("×", "x").replace(" ", "")
                if p not in {"3x3x3","3x3","333","rubik'scube","rubikscube"}:
                    continue

            reconstructor = None
            rid = pick(s, "reconstructor_id")
            if rid is not None:
                reconstructor = pick(reconstructors.get(rid, {}), "name")
            reconstructor = reconstructor or pick(s, "reconstructor")

            solution = pick(s, "solution") or ""
            steps = step_map.get(s["id"], [])
            if not solution and steps:
                solution = "\n".join(
                    f"{x['moves']} // {x['explanation']}".rstrip()
                    for x in steps
                )

            time_value = pick(s, "time")
            time_ms = None
            if isinstance(time_value, (int, float)) and time_value >= 0:
                time_ms = round(float(time_value) * 1000)

            record = {
                "source_record_id": str(s["id"]),
                "average_id": s.get("average_id"),
                "solver_display_name": pick(solver, "name") or pick(s, "solver"),
                "wca_id": pick(solver, "wca_id"),
                "competition": pick(competition, "name") or pick(s, "competition"),
                "puzzle": puzzle_name or None,
                "time_ms": time_ms,
                "penalty": pick(s, "penalty"),
                "scramble_raw": pick(s, "scramble") or "",
                "reconstruction_raw": solution,
                "steps": steps,
                "video_url": pick(s, "youtube"),
                "source_text": pick(s, "source"),
                "source_content": pick(s, "source_content"),
                "source_url": pick(avg, "source_url"),
                "reconstructor": reconstructor,
                "date_added": str(pick(s, "date_added") or "") or None,
                "raw_database_sha256": raw_sha256,
                "raw_database_name": db_path.name,
            }
            out.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            written += 1

    print("G7_P2_CUBESOLVES_EXTRACT_PASS")
    print(f"RAW_DATABASE_SHA256\t{raw_sha256}")
    print(f"RECORDS_WRITTEN\t{written}")

if __name__ == "__main__":
    main()
