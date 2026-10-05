#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random
from collections import Counter

ACTIONS=18
RAW_COUNT=256
HAND_COUNT=141
TOKENS=RAW_COUNT+HAND_COUNT
SEED_TEXT="CUBE_REV_G7_P16_R4_HYBRID_V1"

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def seed_int(s): return int(hashlib.sha256(s.encode()).hexdigest()[:16],16)
def parse_vec(s,n):
    x=[int(v) for v in s.split(",")]
    if len(x)!=n: raise ValueError((n,len(x)))
    return x
def raw_tokens(r):
    cp=parse_vec(r["cp"],8);co=parse_vec(r["co"],8);ep=parse_vec(r["ep"],12);eo=parse_vec(r["eo"],12)
    t=[]
    for pos,piece in enumerate(cp): t.append(pos*8+piece)
    for pos,ori in enumerate(co): t.append(64+pos*3+ori)
    for pos,piece in enumerate(ep): t.append(88+pos*12+piece)
    for pos,ori in enumerate(eo): t.append(232+pos*2+ori)
    if len(t)!=40 or min(t)<0 or max(t)>=RAW_COUNT: raise ValueError("RAW")
    return t
def hand_tokens(feat,shell):
    t=[]
    for i,key in enumerate(("h1_best","h2_best","h3_best","fs_best","ts_best")):
        for a in S(feat[key]): t.append(RAW_COUNT+i*18+a)
    for a in S(shell["desc_actions"]): t.append(RAW_COUNT+90+a)
    lb=int(shell["phase1_lb"]);t.append(RAW_COUNT+108+lb)
    if int(shell["is_g1"]): t.append(RAW_COUNT+140)
    if min(t)<RAW_COUNT or max(t)>=TOKENS: raise ValueError("HAND")
    return t
def init(rank,seed):
    g=random.Random(seed);s=.02
    return (
      [[g.uniform(-s,s) for _ in range(rank)] for _ in range(TOKENS)],
      [[g.uniform(-s,s) for _ in range(rank)] for _ in range(ACTIONS)],
      [0.0]*ACTIONS
    )
def probs(model,tt):
    E,U,b=model;rank=len(U[0]);inv=1/len(tt)
    z=[sum(E[t][j] for t in tt)*inv for j in range(rank)]
    sc=[b[a]+sum(U[a][j]*z[j] for j in range(rank)) for a in range(ACTIONS)]
    mx=max(sc);ex=[math.exp(v-mx) for v in sc];den=sum(ex)
    return [v/den for v in ex],z
def train(rows,rank,epochs,lr,l2,seed):
    E,U,b=init(rank,seed);g=random.Random(seed^0x9E3779B97F4A7C15);order=list(range(len(rows)))
    for ep in range(epochs):
        g.shuffle(order);eta=lr/(1+.06*ep)
        for ii in order:
            r=rows[ii];tt=r["tokens"];y=r["y"];p,z=probs((E,U,b),tt)
            gr=[p[a]-(1 if a==y else 0) for a in range(ACTIONS)]
            dz=[sum(gr[a]*U[a][j] for a in range(ACTIONS)) for j in range(rank)]
            for a in range(ACTIONS):
                ga=gr[a];b[a]-=eta*ga
                for j in range(rank):U[a][j]-=eta*(ga*z[j]+l2*U[a][j])
            inv=1/len(tt)
            for t in tt:
                for j in range(rank):E[t][j]-=eta*(dz[j]*inv+l2*E[t][j])
    return E,U,b
def ev(model,rows):
    nll=0.;ok=0
    for r in rows:
        p,_=probs(model,r["tokens"]);nll-=math.log(max(p[r["y"]],1e-15))
        ok+=max(range(ACTIONS),key=lambda a:p[a])==r["y"]
    return {"n_states":len(rows),"nll":nll/len(rows),"top1_accuracy":ok/len(rows)}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--states",required=True);ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True)
    ap.add_argument("--context",required=True);ap.add_argument("--preseal",required=True);ap.add_argument("--r3-receipt",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal));r3=json.load(open(a.r3_receipt))
    if pre["status"]!="FROZEN_BEFORE_R4_HYBRID_FIT":raise SystemExit("PRESEAL")
    if r3["verdict"]!="HANDCRAFTED_DOMINANCE_DEVELOPMENT":raise SystemExit("R3_PARENT")
    rank=8;epochs=30;lr=.06;l2=.0001

    ctx={}
    for line in open(a.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    states={}
    with open(a.states,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):states[(int(x["source_id"]),int(x["prefix_index"]))]=x
    shell={}
    with open(a.shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):shell[(int(x["source_id"]),int(x["prefix_index"]))]=x

    rows=[];solves={}
    with open(a.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            c=ctx[(sid,pi)];stage=c.get("development_stage")
            if stage not in ("P11","P13","P14","P15"):raise SystemExit("STAGE")
            key=(sid,pi);tt=raw_tokens(states[key])+hand_tokens(x,shell[key])
            rows.append({"sid":sid,"stage":stage,"y":y,"tokens":tt});solves[sid]=stage
    if len(solves)!=296:raise SystemExit("DEV296")

    hybrid={}
    for stage in ("P11","P13","P14","P15"):
        tr=[r for r in rows if r["stage"]!=stage];va=[r for r in rows if r["stage"]==stage]
        m=train(tr,rank,epochs,lr,l2,seed_int(f"{SEED_TEXT}|hold={stage}"))
        hybrid[stage]=ev(m,va)

    hand={s:r3["direct_comparison"][s]["handcrafted_nll"] for s in ("P11","P13","P14","P15")}
    comp={};hw=0;hy=0;diffs=[]
    for s in ("P11","P13","P14","P15"):
        hn=hand[s];yn=hybrid[s]["nll"];d=yn-hn
        winner="HYBRID" if d<0 else ("HANDCRAFTED_SEARCH" if d>0 else "TIE")
        comp[s]={"handcrafted_nll":hn,"hybrid_nll":yn,"hybrid_minus_hand_nll":d,"winner":winner}
        hy+=d<0;hw+=d>0;diffs.append(d)
    mean_diff=sum(diffs)/4
    if hy>=3 and mean_diff<0:verdict="HYBRID_COMPLEMENTARITY_DEVELOPMENT"
    elif hw>=3 and mean_diff>0:verdict="HANDCRAFTED_SUFFICIENT_DEVELOPMENT"
    else:verdict="NO_CLEAR_COMPLEMENTARITY"
    report={
      "schema_version":"g7-p16-r4-hybrid-complementarity-1","solves":296,"states":len(rows),"rank":8,
      "hybrid_heldout":hybrid,"direct_comparison":comp,"hybrid_stage_wins":hy,"handcrafted_stage_wins":hw,
      "mean_hybrid_minus_hand_nll":mean_diff,"verdict":verdict,
      "fresh_confirmation_consumed":False,"new_body_contact":0,
      "boundary":[
        "Hybrid uses a larger token vocabulary at equal rank; this is not parameter-matched.",
        "All evidence is prior-contacted development data.",
        "Metadata are excluded from representation inputs.",
        "A winner only freezes a candidate for later untouched confirmation."
      ]
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"hybrid-complementarity.json").write_text(json.dumps(report,indent=2)+"\n")
    print("G7_P16_R4_HYBRID_STRESS_EXECUTED")
    print("DIRECT",json.dumps(comp,sort_keys=True))
    print("MEAN_HYBRID_MINUS_HAND_NLL",mean_diff)
    print("VERDICT",verdict)
if __name__=="__main__":main()
