#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, Counter
import json, math

CAL=Path('research/0.10.5-r1.8/evidence-null-calibration-r2/NULL_SEGMENT_LEDGER.json')
SEAL=Path('research/0.10.5-r1.8/evidence-null-calibration-r2/NULL_THRESHOLD_SEAL.json')
HOLD=Path('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_COURT.json')
OUT=Path('/tmp/r18zero'); OUT.mkdir(parents=True,exist_ok=True)

cal=json.loads(CAL.read_text())['rows']
seal=json.loads(SEAL.read_text())
h=json.loads(HOLD.read_text())
hseg=h['segments']; hrec=[r for r in h['records'] if r.get('admission')=='STATE_CERTIFIED']
assert h['primary']['attempt_any_algorithm_excess_raw']==0
assert h['secondary']['algorithm_excess_segment_n']==0
assert h['primitive_replication']['positive_attempts']==0

def qupper(xs,q):
    if not xs:return None
    a=sorted(xs); return a[max(0,min(len(a)-1,math.ceil(q*len(a))-1))]
def stats(xs):
    if not xs:return {'n':0}
    return {'n':len(xs),'p50':qupper(xs,.5),'p90':qupper(xs,.9),'p95':qupper(xs,.95),'p99':qupper(xs,.99),'max':max(xs)}

def hierarchy_threshold(rows,method,phase,field):
    mp=[r[field] for r in rows if r['method']==method and r['phase']==phase]
    ph=[r[field] for r in rows if r['phase']==phase]
    gl=[r[field] for r in rows]
    if len(mp)>=40:return {'level':'METHOD_PHASE_99','n':len(mp),'q':.99,'threshold':qupper(mp,.99)}
    if len(ph)>=80:return {'level':'PHASE_99','n':len(ph),'q':.99,'threshold':qupper(ph,.99)}
    return {'level':'GLOBAL_99_5','n':len(gl),'q':.995,'threshold':qupper(gl,.995)}

# Decompose what raises the frozen null envelope.
source=Counter(); deltas=[]
for r in cal:
    vals={'OBSERVED_MAX_EXCURSION':r['actual_excursion']}
    if r.get('representation_max') is not None: vals['REPRESENTATION_MAX']=r['representation_max']
    if r.get('solver_exact_accepted') and r.get('solver_amplitude') is not None: vals['SOLVER_MAX_EXCURSION']=r['solver_amplitude']
    mx=max(vals.values()); winners=[k for k,v in vals.items() if abs(v-mx)<1e-12]
    source['TIE' if len(winners)>1 else winners[0]]+=1
    deltas.append(r['null_envelope']-r['actual_candidate_reversal'])

combos=sorted(set((r['method'],r['phase']) for r in hseg))
rows=[]
posthoc_exceed_segments=[]
for method,phase in combos:
    hs=[r for r in hseg if r['method']==method and r['phase']==phase]
    cs=[r for r in cal if r['method']==method and r['phase']==phase]
    frozen=seal['thresholds'].get(f'{method}|{phase}',{'threshold':seal['calibration_summary']['global']['p995'],'level':'GLOBAL_99_5_UNSEEN'})
    matched=hierarchy_threshold(cal,method,phase,'actual_candidate_reversal')
    hvals=[r['candidate_reversal_amplitude'] for r in hs]
    cvals=[r['actual_candidate_reversal'] for r in cs]
    floor=seal['minimum_candidate_floor']
    nraw=sum(v>=floor-1e-12 for v in hvals)
    nfrozen=sum(v>frozen['threshold']+1e-12 and v>=floor-1e-12 for v in hvals)
    nmatched=sum(v>matched['threshold']+1e-12 and v>=floor-1e-12 for v in hvals)
    for r in hs:
        if r['candidate_reversal_amplitude']>matched['threshold']+1e-12 and r['candidate_reversal_amplitude']>=floor-1e-12:
            posthoc_exceed_segments.append({**r,'posthoc_matched_observed_candidate_threshold':matched['threshold'],'posthoc_level':matched['level']})
    rows.append({
      'method':method,'phase':phase,'holdout_n':len(hs),'calibration_method_phase_n':len(cs),
      'frozen_envelope_threshold':frozen['threshold'],'frozen_level':frozen['level'],
      'posthoc_observed_candidate_threshold':matched['threshold'],'posthoc_level':matched['level'],'posthoc_threshold_n':matched['n'],
      'threshold_gap_frozen_minus_posthoc':frozen['threshold']-matched['threshold'],
      'calibration_candidate':stats(cvals),'holdout_candidate':stats(hvals),
      'holdout_raw_candidate_reversal_ge_floor_n':nraw,
      'holdout_frozen_exceed_n':nfrozen,
      'holdout_posthoc_matched_observed_candidate_exceed_n':nmatched,
      'frozen_threshold_above_holdout_max': frozen['threshold']>(max(hvals) if hvals else -1)+1e-12
    })

# Attempt-level diagnostic under the posthoc observed-candidate thresholds.
pos_attempts=set((r['result_id'],r['attempt_number']) for r in posthoc_exceed_segments)
phase_counts=Counter(r['phase'] for r in posthoc_exceed_segments)
method_counts=Counter(r['method'] for r in posthoc_exceed_segments)
raw_candidates=sum(r['candidate_reversal_amplitude']>=seal['minimum_candidate_floor']-1e-12 for r in hseg)
frozen_above_max=sum(r['frozen_threshold_above_holdout_max'] for r in rows)

out={
 'schema_version':'CR0105R18-ZERO-COURT-RAVEL-DIAGNOSTIC-1',
 'status':'PASS_DIAGNOSTIC',
 'role':'POSTHOC_MEASUREMENT_SUPPORT_AUDIT_NOT_PROSPECTIVE_OUTCOME',
 'prospective_result_unchanged':{'algorithm_excess_attempts':0,'algorithm_excess_segments':0,'r17_r5_primitive_attempts':0},
 'holdout':{'state_certified_attempts':len(hrec),'eligible_segments':len(hseg),'raw_candidate_reversal_ge_floor_segments':raw_candidates,'raw_candidate_reversal_ge_floor_rate':raw_candidates/len(hseg)},
 'calibration':{
   'segments':len(cal),
   'null_envelope_source_counts':dict(source),
   'null_envelope_minus_actual_candidate_reversal':stats(deltas),
   'actual_candidate_reversal':stats([r['actual_candidate_reversal'] for r in cal]),
   'null_envelope':stats([r['null_envelope'] for r in cal])
 },
 'method_phase':rows,
 'frozen_threshold_above_entire_holdout_method_phase_max_combos':frozen_above_max,
 'method_phase_combo_n':len(rows),
 'posthoc_observed_candidate_matched_sensitivity':{
   'warning':'Thresholds in this section were constructed after the prospective zero was observed and use only calibration observed-path candidate-reversal amplitudes. They are diagnostic only, exclude representation/solver candidate-reversal envelopes, and cannot replace the frozen R1.8 estimand.',
   'positive_segments':len(posthoc_exceed_segments),
   'positive_attempts':len(pos_attempts),
   'raw_attempt_rate':len(pos_attempts)/len(hrec),
   'phase_counts':dict(phase_counts),'method_counts':dict(method_counts),
   'segments':posthoc_exceed_segments[:200]
 },
 'adjudication':'If raw pre-endpoint reversals are common but frozen envelope thresholds sit far above matched candidate-reversal tails, the prospective zero is valid for the frozen algorithm-excess definition but cannot be interpreted as a strong null for phase-boundary reversals generally. It diagnoses an over-conservative or estimand-mismatched null court rather than absence of recovery.',
 'scientific_definition_changed':False,
 'human_observations':0
}
OUT.joinpath('ZERO_COURT_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','prospective_result_unchanged','holdout','calibration','frozen_threshold_above_entire_holdout_method_phase_max_combos','method_phase_combo_n','posthoc_observed_candidate_matched_sensitivity','adjudication']},indent=2))
