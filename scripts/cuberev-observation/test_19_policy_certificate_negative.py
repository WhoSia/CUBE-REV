#!/usr/bin/env python3
"""Negative tests: malformed or incomplete policy certificates must be rejected."""
import base64
import copy
import gzip
import hashlib
import json
from pathlib import Path
from verify_19_policy_certificate import verify_one

# The plaintext certificate is intentionally not tracked. Read the immutable
# SHA-pinned blob in memory so unittest discovery also works on a fresh clone.
BLOB = (Path(__file__).resolve().parents[2] / 'formal' / '029' /
        'certificate_blobs' / 'upper-policy-certificate.json.gz.b64')
EXPECTED_PACKED_SHA256 = 'd9dd5f9c283b9d79a86bcf00cefc51e013bc8d20a1c8c34077316a1c81e3f1d3'
EXPECTED_RAW_SHA256 = '80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227'
packed = base64.b64decode(BLOB.read_bytes().strip(), validate=True)
assert hashlib.sha256(packed).hexdigest() == EXPECTED_PACKED_SHA256
raw = gzip.decompress(packed)
assert hashlib.sha256(raw).hexdigest() == EXPECTED_RAW_SHA256
original = json.loads(raw)

base=original['representatives'][0]
assert base['nodes'][0][0]=='read'


def reject(kind,mutate):
    entry=copy.deepcopy(base)
    mutate(entry)
    try:
        verify_one(entry)
    except (AssertionError, KeyError, IndexError, TypeError, ValueError):
        print('REJECT',kind)
        return
    raise RuntimeError('Incorrectly accepted '+kind)

reject('premature ambiguous leaf',lambda e:e['nodes'].__setitem__(0,['leaf']))
reject('missing color reply branch',lambda e:e['nodes'][0][2].pop(next(iter(e['nodes'][0][2]))))
reject('wrong unread address',lambda e:e['nodes'][0].__setitem__(1,(e['nodes'][0][1]+1)%13))
reject('invalid child reference',lambda e:e['nodes'][0][2].__setitem__(next(iter(e['nodes'][0][2])),len(e['nodes'])+1))
print('PASS four negative controls')
