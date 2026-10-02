#!/usr/bin/env python3
import argparse, hashlib, json, math, random, statistics
from collections import defaultdict

ACTIONS=["U","U2","U'","R","R2","R'","F","F2","F'","D","D2","D'","L","L2","L'","B","B2","B'"]

def median(xs):
    return statistics.median(xs) if xs else None

def load_jsonl(path):
    out=[]
    with open(path,encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet",required=True)
    ap.add_argument("--events",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--permutations",type=int,default=20000)
    args=ap.parse_args()

    packet=json.load(open(args.packet,encoding="utf-8"))
    trials={t["trial_id"]:t for t in packet["trials"]}
    events=load_jsonl(args.events)

    session_starts={e["session_id"]:e for e in events if e["event_type"]=="session_start"}
    choices=[e for e in events if e["event_type"]=="choice_committed"]
    completes=[e for e in events if e["event_type"]=="session_complete"]
    sessions=sorted(session_starts)

    rows=[]
    missing_choice=0
    for e in choices:
        t=trials.get(e["trial_id"])
        if not t:
            raise SystemExit("UNKNOWN_TRIAL")
        token=e.get("choice_token")
        if token not in ACTIONS:
            missing_choice+=1
            continue
        idx=ACTIONS.index(token)
        h1=idx in t["predictions"]["H1_PDB_GREEDY"]
        h3=idx in t["predictions"]["H3_PDB_LOOKAHEAD"]
        rows.append({
            "session_id":e["session_id"],"trial_id":e["trial_id"],"pair_id":t["pair_id"],
            "state_id":t["state_id"],"condition":t["condition"]["display_horizon_condition"],
            "latency_ms":float(e["latency_ms"]),"h1_match":int(h1),"h3_match":int(h3),
            "signed_agreement":int(h3)-int(h1)
        })

    expected=len(sessions)*len(packet["trials"])
    missing_expected=expected-len(choices)
    h1_rate=sum(r["h1_match"] for r in rows)/len(rows) if rows else None
    h3_rate=sum(r["h3_match"] for r in rows)/len(rows) if rows else None
    mean_signed=sum(r["signed_agreement"] for r in rows)/len(rows) if rows else None

    neutral=[r["latency_ms"] for r in rows if r["condition"]=="NEUTRAL"]
    deliberate=[r["latency_ms"] for r in rows if r["condition"]=="DELIBERATE"]
    latency_diff=(median(deliberate)-median(neutral)) if neutral and deliberate else None

    by_state=defaultdict(list)
    for r in rows: by_state[r["state_id"]].append(r["signed_agreement"])
    state_effects=[sum(v)/len(v) for _,v in sorted(by_state.items())]

    rng=random.Random(0xC0BE5A17)
    obs=abs(sum(state_effects)/len(state_effects)) if state_effects else 0.0
    extreme=0
    for _ in range(args.permutations):
        x=sum(v*(1 if rng.random()<0.5 else -1) for v in state_effects)/len(state_effects)
        if abs(x)>=obs-1e-15: extreme+=1
    p=(extreme+1)/(args.permutations+1)

    per_session={}
    for sid in sessions:
        sr=[r for r in rows if r["session_id"]==sid]
        n=[r["latency_ms"] for r in sr if r["condition"]=="NEUTRAL"]
        d=[r["latency_ms"] for r in sr if r["condition"]=="DELIBERATE"]
        per_session[sid]={
            "choices":len(sr),
            "h1_agreement_rate":sum(r["h1_match"] for r in sr)/len(sr) if sr else None,
            "h3_agreement_rate":sum(r["h3_match"] for r in sr)/len(sr) if sr else None,
            "median_latency_neutral_ms":median(n),
            "median_latency_deliberate_ms":median(d),
            "paired_median_latency_difference_ms":(median(d)-median(n)) if n and d else None
        }

    report={
        "schema_version":"g7-p5-analysis-1",
        "authority":"SYNTHETIC_VALIDATION_ONLY" if all(x.get("consent_status")=="SYNTHETIC_ONLY" for x in session_starts.values()) else "LIVE_DATA_PRESENT_REQUIRES_SEPARATE_AUTHORITY",
        "packet_sha256":packet["packet_sha256"],
        "sessions":len(sessions),
        "session_complete_events":len(completes),
        "expected_choices":expected,
        "observed_choice_events":len(choices),
        "valid_choice_rows":len(rows),
        "missing_expected_choice_events":missing_expected,
        "invalid_or_missing_choice_tokens":missing_choice,
        "primary":{
            "h1_agreement_rate":h1_rate,
            "h3_agreement_rate":h3_rate,
            "mean_signed_h3_minus_h1_agreement":mean_signed,
            "state_level_label_swap_permutation_p":p,
            "permutations":args.permutations
        },
        "latency":{
            "median_neutral_ms":median(neutral),
            "median_deliberate_ms":median(deliberate),
            "paired_median_difference_ms":latency_diff
        },
        "per_session":per_session,
        "interpretation_boundary":[
            "Agreement with a frozen representation is not evidence that the participant internally used that representation.",
            "Latency differences are behavioral readouts, not direct measures of lookahead.",
            "Synthetic validation cannot promote a human planning mechanism claim."
        ]
    }
    import os
    os.makedirs(args.out,exist_ok=True)
    with open(os.path.join(args.out,"analysis.json"),"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2,ensure_ascii=False);f.write("\n")
    with open(os.path.join(args.out,"analysis-receipt.md"),"w",encoding="utf-8") as f:
        f.write("# G7-P5 preregistered analysis receipt\n\n")
        f.write(f"- authority: {report['authority']}\n")
        f.write(f"- sessions: {report['sessions']}\n")
        f.write(f"- valid choices: {report['valid_choice_rows']}\n")
        f.write(f"- H1 agreement: {h1_rate:.6f}\n")
        f.write(f"- H3 agreement: {h3_rate:.6f}\n")
        f.write(f"- H3-H1 signed agreement: {mean_signed:.6f}\n")
        f.write(f"- state-level permutation p: {p:.6f}\n")
        f.write(f"- deliberate-neutral median latency: {latency_diff:.3f} ms\n")
    print("G7_P5_ANALYSIS_PASS")
    print("AUTHORITY\t"+report["authority"])
    print("SESSIONS\t"+str(len(sessions)))
    print("CHOICES\t"+str(len(rows)))
    print("H1_AGREEMENT\t"+str(h1_rate))
    print("H3_AGREEMENT\t"+str(h3_rate))
    print("PERMUTATION_P\t"+str(p))

if __name__=="__main__":
    main()
