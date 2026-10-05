#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random

ACTIONS=18
RAW_COUNT=256
HAND_COUNT=141
RANK=8
EPOCHS=30
LR=.06
L2=.0001

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
    return t
def hand_tokens(feat,shell,offset=0):
    t=[]
    for i,key in enumerate(("h1_best","h2_best","h3_best","fs_best","ts_best")):
        for a in S(feat[key]): t.append(offset+i*18+a)
    for a in S(shell["desc_actions"]): t.append(offset+90+a)
    lb=int(shell["phase1_lb"]);t.append(offset+108+lb)
    if int(shell["is_g1"]): t.append(offset+140)
    return t
def init(token_count,rank,seed):
    g=random.Random(seed);s=.02
    E=[[g.uniform(-s,s) for _ in range(rank)] for _ in range(token_count)]
    U=[[g.uniform(-s,s) for _ in range(rank)] for _ in range(ACTIONS)]
    b=[0.0]*ACTIONS
    return E,U,b
def probs(model,toks):
    E,U,b=model;rank=len(U[0]);inv=1/len(toks)
    z=[sum(E[t][j] for t in toks)*inv for j in range(rank)]
    sc=[b[a]+sum(U[a][j]*z[j] for j in range(rank)) for a in range(ACTIONS)]
    mx=max(sc);ex=[math.exp(v-mx) for v in sc];den=sum(ex)
    return [v/den for v in ex],z
def train(rows,token_count,seed):
    E,U,b=init(token_count,RANK,seed);g=random.Random(seed^0x9E3779B97F4A7C15);order=list(range(len(rows)))
    for ep in range(EPOCHS):
        g.shuffle(order);eta=LR/(1+.06*ep)
        for ii in order:
            r=rows[ii];tt=r["tokens"];y=r["y"];p,z=probs((E,U,b),tt)
            gr=[p[a]-(1 if a==y else 0) for a in range(ACTIONS)]
            dz=[sum(gr[a]*U[a][j] for a in range(ACTIONS)) for j in range(RANK)]
            for a in range(ACTIONS):
                ga=gr[a];b[a]-=eta*ga
                for j in range(RANK):U[a][j]-=eta*(ga*z[j]+L2*U[a][j])
            inv=1/len(tt)
            for t in tt:
                for j in range(RANK):E[t][j]-=eta*(dz[j]*inv+L2*E[t][j])
    return E,U,b
def evaluate(model,rows):
    nll=0.;ok=0
    for r in rows:
        p,_=probs(model,r["tokens"]);nll-=math.log(max(p[r["y"]],1e-15))
        ok+=max(range(ACTIONS),key=lambda a:p[a])==r["y"]
    return {"states":len(rows),"nll":nll/len(rows),"top1_accuracy":ok/len(rows)}
def write_model(path,obj):
    data=(json.dumps(obj,separators=(",",":"),ensure_ascii=False)+"\n").encode()
    path.write_bytes(data);return hashlib.sha256(data).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--states",required=True);ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True)
    ap.add_argument("--context",required=True);ap.add_argument("--preseal",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal))
    if pre["status"]!="FROZEN_BEFORE_FULL_DEV296_MODEL_FIT":raise SystemExit("PRESEAL")

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

    raw=[];hand=[];hyb=[];solves=set()
    with open(a.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            stage=ctx[(sid,pi)].get("development_stage")
            if stage not in ("P11","P13","P14","P15"):raise SystemExit("STAGE")
            key=(sid,pi);rt=raw_tokens(states[key]);ht=hand_tokens(x,shell[key],0)
            raw.append({"y":y,"tokens":rt});hand.append({"y":y,"tokens":ht})
            hyb.append({"y":y,"tokens":rt+hand_tokens(x,shell[key],RAW_COUNT)})
            solves.add(sid)
    if len(solves)!=296:raise SystemExit("DEV296")

    specs=[
      ("RAW_LATENT",raw,RAW_COUNT,"CUBE_REV_G7_P16_R5_RAW_FULL_V1"),
      ("HANDCRAFTED_SEARCH",hand,HAND_COUNT,"CUBE_REV_G7_P16_R5_HAND_FULL_V1"),
      ("HYBRID",hyb,RAW_COUNT+HAND_COUNT,"CUBE_REV_G7_P16_R5_HYBRID_FULL_V1")
    ]
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    receipt={"schema_version":"g7-p16-r5-model-freeze-1","phase":"G7-P16-R5","solves":296,"states":len(raw),
             "rank":RANK,"fresh_confirmation_consumed":False,"new_body_contact":0,"models":{}}
    for name,rows,tc,seedtxt in specs:
        model=train(rows,tc,seed_int(seedtxt))
        obj={"schema_version":"g7-p16-r5-policy-model-1","name":name,"rank":RANK,"actions":ACTIONS,
             "token_count":tc,"seed":seedtxt,"epochs":EPOCHS,"learning_rate":LR,"l2":L2,
             "embedding_E":model[0],"action_U":model[1],"action_bias":model[2]}
        path=out/(name.lower()+".json");sha=write_model(path,obj)
        receipt["models"][name]={"file":path.name,"sha256":sha,"development_fit":evaluate(model,rows)}
    receipt["selected_candidate"]="HANDCRAFTED_SEARCH"
    receipt["fresh_contract"]="Evaluate frozen model bytes only; no fitting, rank selection, token changes, or metadata additions."
    (out/"model-freeze-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("G7_P16_R5_MODEL_FREEZE_PASS")
    print("MODELS",json.dumps(receipt["models"],sort_keys=True))
    print("SELECTED",receipt["selected_candidate"])
if __name__=="__main__":main()
