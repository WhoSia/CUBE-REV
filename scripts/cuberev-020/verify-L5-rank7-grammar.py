#!/usr/bin/env python3
"""P1-E independent rank-seven face grammar, transported-cut signatures and D4xC2 orbits.
Consumes 640-row C++ rank7.csv; validates against frozen ORIGINAL physical input SHA.
A separate C++ census covers all 18^5 words; this Python file checks witnesses/grammar.
"""
import argparse
import collections
import csv
import hashlib
import itertools
import json
from pathlib import Path

ORIGINAL_SHA="9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1"
INFO={6,7,15,16}
HALF=(2,5,11,14)
QUARTER=(0,1,3,4,9,10,12,13)
E=frozenset((0,2,4,6))
SLOTS=("UR","UF","UL","UB","RD","FD","DL","DB","RF","FL","LB","RB")

def grammar3():
    out=set()
    for outer in (6,15):
        opp=15 if outer==6 else 6
        for first,last in itertools.product((outer,outer+1),repeat=2):
            for i,h in enumerate(HALF):
                for j,k in enumerate(HALF):
                    delta=(j-i)%4
                    if delta==0:continue
                    if delta==2:middle=(opp,opp+1)
                    elif delta==1:middle=(opp if outer==6 else opp+1,)
                    else:middle=(opp+1 if outer==6 else opp,)
                    for m in middle:out.add((first,h,m,k,last))
    assert len(out)==128
    return out

def grammar4():
    out=set()
    faces=((6,7),(15,16))
    for before in ((0,1),(1,0)):
        for after in ((0,1),(1,0)):
            for a,b,d,e in itertools.product(faces[before[0]],faces[before[1]],
                                                faces[after[0]],faces[after[1]]):
                for c in QUARTER:out.add((a,b,c,d,e))
    assert len(out)==512
    return out

def canonical(xs):
    labels={};key=0
    for i,x in enumerate(xs):
        if x not in labels:labels[x]=len(labels)
        key|=labels[x]<<(4*i)
    return key

def blocks(key):
    families=collections.defaultdict(set)
    for i in range(12):families[(key>>(4*i))&15].add(i)
    return list(families.values())

def direct(maps,word):
    position=[2*i for i in range(12)]
    bits=[0]*12
    cuts=[]
    for a in word:
        before=position
        position=[maps[a][x] for x in before]
        cuts.append(sum(1<<i for i in range(12) if (before[i]&1)!=(position[i]&1)))
        bits=[(u<<1)|(x&1) for u,x in zip(bits,position)]
    return canonical(bits),cuts

def symmetry_group():
    dirs="URDL"
    lookup={frozenset(s):i for i,s in enumerate(SLOTS)}
    G=set()
    for n in range(4):
        for flip in (False,True):
            for swap in (False,True):
                p={x:dirs[(dirs.index(x)+n)%4] for x in dirs}
                if flip:p={x:{"U":"U","R":"L","D":"D","L":"R"}[p[x]] for x in dirs}
                p["F"]="B" if swap else "F"
                p["B"]="F" if swap else "B"
                G.add(tuple(lookup[frozenset(p[x] for x in s)] for s in SLOTS))
    assert len(G)==16
    return G

def mapped(key,perm):
    before=[(key>>(4*i))&15 for i in range(12)]
    after=[0]*12
    for i,j in enumerate(perm):after[j]=before[i]
    return canonical(after)

def main(a):
    blob=a.source.read_bytes()
    sha=hashlib.sha256(blob).hexdigest()
    assert sha==ORIGINAL_SHA,("unfrozen input",sha)
    maps=[[int(x) for x in s.split()] for s in a.maps.read_text().splitlines()]
    assert len(maps)==18
    assert all(sorted(x)==list(range(24)) for x in maps)
    assert [i for i,m in enumerate(maps) if any(m[2*p]&1 for p in range(12))]==sorted(INFO)
    assert all(maps[move][p*2]//2 in E for move in INFO|set(HALF) for p in E)
    group={3:set(),4:set()}
    words={3:set(),4:set()}
    tallies=collections.Counter()
    with a.records.open(newline="") as f:
        for row in csv.DictReader(f):
            q=int(row["q"])
            assert q in (3,4)
            word=tuple(int(row["a"+str(i)]) for i in range(5))
            key=int(row["key"])
            cuts=[int(row["c"+str(i)]) for i in range(5)]
            assert word not in words[q]
            words[q].add(word)
            assert sum(i in INFO for i in word)==q
            assert direct(maps,word)==(key,cuts)
            block=blocks(key)
            assert len(block)==7
            active=[v for v in cuts if v]
            assert len(active)==q and all(v.bit_count()==4 for v in active)
            if q==3:
                assert [i for i,v in enumerate(cuts) if v]==[0,2,4]
                assert sorted(map(len,block),reverse=True)==[4,2,2,1,1,1,1]
                assert any(s==E for s in block)
                assert [ (active[i]&active[j]).bit_count()
                         for i,j in itertools.combinations(range(3),2)]==[1,2,1]
                assert active[0]&active[1]&active[2]==0
                assert (active[0]|active[1]|active[2]).bit_count()==8
            else:
                assert [i for i,v in enumerate(cuts) if v]==[0,1,3,4]
                assert sorted(map(len,block),reverse=True)==[3,3,2,1,1,1,1]
                pair=[(active[i]&active[j]).bit_count()
                      for i,j in itertools.combinations(range(4),2)]
                assert pair in ([0,3,0,0,3,0],[0,0,3,3,0,0]),pair
                union=active[0]|active[1]|active[2]|active[3]
                assert union.bit_count()==10
                assert sum(not(union>>i&1) for i in E)==2
            group[q].add(key)
            tallies[q]+=1
    assert words[3]==grammar3()
    assert words[4]==grammar4()
    assert tallies=={3:128,4:512},tallies
    assert len(group[3])==len(group[4])==16
    assert not group[3]&group[4]
    # Independent proof of orbital splitting on the actual 12-position labels.
    G=symmetry_group()
    orbits={}
    for q in (3,4):
        remaining=set(group[q]);parts=[]
        while remaining:
            key=min(remaining)
            orb={mapped(key,g) for g in G}
            assert orb<=group[q]
            remaining-=orb
            parts.append(len(orb))
        orbits[q]=sorted(parts)
    assert orbits=={3:[16],4:[8,8]}
    print(json.dumps({
       "result":"CUBE_REV_020_P1E_REAL_CUBE_RANK7_GRAMMAR_ORBITS_PASS",
       "source_sha256":sha,"rank7_word_counts":{"q3":128,"q4":512},
       "partition_counts":{"q3":16,"q4":16,"overlap":0},
       "block_profiles":{"q3":[4,2,2,1,1,1,1],
                         "q4":[3,3,2,1,1,1,1]},
       "symmetry_orbits":{"q3":[16],"q4":[8,8]},
       "complete_all_18pow5_census":"REQUIRED_SEPARATE_CPP_VERIFIER",
       "external_ci":"NOT_YET_CONFIRMED"},sort_keys=True,indent=2))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True,type=Path)
    parser.add_argument("--maps",required=True,type=Path)
    parser.add_argument("--records",required=True,type=Path)
    main(parser.parse_args())
