#!/usr/bin/env python3
import argparse,csv,json,math,pathlib,random
from collections import defaultdict,Counter

P11=0.056231231231231235
ORDER=["K_D","K_L","D_L","K_D_BINARY_INTERSECTION","K_L_BINARY_NONLOW_DESC"]

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def M(x): return sum(x)/len(x) if x else None
def qbin(p): return min(4,max(0,int(p*5))) if p<1 else 4
def H(counter):
    n=sum(counter.values())
    if n<=1:return 0.0
    return -sum((v/n)*math.log2(v/n) for v in counter.values() if v)
def cond_entropy(rows,repfn):
    full=Counter((r["k"],r["d"],r["l"]) for r in rows)
    hf=H(full)
    if hf==0:return 0.0
    by=defaultdict(Counter)
    for r in rows: by[repfn(r)][(r["k"],r["d"],r["l"])]+=1
    n=len(rows)
    hc=sum((sum(c.values())/n)*H(c) for c in by.values())
    return hc/hf
def rep(name,r):
    k,d,l=r["k"],r["d"],r["l"]
    if name=="K_D":return (k,d)
    if name=="K_L":return (k,l)
    if name=="D_L":return (d,l)
    if name=="K_D_BINARY_INTERSECTION":return (k,d,int(l>0))
    if name=="K_L_BINARY_NONLOW_DESC":return (k,l,int((d-l)>0))
    raise KeyError(name)
def dims(name):return 2 if name in ("K_D","K_L","D_L") else 3
def sf(v,n,seed):
    if not v:return None
    o=abs(M(v));g=random.Random(seed);e=0
    for _ in range(n):
        z=M([x*(1 if g.random()<.5 else -1) for x in v])
        if abs(z)>=o-1e-15:e+=1
    return (e+1)/(n+1)
def common_support(rows,name):
    st=defaultdict(lambda:{"t":0,"c":0})
    for r in rows:
        key=(r["sid"],r["q"],rep(name,r))
        st[key]["t" if r["lb"]==7 else "c"]+=1
    sids=set()
    for key,d in st.items():
        if d["t"] and d["c"]:sids.add(key[0])
    return len(sids),sorted(sids)
def behavior(rows,name,nperm,seed):
    st=defaultdict(lambda:{"t":[],"c":[]})
    for r in rows:
        key=(r["sid"],r["q"],rep(name,r))
        st[key]["t" if r["lb"]==7 else "c"].append(r["ex"])
    per=defaultdict(list)
    for key,d in st.items():
        if d["t"] and d["c"]:
            w=min(len(d["t"]),len(d["c"]))
            per[key[0]].append((M(d["t"])-M(d["c"]),w))
    vals={}
    for sid,xs in per.items():
        den=sum(w for _,w in xs)
        vals[sid]=sum(v*w for v,w in xs)/den
    vv=list(vals.values())
    return {"n_solves":len(vv),"mean":M(vv),"signflip_p":sf(vv,nperm,seed),
            "positive":sum(x>0 for x in vv),"zero":sum(x==0 for x in vv),"negative":sum(x<0 for x in vv),
            "eligible_solve_ids":sorted(vals)}
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
            key=(int(x["source_id"]),int(x["prefix_index"]))
            shell[key]={"lb":int(x["phase1_lb"]),"g1":int(x["is_g1"]),"desc":S(x["desc_actions"])}
    raw=[]; maxpi=defaultdict(int)
    with open(z.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);a=int(x["next_action"])
            if a<0:continue
            sh=shell[(sid,pi)]
            if sh["g1"] or sh["lb"] not in (6,7,8):continue
            sets={r:S(x[r.lower()+"_best"]) for r in ("H1","H2","H3","FS")}
            ts=S(x["ts_best"])
            low={m for m in ts if sum(m in sets[r] for r in sets)<=2}
            if not low:continue
            k=len(low);d=len(sh["desc"]);l=len(low & sh["desc"])
            c=ctx[(sid,pi)]
            ancestry="FRESH40" if str(c.get("cohort") or "").startswith("P11_") else "LEGACY60"
            raw.append({"sid":sid,"pi":pi,"lb":sh["lb"],"k":k,"d":d,"l":l,
                        "ex":(1 if a in low else 0)-k/18,
                        "ancestry":ancestry})
            maxpi[sid]=max(maxpi[sid],pi)
    # denominator must use all face-next progress, not only eligible shell rows
    allmax=defaultdict(int)
    for key,c in ctx.items():
        if c.get("next_action_index") is not None:allmax[key[0]]=max(allmax[key[0]],key[1])
    for r in raw:r["q"]=qbin(r["pi"]/allmax[r["sid"]] if allmax[r["sid"]]>0 else 0)
    scopes={a:[r for r in raw if r["ancestry"]==a] for a in ("FRESH40","LEGACY60")}
    census={}
    passing=[]
    for idx,name in enumerate(ORDER):
        item={"id":name,"dimensions":dims(name)}
        ok=True
        maxloss=0.0
        for anc,rows in scopes.items():
            loss=cond_entropy(rows,lambda r,n=name:rep(n,r))
            cs,ids=common_support(rows,name)
            item[anc]={"normalized_conditional_entropy":loss,"common_support_solves":cs,"common_support_ids":ids}
            maxloss=max(maxloss,loss)
            if anc=="FRESH40":
                ok &= loss<=0.20+1e-15 and cs>=10
            else:
                ok &= loss<=0.20+1e-15 and cs>=20
        item["max_loss"]=maxloss;item["passes"]=bool(ok);item["order"]=idx
        census[name]=item
        if ok:passing.append(item)
    selected=None
    if passing:
        passing.sort(key=lambda x:(x["dimensions"],x["max_loss"],x["order"]))
        selected=passing[0]["id"]
    behavior_out=None;verdict="COMPRESSION_NOT_AUTHORIZED"
    if selected is not None:
        behavior_out={}
        for i,(anc,rows) in enumerate(scopes.items()):
            behavior_out[anc]=behavior(rows,selected,z.permutations,20271400+i)
        f=behavior_out["FRESH40"]
        if f["n_solves"]<10:
            verdict="SELECTED_REPRESENTATION_BEHAVIOR_SUPPORT_LIMITED"
        elif f["mean"] is not None and (f["mean"]<=0 or abs(f["mean"])<=0.5*abs(P11)):
            verdict="STRUCTURAL_OPPORTUNITY_SUFFICIENT_ON_SELECTED_COMPRESSION"
        else:
            verdict="RESIDUAL_LB7_ALIGNMENT_ON_SELECTED_COMPRESSION"
    repout={"schema_version":"g7-p12-r1-opportunity-compression-1",
      "operation_type":"Opportunity-Representation Compression & Sufficiency Audit",
      "selection_behavioral_outcome_blind":True,
      "eligible_state_counts":{k:len(v) for k,v in scopes.items()},
      "candidate_census":census,
      "selected_representation":selected,
      "behavioral_stage":behavior_out,
      "p11_parent_fresh_local_mean":P11,
      "verdict":verdict,
      "boundary":[
        "Candidate selection uses only opportunity geometry, shell labels, progress and ancestry; observed next-action outcomes do not enter selection.",
        "Entropy retention is empirical on observed support and is not universal sufficiency.",
        "Behavioral residual is computed only after the selected structural representation is fixed.",
        "No causal or cognitive mechanism claim follows."
      ]}
    p=pathlib.Path(z.out);p.mkdir(parents=True,exist_ok=True)
    (p/"opportunity-compression-audit.json").write_text(json.dumps(repout,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P12_R1_COMPRESSION_AUDIT_PASS")
    print("CANDIDATES",json.dumps(census,sort_keys=True))
    print("SELECTED",selected)
    print("BEHAVIOR",json.dumps(behavior_out,sort_keys=True))
    print("VERDICT",verdict)
if __name__=="__main__":main()
