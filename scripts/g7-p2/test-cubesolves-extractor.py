#!/usr/bin/env python3
import json, sqlite3, subprocess, sys, tempfile
from pathlib import Path
import unittest

class ExtractorTest(unittest.TestCase):
    def test_finalish_schema(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            db = td / "db.sqlite"
            out = td / "out.jsonl"
            con = sqlite3.connect(db)
            con.executescript("""
            create table solvers(id integer primary key, name text, wca_id text);
            create table competitions(id integer primary key, name text);
            create table puzzles(id integer primary key, name text);
            create table reconstructors(id integer primary key, name text);
            create table averages(id integer primary key, solver_id int, puzzle_id int, competition_id int, source_url text);
            create table solves(
              id integer primary key, average_id int, scramble text, solution text,
              time real, penalty text, youtube text, source text, source_content text,
              date_added text, reconstructor_id int
            );
            create table steps(id integer primary key, moves text, explanation text, solve_id int, position_in_solve int);
            insert into solvers values(1,'Synthetic Solver','2000TEST01');
            insert into competitions values(1,'Synthetic Open');
            insert into puzzles values(1,'3x3x3');
            insert into reconstructors values(1,'Synthetic Reconstructor');
            insert into averages values(1,1,1,1,'https://example.invalid/source');
            insert into solves values(1,1,'R U','',5.43,'','https://example.invalid/video','src','content','2014-02-25',1);
            insert into steps values(1,'R U R''','cross',1,0);
            insert into steps values(2,'U2','1st pair',1,1);
            """)
            con.commit(); con.close()

            cmd=[sys.executable,"scripts/g7-p2/extract-cubesolves.py",str(db),"--out",str(out),"--only-333"]
            proc=subprocess.run(cmd,capture_output=True,text=True,check=True)
            self.assertIn("G7_P2_CUBESOLVES_EXTRACT_PASS",proc.stdout)
            rows=[json.loads(x) for x in out.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows),1)
            r=rows[0]
            self.assertEqual(r["solver_display_name"],"Synthetic Solver")
            self.assertEqual(r["wca_id"],"2000TEST01")
            self.assertEqual(r["puzzle"],"3x3x3")
            self.assertEqual(r["time_ms"],5430)
            self.assertEqual(len(r["steps"]),2)
            self.assertIn("// cross",r["reconstruction_raw"])

if __name__=="__main__":
    unittest.main()
