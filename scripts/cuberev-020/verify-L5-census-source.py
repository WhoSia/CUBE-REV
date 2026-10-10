#!/usr/bin/env python3
"""Independent comparison of an original SHA-locked physical L5 map census with P13."""
import argparse
import hashlib
import json
from pathlib import Path

SOURCE_SHA = "9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1"
WORDS = [537824, 768320, 439040, 125440, 17920, 1024]
MAX_RANK = [1, 2, 4, 7, 7, 3]
GE5 = [0, 0, 0, 43584, 6912, 0]
RANK7 = [0, 0, 0, 128, 512, 0]
RANK7_CLASSES = [0, 0, 0, 16, 16, 0]

def canonical_partition(blocks):
    assert sum(blocks) == (1 << 12) - 1
    assert not any(x & y for i, x in enumerate(blocks) for y in blocks[i+1:])
    labels, key = {}, 0
    for i in range(12):
        b = next(j for j, mask in enumerate(blocks) if (mask >> i) & 1)
        v = labels.setdefault(b, len(labels))
        key |= v << (4 * i)
    return key

def main(args):
    sha = hashlib.sha256(args.physical.read_bytes()).hexdigest()
    assert sha == SOURCE_SHA, ("wrong original physical authority", sha)
    result = json.loads(args.census.read_text())
    assert result["physical_words_enumerated"] == 18**5
    assert result["unique_partitions_all"] == 14938
    assert result["rank7_partition_overlap_q3_q4"] == 0
    rows = result["by_informative_action_count"]
    assert len(rows) == 6
    for q, rec in enumerate(rows):
        assert (rec["q"], rec["words"], rec["max_rank"],
                rec["rank_at_least_five"], rec["rank_seven"],
                rec["rank7_unique_partitions"]) == (
                q, WORDS[q], MAX_RANK[q], GE5[q], RANK7[q], RANK7_CLASSES[q])
        assert sum(rec["rank_histogram"]) == rec["words"]
    from_original_tsv = set()
    count = 0
    for line in args.tsv.read_text().splitlines():
        tokens, blocks = line.split("|")
        actions = list(map(int, tokens.split()))
        assert len(actions) == 5 and all(0 <= a < 18 for a in actions)
        from_original_tsv.add(canonical_partition([int(x) for x in blocks.split()]))
        count += 1
    from_new_cxx = {int(k) for k in args.partition_keys.read_text().splitlines()}
    assert len(from_original_tsv) == count == 14938
    assert from_new_cxx == from_original_tsv, "different physical observation partitions"
    print(json.dumps({
        "result":"CUBE_REV_020_L5_TRANSPORT_CUT_CENSUS_INDEPENDENT_PASS",
        "source_sha256":sha,
        "original_partition_tsv_sha256":hashlib.sha256(args.tsv.read_bytes()).hexdigest(),
        "physical_words":18**5,
        "canonical_partitions":len(from_original_tsv),
        "rank7_q3_partitions":16,"rank7_q4_partitions":16,"overlap":0
    },indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for field in ["physical", "tsv", "census", "partition_keys"]:
        ap.add_argument("--" + field.replace("_","-"), required=True, type=Path)
    main(ap.parse_args())
