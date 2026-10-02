#!/usr/bin/env python3
import argparse, json, pathlib, re, unicodedata, duckdb
from collections import Counter

def norm_text(x):
    s=unicodedata.normalize("NFKC",str(x or "")).replace("’","'").replace("′","'")
    return " ".join(s.casefold().split())

def norm_scramble(x):
    s=unicodedata.normalize("NFKC",str(x or "")).replace("’","'").replace("′","'")
    return re.sub(r"\s+"," ",s.strip())

def first(root,stem):
    xs=sorted(pathlib.Path(root).rglob(f"*{stem}*.tsv"))
    exact=[p for p in xs if p.name.endswith(f"{stem}.tsv")]
    if not xs: raise FileNotFoundError(stem)
    return exact[0] if exact else xs[0]

def qp(p): return str(pathlib.Path(p).resolve()).replace("'","''")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--reco",required=True)
    ap.add_argument("--linkage",required=True)
    ap.add_argument("--wca-dir",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    linkage=json.load(open(args.linkage,encoding="utf-8"))
    link_by={int(x["source_id"]):x for x in linkage["rows"]}

    reco={}
    for line in open(args.reco,encoding="utf-8"):
        if not line.strip(): continue
        x=json.loads(line); p=x.get("parsed",{})
        sid=int(x["source_id"])
        reco[sid]={
            "source_id":sid,
            "scramble_norm":norm_scramble(p.get("scramble_raw")),
            "solver_norm":norm_text(p.get("solver")),
            "competition_norm":norm_text(p.get("competition")),
            "result_text":p.get("result_text"),
            "cohort":x.get("analysis_meta",{}).get("cohort")
        }

    root=pathlib.Path(args.wca_dir)
    scr=first(root,"scrambles"); res=first(root,"results"); comp=first(root,"competitions")
    con=duckdb.connect(); con.execute("PRAGMA threads=4")
    con.execute(f"CREATE VIEW scr AS SELECT * FROM read_csv_auto('{qp(scr)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW res AS SELECT * FROM read_csv_auto('{qp(res)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW comp AS SELECT * FROM read_csv_auto('{qp(comp)}',delim='\\t',header=true,sample_size=200000)")
    sc=[x[0] for x in con.execute("DESCRIBE scr").fetchall()]
    rc=[x[0] for x in con.execute("DESCRIBE res").fetchall()]
    round_key = "CAST(s.round_id AS VARCHAR)" if "round_id" in sc else "CAST(s.round_type_id AS VARCHAR)"
    round_join = "CAST(r.round_id AS VARCHAR)=m.round_key" if "round_id" in rc else "CAST(r.round_type_id AS VARCHAR)=m.round_key"
    norm_scr_sql="trim(regexp_replace(replace(replace(s.scramble,'’',''''),'′',''''),'\\s+',' ','g'))"
    norm_name_sql="lower(trim(regexp_replace(r.person_name,'\\s+',' ','g')))"

    con.execute("CREATE TABLE q(source_id BIGINT,scramble_norm VARCHAR,solver_norm VARCHAR)")
    con.executemany("INSERT INTO q VALUES (?,?,?)",[(sid,x["scramble_norm"],x["solver_norm"]) for sid,x in reco.items()])

    sql=f"""
    WITH m AS (
      SELECT q.source_id,s.competition_id,s.event_id,{round_key} round_key,
             CAST(s.group_id AS VARCHAR) group_id,CAST(s.scramble_num AS INTEGER) scramble_num
      FROM q JOIN scr s ON s.event_id='333' AND {norm_scr_sql}=q.scramble_norm
    ),
    a AS (
      SELECT source_id,count(*) scramble_rows,count(DISTINCT competition_id||'|'||round_key) scramble_rounds
      FROM m GROUP BY source_id
    ),
    b AS (
      SELECT m.source_id,count(*) solver_rows,count(DISTINCT r.person_id) solver_people
      FROM m JOIN q ON q.source_id=m.source_id
             JOIN res r ON r.competition_id=m.competition_id AND r.event_id='333' AND {round_join}
      WHERE {norm_name_sql}=q.solver_norm
      GROUP BY m.source_id
    )
    SELECT q.source_id,coalesce(a.scramble_rows,0) scramble_rows,
           coalesce(a.scramble_rounds,0) scramble_rounds,
           coalesce(b.solver_rows,0) solver_rows,
           coalesce(b.solver_people,0) solver_people
    FROM q LEFT JOIN a USING(source_id) LEFT JOIN b USING(source_id)
    ORDER BY q.source_id
    """
    rows=[dict(zip([d[0] for d in con.execute(sql).description],r)) for r in con.execute(sql).fetchall()]

    out=[]; counts=Counter()
    for x in rows:
        sid=int(x["source_id"]); lk=link_by[sid]
        if lk["linkage_class"]!="U_UNLINKED":
            stage="ALREADY_LINKED"
        elif x["scramble_rows"]==0:
            stage="NO_EXACT_SCRAMBLE_IN_WCA"
        elif x["solver_rows"]==0:
            stage="SCRAMBLE_PRESENT_SOLVER_ABSENT_IN_ROUND"
        else:
            stage="SOLVER_AND_SCRAMBLE_PRESENT_CONTEXT_REJECTED"
        counts[stage]+=1
        out.append({
          "source_id":sid,"cohort":reco[sid]["cohort"],"linkage_class":lk["linkage_class"],
          "failure_stage":stage,"scramble_rows":int(x["scramble_rows"]),
          "scramble_rounds":int(x["scramble_rounds"]),"solver_rows":int(x["solver_rows"]),
          "solver_people":int(x["solver_people"])
        })

    report={
      "schema_version":"g7-p7-linkage-failure-diagnostic-1",
      "authority":"POST_LINKAGE_EXPLORATORY_DIAGNOSTIC",
      "counts":dict(sorted(counts.items())),
      "rows":out,
      "boundary":[
        "Does not change linkage classes.",
        "Does not introduce fuzzy name matching.",
        "Does not use source_display_date as official solve-date evidence.",
        "Used only to locate the next provenance-preserving linkage bottleneck."
      ]
    }
    p=pathlib.Path(args.out); p.mkdir(parents=True,exist_ok=True)
    (p/"linkage-failure-diagnostic.json").write_text(json.dumps(report,indent=2)+"\n")
    print("G7_P7_LINKAGE_FAILURE_DIAGNOSTIC_PASS")
    print(json.dumps(report["counts"],sort_keys=True))

if __name__=="__main__": main()
