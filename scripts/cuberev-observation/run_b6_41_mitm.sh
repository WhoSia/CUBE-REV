#!/usr/bin/env bash
# Explicit local/WSL reproduction, NOT a GitHub Actions bot workflow.
# Usage: bash run_b6_41_mitm.sh HISTORICAL_B1_B5_CERTIFICATES.zip OUTPUT_DIRECTORY
set -euo pipefail
[[ $# == 2 ]] || { echo 'usage: run_b6_41_mitm.sh ARCHIVE.zip OUTPUT_DIR' >&2; exit 2; }
here="$(cd "$(dirname "$0")" && pwd)"
archive="$(realpath "$1")"
mkdir -p "$2"
out="$(realpath "$2")"
python3 "$here/emit_b6_41_mitm_inputs.py" "$archive" "$out"
g++ -std=c++17 -O3 -Wall -Wextra -I "$out" \
  "$here/verify_b6_41_mitm.cpp" -o "$out/verify_b6_41_mitm"
for bounds in "0 8" "8 16" "16 24" "24 32" "32 41"; do
  read -r first last <<< "$bounds"
  echo "Running independent 18-HTM proof classes [$first,$last)"
  "$out/verify_b6_41_mitm" "$out/targets41.txt" "$first" "$last" \
    | tee "$out/mitm_$first_$last.log"
done
python3 - "$out" <<'PY'
import re,sys,hashlib
from pathlib import Path
out=Path(sys.argv[1])
assert hashlib.sha256((out/'targets41.txt').read_bytes()).hexdigest() == (
    '6395e34efe736eecb1bfab8fa9cc713d2378e721ab79f009ec54d37ff69cb340')
all_ids=[]
all_probes=0
for a,b in ((0,8),(8,16),(16,24),(24,32),(32,41)):
    log=(out/f'mitm_{a}_{b}.log').read_text()
    ids=[int(x) for x in re.findall(r'^PASS class=(\d+) probes=8331112 intersection=0$',log,re.M)]
    assert ids==list(range(a,b)),(a,b,ids)
    assert f'CERTIFIED range={a}:{b} classes={b-a} probes={(b-a)*8331112}' in log
    assert 'B6 generated=8331112 unique=8240087' in log
    all_ids.extend(ids)
    all_probes+=len(ids)*8331112
assert all_ids==list(range(41)) and all_probes==341575592
print('PASS complete independent HTM lower bound: 41 classes, 341575592 probes')
PY
