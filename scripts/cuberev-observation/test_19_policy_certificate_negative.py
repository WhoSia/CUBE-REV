#!/usr/bin/env python3
"""Negative tests: malformed or incomplete policy certificates must be rejected."""
import copy
import json
from pathlib import Path
from verify_19_policy_certificate import verify_one

original=json.loads(Path(__file__).with_name('upper-policy-certificate.json').read_text())
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
