#!/usr/bin/env python3
import csv, hashlib, json, os, pathlib, pickle, sys
from collections import OrderedDict

ROOT=pathlib.Path("/input")
OUT=pathlib.Path("/output")
OUT.mkdir(parents=True,exist_ok=True)

# Source class definitions are imported only inside the no-network container.
sys.path.insert(0,"/source")
import CrossTheRiver  # noqa: F401

def load(name):
    with open(ROOT/name,"rb") as f:
        return pickle.load(f)

levels=load("LevelsFinal.pkl")
players=load("ResultsPilot.pkl")
first=load("ResultsFirstDecision.pkl")
all_decisions=load("ResultsAllDecisions.pkl")
time_df=load("ResultsTime.pkl")
additional=load("AdditionalInfo.pkl")

# Build local opaque participant namespace. Raw source keys are never written.
raw_order=[]
def add_raw(x):
    if x is None: return
    k=str(x)
    if k not in raw_order: raw_order.append(k)

for p in players:
    add_raw(getattr(p,"prolific_ID",None))
for d in list(first)+list(all_decisions):
    add_raw(getattr(d,"player_id",None))

# Map any source conversion aliases onto the same local ID where possible.
aliases={}
if isinstance(additional,dict):
    for k,v in additional.items():
        aliases[str(k)]=str(v)
        aliases[str(v)]=str(k)

opaque={}
next_id=1
for raw in raw_order:
    if raw in opaque: continue
    pid=f"P{next_id:03d}"; next_id+=1
    opaque[raw]=pid
    alias=aliases.get(raw)
    if alias is not None: opaque.setdefault(alias,pid)

def pid_of(x):
    k=str(x)
    if k not in opaque:
        opaque[k]=f"P{len(set(opaque.values()))+1:03d}"
    return opaque[k]

def write_csv(path,rows,fields):
    with open(OUT/path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader(); w.writerows(rows)

participant_rows=[]
for p in players:
    participant_rows.append({
      "participant_id":pid_of(getattr(p,"prolific_ID",None)),
      "fps":getattr(p,"fps",None),
      "total_score":getattr(p,"total_score",None),
      "total_time":getattr(p,"total_time",None),
      "levels_completed":len(getattr(p,"level_results",{}) or {})
    })
write_csv("participants.csv",participant_rows,["participant_id","fps","total_score","total_time","levels_completed"])

level_rows=[]
for l in levels:
    level_rows.append({
      "level_name":getattr(l,"level_name",None),
      "level_id":getattr(l,"level_id",None),
      "is_flipped":getattr(l,"is_flipped",None),
      "is_training":getattr(l,"is_training",None),
      "shortcut":getattr(l,"shortcut",None),
      "platform_count":len(getattr(l,"platforms",[]) or []),
      "decision_point_count":len(getattr(l,"decision_points",[]) or [])
    })
write_csv("levels.csv",level_rows,["level_name","level_id","is_flipped","is_training","shortcut","platform_count","decision_point_count"])

def scalarize(v):
    if hasattr(v,"item"):
        try: v=v.item()
        except Exception: pass
    if v is None or isinstance(v,(str,int,float,bool)):
        return v
    return str(v)

def dataframe_rows(df):
    if not hasattr(df,"columns"):
        raise TypeError(f"expected pandas DataFrame, got {type(df)!r}")
    raw_cols=[str(x) for x in df.columns]
    excluded={"Player","ProlificID","prolific_ID","age","Age","gender","Gender","Name","Email"}
    participant_col="SubjectID" if "SubjectID" in raw_cols else ("Player" if "Player" in raw_cols else None)
    keep=[x for x in raw_cols if x not in excluded and x!=participant_col]
    fields=(["participant_id"] if participant_col else [])+keep
    rows=[]
    for _,row in df.iterrows():
        out={}
        if participant_col:
            out["participant_id"]=pid_of(row[participant_col])
        for col in keep:
            out[col]=scalarize(row[col])
        rows.append(out)
    return rows,fields

first_rows,first_fields=dataframe_rows(first)
all_rows,all_fields=dataframe_rows(all_decisions)
write_csv("first_decisions.csv",first_rows,first_fields)
write_csv("all_decisions.csv",all_rows,all_fields)

time_rows,time_columns=dataframe_rows(time_df)
write_csv("timing.csv",time_rows,time_columns)

if "PlatformType" not in [str(x) for x in time_df.columns]:
    raise RuntimeError("TIMING_PLATFORMTYPE_MISSING")
time_analysis_df=time_df[time_df["PlatformType"]!="FirstPlatform"].copy()
time_analysis_rows,time_analysis_columns=dataframe_rows(time_analysis_df)
write_csv("timing_analysis.csv",time_analysis_rows,time_analysis_columns)

def sha(path):
    return hashlib.sha256((OUT/path).read_bytes()).hexdigest()

report={
  "schema_version":"g7-p6-nuzzi-derived-1",
  "source_commit":"911a6f60ad78f1d908dd50c261eaab69e65bf02f",
  "security":{
    "container_network":"none",
    "raw_source_ids_written":False,
    "age_gender_exported":False,
    "raw_pickle_packaged":False
  },
  "counts":{
    "participants":len(participant_rows),
    "levels":len(level_rows),
    "first_decisions":len(first_rows),
    "all_decisions":len(all_rows),
    "timing_rows":len(time_rows),
    "timing_analysis_rows":len(time_analysis_rows)
  },
  "files":{
    x:{"sha256":sha(x),"bytes":(OUT/x).stat().st_size}
    for x in ["participants.csv","levels.csv","first_decisions.csv","all_decisions.csv","timing.csv","timing_analysis.csv"]
  },
  "first_decision_columns":first_fields,
  "all_decision_columns":all_fields,
  "timing_columns":time_columns,
  "timing_analysis_columns":time_analysis_columns
}
(OUT/"derived-receipt.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("G7_P6_NUZZI_DERIVED_PASS")
for k,v in report["counts"].items(): print(f"{k.upper()}\t{v}")
