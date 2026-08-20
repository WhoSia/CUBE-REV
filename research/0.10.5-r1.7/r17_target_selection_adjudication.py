#!/usr/bin/env python3
import json,math
from pathlib import Path
SRC=Path('research/0.10.5-r1.7/evidence-selection/SELECTION_CORRECTION_COURT.json')
OUT=Path('research/0.10.5-r1.7/evidence-selection-target')
OUT.mkdir(parents=True,exist_ok=True)
x=json.loads(SRC.read_text())
SC={s['name']:s for s in x['schemes']}

def wq(vals,q):
    vals=sorted((float(w),int(n)) for w,n in vals if n>0); total=sum(n for _,n in vals); t=q*total; s=0
    for w,n in vals:
        s+=n
        if s>=t:return w
    return vals[-1][0] if vals else None

def adjudicate(name,scheme_name,pred):
    cells=[c for c in SC[scheme_name]['cells'] if pred(c)]
    pop=sum(c['population_n'] for c in cells); linked=sum(c['linked_n'] for c in cells)
    supported=[c for c in cells if c['population_n']>=100 and c['linked_n']>=5]
    spop=sum(c['population_n'] for c in supported); slink=sum(c['linked_n'] for c in supported)
    zero=sum(c['population_n'] for c in cells if c['linked_n']==0)
    low=sum(c['population_n'] for c in cells if 0<c['linked_n']<5)
    if not supported:return {'name':name,'scheme':scheme_name,'status':'HOLD_NO_SUPPORTED_CELLS'}
    mean_raw=spop/max(1,slink)
    weights=[]
    for c in supported:
        w=(c['population_n']/c['linked_n'])/mean_raw
        weights.append((w,c['linked_n'],c))
    sw=sum(w*n for w,n,_ in weights); sw2=sum(w*w*n for w,n,_ in weights); ess=sw*sw/sw2 if sw2 else 0
    stats={'min':min(w for w,_,_ in weights),'p50':wq([(w,n) for w,n,_ in weights],.5),'p90':wq([(w,n) for w,n,_ in weights],.9),'p95':wq([(w,n) for w,n,_ in weights],.95),'p99':wq([(w,n) for w,n,_ in weights],.99),'max':max(w for w,_,_ in weights),'ess':ess,'ess_fraction':ess/max(1,slink)}
    sens=[]
    target={tuple((k,c[k]) for k in SC[scheme_name]['dimensions']):c['population_n']/spop for c in supported}
    for cap in [2,5,10,20,25,50]:
        m={}; den=0; den2=0
        for w,n,c in weights:
            wc=min(w,cap); mass=n*wc; key=tuple((k,c[k]) for k in SC[scheme_name]['dimensions']);m[key]=mass;den+=mass;den2+=n*wc*wc
        tv=.5*sum(abs((m.get(k,0)/den)-v) for k,v in target.items()) if den else 1
        sens.append({'cap':cap,'ess':den*den/den2 if den2 else 0,'target_cell_tv':tv})
    coverage=spop/max(1,pop); linkcov=slink/max(1,linked)
    # Internal gate declared before inspecting route-phenotype outcomes.
    gate=(coverage>=.95 and linkcov>=.90 and ess>=200 and stats['ess_fraction']>=.05 and stats['p99']<=25 and stats['max']<=50)
    return {'name':name,'scheme':scheme_name,'status':'PASS_INTERNAL_WEIGHT_GATE' if gate else 'HOLD_INTERNAL_WEIGHT_GATE',
            'target_population_n':pop,'target_linked_n':linked,'supported_population_n':spop,'supported_population_fraction':coverage,
            'supported_linked_n':slink,'supported_linked_fraction':linkcov,'zero_overlap_population_n':zero,'zero_overlap_fraction':zero/max(1,pop),'lt5_link_population_n':low,'lt5_link_fraction':low/max(1,pop),
            'stabilized_weight':stats,'trim_sensitivity':sens,
            'gate':{'population_coverage_min':.95,'linked_coverage_min':.90,'ess_min':200,'ess_fraction_min':.05,'p99_max':25,'max_weight_max':50}}

is_u10=lambda c:c.get('speed') in ('<5','5-7','7-10')
is_u7=lambda c:c.get('speed') in ('<5','5-7')
is_mod=lambda c:c.get('era')=='2023-26'
results=[
 adjudicate('UNDER10_SPEED_ONLY','speed_only',is_u10),
 adjudicate('UNDER10_SPEED_X_ERA','speed_x_era',is_u10),
 adjudicate('UNDER10_SPEED_X_ERA_X_ROUNDMEDIAN','speed_x_era_x_roundmedian',is_u10),
 adjudicate('UNDER7_SPEED_ONLY','speed_only',is_u7),
 adjudicate('UNDER7_SPEED_X_ERA','speed_x_era',is_u7),
 adjudicate('MODERN_2023_26_UNDER10_SPEED_X_ERA','speed_x_era',lambda c:is_u10(c) and is_mod(c)),
 adjudicate('MODERN_2023_26_UNDER10_SPEED_X_ERA_X_ROUNDMEDIAN','speed_x_era_x_roundmedian',lambda c:is_u10(c) and is_mod(c)),
]
passes=[r['name'] for r in results if r['status'].startswith('PASS')]
out={'schema_version':'CR0105R17-TARGET-SELECTION-ADJUDICATION-1','status':'PASS','source_selection_run_id':32323654544,
     'results':results,'internal_weight_gate_passes':passes,
     'estimand_decision':{
       'full_wca_population':'PROHIBITED_ZERO_OVERLAP',
       'speed_poststratified_sub10':'DESCRIPTIVE_SENSITIVITY_ONLY' if 'UNDER10_SPEED_ONLY' in passes else 'HOLD',
       'multidimensional_sub10':'ADMISSIBLE_OVERLAP_RESTRICTED_ONLY' if any(n in passes for n in ['UNDER10_SPEED_X_ERA','UNDER10_SPEED_X_ERA_X_ROUNDMEDIAN']) else 'HOLD',
       'rule':'Never present speed-only poststratification as removing era/performance selection. If multidimensional target fails the declared gate, estimate route phenotypes only in the explicitly supported overlap domain and report population coverage.'
     },'human_observations':0}
(OUT/'TARGET_SELECTION_ADJUDICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
