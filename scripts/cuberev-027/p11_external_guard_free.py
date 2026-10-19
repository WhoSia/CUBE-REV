#!/usr/bin/env python3
"""Auditable fixed-original RubikOptimal replay without equal-axis strengthening.
Offline independent physical corner court; full run redoes real installed PDB audit."""
import collections
import hashlib
import inspect
import json
import pathlib
import sys

from p9_independent_optimal_probe import P, pos, FACE, check, selftest

TRIAX = (
 '            if UD_dist1 != 0 and UD_dist1 == RL_dist1 and RL_dist1 == FB_dist1:\n'
 '                if UD_dist1 + 1 >= togo:\n'
 '                    continue  # due to design of coordinate\n'
)
FIX = '            # P11: equal-axis extra cutoff entirely disabled.\n'
CORNER_POS = ((1,1,1),(-1,1,1),(-1,1,-1),(1,1,-1),
              (1,-1,1),(-1,-1,1),(-1,-1,-1),(1,-1,-1))
CORNER_IDX = {v:i for i,v in enumerate(CORNER_POS)}

def rank(p):
    a=list(p); b=0
    for j in range(7,0,-1):
        k=0
        while a[j]!=j:
            a[:j+1]=a[1:j+1]+a[:1]
            k+=1
            assert k<=j+1
        b=(j+1)*b+k
    assert 0<=b<40320
    return b

def corner_moves():
    marker=[]
    for v in CORNER_POS:
        sites=[i for i in range(54) if pos(i)==v and i//9 in (0,1)]
        assert len(sites)==1
        marker.append(sites[0])
    moves=[]
    for a in range(18):
        inv=[-1]*54
        for dst,src in enumerate(P[a]):
            assert inv[src]==-1
            inv[src]=dst
        perm=tuple(CORNER_IDX[pos(inv[marker[k]])] for k in range(8))
        assert sorted(perm)==list(range(8))
        for k,v in enumerate(CORNER_POS):
            for original in range(54):
                if pos(original)==v:
                    assert pos(inv[original])==CORNER_POS[perm[k]]
        moves.append(perm)
    return moves

def step(p,m):
    q=[None]*8
    for src,dst in enumerate(m): q[dst]=p[src]
    return tuple(q)

def build_corners():
    mm=corner_moves()
    start=tuple(range(8)); dist={start:0}; queue=collections.deque([start])
    while queue:
        p=queue.popleft()
        for m in mm:
            q=step(p,m)
            if q not in dist:
                dist[q]=dist[p]+1
                queue.append(q)
    assert len(dist)==40320
    raw=bytearray(40320)
    used=set()
    hist=collections.Counter(dist.values())
    for p,d in dist.items():
        i=rank(p)
        assert i not in used
        used.add(i);raw[i]=d
        descendants=[dist[step(p,m)] for m in mm]
        assert all(abs(d-v)<=1 for v in descendants)
        assert d==0 or d-1 in descendants
    assert len(used)==40320
    print('P11_PHYSICAL_INDEPENDENT_CORNER_40320_PASS',json.dumps(dict(sorted(hist.items()))),flush=True)
    print('P11_PHYSICAL_CORNER_40320_SHA256',hashlib.sha256(raw).hexdigest(),flush=True)
    return mm,dist,raw

def mod3_lemma():
    n=0
    for d in range(64):
        for succ in (d-1,d,d+1):
            if succ<0:continue
            same=[z for z in (d-1,d,d+1) if z>=0 and z%3==succ%3]
            assert same==[succ]
            n+=1
    assert n==191
    print('P11_MOD3_NEIGHBOR_DISTANCE_LEMMA_PASS',n,flush=True)

def compare_all_corner_table(mm,dist,raw):
    import optimal.moves as mv
    import optimal.pruning as pr
    assert len(pr.corner_depth)==40320
    assert len(mv.corners_move)==40320*18
    n=0
    for p,d in dist.items():
        i=rank(p)
        assert int(pr.corner_depth[i])==d,('corner PDB mismatch',i,d)
        for a,m in enumerate(mm):
            assert int(mv.corners_move[18*i+a])==rank(step(p,m)),('corner transition mismatch',i,a)
            n+=1
    assert n==725760
    print('P11_ACTUAL_PYPI_ALL_CORNER_DISTANCES_AND_MOVES_PASS',len(dist),n,flush=True)
    assert all(int(pr.distance[3*d+v%3])==v for d in range(18)
               for v in (d-1,d,d+1) if v>=0)
    print('P11_ACTUAL_PYPI_MOD3_RECONSTRUCTION_PASS',flush=True)

def remove_guard(src):
    if src.count(TRIAX)!=1:raise ValueError('source branch mismatch: FAIL CLOSED')
    out=src.replace(TRIAX,FIX)
    assert out.replace(FIX,TRIAX)==src
    for t in ('co_dist1 >= togo','UD_dist1 >= togo',
              'RL_dist1 >= togo','FB_dist1 >= togo'):
        if out.count(t)!=1:raise ValueError('base prune missing/duplicated '+t)
    assert 'UD_dist1 + 1 >= togo' not in out
    compile(out,'<P11-conservative-search>','exec')
    return out

def patch_negative_tests():
    sample=('def search(co_dist1,UD_dist1,RL_dist1,FB_dist1,togo):\n'
            '    for x in range(1):\n'
            '            if co_dist1 >= togo: return 0\n'
            '            if UD_dist1 >= togo: return 0\n'
            '            if RL_dist1 >= togo: return 0\n'
            '            if FB_dist1 >= togo: return 0\n'
            + TRIAX+'            return 1\n')
    ns1={};ns2={}
    exec(sample,ns1);exec(remove_guard(sample),ns2)
    assert ns1['search'](0,2,2,2,3) is None
    assert ns2['search'](0,2,2,2,3)==1
    assert ns1['search'](0,1,2,2,3)==ns2['search'](0,1,2,2,3)==1
    for corrupt in (sample.replace(TRIAX,''),sample.replace('FB_dist1 >= togo','FB_dist1 > togo')):
        try:remove_guard(corrupt)
        except ValueError:pass
        else:raise AssertionError('invalid patch input accepted')
    print('P11_GUARD_FREE_FAIL_CLOSED_MUTATION_TESTS_PASS',flush=True)

def main():
    mod3_lemma();patch_negative_tests()
    mm,dist,raw=build_corners()
    if '--offline' in sys.argv:return
    selftest()
    print('P11_THIRD_PARTY_TABLE_LOADING_STARTED',flush=True)
    import optimal.solver as solver
    original=inspect.getsource(solver.search)
    patched=remove_guard(original)
    name=pathlib.Path(inspect.getfile(solver.search))
    print('P11_INSTALLED_PYPI_SOURCE_SHA256',hashlib.sha256(name.read_bytes()).hexdigest(),flush=True)
    print('P11_ORIGINAL_SEARCH_SHA256',hashlib.sha256(original.encode()).hexdigest(),flush=True)
    print('P11_GUARD_FREE_SEARCH_SHA256',hashlib.sha256(patched.encode()).hexdigest(),flush=True)
    compare_all_corner_table(mm,dist,raw)
    exec(compile(patched,'<P11-conservative-search>','exec'),solver.__dict__)
    assert solver.search.__code__.co_filename=='<P11-conservative-search>'
    print('P11_NONTRIVIAL_EQUAL_TRIAXIAL_CUTOFF_DISABLED_PASS',flush=True)
    res=solver.solve(FACE)
    print('P11_NO_EQUAL_AXIS_SOLVER_RAW',repr(res),flush=True)
    print('P11_NO_EQUAL_AXIS_PHYSICAL_WITNESS_PASS',json.dumps(check(res),sort_keys=True),flush=True)
    print('P11_OPTIMUM_STILL_DEPENDS_ON_CORRECT_THREE_AXIS_PDB',flush=True)

if __name__=='__main__':main()
