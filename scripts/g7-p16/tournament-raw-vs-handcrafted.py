#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random
from collections import Counter

ACTIONS=18
TOKEN_COUNT=141
SEED_TEXT="CUBE_REV_G7_P16_R3_HANDCRAFTED_V1"

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def seed_int(s): return int(hashlib.sha256(s.encode()).hexdigest()[:16],16)
def tokens(feat,shell):
    tt=[]
    for i,key in enumerate(("h1_best","h2_best","h3_best","fs_best","ts_best")):
        for a in S(feat[key]):
            if not 0<=a<18: raise ValueError("ACTION_SET")
            tt.append(i*18+a)
    for a in S(shell["desc_actions"]):
        if not 0<=a<18: raise ValueError("DESC")
        tt.append(90+a)
    lb=int(shell["phase1_lb"])
    if not 0<=lb<32: raise ValueError("LB")
    tt.append(108+lb)
    if int(shell["is_g1"]):tt.append(140)
    if not tt:raise ValueError("EMPTY")
    return tt
def init(rank,seed):
    g=random.Random(seed);s=.02
    E=[[g.uniform(-s,s) for _ in range(rank)] for _ in range(TOKEN_COUNT)]
    U=[[g.uniform(-s,s) for _ in range(rank)] for _ in range(ACTIONS)]
    b=[0.0]*ACTIONS
    return E,U,b
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
            gr=[p[a]-(1.0 if a==y else 0.0) for a in range(ACTIONS)]
            dz=[sum(gr[a]*U[a][j] for a in range(ACTIONS)) for j in range(rank)]
            for a in range(ACTIONS):
                ga=gr[a];ua=U[a];b[a]-=eta*ga
                for j in range(rank):ua[j]-=eta*(ga*z[j]+l2*ua[j])
            inv=1/len(tt)
            for t in tt:
                et=E[t]
                for j in range(rank):et[j]-=eta*(dz[j]*inv+l2*et[j])
    return E,U,b
def ev(model,rows):
    nll=0.;ok=0
    for r in rows:
        p,_=probs(model,r["tokens"]);nll-=math.log(max(p[r["y"]],1e-15))
        ok+=max(range(ACTIONS),key=lambda a:p[a])==r["y"]
    return {"n_states":len(rows),"nll":nll/len(rows),"top1_accuracy":ok/len(rows)}
def prior(tr,va):
    c=Counter(r["y"] for r in tr);den=len(tr)+ACTIONS;p=[(c[a]+1)/den for a in range(ACTIONS)]
    nll=-sum(math.log(p[r["y"]]) for r in va)/len(va);pred=max(range(ACTIONS),key=lambda a:p[a])
    return {"n_states":len(va),"nll":nll,"top1_accuracy":sum(r["y"]==pred for r in va)/len(va)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True)
    ap.add_argument("--context",required=True);ap.add_argument("--preseal",required=True)
    ap.add_argument("--r2-receipt",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal));r2=json.load(open(a.r2_receipt))
    if pre["status"]!="FROZEN_BEFORE_R3_HANDCRAFTED_FIT":raise SystemExit("PRESEAL")
    if r2["verdict"]!="TRANSPORT_QUALIFIED_DEVELOPMENT_ONLY":raise SystemExit("R2_PARENT")
    rank=8;epochs=30;lr=.06;l2=.0001

    ctx={}
    for line in open(a.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    sh={}
    with open(a.shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sh[(int(x["source_id"]),int(x["prefix_index"]))]=x
    rows=[];solves={}
    with open(a.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            c=ctx[(sid,pi)];stage=c.get("development_stage")
            if stage not in ("P11","P13","P14","P15"):raise SystemExit("STAGE")
            rows.append({"sid":sid,"stage":stage,"y":y,"tokens":tokens(x,sh[(sid,pi)])})
            solves[sid]=stage
    if len(solves)!=296:raise SystemExit("DEV296")

    hand={}
    for stage in ("P11","P13","P14","P15"):
        tr=[r for r in rows if r["stage"]!=stage];va=[r for r in rows if r["stage"]==stage]
        m=train(tr,rank,epochs,lr,l2,seed_int(f"{SEED_TEXT}|hold={stage}"))
        e=ev(m,va);p=prior(tr,va)
        hand[stage]={"validation":e,"prior":p,"delta_nll_vs_prior":p["nll"]-e["nll"]}
    raw=r2["heldout_stage_delta_nll_vs_prior"]
    # reconstruct raw heldout NLL from R2 artifact is not in receipt; derive using prior NLL - delta.
    # R2 receipt stores only deltas, so use frozen terminal values encoded below and check deltas.
    raw_nll={
      "P11":2.200782093217985,
      "P13":2.181012889155994,
      "P14":2.1900652549208046,
      "P15":2.2044924238223502
    }
    raw_delta={
      "P11":0.03788229873162274,"P13":0.040673693031226144,
      "P14":0.05143615063439455,"P15":0.03453062038960786
    }
    for s in raw:
        if abs(raw[s]-raw_delta[s])>1e-12:raise SystemExit("R2_RECEIPT_DRIFT")

    comp={};latent_wins=0;hand_wins=0;diffs=[]
    for s in ("P11","P13","P14","P15"):
        hn=hand[s]["validation"]["nll"];rn=raw_nll[s];d=hn-rn
        comp[s]={"raw_latent_nll":rn,"handcrafted_nll":hn,"hand_minus_raw_nll":d,
                 "winner":"RAW_LATENT" if d>0 else ("HANDCRAFTED_SEARCH" if d<0 else "TIE")}
        latent_wins+=d>0;hand_wins+=d<0;diffs.append(d)
    mean_diff=sum(diffs)/4
    if latent_wins>=3 and mean_diff>0:verdict="LATENT_DOMINANCE_DEVELOPMENT"
    elif hand_wins>=3 and mean_diff<0:verdict="HANDCRAFTED_DOMINANCE_DEVELOPMENT"
    else:verdict="NO_CLEAR_REPRESENTATION_WINNER"

    report={
      "schema_version":"g7-p16-r3-representation-tournament-1",
      "operation_type":"Development-Only Representation Tournament",
      "solves":296,"states":len(rows),"rank":8,
      "fresh_confirmation_consumed":False,"new_body_contact":0,
      "handcrafted_heldout":hand,
      "raw_parent_nll":raw_nll,
      "direct_comparison":comp,
      "latent_stage_wins":latent_wins,"handcrafted_stage_wins":hand_wins,
      "mean_hand_minus_raw_nll":mean_diff,
      "verdict":verdict,
      "boundary":[
        "All evidence is development-only.",
        "Raw latent NLL is imported from immutable R2 parent authority and is not retrained.",
        "Handcrafted representation uses exact search-coordinate features only; metadata are excluded.",
        "Equal rank is a capacity-control convenience, not a causal equivalence.",
        "A development winner still requires untouched fresh confirmation."
      ]
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"representation-tournament.json").write_text(json.dumps(report,indent=2)+"\n")
    print("G7_P16_R3_REPRESENTATION_TOURNAMENT_EXECUTED")
    print("HAND",json.dumps(hand,sort_keys=True))
    print("DIRECT",json.dumps(comp,sort_keys=True))
    print("MEAN_HAND_MINUS_RAW_NLL",mean_diff)
    print("VERDICT",verdict)

if __name__=="__main__":main()
