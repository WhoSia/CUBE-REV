"""0.16/P9: exact reduction of the P7 60-weight dual certificate to 50x116.
Input: private/provenance-controlled P7 near_dual_candidates.json (math-only).
This is an independent necessary-condition cover check, NOT a Lean kernel proof.
Run: python scripts/cuberev-016/verify-dual-forced-core.py <path-to-near_dual_candidates.json>
"""
import json, sys
from pathlib import Path

def run(path):
    data=json.loads(Path(path).read_text())
    w={int(k):int(v) for k,v in data['dualweights'].items()}
    c=data['near_tight']
    assert len(w)==60 and len(c)==168 and sum(w.values())==476
    assert all(sum(w[k] for k in z['covered'])==z['cost']
               and z['cost'] in (16,20) for z in c)
    unique={frozenset(z['covered']) for z in c}
    assert len(unique)==126
    heavy={k for k,v in w.items() if v==20}
    assert len(heavy)==10
    assert all(frozenset({k}) in unique for k in heavy)
    assert all(not (p & heavy) or (len(p)==1 and next(iter(p)) in heavy)
               for p in unique)
    other=sorted(set(w)-heavy)
    patterns=[p for p in unique if not p & heavy]
    assert len(other)==50 and len(patterns)==116
    assert sum(w[k] for k in other)==276
    bit={k:1<<i for i,k in enumerate(other)}
    weights=[w[k] for k in other]
    masks=list(set(sum(bit[k] for k in p) for p in patterns))
    assert len(masks)==116
    target=(1<<50)-1
    options=[[m for m in masks if (m>>i)&1] for i in range(50)]
    memo={}
    visits=edges=pruned=0

    def mass(m):
        s=0
        while m:
            t=m & -m
            m^=t
            s+=weights[t.bit_length()-1]
        return s

    def search(covered,used):
        nonlocal visits,edges,pruned
        if covered==target:return True
        if used==14:return False
        missing=target^covered
        rem=mass(missing)
        slots=14-used
        if rem>20*slots:
            pruned+=1
            return False
        if memo.get(covered,99)<=used:return False
        memo[covered]=used
        visits+=1
        candidates=None
        tmp=missing
        while tmp:
            b=tmp & -tmp
            tmp^=b
            i=b.bit_length()-1
            choices=[]
            for m in options[i]:
                gain=mass(m & missing)
                if rem-gain<=20*(slots-1):
                    choices.append((gain,m))
            if candidates is None or len(choices)<len(candidates):
                candidates=choices
                if not choices:break
        if not candidates:
            pruned+=1
            return False
        for _,m in sorted(candidates,reverse=True):
            edges+=1
            if search(covered|m,used+1):
                return True
        return False

    exists=search(0,0)
    result={'input_dual_mass':476,'original_targets':60,'original_candidates':168,
      'deduplicated_patterns':126,'forced_heavy_singletons':10,
      'reduced_targets':50,'reduced_candidates':116,'remaining_budget':14,
      'reduced_total_mass':276,'exists':exists,
      'visited_states':visits,'branches':edges,'prunes':pruned}
    assert not exists and visits==165 and edges==220 and pruned==52
    return result

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python verify-dual-forced-core.py <P7_NEAR_DUAL_CANDIDATES.json>')
    print('CUBE_REV_016_P9_FORCED_CORE_EXACT_PASS')
    print(json.dumps(run(sys.argv[1]),sort_keys=True))
