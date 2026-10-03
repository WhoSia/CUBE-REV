#!/usr/bin/env python3
import argparse,csv,json,math,pathlib
from collections import defaultdict,Counter

LATTICE=[
 ("K",("k",)),("D",("d",)),("L",("l",)),
 ("K_D",("k","d")),("K_L",("k","l")),("D_L",("d","l")),
 ("K_D_L",("k","d","l"))
]
R1_GATE={"fresh_max_loss":0.20,"legacy_max_loss":0.20,"fresh_min_support":10,"legacy_min_support":20}

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def qbin(p): return min(4,max(0,int(p*5))) if p<1 else 4
def entropy(counter):
    n=sum(counter.values())
    if n<=1:return 0.0
    return -sum((v/n)*math.log2(v/n) for v in counter.values() if v)
def projection(row,coords):
    return tuple(row[c] for c in coords)
def normalized_conditional_entropy(rows,coords):
    full=Counter((r["k"],r["d"],r["l"]) for r in rows)
    hfull=entropy(full)
    if hfull==0:return 0.0
    groups=defaultdict(Counter)
    for r in rows:
        groups[projection(r,coords)][(r["k"],r["d"],r["l"])]+=1
    n=len(rows)
    hcond=sum((sum(c.values())/n)*entropy(c) for c in groups.values())
    return hcond/hfull
def common_support(rows,coords):
    strata=defaultdict(lambda:{"t":0,"c":0})
    for r in rows:
        key=(r["sid"],r["q"],projection(r,coords))
        strata[key]["t" if r["lb"]==7 else "c"]+=1
    ids=sorted({key[0] for key,v in strata.items() if v["t"] and v["c"]})
    matched_strata=sum(1 for v in strata.values() if v["t"] and v["c"])
    matched_mass=sum(min(v["t"],v["c"]) for v in strata.values() if v["t"] and v["c"])
    return {"solves":len(ids),"solve_ids":ids,"matched_strata":matched_strata,"matched_pair_mass":matched_mass}
def collision_stats(rows,coords):
    groups=defaultdict(Counter)
    for r in rows:
        groups[projection(r,coords)][(r["k"],r["d"],r["l"])]+=1
    merged=[(g,c) for g,c in groups.items() if len(c)>1]
    mass=sum(sum(c.values()) for _,c in merged)
    return {
      "projection_values":len(groups),
      "collision_values":len(merged),
      "collision_state_mass":mass,
      "collision_state_fraction":mass/len(rows) if rows else 0.0,
      "max_exact_tuples_per_projection_value":max((len(c) for c in groups.values()),default=0)
    }
def dominates(a,b):
    return a["loss"]<=b["loss"]+1e-15 and a["support"]>=b["support"] and (
      a["loss"]<b["loss"]-1e-15 or a["support"]>b["support"])
def joint_dominates(a,b):
    return (a["fresh_loss"]<=b["fresh_loss"]+1e-15 and
            a["fresh_support"]>=b["fresh_support"] and
            a["legacy_loss"]<=b["legacy_loss"]+1e-15 and
            a["legacy_support"]>=b["legacy_support"] and
            (a["fresh_loss"]<b["fresh_loss"]-1e-15 or
             a["fresh_support"]>b["fresh_support"] or
             a["legacy_loss"]<b["legacy_loss"]-1e-15 or
             a["legacy_support"]>b["legacy_support"]))
def pareto(records,domfn):
    out=[]
    for k,a in records.items():
        if not any(j!=k and domfn(b,a) for j,b in records.items()):
            out.append(k)
    return out
def rank_order(records):
    return sorted(records,key=lambda k:(records[k]["loss"],-records[k]["support"],k))
def kendall_tau(order1,order2):
    pos1={x:i for i,x in enumerate(order1)};pos2={x:i for i,x in enumerate(order2)}
    items=list(pos1)
    c=d=0
    for i in range(len(items)):
        for j in range(i+1,len(items)):
            a,b=items[i],items[j]
            s1=(pos1[a]-pos1[b]);s2=(pos2[a]-pos2[b])
            if s1*s2>0:c+=1
            elif s1*s2<0:d+=1
    return (c-d)/(c+d) if c+d else 1.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True);ap.add_argument("--context",required=True);ap.add_argument("--out",required=True)
    z=ap.parse_args()
    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    shell={}
    with open(z.shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            shell[(int(x["source_id"]),int(x["prefix_index"]))]={
              "lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),"desc":S(x["desc_actions"])
            }
    allmax=defaultdict(int)
    for (sid,pi),c in ctx.items():
        if c.get("next_action_index") is not None: allmax[sid]=max(allmax[sid],pi)
    rows=[]
    with open(z.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"])
            sh=shell[(sid,pi)]
            if sh["g1"] or sh["lb"] not in (6,7,8):continue
            # R2 uses only structural support geometry. next_action is intentionally not read.
            rivals={r:S(x[r.lower()+"_best"]) for r in ("H1","H2","H3","FS")}
            ts=S(x["ts_best"])
            low={m for m in ts if sum(m in rivals[r] for r in rivals)<=2}
            if not low:continue
            c=ctx[(sid,pi)]
            ancestry="FRESH40" if str(c.get("cohort") or "").startswith("P11_") else "LEGACY60"
            rows.append({
              "sid":sid,"pi":pi,"lb":sh["lb"],"q":qbin(pi/allmax[sid] if allmax[sid]>0 else 0),
              "k":len(low),"d":len(sh["desc"]),"l":len(low & sh["desc"]),"ancestry":ancestry
            })
    scopes={a:[r for r in rows if r["ancestry"]==a] for a in ("FRESH40","LEGACY60")}
    census={}
    ancestry_records={"FRESH40":{},"LEGACY60":{}}
    for name,coords in LATTICE:
        item={"id":name,"coordinates":[c.upper() for c in coords],"dimensions":len(coords)}
        for anc,rs in scopes.items():
            loss=normalized_conditional_entropy(rs,coords)
            support=common_support(rs,coords)
            collision=collision_stats(rs,coords)
            gate_dist={
              "loss_margin_to_r1_gate":0.20-loss,
              "support_margin_to_r1_gate":support["solves"]-(10 if anc=="FRESH40" else 20)
            }
            item[anc]={
              "normalized_conditional_entropy":loss,
              "common_support":support,
              "collision":collision,
              "r1_gate_distance":gate_dist
            }
            ancestry_records[anc][name]={"loss":loss,"support":support["solves"]}
        census[name]=item
    fresh_front=pareto(ancestry_records["FRESH40"],dominates)
    legacy_front=pareto(ancestry_records["LEGACY60"],dominates)
    joint={}
    for name in census:
        joint[name]={
          "fresh_loss":census[name]["FRESH40"]["normalized_conditional_entropy"],
          "fresh_support":census[name]["FRESH40"]["common_support"]["solves"],
          "legacy_loss":census[name]["LEGACY60"]["normalized_conditional_entropy"],
          "legacy_support":census[name]["LEGACY60"]["common_support"]["solves"]
        }
    joint_front=pareto(joint,joint_dominates)
    of=rank_order(ancestry_records["FRESH40"]);ol=rank_order(ancestry_records["LEGACY60"])
    exact="K_D_L"
    verdict="JOINT_PARETO_FRONTIER_MAPPED__NO_THRESHOLD_SELECTION"
    out={
      "schema_version":"g7-p12-r2-pareto-census-1",
      "operation_type":"Support–Information Pareto Frontier Census",
      "behavioral_outcomes_used":False,
      "eligible_state_counts":{k:len(v) for k,v in scopes.items()},
      "lattice_census":census,
      "fresh_pareto_frontier":fresh_front,
      "legacy_pareto_frontier":legacy_front,
      "joint_pareto_frontier":joint_front,
      "ordering":{
        "fresh_loss_then_support_order":of,
        "legacy_loss_then_support_order":ol,
        "kendall_tau":kendall_tau(of,ol),
        "same_order":of==ol
      },
      "exact_endpoint":{
        "id":exact,
        "fresh_loss":census[exact]["FRESH40"]["normalized_conditional_entropy"],
        "fresh_support":census[exact]["FRESH40"]["common_support"]["solves"],
        "legacy_loss":census[exact]["LEGACY60"]["normalized_conditional_entropy"],
        "legacy_support":census[exact]["LEGACY60"]["common_support"]["solves"]
      },
      "singletons":{k:{
        "fresh_loss":census[k]["FRESH40"]["normalized_conditional_entropy"],
        "fresh_support":census[k]["FRESH40"]["common_support"]["solves"],
        "legacy_loss":census[k]["LEGACY60"]["normalized_conditional_entropy"],
        "legacy_support":census[k]["LEGACY60"]["common_support"]["solves"]
      } for k in ("K","D","L")},
      "r1_gate_reference":R1_GATE,
      "verdict":verdict,
      "boundary":[
        "R2 does not read observed next-action outcomes and does not select a behavioral matching representation.",
        "Pareto membership is descriptive on the observed fresh/legacy state surfaces.",
        "Distances to R1 gates are reported without changing those gates.",
        "No result in R2 authorizes cognitive or causal mechanism promotion."
      ]
    }
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"support-information-pareto-census.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P12_R2_PARETO_CENSUS_PASS")
    print("FRESH_FRONTIER",json.dumps(fresh_front))
    print("LEGACY_FRONTIER",json.dumps(legacy_front))
    print("JOINT_FRONTIER",json.dumps(joint_front))
    print("ORDERING",json.dumps(out["ordering"]))
    print("EXACT",json.dumps(out["exact_endpoint"]))
    print("SINGLETONS",json.dumps(out["singletons"]))
    print("CENSUS",json.dumps(census,sort_keys=True))
    print("VERDICT",verdict)

if __name__=="__main__": main()
