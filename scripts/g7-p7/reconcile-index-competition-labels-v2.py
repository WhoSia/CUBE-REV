#!/usr/bin/env python3
import argparse, json, pathlib, re, unicodedata
from collections import defaultdict, Counter
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

def explicit_year(x):
    m=re.search(r"\b(19\d{2}|20\d{2})\b",str(x or ""))
    return int(m.group(1)) if m else None

def first(root,stem):
    xs=sorted(pathlib.Path(root).rglob(f"*{stem}*.tsv"))
    exact=[p for p in xs if p.name.endswith(f"{stem}.tsv")]
    if not xs: raise FileNotFoundError(stem)
    return exact[0] if exact else xs[0]

def qp(p):
    return str(pathlib.Path(p).resolve()).replace("'","''")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--index",required=True)
    ap.add_argument("--wca-dir",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    rows=[]
    for line in open(args.index,encoding="utf-8"):
        if not line.strip(): continue
        x=json.loads(line)
        if x.get("puzzle")!="3x3": continue
        rows.append({
            "source_id":int(x["source_id"]),
            "competition":x.get("competition"),
            "solver":x.get("solver"),
            "result":x.get("result"),
            "result_cs":parse_result_cs(x.get("result")),
        })

    root=pathlib.Path(args.wca_dir)
    comp=first(root,"competitions"); res=first(root,"results"); att=first(root,"result_attempts")
    con=duckdb.connect(); con.execute("PRAGMA threads=4")
    con.execute(f"CREATE VIEW comp AS SELECT * FROM read_csv_auto('{qp(comp)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW res AS SELECT * FROM read_csv_auto('{qp(res)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW att AS SELECT * FROM read_csv_auto('{qp(att)}',delim='\\t',header=true,sample_size=200000)")
    cc=[x[0] for x in con.execute("DESCRIBE comp").fetchall()]
    rc=[x[0] for x in con.execute("DESCRIBE res").fetchall()]
    if not {"id","name"}.issubset(cc): raise SystemExit("WCA_COMP_SCHEMA_MISMATCH")
    if not {"id","competition_id","event_id","person_name"}.issubset(rc): raise SystemExit("WCA_RESULTS_SCHEMA_MISMATCH")
    if "start_date" in cc:
        year_expr="CAST(EXTRACT(year FROM CAST(start_date AS DATE)) AS INTEGER)"
    elif "year" in cc:
        year_expr="CAST(year AS INTEGER)"
    else:
        raise SystemExit("WCA_COMPETITION_YEAR_UNAVAILABLE")

    exact_names={norm_text(x[0]) for x in con.execute("SELECT name FROM comp").fetchall()}
    platform={"speedcubedb","speed cube database","cubesolv.es","cubesolves","cubedb"}
    def target(r):
        n=norm_text(r["competition"])
        if not n or n=="unofficial" or "monkey league" in n or n in platform or n in exact_names:
            return False
        return True
    target_rows=[r for r in rows if target(r)]
    if len(target_rows)!=232:
        raise SystemExit(f"TARGET_232_MISMATCH_{len(target_rows)}")

    con.execute("CREATE TABLE q(label VARCHAR,source_id BIGINT,label_year INTEGER,solver_norm VARCHAR,result_cs BIGINT)")
    con.executemany("INSERT INTO q VALUES (?,?,?,?,?)",[
        (r["competition"],r["source_id"],explicit_year(r["competition"]),norm_text(r["solver"]),r["result_cs"])
        for r in target_rows
    ])
    norm_name_sql="lower(trim(regexp_replace(r.person_name,'\\\\s+',' ','g')))"
    sql=f"""
    WITH hits AS (
      SELECT q.label,q.source_id,
             CAST(c.id AS VARCHAR) competition_id,c.name competition_name
      FROM q
      JOIN res r
        ON r.event_id='333'
       AND {norm_name_sql}=q.solver_norm
      JOIN att a
        ON a.result_id=r.id
       AND q.result_cs IS NOT NULL
       AND CAST(a.value AS BIGINT)=q.result_cs
      JOIN comp c
        ON CAST(c.id AS VARCHAR)=CAST(r.competition_id AS VARCHAR)
       AND q.label_year IS NOT NULL
       AND {year_expr}=q.label_year
    )
    SELECT label,competition_id,competition_name,
           count(DISTINCT source_id) candidate_rows,
           count(DISTINCT source_id) support_rows
    FROM hits
    GROUP BY label,competition_id,competition_name
    ORDER BY label,support_rows DESC,competition_id
    """
    cur=con.execute(sql); cols=[d[0] for d in cur.description]
    evidence=defaultdict(list)
    for row in cur.fetchall():
        x=dict(zip(cols,row))
        x["candidate_rows"]=int(x["candidate_rows"]); x["support_rows"]=int(x["support_rows"])
        evidence[x["label"]].append(x)

    by_label=defaultdict(list)
    for r in target_rows: by_label[r["competition"]].append(r)
    out_labels=[]; row_counts=Counter()
    for label,xs in sorted(by_label.items()):
        parseable=sum(1 for r in xs if explicit_year(label) is not None and r["result_cs"] is not None and norm_text(r["solver"]))
        ev=sorted(evidence[label],key=lambda z:(-z["support_rows"],z["competition_id"]))
        best=ev[0] if ev else None
        second=ev[1] if len(ev)>1 else None
        strong=False
        if best and parseable:
            frac=best["support_rows"]/parseable
            second_support=second["support_rows"] if second else 0
            strong=(best["support_rows"]>=3 and frac>=0.80 and second_support < best["support_rows"]*0.50)
        if explicit_year(label) is None:
            cls="NO_EXPLICIT_YEAR_NO_AUTO_RECOVERY"
        elif strong:
            cls="WCA_COMPETITION_ALIAS_STRONG_CONTEXT_RECOVERED_V2"
        elif best:
            cls="WCA_COMPETITION_ALIAS_EVIDENCE_CANDIDATE_V2"
        else:
            cls="NO_WCA_YEAR_WIDE_PERSON_RESULT_SUPPORT"
        row_counts[cls]+=len(xs)
        out_labels.append({
            "source_label":label,
            "rows":len(xs),
            "explicit_year":explicit_year(label),
            "parseable_solver_result_rows":parseable,
            "reconciliation_class":cls,
            "best_candidate":best,
            "supported_candidates":ev[:20]
        })

    report={
      "schema_version":"g7-p7-competition-label-reconciliation-audit-2",
      "operation_type":"Competition-Label Reconciliation Audit",
      "version":2,
      "authority":"POST_V1_DISCOVERY_REPAIR_AUDIT",
      "target_rows":len(target_rows),
      "unique_labels":len(by_label),
      "row_class_counts":dict(sorted(row_counts.items())),
      "labels":out_labels,
      "boundary":[
        "Candidate evidence search scans all WCA competitions in the explicit source-label year.",
        "Only exact normalized solver plus exact official 3x3 attempt result counts as row support.",
        "Lexical similarity is not used for candidate eligibility or promotion in v2.",
        "No-year labels are never automatically recovered.",
        "Competition alias recovery is not exact scramble or attempt linkage.",
        "No new reco.nz body contact occurs."
      ]
    }
    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"competition-label-reconciliation-audit-v2.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P7_COMPETITION_LABEL_RECONCILIATION_V2_PASS")
    print("TARGET_ROWS\t"+str(report["target_rows"]))
    print("UNIQUE_LABELS\t"+str(report["unique_labels"]))
    print("ROW_CLASS_COUNTS\t"+json.dumps(report["row_class_counts"],sort_keys=True))
    for x in out_labels:
        b=x["best_candidate"]
        print("LABEL\t"+x["source_label"]+"\tN="+str(x["rows"])+"\t"+x["reconciliation_class"]+"\tBEST="+(b["competition_name"] if b else "NONE")+"\tSUPPORT="+str(b["support_rows"] if b else 0))

if __name__=="__main__":
    main()
