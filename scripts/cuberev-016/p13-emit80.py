#!/usr/bin/env python3
"""Derive canonical 80 B-component 28-bit masks from original P10/P12 math data."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=json.loads((root/'docs/0.16/P10_50_BY_116.json').read_text())
c=json.loads((root/'docs/0.16/P12_CORE_CERTIFICATE.json').read_text())
idx=c['heavy20'] if 'heavy20' in c else c['heavy20_indices']
light=c['light8'] if 'light8' in c else c['light8_indices']
assert len(idx)==20 and len(light)==8
result=[]
for s in p['coverage_masks']:
    n=int(s)
    bits=sum(1<<i for i,k in enumerate(idx+light) if (n>>k)&1)
    if bits:result.append(bits)
assert len(result)==80 and len(set(result))==80
for bits in result:print(bits)
