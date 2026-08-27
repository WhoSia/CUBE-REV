#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict,Counter
import json,math,random,hashlib

CAL=Path('research/0.10.5-r1.8/evidence-matched-null-remand/MATCHED_CANDIDATE_NULL_SEGMENT_LEDGER.json')
TH=Path('research/0.10.5-r1.8/evidence-matched-null-remand/MATCHED_CANDIDATE_NULL_THRESHOLD.json')
SENS=Path('research/0.10.5-r1.8/evidence-matched-null-remand/MATCHED_NULL_HOLDOUT_SENSITIVITY.json')
R17=Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json')
SUP=Path('research/0.10.5-r1.8/evidence-support-preflight/SUPPORT_PREFLIGHT.json')
OUT=Path('/tmp/r18fwer');OUT.mkdir(parents=True,exist_ok=True)

cal=json.loads(CAL.read_text())['rows']; th=json.loads(TH.read_text()); sens=json.loads(SENS.read_text()); r17=json.loads(R17.read_text()); sup=json.loads(SUP.read_text())
assert sens['status']=='PASS_POSTHOC_DIAGNOSTIC'
assert sens['prospective_primary_unchanged']['attempt_positive_rate_standardized']==0

def q(xs,p):
    if not xs:return None
    a=sorted(xs);return a[min(len(a)-1,max(0,math.ceil(p*len(a))-1))]
def cell_of(r):return f"{r['speed']}|{r['era']}"
def fixed_thr(m,p):
    z=th['thresholds'].get(f'{m}|{p}')
    return z['threshold'] if z else th['calibration_summary']['global']['p995']
def loo_thr(rows,excluded_key,m,p):
    keep=[r for r in rows if (int(r['result_id']),int(r['attempt_number']))!=excluded_key]
    mp=[float(r['null_envelope']) for r in keep if r['method']==m and r['phase']==p]
    ph=[float(r['null_envelope']) for r in keep if r['phase']==p]
    gl=[float(r['null_envelope']) for r in keep]
    if len(mp)>=40:return q(mp,.99),'METHOD_PHASE_99'
    if len(ph)>=80:return q(ph,.99),'PHASE_99'
    return q(gl,.995),'GLOBAL_99_5'

# Map calibration attempt keys to R1.7 route metadata/cells.
r17map={(int(r['result_id']),int(r['attempt_number'])):r for r in r17['records']}
by_attempt=defaultdict(list)
for z in cal:by_attempt[(int(z['result_id']),int(z['attempt_number']))].append(z)
fixed_pos={};loo_pos={};fixed_seg=0;loo_seg=0;loo_levels=Counter()
for key,zs in by_attempt.items():
    fp=lp=False
    for z in zs:
        v=float(z['null_envelope']);ft=fixed_thr(z['method'],z['phase'])
        if v>ft+1e-12:fp=True;fixed_seg+=1
        lt,ll=loo_thr(cal,key,z['method'],z['phase']);loo_levels[ll]+=1
        if v>lt+1e-12:lp=True;loo_seg+=1
    fixed_pos[key]=fp;loo_pos[key]=lp

support_cells={f"{c['speed']}|{c['era']}":int(c['population_n']) for c in sup['cell_support'] if c['untouched_supported']}

def standardized(keys,posmap):
    num=den=0.0;cells={}
    for cell,N in support_cells.items():
        ks=[k for k in keys if k in r17map and cell_of(r17map[k])==cell]
        if not ks:continue
        rate=sum(1 if posmap[k] else 0 for k in ks)/len(ks);cells[cell]={'n':len(ks),'population_n':N,'rate':rate,'positives':sum(1 if posmap[k] else 0 for k in ks)};num+=N*rate;den+=N
    return (num/den if den else None),cells,den/sum(support_cells.values())
keys=list(by_attempt)
fixed_std,fixed_cells,fixed_cov=standardized(keys,fixed_pos);loo_std,loo_cells,loo_cov=standardized(keys,loo_pos)
fixed_raw=sum(fixed_pos.values())/len(keys);loo_raw=sum(loo_pos.values())/len(keys)

# Holdout matched sensitivity cells/positives reconstructed from its positive_attempt list and R1.8 holdout court records.
H=Path('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_COURT.json');h=json.loads(H.read_text());hrec=[r for r in h['records'] if r.get('admission')=='STATE_CERTIFIED'];hkeys=[(int(r['result_id']),int(r['attempt_number'])) for r in hrec];hmap={(int(r['result_id']),int(r['attempt_number'])):r for r in hrec};hposkeys={(int(r['result_id']),int(r['attempt_number'])) for r in sens['positive_attempts']}
hpos={k:k in hposkeys for k in hkeys}
def hstandardized(posmap):
    num=den=0.0;cells={}
    for cell,N in support_cells.items():
        ks=[k for k in hkeys if hmap[k]['cell']==cell]
        if not ks:continue
        rate=sum(1 if posmap[k] else 0 for k in ks)/len(ks);cells[cell]={'n':len(ks),'population_n':N,'rate':rate,'positives':sum(1 if posmap[k] else 0 for k in ks)};num+=N*rate;den+=N
    return num/den,cells
hstd,hcells=hstandardized(hpos)

# Independent stratified bootstrap difference: holdout matched-positive rate minus calibration LOO null-FWER rate.
seed=int(hashlib.sha256(b'CR0105R18_ATTEMPT_FWER_POSTHOC').hexdigest()[:16],16);rng=random.Random(seed);diffs=[];hboots=[];cboots=[]
common=[c for c in support_cells if any(hmap[k]['cell']==c for k in hkeys) and any(k in r17map and cell_of(r17map[k])==c for k in keys)]
for _ in range(5000):
    hn=hd=cn=cd=0.0
    for cell in common:
        N=support_cells[cell];hk=[k for k in hkeys if hmap[k]['cell']==cell];ck=[k for k in keys if k in r17map and cell_of(r17map[k])==cell]
        hs=sum(1 if hpos[rng.choice(hk)] else 0 for _ in range(len(hk)))/len(hk)
        cs=sum(1 if loo_pos[rng.choice(ck)] else 0 for _ in range(len(ck)))/len(ck)
        hn+=N*hs;hd+=N;cn+=N*cs;cd+=N
    hv=hn/hd;cv=cn/cd;hboots.append(hv);cboots.append(cv);diffs.append(hv-cv)

def summary(xs):return {'p2_5':q(xs,.025),'p50':q(xs,.5),'p97_5':q(xs,.975)}

# Distribution of number of eligible phase tests per attempt: multiplicity diagnostic.
phase_counts=[len(zs) for zs in by_attempt.values()];hphase=Counter((int(z['result_id']),int(z['attempt_number'])) for z in h['segments']);hphase_counts=[hphase[k] for k in hkeys]

out={
 'schema_version':'CR0105R18-ATTEMPT-FAMILYWISE-NULL-AUDIT-POSTHOC-1','status':'PASS_DIAGNOSTIC','role':'POSTHOC_MULTIPLICITY_AND_ROUTE_LEVEL_NULL_AUDIT_NOT_PROSPECTIVE_PRIMARY',
 'prospective_primary_unchanged':0,
 'matched_holdout':{'positive_attempts':len(hposkeys),'state_certified_attempts':len(hkeys),'raw_rate':len(hposkeys)/len(hkeys),'untouched_support_standardized_rate':hstd,'cells':hcells},
 'calibration_familywise':{
   'attempts':len(keys),'eligible_segments':len(cal),'fixed_full_calibration_threshold':{'positive_attempts':sum(fixed_pos.values()),'raw_rate':fixed_raw,'positive_segments':fixed_seg,'untouched_support_standardized_rate':fixed_std,'coverage_of_untouched_support':fixed_cov,'cells':fixed_cells},
   'leave_one_attempt_out':{'positive_attempts':sum(loo_pos.values()),'raw_rate':loo_raw,'positive_segments':loo_seg,'untouched_support_standardized_rate':loo_std,'coverage_of_untouched_support':loo_cov,'threshold_levels':dict(loo_levels),'cells':loo_cells}
 },
 'multiplicity':{
   'calibration_segments_per_attempt':{'p50':q(phase_counts,.5),'p90':q(phase_counts,.9),'max':max(phase_counts)},
   'holdout_segments_per_attempt':{'p50':q(hphase_counts,.5),'p90':q(hphase_counts,.9),'max':max(hphase_counts)},
   'independent_six_tests_reference_probability':1-(.99**6)
 },
 'bootstrap_holdout_minus_calibration_loo':{'replicates':len(diffs),'holdout':summary(hboots),'calibration_loo':summary(cboots),'difference':summary(diffs),'probability_difference_gt_zero':sum(d>0 for d in diffs)/len(diffs)},
 'adjudication':'A matched segment-level tail can only motivate a recovery-like route anomaly if the holdout attempt-level exceedance is above the attempt-level familywise rate generated by the calibration null under the same multiplicity. If not, the apparent matched-null positives are explained by repeated per-phase testing and remain null-compatible.',
 'human_observations':0
}
OUT.joinpath('ATTEMPT_FAMILYWISE_NULL_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
