#!/usr/bin/env python3
"""Physical full-cube sensor placement theorem, with executable 54-sticker checks.

Sensor j: orientation bit of one ORIGINAL tagged edge cubie, not a stationary
edge-slot bit. A complete tagged-cubie state has 12 positions x 2 orientations.
The complete goal is all 54 facelets solved. A finite initial belief B is
globally contingently solvable (with unrestricted future HTM actions and
noiseless readings) iff its tagged-cubie factor vector is injective on B.
The closed factor and pairwise output separation are physical proof premises
checked for all twelve possible single tagged-edge sensors.
"""
from __future__ import annotations
import collections,itertools,json
from fullcube_goal_info_conflict import A,F,EDGES,physical_cube

PERMS,EDGE_SLOTS=physical_cube()
SOLVED=''.join(f*9 for f in F)

def turn(s,a):
    a=A.index(a) if isinstance(a,str) else a
    out=['?']*54
    for i,j in enumerate(PERMS[a]):out[j]=s[i]
    return ''.join(out)

def factor(s,tag):
    first,second=EDGES[tag]
    for pos,(i,j) in enumerate(EDGE_SLOTS):
        if {s[i],s[j]}=={first,second}:
            return 2*pos+int(s[i]!=first)
    raise AssertionError('missing original edge')

def single_edge_automaton(tag):
    representatives={factor(SOLVED,tag):SOLVED}
    pending=collections.deque([SOLVED])
    while pending:
        s=pending.popleft()
        for a in range(18):
            t=turn(s,a);q=factor(t,tag)
            if q not in representatives:
                representatives[q]=t;pending.append(t)
    assert set(representatives)==set(range(24))
    trans=[[factor(turn(representatives[q],a),tag)
            for q in range(24)] for a in range(18)]
    assert all(sorted(t)==list(range(24)) for t in trans)
    # Independent full-world witnesses for the quotient transition.
    for state in [SOLVED]+[turn(SOLVED,a) for a in range(18)]:
        for a in range(18):
            assert factor(turn(state,a),tag)==trans[a][factor(state,tag)]
    distances=collections.Counter()
    for x,y in itertools.combinations(range(24),2):
        if any(trans[a][x]%2!=trans[a][y]%2 for a in range(18)):
            distances[1]+=1
        elif any(trans[b][trans[a][x]]%2!=trans[b][trans[a][y]]%2
                 for a in range(18) for b in range(18)):
            distances[2]+=1
        else:raise AssertionError(('undistinguishable factor',tag,x,y))
    assert distances=={1:240,2:36}
    return dict(distances)

def depth_one_sensor_classes(tags):
    buckets=collections.defaultdict(list)
    for a in range(18):
        s=turn(SOLVED,a)
        buckets[tuple(factor(s,tag) for tag in tags)].append(A[a])
    hidden_faces=6-len({face for tag in tags for face in EDGES[tag]})
    indefinitely_indistinguishable_pairs=sum(
        len(v)*(len(v)-1)//2 for v in buckets.values())
    assert indefinitely_indistinguishable_pairs==(3*hidden_faces)*(3*hidden_faces-1)//2
    assert sorted(map(len,buckets.values()))==sorted(
        [1]*(3*(6-hidden_faces))+([3*hidden_faces] if hidden_faces else []))
    return indefinitely_indistinguishable_pairs

def audit():
    transition_spectrum={
        ''.join(EDGES[tag]):single_edge_automaton(tag)
        for tag in range(12)}
    distribution={}
    matching_sensors=[]
    for n in (1,2,3):
        counter=collections.Counter()
        for tags in itertools.combinations(range(12),n):
            count=depth_one_sensor_classes(tags)
            counter[count]+=1
            if n==3 and count==0:
                matching_sensors.append([''.join(EDGES[t]) for t in tags])
        distribution[str(n)]={str(k):v for k,v in sorted(counter.items())}
    assert distribution=={
        '1':{'66':12},
        '2':{'15':30,'36':36},
        '3':{'0':8,'3':96,'15':108,'36':8}}
    assert len(matching_sensors)==8
    # Goal-relativity: F and D differ in complete cube, yet the
    # original UR edge is already in the solved factor state.
    f,d=turn(SOLVED,'F'),turn(SOLVED,'D')
    assert f!=d and factor(f,0)==factor(d,0)==factor(SOLVED,0)
    return {
      'status':'FULL54_SENSOR_GOAL_THEOREM_CHECKS_PASS',
      'individual_sensor_automata_verified':12,
      'possible_tagged_edge_factor_states':24,
      'forward_separation_one_or_two_turns':{'1':240,'2':36},
      'sensor_count_to_impossible_pair_count_frequency':distribution,
      'minimum_sensors_for_all_eighteen_single_turn_states':3,
      'all_eight_minimal_face_cover_sensor_sets':matching_sensors,
      'unobservable_pair_formula':'binomial(3*(6-number_of_faces_touched_by_sensors),2)',
      'goal_relative_example':{'starts':['F','D'],
          'full_cube_goal':'IMPOSSIBLE_IN_ANY_HORIZON_WITH_UR_SENSOR',
          'tagged_UR_cubie_home_goal':'ALREADY_SATISFIED'},
      'constructive_upper_bound':'2*(|B|-1)+20 HTM for injective tagged factor projection',
      'scope':'noiseless tagged-edge orientation sensor; finite known belief; full 54-facelet cube goal',
      'global_new_algorithm_claim':False}
if __name__=='__main__':
    print(json.dumps(audit(),sort_keys=True,indent=2))
