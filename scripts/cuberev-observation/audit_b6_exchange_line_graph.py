#!/usr/bin/env python3
"""Explain the B6 156-optimum swap graph through the cube edge line graph.

Inputs: geometrically defined 13 accepted omitted-edge pairs per adjacent
omitted-corner core, independently P48-validated by the B6 41-class MITM.
The script does NOT itself certify 13-HTM exclusion; its theorem is the
exact local-to-global combinatorial structure of that certified family.

A graph edge swaps exactly one selected sensor (equivalently one omitted
cubie); we reason on FOUR OMITTED physical cubie positions.
"""
from collections import Counter, defaultdict
from itertools import combinations
from b6_independent_48sticker_goals import (
    CORNERS, EDGE_NAMES, EDGE_POS, EDGE_POSITION, edge_ends, valid_pairs
)

def positive_omissions():
    layouts={}
    for core in EDGE_NAMES:
        for pair in valid_pairs(core):
            removed=frozenset(edge_ends(core) |
                              frozenset(EDGE_POSITION[e] for e in pair))
            if removed in layouts:
                raise AssertionError("duplicate positive four-cubie omission")
            layouts[removed]=(core,frozenset(pair))
    assert len(layouts)==156
    return layouts

def swap_graph(layouts):
    graph={p:set() for p in layouts}
    for a,b in combinations(layouts,2):
        if len(a.symmetric_difference(b))==2:
            graph[a].add(b)
            graph[b].add(a)
    return graph

def components(graph):
    unvisited=set(graph)
    result=[]
    while unvisited:
        root=next(iter(unvisited));stack=[root];unvisited.remove(root)
        component=set()
        while stack:
            vertex=stack.pop();component.add(vertex)
            for neighbor in graph[vertex]&unvisited:
                unvisited.remove(neighbor);stack.append(neighbor)
        result.append(frozenset(component))
    return sorted(result,key=lambda c:(-len(c),repr(sorted(c))))

def audit():
    layouts=positive_omissions()
    graph=swap_graph(layouts)
    assert all(u in graph[v] for v in graph for u in graph[v])
    groups=components(graph)
    sizes=Counter(map(len,groups))
    assert sizes==Counter({96:1,4:12,1:12}),sizes
    assert sum(map(len,graph.values()))//2==336

    per_core=defaultdict(list)
    for omitted,(core,pair) in layouts.items():
        per_core[core].append(omitted)
    assert len(per_core)==12 and set(map(len,per_core.values()))=={13}

    giant=next(group for group in groups if len(group)==96)
    squares=[group for group in groups if len(group)==4]
    isolates=[group for group in groups if len(group)==1]
    for c in squares:
        assert len({layouts[x][0] for x in c})==1
        assert all(len(graph[v])==2 and graph[v]<=c for v in c)
        assert sum(len(graph[v]) for v in c)//2==4
    for c in isolates:
        assert len(next(iter(c)) & set(CORNERS))==2
        assert len(graph[next(iter(c))])==0
    assert Counter(layouts[next(iter(g))][0] for g in squares)==Counter({h:1 for h in EDGE_NAMES})
    assert Counter(layouts[next(iter(g))][0] for g in isolates)==Counter({h:1 for h in EDGE_NAMES})
    assert Counter(layouts[v][0] for v in giant)==Counter({h:8 for h in EDGE_NAMES})
    assert Counter(len(graph[v]) for v in giant)==Counter({7:48,6:24,4:24})

    intra=Counter()
    cross=Counter()
    for a,b in combinations(giant,2):
        if b not in graph[a]:continue
        h,k=layouts[a][0],layouts[b][0]
        if h==k:intra[h]+=1
        else:cross[frozenset((h,k))]+=1
    assert intra==Counter({h:18 for h in EDGE_NAMES})
    assert len(cross)==24 and set(cross.values())=={3}

    cube_line_edges={frozenset((a,b)) for a,b in combinations(EDGE_NAMES,2)
                     if edge_ends(a)&edge_ends(b)}
    assert len(cube_line_edges)==24
    assert set(cross)==cube_line_edges, (
        "the large component quotient is not the line graph of Q3")
    # The quotient has degree four at each cube-edge vertex because each
    # cube edge has two endpoints with two other incident cube edges each.
    quotient_degrees=Counter(h for pair in cross for h in pair)
    assert quotient_degrees==Counter({h:4 for h in EDGE_NAMES})
    assert sum(intra.values())==216 and sum(cross.values())==72
    assert sum(intra.values())+sum(cross.values())+12*4==336

    print("B6_EXCHANGE_CUBE_LINE_GRAPH_QUOTIENT_PASS 12 vertices 24 edges 3 links per incident pair")
    print("B6_EXCHANGE_PER_CORE_FIBERS_PASS eight giant + four C4 + one isolate")
    print("B6_EXCHANGE_25_COMPONENTS_PASS 96 + 12x4 + 12x1 = 156")
    print("B6_EXCHANGE_336_EDGES_PASS giant internal 216 giant cross 72 squares 48")
    print("B6_EXCHANGE_LARGE_DEGREES_PASS",dict(sorted(Counter(len(graph[v]) for v in giant).items())))
    print("BOUNDARY local finite structural explanation, not a general cube-base exchange law")
    return {"vertices":156,"edges":336,"components":sizes,
            "cube_line_graph_edges":len(cross),"links_per_incident_core_pair":3,
            "giant_internal_edges":sum(intra.values()),
            "giant_external_edges":sum(cross.values()),
            "square_edges":48}

if __name__=="__main__":
    audit()
