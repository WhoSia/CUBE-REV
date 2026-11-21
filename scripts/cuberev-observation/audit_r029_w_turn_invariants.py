#!/usr/bin/env python3
"""Derive finite generator invariants for full physical cube legality.

For each of twelve face quarter turns, derive the source cubie permutation
and per-position edge-flip / corner-twist offsets from the 48-slot geometry.
The sum congruences extend to all turn words by composition (the offsets
are permuted before addition). The generated tables are potential Lean inputs.
"""
import json
from audit_r029_w_corner_geometric_decoder import geometry
from audit_r029_w_transport_all_prefixes import permutation_parity


def read_action(row,base,count,size):
    perm=[]
    offset=[]
    for p in range(count):
        origin=[row[base+size*p+j] for j in range(size)]
        assert all(base<=v<base+size*count for v in origin)
        q=(origin[0]-base)//size
        assert all((v-base)//size==q for v in origin)
        local=tuple((v-base)%size for v in origin)
        shift=local[0]
        assert local==tuple((j+shift)%size for j in range(size)),(p,local)
        perm.append(q)
        offset.append(shift)
    assert sorted(perm)==list(range(count))
    return perm,offset


def run():
    all_moves=geometry()
    results=[]
    for t,row in enumerate(all_moves):
        eperm,eflip=read_action(row,0,12,2)
        cperm,ctwist=read_action(row,24,8,3)
        assert sum(eflip)%2==0,(t,eflip)
        assert sum(ctwist)%3==0,(t,ctwist)
        assert permutation_parity(eperm)==permutation_parity(cperm),(t,eperm,cperm)
        results.append({'turn':t,'edge_source_positions':eperm,'edge_flip_offsets':eflip,
                        'corner_source_positions':cperm,'corner_twist_offsets':ctwist,
                        'sign':permutation_parity(eperm)})
    assert len(results)==12
    return {'status':'PASS','face_quarter_turns':12,
            'edge_flip_offset_sum_mod2':[sum(x['edge_flip_offsets'])%2 for x in results],
            'corner_twist_offset_sum_mod3':[sum(x['corner_twist_offsets'])%3 for x in results],
            'edge_corner_signs_agree':True,
            'generator_table':results,
            'consequence':'Every legal turn word preserves flip parity, twist sum and equality of the edge/corner permutation signs.'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
