#!/usr/bin/env python3
import argparse, json, math, random, statistics

def one_run(n_participants, delta, states, rng):
    # Calibration model only:
    # P(+1)=0.25+delta/2, P(-1)=0.25-delta/2, P(0)=0.5
    # where +1 means H3-only agreement and -1 means H1-only agreement.
    state_means=[]
    for _ in range(states):
        s=0
        for _ in range(n_participants):
            u=rng.random()
            p_plus=0.25+delta/2
            p_minus=0.25-delta/2
            if u<p_plus: s+=1
            elif u<p_plus+p_minus: s-=1
        state_means.append(s/n_participants)
    if len(state_means)<2: return False
    m=statistics.mean(state_means)
    sd=statistics.stdev(state_means)
    if sd==0: return False
    # Fixed normal approximation threshold used only for design sensitivity,
    # not for final confirmatory inference.
    z=abs(m)/(sd/math.sqrt(states))
    return z>=1.96

def estimate(n, delta, states, reps, seed):
    rng=random.Random(seed ^ (n<<16) ^ int(delta*10000))
    return sum(one_run(n,delta,states,rng) for _ in range(reps))/reps

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    ap.add_argument("--reps",type=int,default=5000)
    args=ap.parse_args()
    ns=[12,16,20,24,30,40]
    deltas=[0.05,0.10,0.15,0.20]
    rows=[]
    for n in ns:
        for d in deltas:
            rows.append({"complete_sessions":n,"signed_agreement_delta":d,
                         "sensitivity":estimate(n,d,24,args.reps,0xC0BE5A17)})
    target=next(r for r in rows if r["complete_sessions"]==24 and r["signed_agreement_delta"]==0.10)
    report={
      "schema_version":"g7-p5-sensitivity-1",
      "authority":"DESIGN_CALIBRATION_ONLY",
      "states_per_session":24,
      "simulation_reps":args.reps,
      "model":{
        "signed_outcome_values":[-1,0,1],
        "p_zero":0.5,
        "p_plus":"0.25 + delta/2",
        "p_minus":"0.25 - delta/2",
        "note":"illustrative sensitivity model; not an empirical effect-size prior"
      },
      "table":rows,
      "frozen_complete_session_target":24,
      "reference_cell":{"delta":0.10,"estimated_sensitivity":target["sensitivity"]},
      "stopping_rule":"stop recruitment when 24 valid complete sessions are obtained; do not inspect outcome direction for stopping"
    }
    with open(args.out,"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2);f.write("\n")
    print("G7_P5_SENSITIVITY_PASS")
    print("TARGET_SESSIONS\t24")
    print("DELTA_010_SENSITIVITY\t"+str(target["sensitivity"]))

if __name__=="__main__":
    main()
