#!/usr/bin/env python3
"""Physical B5 220-triple-edge certificate verifier (fail-closed).

Accepts explicit B5 pairs of <=5 18-HTM moves; replays BOTH states with
standalone 48-movable-sticker physics; rotates each word under all 24 proper
cube symmetries; and derives actual original-cubie difference supports.
No 220-outcome list is synthesized from combinations as purported evidence.

Without an externally supplied sufficient witness-pair manifest this does
NOT claim the complete 220/220 result. Historical SHA and archive custody
are separate from this source-independent physical replay.
"""
from __future__ import annotations
import argparse
import json
from itertools import combinations
from pathlib import Path

from verify_short_support_phase import (
    initial, factors, play, proper24, N
)

FACES = tuple("URFDLB")
NORMAL_TO_FACE = {v:k for k,v in N.items()}
ORIGINAL = factors(initial())
EDGE_TAGS = {tag for tag in ORIGINAL if len(tag)==2}
CORNER_TAGS = {tag for tag in ORIGINAL if len(tag)==3}
assert len(EDGE_TAGS)==12 and len(CORNER_TAGS)==8

def validate_tokens(word):
    if not isinstance(word,str):
        raise ValueError("HTM word must be string")
    seq=word.split()
    if len(seq)>5:
        raise ValueError("B5 witness half path exceeds five moves")
    for token in seq:
        if len(token) not in (1,2) or token[0] not in FACES or (
            len(token)==2 and token[1] not in ("2","'")
        ):
            raise ValueError("Non-18HTM token: "+token)
    return seq

def rotate_word(word, rotation):
    seq=validate_tokens(word)
    return " ".join(
        NORMAL_TO_FACE[rotation(N[m[0]])]+m[1:] for m in seq
    )

def physical_support(left,right):
    validate_tokens(left)
    validate_tokens(right)
    l=factors(play(left))
    r=factors(play(right))
    diff=frozenset(tag for tag in ORIGINAL if l[tag]!=r[tag])
    if not diff or not diff<=EDGE_TAGS or len(diff)!=3:
        raise ValueError("Not precisely 3 differing ORIGINAL edges: "+repr(diff))
    return diff

def original_tag_position(tag):
    return ORIGINAL[tag][0]

def orbit_from_replayed_words(left,right):
    baseline=physical_support(left,right)
    position_to_tag={original_tag_position(tag):tag for tag in ORIGINAL}
    orbit=set()
    for rot in proper24():
        physical=physical_support(rotate_word(left,rot),rotate_word(right,rot))
        predicted=frozenset(
            position_to_tag[rot(original_tag_position(tag))]
            for tag in baseline
        )
        if physical!=predicted:
            raise AssertionError("Face-word physical covariance failure")
        orbit.add(physical)
    return frozenset(orbit)

def full_three_edge_rotation_orbits():
    """Algebraically derive all 13 cube-rotation orbits of 220 edge triples.

    These are targets only; constructing an orbit is NOT physical evidence
    that some B5 pair realizes it.
    """
    position_to_tag={original_tag_position(tag):tag for tag in ORIGINAL}
    universe={frozenset(p) for p in combinations(EDGE_TAGS,3)}
    unseen=set(universe)
    orbits=[]
    while unseen:
        representative=min(unseen,key=lambda x:tuple(sorted(x)))
        orbit=frozenset(frozenset(
            position_to_tag[rot(original_tag_position(t))] for t in representative
        ) for rot in proper24())
        if not orbit<=unseen:
            raise AssertionError("Orbit intersects already partitioned region")
        unseen-=orbit
        orbits.append(orbit)
    assert len(orbits)==13
    sizes=sorted(map(len,orbits))
    assert sizes==[4,4,8,12,12,12,24,24,24,24,24,24,24],sizes
    assert set().union(*orbits)==universe
    return tuple(sorted(orbits,key=lambda o:(len(o),tuple(sorted(min(
        o,key=lambda x:tuple(sorted(x))))))))

def verify_manifest(payload, require_complete=True):
    if not isinstance(payload,dict) or payload.get("schema_version")!=1:
        raise ValueError("Expected schema_version=1 JSON object")
    records=payload.get("witnesses")
    if not isinstance(records,list) or not records:
        raise ValueError("Nonempty witnesses array required")
    support_union=set()
    orbit_sizes=[]
    for i,record in enumerate(records):
        if not isinstance(record,dict) or "left" not in record or "right" not in record:
            raise ValueError("Witness entry requires left and right physical words")
        orb=orbit_from_replayed_words(record["left"],record["right"])
        support_union.update(orb)
        orbit_sizes.append(len(orb))
    orbit_partition=full_three_edge_rotation_orbits()
    universe=set().union(*orbit_partition)
    physical_orbits_covered=sum(bool(orb & support_union)
                                for orb in orbit_partition)
    if not support_union<=universe:
        raise AssertionError("Support semantics inconsistent")
    summary={
        "witness_pairs_replayed":len(records),
        "proper_rotations_checked_per_witness":24,
        "orbit_sizes":orbit_sizes,
        "distinct_triple_edge_supports_physically_replayed":len(support_union),
        "total_possible_triple_edge_supports":len(universe),
        "missing_triple_edge_supports":len(universe-support_union),
        "physical_orbits_covered":physical_orbits_covered,
        "total_geometric_orbits":len(orbit_partition),
        "full_220_certificate":support_union==universe
    }
    if require_complete and support_union!=universe:
        raise ValueError("INCOMPLETE physical B5 three-edge coverage: "+json.dumps(summary))
    return summary

B3_DEMONSTRATION={
    "schema_version":1,
    "witnesses":[{"left":"U R2 U'","right":"D B2 D'"}],
}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("manifest",nargs="?",help="JSON with all physical B5 witness pairs")
    parser.add_argument("--demo-b3",action="store_true",help="Replay known B3 orbit; explicitly NOT a full B5 certificate")
    args=parser.parse_args()
    if args.demo_b3 and args.manifest:
        parser.error("choose B3 demo OR external full manifest")
    if args.demo_b3:
        result=verify_manifest(B3_DEMONSTRATION,require_complete=False)
        assert result["distinct_triple_edge_supports_physically_replayed"]==12
        assert not result["full_220_certificate"]
        print(json.dumps({"status":"PARTIAL_B3_ONLY","audit":result},indent=2))
    elif args.manifest:
        payload=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        result=verify_manifest(payload,require_complete=True)
        print(json.dumps({"status":"COMPLETE_B5_220_PHYSICAL_REPLAY","audit":result},indent=2))
    else:
        parser.error("missing physical manifest: fail closed; use --demo-b3 only for partial witness")

if __name__=="__main__":
    main()
