#!/usr/bin/env python3
"""CUBE-REV 0.21 P7 — exact poset linear-extension and non-identification court.

Counts completions of documented *reported* event order, not unobserved human
cognitive sequences. No probability measure over actual human histories.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path

def count_extensions(n, parent_bits):
    full=(1<<n)-1
    @lru_cache(None)
    def f(done):
        if done==full:return 1
        return sum(f(done|(1<<i)) for i in range(n)
                   if not(done>>i&1) and parent_bits[i]&~done==0)
    return f(0)

def audit(graph_path, out):
    raw=Path(graph_path).read_bytes()
    graph=json.loads(raw)
    assert graph["schema"]=="cuberev-021-p6-fmc-partial-order-derived-v1"
    assert graph["author_reports_do_not_imply_total_order"]
    nodes=graph["nodes"]
    edges=graph["edges"]
    assert len(nodes)==41
    episode_map=defaultdict(list)
    for node in nodes:episode_map[node["episode_id"]].append(node)
    assert len(episode_map)==8
    cases={}
    total=1
    unordered_total=ordered_total=direct_total=0
    witness_pair_counts=0
    for case,case_nodes in sorted(episode_map.items()):
        n=len(case_nodes)
        ix={node["id"]:i for i,node in enumerate(case_nodes)}
        assert len(ix)==n
        pred=[0]*n
        legal_direct=[]
        for e in edges:
            if e["relation"]=="AUTHOR_REPORTED_BEFORE" and e["src"] in ix:
                assert e["dst"] in ix
                u,v=ix[e["src"]],ix[e["dst"]]
                assert u!=v and not(pred[v]>>u&1)
                pred[v]|=1<<u
                legal_direct.append((u,v))
        c=count_extensions(n,pred)
        assert c>0,"source-implied precedence contains cycle"
        # Independent closure implementation computes comparable pairs.
        reach=[0]*n
        for u,v in legal_direct:reach[u]|=1<<v
        for k in range(n):
            for i in range(n):
                if reach[i]>>k&1:reach[i]|=reach[k]
        assert all(not reach[i]>>i&1 for i in range(n))
        comparable=sum(1 for i in range(n) for j in range(i+1,n)
                       if reach[i]>>j&1 or reach[j]>>i&1)
        ambiguous=n*(n-1)//2-comparable
        # Every pair NOT reachable in either direction admits BOTH opposite
        # linear extensions; exact DP gives constructive non-identifiability.
        examples=[]
        for i in range(n):
            for j in range(i+1,n):
                if reach[i]>>j&1 or reach[j]>>i&1:continue
                p1=pred.copy();p1[j]|=1<<i
                p2=pred.copy();p2[i]|=1<<j
                c1=count_extensions(n,p1)
                c2=count_extensions(n,p2)
                assert c1>0 and c2>0
                assert c1+c2==c
                witness_pair_counts+=1
                if len(examples)<15:
                    examples.append({
                        "event_a":case_nodes[i]["event_id"],
                        "event_b":case_nodes[j]["event_id"],
                        "completions_with_a_before_b":c1,
                        "completions_with_b_before_a":c2,
                        "no_probability_over_real_human_behavior_inferred":True
                    })
        assert ambiguous==len(examples) or ambiguous>15
        assert graph["per_episode"][case]["temporally_comparable_pairs_via_author_report"]==comparable
        assert graph["per_episode"][case]["unordered_event_pairs"]==ambiguous
        cases[case]={
            "reported_events":n,
            "direct_reported_precedence":len(legal_direct),
            "reported_event_linear_extensions":c,
            "ambiguously_ordered_pairs":ambiguous,
            "comparable_pairs":comparable,
            "self_information_if_uniform_extension_chosen_bits":math.log2(c),
            "examples_of_two_sided_unidentified_event_order":examples
        }
        total*=c
        ordered_total+=comparable
        unordered_total+=ambiguous
        direct_total+=len(legal_direct)
    assert ordered_total==71 and unordered_total==34
    assert direct_total==27
    assert witness_pair_counts==34
    assert total==288000
    assert cases["WHEELER_SEFMC2026_A1"]["reported_event_linear_extensions"]==40
    assert cases["GUIDO_ARCHIVE_REWRITE_24"]["reported_event_linear_extensions"]==4
    assert cases["UTOMO_FMCWORLD2026_A3"]["reported_event_linear_extensions"]==30
    assert cases["WONG_DDDSINGAPORE2025_A3"]["reported_event_linear_extensions"]==60
    assert math.isclose(math.log2(total),18.1357092861044)
    receipt={
        "marker":"CUBE_REV_021_P7_EXACT_FMC_REPORTED_EVENT_POSET_COMPLETIONS_PASS",
        "scope":"documented source-qualified partial event orders only, no hidden human actions",
        "original_graph_sha256":sha256(raw).hexdigest(),
        "episodes":len(cases),
        "observed_reported_event_nodes":len(nodes),
        "direct_supported_before_edges":direct_total,
        "event_pairs_ordered_by_supported_precedence":ordered_total,
        "event_pairs_unordered_in_documentation":unordered_total,
        "unidentified_pair_opposite_order_witnesses":witness_pair_counts,
        "possible_total_order_completions_across_eight_independent_case_graphs":total,
        "log2_total_order_completions_bits":math.log2(total),
        "cases":cases,
        "epistemic_warrant":"288000 is a combinatorial count of completions consistent with authored reports, NOT a distribution over hidden actual FMC cognitive searches; 18.136 bits is completion-index description length, NOT human working memory."
    }
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(receipt["marker"])
    print(json.dumps({k:receipt[k] for k in [
        "episodes","event_pairs_unordered_in_documentation",
        "possible_total_order_completions_across_eight_independent_case_graphs",
        "log2_total_order_completions_bits"]},sort_keys=True))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--graph",required=True)
    p.add_argument("--output",required=True)
    x=p.parse_args()
    audit(x.graph,x.output)
if __name__=="__main__":main()
