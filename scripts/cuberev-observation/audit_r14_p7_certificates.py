#!/usr/bin/env python3
"""Independent exact 648-state coupled-parity model: individualized certificates
and alternating matching-cycle ambiguity, no repository dependencies."""
from itertools import permutations,product,combinations
from collections import Counter
from pathlib import Path
import json
E_TYPES=('UR','UF','UL'); C_TYPES=('URF','UFL','ULB')
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def builds(types,r):
    result=[]
    for p in permutations(range(len(types))):
        for prefix in product(range(r),repeat=len(types)-1):
            o=prefix+((-sum(prefix))%r,)
            word=''.join(types[p[i]][(j+o[i])%r] for i in range(len(types)) for j in range(r))
            result.append((word,parity(p),p,o))
    return result
E=builds(E_TYPES,2);C=builds(C_TYPES,3)
S=[(e,c) for e in E for c in C if e[1]==c[1]]
assert len(S)==648
full=(1<<648)-1
nE=6;nC=9
# For each target and each chosen subset of edge/corner facelet slots, exact
# competing joint-state bit masks conditioned on these chosen observations.
E_SUBSETS=[tuple(combinations(range(nE),k)) for k in range(5)]
C_SUBSETS=[tuple(combinations(range(nC),k)) for k in range(5)]
E_BYTES=[s[0][0] for s in S];C_BYTES=[s[1][0] for s in S]
# For each query marginal label, mask over entire joint legal state universe.
E_COLOR=[{} for _ in range(nE)];C_COLOR=[{} for _ in range(nC)]
for i,(ew,cw) in enumerate(zip(E_BYTES,C_BYTES)):
    for j,v in enumerate(ew):E_COLOR[j][v]=E_COLOR[j].get(v,0)|(1<<i)
    for j,v in enumerate(cw):C_COLOR[j][v]=C_COLOR[j].get(v,0)|(1<<i)

def signature_masks(words,color_masks,subsets):
    # output[s][k] -> list of (slot_subset, mask) of legal states matching
    # sector's known colors at those slots.
    out=[]
    for target in words:
        cur=[((),full)]
        by_level=[cur]
        for k in range(1,5):
            arr=[]
            for indices in subsets[k]:
                mask=full
                for j in indices:mask &= color_masks[j][target[j]]
                arr.append((indices,mask))
            by_level.append(arr)
        out.append(by_level)
    return out
em=signature_masks(E_BYTES,E_COLOR,E_SUBSETS)
cm=signature_masks(C_BYTES,C_COLOR,C_SUBSETS)
distribution=Counter();witnesses={};minimal_certificates=[]
for ix in range(len(S)):
    best=None
    bit=1<<ix
    for k in range(1,5):
        for es,emask in em[ix][k]:
            for cs,cmask in cm[ix][k]:
                if emask & cmask == bit:
                    best=(k,es,cs);break
            if best:break
        if best:break
    if best is None:raise AssertionError('No <=4 certificate')
    distribution[best[0]]+=1
    if best[0] not in witnesses:witnesses[best[0]]=(ix,best)
    minimal_certificates.append(best[0])
print('certificate lengths:',dict(distribution), 'examples:',witnesses,flush=True)
# Full cube 20-slot star construction is a separate general proof, not
# measured from this miniature model.
result={'result':'R14_P7_INDIVIDUAL_CERTIFICATES_PASS',
'legal_micro_states':len(S),'query_pairs':nE*nC,
'individual_min_certificate_histogram':dict(sorted(distribution.items())),
'max_individual_certificate':max(minimal_certificates),
'witnesses':{str(k):{'state_index':i,'edge_slots':list(cert[1]),'corner_slots':list(cert[2]),'state_edge_word':S[i][0][0],'state_corner_word':S[i][1][0]} for k,(i,cert) in witnesses.items()},
'known_exact_global_minimax':4,
'full_cube_state_dependent_star_certificate_bound':20,
'full_cube_star_proof_scope':'Every given legal state x has a 20-paired-query separating certificate chosen with foreknowledge of x; not an online 20-query strategy.'}
print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))

# Exact one-sector residual courts: parity-known, unknown n oriented edges.
# Every target has same individualized certificate complexity by the full
# even-permutation/even-flip spatial action transitive on parity-zero sector.
residual=[]
for L,reference_depth in [
 (('UR','UF','UL','UB'),5),
 (('UR','UF','UL','UB','FR'),7),
 (('UR','UF','UL','UB','FR','FL'),9)]:
    n=len(L);r=2
    allperm=[]
    for p in permutations(range(n)):
        if parity(p):continue
        for prefix in product((0,1),repeat=n-1):
            orient=prefix+(sum(prefix)%2,)
            allperm.append(''.join(L[p[i]][(j+orient[i])%2] for i in range(n) for j in range(2)))
    target=''.join(L)
    assert allperm[0]==target
    candidate_bits=(1<<len(allperm))-1
    # Use direct exact color comparisons for every possible spatial slot.
    matching_masks=[]
    for k in range(2*n):
        mask=0
        for idx,w in enumerate(allperm):
            if w[k]==target[k]:mask|=1<<idx
        matching_masks.append(mask)
    best_cert=None
    for k in range(1,2*n+1):
        for subset in combinations(range(2*n),k):
            alive=candidate_bits
            for pos in subset:alive &= matching_masks[pos]
            if alive.bit_count()==1:
                best_cert=subset;break
        if best_cert is not None:break
    assert best_cert is not None
    residual.append({'remaining_cubies':n,'types':list(L),'legal_states':len(allperm),
      'target_certificate_length':len(best_cert),'certificate_sticker_slots':list(best_cert),
      'known_exact_residual_adaptive_minimax':reference_depth,
      'certificate_to_adaptive_gap':reference_depth-len(best_cert)})
print('residual certificates',residual,flush=True)
result['residual_courts']=residual
# Strict one-frame impossibility witness for EVERY physical paired query on
# the complete 648-state micro prior: at least two hidden legal states share
# one outcome for every query (in fact pigeonhole: 648 >36).
for ei in range(nE):
    for ci in range(nC):
        colors=Counter((s[0][0][ei],s[1][0][ci]) for s in S)
        assert max(colors.values())>=2
result['all_54_single_query_choices_not_sufficient']=True
with open(str(Path(__file__).resolve().parent/'R14_P7_CERTIFICATE_RESULTS.json'),'w') as f:
    json.dump(result,f,sort_keys=True,indent=2)

# A complete compact, independently checkable lower-bound witness ledger:
# for every observation subset of size k-1, a distinct legal assignment has
# identical visible colors. Encode permutation cycles and flip supports.
collision_ledgers=[]
for row in residual:
    L=tuple(row['types']);n=len(L);k=row['target_certificate_length']
    configurations=[]
    for p in permutations(range(n)):
        if parity(p):continue
        for prefix in product((0,1),repeat=n-1):
            o=prefix+(sum(prefix)%2,)
            word=''.join(L[p[i]][(j+o[i])%2] for i in range(n) for j in range(2))
            configurations.append((word,p,o))
    target=''.join(L)
    ledger=[]
    shape=Counter()
    for subset in combinations(range(2*n),k-1):
        other=next((entry for entry in configurations if entry[0]!=target and all(entry[0][z]==target[z] for z in subset)),None)
        if other is None:raise AssertionError('Missing lower certificate '+str((n,subset)))
        word,p,o=other
        visited=set();cycles=[]
        for j in range(n):
            if j in visited:continue
            cyc=[];z=j
            while z not in visited:
                visited.add(z);cyc.append(z);z=p[z]
            if len(cyc)>1:cycles.append(cyc)
        kind=('permutation '+str(sorted(map(len,cycles))) if cycles else 'orientation-only')
        shape[kind]+=1
        ledger.append({'read_slots':list(subset),'alternative_word':word,'permutation':list(p),'edge_flip':list(o),'nontrivial_cycles':cycles})
    collision_ledgers.append({'types':list(L),'n':n,'all_k_minus_1_read_sets':len(ledger),'shape_of_first_witnesses':dict(shape),'witnesses':ledger})
result['complete_static_collision_ledgers']=[{k:v for k,v in a.items() if k!='witnesses'} for a in collision_ledgers]
with open(str(Path(__file__).resolve().parent/'R14_P7_COLLISION_CERTIFICATES.json'),'w') as f:
    json.dump(collision_ledgers,f,sort_keys=True,indent=2)
with open(str(Path(__file__).resolve().parent/'R14_P7_CERTIFICATE_RESULTS.json'),'w') as f:
    json.dump(result,f,sort_keys=True,indent=2)
print('collision shapes',[(a['n'],a['all_k_minus_1_read_sets'],a['shape_of_first_witnesses']) for a in collision_ledgers])

# Compact reusable obstruction nuclei: greedy set-cover over all k-1 read
# subsets. These are VALID upper bounds on the size of a hardness witness
# set, not claims of minimum-size hitting families.
distilled=[]
for row in residual:
    L=tuple(row['types']);n=len(L);k=row['target_certificate_length']-1
    target=''.join(L)
    subsets=list(combinations(range(2*n),k)); sub_idx={s:i for i,s in enumerate(subsets)}
    W=[]
    for p in permutations(range(n)):
        if parity(p):continue
        for prefix in product((0,1),repeat=n-1):
            o=prefix+(sum(prefix)%2,)
            word=''.join(L[p[i]][(j+o[i])%2] for i in range(n) for j in range(2))
            if word==target:continue
            equal=[i for i in range(2*n) if word[i]==target[i]]
            bits=0
            for subset in combinations(equal,k):bits|=1<<sub_idx[subset]
            if bits:W.append((bits,word,p,o))
    uncovered=(1<<len(subsets))-1
    picked=[]
    while uncovered:
        best=max(W,key=lambda x:(x[0]&uncovered).bit_count())
        ncover=(best[0]&uncovered).bit_count()
        assert ncover
        picked.append({'word':best[1],'permutation':list(best[2]),'orientation':list(best[3]),'newly_covered_subsets':ncover})
        uncovered &= ~best[0]
    assert sum(w['newly_covered_subsets'] for w in picked)==len(subsets)
    distilled.append({'n':n,'types':list(L),'all_subsets_proved_impossible':len(subsets),'number_of_distilled_other_states':len(picked),'witnesses':picked})
result['greedy_hardness_cores']=[{z:v for z,v in p.items() if z!='witnesses'} for p in distilled]
with open(str(Path(__file__).resolve().parent/'R14_P7_DISTILLED_HARDNESS_CORES.json'),'w') as f:json.dump(distilled,f,sort_keys=True,indent=2)
with open(str(Path(__file__).resolve().parent/'R14_P7_CERTIFICATE_RESULTS.json'),'w') as f:json.dump(result,f,sort_keys=True,indent=2)
print('distilled cores',[(x['n'],x['number_of_distilled_other_states']) for x in distilled])
