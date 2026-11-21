#!/usr/bin/env python3
"""Audit seven nonoverlapping X ranges; verify complete 1362-vector coverage."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path

if not __debug__:
    raise RuntimeError('This proof audit uses assertions; Python -O/-OO is forbidden.')

STEPS=[(0,200),(200,200),(400,200),(600,200),(800,200),(1000,200),(1200,162)]
POLICY_SHA='80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227'
EXPECTED_RECORDS=3215616


def check(folder):
    folder=Path(folder)
    records=0;hist=Counter();parity=Counter();filenames={}
    last_physical=None
    for start,n in STEPS:
        f=folder/f'X-part-{start}.json';raw=f.read_bytes()
        row=json.loads(raw)
        assert row['status']=='PASS' and row['policy_sha256']==POLICY_SHA
        part=row['all_orbits'];assert part['status']=='PASS'
        assert part['start_vector']==start and part['vectors']==n
        assert part['edge_read_frames']==19 and part['corner_distinct_read_positions']==14
        assert part['representatives']==52
        count=part['reconstructed_edge_records']
        assert sum(part['distinct_read_address_histogram'].values())==count
        records+=count
        hist.update({int(i):v for i,v in part['distinct_read_address_histogram'].items()})
        parity.update({int(i):v for i,v in part['canonical_sign_correction_vector_count'].items()})
        filenames[f.name]=hashlib.sha256(raw).hexdigest()
        if start==1200:last_physical=row['physical_replay']
    assert records==EXPECTED_RECORDS,(records,EXPECTED_RECORDS)
    assert sum(hist.values())==records
    assert sum(parity.values())==1362
    assert last_physical['status']=='PASS'
    assert last_physical['full_48_sticker_reconstructions']==1000
    return {'status':'PASS','policy_sha256':POLICY_SHA,
            'first_color_count_vectors':1362,'representatives':52,
            'exhaustive_original_edge_records':records,'frames':19,'corner_unique_addresses':14,
            'unique_adaptive_edge_address_count':dict(sorted(hist.items())),
            'sign_correction_per_count_vector':dict(sorted(parity.items())),
            'fixed_probe_replay':last_physical,
            'part_sha256':filenames,
            'scope':'every oriented edge record for each sorted prefix count vector, with arbitrary-order transport handled algebraically; plus 1000 geometric random scrambles; no all-states Lean theorem claimed'}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path,nargs='?',default=Path(__file__).resolve().parent)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();receipt=check(args.folder)
    text=json.dumps(receipt,indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.write_text(text)
    print(text)
