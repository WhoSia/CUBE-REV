#!/usr/bin/env python3
"""Exact 54-facelet adaptive goal-solving case for hidden U/U' states.

Geometry ported from CUBE-REV 0.24 physical sticker coordinate engine.
At each action the agent observes orientation of ORIGINAL UR cubie.
Full goal success requires all hidden-world candidates solved, not merely
identification. No erasure/noisy readings in this particular experiment.
"""
from functools import lru_cache
import json
F='URFDLB'
N={'U':(0,1,0),'R':(1,0,0),'F':(0,0,1),'D':(0,-1,0),'L':(-1,0,0),'B':(0,0,-1)}
G={'U':(1,1,-1),'R':(0,1,-1),'F':(2,1,-1),'D':(1,-1,1),'L':(0,-1,1),'B':(2,-1,1)}
A=tuple(f+s for f in F for s in ('',"'",'2'))
def rot(v,ax,n):
    x,y,z=v
    for _ in range(n%4):
        if ax==0:y,z=-z,y
        elif ax==1:x,z=z,-x
        else:x,y=-y,x
    return x,y,z
def geometry():
    slots=[]
    for face in F:
        n=N[face];row=[]
        for x in (-1,0,1):
            for y in (-1,0,1):
                row.append(((n[0],x,y) if n[0] else ((x,n[1],y) if n[1] else (x,y,n[2])),n))
        row.sort(key=lambda q:','.join(map(str,q[0])))
        slots+=row
    loc={s:i for i,s in enumerate(slots)}
    assert len(loc)==54
    perms=[]
    for action in A:
        ax,ly,q=G[action[0]]
        power=3 if action.endswith("'") else 2 if action.endswith('2') else 1
        perms.append(tuple(loc[(rot(p,ax,q*power),rot(n,ax,q*power))] if p[ax]==ly else loc[(p,n)] for p,n in slots))
    edges=[]
    pairs=(('U','R'),('U','F'),('U','L'),('U','B'),('D','R'),('D','F'),
           ('D','L'),('D','B'),('F','R'),('F','L'),('B','L'),('B','R'))
    for f,g in pairs:
        n,m=N[f],N[g];p=tuple(n[i]+m[i] for i in range(3))
        edges.append((loc[(p,n)],loc[(p,m)]))
    return perms,edges

def audit():
    perms,edges=geometry()
    solved=''.join(f*9 for f in F)
    @lru_cache(None)
    def move(s,i):
        out=['?']*54
        for j,k in enumerate(perms[i]):out[k]=s[j]
        return ''.join(out)
    def observe(s):
        for i,j in edges:
            if {s[i],s[j]}=={'U','R'}:return int(s[i]!='U')
        raise AssertionError('tracked UR cubie missing')
    u=move(solved,A.index('U'))
    up=move(solved,A.index("U'"))
    assert observe(u)==observe(up)==0
    inf=10**6
    @lru_cache(None)
    def dp(belief,horizon):
        if all(s==solved for s in belief):return (0,None)
        if not horizon:return (inf,None)
        best=(inf,None)
        for action in range(18):
            branches={}
            for s in belief:
                next_state=move(s,action)
                branches.setdefault(observe(next_state),set()).add(next_state)
            worst=max(dp(tuple(sorted(b)),horizon-1)[0] for b in branches.values())
            if (1+worst,action)<best:best=(1+worst,action)
        return best
    belief=tuple(sorted((u,up)))
    assert dp(belief,2)[0]>=inf
    result=dp(belief,3)
    assert result==(3,A.index('F')),(result,A[result[1]])
    branches={}
    for name,state in (('U',u),("U'",up)):
        moved=move(state,A.index('F'))
        bit=observe(moved)
        branches[bit]={'initial_state':name,'next_state':moved}
    assert set(branches)=={0,1}
    plans={}
    for bit,record in branches.items():
        b=(record['next_state'],)
        plan=['F']
        for horizon in (2,1):
            cost,action=dp(b,horizon)
            assert action is not None
            b=(move(b[0],action),)
            plan.append(A[action])
        assert b==(solved,),plan
        plans[str(bit)]={'hidden_start':record['initial_state'],'actions':plan}
    # No single open-loop word can map distinct hidden full-cube states
    # to identical solved state because every physical action is bijective.
    return {'status':'FULL54_ADAPTIVE_GOAL_POLICY_PASS',
            'starts':['U',"U'"],'sensor':'original UR edge orientation',
            'best_worst_case_turns':3,'no_goal_policy_within_two_turns':True,
            'first_action':'F','branches_after_first_readout':plans,
            'nonadaptive_single_word_impossible_by_bijectivity':True,
            'cached_search_nodes':dp.cache_info().currsize,
            'scope':'EXACT_TWO_FULL_CUBE_STATES_NO_SENSOR_ERRORS'}

if __name__=='__main__':
    print(json.dumps(audit(),sort_keys=True,indent=2))
