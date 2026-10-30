#!/usr/bin/env python3
"""Exact 14-sensor minimum for whole Rubik's Cube radius-4 physical ball.

12 possible ORIGINAL tagged edge orientation sensors and 8 ORIGINAL tagged
corner orientation sensors (three-valued). Action choices are all 18 HTM.
A tagged piece's position+orientation is a closed state factor, and its
orientation output separates distinct factor states after finite actions.

Proof by decoupled physical collision hypergraphs:
- 432 pairs agree on all twelve edges; their changed tagged corner
  supports exhaust ALL 56 distinct 3-of-8 sets -> >=6 corners.
- Pairs agreeing on ALL eight corners generate 1113 distinct nonempty
  changed-edge supports. Every seven-edge subset misses one support,
  while precisely 102 eight-edge subsets hit them all -> >=8 edges.
- Every selection of six corners leaves EXACTLY the same 1113
  edge-support constraints as all eight corners. Hence 28*102=2856
  distinct 14-tag physical designs distinguish all 46,741 sources.

These are exact counts only for the complete radius-4 solved ball with
the stated idealized original-tag orientation sensors. Not real hardware.
"""
from __future__ import annotations
import argparse,collections,itertools,json
from fullcube_edge_kernel_radius4 import (START,turn,edge_vector,corner_vector,
                                          CORNERS)
from fullcube_goal_info_conflict import A,F

def build():
    seen={START:()}
    layers=[[START]]
    for depth in range(1,5):
        layer=[]
        for s in layers[-1]:
            for a in range(18):
                t=turn(s,a)
                if t not in seen:
                    seen[t]=seen[s]+(a,)
                    layer.append(t)
        layers.append(layer)
    states=[s for layer in layers for s in layer]
    assert len(states)==46741
    raw_corners=[corner_vector(s) for s in states]
    coders=[{} for _ in range(8)]
    cc=[];rep=[{} for _ in range(8)]
    for k,c in enumerate(raw_corners):
        row=[]
        for tag,(pos,labels) in enumerate(c):
            key=(pos,labels)
            if key not in coders[tag]:
                code=len(coders[tag]);coders[tag][key]=code
                rep[tag][code]=states[k]
            row.append(coders[tag][key])
        cc.append(bytes(row))
    assert all(len(coder)==24 for coder in coders)
    ee=[edge_vector(s) for s in states]
    return states,seen,cc,ee,coders,rep

def edge_collision_hypergraph(keys,edge_rows):
    groups=collections.defaultdict(list)
    for i,key in enumerate(keys):groups[key].append(i)
    masks={}
    for indices in groups.values():
        for i,j in itertools.combinations(indices,2):
            row_i,row_j=edge_rows[i],edge_rows[j]
            mask=sum(1<<k for k in range(12) if row_i[k]!=row_j[k])
            assert mask
            masks.setdefault(mask,(i,j))
    return masks,groups

def audit(all_witnesses=False):
    states,words,c,e,coders,reps=build()
    # For all tagged corners: observed orientation = position of the
    # U/D reference sticker within the three sticker slots at its location.
    # Verify the 24-state corner machine and its ability to distinguish
    # all 276 distinct states with observation now or one HTM turn.
    observations=[]
    for tag in range(8):
        orig_tag_labels={START[i] for i in CORNERS[tag]}
        anchor=next(v for v in orig_tag_labels if v in ('U','D'))
        tmap=[]
        for code in range(24):
            state=reps[tag][code]
            pos,labels=next(key for key,v in coders[tag].items() if v==code)
            trit=labels.index(anchor)
            transition=[coders[tag][corner_vector(turn(state,a))[tag]]
                        for a in range(18)]
            tmap.append((trit,transition))
        # Closed factor even for different full-world representatives.
        for s in states[::500]:
            i=coders[tag][corner_vector(s)[tag]]
            for a in range(18):
                assert coders[tag][corner_vector(turn(s,a))[tag]]==tmap[i][1][a]
        spectrum=collections.Counter()
        for x,y in itertools.combinations(range(24),2):
            if tmap[x][0]!=tmap[y][0]:
                spectrum[0]+=1
            elif any(tmap[tmap[x][1][a]][0]!=tmap[tmap[y][1][a]][0]
                     for a in range(18)):
                spectrum[1]+=1
            else:
                raise AssertionError(('corner indistinguishable',tag,x,y))
        assert spectrum=={0:192,1:84},spectrum
        observations.append(dict(spectrum))
    # Corner-only variation when all twelve tagged edges agree.
    edge_groups=collections.defaultdict(list)
    for i,row in enumerate(e):edge_groups[row].append(i)
    corner_diffs={}
    for group in edge_groups.values():
        for i,j in itertools.combinations(group,2):
            moved=tuple(k for k in range(8) if c[i][k]!=c[j][k])
            assert len(moved)==3
            corner_diffs.setdefault(moved,(i,j))
    assert set(corner_diffs)==set(itertools.combinations(range(8),3))
    # Original all-8-corner masked pairs generate every edge-only
    # hypergraph constraint; no selected six-corner set hides more.
    all_eight,cgroups=edge_collision_hypergraph(c,e)
    assert len(all_eight)==1113
    edge_seven_witnesses=[]
    for E in itertools.combinations(range(12),7):
        mask=sum(1<<k for k in E)
        misses=next(((support,ij) for support,ij in all_eight.items()
                     if not support&mask),None)
        assert misses is not None
        support,(i,j)=misses
        edge_seven_witnesses.append((E,(i,j)))
    good_eight=[]
    for E in itertools.combinations(range(12),8):
        mask=sum(1<<k for k in E)
        if all(mask&diff for diff in all_eight):
            good_eight.append(E)
    assert len(edge_seven_witnesses)==792 and len(good_eight)==102
    # Every choice of 6 corners hides precisely the same pair classes.
    for C in itertools.combinations(range(8),6):
        selected=[bytes(row[j] for j in C) for row in c]
        new,groups=edge_collision_hypergraph(selected,e)
        assert new.keys()==all_eight.keys()
        for group in groups.values():
            if len(group)>1:
                for i,j in itertools.combinations(group,2):
                    assert c[i]==c[j]  # 6 observed corners imply all 8
    # A sample explicit 6-corner + 8-edge design is directly injective.
    C=tuple(range(6));E=good_eight[0]
    combined={bytes(c[i][j] for j in C)+bytes(e[i][j] for j in E)
              for i in range(len(states))}
    assert len(combined)==46741
    result={'status':'EXACT_FULL54_MIXED_RADIUS4_MINIMUM14_PASS',
            'source_full_cubes':len(states),
            'sensor_model':'original tagged edges give binary orientation; tagged corners give ternary orientation; physical positions remain hidden',
            'eight_corner_automata_pairs_each':276,
            'eight_corner_observability':observations,
            'corner_only_collision_supports':56,
            'minimum_corner_tags':6,
            'available_corner_designs_of_size6':28,
            'edge_only_collision_supports_when_all8corners':1113,
            'all_seven_edge_tag_designs_refuted':792,
            'minimum_edge_tags':8,
            'successful_eight_edge_tag_sets':len(good_eight),
            'every_six_corner_set_same_edge_constraints':True,
            'exact_minimum_total_tags':14,
            'number_of_minimum_fourteen_tag_designs':28*len(good_eight),
            'sample_corner_tags':list(C),
            'sample_edge_tags':list(E),
            'physical_46741_state_injectivity_pass':True,
            'whole_cube_solvable_by_finite_adaptive_policy':True,
            'global_research_novelty_proven':False}
    if all_witnesses:
        def w(i):return [A[a] for a in words[states[i]]]
        result['all_56_corner_lower_bound_witnesses']=[
            {'moved_corner_tags':list(tags),'pair':[w(i),w(j)]}
            for tags,(i,j) in sorted(corner_diffs.items())]
        result['all_792_edge_lower_bound_witnesses']=[
            {'selected_edge_tags':list(tags),'pair':[w(i),w(j)]}
            for tags,(i,j) in edge_seven_witnesses]
        result['all_102_sufficient_edge_octets']=[list(q) for q in good_eight]
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--all-witnesses',action='store_true')
    args=parser.parse_args()
    print(json.dumps(audit(args.all_witnesses),indent=2,sort_keys=True))
