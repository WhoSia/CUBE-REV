#!/usr/bin/env python3
from pathlib import Path
from collections import Counter,defaultdict
import json,math,random,hashlib

ROOT=Path('/tmp/r18matched')
TH=ROOT/'MATCHED_CANDIDATE_NULL_THRESHOLD.json'
CAL=ROOT/'MATCHED_CANDIDATE_NULL_CALIBRATION.json'
HOLD=Path('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_COURT.json')
SUP=Path('research/0.10.5-r1.8/evidence-support-preflight/SUPPORT_PREFLIGHT.json')
PROS=Path('research/0.10.5-r1.8/evidence-null-calibration-r2/NULL_THRESHOLD_SEAL.json')

th=json.loads(TH.read_text()); cal=json.loads(CAL.read_text()); h=json.loads(HOLD.read_text()); sup=json.loads(SUP.read_text()); pros=json.loads(PROS.read_text())
assert th['status']=='POSTHOC_REMAND_AFTER_PROSPECTIVE_ZERO'
assert h['primary']['attempt_any_algorithm_excess_standardized']==0
assert pros['seal_sha256']=='1343a667600a4a859ae081b3b3042cbe365e447b7b082dd7ebf77b9edc8494ea'
floor=pros['minimum_candidate_floor']

records=[r for r in h['records'] if r.get('admission')=='STATE_CERTIFIED']
record_by_key={(int(r['result_id']),int(r['attempt_number'])):r for r in records}
segments=h['segments']

def threshold(method,phase):
    x=th['thresholds'].get(f'{method}|{phase}')
    if x:return x['threshold'],x['level']
    return th['calibration_summary']['global']['p995'],'GLOBAL_99_5_UNSEEN'

positive=[]
for z in segments:
    t,level=threshold(z['method'],z['phase'])
    amp=float(z['candidate_reversal_amplitude'])
    if amp>=floor-1e-12 and amp>t+1e-12:
        positive.append({**z,'posthoc_matched_threshold':t,'posthoc_threshold_level':level,'posthoc_excess_margin':amp-t})
poskeys={(int(z['result_id']),int(z['attempt_number'])) for z in positive}
for k,r in record_by_key.items():r['_posthoc_positive']=k in poskeys

support_cells={f"{c['speed']}|{c['era']}":int(c['population_n']) for c in sup['cell_support'] if c['untouched_supported']}
covered={cell:N for cell,N in support_cells.items() if any(r['cell']==cell for r in records)}

def standardize(getter):
    num=den=0.0
    for cell,N in covered.items():
        rs=[r for r in records if r['cell']==cell]
        if not rs:continue
        v=sum(float(getter(r)) for r in rs)/len(rs)
        num+=N*v;den+=N
    return num/den if den else None
point=standardize(lambda r:1 if r['_posthoc_positive'] else 0)

seed=int(hashlib.sha256((pros['seal_sha256']+'POSTHOC_MATCHED_NULL').encode()).hexdigest()[:16],16)
rng=random.Random(seed); boots=[]
for _ in range(2000):
    num=den=0.0
    for cell,N in covered.items():
        rs=[r for r in records if r['cell']==cell]
        if not rs:continue
        s=sum(1 if rng.choice(rs)['_posthoc_positive'] else 0 for _ in range(len(rs)))
        num+=N*(s/len(rs));den+=N
    if den:boots.append(num/den)
def q(xs,p):
    a=sorted(xs);return a[min(len(a)-1,max(0,math.ceil(p*len(a))-1))] if a else None

by_mp={}
for key in sorted(set((z['method'],z['phase']) for z in segments)):
    m,p=key;t,level=threshold(m,p);zs=[z for z in segments if z['method']==m and z['phase']==p];pp=[z for z in positive if z['method']==m and z['phase']==p]
    by_mp[f'{m}|{p}']={'holdout_segments':len(zs),'threshold':t,'level':level,'positive_segments':len(pp),'rate':len(pp)/len(zs) if zs else None,'max_candidate_reversal':max([float(z['candidate_reversal_amplitude']) for z in zs],default=None)}

phase=Counter(z['phase'] for z in positive);method=Counter(z['method'] for z in positive);cells=Counter(record_by_key[(int(z['result_id']),int(z['attempt_number']))]['cell'] for z in positive)
unique_positive_records=[record_by_key[k] for k in poskeys]
raw=len(poskeys)/len(records)

out={
 'schema_version':'CR0105R18-MATCHED-CANDIDATE-NULL-HOLDOUT-SENSITIVITY-POSTHOC-1',
 'status':'PASS_POSTHOC_DIAGNOSTIC',
 'role':'POSTHOC_REMAND_DIAGNOSTIC_ONLY_AFTER_PROSPECTIVE_ZERO',
 'prospective_primary_unchanged':{'attempt_positive_rate_raw':0,'attempt_positive_rate_standardized':0,'null_seal':pros['seal_sha256']},
 'matched_null':{
   'calibration_status':cal['status'],'calibration_segments':cal['eligible_phase_segments'],
   'global':cal['global'],'threshold_file_sha256':hashlib.sha256(TH.read_bytes()).hexdigest(),
   'warning':'Matched thresholds were constructed after the prospective zero was known. They cannot replace, rescue, or reinterpret the prospective primary result.'
 },
 'holdout':{
   'state_certified_attempts':len(records),'eligible_segments':len(segments),
   'positive_segments':len(positive),'positive_attempts':len(poskeys),'raw_attempt_rate':raw,
   'untouched_support_standardized_attempt_rate':point,
   'bootstrap_95':{'lo':q(boots,.025),'hi':q(boots,.975),'replicates':len(boots)},
   'phase_counts':dict(phase),'method_counts':dict(method),'cell_counts':dict(cells)
 },
 'method_phase':by_mp,
 'positive_segments':positive,
 'positive_attempts':[{'result_id':int(r['result_id']),'attempt_number':int(r['attempt_number']),'reco_id':r['reco_id'],'cell':r['cell'],'method':r['method'],'algorithm_excess_segments':sum(1 for z in positive if int(z['result_id'])==int(r['result_id']) and int(z['attempt_number'])==int(r['attempt_number']))} for r in unique_positive_records],
 'adjudication':'If this matched-statistic posthoc sensitivity is materially nonzero while the prospective frozen-envelope court is zero, the correct R1.8 conclusion is measurement-court mismatch/over-conservatism, not prospective evidence of recovery. The matched construction should be prospectively frozen and retested on a new data vintage in a later version.',
 'human_observations':0
}
ROOT.joinpath('MATCHED_NULL_HOLDOUT_SENSITIVITY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','prospective_primary_unchanged','matched_null','holdout','adjudication']},indent=2))
