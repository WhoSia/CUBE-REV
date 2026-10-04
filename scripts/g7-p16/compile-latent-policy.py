#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random,re
from collections import Counter,defaultdict

ACTIONS=18
TOKENS=256
SEED_TEXT="CUBE_REV_G7_P16_R1_LATENT_POLICY_V1"

def seed_int(s):
    return int(hashlib.sha256(s.encode()).hexdigest()[:16],16)

def parse_vec(s,n):
    x=[int(v) for v in s.split(",")]
    if len(x)!=n: raise ValueError((n,len(x)))
    return x

def tokens_from_row(r):
    cp=parse_vec(r["cp"],8);co=parse_vec(r["co"],8)
    ep=parse_vec(r["ep"],12);eo=parse_vec(r["eo"],12)
    t=[]
    for pos,piece in enumerate(cp):
        if not 0<=piece<8: raise ValueError("CP")
        t.append(pos*8+piece)
    for pos,ori in enumerate(co):
        if not 0<=ori<3: raise ValueError("CO")
        t.append(64+pos*3+ori)
    for pos,piece in enumerate(ep):
        if not 0<=piece<12: raise ValueError("EP")
        t.append(88+pos*12+piece)
    for pos,ori in enumerate(eo):
        if not 0<=ori<2: raise ValueError("EO")
        t.append(232+pos*2+ori)
    if len(t)!=40 or min(t)<0 or max(t)>=TOKENS: raise ValueError("TOKENS")
    return t

def batch_no(s):
    m=re.search(r"(\d+)$",str(s or ""))
    return int(m.group(1)) if m else None

def init_model(rank,seed):
    g=random.Random(seed)
    scale=0.02
    E=[[g.uniform(-scale,scale) for _ in range(rank)] for _ in range(TOKENS)]
    U=[[g.uniform(-scale,scale) for _ in range(rank)] for _ in range(ACTIONS)]
    b=[0.0]*ACTIONS
    return E,U,b

def probs_for(E,U,b,toks):
    rank=len(b) and len(U[0])
    inv=1.0/len(toks)
    z=[sum(E[t][j] for t in toks)*inv for j in range(rank)]
    sc=[b[a]+sum(U[a][j]*z[j] for j in range(rank)) for a in range(ACTIONS)]
    mx=max(sc); ex=[math.exp(v-mx) for v in sc]; den=sum(ex)
    return [v/den for v in ex],z

def train(rows,rank,epochs,lr,l2,seed):
    E,U,b=init_model(rank,seed)
    g=random.Random(seed^0x9E3779B97F4A7C15)
    order=list(range(len(rows)))
    for ep in range(epochs):
        g.shuffle(order)
        eta=lr/(1.0+0.06*ep)
        for ii in order:
            r=rows[ii];toks=r["tokens"];y=r["y"]
            p,z=probs_for(E,U,b,toks)
            grad=[p[a]-(1.0 if a==y else 0.0) for a in range(ACTIONS)]
            dz=[sum(grad[a]*U[a][j] for a in range(ACTIONS)) for j in range(rank)]
            for a in range(ACTIONS):
                ga=grad[a]
                b[a]-=eta*ga
                ua=U[a]
                for j in range(rank):
                    ua[j]-=eta*(ga*z[j]+l2*ua[j])
            inv=1.0/len(toks)
            for t in toks:
                et=E[t]
                for j in range(rank):
                    et[j]-=eta*(dz[j]*inv+l2*et[j])
    return E,U,b

def eval_model(model,rows):
    E,U,b=model
    nll=0.0;correct=0
    for r in rows:
        p,_=probs_for(E,U,b,r["tokens"])
        py=max(p[r["y"]],1e-15)
        nll-=math.log(py)
        pred=max(range(ACTIONS),key=lambda a:p[a])
        correct+=pred==r["y"]
    return {"n_states":len(rows),"nll":nll/len(rows),"top1_accuracy":correct/len(rows)}

def prior_eval(train_rows,val_rows):
    c=Counter(r["y"] for r in train_rows)
    den=len(train_rows)+ACTIONS
    p=[(c[a]+1)/den for a in range(ACTIONS)]
    nll=-sum(math.log(p[r["y"]]) for r in val_rows)/len(val_rows)
    pred=max(range(ACTIONS),key=lambda a:p[a])
    acc=sum(r["y"]==pred for r in val_rows)/len(val_rows)
    return {"n_states":len(val_rows),"nll":nll,"top1_accuracy":acc}

def cv(rows,rank,epochs,lr,l2):
    folds=[]
    for f in range(6):
        va=[r for r in rows if r["fold"]==f]
        tr=[r for r in rows if r["fold"]!=f]
        if not va or not tr: raise SystemExit("EMPTY_FOLD")
        model=train(tr,rank,epochs,lr,l2,seed_int(f"{SEED_TEXT}|rank={rank}|fold={f}"))
        ev=eval_model(model,va); pr=prior_eval(tr,va)
        folds.append({"fold":f,"train_states":len(tr),"validation":ev,"prior":pr,
                      "delta_nll_vs_prior":pr["nll"]-ev["nll"]})
    return {
      "rank":rank,
      "folds":folds,
      "mean_nll":sum(x["validation"]["nll"] for x in folds)/len(folds),
      "mean_prior_nll":sum(x["prior"]["nll"] for x in folds)/len(folds),
      "mean_delta_nll_vs_prior":sum(x["delta_nll_vs_prior"] for x in folds)/len(folds),
      "mean_top1_accuracy":sum(x["validation"]["top1_accuracy"] for x in folds)/len(folds)
    }

def era_transport(rows,rank,epochs,lr,l2):
    eras=sorted({r["era"] for r in rows if r["era"]})
    out={}
    for i,e in enumerate(eras):
        va=[r for r in rows if r["era"]==e]
        tr=[r for r in rows if r["era"]!=e]
        if not va or not tr: continue
        model=train(tr,rank,epochs,lr,l2,seed_int(f"{SEED_TEXT}|era={e}|rank={rank}"))
        ev=eval_model(model,va);pr=prior_eval(tr,va)
        out[e]={"validation":ev,"prior":pr,"delta_nll_vs_prior":pr["nll"]-ev["nll"]}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--states",required=True)
    ap.add_argument("--context",required=True)
    ap.add_argument("--preseal",required=True)
    ap.add_argument("--out",required=True)
    z=ap.parse_args()
    pre=json.load(open(z.preseal,encoding="utf-8"))
    if pre["status"]!="FROZEN_BEFORE_P16_R1_MODEL_FIT": raise SystemExit("PRESEAL")
    ranks=pre["model_family"]["ranks"];epochs=pre["model_family"]["epochs"]
    lr=pre["model_family"]["learning_rate"];l2=pre["model_family"]["l2"]

    ctx={}
    for line in open(z.context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x

    rows=[];solves=set();batches=set()
    with open(z.states,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0: continue
            c=ctx[(sid,pi)]
            b=batch_no(c.get("cohort"))
            if b is None or not 1<=b<=12: raise SystemExit("BATCH_META")
            fold=(b-1)%6
            rows.append({"sid":sid,"pi":pi,"y":y,"tokens":tokens_from_row(x),
                         "batch":b,"fold":fold,"era":c.get("selection_era")})
            solves.add(sid);batches.add(b)
    if len(solves)!=96: raise SystemExit("DEV96_SOLVES_"+str(len(solves)))
    if batches!=set(range(1,13)): raise SystemExit("BATCH12")
    if len(rows)<1000: raise SystemExit("TOO_FEW_STATES")

    cvs=[cv(rows,r,epochs,lr,l2) for r in ranks]
    best=min(cvs,key=lambda q:(round(q["mean_nll"],6),q["rank"]))
    rank=best["rank"]
    final=train(rows,rank,epochs,lr,l2,seed_int(f"{SEED_TEXT}|final|rank={rank}"))
    full=eval_model(final,rows)
    era=era_transport(rows,rank,epochs,lr,l2)
    pass_compiler=all(math.isfinite(q["mean_nll"]) for q in cvs) and best["mean_delta_nll_vs_prior"]>0

    E,U,b=final
    model_obj={
      "schema_version":"g7-p16-r1-latent-policy-model-1",
      "rank":rank,"token_count":TOKENS,"actions":ACTIONS,
      "token_schema":{
        "CP":"0..63 = position*8 + piece",
        "CO":"64..87 = 64 + position*3 + orientation",
        "EP":"88..231 = 88 + position*12 + piece",
        "EO":"232..255 = 232 + position*2 + orientation"
      },
      "embedding_E":E,"action_U":U,"action_bias":b
    }
    report={
      "schema_version":"g7-p16-r1-learned-policy-compiler-readout-1",
      "operation_type":"Development-Only Learned Policy Representation Compiler",
      "development_only":True,
      "fresh_confirmation_consumed":False,
      "new_body_contact":0,
      "solves":len(solves),"states":len(rows),"batches":12,
      "metadata_input_excluded":True,
      "candidate_cv":cvs,
      "selected_rank":rank,
      "selected_full_development_fit":full,
      "leave_one_era_out_descriptive":era,
      "verdict":"COMPILER_PASS_DEVELOPMENT_READY" if pass_compiler else "COMPILER_HOLD",
      "boundary":[
        "P15 dev96 has already been outcome-exposed and carries no P16 confirmation authority.",
        "The latent dimensions are predictive coordinates only, not cognitive variables.",
        "Era/method/reconstructor/solver are excluded from model input.",
        "Fresh independent confirmation is required before any representation superiority claim."
      ]
    }
    out=pathlib.Path(z.out);out.mkdir(parents=True,exist_ok=True)
    (out/"latent-policy-compiler-readout.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (out/"latent-policy-model.json").write_text(json.dumps(model_obj,separators=(",",":"),ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P16_R1_LATENT_POLICY_COMPILER_EXECUTED")
    print("SOLVES",len(solves),"STATES",len(rows))
    print("CV",json.dumps([{k:q[k] for k in ("rank","mean_nll","mean_prior_nll","mean_delta_nll_vs_prior","mean_top1_accuracy")} for q in cvs],sort_keys=True))
    print("SELECTED_RANK",rank)
    print("ERA",json.dumps(era,sort_keys=True))
    print("VERDICT",report["verdict"])

if __name__=="__main__": main()
