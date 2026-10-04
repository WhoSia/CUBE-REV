#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random
from collections import Counter

ACTIONS=18;TOKENS=256
SEED_TEXT="CUBE_REV_G7_P16_R1_LATENT_POLICY_V1"

def seed_int(s): return int(hashlib.sha256(s.encode()).hexdigest()[:16],16)
def pv(s,n):
    x=[int(v) for v in s.split(",")]
    if len(x)!=n:raise ValueError((n,len(x)))
    return x
def toks(r):
    cp=pv(r["cp"],8);co=pv(r["co"],8);ep=pv(r["ep"],12);eo=pv(r["eo"],12)
    z=[p*8+v for p,v in enumerate(cp)]
    z += [64+p*3+v for p,v in enumerate(co)]
    z += [88+p*12+v for p,v in enumerate(ep)]
    z += [232+p*2+v for p,v in enumerate(eo)]
    if len(z)!=40 or min(z)<0 or max(z)>=TOKENS:raise ValueError("TOKENS")
    return z
def init(rank,seed):
    g=random.Random(seed);s=.02
    E=[[g.uniform(-s,s) for _ in range(rank)] for _ in range(TOKENS)]
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
                ga=gr[a];ua=U[a]
                b[a]-=eta*ga
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
        ok += max(range(ACTIONS),key=lambda a:p[a])==r["y"]
    return {"n_states":len(rows),"nll":nll/len(rows),"top1_accuracy":ok/len(rows)}
def prior(tr,va):
    c=Counter(r["y"] for r in tr);den=len(tr)+ACTIONS;p=[(c[a]+1)/den for a in range(ACTIONS)]
    nll=-sum(math.log(p[r["y"]]) for r in va)/len(va);pred=max(range(ACTIONS),key=lambda a:p[a])
    return {"n_states":len(va),"nll":nll,"top1_accuracy":sum(r["y"]==pred for r in va)/len(va)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--states",required=True);ap.add_argument("--context",required=True)
    ap.add_argument("--preseal",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal))
    if pre["status"]!="FROZEN_BEFORE_R2_MULTICOHORT_FIT":raise SystemExit("PRESEAL")
    rank=pre["fixed_model"]["rank"];epochs=pre["fixed_model"]["epochs"];lr=pre["fixed_model"]["learning_rate"];l2=pre["fixed_model"]["l2"]
    ctx={}
    for line in open(a.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    rows=[];solves={};stages=set()
    with open(a.states,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            c=ctx[(sid,pi)];stage=c.get("development_stage")
            if stage not in ("P11","P13","P14","P15"):raise SystemExit("STAGE")
            rows.append({"sid":sid,"y":y,"tokens":toks(x),"stage":stage})
            solves[sid]=stage;stages.add(stage)
    if len(solves)!=296 or stages!={"P11","P13","P14","P15"}:raise SystemExit("DEV296")

    folds={}
    for stage in ("P11","P13","P14","P15"):
        tr=[r for r in rows if r["stage"]!=stage];va=[r for r in rows if r["stage"]==stage]
        model=train(tr,rank,epochs,lr,l2,seed_int(f"{SEED_TEXT}|R2|hold={stage}"))
        e=ev(model,va);p=prior(tr,va)
        folds[stage]={"validation":e,"prior":p,"delta_nll_vs_prior":p["nll"]-e["nll"],
                      "train_states":len(tr),"heldout_solves":sum(1 for s,v in solves.items() if v==stage)}
    ds=[folds[s]["delta_nll_vs_prior"] for s in ("P11","P13","P14","P15")]
    mean_delta=sum(ds)/4;positive=sum(d>0 for d in ds)
    verdict="TRANSPORT_QUALIFIED_DEVELOPMENT_ONLY" if mean_delta>0 and positive>=3 else "HOLD_TRANSPORT"

    final=train(rows,rank,epochs,lr,l2,seed_int(f"{SEED_TEXT}|R2|full296"))
    full=ev(final,rows)
    E,U,b=final
    report={
      "schema_version":"g7-p16-r2-multicohort-latent-transport-1",
      "operation_type":"Multi-Cohort Development Representation Transport Stress Test",
      "development_only":True,"fresh_confirmation_consumed":False,"new_body_contact":0,
      "solves":296,"states":len(rows),"fixed_rank":rank,"rank_reselected":False,
      "heldout_stage_results":folds,
      "mean_delta_nll_vs_prior":mean_delta,
      "positive_heldout_stages":positive,
      "verdict":verdict,
      "boundary":[
        "All four cohorts are prior-contacted development evidence.",
        "A positive transport verdict only qualifies the representation family for further development; it is not fresh confirmation.",
        "Archive metadata are used only to define held-out stages and are not model inputs.",
        "No cognitive interpretation of latent axes is authorized."
      ]
    }
    model={"schema_version":"g7-p16-r2-latent-policy-model-1","rank":rank,"token_count":TOKENS,"actions":ACTIONS,
           "embedding_E":E,"action_U":U,"action_bias":b}
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"multicohort-latent-transport.json").write_text(json.dumps(report,indent=2)+"\n")
    (out/"latent-policy-model-dev296.json").write_text(json.dumps(model,separators=(",",":"))+"\n")
    print("G7_P16_R2_MULTICOHORT_LATENT_TRANSPORT_EXECUTED")
    print("FOLDS",json.dumps(folds,sort_keys=True))
    print("MEAN_DELTA_NLL",mean_delta,"POSITIVE_STAGES",positive)
    print("VERDICT",verdict)

if __name__=="__main__":main()
