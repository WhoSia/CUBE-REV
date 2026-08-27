#!/usr/bin/env python3
import json
from collections import defaultdict,Counter
from pathlib import Path
R=json.loads(Path('research/0.10.5-r1.7/evidence-full-route-r4/FULL_ROUTE_COURT.json').read_text())
M=json.loads(Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json').read_text())
OUT=Path('research/0.10.5-r1.7/evidence-irred-audit');OUT.mkdir(parents=True,exist_ok=True)
cellpop={(c['speed'],c['era']):c['population_n'] for c in M['target_cells']}
by=defaultdict(list)
for r in R['records']:by[(r['speed'],r['era'])].append(r)

def ess(ws):
 s=sum(ws);s2=sum(w*w for w in ws);return s*s/s2 if s2 else 0

def target(name,pred):
 cells=[k for k in cellpop if pred(k)];N=sum(cellpop[k] for k in cells);covered=[k for k in cells if by.get(k)];Nc=sum(cellpop[k] for k in covered)
 ws=[]
 for k in covered:ws += [cellpop[k]/len(by[k])]*len(by[k])
 def est(fn):
  den=sum(cellpop[k] for k in covered)
  return sum(cellpop[k]*(sum(fn(r) for r in by[k])/len(by[k])) for k in covered)/den if den else None
 return {'name':name,'target_population_n':N,'coverage':Nc/N if N else 0,'certified_n':sum(len(by[k]) for k in covered),'weight_ess':ess(ws),
 'any_minimal_irreducible':est(lambda r:1 if r['outcome']['any_minimal_irreducible_redundancy'] else 0),
 'any_exact_loop':est(lambda r:1 if r['outcome']['any_exact_loop'] else 0),'any_shorter_rewrite':est(lambda r:1 if r['outcome']['any_shorter_rewrite'] else 0),
 'mean_saved_moves':est(lambda r:r['outcome']['total_saved_moves'])}

intervals=[]
for r in R['records']:
 for c in r['outcome']['selected_nonoverlap_intervals']:
  intervals.append({'reco_id':r['reco_id'],'result_id':r['result_id'],'attempt_number':r['attempt_number'],'speed':r['speed'],'era':r['era'],'method':r['method'],**c})
patterns=Counter((c['kind'],c['actual'],c.get('replacement','')) for c in intervals)
lengths=Counter((c['kind'],c['actual_length'],c.get('replacement_length',0)) for c in intervals)
phase=Counter(c['phase'] for c in intervals);kind=Counter(c['kind'] for c in intervals)
# Cell-specific positive rates and target contribution for the sub10 estimate.
cells=[]
for k in sorted(by):
 arr=by[k];N=cellpop.get(k,0);p=sum(r['outcome']['any_minimal_irreducible_redundancy'] for r in arr)/len(arr)
 cells.append({'speed':k[0],'era':k[1],'population_n':N,'target_share':N/M['target_population_under10'],'certified_n':len(arr),'minimal_irreducible_rate':p,'target_contribution':N/M['target_population_under10']*p})
out={'schema_version':'CR0105R17-IRREDUCIBLE-CANDIDATE-AUDIT-1','status':'PASS','source_role':'POSTHOC_ADVERSARIAL_ROBUSTNESS_NOT_PRIMARY_PREREGISTRATION',
 'targets':[target('SUB10',lambda k:True),target('SUB7',lambda k:k[0] in ('<5','5-7')),target('7_TO_10',lambda k:k[0]=='7-10'),target('SUB10_2023_26',lambda k:k[1]=='2023-26')],
 'selected_interval_n':len(intervals),'kind_counts':dict(kind),'phase_counts':dict(phase),'length_transition_counts':[{'kind':k[0],'actual_length':k[1],'replacement_length':k[2],'n':n} for k,n in lengths.most_common()],
 'pattern_counts':[{'kind':k[0],'actual':k[1],'replacement':k[2],'n':n} for k,n in patterns.most_common()],
 'selected_intervals':intervals,'cell_table':cells,
 'interpretation':'These intervals survived the posthoc minimal-irreducible adversarial filter. They remain route-algebra phenotypes, not cognitive-error/recovery labels; normal algorithms, ergonomics, and unobserved solver objectives can still make a shorter local group-equivalent route non-dominated in practice.',
 'human_observations':0}
(OUT/'IRREDUCIBLE_CANDIDATE_AUDIT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,indent=2,ensure_ascii=False))
