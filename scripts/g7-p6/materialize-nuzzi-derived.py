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

decision_fields=[
 "participant_id","level_name","time","choice_small","distance","euclidean_distance",
 "angle_goal_rad","angle_trajectory_rad","distance_diff","angle_goal_diff",
 "angle_trajectory_diff","normalized_trial_time","unique_rock_id",
 "best_path_steps","trajectory_platform_steps","trajectory_samples"
]
def decision_rows(xs):
    out=[]
    for d in xs:
        out.append({
          "participant_id":pid_of(getattr(d,"player_id",None)),
          "level_name":getattr(d,"level_name",None),
          "time":getattr(d,"time",None),
          "choice_small":getattr(d,"neigh_small",None),
          "distance":getattr(d,"distance",None),
          "euclidean_distance":getattr(d,"euclidean_distance",None),
          "angle_goal_rad":getattr(d,"angle_goal",None),
          "angle_trajectory_rad":getattr(d,"angle_trajectory",None),
          "distance_diff":getattr(d,"distance_diff",None),
          "angle_goal_diff":getattr(d,"angle_goal_diff",None),
          "angle_trajectory_diff":getattr(d,"angle_trajectory_diff",None),
          "normalized_trial_time":getattr(d,"normalized_trial_time",None),
          "unique_rock_id":getattr(d,"unique_rock_id",None),
          "best_path_steps":len(getattr(d,"best_path",[]) or []),
          "trajectory_platform_steps":len(getattr(d,"trajectory_platforms",[]) or []),
          "trajectory_samples":len(getattr(d,"trajectory_real",[]) or [])
        })
    return out

first_rows=decision_rows(first)
all_rows=decision_rows(all_decisions)
write_csv("first_decisions.csv",first_rows,decision_fields)
write_csv("all_decisions.csv",all_rows,decision_fields)

# Preserve only scalar timing-table columns, and re-key participant field.
time_rows=[]
time_columns=[]
if hasattr(time_df,"columns"):
    raw_cols=[str(c) for c in time_df.columns]
    excluded={"Player","ProlificID","prolific_ID","age","Age","gender","Gender","Name","Email"}
    scalar_cols=[]
    for c in raw_cols:
        if c in excluded or c=="SubjectID": continue
        series=time_df[c]
        sample=next((x for x in series.tolist() if x is not None),None)
        if sample is None or isinstance(sample,(str,int,float,bool)):
            scalar_cols.append(c)
    time_columns=["participant_id"]+scalar_cols
    for _,row in time_df.iterrows():
        source_id=row["SubjectID"] if "SubjectID" in raw_cols else row.get("Player",None)
        rec={"participant_id":pid_of(source_id)}
        for c in scalar_cols:
            v=row[c]
            if hasattr(v,"item"):
                try: v=v.item()
                except Exception: pass
            rec[c]=v
        time_rows.append(rec)
write_csv("timing.csv",time_rows,time_columns)

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
    "timing_rows":len(time_rows)
  },
  "files":{
    x:{"sha256":sha(x),"bytes":(OUT/x).stat().st_size}
    for x in ["participants.csv","levels.csv","first_decisions.csv","all_decisions.csv","timing.csv"]
  },
  "timing_columns":time_columns
}
(OUT/"derived-receipt.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("G7_P6_NUZZI_DERIVED_PASS")
for k,v in report["counts"].items(): print(f"{k.upper()}\t{v}")
