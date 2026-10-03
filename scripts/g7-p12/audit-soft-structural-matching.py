#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random,statistics
from collections import defaultdict,Counter

N=18
P11=0.056231231231231235
ORDER=["R0","R1","R2","R3","R4","NN1","NN3","EXP1","EXP2"]

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(xs): return sum(xs)/len(xs) if xs else None
def MED(xs):
    if not xs:return None
    y=sorted(xs);m=len(y)//2
    return y[m] if len(y)%2 else (y[m-1]+y[m])/2
def qbin(p): return min(4,max(0,int(p*5))) if p<1 else 4
def cells(k,d,l): return (l,k-l,d-l,N-k-d+l)
def dist_units(a,b):
    ca=cells(a["k"],a["d"],a["l"]); cb=cells(b["k"],b["d"],b["l"])
    return sum(abs(x-y) for x,y in zip(ca,cb))/2.0
def wquantile(pairs,q):
    if not pairs:return None
    z=sorted(pairs,key=lambda x:x[0]);tot=sum(w for _,w in z)
    if tot<=0:return None
    acc=0.0
    for v,w in z:
        acc+=w
        if acc/tot>=q:return v
    return z[-1][0]
def sf(v,n,seed):
    if not v:return None
    obs=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        z=M([x*(1 if g.random()<.5 else -1) for x in v])
        if abs(z)>=obs-1e-15:e+=1
    return (e+1)/(n+1)
def stat(v,n,seed):
    return {"n_solves":len(v),"mean":M(v),"median":MED(v),
            "positive":sum(x>0 for x in v),"zero":sum(x==0 for x in v),
            "negative":sum(x<0 for x in v),"signflip_p":sf(v,n,seed)}

def candidate_weights(name,target,comparators):
    ds=[(j,dist_units(target,c)) for j,c in enumerate(comparators)]
    if not ds:return []
    if name.startswith("R"):
        rad=int(name[1:])
        ids=[(j,d) for j,d in ds if d<=rad+1e-15]
        if not ids:return []
        w=1/len(ids);return [(j,w,d) for j,d in ids]
    if name.startswith("NN"):
        k=int(name[2:])
        vals=sorted(set(d for _,d in ds))
        if not vals:return []
        # retain full distance tie at kth neighbor boundary
        ordered=sorted(ds,key=lambda x:(x[1],x[0]))
        cutoff=ordered[min(k,len(ordered))-1][1]
        ids=[(j,d) for j,d in ds if d<=cutoff+1e-15]
        # normalize equally inside each retained set
        w=1/len(ids);return [(j,w,d) for j,d in ids]
    if name.startswith("EXP"):
        tau=int(name[3:])
        vals=[(j,math.exp(-d/tau),d) for j,d in ds]
        den=sum(w for _,w,_ in vals)
        return [(j,w/den,d) for j,w,d in vals] if den>0 else []
    raise KeyError(name)

def structural_eval(rows,name):
    by=defaultdict(list)
    for r in rows:by[(r["sid"],r["q"])].append(r)
    solve_targets=defaultdict(int)
    dist_pairs=[]
    eff_mass=0.0
    target_count=0
    for (_, _),grp in by.items():
        targets=[r for r in grp if r["lb"]==7]
        comps=[r for r in grp if r["lb"] in (6,8)]
        if not targets or not comps:continue
        for t in targets:
            ww=candidate_weights(name,t,comps)
            if not ww:continue
            solve_targets[t["sid"]]+=1;target_count+=1
            # weights normalize within target; effective comparator mass = 1/sum(w^2)
            eff_mass+=1/sum(w*w for _,w,_ in ww)
            for _,w,d in ww:dist_pairs.append((d,w))
    solves=len(solve_targets)
    mean_dist=(sum(d*w for d,w in dist_pairs)/sum(w for _,w in dist_pairs)) if dist_pairs else None
    return {
      "eligible_solves":solves,
      "eligible_solve_ids":sorted(solve_targets),
      "matched_target_states":target_count,
      "effective_comparator_mass_sum":eff_mass,
      "mean_distance_units":mean_dist,
      "p90_distance_units":wquantile(dist_pairs,0.90),
      "max_distance_units":max((d for d,w in dist_pairs if w>0),default=None)
    }

def behavior_eval(rows,name,nperm,seed,override_lb=None):
    by=defaultdict(list)
    for r in rows:by[(r["sid"],r["q"])].append(r)
    per=defaultdict(list)
    for key,grp in by.items():
        def lab(r): return override_lb.get((r["sid"],r["pi"]),r["lb"]) if override_lb else r["lb"]
        targets=[r for r in grp if lab(r)==7]
        comps=[r for r in grp if lab(r) in (6,8)]
        if not targets or not comps:continue
        for t in targets:
            ww=candidate_weights(name,t,comps)
            if not ww:continue
            cmean=sum(w*comps[j]["ex"] for j,w,_ in ww)
            per[t["sid"]].append(t["ex"]-cmean)
    vals={sid:M(xs) for sid,xs in per.items() if xs}
    out=stat(list(vals.values()),nperm,seed)
    out["eligible_solve_ids"]=sorted(vals)
    out["per_solve_delta"]={str(k):v for k,v in sorted(vals.items())}
    return out

def rotated_labels(rows):
    out={}
    by=defaultdict(list)
    for r in rows:by[(r["sid"],r["q"])].append(r)
    for key,grp in by.items():
        grp=sorted(grp,key=lambda r:r["pi"])
        labs=[r["lb"] for r in grp]
        if len(labs)<=1:
            rot=labs
        else:
            rot=labs[1:]+labs[:1]
        for r,l in zip(grp,rot):out[(r["sid"],r["pi"])]=l
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True);ap.add_argument("--context",required=True)
    ap.add_argument("--out",required=True);ap.add_argument("--permutations",type=int,default=100000)
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
        if c.get("next_action_index") is not None:allmax[sid]=max(allmax[sid],pi)

    # Stage 1: structural-only parse. Do not read next_action identity.
    structural=[]
    with open(z.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);c=ctx[(sid,pi)];sh=shell[(sid,pi)]
            if c.get("next_action_index") is None:continue
            if sh["g1"] or sh["lb"] not in (6,7,8):continue
            rivals={r:S(x[r.lower()+"_best"]) for r in ("H1","H2","H3","FS")}
            ts=S(x["ts_best"])
            low={m for m in ts if sum(m in rivals[r] for r in rivals)<=2}
            if not low:continue
            structural.append({
              "sid":sid,"pi":pi,"q":qbin(pi/allmax[sid] if allmax[sid]>0 else 0),
              "lb":sh["lb"],"k":len(low),"d":len(sh["desc"]),"l":len(low & sh["desc"]),
              "ancestry":"FRESH40" if str(c.get("cohort") or "").startswith("P11_") else "LEGACY60"
            })
    scopes={a:[r for r in structural if r["ancestry"]==a] for a in ("FRESH40","LEGACY60")}
    if len({r["sid"] for r in scopes["FRESH40"]})!=40:raise SystemExit("FRESH40_REQUIRED")
    if len({r["sid"] for r in scopes["LEGACY60"]})!=60:raise SystemExit("LEGACY60_REQUIRED")

    census={}
    passing=[]
    for idx,name in enumerate(ORDER):
        f=structural_eval(scopes["FRESH40"],name);l=structural_eval(scopes["LEGACY60"],name)
        ok=(f["eligible_solves"]>=20 and l["eligible_solves"]>=30 and
            f["mean_distance_units"] is not None and l["mean_distance_units"] is not None and
            f["mean_distance_units"]<=1.0+1e-15 and l["mean_distance_units"]<=1.0+1e-15 and
            f["p90_distance_units"]<=2.0+1e-15 and l["p90_distance_units"]<=2.0+1e-15)
        item={"id":name,"order":idx,"FRESH40":f,"LEGACY60":l,"passes":ok,
              "max_ancestry_mean_distance_units":max(v for v in (f["mean_distance_units"],l["mean_distance_units"]) if v is not None),
              "min_ancestry_eligible_fraction":min(f["eligible_solves"]/40,l["eligible_solves"]/60)}
        census[name]=item
        if ok:passing.append(item)

    selected=None
    if passing:
        passing.sort(key=lambda x:(x["max_ancestry_mean_distance_units"],-x["min_ancestry_eligible_fraction"],x["order"]))
        selected=passing[0]["id"]

    # Stage 2: only after structural selection, read action outcomes.
    behavioral=None;negative=None;verdict="SOFT_MATCHING_NOT_AUTHORIZED"
    if selected is not None:
        rows=[]
        with open(z.features,encoding="utf-8",newline="") as f:
            for x in csv.DictReader(f,delimiter="\t"):
                sid=int(x["source_id"]);pi=int(x["prefix_index"]);c=ctx[(sid,pi)];sh=shell[(sid,pi)]
                a=int(x["next_action"])
                if a<0 or c.get("next_action_index") is None:continue
                if sh["g1"] or sh["lb"] not in (6,7,8):continue
                rivals={r:S(x[r.lower()+"_best"]) for r in ("H1","H2","H3","FS")}
                ts=S(x["ts_best"]);low={m for m in ts if sum(m in rivals[r] for r in rivals)<=2}
                if not low:continue
                rows.append({
                  "sid":sid,"pi":pi,"q":qbin(pi/allmax[sid] if allmax[sid]>0 else 0),
                  "lb":sh["lb"],"k":len(low),"d":len(sh["desc"]),"l":len(low & sh["desc"]),
                  "ex":(1 if a in low else 0)-len(low)/N,
                  "ancestry":"FRESH40" if str(c.get("cohort") or "").startswith("P11_") else "LEGACY60"
                })
        bscopes={a:[r for r in rows if r["ancestry"]==a] for a in ("FRESH40","LEGACY60")}
        behavioral={
          "FRESH40":behavior_eval(bscopes["FRESH40"],selected,z.permutations,20271501),
          "LEGACY60":behavior_eval(bscopes["LEGACY60"],selected,z.permutations,20271502)
        }
        negative={}
        for i,anc in enumerate(("FRESH40","LEGACY60")):
            rot=rotated_labels(bscopes[anc])
            negative[anc]=behavior_eval(bscopes[anc],selected,z.permutations,20271511+i,rot)
        f=behavioral["FRESH40"]
        if f["n_solves"]<20:
            verdict="SELECTED_SOFT_MATCH_BEHAVIOR_SUPPORT_LIMITED"
        elif f["mean"] is not None and (f["mean"]<=0 or abs(f["mean"])<=0.5*abs(P11)):
            verdict="STRUCTURAL_OPPORTUNITY_SUFFICIENT_UNDER_PRESEALED_SOFT_MATCHING"
        else:
            verdict="RESIDUAL_LB7_ALIGNMENT_AFTER_PRESEALED_SOFT_MATCHING"

    out={
      "schema_version":"g7-p12-r3-soft-structural-matching-1",
      "operation_type":"Soft Structural-Matching Partial-Identification Audit",
      "structural_selection_behavioral_outcome_blind":True,
      "structural_state_counts":{k:len(v) for k,v in scopes.items()},
      "candidate_census":census,
      "selected_candidate":selected,
      "behavioral_stage_opened":selected is not None,
      "behavioral_stage":behavioral,
      "negative_control_rotated_shell_labels":negative,
      "parent_fresh_local_mean":P11,
      "fresh_residual_to_parent_abs_ratio":(
        abs(behavioral["FRESH40"]["mean"])/abs(P11)
        if behavioral and behavioral["FRESH40"]["mean"] is not None else None),
      "verdict":verdict,
      "boundary":[
        "Structural candidate selection does not use observed next-action identity or behavioral excess.",
        "TV distance is defined on the exact 2x2 action-opportunity contingency table.",
        "Soft matching provides approximate structural adjustment and does not identify causal mediation.",
        "The rotated-label negative control cannot alter the selected candidate.",
        "No human cognitive mechanism is identified."
      ]
    }
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"soft-structural-matching-audit.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P12_R3_SOFT_MATCH_AUDIT_PASS")
    print("CANDIDATES",json.dumps(census,sort_keys=True))
    print("SELECTED",selected)
    print("BEHAVIOR",json.dumps(behavioral,sort_keys=True))
    print("NEGATIVE",json.dumps(negative,sort_keys=True))
    print("RATIO",out["fresh_residual_to_parent_abs_ratio"])
    print("VERDICT",verdict)

if __name__=="__main__":main()
