#!/usr/bin/env python3
"""CUBE-REV 0.22 P4: exact source-constrained FMC process identifiability bounds.

The underlying P5/P6 records are *retrospective reported-event graphs*.
A linear extension is a possible ordering OF THE RECORDED NODE SET only.
Do not confuse it with an observed human process or assign a human probability.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from collections import defaultdict
from functools import lru_cache
from math import comb, log2
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BUILDER=ROOT/"scripts/cuberev-021/verify-p6-fmc-source-grounded-partial-order.py"
MATCHED=ROOT/"data/cuberev-022/p3_fmc_matched_scramble_author_evidence.json"
def import_builder():
    spec=importlib.util.spec_from_file_location("cuberev_021_p6_builder",BUILDER)
    mod=importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def count_extensions(n,arc_pairs):
    pred=[0]*n
    for i,j in arc_pairs:
        assert 0<=i<n and 0<=j<n and i!=j
        pred[j]|=1<<i
    @lru_cache(None)
    def f(done):
        if done==(1<<n)-1:return 1
        total=0
        for j in range(n):
            if not done&(1<<j) and not pred[j]&~done:
                total+=f(done|(1<<j))
        return total
    return f(0)
def closure(n,arcs):
    r=[0]*n
    for i,j in arcs:r[i]|=1<<j
    for k in range(n):
        for i in range(n):
            if r[i]&(1<<k):r[i]|=r[k]
    assert all(not (r[i]>>i)&1 for i in range(n))
    return r
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    x=p.parse_args()
    builder=import_builder()
    graph,old_receipt=builder.audit()
    assert graph["schema"]=="cuberev-021-p6-fmc-partial-order-derived-v1"
    assert graph["author_reports_do_not_imply_total_order"]
    assert old_receipt["episodes"]==8 and old_receipt["reported_event_nodes"]==41
    nodes_by=defaultdict(list)
    edges_by=defaultdict(list)
    for item in graph["nodes"]:nodes_by[item["episode_id"]].append(item)
    for e in graph["edges"]:
        if e["relation"]=="AUTHOR_REPORTED_BEFORE":
            c=e["src"].split("::")[0]
            assert e["dst"].split("::")[0]==c
            edges_by[c].append(e)
    assert len(nodes_by)==8 and sum(map(len,nodes_by.values()))==41
    cases={}
    all_ambiguities=[]
    edge_ablations=[]
    total_original=1
    pair_total=0
    direct_total=0
    for case in sorted(nodes_by):
        nodes=nodes_by[case]
        idx={it["id"]:i for i,it in enumerate(nodes)}
        n=len(nodes)
        arcs=[(idx[e["src"]],idx[e["dst"]]) for e in edges_by[case]]
        L=count_extensions(n,arcs)
        assert L>=1
        reach=closure(n,arcs)
        possible=comb(n,2)
        ambiguities=[]
        for a in range(n):
            for b in range(a+1,n):
                if reach[a]>>b&1 or reach[b]>>a&1:continue
                L_ab=count_extensions(n,arcs+[(a,b)])
                L_ba=count_extensions(n,arcs+[(b,a)])
                assert L_ab>=1 and L_ba>=1
                assert L_ab+L_ba==L
                bound=max(L_ab,L_ba)
                record={
                    "case":case,
                    "first_reported_event_id":nodes[a]["event_id"],
                    "second_reported_event_id":nodes[b]["event_id"],
                    "completions_if_first_precedes_second":L_ab,
                    "completions_if_second_precedes_first":L_ba,
                    "worst_remaining_with_one_true_binary_order_fact":bound,
                    "best_case_eliminated_with_one_true_binary_order_fact":L-min(L_ab,L_ba),
                    "worst_case_eliminated_with_one_true_binary_order_fact":min(L_ab,L_ba),
                    "human_order_probability_unidentified":True
                }
                ambiguities.append(record);all_ambiguities.append(record)
        ordered=possible-len(ambiguities)
        assert ordered==graph["per_episode"][case]["temporally_comparable_pairs_via_author_report"]
        assert len(ambiguities)==graph["per_episode"][case]["unordered_event_pairs"]
        if ambiguities:
            best=min(ambiguities,key=lambda r:(r["worst_remaining_with_one_true_binary_order_fact"],
                -r["worst_case_eliminated_with_one_true_binary_order_fact"],
                r["first_reported_event_id"],r["second_reported_event_id"]))
        else:best=None
        for i,e in enumerate(edges_by[case]):
            rest=arcs[:i]+arcs[i+1:]
            leave=count_extensions(n,rest)
            assert leave>=L
            edge_ablations.append({
                "case":case,"before":e["src"].split("::")[-1],"after":e["dst"].split("::")[-1],
                "warrant":e["reason"],"base_completions":L,
                "completions_without_this_single_curated_temporal_edge":leave,
                "additional_completions_on_edge_withdrawal":leave-L,
                "inflation_ratio_vs_case_base":leave/L,
                "transitively_redundant_under_other_curated_edges":leave==L,
                "edge_grade":"CURATOR_ASSERTED_EXPLICIT_AUTHOR_PRECEDENCE; not a recording"
            })
        cases[case]={
            "reported_events":n,"curated_direct_precedence":len(arcs),
            "case_linear_extensions":L,"known_relative_order_pairs":ordered,
            "unidentified_relative_order_pairs":len(ambiguities),
            "one_order_fact_maximin_selection":best,
            "ambiguous_order_queries_count":len(ambiguities),
            "not_full_hidden_search":True
        }
        total_original*=L
        pair_total+=possible
        direct_total+=len(arcs)
    assert total_original==288000
    assert pair_total==105
    assert len(all_ambiguities)==34
    assert direct_total==27
    for a in all_ambiguities:
        C=cases[a["case"]]["case_linear_extensions"]
        a["total_8_case_completions_if_first_precedes_second"]=total_original//C*a["completions_if_first_precedes_second"]
        a["total_8_case_completions_if_second_precedes_first"]=total_original//C*a["completions_if_second_precedes_first"]
        a["global_worst_remaining_completions"]=max(
            a["total_8_case_completions_if_first_precedes_second"],
            a["total_8_case_completions_if_second_precedes_first"]
        )
        assert (a["total_8_case_completions_if_first_precedes_second"]
                +a["total_8_case_completions_if_second_precedes_first"]==total_original)
    optimal_question=min(all_ambiguities,key=lambda r:(r["global_worst_remaining_completions"],
        r["case"],r["first_reported_event_id"],r["second_reported_event_id"]))
    assert total_original-optimal_question["global_worst_remaining_completions"]>0
    # NEW 0.22-P4 PROCESS-DOMAIN CORRECTION:
    # Guido g04 is another author's later *documentary annotation*, not a
    # cognitive decision by the original FMC solver. Historical P7's 288000
    # count includes its source-document placement; preserve 288000 as
    # a source-MIXED document-poset count, NOT a searcher-only count.
    solver_cases={}
    solver_ambiguities=[]
    solver_event_total=0
    solver_pair_total=0
    solver_ordered_total=0
    solver_product=1
    omitted_documentary=[]
    for case in sorted(nodes_by):
        original=nodes_by[case]
        kept=[n for n in original if n["reported_event_kind"]!="OTHER_AUTHOR_POSTHOC_NOTE"]
        dropped=[n for n in original if n["reported_event_kind"]=="OTHER_AUTHOR_POSTHOC_NOTE"]
        omitted_documentary.extend({"case":case,"event_id":n["event_id"],
          "reason":"separate author's later documentary improvement; not original solver cognition"} for n in dropped)
        idx={z["id"]:i for i,z in enumerate(kept)}
        n=len(kept)
        arcs=[(idx[e["src"]],idx[e["dst"]]) for e in edges_by[case]
              if e["src"] in idx and e["dst"] in idx]
        L=count_extensions(n,arcs)
        assert L>0
        reach=closure(n,arcs)
        events=0
        for a in range(n):
            for b in range(a+1,n):
                if reach[a]>>b&1 or reach[b]>>a&1:continue
                up=count_extensions(n,arcs+[(a,b)])
                dn=count_extensions(n,arcs+[(b,a)])
                assert up>0 and dn>0 and up+dn==L
                solver_ambiguities.append({
                  "case":case,
                  "first_solver_event":kept[a]["event_id"],
                  "second_solver_event":kept[b]["event_id"],
                  "solver_case_completions":L,
                  "first_before_second":up,
                  "second_before_first":dn,
                  "maximum_surviving_case_orders_after_true_binary_report":max(up,dn),
                  "not_a_human_posterior_probability":True
                })
                events+=1
        solver_product*=L
        solver_event_total+=n
        solver_pair_total+=comb(n,2)
        solver_ordered_total+=comb(n,2)-events
        solver_cases[case]={"original_author_reported_events":n,
            "completions_without_other_author_posthoc_nodes":L,
            "ambiguous_relative_order_pairs":events,
            "comparable_pairs":comb(n,2)-events}
    assert len(omitted_documentary)==1
    assert omitted_documentary[0]["event_id"]=="g04"
    assert solver_event_total==40
    assert solver_pair_total==102
    assert solver_ordered_total==71
    assert len(solver_ambiguities)==31
    assert solver_product==72000
    for record in solver_ambiguities:
        L=record["solver_case_completions"]
        factor=solver_product//L
        record["global_first_before_second"]=factor*record["first_before_second"]
        record["global_second_before_first"]=factor*record["second_before_first"]
        record["global_minimax_worst_remaining"]=factor*record["maximum_surviving_case_orders_after_true_binary_report"]
        assert record["global_first_before_second"]+record["global_second_before_first"]==solver_product
    best_solver_only=min(solver_ambiguities,key=lambda a:(
       a["global_minimax_worst_remaining"],a["case"],a["first_solver_event"],a["second_solver_event"]))
    essential=[e for e in edge_ablations if not e["transitively_redundant_under_other_curated_edges"]]
    redundant=[e for e in edge_ablations if e["transitively_redundant_under_other_curated_edges"]]
    worst_edge=max(edge_ablations,key=lambda e:(e["inflation_ratio_vs_case_base"],e["case"]))
    matched=json.loads(MATCHED.read_text())
    assert matched["schema"]=="cuberev-022-p3-fmc-matched-scramble-retrospective-v1"
    people=matched["competitors"]
    assert len(people)==2
    Y=next(p for p in people if p["id"]=="2018RIAB01")
    M=next(p for p in people if p["id"]=="2014MIAO02")
    assert len(Y["attempts"])==len(M["attempts"])==3
    a3=Y["attempts"][2]
    assert a3["written_EO_candidates_about"]==70
    assert a3["checked_EO_candidates_about"]==30
    assert [a["solution_htm"] for a in Y["attempts"]]==[19,19,23]
    assert [a["solution_htm"] for a in M["attempts"]]==[19,19,23]
    for a,b in zip(Y["attempts"],M["attempts"]):
        assert a["attempt"]==b["attempt"]
        assert a["official_scramble"]==b["official_scramble"]
    def frechet_bounds_written_tested(W,E):
        # |written∩tested| between 0 and min(W,E) when universe unrestricted,
        # |written\tested| lies between max(0,W-E) and W.
        # This is conditional on TRUE cardinalities W,E being fixed; reported
        # '~70/~30' does NOT fix them as exact. If both are exact, min 40.
        return {"written":W,"actually_evaluated":E,
            "tested_and_written_overlap_lower":0,
            "tested_and_written_overlap_upper":min(W,E),
            "written_but_not_tested_lower":max(0,W-E),
            "written_but_not_tested_upper":W,
            "written_not_tested_fraction_lower":max(0,W-E)/W if W else None,
            "tested_of_written_fraction_upper":min(W,E)/W if W else None}
    exact_scenario=frechet_bounds_written_tested(70,30)
    assert exact_scenario["written_but_not_tested_lower"]==40
    assert exact_scenario["tested_of_written_fraction_upper"]==3/7
    hypothetical_error=[{"hypothetical_symmetric_uncertainty_margin":delta,
       "smallest_guaranteed_written_not_tested_if_counts_within_window":
       max(0,(70-delta)-(30+delta)),
       "largest_possible_fraction_tested_of_written_under_window":
       min(1,(30+delta)/(70-delta))}
      for delta in [0,5,10,15,20]]
    assert [x["smallest_guaranteed_written_not_tested_if_counts_within_window"] for x in hypothetical_error]==[40,30,20,10,0]
    source_grade={
       "distinct_published_competitor_authors":2,
       "same_scrambles_and_same_endpoint_htm_for_each_attempt":3,
       "nested_attempts_total":6,
       "NOT_independent_subject_count":6,
       "author_retrospective_reported_approximate_counts":{"W_about":70,"E_about":30},
       "conditional_if_cardinalities_exact_70_and_30":exact_scenario,
       "hypothetical_error_margin_sensitivity_NOT_estimated_measurement_error":hypothetical_error,
       "upper_bound_on_evaluation_coverage_of_ALL_PHYSICALLY_FEASIBLE_CANDIDATES":None,
       "reason_no_population_process_rate":"Author-reported approximate counts, overlapping written/tested sets not exhaustively enumerated, and feasible candidate universe has no audited finite denominator.",
       "Miao_attempt3_candidate_count":"UNKNOWN_NOT_ZERO",
       "not_novel_empirical_recruitment":True,
       "new_matched_score_is_NOT_identification_of_same_internal_process":True
    }
    receipt={
        "marker":"CUBE_REV_022_P4_EXACT_FMC_PARTIAL_ORDER_PROCESS_IDENTIFIABILITY_PASS",
        "source_inputs_sha256":{
          "P5":sha(ROOT/"data/cuberev-021/p5_fmc_existing_search_event_seed.json"),
          "P6":sha(ROOT/"data/cuberev-021/p6_fmc_partial_order_extension.json"),
          "P3_matched":sha(MATCHED)
        },
        "data_frozen":"Eight hand-curated retrospective attempt/work-note DAGs + separate two-author three-matched-scramble ledger",
        "p6_original_reported_events":len(graph["nodes"]),
        "p6_original_curator_asserted_temporal_edges":direct_total,
        "within_case_recorded_event_pairs":pair_total,
        "known_comparable_recorded_event_pairs":pair_total-len(all_ambiguities),
        "unidentified_relative_order_pairs":len(all_ambiguities),
        "linear_extensions_product_not_real_human_histories":total_original,
        "global_one_extra_supported_binary_order_fact_minimax_query":optimal_question,
        "critical_no_other_author_cognitive_conflation_correction":{
           "historical_mixed_documentary_poset_completions":total_original,
           "reported_original_solver_event_nodes":solver_event_total,
           "excluded_separately_authored_posthoc_event_nodes":omitted_documentary,
           "within_solver_episode_node_pairs":solver_pair_total,
           "solver_reported_temporal_comparable_pairs":solver_ordered_total,
           "solver_reported_temporal_ambiguous_pairs":len(solver_ambiguities),
           "original_solver_only_poset_completions":solver_product,
           "best_single_same_solver_order_question_by_minimax_remaining_order_count":best_solver_only,
           "all_31_same_solver_binary_order_splits":solver_ambiguities,
           "per_episode":solver_cases,
           "do_not_report_288000_as_one_person_search_process":True,
           "old_288000_correct_as_mixed_documentary_node_count_only":True
        },
        "all_34_ambiguous_pairs_with_opposite_order_extension_counts":all_ambiguities,
        "case_exact_bounds":cases,
        "curated_edge_withdrawal_sensitivity":{
          "all_direct_precedence_edges":len(edge_ablations),
          "essential_to_reported_event_extension_count":len(essential),
          "already_transitively_implied_under_remaining_warrants":len(redundant),
          "max_effect_single_edge_withdrawal":worst_edge,
          "per_edge":edge_ablations
        },
        "matched_FMC_branch_coverage_partial_identification":source_grade,
        "identifiability_theorems":[
          "Each incomparable pair of recorded events has at least two source-compatible relative orders, explicitly counted. This is about curator-warranted source DAGs, not hidden cognitive truth.",
          "A single additional true binary order fact divides finite compatible complete orders into two disjoint sets. Minimax reduction is exact with no prior probabilities over actual human chronology.",
          "Deleting a single source-curated precedence edge weakens constraints and can only weakly increase compatible full orders. Reported inflation quantifies reliance on that warrant, not its probability of being wrong.",
          "With fixed exact written count W and tested count E, arbitrary overlap obeys max(0,W-E)<=|W\\E|<=W; reported approximate counts do not imply exact cardinality or population-level effect.",
          "Equal official scrambles and official HTM endpoints do not identify the hidden search paths, candidate evaluation sets or psychological parameters without a specified observational bridge."
        ],
        "strict_evidence_limits":{
          "no_constructed_hidden_human_event_timeline":True,
          "no_probabilistic_prior_over_linear_extensions":True,
          "no_negative_evidence_from_missing_candidate_checks":True,
          "reported_EO_counts_not_sensor_counts":True,
          "no_videos_or_new_participants":True,
          "no_measured_human_cognitive_cost":True,
          "source_conditioned_not_full_external_web_reverification":True
        }
    }
    target=Path(x.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(receipt["marker"])
    print(json.dumps({"completions":total_original,"best_order_query":optimal_question,
      "essential_edges":len(essential),"redundant_edges":len(redundant),
      "worst_edge":worst_edge,"conditional_70_30":exact_scenario,
      "sensitivity":hypothetical_error},ensure_ascii=False))
if __name__=="__main__":main()
