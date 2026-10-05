#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,random
from collections import defaultdict

BOOT_SEED="CUBE_REV_G7_P19_P0_HYBRID_HAND_BOOTSTRAP_V1"

def mean(xs): return sum(xs)/len(xs) if xs else None
def pct(xs,p):
    y=sorted(xs)
    if not y:return None
    k=min(len(y)-1,max(0,int((p*len(y)+0.999999999999)-1)))
    return y[k]
def seed_int(s): return int(hashlib.sha256(s.encode()).hexdigest()[:16],16)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--p17-report",required=True)
    ap.add_argument("--preseal",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    pre=json.load(open(a.preseal,encoding="utf-8"))
    if pre.get("status")!="FROZEN_BEFORE_P19_FRESH_SELECTION_OR_BODY_CONTACT":
        raise SystemExit("PRESEAL_NOT_FROZEN")
    rep=json.load(open(a.p17_report,encoding="utf-8"))
    if rep.get("solves")!=48 or rep.get("verdict")!="DIRECTION_ONLY":
        raise SystemExit("P17_REPORT_AUTHORITY")
    rows=rep.get("per_solve") or []
    if len(rows)!=48:raise SystemExit("P17_PER_SOLVE_48_REQUIRED")

    bycell=defaultdict(list)
    normalized=[]
    for r in rows:
        cell=r.get("sampling_cell")
        if not cell:raise SystemExit("MISSING_CELL")
        margin=float(r["hybrid_nll"])-float(r["hand_nll"])
        x={
          "source_id":int(r["source_id"]),
          "margin_hybrid_minus_hand":margin,
          "method_family":r.get("method_family"),
          "reconstructor_frequency_band":r.get("reconstructor_frequency_band"),
          "selection_era":r.get("selection_era"),
          "sampling_cell":cell,
          "states":int(r.get("states") or 0)
        }
        bycell[cell].append(x);normalized.append(x)

    if len(bycell)!=16:raise SystemExit(f"CELL16_REQUIRED_{len(bycell)}")
    if any(len(v)!=3 for v in bycell.values()):raise SystemExit("CELL3_REQUIRED")

    rng=random.Random(seed_int(BOOT_SEED))
    reps=int(pre["planning_evidence"]["repetitions"])
    planning={}
    for n in pre["candidate_sizes"]:
        if n%16:raise SystemExit("N_NOT_DIV16")
        k=n//16
        means=[]
        for _ in range(reps):
            draw=[]
            for cell in sorted(bycell):
                pool=bycell[cell]
                draw.extend(pool[rng.randrange(len(pool))]["margin_hybrid_minus_hand"] for __ in range(k))
            means.append(mean(draw))
        p05=pct(means,.05);p95=pct(means,.95);bm=mean(means)
        planning[str(n)]={
          "per_cell":k,
          "bootstrap_mean":bm,
          "bootstrap_p05":p05,
          "bootstrap_p95":p95,
          "assurance_pass":p95<0
        }

    selected=None
    for n in pre["candidate_sizes"]:
        if planning[str(n)]["assurance_pass"]:
            selected=n;break
    verdict="ASSURANCE_REACHED" if selected is not None else "ASSURANCE_NOT_REACHED_AT_CEILING"
    if selected is None:selected=max(pre["candidate_sizes"])

    cell_summary={c:{
      "n":len(v),
      "mean_hybrid_minus_hand":mean([x["margin_hybrid_minus_hand"] for x in v])
    } for c,v in sorted(bycell.items())}

    def group(axis):
        g=defaultdict(list)
        for x in normalized:g[str(x.get(axis))].append(x["margin_hybrid_minus_hand"])
        return {k:{"n":len(v),"mean_hybrid_minus_hand":mean(v)} for k,v in sorted(g.items())}

    report={
      "schema_version":"g7-p19-p0-contact-budget-1",
      "operation_type":"Pre-Contact Fresh-Sample Budget Planning Audit",
      "development_only":True,
      "new_body_contact":0,
      "source_report":{
        "p17_solves":48,
        "observed_mean_hybrid_minus_hand":mean([x["margin_hybrid_minus_hand"] for x in normalized]),
        "mean_states_per_solve":mean([x["states"] for x in normalized])
      },
      "cell_summary":cell_summary,
      "marginals":{
        "method_family":group("method_family"),
        "reconstructor_frequency_band":group("reconstructor_frequency_band"),
        "selection_era":group("selection_era")
      },
      "candidate_planning":planning,
      "selected_fresh_solves":selected,
      "selected_per_16cell":selected//16,
      "verdict":verdict,
      "boundary":[
        "P17 fresh48 is development-only for the HYBRID complementarity hypothesis.",
        "No P19 body data are used.",
        "Frozen HAND/HYBRID model bytes are not retrained or altered.",
        "Bootstrap assurance selects contact budget only and is not confirmation evidence."
      ]
    }
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"contact-budget-planning.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G7_P19_P0_CONTACT_BUDGET_PASS")
    print("OBSERVED_MEAN",report["source_report"]["observed_mean_hybrid_minus_hand"])
    print("PLANNING",json.dumps(planning,sort_keys=True))
    print("SELECTED",selected)
    print("VERDICT",verdict)

if __name__=="__main__":main()
