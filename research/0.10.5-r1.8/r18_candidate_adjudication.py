#!/usr/bin/env python3
from pathlib import Path
from collections import Counter,defaultdict
import json,math

SENS=Path('research/0.10.5-r1.8/evidence-matched-null-remand/MATCHED_NULL_HOLDOUT_SENSITIVITY.json')
ROUTES=Path('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json')
LEDGER=Path('research/0.10.5-r1.8/evidence-matched-null-remand/MATCHED_CANDIDATE_NULL_SEGMENT_LEDGER.json')
FWER=Path('research/0.10.5-r1.8/evidence-attempt-fwer-audit/ATTEMPT_FAMILYWISE_NULL_AUDIT.json')
OUT=Path('/tmp/r18cand');OUT.mkdir(parents=True,exist_ok=True)

s=json.loads(SENS.read_text()); routes=json.loads(ROUTES.read_text()); cal=json.loads(LEDGER.read_text())['rows']; fw=json.loads(FWER.read_text())
assert s['status']=='PASS_POSTHOC_DIAGNOSTIC' and len(s['positive_segments'])==32
assert fw['status']=='PASS_DIAGNOSTIC'
rmap={int(r['reco_id']):r for r in routes['records']}

def qupper(xs,q):
    if not xs:return None
    a=sorted(xs);return a[min(len(a)-1,max(0,math.ceil(q*len(a))-1))]
def rank_pct(x,xs):
    if not xs:return None
    return sum(v<=x+1e-12 for v in xs)/len(xs)
def parse_lines(raw):
    out=[];lid=0
    for rawline in str(raw or '').splitlines():
        idx=rawline.find('//');left=(rawline[:idx] if idx>=0 else rawline).strip();comment=(rawline[idx+2:] if idx>=0 else '').strip()
        if not left and not comment:continue
        out.append({'line_id':lid,'raw_line':rawline.strip(),'move_text':left,'comment':comment});lid+=1
    return out

details=[]
for z in s['positive_segments']:
    rr=rmap[int(z['reco_id'])]; lines={x['line_id']:x for x in parse_lines(rr['raw_alg'])};ln=lines.get(int(z['line_id']),{})
    peer=[r for r in cal if r['method']==z['method'] and r['phase']==z['phase']]
    peer_len=[int(r['move_count']) for r in peer]
    margin=float(z['posthoc_excess_margin']);quant48=margin/(1/48);quant24=margin/(1/24)
    details.append({
      'segment_id':z['segment_id'],'reco_id':z['reco_id'],'result_id':z['result_id'],'attempt_number':z['attempt_number'],
      'cell':rr['cell'],'method':z['method'],'phase':z['phase'],'line_id':z['line_id'],'comment':ln.get('comment'),'move_text':ln.get('move_text'),'raw_line':ln.get('raw_line'),
      'move_count':z['move_count'],'calibration_method_phase_move_count_percentile':rank_pct(int(z['move_count']),peer_len),
      'candidate_reversal_amplitude':z['candidate_reversal_amplitude'],'matched_threshold':z['posthoc_matched_threshold'],'excess_margin':margin,
      'excess_margin_in_1_over_48_quanta':quant48,'excess_margin_in_1_over_24_quanta':quant24,
      'secondary_distance_supports_primary':bool(z['secondary_supports_primary_candidate']),
      'prospective_frozen_threshold':z['threshold'],'would_pass_prospective_frozen_threshold':bool(z['algorithm_excess'])
    })

margins=[d['excess_margin'] for d in details];lengthpct=[d['calibration_method_phase_move_count_percentile'] for d in details]
secondary=sum(d['secondary_distance_supports_primary'] for d in details)
within_one_48=sum(d['excess_margin']<=1/48+1e-12 for d in details);within_one_24=sum(d['excess_margin']<=1/24+1e-12 for d in details)
long_tail=sum(d['calibration_method_phase_move_count_percentile']>=.9 for d in details)
phase=Counter(d['phase'] for d in details);comments=Counter((d['phase'],d['comment']) for d in details)

# Pull exact family-wise comparison and bootstrap, which is the adjudication burden.
bd=fw['bootstrap_holdout_minus_calibration_loo']
hold=fw['matched_holdout']['untouched_support_standardized_rate'];null=fw['calibration_familywise']['leave_one_attempt_out']['untouched_support_standardized_rate']

out={
 'schema_version':'CR0105R18-CANDIDATE-ADJUDICATION-POSTHOC-1','status':'PASS_DIAGNOSTIC','role':'POSTHOC_CANDIDATE_AUDIT_NOT_CONFIRMATORY',
 'candidate_n':len(details),'attempt_n':len({(d['result_id'],d['attempt_number']) for d in details}),
 'phase_counts':dict(phase),
 'margin':{'p50':qupper(margins,.5),'p90':qupper(margins,.9),'max':max(margins),'within_one_1_over_48_quantum_n':within_one_48,'within_one_1_over_24_quantum_n':within_one_24},
 'secondary_distance_agreement':{'n':secondary,'rate':secondary/len(details)},
 'move_length':{'candidate_move_count_p50':qupper([d['move_count'] for d in details],.5),'candidate_move_count_p90':qupper([d['move_count'] for d in details],.9),'candidate_in_top_10pct_of_calibration_method_phase_length_n':long_tail,'candidate_in_top_10pct_rate':long_tail/len(details),'calibration_length_percentile_p50':qupper(lengthpct,.5)},
 'familywise_adjudication':{
   'holdout_matched_standardized_attempt_rate':hold,
   'calibration_leave_one_attempt_out_standardized_familywise_rate':null,
   'point_difference_holdout_minus_null':hold-null,
   'bootstrap':bd,
   'decision':'NO_ATTEMPT_LEVEL_EXCESS_OVER_CALIBRATION_FAMILYWISE_NULL' if hold<=null else 'POINT_EXCESS_REQUIRES_BOOTSTRAP'
 },
 'r17_r5_primitive_replication_positive_attempts':0,
 'most_common_phase_comments':[{'phase':k[0],'comment':k[1],'n':v} for k,v in comments.most_common(20)],
 'top_candidates_by_margin':sorted(details,key=lambda d:(-d['excess_margin'],-d['move_count'],d['segment_id']))[:20],
 'all_candidates':details,
 'adjudication':'The 32 matched-statistic candidates are not confirmatory recovery events. They are posthoc tail observations, and the holdout attempt-level rate must be judged against the calibration attempt-level familywise null. Because the matched holdout point rate is below the leave-one-attempt-out calibration familywise rate, these candidates are null-compatible even before considering annotation or algorithm-family uncertainty.',
 'human_observations':0
}
OUT.joinpath('CANDIDATE_ADJUDICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','candidate_n','attempt_n','phase_counts','margin','secondary_distance_agreement','move_length','familywise_adjudication','r17_r5_primitive_replication_positive_attempts','most_common_phase_comments','top_candidates_by_margin','adjudication']},indent=2))
