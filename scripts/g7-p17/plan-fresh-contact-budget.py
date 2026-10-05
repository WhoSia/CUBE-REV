#!/usr/bin/env python3
import argparse,csv,hashlib,json,math,pathlib,random
from collections import Counter,defaultdict

ACTIONS=18; RAW_TOKENS=256; HAND_TOKENS=141
RANK=8; EPOCHS=30; LR=.06; L2=.0001
STAGES=("P11","P13","P14","P15")
RAW_SEED="CUBE_REV_G7_P16_R1_LATENT_POLICY_V1"
HAND_SEED="CUBE_REV_G7_P16_R3_HANDCRAFTED_V1"
BOOT_SEED="CUBE_REV_G7_P17_P0_BOOTSTRAP_V1"

def S(x): return {int(v) for v in (x or "").split(",") if v!=""}
def seed_int(s): return int(hashlib.sha256(s.encode()).hexdigest()[:16],16)
def vec(s,n):
    x=[int(v) for v in s.split(",")]
    if len(x)!=n: raise ValueError((n,len(x)))
    return x
def raw_tokens(r):
    cp=vec(r["cp"],8);co=vec(r["co"],8);ep=vec(r["ep"],12);eo=vec(r["eo"],12)
    t=[p*8+v for p,v in enumerate(cp)]
    t += [64+p*3+v for p,v in enumerate(co)]
    t += [88+p*12+v for p,v in enumerate(ep)]
    t += [232+p*2+v for p,v in enumerate(eo)]
    return t
def hand_tokens(f,s):
    t=[]
    for i,k in enumerate(("h1_best","h2_best","h3_best","fs_best","ts_best")):
        for a in S(f[k]):t.append(i*18+a)
    for a in S(s["desc_actions"]):t.append(90+a)
    t.append(108+int(s["phase1_lb"]))
    if int(s["is_g1"]):t.append(140)
    return t
def init(tc,seed):
    g=random.Random(seed);sc=.02
    E=[[g.uniform(-sc,sc) for _ in range(RANK)] for _ in range(tc)]
    U=[[g.uniform(-sc,sc) for _ in range(RANK)] for _ in range(ACTIONS)]
    return E,U,[0.0]*ACTIONS
def probs(model,tt):
    E,U,b=model;inv=1/len(tt)
    z=[sum(E[t][j] for t in tt)*inv for j in range(RANK)]
    ss=[b[a]+sum(U[a][j]*z[j] for j in range(RANK)) for a in range(ACTIONS)]
    mx=max(ss);ex=[math.exp(x-mx) for x in ss];den=sum(ex)
    return [x/den for x in ex],z
def train(rows,tc,seed):
    E,U,b=init(tc,seed);g=random.Random(seed^0x9E3779B97F4A7C15);order=list(range(len(rows)))
    for ep in range(EPOCHS):
        g.shuffle(order);eta=LR/(1+.06*ep)
        for ii in order:
            r=rows[ii];p,z=probs((E,U,b),r["tokens"]);y=r["y"]
            gr=[p[a]-(1 if a==y else 0) for a in range(ACTIONS)]
            dz=[sum(gr[a]*U[a][j] for a in range(ACTIONS)) for j in range(RANK)]
            for a in range(ACTIONS):
                ga=gr[a];b[a]-=eta*ga
                for j in range(RANK):U[a][j]-=eta*(ga*z[j]+L2*U[a][j])
            inv=1/len(r["tokens"])
            for t in r["tokens"]:
                for j in range(RANK):E[t][j]-=eta*(dz[j]*inv+L2*E[t][j])
    return E,U,b
def nll(model,r):
    p,_=probs(model,r["tokens"]);return -math.log(max(p[r["y"]],1e-15))
def prior_probs(rows):
    c=Counter(r["y"] for r in rows);den=len(rows)+ACTIONS
    return [(c[a]+1)/den for a in range(ACTIONS)]
def quotas(n,counts):
    tot=sum(counts.values());raw={s:n*counts[s]/tot for s in STAGES}
    q={s:int(math.floor(raw[s])) for s in STAGES}
    rem=n-sum(q.values())
    for s in sorted(STAGES,key=lambda z:(-(raw[z]-q[z]),STAGES.index(z)))[:rem]:q[s]+=1
    return q
def pct(xs,p):
    y=sorted(xs)
    k=min(len(y)-1,max(0,int(math.ceil(p*len(y))-1)))
    return y[k]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--states",required=True);ap.add_argument("--features",required=True);ap.add_argument("--shell",required=True)
    ap.add_argument("--context",required=True);ap.add_argument("--preseal",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args()
    pre=json.load(open(a.preseal))
    if pre["status"]!="FROZEN_BEFORE_P17_FRESH_SELECTION_OR_BODY_CONTACT":raise SystemExit("PRESEAL")

    ctx={}
    for line in open(a.context):
        if line.strip():
            x=json.loads(line);ctx[(int(x["source_id"]),int(x["prefix_index"]))]=x
    states={}
    with open(a.states,newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):states[(int(x["source_id"]),int(x["prefix_index"]))]=x
    shell={}
    with open(a.shell,newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):shell[(int(x["source_id"]),int(x["prefix_index"]))]=x

    raw=[];hand=[];solves={}
    with open(a.features,newline="") as f:
        for x in csv.DictReader(f,delimiter="\t"):
            sid=int(x["source_id"]);pi=int(x["prefix_index"]);y=int(x["next_action"])
            if y<0:continue
            stage=ctx[(sid,pi)].get("development_stage")
            if stage not in STAGES:raise SystemExit("STAGE")
            key=(sid,pi)
            raw.append({"sid":sid,"stage":stage,"y":y,"tokens":raw_tokens(states[key])})
            hand.append({"sid":sid,"stage":stage,"y":y,"tokens":hand_tokens(x,shell[key])})
            solves[sid]=stage
    if len(solves)!=296:raise SystemExit("DEV296")
    stage_counts=Counter(solves.values())

    solve_margin={};stage_summary={}
    for stage in STAGES:
        rtr=[r for r in raw if r["stage"]!=stage];rva=[r for r in raw if r["stage"]==stage]
        htr=[r for r in hand if r["stage"]!=stage];hva=[r for r in hand if r["stage"]==stage]
        rm=train(rtr,RAW_TOKENS,seed_int(f"{RAW_SEED}|R2|hold={stage}"))
        hm=train(htr,HAND_TOKENS,seed_int(f"{HAND_SEED}|hold={stage}"))
        pp=prior_probs(htr)
        rr=defaultdict(list);hh=defaultdict(list);pr=defaultdict(list)
        for r in rva:rr[r["sid"]].append(nll(rm,r))
        for r in hva:
            hh[r["sid"]].append(nll(hm,r));pr[r["sid"]].append(-math.log(pp[r["y"]]))
        vals=[]
        for sid in sorted(rr):
            hand_n=sum(hh[sid])/len(hh[sid]);raw_n=sum(rr[sid])/len(rr[sid]);prior_n=sum(pr[sid])/len(pr[sid])
            rec={"sid":sid,"stage":stage,"states":len(hh[sid]),"hand_minus_raw":hand_n-raw_n,"hand_minus_prior":hand_n-prior_n}
            solve_margin[sid]=rec;vals.append(rec)
        stage_summary[stage]={
          "solves":len(vals),
          "mean_hand_minus_raw":sum(v["hand_minus_raw"] for v in vals)/len(vals),
          "mean_hand_minus_prior":sum(v["hand_minus_prior"] for v in vals)/len(vals),
          "mean_states_per_solve":sum(v["states"] for v in vals)/len(vals)
        }

    bystage={s:[v for v in solve_margin.values() if v["stage"]==s] for s in STAGES}
    rng=random.Random(seed_int(BOOT_SEED));planning={}
    reps=int(pre["planning_evidence"]["repetitions"])
    for n in pre["candidate_sizes"]:
        q=quotas(n,stage_counts);means=[]
        for _ in range(reps):
            draw=[]
            for s in STAGES:
                pool=bystage[s]
                draw += [pool[rng.randrange(len(pool))] for _ in range(q[s])]
            means.append(sum(v["hand_minus_raw"] for v in draw)/len(draw))
        planning[str(n)]={
          "stage_quotas":q,
          "bootstrap_mean":sum(means)/len(means),
          "bootstrap_p05":pct(means,.05),
          "bootstrap_p95":pct(means,.95),
          "assurance_pass":pct(means,.95)<0
        }
    selected=None
    for n in pre["candidate_sizes"]:
        if planning[str(n)]["assurance_pass"]:
            selected=n;break
    verdict="ASSURANCE_REACHED" if selected else "ASSURANCE_NOT_REACHED_AT_CEILING"
    if selected is None:selected=max(pre["candidate_sizes"])

    allv=list(solve_margin.values())
    report={
      "schema_version":"g7-p17-p0-contact-budget-1",
      "operation_type":"Pre-Contact Fresh-Sample Budget Planning Audit",
      "development_only":True,"fresh_contact":0,
      "dev296":{"solves":296,"states":len(hand),"stage_counts":dict(stage_counts),
                "mean_states_per_solve":sum(v["states"] for v in allv)/len(allv)},
      "stage_summary":stage_summary,
      "candidate_planning":planning,
      "selected_fresh_solves":selected,
      "selected_per_16cell":selected//16,
      "verdict":verdict,
      "boundary":["Development bootstrap is a contact-budget planning device, not fresh inferential evidence.",
                  "No P17 body data were used.","Frozen representation family and rank are unchanged."]
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"contact-budget-planning.json").write_text(json.dumps(report,indent=2)+"\n")
    print("G7_P17_P0_CONTACT_BUDGET_PASS")
    print("STAGES",json.dumps(stage_summary,sort_keys=True))
    print("PLANNING",json.dumps(planning,sort_keys=True))
    print("SELECTED",selected)
    print("VERDICT",verdict)
if __name__=="__main__":main()
