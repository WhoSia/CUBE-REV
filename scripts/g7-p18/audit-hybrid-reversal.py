#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random
from collections import Counter,defaultdict

ACTIONS=18
RAW_COUNT=256
HAND_COUNT=141
RANK=8
EPOCHS=30
LR=.06
L2=.0001
SCALES=(160,224,296)
SEEDS=("CUBE_REV_G7_P18_SEED_A","CUBE_REV_G7_P18_SEED_B","CUBE_REV_G7_P18_SEED_C","CUBE_REV_G7_P18_SEED_D")
STAGES=("P11","P13","P14","P15")

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def seed_int(s): return int(hashlib.sha256(s.encode()).hexdigest()[:16],16)
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
def init(token_count,seed):
    g=random.Random(seed);s=.02
    E=[[g.uniform(-s,s) for _ in range(RANK)] for _ in range(token_count)]
    U=[[g.uniform(-s,s) for _ in range(RANK)] for _ in range(ACTIONS)]
    b=[0.0]*ACTIONS
    return E,U,b
def probs(model,toks):
    E,U,b=model;inv=1/len(toks)
    z=[sum(E[t][j] for t in toks)*inv for j in range(RANK)]
    sc=[b[a]+sum(U[a][j]*z[j] for j in range(RANK)) for a in range(ACTIONS)]
    mx=max(sc);ex=[math.exp(v-mx) for v in sc];den=sum(ex)
    return [v/den for v in ex]
def train(rows,token_count,seed):
    E,U,b=init(token_count,seed);g=random.Random(seed^0x9E3779B97F4A7C15);order=list(range(len(rows)))
    for ep in range(EPOCHS):
        g.shuffle(order);eta=LR/(1+.06*ep)
        for ii in order:
            r=rows[ii];tt=r["tokens"];y=r["y"];p=probs((E,U,b),tt)
            inv=1/len(tt)
            z=[sum(E[t][j] for t in tt)*inv for j in range(RANK)]
            gr=[p[a]-(1 if a==y else 0) for a in range(ACTIONS)]
            dz=[sum(gr[a]*U[a][j] for a in range(ACTIONS)) for j in range(RANK)]
            for a in range(ACTIONS):
                ga=gr[a];b[a]-=eta*ga
                for j in range(RANK):U[a][j]-=eta*(ga*z[j]+L2*U[a][j])
            for t in tt:
                for j in range(RANK):E[t][j]-=eta*(dz[j]*inv+L2*E[t][j])
    return E,U,b
def eval_solve(model,rows):
    per=defaultdict(list)
    for r in rows:
        p=probs(model,r["tokens"]);per[r["sid"]].append(-math.log(max(p[r["y"]],1e-15)))
    return {sid:sum(v)/len(v) for sid,v in per.items()}
def mean(xs): return sum(xs)/len(xs) if xs else None
def median(xs):
    y=sorted(xs);n=len(y)
    if not n:return None
    return y[n//2] if n%2 else (y[n//2-1]+y[n//2])/2
def quotas(n,counts):
    raw={s:n*counts[s]/sum(counts.values()) for s in STAGES}
    q={s:int(math.floor(raw[s])) for s in STAGES}
    left=n-sum(q.values())
    for s in sorted(STAGES,key=lambda x:(-(raw[x]-q[x]),x))[:left]:q[s]+=1
    return q
def hash_rank(seed,sid):return hashlib.sha256(f"{seed}|{sid}".encode()).hexdigest()
def select_sids(stage_sids,n,seed):
    counts={s:len(stage_sids[s]) for s in STAGES};q=quotas(n,counts);out=set()
    for s in STAGES:
        xs=sorted(stage_sids[s],key=lambda sid:(hash_rank(seed+"|"+s,sid),sid))
        out.update(xs[:q[s]])
    if len(out)!=n:raise SystemExit("SCALE_SELECTION_FAIL")
    return out,q
def reweight_margin(per_solve,dev_meta,stage,axis):
    stage_rows=[m for m in dev_meta.values() if m.get("development_stage")==stage]
    if not stage_rows:return {"evaluable":False,"reason":"NO_STAGE"}
    target=Counter(m.get(axis) for m in stage_rows if m.get(axis) not in (None,"NULL","UNKNOWN"))
    if not target:return {"evaluable":False,"reason":"NO_TARGET_LEVELS"}
    p17_levels=Counter(r.get(axis) for r in per_solve if r.get(axis) not in (None,"NULL","UNKNOWN"))
    if any(level not in p17_levels for level in target):
        return {"evaluable":False,"reason":"UNSUPPORTED_LEVEL","target_levels":dict(target),"p17_levels":dict(p17_levels)}
    total=sum(target.values());val=0.0
    level_means={}
    for level,c in target.items():
        xs=[r["hybrid_nll"]-r["hand_nll"] for r in per_solve if r.get(axis)==level]
        if not xs:return {"evaluable":False,"reason":"EMPTY_LEVEL"}
        lm=mean(xs);level_means[str(level)]=lm;val+=(c/total)*lm
    return {"evaluable":True,"weighted_hybrid_minus_hand":val,"target_levels":dict(target),"level_means":level_means}

def main():
    ap=argparse.ArgumentParser()
    for x in ("dev_states","dev_features","dev_shell","dev_context","fresh_states","fresh_features","fresh_shell","fresh_metadata","p17_report","preseal","out"):
        ap.add_argument("--"+x.replace("_","-"),dest=x,required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal))
    if pre["status"]!="FROZEN_AFTER_P17_BEFORE_P18_OUTCOME":raise SystemExit("PRESEAL")

    # Development rows/meta
    dctx={}
    dev_meta={}
    for line in open(a.dev_context,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);key=(int(x["source_id"]),int(x["prefix_index"]));dctx[key]=x
            sid=key[0]
            dev_meta.setdefault(sid,{
              "development_stage":x.get("development_stage"),
              "method_family":x.get("method_family"),
              "reconstructor_frequency_band":x.get("reconstructor_frequency_band"),
              "selection_era":x.get("selection_era")
            })
    dstates={}
    with open(a.dev_states,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):dstates[(int(x["source_id"]),int(x["prefix_index"]))]=x
    dshell={}
    with open(a.dev_shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):dshell[(int(x["source_id"]),int(x["prefix_index"]))]=x
    dev_hand=[];dev_hyb=[];stage_sids=defaultdict(set)
    with open(a.dev_features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            stage=dctx[(sid,pi)].get("development_stage")
            if stage not in STAGES:raise SystemExit("DEV_STAGE")
            key=(sid,pi);rt=raw_tokens(dstates[key]);ht=hand_tokens(x,dshell[key],0)
            dev_hand.append({"sid":sid,"stage":stage,"y":y,"tokens":ht})
            dev_hyb.append({"sid":sid,"stage":stage,"y":y,"tokens":rt+hand_tokens(x,dshell[key],RAW_COUNT)})
            stage_sids[stage].add(sid)
    if sum(len(stage_sids[s]) for s in STAGES)!=296:raise SystemExit("DEV296")

    # Fresh rows
    fmeta={}
    for line in open(a.fresh_metadata,encoding="utf-8"):
        if line.strip():
            x=json.loads(line);fmeta[int(x["source_id"])]=x
    if len(fmeta)!=48:raise SystemExit("FRESH48_META")
    fstates={}
    with open(a.fresh_states,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):fstates[(int(x["source_id"]),int(x["prefix_index"]))]=x
    fshell={}
    with open(a.fresh_shell,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):fshell[(int(x["source_id"]),int(x["prefix_index"]))]=x
    fresh_hand=[];fresh_hyb=[]
    with open(a.fresh_features,encoding="utf-8",newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            key=(sid,pi);rt=raw_tokens(fstates[key]);ht=hand_tokens(x,fshell[key],0)
            fresh_hand.append({"sid":sid,"y":y,"tokens":ht})
            fresh_hyb.append({"sid":sid,"y":y,"tokens":rt+hand_tokens(x,fshell[key],RAW_COUNT)})

    scale={}
    for n in SCALES:
        scale[str(n)]={}
        for seedtxt in SEEDS:
            chosen,q=select_sids(stage_sids,n,seedtxt+"|scale="+str(n))
            trh=[r for r in dev_hand if r["sid"] in chosen];tryb=[r for r in dev_hyb if r["sid"] in chosen]
            hm=train(trh,HAND_COUNT,seed_int(seedtxt+"|HAND|n="+str(n)))
            ym=train(tryb,RAW_COUNT+HAND_COUNT,seed_int(seedtxt+"|HYB|n="+str(n)))
            he=eval_solve(hm,fresh_hand);ye=eval_solve(ym,fresh_hyb)
            ids=sorted(set(he)&set(ye))
            diffs=[ye[s]-he[s] for s in ids]
            scale[str(n)][seedtxt]={
              "n_train_solves":n,"stage_quotas":q,"n_fresh_solves":len(ids),
              "hybrid_minus_hand_mean":mean(diffs),
              "hybrid_minus_hand_median":median(diffs),
              "hybrid_win_solves":sum(d<0 for d in diffs),
              "hand_win_solves":sum(d>0 for d in diffs)
            }

    med={n:median([scale[str(n)][s]["hybrid_minus_hand_mean"] for s in SEEDS]) for n in SCALES}
    h_scale=(med[160]>=med[224]-1e-15 and med[224]>=med[296]-1e-15 and med[296]<0 and (med[160]-med[296])>=0.01-1e-15)
    full=[scale["296"][s]["hybrid_minus_hand_mean"] for s in SEEDS]
    neg=sum(x<0 for x in full)
    h_variance=(neg<3 or (min(full)<=-0.01 and max(full)>=0.01))

    p17=json.load(open(a.p17_report,encoding="utf-8"))
    ps=p17["per_solve"]
    base=mean([r["hybrid_nll"]-r["hand_nll"] for r in ps])
    comp={}
    comp_trigger=False
    for stage in STAGES:
        comp[stage]={}
        for axis in ("method_family","reconstructor_frequency_band","selection_era"):
            rr=reweight_margin(ps,dev_meta,stage,axis);comp[stage][axis]=rr
            if rr.get("evaluable"):
                v=rr["weighted_hybrid_minus_hand"]
                if (base<0<v or base>0>v) or abs(v-base)>=0.01-1e-15:comp_trigger=True
    h_composition=comp_trigger

    raw_better=[r for r in ps if (r["hand_nll"]-r["raw_nll"])>0]
    hand_better=[r for r in ps if (r["hand_nll"]-r["raw_nll"])<0]
    rb=mean([r["hand_nll"]-r["hybrid_nll"] for r in raw_better])
    hb=mean([r["hand_nll"]-r["hybrid_nll"] for r in hand_better])
    h_complementarity=(rb is not None and hb is not None and rb>0 and (rb-hb)>=0.01-1e-15)

    if h_scale and h_composition:
        verdict="MIXED_SCALE_COMPOSITION_REVERSAL_DEVELOPMENT"
    elif h_scale and not h_variance:
        verdict="TRAINING_SCALE_MEDIATED_HYBRID_COMPLEMENTARITY_DEVELOPMENT"
    elif h_variance and not h_scale:
        verdict="ESTIMATION_VARIANCE_DOMINANT_DEVELOPMENT"
    elif h_composition and not h_scale and not h_variance:
        verdict="COMPOSITION_MEDIATED_FRESH_REVERSAL_DEVELOPMENT"
    elif h_complementarity:
        verdict="LOCALIZED_COMPLEMENTARITY_WITH_UNRESOLVED_REVERSAL"
    else:
        verdict="REVERSAL_ATTRIBUTION_UNRESOLVED"

    report={
      "schema_version":"g7-p18-hybrid-reversal-attribution-1",
      "phase":"G7-P18",
      "development_only":True,
      "new_body_contact":0,
      "scale_learning_curve":scale,
      "scale_median_by_n":med,
      "full296_seed_means":full,
      "composition_reweighting":{"fresh_unweighted_hybrid_minus_hand":base,"by_stage_axis":comp},
      "complementarity_localization":{
        "raw_better_n":len(raw_better),"hand_better_n":len(hand_better),
        "mean_hand_minus_hybrid_when_raw_better":rb,
        "mean_hand_minus_hybrid_when_hand_better":hb,
        "difference":None if rb is None or hb is None else rb-hb
      },
      "rivals":{
        "H_SCALE":h_scale,"H_VARIANCE":h_variance,"H_COMPOSITION":h_composition,"H_COMPLEMENTARITY":h_complementarity
      },
      "verdict":verdict,
      "boundary":[
        "P17 fresh48 is development-only in P18 because the reversal hypothesis came from P17.",
        "No P18 fit is eligible for confirmation or deployment.",
        "Composition reweighting is descriptive and noncausal.",
        "Predictive complementarity is not cognitive mechanism evidence.",
        "No new body contact occurred."
      ]
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"hybrid-reversal-attribution.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P18_REVERSAL_ATTRIBUTION_PASS")
    print("SCALE_MEDIANS",json.dumps(med,sort_keys=True))
    print("FULL296_SEEDS",json.dumps(full))
    print("RIVALS",json.dumps(report["rivals"],sort_keys=True))
    print("COMPLEMENTARITY",json.dumps(report["complementarity_localization"],sort_keys=True))
    print("VERDICT",verdict)

if __name__=="__main__":main()
