#!/usr/bin/env python3
"""Exact source-family antichain theorem independent of cube move enumerations.

For every state-identification dictionary, injectivity on B implies
injectivity on any A subset B; hence replacing R by its unique inclusion-
maximal antichain does not change M_T(R,L) for ANY length or transducer.
"""
import argparse,hashlib,json,itertools,collections
from pathlib import Path
P=argparse.ArgumentParser()
P.add_argument('--physical',required=True)
P.add_argument('--output',required=True)
a=P.parse_args();raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
R=json.loads(raw)['bases'];assert len(R)==1192 and len(set(R))==1192
assert collections.Counter(x.bit_count() for x in R)=={3:220,4:492,5:480}
maxima=[m for m in R if not any(n!=m and m&n==m for n in R)]
assert len(maxima)==544
assert collections.Counter(m.bit_count() for m in maxima)=={5:480,4:64}
assert all(any(m&z==m for z in maxima) for m in R)
assert all(not any(m!=n and m&n==m for n in maxima) for m in maxima)
F={1,5,8,9};B={3,7,10,11};Q=set(range(12))
q4=[m for m in maxima if m.bit_count()==4]
r5=[m for m in maxima if m.bit_count()==5]
assert len(q4)==64 and len(r5)==480
expected=set()
for face in (F,B):
 for tri in itertools.combinations(sorted(face),3):
  for extra in Q-face:
   expected.add(sum(1<<x for x in (*tri,extra)))
assert len(expected)==64 and set(q4)==expected
# Exactly 72 elements lie outside the downward closure of the admitted
# 480 five-element sources: 64 cross-face quartets and eight face triples.
not_implied_by_R5=[m for m in R if not any(m&f==m for f in r5)]
assert collections.Counter(x.bit_count() for x in not_implied_by_R5)=={3:8,4:64}
assert set(x for x in not_implied_by_R5 if x.bit_count()==4)==set(q4)
face_tris=set(sum(1<<x for x in tri) for face in (F,B) for tri in itertools.combinations(sorted(face),3))
assert set(x for x in not_implied_by_R5 if x.bit_count()==3)==face_tris
assert all(sum(t&q==t for q in q4)==8 for t in face_tris)
# All eight face-triples are covered by the 64 primitive quartets, and all
# other original requirements lie in the downward shadow of R5.
assert all(any(m&z==m for z in maxima) for m in R)
receipt={'result':'CUBE_REV_019_ORIGINAL_SOURCE_MAXIMAL_544_480PLUS64_ANTICHAIN_EXACT_GEOMETRY_PASS',
 'physical_source_sha256':sha,'original_source_count':len(R),'unique_inclusion_maximal_count':len(maxima),
 'maximal_cardinality_histogram':{'5':480,'4':64},
 'outside_original_R5_downward_shadow':{'3':8,'4':64},
 'eight_face_triples_each_contained_in_exactly_eight_primitive_quartets':True,
 'quartet_pattern':'three of four edge positions from F={1,5,8,9} or B={3,7,10,11}, plus one of 8 off-face positions',
 'all_dictionary_lengths_and_executable_word_families_preserved':True,
 'reason':'injectivity of a word on any source B implies its injectivity on every A subset B; finite inclusion-maximal generators form a unique antichain'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'])