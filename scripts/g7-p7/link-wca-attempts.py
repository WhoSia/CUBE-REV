#!/usr/bin/env python3
import argparse, csv, hashlib, json, pathlib, re, unicodedata
from collections import Counter, defaultdict
import duckdb

def norm_text(x):
    s=unicodedata.normalize("NFKC",str(x or "")).replace("’","'").replace("′","'")
    return " ".join(s.casefold().split())

def norm_scramble(x):
    s=unicodedata.normalize("NFKC",str(x or "")).replace("’","'").replace("′","'")
    s=re.sub(r"\s+"," ",s.strip())
    return s

def parse_date(x):
    s=str(x or "").strip()
    m=re.search(r"(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})",s)
    if not m: return None
    return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

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

def qp(p): return str(pathlib.Path(p).resolve()).replace("'","''")

def classify(rows, reco):
    if not rows:
        return "U_UNLINKED","NO_OFFICIAL_CANDIDATE"
    strict=[]
    compatible=[]
    for x in rows:
        result_ok = reco["result_cs"] is None or x["attempt_value"]==reco["result_cs"]
        date_ok = reco["solve_date"] is None or x["date_ok"] is True
        if result_ok and date_ok:
            compatible.append(x)
            if reco["result_cs"] is not None and reco["solve_date"] is not None:
                strict.append(x)
    use = strict if strict else compatible
    if not use:
        return "C_AMBIGUOUS","CONTEXT_CONFLICT"
    uniq={(x["competition_id"],x["round_key"],x["person_id"],x["attempt_number"],x["attempt_value"]) for x in use}
    if len(uniq)>1:
        return "C_AMBIGUOUS","MULTIPLE_OFFICIAL_CANDIDATES"
    x=use[0]
    complete=(reco["result_cs"] is not None and reco["solve_date"] is not None)
    if complete and x["round_group_count"]==1 and x["global_scramble_match_count"]==1:
        return "A_EXACT_EXTERNAL","UNIQUE_SINGLE_GROUP_FULL_CONTEXT"
    return "B_STRONG_EXTERNAL","UNIQUE_CANDIDATE_WITH_PUBLIC_GROUP_OR_FIELD_LIMIT"

def self_test():
    base={"result_cs":623,"solve_date":"2026-01-01"}
    row={"competition_id":"C","round_key":"R","person_id":"P","attempt_number":1,"attempt_value":623,
         "date_ok":True,"round_group_count":1,"global_scramble_match_count":1}
    assert classify([row],base)[0]=="A_EXACT_EXTERNAL"
    assert classify([{**row,"round_group_count":2}],base)[0]=="B_STRONG_EXTERNAL"
    assert classify([row,{**row,"person_id":"Q"}],base)[0]=="C_AMBIGUOUS"
    assert classify([],base)[0]=="U_UNLINKED"
    assert parse_result_cs("6.23")==623
    assert parse_result_cs("1:02.34")==6234
    assert parse_result_cs("DNF")==-1
    print("G7_P7_WCA_LINKAGE_SELF_TEST_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--reco")
    ap.add_argument("--wca-dir")
    ap.add_argument("--out")
    ap.add_argument("--wca-source-sha256")
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if args.self_test:
        self_test(); return
    if not all([args.reco,args.wca_dir,args.out,args.wca_source_sha256]):
        raise SystemExit("ARGS_REQUIRED")

    solves=[]
    with open(args.reco,encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            x=json.loads(line)
            p=x.get("parsed",{})
            solves.append({
                "source_id":int(x["source_id"]),
                "scramble_norm":norm_scramble(p.get("scramble_raw")),
                "scramble_sha256":hashlib.sha256(norm_scramble(p.get("scramble_raw")).encode()).hexdigest(),
                "solver":p.get("solver"),
                "solver_norm":norm_text(p.get("solver")),
                "result_text":p.get("result_text"),
                "result_cs":parse_result_cs(p.get("result_text")),
                "solve_date":parse_date(p.get("solve_date")),
                "competition":p.get("competition"),
                "competition_norm":norm_text(p.get("competition")),
                "cohort":x.get("analysis_meta",{}).get("cohort"),
            })
    if len(solves)!=60 or len({x["source_id"] for x in solves})!=60:
        raise SystemExit("RECO_60_AUTHORITY")

    root=pathlib.Path(args.wca_dir)
    scr=first(root,"scrambles"); res=first(root,"results"); att=first(root,"result_attempts"); comp=first(root,"competitions")
    con=duckdb.connect()
    con.execute("PRAGMA threads=4")
    con.execute("PRAGMA preserve_insertion_order=false")
    for name,p in [("scrambles",scr),("results",res),("attempts",att),("competitions",comp)]:
        con.execute(f"CREATE VIEW {name} AS SELECT * FROM read_csv_auto('{qp(p)}',delim='\\t',header=true,sample_size=200000,ignore_errors=false)")
    sc=[x[0] for x in con.execute("DESCRIBE scrambles").fetchall()]
    rc=[x[0] for x in con.execute("DESCRIBE results").fetchall()]
    cc=[x[0] for x in con.execute("DESCRIBE competitions").fetchall()]
    required_scr={"competition_id","event_id","group_id","scramble","scramble_num"}
    required_res={"id","competition_id","event_id","person_id","person_name"}
    if not required_scr.issubset(sc) or not required_res.issubset(rc):
        raise SystemExit("WCA_SCHEMA_MISMATCH")
    round_join = "sm.round_key=CAST(r.round_id AS VARCHAR)" if "round_id" in sc and "round_id" in rc else "sm.round_key=CAST(r.round_type_id AS VARCHAR)"
    round_key = "CAST(s.round_id AS VARCHAR)" if "round_id" in sc else "CAST(s.round_type_id AS VARCHAR)"
    start_expr = "CAST(c.start_date AS DATE)" if "start_date" in cc else "make_date(CAST(c.year AS INTEGER),CAST(c.month AS INTEGER),CAST(c.day AS INTEGER))"
    if "end_date" in cc:
        end_expr="CAST(c.end_date AS DATE)"
    elif all(x in cc for x in ["end_month","end_day","year"]):
        end_expr="make_date(CAST(c.year AS INTEGER),CAST(c.end_month AS INTEGER),CAST(c.end_day AS INTEGER))"
    else:
        end_expr=start_expr

    con.execute("CREATE TABLE reco(source_id BIGINT,scramble_norm VARCHAR,solver_norm VARCHAR,result_cs BIGINT,solve_date DATE)")
    vals=[(x["source_id"],x["scramble_norm"],x["solver_norm"],x["result_cs"],x["solve_date"]) for x in solves]
    con.executemany("INSERT INTO reco VALUES (?,?,?,?,?)",vals)

    norm_scr_sql="trim(regexp_replace(replace(replace(s.scramble,'’',''''),'′',''''),'\\s+',' ','g'))"
    norm_name_sql="lower(trim(regexp_replace(r.person_name,'\\s+',' ','g')))"
    query=f"""
    WITH sm AS (
      SELECT q.source_id,s.competition_id,s.event_id,{round_key} round_key,
             CAST(s.group_id AS VARCHAR) group_id,CAST(s.scramble_num AS INTEGER) scramble_num,
             count(*) OVER(PARTITION BY q.source_id) global_scramble_match_count,
             count(DISTINCT s.group_id) OVER(PARTITION BY s.competition_id,s.event_id,{round_key}) round_group_count
      FROM reco q JOIN scrambles s
        ON s.event_id='333' AND {norm_scr_sql}=q.scramble_norm
    )
    SELECT sm.source_id,sm.competition_id,sm.round_key,sm.group_id,sm.scramble_num,
           sm.global_scramble_match_count,sm.round_group_count,
           CAST(r.person_id AS VARCHAR) person_id,r.person_name,
           CAST(a.attempt_number AS INTEGER) attempt_number,CAST(a.value AS BIGINT) attempt_value,
           CAST({start_expr} AS VARCHAR) start_date,CAST({end_expr} AS VARCHAR) end_date,
           CASE WHEN q.solve_date IS NULL THEN NULL
                WHEN q.solve_date BETWEEN {start_expr} AND {end_expr} THEN TRUE ELSE FALSE END date_ok,
           c.name competition_name
    FROM sm
    JOIN reco q ON q.source_id=sm.source_id
    JOIN results r ON r.competition_id=sm.competition_id AND r.event_id='333' AND {round_join}
    JOIN attempts a ON a.result_id=r.id AND CAST(a.attempt_number AS INTEGER)=sm.scramble_num
    LEFT JOIN competitions c ON c.id=sm.competition_id
    WHERE {norm_name_sql}=q.solver_norm
    ORDER BY sm.source_id,sm.competition_id,sm.round_key,r.person_id,a.attempt_number
    """
    cols=[d[0] for d in con.execute(query).description]
    data=[dict(zip(cols,row)) for row in con.execute(query).fetchall()]
    by=defaultdict(list)
    for x in data: by[int(x["source_id"])].append(x)

    out_rows=[]; counts=Counter()
    for r in solves:
        cand=by.get(r["source_id"],[])
        cls,reason=classify(cand,r); counts[cls]+=1
        unique_candidates=[]
        seen=set()
        for x in cand:
            key=(x["competition_id"],x["round_key"],x["person_id"],x["attempt_number"],x["attempt_value"])
            if key in seen: continue
            seen.add(key)
            unique_candidates.append({
                "competition_id":x["competition_id"],"competition_name":x["competition_name"],
                "round_key":x["round_key"],"group_id":x["group_id"],
                "round_group_count":x["round_group_count"],
                "person_id":x["person_id"],"person_name":x["person_name"],
                "attempt_number":x["attempt_number"],"attempt_value":x["attempt_value"],
                "date_ok":x["date_ok"],"start_date":x["start_date"],"end_date":x["end_date"],
                "global_scramble_match_count":x["global_scramble_match_count"]
            })
        out_rows.append({
            "source_id":r["source_id"],"cohort":r["cohort"],"scramble_sha256":r["scramble_sha256"],
            "solver":r["solver"],"result_text":r["result_text"],"result_cs":r["result_cs"],
            "solve_date":r["solve_date"],"competition_source":r["competition"],
            "linkage_class":cls,"reason":reason,"official_candidate_count":len(unique_candidates),
            "official_candidates":unique_candidates
        })

    report={
      "schema_version":"g7-p7-reco-wca-linkage-audit-1",
      "operation_type":"Linkage Audit",
      "authority":"FROZEN_60_RECO_X_FROZEN_WCA_EXPORT",
      "wca_source_sha256":args.wca_source_sha256,
      "reco_solves":60,
      "class_counts":dict(sorted(counts.items())),
      "rows":out_rows,
      "rules":{
        "A_EXACT_EXTERNAL":"unique full-context candidate, exact solver/result/date, globally exact scramble, and one WCA scramble group in round",
        "B_STRONG_EXTERNAL":"unique compatible candidate but public group assignment or source-field completeness prevents A",
        "C_AMBIGUOUS":"multiple official candidates or context conflict",
        "U_UNLINKED":"no official candidate after exact scramble+solver+round+attempt crosswalk"
      },
      "boundary":[
        "no fuzzy solver-name matching",
        "no new reco.nz source contact",
        "WCA public export does not directly expose competitor group assignment",
        "linkage does not identify a cognitive mechanism"
      ]
    }
    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"reco-wca-linkage.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,default=str)+"\n",encoding="utf-8")
    with open(out/"reco-wca-linkage.csv","w",newline="",encoding="utf-8") as f:
        fields=["source_id","cohort","scramble_sha256","solver","result_text","result_cs","solve_date","competition_source","linkage_class","reason","official_candidate_count"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for x in out_rows: w.writerow({k:x.get(k) for k in fields})
    print("G7_P7_RECO_WCA_LINKAGE_AUDIT_PASS")
    print("CLASS_COUNTS\t"+json.dumps(report["class_counts"],sort_keys=True))
    print("CANDIDATE_ROWS\t"+str(len(data)))

if __name__=="__main__":
    main()
