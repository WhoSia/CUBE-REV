#!/usr/bin/env python3
"""CUBE-REV 0.19 exact-k SAT court on original real 3x3 sticker-derived L5 HTM.
No unsat claim unless external drat-trim independently checks Glucose4 DRUP.
Reconstructs exact all-k row/column quotient. Full physical 8-word upper replay.
"""
import argparse, json, hashlib, time
from pathlib import Path
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose4

p=argparse.ArgumentParser()
for v in ('physical','partitions','maps','output'):p.add_argument('--'+v,required=True)
p.add_argument('--conflicts',type=int,default=4500000)
a=p.parse_args()
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
raw=Path(a.physical).read_bytes()
physical=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
bases=physical['bases'];assert len(bases)==1192
moves=json.loads(Path(a.maps).read_text())
assert len(moves)==18 and all(len(x)==24 and len(set(x))==24 for x in moves)
ACTIONS=[f+s for f in 'URFDLB' for s in ('',"'",'2')]
WITNESSES=[
 "F' B' L F B","F' B' R F B","F' B' D F B",
 "F L2 B' D2 F","F U2 B R2 F","F' B' U F B",
 "F B L F B","F B R F B"]
def blocks_for_word(word):
 states=[2*i for i in range(12)];observ=[0]*12
 for t,x in enumerate(word):
  for j in range(12):
   states[j]=moves[x][states[j]]
   observ[j]|=(states[j]&1)<<t
 d={}
 for j,o in enumerate(observ):d[o]=d.get(o,0)|(1<<j)
 return tuple(sorted(d.values()))
def coverage(blocks):
 mask=0
 for i,base in enumerate(bases):
  if all((base&b).bit_count()<=1 for b in blocks):mask|=1<<i
 return mask
full=(1<<1192)-1
witness_words=[[ACTIONS.index(t) for t in w.split()] for w in WITNESSES]
assert all(len(w)==5 for w in witness_words)
covered=0
for w in witness_words:covered|=coverage(blocks_for_word(w))
assert covered==full, ('PHYSICAL_8_UPPER_FAILED',covered.bit_count())
print('CUBE_REV_019_PHYSICAL_8_WORD_UPPER_REPLAY_PASS',flush=True)

t0=time.time()
coverage_map={}
partitions=0
for line in Path(a.partitions).read_text().splitlines():
 act,blk=line.split('|'); blocks=tuple(map(int,blk.split()))
 assert blocks_for_word(tuple(map(int,act.split())))==blocks, 'physical-map-to-partition lineage mismatch'
 assert len(act.split())==5
 assert len(blocks)==len(set(blocks)) and sum(b.bit_count() for b in blocks)==12
 x=0
 for b in blocks:assert x&b==0; x|=b
 assert x==4095
 mask=coverage(blocks)
 coverage_map.setdefault(mask,(tuple(map(int,act.split())),blocks))
 partitions+=1
assert partitions==14938 and len(coverage_map)==14446, (partitions,len(coverage_map))
print('CUBE_REV_019_14938_PHYSICAL_PARTITIONS_14446_COVERAGE_TYPES_PASS',round(time.time()-t0,1),flush=True)
dual_path=Path(__file__).resolve().parents[2]/'docs/0.19/P0_L5_INTEGER_LOWER6_DUAL.json'
dc=json.loads(dual_path.read_text())
assert dc['source_L4_sha256']==hashlib.sha256(raw).hexdigest()
wt={int(i):int(w) for i,w in dc['row_index_weight_numerator'].items()}
assert len(wt)==70 and sum(wt.values())==384 and dc['denominator']==72
dualmax=max(sum(w for i,w in wt.items() if (mask>>i)&1) for mask in coverage_map)
assert dualmax==72
print('CUBE_REV_019_ALL_14938_PHYSICAL_PARTITIONS_DUAL_LOWER6_PASS',json.dumps({'mass':sum(wt.values()),'max_per_experiment':dualmax}),flush=True)


def maxima(items):
 ranked=sorted(items,key=int.bit_count,reverse=True)
 keep=[]
 for mask in ranked:
  if not any(mask&~k==0 for k in keep):keep.append(mask)
 return keep
max_columns=maxima(coverage_map)
assert len(max_columns)==8807,len(max_columns)
assert __import__('functools').reduce(int.__or__,max_columns,0)==full
print('CUBE_REV_019_8807_MAXIMUM_COVERAGE_TYPES_PASS',round(time.time()-t0,1),flush=True)

# All-k row implication, restricted to undominated columns.
support=[0]*1192
for j,mask in enumerate(max_columns):
 bit=1<<j
 while mask:
  lb=mask&-mask
  support[lb.bit_length()-1]|=bit
  mask-=lb
assert all(support)
row_order=sorted(range(1192),key=lambda i:support[i].bit_count())
keep_rows=[]; row_implies={}
for i in row_order:
 parent=next((j for j in keep_rows if support[j]&~support[i]==0),None)
 if parent is None:keep_rows.append(i)
 else:row_implies[i]=parent
assert len(keep_rows)==544,(len(keep_rows),len(row_implies))
assert sorted(set(bases[i].bit_count() for i in keep_rows))==[4,5]
assert sum(bases[i].bit_count()==5 for i in keep_rows)==480
print('CUBE_REV_019_ALL_K_544_ROW_REDUCTION_PASS',round(time.time()-t0,1),flush=True)

projected_map={}
for orig_mask in max_columns:
 short=0
 for k,i in enumerate(keep_rows):
  if (orig_mask>>i)&1:short|=1<<k
 projected_map.setdefault(short,orig_mask)
projected_maxima=maxima(projected_map)
assert len(projected_maxima)==2887,len(projected_maxima)
candidate_original=[projected_map[m] for m in projected_maxima]
assert __import__('functools').reduce(int.__or__,candidate_original,0)==full
print('CUBE_REV_019_ALL_K_2887_COLUMN_REDUCTION_PASS',round(time.time()-t0,1),flush=True)

# Independently replay a 70-row integer dual lower bound from previous frozen analysis?

# A full 16-element signed-coordinate incidence automorphism group.
# Includes eight orientation-reversing relabelings: these are NOT moves.
# Group actions are used only after certifying closure of the physical
# source requirement family AND all 8807 realized maximal L5 experiments.
from itertools import product
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),
        (1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),
        (1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
coord_index={v:i for i,v in enumerate(coords)}
base_index={v:i for i,v in enumerate(bases)}
core_index={v:i for i,v in enumerate(keep_rows)}
all_maximal=set(max_columns)
reduced_index={v:i for i,v in enumerate(projected_maxima)}
group_column_maps=[]
for axes in ((0,1,2),(1,0,2)):
    for signs in product((-1,1), repeat=3):
        perm=[coord_index[tuple(signs[k]*pos[axes[k]]
                for k in range(3))] for pos in coords]
        transformed_bases=[]
        for b in bases:
            b2=sum(1<<perm[i] for i in range(12) if b>>i&1)
            assert b2 in base_index
            transformed_bases.append(base_index[b2])
        transformed_core=[core_index[transformed_bases[i]] for i in keep_rows]
        assert set(transformed_core)==set(range(544))
        # Important: exact closure on full physically realized (pre-quotient) cover family.
        for mask in max_columns:
            z=0; remaining=mask
            while remaining:
                bit=remaining&-remaining
                z|=1<<transformed_bases[bit.bit_length()-1]
                remaining-=bit
            assert z in all_maximal, ('SOURCE_AUTOMORPHISM_NOT_PHYSICAL',axes,signs)
        perm_cols=[]
        for mask in projected_maxima:
            z=0; remaining=mask
            while remaining:
                bit=remaining&-remaining
                z|=1<<transformed_core[bit.bit_length()-1]
                remaining-=bit
            assert z in reduced_index, ('REDUCED_COL_AUTOMORPHISM_FAIL',axes,signs)
            perm_cols.append(reduced_index[z])
        group_column_maps.append(perm_cols)
assert len(group_column_maps)==16
unseen=set(range(len(projected_maxima)))
orbit_representatives=[];orbit_hist={}
while unseen:
    seed=min(unseen)
    orbit=set(g[seed] for g in group_column_maps)
    assert seed in orbit and orbit<=unseen
    unseen-=orbit
    orbit_representatives.append(seed+1)
    orbit_hist[len(orbit)]=orbit_hist.get(len(orbit),0)+1
assert len(orbit_representatives)==196
symmetry_receipt={'group_order':16,'physical_maximal_columns_checked':8807,
   'row_core':544,'column_core':2887,'column_orbits':196,
   'orbit_histogram':orbit_hist,'symmetry_break_clause_size':196,
   'validity':'Any nonempty cover can be globally relabeled to contain at least one orbit representative; cannot identify orbit variables.'}
(out/'symmetry_exact_incidence_receipt.json').write_text(json.dumps(symmetry_receipt,indent=2)+'\n')
print('CUBE_REV_019_16_INCIDENCE_AUTOMORPHISMS_196_ORBIT_REPS_PASS',
      json.dumps(symmetry_receipt),flush=True)

# Order-invariant original-1192-source fractional certificate gate.
# Reduced-column IDs depend on candidate iteration order. The sealed P8
# certificates instead identify actual physical coverage masks on ALL original
# 1192 source rows and verify the group orbit as a set, not an index array.
import subprocess,sys
root=Path(__file__).resolve().parents[2]
subprocess.run([
 sys.executable,str(root/'scripts/cuberev-019/verify-L5-order-invariant-LP.py'),
 '--physical',a.physical,'--partitions',a.partitions,
 '--full_cert',str(root/'docs/0.19/P8_ORDER_INVARIANT_L5_FULL_LP_CERT.json'),
 '--five_cert',str(root/'docs/0.19/P8_ORDER_INVARIANT_L5_FIVE_ONLY_LP_CERT.json'),
 '--output',str(out/'P8_L5_order_invariant_LP_receipt.json')],check=True)
print('CUBE_REV_019_ORDER_INVARIANT_FULL_AND_FIVE_SOURCE_FRACTIONAL_LP_PROOF_PASS',flush=True)

# Physically restricted perfect-hash subcourt: can FIVE 5-turn words
# jointly distinguish every admitted FIVE-STATE source? This is a smaller
# necessary subproblem of any full dictionary. Its UNSAT certificate, if
# externally checked, implies a full k<=6 dictionary can contain NO rank-4
# experiment (such a word covers no five-state source and leaves <=5 words).
# The court is a separate proof obligation; an UNKNOWN leaves M*(5) unchanged.
five_positions=[k for k,original_i in enumerate(keep_rows)
                if bases[original_i].bit_count()==5]
assert len(five_positions)==480
five_bits=sum(1<<j for j in five_positions)
five_candidates=[j for j,x in enumerate(projected_maxima) if x&five_bits]
assert len(five_candidates)==2403,('FIVE_SOURCE_SUBPROBLEM_LINEAGE_CHANGED',len(five_candidates))
five_cnf=CNF()
for pos in five_positions:
    clause=[k+1 for k,j in enumerate(five_candidates) if projected_maxima[j]>>pos&1]
    assert clause
    five_cnf.append(clause)
five_pool=IDPool(start_from=len(five_candidates)+1)
five_cnf.extend(CardEnc.atmost(lits=list(range(1,len(five_candidates)+1)),bound=5,
                            encoding=EncType.seqcounter,vpool=five_pool).clauses)
five_stem='cube_L5_five_k5'
five_path=out/(five_stem+'.cnf')
five_cnf.to_file(str(five_path))
five_result={'scope':'Only original 480 five-state sources, not all original 1192',
 'k':5,'columns':len(five_candidates),'rows':480,
 'cnf_sha256':hashlib.sha256(five_path.read_bytes()).hexdigest(),
 'state':'UNKNOWN','external_check':'NOT_CHECKED'}
with Glucose4(bootstrap_with=five_cnf.clauses,with_proof=True) as solver:
    solver.conf_budget(a.conflicts)
    ans=solver.solve_limited(expect_interrupt=False)
    if ans is True:
        model=set(solver.get_model())
        selected=[j for k,j in enumerate(five_candidates) if (k+1) in model]
        assert len(selected)<=5
        for pos in five_positions:
            assert any(projected_maxima[j]>>pos&1 for j in selected)
        five_result['state']='SAT_FIVE_SOURCE_ONLY_PHYSICAL_QUOTIENT_REPLAY_PASS'
        five_result['columns_selected']=selected
    elif ans is False:
        proof=solver.get_proof()
        assert proof and proof[-1].strip()=='0'
        pf=out/(five_stem+'.drup')
        pf.write_text(chr(10).join(proof)+chr(10))
        five_result['state']='UNSAT_EXTERNAL_DRUP_CHECK_PENDING'
        five_result['proof_sha256']=hashlib.sha256(pf.read_bytes()).hexdigest()
        five_result['proof_lines']=len(proof)
    else:
        five_result['state']='UNKNOWN_CONFLICT_BUDGET'
(out/(five_stem+'.receipt.json')).write_text(json.dumps(five_result,indent=2)+chr(10))
print('CUBE_REV_019_L5_480_FIVE_SOURCE_K5_SEPARATE_COURT',
      json.dumps(five_result),flush=True)

# First court: 7-SAT. If SAT, court 6-SAT. If UNSAT, DRUP certificate.
summary={'schema':'cube-rev.019.L5.SAT-court.v1',
 'baseline_physical_sha256':hashlib.sha256(raw).hexdigest(),
 'partition_file_sha256':hashlib.sha256(Path(a.partitions).read_bytes()).hexdigest(),
 'original_rows':1192,'physical_words':18**5,'unique_partitions':14938,
 'maximal_physical_columns':8807,'row_core':544,'final_candidates':2887,
 'physical_8_word_upper':True,'decisions':[],
 'status':'EXACT_MSTAR5_NOT_YET_PROVEN'}
for k in (7,6):
 cnf=CNF()
 # Sound automorphism symmetry breaker: retain ALL 2887 column variables.
 cnf.append(orbit_representatives)
 if k==7:
    # Exact two-column integer-cover obstruction from the verified original
    # 70-row dual: total weight 384, maximum per physical word 72.
    # With <=7 selected, if two selected words jointly cover <24 weight,
    # the other five contribute <=5*72=360, so coverage is impossible.
    # These clauses are sound CONSEQUENCES of physical coverage and the
    # cardinality <=7, not arbitrary cuts. Keep all column variables.
    weighted_rows=sorted(wt.items())
    masks70=[]; masses70=[]
    for candidate in candidate_original:
        qmask=0; qmass=0
        for z,(source_row,weight) in enumerate(weighted_rows):
            if candidate>>source_row&1:
                qmask|=1<<z; qmass+=weight
        masks70.append(qmask);masses70.append(qmass)
    low=[j for j in range(len(candidate_original)) if masses70[j]<24]
    cuts=0
    for pos,i in enumerate(low):
        for j in low[pos+1:]:
            if masses70[i]+masses70[j]<24:
                incompatible=True
            else:
                common=masks70[i]&masks70[j]
                overlap=0
                while common:
                    bit=common&-common
                    overlap+=weighted_rows[bit.bit_length()-1][1]
                    common-=bit
                incompatible=(masses70[i]+masses70[j]-overlap)<24
            if incompatible:
                cnf.append([-(i+1),-(j+1)])
                cuts+=1
    assert cuts==247348,('INCORRECT_OR_UNSOUND_K7_PAIR_CUTS',cuts)
    print('CUBE_REV_019_EXACT_DUAL_DERIVED_K7_PAIR_INCOMPATIBILITY_CLAUSES_PASS',
          json.dumps({'bound_k':7,'physical_70row_weight_sum':384,
                      'max_one_experiment':72,'threshold_for_two_selected':24,
                      'disallowed_pairs':cuts}),flush=True)
 if k==6:
    # For a 6-word dictionary every chosen word must have weighted capacity
    # at least 384-5*72=24. Every selected pair must cover at least
    # 384-4*72=96 distinct weighted source demand. These unit/binary cuts
    # are necessary logical consequences of the SAME original 70-row dual.
    weighted_rows=sorted(wt.items())
    masses=[]; hit_masks=[]
    for wordmask in candidate_original:
        mass=0;bits=0
        for j,(original_row,weight) in enumerate(weighted_rows):
            if (wordmask>>original_row)&1:
                bits|=1<<j;mass+=weight
        masses.append(mass);hit_masks.append(bits)
    eligible=[]
    for j,mass in enumerate(masses):
        if mass<24:cnf.append([-(j+1)])
        else:eligible.append(j)
    assert len(eligible)==1877
    forbidden=0
    for p,i in enumerate(eligible):
        for j in eligible[p+1:]:
            common=hit_masks[i]&hit_masks[j]
            shared=0
            while common:
                bit=common&-common
                shared+=weighted_rows[bit.bit_length()-1][1]
                common-=bit
            if masses[i]+masses[j]-shared<96:
                cnf.append([-(i+1),-(j+1)])
                forbidden+=1
    assert forbidden==1194707,('K6_PAIR_DUAL_AUDIT_FAILED',forbidden)
    print('CUBE_REV_019_K6_EXACT_WEIGHTED_PAIR_CUTS_PASS',
          json.dumps({'k':6,'eligible_words':len(eligible),
                      'forbidden_pair_choices':forbidden,
                      'pair_union_mass_minimum':96}),flush=True)
 for i in range(len(keep_rows)):
  clause=[j+1 for j,v in enumerate(projected_maxima) if (v>>i)&1]
  assert clause
  cnf.append(clause)
 pool=IDPool(start_from=len(projected_maxima)+1)
 cnf.extend(CardEnc.atmost(lits=list(range(1,len(projected_maxima)+1)),
                       bound=k,encoding=EncType.seqcounter,vpool=pool).clauses)
 stem=f'cube_L5_k{k}'
 cnff=out/(stem+'.cnf');cnf.to_file(str(cnff))
 record={'k':k,'cnf_sha256':hashlib.sha256(cnff.read_bytes()).hexdigest(),
         'variables':cnf.nv,'clauses':len(cnf.clauses),'state':'UNKNOWN',
         'conflict_budget':a.conflicts}
 print('CUBE_REV_019_SAT_COURT_START',record,flush=True)
 started=time.time()
 with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as solver:
  solver.conf_budget(a.conflicts)
  answer=solver.solve_limited(expect_interrupt=False)
  record['elapsed_seconds']=round(time.time()-started,3)
  if answer is True:
   selected=[j for j in range(len(projected_maxima)) if j+1 in set(solver.get_model())]
   cover=0
   for j in selected:cover|=candidate_original[j]
   assert cover==full and len(selected)<=k
   record.update(state='SAT_PHYSICAL_WITNESS_VALIDATED',
                 selected_original_source_masks_sha256=hashlib.sha256(','.join(str(j) for j in selected).encode()).hexdigest(),
                 selected_original_word_representatives=[list(coverage_map[x][0]) for x in (candidate_original[j] for j in selected)])
   assert all(len(w)==5 for w in record['selected_original_word_representatives'])
   trace=0
   for w in record['selected_original_word_representatives']:
    trace|=coverage(blocks_for_word(w))
   assert trace==full,'Independent sticker transition witness replay failed'
   (out/(stem+'.witness.json')).write_text(json.dumps(record,indent=2)+'\n')
   print('CUBE_REV_019_K_SAT_PHYSICAL_REPLAY_PASS',k,len(selected),flush=True)
  elif answer is False:
   proof=solver.get_proof()
   assert proof and proof[-1].strip()=='0'
   pf=out/(stem+'.drup');pf.write_text('\n'.join(proof)+'\n')
   record.update(state='UNSAT_EXTERNAL_DRUP_CHECK_PENDING',
                 proof_lines=len(proof),proof_sha256=hashlib.sha256(pf.read_bytes()).hexdigest())
   print('CUBE_REV_019_UNSAT_DRUP_EMITTED_EXTERNAL_CHECK_PENDING',k,len(proof),flush=True)
  else:
   record['state']='UNKNOWN_CONFLICT_BUDGET'
   print('CUBE_REV_019_K_UNRESOLVED',k,flush=True)
 summary['decisions'].append(record)
 (out/(stem+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
 (out/'all_courts.json').write_text(json.dumps(summary,indent=2)+'\n')
 if answer is not True:break
print('CUBE_REV_019_LOCAL_COURT_RECORDED_NO_PREMATURE_THEOREM',flush=True)
