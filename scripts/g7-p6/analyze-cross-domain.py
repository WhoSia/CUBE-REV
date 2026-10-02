#!/usr/bin/env python3
import csv, hashlib, json, math, pathlib, random, statistics, sys
from collections import defaultdict

ROOT=pathlib.Path(sys.argv[1])
OUT=pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True,exist_ok=True)
PRE=json.load(open("g7/p6/cross-domain-transport.json",encoding="utf-8"))

def read_csv(name):
    with open(ROOT/name,encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def as_bool(v):
    s=str(v).strip().lower()
    if s in {"1","true","t","yes","y"}: return 1
    if s in {"0","false","f","no","n"}: return 0
    try:
        x=float(s)
        if x in (0.0,1.0): return int(x)
    except Exception:
        pass
    raise ValueError(f"not bool: {v!r}")

def as_float(v):
    if v is None or str(v).strip()=="":
        return None
    try: return float(v)
    except Exception: return None

def mean(xs):
    xs=[x for x in xs if x is not None and math.isfinite(x)]
    return sum(xs)/len(xs) if xs else None

def signflip_p(effects,reps=20000,label=""):
    vals=[x for x in effects if x is not None and math.isfinite(x)]
    if not vals: return None
    obs=abs(mean(vals))
    seed=int(hashlib.sha256((PRE["inference"]["seed"]+"|"+label).encode()).hexdigest()[:16],16)
    rng=random.Random(seed)
    extreme=0
    for _ in range(reps):
        x=abs(sum(v*(1 if rng.random()<0.5 else -1) for v in vals)/len(vals))
        if x>=obs-1e-15: extreme+=1
    return (extreme+1)/(reps+1)

def choice_analysis(rows,label):
    req={"participant_id","ChoiceSmall","SmallShorter","SmallSmallerAngle"}
    if not rows or not req.issubset(rows[0]): raise RuntimeError(f"{label}: missing columns")
    clean=[]
    for r in rows:
        clean.append({
            "p":r["participant_id"],
            "y":as_bool(r["ChoiceSmall"]),
            "short":as_bool(r["SmallShorter"]),
            "angle":as_bool(r["SmallSmallerAngle"])
        })
    cells={}
    for s in (0,1):
        for a in (0,1):
            ys=[x["y"] for x in clean if x["short"]==s and x["angle"]==a]
            cells[f"{s}{a}"]={"n":len(ys),"choice_rate":mean(ys)}
    short_effect=mean([x["y"] for x in clean if x["short"]==1])-mean([x["y"] for x in clean if x["short"]==0])
    angle_effect=mean([x["y"] for x in clean if x["angle"]==1])-mean([x["y"] for x in clean if x["angle"]==0])
    interaction=(cells["11"]["choice_rate"]-cells["10"]["choice_rate"])-(cells["01"]["choice_rate"]-cells["00"]["choice_rate"])
    byp=defaultdict(list)
    for x in clean:byp[x["p"]].append(x)
    pe_short=[];pe_angle=[];pe_inter=[]
    for p,xs in sorted(byp.items()):
        s1=[x["y"] for x in xs if x["short"]==1];s0=[x["y"] for x in xs if x["short"]==0]
        a1=[x["y"] for x in xs if x["angle"]==1];a0=[x["y"] for x in xs if x["angle"]==0]
        if s1 and s0: pe_short.append(mean(s1)-mean(s0))
        if a1 and a0: pe_angle.append(mean(a1)-mean(a0))
        c={}
        for s in (0,1):
            for a in (0,1):
                ys=[x["y"] for x in xs if x["short"]==s and x["angle"]==a]
                c[(s,a)]=mean(ys) if ys else None
        if all(c[k] is not None for k in c):
            pe_inter.append((c[(1,1)]-c[(1,0)])-(c[(0,1)]-c[(0,0)]))
    return {
      "rows":len(clean),"participants":len(byp),"cells":cells,
      "marginal":{"small_shorter":short_effect,"small_smaller_angle":angle_effect,"interaction":interaction},
      "participant_paired":{
        "small_shorter":{"n":len(pe_short),"mean":mean(pe_short),"p_signflip":signflip_p(pe_short,label=label+"-short")},
        "small_smaller_angle":{"n":len(pe_angle),"mean":mean(pe_angle),"p_signflip":signflip_p(pe_angle,label=label+"-angle")},
        "interaction":{"n":len(pe_inter),"mean":mean(pe_inter),"p_signflip":signflip_p(pe_inter,label=label+"-interaction")}
      }
    }

def timing_analysis(rows):
    req={"participant_id","PlatformType","StillTime"}
    if not rows or not req.issubset(rows[0]): raise RuntimeError("timing missing columns")
    byp=defaultdict(lambda:defaultdict(list))
    for r in rows:
        t=r["PlatformType"]
        v=as_float(r["StillTime"])
        if v is not None:byp[r["participant_id"]][t].append(v)
    effects_dn=[];effects_pn=[]
    type_means=defaultdict(list)
    for p,d in sorted(byp.items()):
        pm={k:mean(v) for k,v in d.items() if v}
        for k,v in pm.items(): type_means[k].append(v)
        if pm.get("Decision") is not None and pm.get("Nondecision") is not None:
            effects_dn.append(pm["Decision"]-pm["Nondecision"])
        if pm.get("Predecision") is not None and pm.get("Nondecision") is not None:
            effects_pn.append(pm["Predecision"]-pm["Nondecision"])
    return {
      "rows":len(rows),"participants":len(byp),
      "participant_mean_still_time":{k:mean(v) for k,v in sorted(type_means.items())},
      "participant_paired":{
        "decision_minus_nondecision":{"n":len(effects_dn),"mean":mean(effects_dn),"p_signflip":signflip_p(effects_dn,label="timing-D-N")},
        "predecision_minus_nondecision":{"n":len(effects_pn),"mean":mean(effects_pn),"p_signflip":signflip_p(effects_pn,label="timing-P-N")}
      }
    }

first=choice_analysis(read_csv("first_decisions.csv"),"first")
allc=choice_analysis(read_csv("all_decisions.csv"),"all")
timing=timing_analysis(read_csv("timing_analysis.csv"))
participants=len(read_csv("participants.csv"))

expected=PRE["replication_gate"]["required_counts"]
count_pass=(participants==expected["participants"] and first["rows"]==expected["first_decisions"]
            and allc["rows"]==expected["all_decisions"] and timing["rows"]==expected["timing_analysis_rows"])
def cue_pass(res,key):
    x=res["participant_paired"][key]
    return x["mean"] is not None and x["mean"]>0 and x["p_signflip"] is not None and x["p_signflip"]<=0.01
timing_gate=timing["participant_paired"]["decision_minus_nondecision"]
signal_pass=(cue_pass(first,"small_shorter") and cue_pass(first,"small_smaller_angle")
             and cue_pass(allc,"small_shorter") and cue_pass(allc,"small_smaller_angle")
             and timing_gate["mean"] is not None and timing_gate["mean"]>0
             and timing_gate["p_signflip"] is not None and timing_gate["p_signflip"]<=0.01)
if not count_pass:
    verdict="HOLD_EXTERNAL_TRANSPORT_UNUSABLE"
elif signal_pass:
    verdict="PASS_EXTERNAL_MULTI_CUE_BEHAVIORAL_STRUCTURE"
else:
    verdict="PASS_EXTERNAL_BEHAVIOR_DESCRIPTIVE_ONLY"

report={
  "schema_version":"g7-p6-cross-domain-analysis-1",
  "verdict":verdict,
  "authority":"EXTERNAL_COMPARISON_WORLD_ONLY",
  "counts_match_source_notebook":count_pass,
  "first_decision":first,
  "all_decisions":allc,
  "timing":timing,
  "source_informed_replication_gate_pass":signal_pass,
  "boundary":[
    "This replication supports generic multi-cue and decision-state behavioral structure only.",
    "It is not evidence that cube solvers use the same latent representations.",
    "It cannot promote any cube-specific mechanism or P6 rival family.",
    "The cube development and confirmation packets remain unchanged regardless of this result."
  ]
}
(OUT/"cross-domain-analysis.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
with open(OUT/"cross-domain-analysis.md","w",encoding="utf-8") as f:
    f.write("# G7-P6 external planning-data transport\n\n")
    f.write(f"**{verdict}**\n\n")
    f.write(f"- participants: {participants}\n")
    f.write(f"- first decisions: {first['rows']}\n")
    f.write(f"- all decisions: {allc['rows']}\n")
    f.write(f"- timing analysis rows: {timing['rows']}\n")
    f.write(f"- first shorter paired effect: {first['participant_paired']['small_shorter']['mean']:.6f}, p={first['participant_paired']['small_shorter']['p_signflip']:.6g}\n")
    f.write(f"- first angle paired effect: {first['participant_paired']['small_smaller_angle']['mean']:.6f}, p={first['participant_paired']['small_smaller_angle']['p_signflip']:.6g}\n")
    f.write(f"- all shorter paired effect: {allc['participant_paired']['small_shorter']['mean']:.6f}, p={allc['participant_paired']['small_shorter']['p_signflip']:.6g}\n")
    f.write(f"- all angle paired effect: {allc['participant_paired']['small_smaller_angle']['mean']:.6f}, p={allc['participant_paired']['small_smaller_angle']['p_signflip']:.6g}\n")
    f.write(f"- decision-nondecision still-time effect: {timing_gate['mean']:.6f}, p={timing_gate['p_signflip']:.6g}\n")
print("G7_P6_CROSS_DOMAIN_ANALYSIS_PASS")
print("VERDICT\t"+verdict)
print("FIRST_SHORT_EFFECT\t"+str(first["participant_paired"]["small_shorter"]["mean"]))
print("FIRST_ANGLE_EFFECT\t"+str(first["participant_paired"]["small_smaller_angle"]["mean"]))
print("ALL_SHORT_EFFECT\t"+str(allc["participant_paired"]["small_shorter"]["mean"]))
print("ALL_ANGLE_EFFECT\t"+str(allc["participant_paired"]["small_smaller_angle"]["mean"]))
print("DECISION_TIME_EFFECT\t"+str(timing_gate["mean"]))
