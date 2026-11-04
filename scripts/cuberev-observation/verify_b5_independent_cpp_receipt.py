#!/usr/bin/env python3
"""Cross-language bridge: accept only physical B5 witnesses printed by fresh C++ BFS.

Replays actual generated word pairs using the separate Python 48-sticker
engine. Also checks C++-reported ORIGINAL edge triples and the committed
deterministic receipt. This avoids the false-positive pipeline in which
C++ has 13 generic FOUND lines but Python separately tests unrelated seeds.
"""
import argparse
import json
import re
from pathlib import Path
from verify_b5_three_edge_physical_manifest import (
    physical_support,verify_manifest,full_three_edge_rotation_orbits
)

PATTERN = re.compile(
    r'^ORBIT (?P<index>\d+) size=(?P<size>\d+) '
    r'triple=(?P<triple>[A-Z]{2},[A-Z]{2},[A-Z]{2}) '
    r'FOUND left="(?P<left>[^"]*)" right="(?P<right>[^"]*)"$'
)

def parse_receipt(text):
    entries=[]
    for line in text.splitlines():
        if not line.strip():
            continue
        m=PATTERN.fullmatch(line.strip())
        if not m:
            raise ValueError("Invalid or non-witness C++ receipt line: "+repr(line))
        record=m.groupdict()
        if int(record["index"])!=len(entries):
            raise ValueError("Non-consecutive or repeated orbit index")
        triple=record["triple"].split(",")
        expected=frozenset(tuple(sorted(e)) for e in triple)
        actual=physical_support(record["left"],record["right"])
        if actual!=expected:
            raise ValueError("C++ stated cubie names != independently replayed originals")
        entries.append({
            "id":f'B5-R{len(entries)+1:02d}',
            "representative_triple":record["triple"],
            "left":record["left"],"right":record["right"],
            "orbit_size":int(record["size"])
        })
    if len(entries)!=13:
        raise ValueError(f"Expected 13 independently generated orbits, got {len(entries)}")
    # These sizes are tied to physical supports, not mere printed C++ numbers.
    orbit_sets=full_three_edge_rotation_orbits()
    by_support={support:len(o) for o in orbit_sets for support in o}
    for item in entries:
        support=frozenset(tuple(sorted(e)) for e in item["representative_triple"].split(","))
        if by_support[support]!=item["orbit_size"]:
            raise ValueError("C++ orbit size disagrees with separate Python rotation geometry")
    return entries

def bridge(receipt_text,pinned_json):
    records=parse_receipt(receipt_text)
    result=verify_manifest({"schema_version":1,"witnesses":records},True)
    assert result["full_220_certificate"] and result["physical_orbits_covered"]==13
    expected=pinned_json["witnesses"]
    observed=[{k:r[k] for k in ("id","representative_triple","left","right")}
              for r in records]
    if observed!=expected:
        raise ValueError("Generated C++ words differ from pinned original word-pair manifest")
    return {
        "generator":"fresh 48-sticker C++ B5 621649-state BFS",
        "independent_replayer":"Python 48-sticker word/rotation original-tag factors",
        "generated_word_pairs_replayed":len(records),
        "original_edge_triples_replayed":result["distinct_triple_edge_supports_physically_replayed"],
        "rotation_orbits_physically_covered":result["physical_orbits_covered"],
        "pinned_receipt_identical":True,
        "complete_physical_certificate":True
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("cpp_stdout")
    p.add_argument("pinned_manifest")
    args=p.parse_args()
    content=Path(args.cpp_stdout).read_text(encoding="utf-8")
    manifest=json.loads(Path(args.pinned_manifest).read_text(encoding="utf-8"))
    result=bridge(content,manifest)
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
