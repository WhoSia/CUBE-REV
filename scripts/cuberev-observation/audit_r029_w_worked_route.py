#!/usr/bin/env python3
"""Replay V's eight final paired reads in original cube coordinates.

Verifies the data's stored lookup-order turn routes against the 48-sticker
geometric model, all edge replies against the reconstructed original edge
arrangement, and existence of legal consistent corner twists.
"""
import json
from itertools import product
from collections import Counter
from pathlib import Path
from audit_r029_w_corner_geometric_decoder import geometry,EDGES,CORNERS
from audit_r029_w_joint_routes import follow
from audit_r029_w_transport_all_prefixes import COLORS, LABELS, permutation_parity

HERE=Path(__file__).resolve()
DATA=HERE.with_name('worked-physical-replay.json')


def sticker_number(address):
    name,part=address.split('[')
    ix=int(part.rstrip(']'))-1
    if name in EDGES:return 2*EDGES.index(name)+ix
    return 24+3*CORNERS.index(name)+ix


def turns(names):
    result=[]
    for item in names:
        assert item[0] in COLORS
        base=2*COLORS.index(item[0])
        if item.endswith('2'):result.extend([base,base])
        elif item.endswith("'"):result.append(base+1)
        else:result.append(base)
    return tuple(result)


def run(data=DATA):
    record=json.loads(Path(data).read_text())
    cmap=record['colors']
    inv={v:k for k,v in cmap.items()}
    assert len(inv)==6
    original=record['prefix']
    order=sorted(range(11),key=lambda i: COLORS.index(cmap[original[i]])) + [11]
    labelmap={frozenset(k):i for i,k in enumerate(LABELS)}
    induced=[labelmap[frozenset(cmap[k] for k in edge)] for edge in LABELS]
    corrected=record['physical_corner_sign'] ^ permutation_parity(order) ^ permutation_parity(induced)
    assert corrected==record['representative_sign']
    (word,)=[w for w,b in record['terminal_words_and_signs'] if b==corrected]
    assert len(word)==13
    second=[None]*11
    for i,pos in enumerate(order[:11]):second[pos]=inv[word[i]]
    original_edges=''.join(a+b for a,b in zip(original,second)) + ''.join(inv[c] for c in word[11:13])
    assert len(original_edges)==24
    edge_assignment=[original_edges[i:i+2] for i in range(0,24,2)]
    cubie_ids=[labelmap[frozenset(name)] for name in edge_assignment]
    assert sorted(cubie_ids)==list(range(12))
    assert permutation_parity(cubie_ids)==record['physical_corner_sign']
    cornerpieces=record['corner_permutation']
    assert sorted(cornerpieces)==sorted(CORNERS)
    assert permutation_parity([CORNERS.index(c) for c in cornerpieces])==record['physical_corner_sign']
    geom=geometry()
    source_probe=[sticker_number(s) for s in record['fixed_probes']]
    corner_conditions=[]
    for row in record['trace']:
        target=(sticker_number(row['edge']),sticker_number(row['corner']))
        route=turns(row['forward_route_from_probes_to_addresses'])
        actual=(follow(geom,route,source_probe[0]),follow(geom,route,source_probe[1]))
        assert actual==target,(row['frame'],actual,target)
        assert original_edges[target[0]]==row['edge_color'],(row['frame'],'edge color')
        corner_conditions.append((target[1]-24,row['corner_color']))
    consistent=[]
    for twist in product(range(3),repeat=8):
        if sum(twist)%3:continue
        corners=''.join(c[k:]+c[:k] for c,k in zip(cornerpieces,twist))
        if all(corners[slot]==color for slot,color in corner_conditions):
            consistent.append(twist)
    assert consistent, 'The example corner replies contradict twist legality.'
    if 'corner_twists' in record:
        assert tuple(record['corner_twists']) in consistent
        twists=tuple(record['corner_twists'])
        complete_corners=''.join(c[k:]+c[:k] for c,k in zip(cornerpieces,twists))
        first=record['first_11_corner_reads']
        assert [r['frame'] for r in first] == list(range(1,12))
        for r in first:
            assert complete_corners[sticker_number(r['corner'])-24] == r['corner_color']
        scheduled=[r['corner'] for r in first]+[record['trace'][0]['corner'],
                 record['trace'][1]['corner'],record['trace'][-1]['corner']]
        assert scheduled==record['planned_14_corner_addresses']
        assert len(set(scheduled))==14
        counts=Counter(item.split('[')[0] for item in scheduled)
        assert len(counts)==7 and all(n==2 for n in counts.values())
        assert 'DLB[1]' in scheduled[:11], 'Repeated frame-14–18 read must be known.'
        assert all(row['corner']=='DLB[1]' and row['corner_color']==complete_corners[sticker_number('DLB[1]')-24]
                   for row in record['trace'][2:-1])
    return {'status':'PASS','worked_example_frames':len(record['trace']),
            'route_endpoint_checks':len(record['trace'])*2,
            'edge_reply_checks':len(record['trace']),
            'selected_representative_word':word,
            'reconstructed_original_edges':edge_assignment,
            'compatible_legal_corner_twist_assignments':len(consistent),
            'explicit_corner_schedule_checked': 'corner_twists' in record,
            'query_order_convention':'stored move strings are lookup-order routes; physical execution reverses the list',
            'scope':'the frozen worked example, not the universal policy'}

if __name__=='__main__':
    raw=HERE.with_name('worked-physical-replay.json')
    try:
        run(raw)
    except AssertionError as e:
        assert str(e)=='The example corner replies contradict twist legality.'
        print('REJECT original V physical example:',e)
    else:
        raise AssertionError('Original V example unexpectedly passed the physical corner check')
    print(json.dumps(run(HERE.with_name('worked-physical-replay-corrected.json')),indent=2))
