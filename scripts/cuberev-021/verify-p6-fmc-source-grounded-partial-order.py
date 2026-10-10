#!/usr/bin/env python3
"""CUBE-REV 0.21 P6: strictly evidence-graded FMC search *partial order*.

Never infer chronological order from the source's narrative index alone.
Retrospective notes ≠ observed cognitive operation; possible options ≠ evaluated branches.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P5 = ROOT / "data/cuberev-021/p5_fmc_existing_search_event_seed.json"
P6 = ROOT / "data/cuberev-021/p6_fmc_partial_order_extension.json"

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def audit():
    old_bytes, new_bytes = P5.read_bytes(), P6.read_bytes()
    old, supplement = json.loads(old_bytes), json.loads(new_bytes)
    assert old["schema"] == "cuberev-021-p5-fmc-retrospective-process-v1"
    assert supplement["schema"] == "cuberev-021-p6-source-qualified-partial-order-v1"
    assert all(supplement["explicit_controls"].values())  # strings are nonempty
    assert len(old["episodes"]) == 6 and len(supplement["added_public_episodes"]) == 2
    episodes = old["episodes"] + supplement["added_public_episodes"]
    assert len(episodes) == 8
    indexed = {e["id"]: e for e in episodes}
    assert len(indexed) == 8
    assert len({e["author"] for e in episodes}) == 7
    assert "UTOMO_FMCWORLD2026_A3" in indexed
    assert "WONG_DDDSINGAPORE2025_A3" in indexed
    assert "24" in indexed["UTOMO_FMCWORLD2026_A3"]["events"][-1]["author_paraphrase_ko"]
    assert "Attempt 3" in indexed["UTOMO_FMCWORLD2026_A3"]["attempt"]
    assert "Attempt 3" in indexed["WONG_DDDSINGAPORE2025_A3"]["attempt"]
    w = indexed["WONG_DDDSINGAPORE2025_A3"]
    assert w["author_linked_video"] == "https://www.youtube.com/watch?v=ftj2Mh0dEpw"
    assert w["video_evidence_grade"] == "URL_IN_AUTHOR_RECONSTRUCTION__NOT_FRAME_REVIEWED"

    by_case = {row["episode_id"]: row for row in supplement["case_edges"]}
    assert set(by_case) == {e["id"] for e in old["episodes"]}
    nodes, all_edges, metrics = [], [], {}
    total_temporal = total_documentary = total_references = 0
    total_comparable = total_possible = 0
    for ep in episodes:
        case = ep["id"]
        event_map = {e["event_id"]: e for e in ep["events"]}
        assert len(event_map) == len(ep["events"]) and len(event_map) >= 3
        assert [e["sequence_index"] for e in ep["events"]] == list(range(1, len(event_map) + 1))
        assert all(e["basis"] == "AUTHOR_RETROSPECTIVE_STATEMENT" for e in ep["events"])
        for event in ep["events"]:
            assert "SENSOR" not in event["basis"] and "VIDEO" not in event["basis"]
            nodes.append({
                "id":case+"::"+event["event_id"],
                "episode_id":case,
                "event_id":event["event_id"],
                "reported_event_kind":event["kind"],
                "source_text_paraphrase_ko":event["author_paraphrase_ko"],
                "evidence_grade":"REPORTED_OR_DOCUMENTED_RETROSPECTIVELY",
                "author":ep["author"],
                "source_url":ep["source_url"],
                "temporal_anchor":event.get("time_anchor"),
                "candidate_quantity":event.get("candidate_quantity")
            })
        relations=by_case[case] if case in by_case else ep
        precedences=relations.get("temporal", [])
        documentary=relations.get("documentary_after", [])
        references=relations.get("references", [])
        pred = {k:set() for k in event_map}
        succ = {k:set() for k in event_map}
        for a,b,reason in precedences:
            assert a in event_map and b in event_map and a != b
            assert b not in succ[a], "duplicate temporal assertion"
            succ[a].add(b);pred[b].add(a)
            all_edges.append({"src":case+"::"+a,"dst":case+"::"+b,
                "relation":"AUTHOR_REPORTED_BEFORE","basis":"CURATOR_SELECTED_EXPLICIT_PRIOR_CONSEQUENCE_OR_REPORTED_TIME",
                "source_url":ep["source_url"],"reason":reason})
        for a,b,reason in documentary:
            assert a in event_map and b in event_map and a!=b
            assert ep["events"][next(i for i,e in enumerate(ep["events"]) if e["event_id"]==b)]["kind"]=="OTHER_AUTHOR_POSTHOC_NOTE"
            all_edges.append({"src":case+"::"+a,"dst":case+"::"+b,
                "relation":"LATER_DOCUMENT_ADDENDUM_SEPARATE_ACTOR",
                "basis":"SOURCE_DOCUMENT_SEPARATELY_ATTRIBUTED",
                "source_url":ep["source_url"],"reason":reason})
        for a,b,rel,reason in references:
            assert a in event_map and b in event_map and a != b
            assert rel not in {"AUTHOR_REPORTED_BEFORE","DOCUMENTED_REJECTED_BY_ACTUAL_TEST"}
            all_edges.append({"src":case+"::"+a,"dst":case+"::"+b,"relation":rel,
                "basis":"AUTHOR_REPORTED_REFERENCE_NOT_AUTO_TEMPORAL",
                "source_url":ep["source_url"],"reason":reason})
        # Exact reachability; pred is NOT populated from narrative 'sequence_index'.
        reach = {k:set() for k in event_map}
        def successors(a,active):
            assert a not in active, "cycle in explicit temporal assertions"
            if reach[a]:
                return reach[a]
            active=active|{a}
            found=set(succ[a])
            for b in succ[a]:
                found |= successors(b,active)
            reach[a]=found
            return found
        for a in event_map: successors(a,set())
        assert all(a not in reach[a] for a in event_map)
        ordered=sum(len(v) for v in reach.values())
        total = len(event_map)*(len(event_map)-1)//2
        assert ordered<=total
        assert not any(a in reach[b] and b in reach[a] for a in event_map for b in event_map if a!=b)
        total_comparable+=ordered
        total_possible+=total
        # Order invariant: topological chain length <= event count.
        topo=[];todo=set(event_map)
        while todo:
            ready=sorted(k for k in todo if pred[k].isdisjoint(todo))
            assert ready, "DAG not topologically sortable"
            for k in ready:todo.remove(k);topo.append(k)
        longest={k:1 for k in event_map}
        for a in topo:
            for b in succ[a]:longest[b]=max(longest[b],longest[a]+1)
        # Maximum bipartite matching on comparability relation -> poset width (Dilworth).
        matching={}
        def augment(u,visited):
            for v in sorted(reach[u]):
                if v in visited:continue
                visited.add(v)
                if v not in matching or augment(matching[v],visited):
                    matching[v]=u;return True
            return False
        matched=sum(augment(u,set()) for u in sorted(event_map))
        width=len(event_map)-matched
        assert width>=1
        if len(event_map)>=5 and case in {"WHEELER_SEFMC2026_A1","UTOMO_FMCWORLD2026_A3","WONG_DDDSINGAPORE2025_A3"}:
            assert ordered<total, "these case studies must retain unreported relative orders"
        metrics[case]={
            "author":ep["author"],"nodes":len(event_map),
            "explicit_temporal_edges":len(precedences),
            "separately_attributed_document_addenda":len(documentary),
            "candidate_or_revision_references":len(references),
            "temporally_comparable_pairs_via_author_report":ordered,
            "unordered_event_pairs":total-ordered,
            "possible_pairs":total,
            "longest_certified_reported_precedence_chain":max(longest.values()),
            "max_set_of_currently_incomparable_events":width,
            "original_timeline_is_direct_video_ground_truth":False
        }
        total_temporal+=len(precedences)
        total_documentary+=len(documentary)
        total_references+=len(references)
    assert len(nodes)==41 and len({n["id"] for n in nodes})==41
    assert total_temporal==27, total_temporal
    assert total_documentary==1
    assert total_references==11
    counts=collections.Counter(n["reported_event_kind"] for n in nodes)
    revisits=sum(v for k,v in counts.items() if k.startswith("REVISIT_") or k=="LATE_REVISIT")
    assert revisits==4
    assert counts["DEFERRED_UNEVALUATED"]==3
    assert counts["CANDIDATE_NOT_WRITTEN"]==1
    anchors=[n for n in nodes if n["temporal_anchor"] is not None]
    assert len(anchors)==9
    for n in anchors:
        assert n["temporal_anchor"]["kind"].startswith("self_report_")
    graph={
        "schema":"cuberev-021-p6-fmc-partial-order-derived-v1",
        "scope":"REPORTED_RETROSPECTIVE_EVENT_RELATIONS; not directly observed choices",
        "author_reports_do_not_imply_total_order":True,
        "all_unlinked_event_pairs":"UNKNOWN_RELATIVE_ORDER",
        "complete_candidate_lists_recovered":False,
        "complete_video_frame_verified_processes":0,
        "source_input_sha256":{"p5":sha256(old_bytes),"p6":sha256(new_bytes)},
        "nodes":nodes,
        "edges":all_edges,
        "per_episode":metrics
    }
    receipt={
        "marker":"CUBE_REV_021_P6_SOURCE_GROUNDED_FMC_PARTIAL_ORDER_PASS",
        "scope":"Existing published retrospective narratives, original 6 P5 + 2 already published P6; no new human participants",
        "episodes":len(episodes),"distinct_author_names":len({e["author"] for e in episodes}),
        "reported_event_nodes":len(nodes),
        "explicit_author_temporal_edges":total_temporal,
        "separately_attributed_document_after_edges":total_documentary,
        "reported_candidate_reference_edges":total_references,
        "ordered_event_pairs_implied_by_reported_temporal_edges":total_comparable,
        "event_pairs_without_supported_relative_order":total_possible-total_comparable,
        "total_event_pairs_within_episodes":total_possible,
        "reported_candidate_revisits":revisits,
        "reported_untried_or_unassessed_candidates":counts["DEFERRED_UNEVALUATED"],
        "reported_candidates_not_even_written":counts["CANDIDATE_NOT_WRITTEN"],
        "author_report_time_anchors":len(anchors),
        "independent_video_or_timestamp_grounded_time_anchors":0,
        "real_external_vfmc_sessions_acquired":0,
        "author_linked_candidate_video_urls":1,
        "youtube_video_frames_actually_inspected":0,
        "wong_video_continuity_authenticated":False,
        "vincent_primary_source_attempt_corrected_to":"FMCWorld2026 Attempt 3; 24 HTM",
        "event_kind_counts":dict(sorted(counts.items())),
        "per_episode":metrics,
        "source_sha256":graph["source_input_sha256"],
        "warning":"No chronological edge generated from narrative index by default; graphs do not prove full hidden search, human memory parameters, or causal psychological effects."
    }
    return graph,receipt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",required=True)
    args=ap.parse_args()
    g,r=audit()
    p=Path(args.outdir)
    p.mkdir(parents=True,exist_ok=True)
    graph_json=(json.dumps(g,indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode()
    r["graph_json_sha256"]=sha256(graph_json)
    (p/"p6_fmc_source_grounded_event_graph.json").write_bytes(graph_json)
    (p/"p6_fmc_partial_order_receipt.json").write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print(r["marker"])
    print(json.dumps({k:r[k] for k in [
        "episodes","reported_event_nodes","explicit_author_temporal_edges",
        "ordered_event_pairs_implied_by_reported_temporal_edges",
        "event_pairs_without_supported_relative_order",
        "reported_candidate_revisits","reported_untried_or_unassessed_candidates",
        "author_linked_candidate_video_urls","youtube_video_frames_actually_inspected"
    ]},sort_keys=True))

if __name__=="__main__":main()
