#!/usr/bin/env python3
import argparse, json, pathlib, re, unicodedata, math
from collections import Counter, defaultdict
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
    minutes=int(m.group(1) or 0)
    sec=int(m.group(2))
    frac=(m.group(3) or "0")
    cs=int((frac+"00")[:2])
    return (minutes*60+sec)*100+cs

def first(root,stem):
    xs=sorted(pathlib.Path(root).rglob(f"*{stem}*.tsv"))
    exact=[p for p in xs if p.name.endswith(f"{stem}.tsv")]
    if not xs: raise FileNotFoundError(stem)
    return exact[0] if exact else xs[0]

def qp(p):
    return str(pathlib.Path(p).resolve()).replace("'","''")

def source_label_class(comp, competition_matches):
    n=norm_text(comp)
    if not n:
        return "NO_SOURCE_COMPETITION_CONTEXT"
    if n=="unofficial":
        return "SOURCE_DECLARED_UNOFFICIAL"
    if "monkey league" in n:
        return "MONKEY_LEAGUE_LABEL"
    if n in {"speedcubedb","speed cube database","cubesolv.es","cubesolves","cubedb"}:
        return "RECONSTRUCTION_PLATFORM_LABEL"
    if competition_matches>0:
        return "EXACT_NORMALIZED_WCA_COMPETITION_NAME"
    return "OTHER_UNMATCHED_SOURCE_LABEL"

def wca_support_class(comp_matches, solver_rows, result_rows):
    if result_rows>0:
        return "WCA_COMPETITION_SOLVER_RESULT_EXACT_CONTEXT"
    if solver_rows>0:
        return "WCA_COMPETITION_SOLVER_EXACT_CONTEXT"
    if comp_matches>0:
        return "WCA_COMPETITION_EXACT_ONLY"
    return "NO_EXACT_WCA_COMPETITION_CONTEXT"

def shares(counts,total):
    return {k:{"count":v,"share":v/total if total else None} for k,v in sorted(counts.items())}

def year_of(x):
    m=re.match(r"(20\d{2})",str(x or ""))
    return m.group(1) if m else "UNKNOWN"

def cross_counts(rows,a,b):
    c=Counter((x[a],x[b]) for x in rows)
    return [{"a":k[0],"b":k[1],"count":v} for k,v in sorted(c.items())]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--index",required=True)
    ap.add_argument("--wca-dir",required=True)
    ap.add_argument("--sample-registry",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--wca-source-sha256",required=True)
    args=ap.parse_args()

    rows=[]
    for line in open(args.index,encoding="utf-8"):
        if not line.strip(): continue
        x=json.loads(line)
        rows.append({
            "source_id":int(x["source_id"]),
            "puzzle":x.get("puzzle"),
            "solver":x.get("solver"),
            "solver_norm":norm_text(x.get("solver")),
            "date":x.get("date"),
            "year":year_of(x.get("date")),
            "competition":x.get("competition"),
            "competition_norm":norm_text(x.get("competition")),
            "result":x.get("result"),
            "result_cs":parse_result_cs(x.get("result")),
            "legacy_p3_tier":x.get("tier"),
        })
    if len(rows)!=12941 or len({x["source_id"] for x in rows})!=12941:
        raise SystemExit("INDEX_12941_AUTHORITY_MISMATCH")
    three=[x for x in rows if x["puzzle"]=="3x3"]
    if len(three)!=10591:
        raise SystemExit("INDEX_3X3_10591_AUTHORITY_MISMATCH")

    root=pathlib.Path(args.wca_dir)
    res=first(root,"results")
    att=first(root,"result_attempts")
    comp=first(root,"competitions")
    con=duckdb.connect()
    con.execute("PRAGMA threads=4")
    con.execute("PRAGMA preserve_insertion_order=false")
    con.execute(f"CREATE VIEW res AS SELECT * FROM read_csv_auto('{qp(res)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW att AS SELECT * FROM read_csv_auto('{qp(att)}',delim='\\t',header=true,sample_size=200000)")
    con.execute(f"CREATE VIEW comp AS SELECT * FROM read_csv_auto('{qp(comp)}',delim='\\t',header=true,sample_size=200000)")
    rc=[x[0] for x in con.execute("DESCRIBE res").fetchall()]
    cc=[x[0] for x in con.execute("DESCRIBE comp").fetchall()]
    if not {"id","competition_id","event_id","person_name"}.issubset(rc):
        raise SystemExit("WCA_RESULTS_SCHEMA_MISMATCH")
    if not {"id","name"}.issubset(cc):
        raise SystemExit("WCA_COMPETITIONS_SCHEMA_MISMATCH")

    con.execute("CREATE TABLE q(source_id BIGINT,competition_norm VARCHAR,solver_norm VARCHAR,result_cs BIGINT)")
    con.executemany("INSERT INTO q VALUES (?,?,?,?)",[
        (x["source_id"],x["competition_norm"],x["solver_norm"],x["result_cs"]) for x in three
    ])
    norm_comp_sql="lower(trim(regexp_replace(c.name,'\\s+',' ','g')))"
    norm_name_sql="lower(trim(regexp_replace(r.person_name,'\\s+',' ','g')))"
    sql=f"""
    WITH cm AS (
      SELECT q.source_id,c.id competition_id
      FROM q JOIN comp c ON q.competition_norm<>'' AND {norm_comp_sql}=q.competition_norm
    ),
    sm AS (
      SELECT cm.source_id,r.id result_id
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
      SELECT source_id,count(DISTINCT competition_id) competition_matches
      FROM cm GROUP BY source_id
    ),
    sa AS (
      SELECT source_id,count(*) solver_result_rows
      FROM sm GROUP BY source_id
    )
    SELECT q.source_id,
           coalesce(ca.competition_matches,0) competition_matches,
           coalesce(sa.solver_result_rows,0) solver_result_rows,
           coalesce(rm.result_match_rows,0) result_match_rows
    FROM q
    LEFT JOIN ca USING(source_id)
    LEFT JOIN sa USING(source_id)
    LEFT JOIN rm USING(source_id)
    ORDER BY q.source_id
    """
    cur=con.execute(sql)
    cols=[d[0] for d in cur.description]
    support={int(r[0]):dict(zip(cols,r)) for r in cur.fetchall()}

    for x in rows:
        if x["puzzle"]=="3x3":
            s=support[x["source_id"]]
            x["competition_matches"]=int(s["competition_matches"])
            x["solver_result_rows"]=int(s["solver_result_rows"])
            x["result_match_rows"]=int(s["result_match_rows"])
            x["source_label_class"]=source_label_class(x["competition"],x["competition_matches"])
            x["wca_context_support"]=wca_support_class(x["competition_matches"],x["solver_result_rows"],x["result_match_rows"])
        else:
            x["competition_matches"]=None
            x["solver_result_rows"]=None
            x["result_match_rows"]=None
            x["source_label_class"]=source_label_class(x["competition"],0)
            x["wca_context_support"]="NOT_EVALUATED_NON_3X3"

    rec=json.load(open(args.sample_registry,encoding="utf-8"))
    sample_ids={int(x) for x in rec["source_id_to_broad_provenance_class"]}
    if len(sample_ids)!=60:
        raise SystemExit("SAMPLE_REGISTRY_60_REQUIRED")
    row_ids={x["source_id"] for x in rows}
    if not sample_ids.issubset(row_ids):
        raise SystemExit("SAMPLE_IDS_NOT_IN_INDEX")
    sample=[x for x in three if x["source_id"] in sample_ids]
    if len(sample)!=60:
        raise SystemExit("SAMPLE_60_NOT_3X3")
    broad={str(k):v for k,v in rec["source_id_to_broad_provenance_class"].items()}

    def summary(xs):
        return {
            "rows":len(xs),
            "source_label_classes":shares(Counter(x["source_label_class"] for x in xs),len(xs)),
            "wca_context_support":shares(Counter(x["wca_context_support"] for x in xs),len(xs)),
            "year_counts":dict(sorted(Counter(x["year"] for x in xs).items())),
            "legacy_p3_tier_counts":dict(sorted(Counter(x["legacy_p3_tier"] for x in xs).items())),
        }

    pop=summary(three)
    samp=summary(sample)
    transport={}
    for k in sorted(set(pop["source_label_classes"])|set(samp["source_label_classes"])):
        ps=pop["source_label_classes"].get(k,{"share":0})["share"] or 0
        ss=samp["source_label_classes"].get(k,{"share":0})["share"] or 0
        transport[k]={
            "population_share":ps,
            "sample_share":ss,
            "sample_minus_population":ss-ps,
            "sample_to_population_ratio":(ss/ps if ps>0 else None)
        }

    unmatched=Counter(x["competition"] or "" for x in three if x["source_label_class"]=="OTHER_UNMATCHED_SOURCE_LABEL")
    result={
      "schema_version":"g7-p7-full-index-provenance-support-census-1",
      "operation_type":"Full-Index Provenance-Support Census",
      "authority":"POPULATION_METADATA_CENSUS_ONLY",
      "reco_rows_all":len(rows),
      "reco_rows_3x3":len(three),
      "wca_source_sha256":args.wca_source_sha256,
      "population_3x3":pop,
      "frozen_body_sample_60":samp,
      "sample_transport_source_label":transport,
      "sample_broad_provenance_x_index_source_label":[
        {"broad_provenance":k[0],"index_source_label_class":k[1],"count":v}
        for k,v in sorted(Counter((broad[str(x["source_id"])],x["source_label_class"]) for x in sample).items())
      ],
      "sample_broad_provenance_x_index_wca_support":[
        {"broad_provenance":k[0],"index_wca_context_support":k[1],"count":v}
        for k,v in sorted(Counter((broad[str(x["source_id"])],x["wca_context_support"]) for x in sample).items())
      ],
      "source_label_x_wca_support":cross_counts(three,"source_label_class","wca_context_support"),
      "year_x_source_label":cross_counts(three,"year","source_label_class"),
      "top_other_unmatched_source_labels":[{"label":k,"count":v} for k,v in unmatched.most_common(50)],
      "data_availability_boundary":[
        "retained row-level metadata does not contain method/reconstructor for the full population",
        "no population provenance×method or provenance×reconstructor cross-table is inferred",
        "automatic WCA matching is exact-normalized only",
        "no fuzzy alias recovery is used in this Census",
        "failure of exact WCA context support is not proof of non-WCA provenance",
        "index-visible blank competition is not equivalent to body-recovered unofficial provenance",
        "sample broad provenance and index-visible source labels are reported as separate variables",
        "no new reco.nz solve-body contact occurred"
      ]
    }

    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"full-index-provenance-support-census.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with open(out/"full-index-provenance-rows.jsonl","w",encoding="utf-8") as f:
        for x in three:
            f.write(json.dumps({
                "source_id":x["source_id"],"year":x["year"],"source_label_class":x["source_label_class"],
                "wca_context_support":x["wca_context_support"],
                "competition_matches":x["competition_matches"],
                "solver_result_rows":x["solver_result_rows"],
                "result_match_rows":x["result_match_rows"]
            },ensure_ascii=False)+"\n")

    print("G7_P7_FULL_INDEX_PROVENANCE_CENSUS_PASS")
    print("ALL_ROWS\t"+str(len(rows)))
    print("THREE_ROWS\t"+str(len(three)))
    print("SOURCE_LABEL_COUNTS\t"+json.dumps({k:v["count"] for k,v in pop["source_label_classes"].items()},sort_keys=True))
    print("WCA_SUPPORT_COUNTS\t"+json.dumps({k:v["count"] for k,v in pop["wca_context_support"].items()},sort_keys=True))
    print("SAMPLE_SOURCE_LABEL_COUNTS\t"+json.dumps({k:v["count"] for k,v in samp["source_label_classes"].items()},sort_keys=True))

if __name__=="__main__":
    main()
