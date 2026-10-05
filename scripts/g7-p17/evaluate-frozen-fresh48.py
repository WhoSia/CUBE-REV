#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random

ACTIONS=18
RAW_COUNT=256
HAND_COUNT=141

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def parse_vec(s,n):
    x=[int(v) for v in s.split(",")]
    if len(x)!=n:raise ValueError((n,len(x)))
    return x
def raw_tokens(r):
    cp=parse_vec(r["cp"],8);co=parse_vec(r["co"],8);ep=parse_vec(r["ep"],12);eo=parse_vec(r["eo"],12)
    t=[]
    for pos,piece in enumerate(cp):t.append(pos*8+piece)
    for pos,ori in enumerate(co):t.append(64+pos*3+ori)
    for pos,piece in enumerate(ep):t.append(88+pos*12+piece)
    for pos,ori in enumerate(eo):t.append(232+pos*2+ori)
    return t
def hand_tokens(feat,shell,offset=0):
    t=[]
    for i,key in enumerate(("h1_best","h2_best","h3_best","fs_best","ts_best")):
        for a in S(feat[key]):t.append(offset+i*18+a)
    for a in S(shell["desc_actions"]):t.append(offset+90+a)
    lb=int(shell["phase1_lb"]);t.append(offset+108+lb)
    if int(shell["is_g1"]):t.append(offset+140)
    return t
def probs(model,toks):
    E=model["embedding_E"];U=model["action_U"];b=model["action_bias"];rank=model["rank"]
    inv=1/len(toks)
    z=[sum(E[t][j] for t in toks)*inv for j in range(rank)]
    sc=[b[a]+sum(U[a][j]*z[j] for j in range(rank)) for a in range(ACTIONS)]
    mx=max(sc);ex=[math.exp(v-mx) for v in sc];den=sum(ex)
    return [v/den for v in ex]
def percentile(xs,p):
    y=sorted(xs)
    if not y:return None
    k=(len(y)-1)*p
    lo=int(math.floor(k));hi=int(math.ceil(k))
    if lo==hi:return y[lo]
    return y[lo]*(hi-k)+y[hi]*(k-lo)
def bootstrap(vals,n,seed):
    g=random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:16],16))
    out=[];m=len(vals)
    for _ in range(n):
        out.append(sum(vals[g.randrange(m)] for __ in range(m))/m)
    return {"repetitions":n,"p05":percentile(out,.05),"p95":percentile(out,.95),"mean_of_bootstrap":sum(out)/len(out)}
def load_model(path,expected):
    b=pathlib.Path(path).read_bytes()
    sha=hashlib.sha256(b).hexdigest()
    if sha!=expected:raise SystemExit("MODEL_SHA_MISMATCH_"+sha)
    return json.loads(b),sha

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--states",required=True);ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True)
    ap.add_argument("--metadata",required=True);ap.add_argument("--hand-model",required=True);ap.add_argument("--raw-model",required=True)
    ap.add_argument("--hybrid-model",required=True);ap.add_argument("--preseal",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal))
    if pre["status"]!="FROZEN_BEFORE_FRESH48_MODEL_EVALUATION":raise SystemExit("PRESEAL")
    fm=pre["frozen_models"]
    hand,_=load_model(a.hand_model,fm["HANDCRAFTED_SEARCH"])
    raw,_=load_model(a.raw_model,fm["RAW_LATENT"])
    hyb,_=load_model(a.hybrid_model,fm["HYBRID"])
    if hand["name"]!="HANDCRAFTED_SEARCH" or raw["name"]!="RAW_LATENT" or hyb["name"]!="HYBRID":raise SystemExit("MODEL_NAME")

    meta={}
    for line in open(a.metadata,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);meta[int(x["source_id"])]=x
    if len(meta)!=48:raise SystemExit("META48")

    states={}
    with open(a.states,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):states[(int(x["source_id"]),int(x["prefix_index"]))]=x
    shell={}
    with open(a.shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):shell[(int(x["source_id"]),int(x["prefix_index"]))]=x

    per={sid:{"hand":[],"raw":[],"hyb":[],"hand_ok":[],"raw_ok":[],"hyb_ok":[]} for sid in meta}
    nstates=0
    with open(a.features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            key=(sid,pi);rt=raw_tokens(states[key]);ht=hand_tokens(x,shell[key],0);yt=rt+hand_tokens(x,shell[key],RAW_COUNT)
            ph=probs(hand,ht);pr=probs(raw,rt);py=probs(hyb,yt)
            per[sid]["hand"].append(-math.log(max(ph[y],1e-15)))
            per[sid]["raw"].append(-math.log(max(pr[y],1e-15)))
            per[sid]["hyb"].append(-math.log(max(py[y],1e-15)))
            per[sid]["hand_ok"].append(max(range(ACTIONS),key=lambda z:ph[z])==y)
            per[sid]["raw_ok"].append(max(range(ACTIONS),key=lambda z:pr[z])==y)
            per[sid]["hyb_ok"].append(max(range(ACTIONS),key=lambda z:py[z])==y)
            nstates+=1

    valid=[sid for sid,v in per.items() if v["hand"]]
    if len(valid)<40:
        verdict="SUPPORT_LIMITED"
    else:
        pass

    solve=[]
    for sid in valid:
        v=per[sid]
        mh=sum(v["hand"])/len(v["hand"]);mr=sum(v["raw"])/len(v["raw"]);my=sum(v["hyb"])/len(v["hyb"])
        solve.append({
          "source_id":sid,"states":len(v["hand"]),"hand_nll":mh,"raw_nll":mr,"hybrid_nll":my,
          "hand_minus_raw":mh-mr,"hand_minus_hybrid":mh-my,
          "hand_top1":sum(v["hand_ok"])/len(v["hand_ok"]),
          "raw_top1":sum(v["raw_ok"])/len(v["raw_ok"]),
          "hybrid_top1":sum(v["hyb_ok"])/len(v["hyb_ok"]),
          **meta[sid]
        })
    def mean(key,rows=solve):return sum(r[key] for r in rows)/len(rows) if rows else None
    primary_vals=[r["hand_minus_raw"] for r in solve]
    boot=bootstrap(primary_vals,pre["primary_estimand"]["bootstrap_repetitions"],pre["primary_estimand"]["bootstrap_seed"])
    primary={"n_solves":len(solve),"mean_hand_minus_raw":mean("hand_minus_raw"),**boot}
    if len(solve)<40:
        verdict="SUPPORT_LIMITED"
    elif primary["mean_hand_minus_raw"]<0 and primary["p95"]<0:
        verdict="FRESH_CONFIRMED"
    elif primary["mean_hand_minus_raw"]<0:
        verdict="DIRECTION_ONLY"
    else:
        verdict="NOT_CONFIRMED"

    secondary={
      "mean_hand_minus_hybrid":mean("hand_minus_hybrid"),
      "mean_nll":{"HANDCRAFTED_SEARCH":mean("hand_nll"),"RAW_LATENT":mean("raw_nll"),"HYBRID":mean("hybrid_nll")},
      "mean_top1":{"HANDCRAFTED_SEARCH":mean("hand_top1"),"RAW_LATENT":mean("raw_top1"),"HYBRID":mean("hybrid_top1")}
    }
    groups={}
    for field in ("sampling_cell","method_family","reconstructor_frequency_band","selection_era","cohort"):
        groups[field]={}
        for val in sorted({r[field] for r in solve}):
            rr=[r for r in solve if r[field]==val]
            groups[field][val]={"n":len(rr),"mean_hand_minus_raw":mean("hand_minus_raw",rr),"mean_hand_minus_hybrid":mean("hand_minus_hybrid",rr)}
    report={
      "schema_version":"g7-p17-p4-fresh48-confirmation-1",
      "phase":"G7-P17-P4","fresh_only":True,"retrained":False,"states":nstates,
      "solves":len(solve),"primary":primary,"secondary":secondary,"transport_groups":groups,
      "per_solve":solve,"verdict":verdict,
      "boundary":[
        "Frozen P16-R5 model bytes evaluated without fitting.",
        "HANDCRAFTED_SEARCH vs RAW_LATENT is the sole primary confirmation contrast.",
        "HYBRID and subgroup transport are secondary and cannot rescue primary failure.",
        "No cognitive mechanism claim follows from predictive representation confirmation."
      ]
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"fresh48-frozen-representation-confirmation.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P17_P4_FROZEN_CONFIRMATION_PASS")
    print("PRIMARY",json.dumps(primary,sort_keys=True))
    print("SECONDARY",json.dumps(secondary,sort_keys=True))
    print("VERDICT",verdict)

if __name__=="__main__":main()
