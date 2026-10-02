#!/usr/bin/env python3
import argparse, json, pathlib, re, unicodedata, difflib
from collections import defaultdict, Counter
import duckdb

def norm_text(x):
    s=unicodedata.normalize("NFKC",str(x or "")).replace("’","'").replace("′","'")
    return " ".join(s.casefold().split())

def lex_norm(x):
    s=unicodedata.normalize("NFKC",str(x or "")).casefold()
    s=re.sub(r"[^0-9a-z]+"," ",s)
    return " ".join(s.split())

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

def explicit_year(label):
    m=re.search(r"\b(20\d{2}|19\d{2})\b",str(label or ""))
    return int(m.group(1)) if m else None

def token_jaccard(a,b):
    A=set(a.split()); B=set(b.split())
    if not A or not B: return 0.0
    return len(A&B)/len(A|B)

def sim(a,b):
    return max(difflib.SequenceMatcher(None,a,b).ratio(), token_jaccard(a,b))

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
        year_expr="NULL"

    comps=[]
    cur=con.execute(f"SELECT CAST(id AS VARCHAR),name,{year_expr} AS year FROM comp")
    for cid,name,year in cur.fetchall():
        comps.append({"id":cid,"name":name,"year":int(year) if year is not None else None,"lex":lex_norm(name),"norm":norm_text(name)})
    exact_names={c["norm"] for c in comps}

    target=[r for r in rows if norm_text(r["competition"]) and norm_text(r["competition"]) not in exact_names]
    grouped=defaultdict(list)
    for r in target: grouped[r["competition"]].append(r)

    candidate_rows=[]
    for label,xs in grouped.items():
        ln=lex_norm(label); y=explicit_year(label)
        pool=[c for c in comps if y is None or c["year"]==y]
        scored=sorted(((sim(ln,c["lex"]),c) for c in pool),key=lambda z:(-z[0],z[1]["id"]))[:5]
        for score,c in scored:
            candidate_rows.append((label,c["id"],c["name"],float(score)))

    con.execute("CREATE TABLE q(label VARCHAR,source_id BIGINT,solver_norm VARCHAR,result_cs BIGINT)")
    qrows=[]
    for label,xs in grouped.items():
        for r in xs:
            qrows.append((label,r["source_id"],norm_text(r["solver"]),r["result_cs"]))
    con.executemany("INSERT INTO q VALUES (?,?,?,?)",qrows)

    con.execute("CREATE TABLE cand(label VARCHAR,competition_id VARCHAR,competition_name VARCHAR,lexical_score DOUBLE)")
    con.executemany("INSERT INTO cand VALUES (?,?,?,?)",candidate_rows)
    name_sql="lower(trim(regexp_replace(r.person_name,'\\s+',' ','g')))"
    sql=f"""
    WITH base AS (
      SELECT c.label,c.competition_id,c.competition_name,c.lexical_score,
             q.source_id,q.solver_norm,q.result_cs
      FROM cand c JOIN q USING(label)
    ),
    supported AS (
      SELECT b.label,b.competition_id,b.competition_name,b.lexical_score,b.source_id,
             max(CASE WHEN a.value IS NOT NULL THEN 1 ELSE 0 END) support
      FROM base b
      LEFT JOIN res r ON CAST(r.competition_id AS VARCHAR)=b.competition_id
                     AND r.event_id='333'
                     AND {name_sql}=b.solver_norm
      LEFT JOIN att a ON a.result_id=r.id AND b.result_cs IS NOT NULL AND CAST(a.value AS BIGINT)=b.result_cs
      GROUP BY b.label,b.competition_id,b.competition_name,b.lexical_score,b.source_id
    )
    SELECT label,competition_id,competition_name,lexical_score,
           count(*) n_rows,
           sum(support) support_rows
    FROM supported
    GROUP BY label,competition_id,competition_name,lexical_score
    ORDER BY label,support_rows DESC,lexical_score DESC,competition_id
    """
    cur=con.execute(sql); cols=[d[0] for d in cur.description]
    evidence=defaultdict(list)
    for row in cur.fetchall():
        x=dict(zip(cols,row)); x["n_rows"]=int(x["n_rows"]); x["support_rows"]=int(x["support_rows"])
        x["support_fraction"]=x["support_rows"]/x["n_rows"] if x["n_rows"] else None
        evidence[x["label"]].append(x)

    label_results=[]; counts=Counter(); recovered_rows=0
    for label,xs in sorted(grouped.items()):
        ev=evidence[label]
        ev=sorted(ev,key=lambda z:(-z["support_rows"],-z["lexical_score"],z["competition_id"]))
        best=ev[0] if ev else None
        second=ev[1] if len(ev)>1 else None
        parseable=sum(1 for x in xs if x["result_cs"] is not None and norm_text(x["solver"]))
        strong=False
        if best and parseable:
            frac=best["support_rows"]/parseable
            competing=second["support_rows"] if second else 0
            strong=(best["support_rows"]>=3 and frac>=0.80 and competing < best["support_rows"]*0.50)
        if strong:
            cls="WCA_COMPETITION_ALIAS_STRONG_CONTEXT_RECOVERED"; recovered_rows+=len(xs)
        elif best and best["support_rows"]>0:
            cls="WCA_COMPETITION_ALIAS_CANDIDATE"
        else:
            cls="NO_WCA_ALIAS_CONTEXT_SUPPORT"
        counts[cls]+=len(xs)
        label_results.append({
            "source_label":label,
            "rows":len(xs),
            "parseable_solver_result_rows":parseable,
            "reconciliation_class":cls,
            "best_candidate":best,
            "top_candidates":ev[:5],
        })

    report={
      "schema_version":"g7-p7-competition-label-reconciliation-audit-1",
      "operation_type":"Competition-Label Reconciliation Audit",
      "authority":"POST_POPULATION_CENSUS_PROVENANCE_RECONCILIATION",
      "target_rows":len(target),
      "unique_labels":len(grouped),
      "row_class_counts":dict(sorted(counts.items())),
      "strong_recovered_rows":recovered_rows,
      "labels":label_results,
      "boundary":[
        "Lexical similarity is candidate discovery only.",
        "Strong recovery requires exact normalized person-name plus exact official result support in one WCA competition.",
        "Competition alias recovery is not exact attempt or scramble linkage.",
        "Unresolved labels remain unresolved.",
        "No new reco.nz body contact occurs."
      ]
    }
    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"competition-label-reconciliation-audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P7_COMPETITION_LABEL_RECONCILIATION_AUDIT_PASS")
    print("TARGET_ROWS\t"+str(report["target_rows"]))
    print("UNIQUE_LABELS\t"+str(report["unique_labels"]))
    print("ROW_CLASS_COUNTS\t"+json.dumps(report["row_class_counts"],sort_keys=True))
    for x in label_results[:50]:
        b=x["best_candidate"]
        print("LABEL\t"+x["source_label"]+"\tN="+str(x["rows"])+"\t"+x["reconciliation_class"]+"\tBEST="+(b["competition_name"] if b else "NONE")+"\tSUPPORT="+str(b["support_rows"] if b else 0))

if __name__=="__main__":
    main()
