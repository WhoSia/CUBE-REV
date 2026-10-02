#!/usr/bin/env python3
import argparse, json, pathlib, duckdb, hashlib

ap=argparse.ArgumentParser()
ap.add_argument("--extract-dir",required=True)
ap.add_argument("--out-dir",required=True)
ap.add_argument("--source-sha256",required=True)
ap.add_argument("--api-json",required=True)
args=ap.parse_args()
root=pathlib.Path(args.extract_dir); out=pathlib.Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
api=json.load(open(args.api_json,encoding="utf-8"))

def first(stem):
    xs=sorted(root.rglob(f"*{stem}*.tsv"))
    exact=[p for p in xs if p.name.endswith(f"{stem}.tsv")]
    if not xs: raise FileNotFoundError(stem)
    return exact[0] if exact else xs[0]
def qp(p): return str(p.resolve()).replace("'","''")

res=first("results"); att=first("result_attempts"); comp=first("competitions"); scr=first("scrambles")
con=duckdb.connect()
con.execute("PRAGMA threads=4")
con.execute("PRAGMA preserve_insertion_order=false")
for name,p in [("results",res),("attempts",att),("competitions",comp),("scrambles",scr)]:
    con.execute(f"""CREATE VIEW {name} AS SELECT * FROM read_csv_auto('{qp(p)}',delim='\t',header=true,sample_size=200000,ignore_errors=false)""")
rc=[x[0] for x in con.execute("describe results").fetchall()]
cc=[x[0] for x in con.execute("describe competitions").fetchall()]
sc=[x[0] for x in con.execute("describe scrambles").fetchall()]
date_expr="CAST(c.start_date AS DATE)" if "start_date" in cc else "make_date(CAST(c.year AS INTEGER),CAST(c.month AS INTEGER),CAST(c.day AS INTEGER))"

con.execute(f"""
CREATE VIEW a333 AS
SELECT r.id result_id,r.competition_id,{date_expr} competition_date,
       CAST(r.person_id AS VARCHAR) person_id,
       a.attempt_number,CAST(a.value AS BIGINT) value,
       CASE WHEN a.value>0 THEN 'VALID' WHEN a.value=-1 THEN 'DNF'
            WHEN a.value=-2 THEN 'DNS' WHEN a.value=0 THEN 'NO_RESULT'
            ELSE 'UNEXPECTED_VALUE' END status
FROM attempts a JOIN results r ON a.result_id=r.id
LEFT JOIN competitions c ON r.competition_id=c.id
WHERE r.event_id='333'
""")
status=dict(con.execute("select status,count(*) from a333 group by status order by status").fetchall())
attempt_rows=con.execute("select count(*) from a333").fetchone()[0]
persons=con.execute("select count(distinct person_id) from a333").fetchone()[0]
competitions=con.execute("select count(distinct competition_id) from a333").fetchone()[0]
dmin,dmax=con.execute("select min(competition_date),max(competition_date) from a333").fetchone()
results_333=con.execute("select count(*) from results where event_id='333'").fetchone()[0]

# Sequential adjacency coverage for future order-dependent analyses.
pairs=con.execute("""
select count(*) from (
 select result_id,attempt_number,
        lag(status) over(partition by result_id order by attempt_number) prev
 from a333
) where prev is not null
""").fetchone()[0]

# Scramble schema is source-version dependent; count 333 rows if event_id is available.
scramble_rows=con.execute("select count(*) from scrambles").fetchone()[0]
scramble_333=None
if "event_id" in sc:
    scramble_333=con.execute("select count(*) from scrambles where event_id='333'").fetchone()[0]

unexpected=status.get("UNEXPECTED_VALUE",0)
report={
 "schema_version":"g7-p6-wca-latest-census-1",
 "source":{
   "api_export_date":api.get("export_date"),
   "api_export_version":api.get("export_version") or api.get("export_format_version"),
   "tsv_url":api.get("tsv_url"),
   "archive_sha256":args.source_sha256,
   "files":{"results":res.name,"attempts":att.name,"competitions":comp.name,"scrambles":scr.name}
 },
 "wca_333":{
   "attempt_rows":attempt_rows,"result_rows":results_333,
   "persons":persons,"competitions":competitions,
   "date_min":str(dmin),"date_max":str(dmax),
   "status_counts":status,"within_result_adjacent_pairs":pairs
 },
 "scrambles":{"all_rows":scramble_rows,"event_333_rows":scramble_333},
 "verdict":"PASS_SOURCE_SEMANTICS" if unexpected==0 else "HOLD_UNEXPECTED_ATTEMPT_VALUES",
 "boundary":[
   "official attempt/scramble authority only",
   "not move-level reconstruction data",
   "not population-representative outside WCA competitors"
 ]
}
(out/"wca-latest-census.json").write_text(json.dumps(report,indent=2,default=str)+"\n",encoding="utf-8")
print("G7_P6_WCA_LATEST_CENSUS_PASS")
print("EXPORT_DATE\t"+str(report["source"]["api_export_date"]))
print("ATTEMPT_ROWS\t"+str(attempt_rows))
print("PERSONS\t"+str(persons))
print("COMPETITIONS\t"+str(competitions))
print("STATUS_COUNTS\t"+json.dumps(status,sort_keys=True))
print("SCRAMBLES_333\t"+str(scramble_333))
