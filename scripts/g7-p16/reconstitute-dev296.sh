#!/usr/bin/env bash
set -euo pipefail
: "${GH_TOKEN:?GH_TOKEN required}"
: "${REPO:?REPO required}"
OUT="${1:-/tmp/p16-dev296}"
rm -rf "$OUT"
mkdir -p "$OUT/input" "$OUT/build"

fetch_artifact () {
  stage="$1"; name="$2"; id="$3"; expected="$4"
  dir="$OUT/input/$stage/$name"; mkdir -p "$dir"
  zip="$OUT/input/$stage-$name.zip"
  curl --fail --location --silent --show-error \
    -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$REPO/actions/artifacts/$id/zip" -o "$zip"
  echo "$expected  $zip" | sha256sum -c -
  unzip -q "$zip" -d "$dir"
}
# P11
fetch_artifact p11 b1 11242854238 0bc3c845d0caadcd84a6df4ce8db4a65fae083d6ef01e076f5ce95755676c6ea
fetch_artifact p11 b2 11243410683 c4589ff7955ea3fe7fe1d452f8a137e4f2c799e60cad27e863fa91bfcc7f975e
fetch_artifact p11 b3 11243041519 82ce3af8a36c0eb3bf8f6192a72db1adb17f2046cf8ef2f602b4d583887ffe38
fetch_artifact p11 b4 11243391026 8575409309eadab60cf5d2145925108c8139a62e75a7f2060785c4de75a3028a
# P13
fetch_artifact p13 b1 11301352851 965a18ca9969be65469e52c92d8d1a1a21cd2e022ec4ae7431ae500113e45051
fetch_artifact p13 b2 11301148487 183b58f8c596872c816f5ef93e51251d984f55761a0dfd35f280c4487c40c746
fetch_artifact p13 b3 11301576955 a3a1fcec681ee94d5a9724ee3ac8feb21e8deed8578808e0eaedf0e9afe2af2a
fetch_artifact p13 b4 11300573510 0938a546d123d915942ee67e18dabfc212c90afa2a44c7b7197d03ad4e61b81e
fetch_artifact p13 b5 11301551669 731d668e88ede7d61a9d73ea4d45ed19b1b13a36a0172b4b2c2239fdd15daa7c
fetch_artifact p13 b6 11301123162 a6ffff8bdb75437593f4cf99d7b1d36f281531868f82edb7b677c7b20f77f2f8
fetch_artifact p13 b7 11300877650 14448550881dbc0966fb447f5fdae92482ea54086d0eb5dab142fe4801d3ee14
fetch_artifact p13 b8 11301252675 9900a87195dec52002e5aecabbdc7a357163e4d20f7a590a0241fc6bb76ad519
# P14
fetch_artifact p14 b1 11301434538 10b056559d6486a7bf3153353cd2a93d609cfd37974adf9071996033ecca0262
fetch_artifact p14 b2 11301686530 bb5919026b03e5d45e36e7d60f54981559924bb98b780747a9808627556a05bb
fetch_artifact p14 b3 11301935198 c85beed299f73e059f5293d38b642e605b5f22c5c44034a88ed1cd98443b2216
fetch_artifact p14 b4 11301439628 47913670114c1f7bc715bb9ff20bbaa456f945c614fcf2e34d44889a1ca6b13c
fetch_artifact p14 b5 11301504923 c989ea28d5fd70fce9b8cf373fb1f3b0b560525a66c716a3e718f8259e0bd970
fetch_artifact p14 b6 11302415570 db2d5fced477a412e97c9e5f20e6dcdef138f805275870e0a4bc5a55ab186d88
fetch_artifact p14 b7 11301995531 d62e24a1d9af8383d9ba477c2022eda5ae1c046c7eeafcaf90fe8ca9bbe9acf5
fetch_artifact p14 b8 11301483305 fdad7d0ff7be88595c8465d79a1e81169223d3a46615ce7d2f6e9838575eb588
# P15
fetch_artifact p15 b1 11308256128 8bae1261d1479f9d8e0570df4a448707893054ca801486b2b485500249dbf3f8
fetch_artifact p15 b2 11308055254 c0f0556b3cf9899f0912a81783c3749a8700f01a413ea95adf575cb4554b1bd9
fetch_artifact p15 b3 11307558080 76d647d131dea35acd2dcc09797fd0d523997e2c5367e00f7ef58aa85ac0228d
fetch_artifact p15 b4 11307722609 7904a95284f5cd64f6fa062f1560fa0ecd9ca281940bfd54a8ce7007370f0d16
fetch_artifact p15 b5 11308075168 89f3d4bfb1188280143d083f6e0c424776240d4cf451850a5474ed47a0468a2f
fetch_artifact p15 b6 11307990571 8f3eb62796cf3ae59fda24d93664763312b8e1492dfad1e119801901fde53e85
fetch_artifact p15 b7 11307533260 3413ffb6792bc6988abdab3a0822739cd3c87fde35428cc13d8b2aed74e1c1b0
fetch_artifact p15 b8 11307224714 6d8204f7e70342edf67f341237ce113b14561a471f05e5d5f38705e059a795cb
fetch_artifact p15 b9 11307178834 307a6b72df17bcb146622527194a7d69ba98d2618454b8bc5381b7e88b103284
fetch_artifact p15 b10 11307966560 c6d725ca24686012ecc1986f113c47bb15bcc3a50f8d7353ced80936d78de7d5
fetch_artifact p15 b11 11308165106 767aabe7425ce4b9e618740c4669049e9ec5844a2ceae23126d37b93fb787091
fetch_artifact p15 b12 11307559284 6b8c988933fe3776a14d88dfb50dccc9ecbe51ff181eb87b8a67f149dce09120

mkdir -p "$OUT/build"/{p11,p13,p14,p15}
node scripts/g7-p11/merge-fresh-corpus.mjs \
  --source P11_BATCH1="$OUT/input/p11/b1" --source P11_BATCH2="$OUT/input/p11/b2" \
  --source P11_BATCH3="$OUT/input/p11/b3" --source P11_BATCH4="$OUT/input/p11/b4" \
  --out "$OUT/build/p11/corpus"
node scripts/g7-p13/merge-fresh80-corpus.mjs \
  --source P13_BATCH1="$OUT/input/p13/b1" --source P13_BATCH2="$OUT/input/p13/b2" \
  --source P13_BATCH3="$OUT/input/p13/b3" --source P13_BATCH4="$OUT/input/p13/b4" \
  --source P13_BATCH5="$OUT/input/p13/b5" --source P13_BATCH6="$OUT/input/p13/b6" \
  --source P13_BATCH7="$OUT/input/p13/b7" --source P13_BATCH8="$OUT/input/p13/b8" \
  --out "$OUT/build/p13/corpus"
node scripts/g7-p14/merge-confirm80-corpus.mjs \
  --source P14_BATCH1="$OUT/input/p14/b1" --source P14_BATCH2="$OUT/input/p14/b2" \
  --source P14_BATCH3="$OUT/input/p14/b3" --source P14_BATCH4="$OUT/input/p14/b4" \
  --source P14_BATCH5="$OUT/input/p14/b5" --source P14_BATCH6="$OUT/input/p14/b6" \
  --source P14_BATCH7="$OUT/input/p14/b7" --source P14_BATCH8="$OUT/input/p14/b8" \
  --out "$OUT/build/p14/corpus"
ROOT () { file="$(find "$1" -path '*/derived/solves.jsonl' -print -quit)"; test -n "$file"; dirname "$(dirname "$file")"; }
node scripts/g7-p15/merge-fresh96-corpus.mjs \
  --source P15_BATCH1="$(ROOT "$OUT/input/p15/b1")" --source P15_BATCH2="$(ROOT "$OUT/input/p15/b2")" \
  --source P15_BATCH3="$(ROOT "$OUT/input/p15/b3")" --source P15_BATCH4="$(ROOT "$OUT/input/p15/b4")" \
  --source P15_BATCH5="$(ROOT "$OUT/input/p15/b5")" --source P15_BATCH6="$(ROOT "$OUT/input/p15/b6")" \
  --source P15_BATCH7="$(ROOT "$OUT/input/p15/b7")" --source P15_BATCH8="$(ROOT "$OUT/input/p15/b8")" \
  --source P15_BATCH9="$(ROOT "$OUT/input/p15/b9")" --source P15_BATCH10="$(ROOT "$OUT/input/p15/b10")" \
  --source P15_BATCH11="$(ROOT "$OUT/input/p15/b11")" --source P15_BATCH12="$(ROOT "$OUT/input/p15/b12")" \
  --out "$OUT/build/p15/corpus"

for stage in p11 p13 p14 p15; do
  node scripts/cube/replay-exact-trajectories.mjs \
    --input "$OUT/build/$stage/corpus/combined-solves.jsonl" --out "$OUT/build/$stage/exact"
  node scripts/g7-p7/prefix-context.mjs \
    "$OUT/build/$stage/exact/exact-trajectories.json" "$OUT/build/$stage/corpus/solve-metadata.jsonl" \
    "$OUT/build/$stage/prefix-states.tsv" "$OUT/build/$stage/context.jsonl"
done

python3 scripts/g7-p16/merge-multicohort-development.py \
  --source P11="$OUT/build/p11/prefix-states.tsv,$OUT/build/p11/context.jsonl" \
  --source P13="$OUT/build/p13/prefix-states.tsv,$OUT/build/p13/context.jsonl" \
  --source P14="$OUT/build/p14/prefix-states.tsv,$OUT/build/p14/context.jsonl" \
  --source P15="$OUT/build/p15/prefix-states.tsv,$OUT/build/p15/context.jsonl" \
  --out "$OUT/build/multicohort"

echo G7_P16_DEV296_RECONSTITUTION_PASS
