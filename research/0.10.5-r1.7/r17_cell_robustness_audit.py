#!/usr/bin/env python3
import json,math
from collections import defaultdict
from pathlib import Path
R3=json.loads(Path('research/0.10.5-r1.7/evidence-full-route-r3/FULL_ROUTE_COURT.json').read_text())
G=json.loads(Path('research/0.10.5-r1.7/evidence-full-route-r3/ROUTE_ADMISSION_GATE.json').read_text())
M=json.loads(Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json').read_text())
OUT=Path('research/0.10.5-r1.7/evidence-robustness');OUT.mkdir(parents=True,exist_ok=True)
records=R3['records']
cellpop={(c['speed'],c['era']):c['population_n'] for c in M['target_cells']}
supported={(c['speed'],c['era']):c for c in M['target_cells'] if c['supported']}
by=defaultdict(list)
for r in records:by[(r['speed'],r['era'])].append(r)

def ess(weights):
    s=sum(weights);s2=sum(w*w for w in weights);return s*s/s2 if s2 else 0

def calc(name,pred):
    target_cells=[k for k in cellpop if pred(k)]
    target_n=sum(cellpop[k] for k in target_cells)
    covered=[k for k in target_cells if len(by.get(k,[]))>0]
    covered_n=sum(cellpop[k] for k in covered)
    ws=[]
    for k in covered:
        w=cellpop[k]/len(by[k]);ws.extend([w]*len(by[k]))
    def est(fn):
        num=den=0
        for k in covered:
            arr=by[k];mu=sum(fn(r) for r in arr)/len(arr);num+=cellpop[k]*mu;den+=cellpop[k]
        return num/den if den else None
    stab=[]
    if ws:
        mw=sum(ws)/len(ws);stab=[w/mw for w in ws]
    return {
      'name':name,'target_population_n':target_n,'covered_population_n':covered_n,'coverage':covered_n/target_n if target_n else 0,
      'certified_n':sum(len(by[k]) for k in covered),'weight_ess':ess(ws),'weight_ess_fraction':ess(ws)/max(1,sum(len(by[k]) for k in covered)),
      'stabilized_weight_max':max(stab) if stab else None,
      'any_multi_generator_redundancy':est(lambda r:1 if r['outcome']['any_structural_redundancy'] else 0),
      'any_exact_loop':est(lambda r:1 if r['outcome']['any_exact_loop'] else 0),
      'any_shorter_exact_rewrite':est(lambda r:1 if r['outcome']['any_shorter_rewrite'] else 0),
      'mean_saved_moves':est(lambda r:r['outcome']['total_saved_moves']),
      'mean_face_turn_redundancy_fraction':est(lambda r:r['outcome']['face_turn_token_redundancy_fraction'] or 0),
    }

cells=[]
sub10_std=R3['metrics']['any_multi_generator_state_verified_redundancy']['standardized']
for k in sorted(supported):
    arr=by.get(k,[]);N=cellpop[k]
    if not arr:continue
    p=sum(1 for r in arr if r['outcome']['any_structural_redundancy'])/len(arr)
    loop=sum(1 for r in arr if r['outcome']['any_exact_loop'])/len(arr)
    rw=sum(1 for r in arr if r['outcome']['any_shorter_rewrite'])/len(arr)
    mu=sum(r['outcome']['total_saved_moves'] for r in arr)/len(arr)
    share=N/M['target_population_under10']
    cells.append({'speed':k[0],'era':k[1],'population_n':N,'target_share':share,'certified_n':len(arr),'structural_redundancy_rate':p,'exact_loop_rate':loop,'shorter_rewrite_rate':rw,'mean_saved_moves':mu,'contribution_to_sub10_structural_rate':share*p})

# Cell-deletion diagnostic standardized on the remaining target, not a claim about the original target.
loo=[]
for omit in cells:
    kept=[c for c in cells if not(c['speed']==omit['speed'] and c['era']==omit['era'])]
    den=sum(c['population_n'] for c in kept);p=sum(c['population_n']*c['structural_redundancy_rate'] for c in kept)/den
    loo.append({'omitted_cell':f"{omit['speed']}|{omit['era']}",'omitted_target_share':omit['target_share'],'remaining_target_rate':p,'delta_from_full_supported_sub10':p-sub10_std})
loo.sort(key=lambda x:abs(x['delta_from_full_supported_sub10']),reverse=True)

targets=[
 calc('SUB10',lambda k:True),
 calc('SUB7',lambda k:k[0] in ('<5','5-7')),
 calc('7_TO_10',lambda k:k[0]=='7-10'),
 calc('SUB10_2023_26',lambda k:k[1]=='2023-26'),
 calc('SUB7_2023_26',lambda k:k[1]=='2023-26' and k[0] in ('<5','5-7')),
]
out={'schema_version':'CR0105R17-CELL-ROBUSTNESS-1','status':'PASS','source_r3_status':R3['status'],'targets':targets,'cell_table':cells,'leave_one_cell_out_top':loo[:8],
 'interpretation':{'primary':'SUB10 is the R3 speed x era standardized descriptive linked-reconstruction target. SUB7 is a prospectively supported robustness target from the earlier selection court. 7_TO_10 and era-specific values are diagnostics, not newly promoted population estimands.','cell_influence':'Large target-share cells can dominate the standardized result; leave-one-cell-out values change the estimand and are diagnostic only.'},'human_observations':0}
(OUT/'CELL_ROBUSTNESS_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
