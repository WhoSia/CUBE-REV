#!/usr/bin/env python3
"""R14-P8.23: exactly classify pointwise stabilizers of persistent original
cubie tags in the entire legal 3x3 fixed-centre Rubik group.

No cube word-distance code or P48 positive certificate imported here.
This is an independent finite algebraic witness enumerator: permutation
parity, mod-3 corner orientation sum and mod-2 edge flip sum.

The radius-10 statement also uses the *external, published* symmetric
18-HTM Rubik group diameter D=20, NOT a new diameter computation:
B_10^{-1} B_10 = B_20 = G, so an identifying B10 tag set is exactly
a full-group pointwise stabilizer base.
"""
from collections import Counter
from itertools import combinations, permutations, product
from math import factorial, comb
import json

CORNERS=tuple(range(8))
EDGES=tuple(range(12))
def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def modzero_vectors(length,base):
    for v in product(range(base),repeat=length):
        if sum(v)%base==0:
            yield v

def stabilizer_count(ncorners,nedges):
    """Explicitly enumerate legal permutations and orientations of unobserved
    ORIGINAL cubies while fixing all observed cubies in position+orientation.
    """
    pc=tuple(p for p in permutations(range(ncorners)))
    pe=tuple(p for p in permutations(range(nedges)))
    nori_c=sum(1 for _ in modzero_vectors(ncorners,3))
    nori_e=sum(1 for _ in modzero_vectors(nedges,2))
    pairs=sum(1 for c in pc for e in pe if parity(c)==parity(e))
    return pairs*nori_c*nori_e

assert stabilizer_count(0,0)==1
assert stabilizer_count(1,1)==1
assert stabilizer_count(2,0)==3
assert stabilizer_count(0,2)==2
assert stabilizer_count(3,0)==27
assert stabilizer_count(0,3)==12
assert stabilizer_count(2,1)==3
assert stabilizer_count(1,2)==2
assert stabilizer_count(2,2)==12

# Independently examine EVERY omission shape of 0..3 original tags:
# the same result holds for all labels of a shape (legal Rubik cubie
# constraints are label-invariant in the full global state space).
global_bases=Counter()
global_nonbases=Counter()
stabilizer_histogram={}
for omissions in range(4):
    record=Counter()
    for ncorner in range(max(0,omissions-12),min(omissions,8)+1):
        nedge=omissions-ncorner
        if nedge>12:
            continue
        multiplicity=comb(8,ncorner)*comb(12,nedge)
        hsize=stabilizer_count(ncorner,nedge)
        record[str(hsize)]+=multiplicity
        if hsize==1:
            global_bases[20-omissions]+=multiplicity
        else:
            global_nonbases[20-omissions]+=multiplicity
    assert sum(record.values())==comb(20,omissions)
    stabilizer_histogram[str(20-omissions)]=dict(record)
assert global_bases=={20:1,19:20,18:96}
assert global_nonbases=={18:94,17:1140}
# Every set with <=16 observed tags is also non-identifying:
# its missing set contains two missing corners or two missing edges,
# and these alone already yield an explicit nonidentity stabilizer.
full_group_order=factorial(8)*3**7*factorial(12)*2**11//2
assert full_group_order==43252003274489856000

# From old B6 physically certified positive layout counts:
# 16 (2C+2E omissions), 17 (528 1C2E + 144 2C1E), and
# 18 (96 1C1E + 66 2E + 12 2-adjacent-C omissions).
b6_residual={
    '16':{'order_12':156},
    '17':{'order_2':528,'order_3':144},
    '18':{'order_1':96,'order_2':66,'order_3':12},
    '19':{'order_1':20},
    '20':{'order_1':1},
}
assert sum(b6_residual['17'].values())==672
assert sum(b6_residual['18'].values())==174

# Rigorous interval: b6=16 by the inherited B6 certificate,
# b10=18 by |G| diameter 20 (HTM), and monotonicity in radius.
# The minimum b7..b9 remains UNKNOWN here. No exact jump date claimed.
print(json.dumps({
 'status':'R14_P823_FULL_GROUP_BASE_AND_RADIUS10_BRIDGE_FINITE_ALGEBRA_PASS',
 'legal_group_order':full_group_order,
 'full_group_minimum_tag_sensors':18,
 'full_group_optimum_designs':96,
 'full_group_identifying_sensor_counts':{'18':96,'19':20,'20':1},
 'full_group_all_0_to_3_omission_stabilizer_histogram':stabilizer_histogram,
 'B6_certified_layouts_residual_global_stabilizer_orders':b6_residual,
 'B6_minimum_tag_sensors_inherited':16,
 'B10_minimum_tag_sensors_conditional_on_published_HTM_diameter20':18,
 'unknown_radii':['B7','B8','B9'],
 'B6_min16_stabilizer_size':12,
 'physical_distance_search_executed':False,
 'diameter20_derived_here':False,
},sort_keys=True))
