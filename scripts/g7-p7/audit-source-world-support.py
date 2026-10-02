#!/usr/bin/env python3
import argparse, json, pathlib, re, unicodedata
from collections import Counter
import duckdb

def norm_text(x):
    s=unicodedata.normalize("NFKC",str(x or "")).replace("’","'").replace("′","'")
    return " ".join(s.casefold().split())

def parse_result_cs(x):
    s=str(x or "").strip().upper()
    if not s: return None
    if "DNF" in s: return -1
    if "DNS" in s: return -2
    s=s.replace(",","").replace(" ","")
    m=re.search(r"(?:(\d+):)?(\d{1,2})(?:\.(\d{1,2}))?",s)
    if not m: return None
    minutes=int(m.group(1) or 0); sec=int(m.group(2)); frac=(m.group(3) or "0")
    cs=int((frac+"00")[:2])
    return (minutes*60+sec)*100+cs

def first(root,stem):
    xs=sorted(pathlib.Path(root).rglob(f"*{stem}*.tsv"))
    exact=[p for p in xs if p.name.endswith(f"{stem}.tsv")]
    if not xs: raise FileNotFoundError(stem)
    return exact[0] if exact else xs[0]

def qp(p):
    return str(pathlib.Path(p).resolve()).replace("'","''")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--reco",required=True)
    ap.add_argument("--linkage",required=True)
    ap.add_argument("--failure-diagnostic",required=True)
    ap.add_argument("--wca-dir",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    linkage=json.load(open(args.linkage,encoding="utf-8"))
    failure=json.load(open(args.failure_diagnostic,encoding="utf-8"))
    link_by={int(x["source_id"]):x for x in linkage["rows"]}
    fail_by={int(x["source_id"]):x for x in failure["rows"]}

    reco={}
    for line in open(args.reco,encoding="utf-8"):
        if not line.strip(): continue
        x=json.loads(line); p=x.get("parsed",{})
        sid=int(x["source_id"])
        reco[sid]={
            "source_id":sid,
            "solver":p.get("solver"),
            "solver_norm":norm_text(p.get("solver")),
            "competition":p.get("competition"),
            "competition_norm":norm_text(p.get("competition")),
            "result_text":p.get("result_text"),
            "result_cs":parse_result_cs(p.get("result_text")),
            "cohort":x.get("analysis_meta",{}).get("cohort"),
        }

    root=pathlib.Path(args.wca_dir)
    res=first(root,"results"); att=first(root,"result_attempts"); comp=first(root,"competitions")
    con=duckdb.connect(); con.execute("PRAGMA threads=4")
    con.execute(f"CREATE VIEW res AS SELECT * FROM read_csv_auto('{qp(res)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW att AS SELECT * FROM read_csv_auto('{qp(att)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW comp AS SELECT * FROM read_csv_auto('{qp(comp)}',delim='\\t',header=true,sample_size=200000)")
    rc=[x[0] for x in con.execute("DESCRIBE res").fetchall()]
    cc=[x[0] for x in con.execute("DESCRIBE comp").fetchall()]
    if not {"id","competition_id","event_id","person_id","person_name"}.issubset(rc):
        raise SystemExit("WCA_RESULTS_SCHEMA_MISMATCH")
    if not {"id","name"}.issubset(cc):
        raise SystemExit("WCA_COMPETITIONS_SCHEMA_MISMATCH")

    con.execute("CREATE TABLE q(source_id BIGINT,competition_norm VARCHAR,solver_norm VARCHAR,result_cs BIGINT)")
    con.executemany("INSERT INTO q VALUES (?,?,?,?)",[
        (sid,x["competition_norm"],x["solver_norm"],x["result_cs"]) for sid,x in reco.items()
    ])

    norm_comp_sql="lower(trim(regexp_replace(c.name,'\\s+',' ','g')))"
    norm_name_sql="lower(trim(regexp_replace(r.person_name,'\\s+',' ','g')))"
    sql=f"""
    WITH cm AS (
      SELECT q.source_id,c.id competition_id
      FROM q JOIN comp c ON q.competition_norm<>'' AND {norm_comp_sql}=q.competition_norm
    ),
    sm AS (
      SELECT cm.source_id,r.id result_id,r.person_id
      FROM cm JOIN q USING(source_id)
      JOIN res r ON r.competition_id=cm.competition_id AND r.event_id='333'
      WHERE {norm_name_sql}=q.solver_norm
    ),
    rm AS (
      SELECT sm.source_id,count(*) result_match_rows
      FROM sm JOIN q USING(source_id)
      JOIN att a ON a.result_id=sm.result_id
      WHERE q.result_cs IS NOT NULL AND CAST(a.value AS BIGINT)=q.result_cs
      GROUP BY sm.source_id
    ),
    ca AS (
      SELECT source_id,count(DISTINCT competition_id) competition_matches FROM cm GROUP BY source_id
    ),
    sa AS (
      SELECT source_id,count(*) solver_result_rows,count(DISTINCT person_id) solver_people FROM sm GROUP BY source_id
    )
    SELECT q.source_id,
           coalesce(ca.competition_matches,0) competition_matches,
           coalesce(sa.solver_result_rows,0) solver_result_rows,
           coalesce(sa.solver_people,0) solver_people,
           coalesce(rm.result_match_rows,0) result_match_rows
    FROM q
    LEFT JOIN ca USING(source_id)
    LEFT JOIN sa USING(source_id)
    LEFT JOIN rm USING(source_id)
    ORDER BY q.source_id
    """
    cur=con.execute(sql); cols=[d[0] for d in cur.description]
    support={int(r[0]):dict(zip(cols,r)) for r in cur.fetchall()}

    counts=Counter(); rows=[]
    for sid in sorted(reco):
        r=reco[sid]; lk=link_by[sid]; fd=fail_by[sid]; s=support[sid]
        if lk["linkage_class"]=="A_EXACT_EXTERNAL":
            world="WCA_EXACT_ATTEMPT_LINKED"
        elif fd["failure_stage"]=="SCRAMBLE_PRESENT_SOLVER_ABSENT_IN_ROUND":
            world="WCA_SCRAMBLE_PRESENT_SOLVER_ABSENT_IN_MATCHED_ROUND"
        elif fd["failure_stage"]!="NO_EXACT_SCRAMBLE_IN_WCA":
            world="OTHER_EXISTING_LINKAGE_STATE"
        elif not r["competition_norm"]:
            world="NO_SOURCE_COMPETITION_CONTEXT"
        elif s["result_match_rows"]>0:
            world="WCA_ATTEMPT_CONTEXT_SUPPORTED_SCRAMBLE_UNSUPPORTED"
        elif s["solver_result_rows"]>0:
            world="WCA_SOLVER_CONTEXT_SUPPORTED_SCRAMBLE_UNSUPPORTED"
        elif s["competition_matches"]>0:
            world="WCA_COMPETITION_CONTEXT_ONLY_SCRAMBLE_UNSUPPORTED"
        else:
            world="NO_EXACT_WCA_COMPETITION_CONTEXT_MATCH"
        counts[world]+=1
        rows.append({
            "source_id":sid,
            "cohort":r["cohort"],
            "failure_stage":fd["failure_stage"],
            "linkage_class":lk["linkage_class"],
            "source_world_support":world,
            "competition_source":r["competition"],
            "solver":r["solver"],
            "result_text":r["result_text"],
            "competition_matches":int(s["competition_matches"]),
            "solver_result_rows":int(s["solver_result_rows"]),
            "solver_people":int(s["solver_people"]),
            "result_match_rows":int(s["result_match_rows"]),
        })

    report={
      "schema_version":"g7-p7-source-world-support-audit-1",
      "operation_type":"Source-World Support Audit",
      "authority":"POST_LINKAGE_FAILURE_DIAGNOSTIC_EXPLORATORY",
      "counts":dict(sorted(counts.items())),
      "rows":rows,
      "interpretation_boundary":[
        "WCA context support without exact scramble is not an exact attempt linkage.",
        "NO_EXACT_WCA_COMPETITION_CONTEXT_MATCH does not prove a practice or non-WCA solve.",
        "No fuzzy solver or competition matching is used.",
        "No new reco.nz source contact occurs.",
        "This audit localizes provenance support and cannot promote a cognitive mechanism."
      ]
    }
    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"source-world-support-audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P7_SOURCE_WORLD_SUPPORT_AUDIT_PASS")
    print(json.dumps(report["counts"],sort_keys=True))

if __name__=="__main__":
    main()
