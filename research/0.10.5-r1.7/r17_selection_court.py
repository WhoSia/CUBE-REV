#!/usr/bin/env python3
import json,math,os
from pathlib import Path
import duckdb

DB=Path(os.environ['R17_PARENT_DB'])
OUT=Path(os.environ.get('R17_OUT','research/0.10.5-r1.7/evidence-selection'))
OUT.mkdir(parents=True,exist_ok=True)
con=duckdb.connect(str(DB),read_only=True)

con.execute("""CREATE TEMP TABLE linked_attempts AS
select distinct c.result_id,c.attempt_number
from linkage_class l join linkage_candidates c using(reco_id)
where l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE')""")
con.execute("""CREATE TEMP TABLE selection_frame AS
select p.result_id,p.attempt_number,p.attempt_value,p.comp_year,p.med_valid,
 case when p.attempt_value<500 then '<5' when p.attempt_value<700 then '5-7' when p.attempt_value<1000 then '7-10'
      when p.attempt_value<1500 then '10-15' when p.attempt_value<3000 then '15-30' else '30+' end speed,
 case when p.comp_year<=2012 then '<=2012' when p.comp_year<=2016 then '2013-16' when p.comp_year<=2019 then '2017-19'
      when p.comp_year<=2022 then '2020-22' else '2023-26' end era,
 case when p.med_valid<700 then '<7' when p.med_valid<1000 then '7-10' when p.med_valid<1500 then '10-15'
      when p.med_valid<3000 then '15-30' else '30+' end perf,
 case when l.result_id is null then 0 else 1 end selected
from phenotype_attempts p left join linked_attempts l using(result_id,attempt_number)
where p.attempt_value>0""")

TOTAL_POP=con.execute('select count(*) from selection_frame').fetchone()[0]
TOTAL_LINK=con.execute('select count(*) from selection_frame where selected=1').fetchone()[0]

def aggregate(cols):
    g=','.join(cols)
    rows=con.execute(f"select {g},count(*) n,sum(selected) linked from selection_frame group by {g} order by {g}").fetchall()
    out=[]
    for row in rows:
        key=dict(zip(cols,row[:len(cols)])); n=int(row[-2]); linked=int(row[-1] or 0)
        out.append({**key,'population_n':n,'linked_n':linked,'p_select':linked/n if n else 0.0})
    return out

def weighted_quantile(vals,q):
    # vals = (value, multiplicity)
    vals=sorted((float(v),int(n)) for v,n in vals if n>0)
    total=sum(n for _,n in vals)
    if not total:return None
    target=q*total; s=0
    for v,n in vals:
        s+=n
        if s>=target:return v
    return vals[-1][0]

def scheme(name,cols,min_link=5,min_pop=100):
    cells=aggregate(cols)
    supported=[c for c in cells if c['linked_n']>=min_link and c['population_n']>=min_pop]
    positive=[c for c in cells if c['linked_n']>0]
    pop=sum(c['population_n'] for c in supported); link=sum(c['linked_n'] for c in supported)
    # stabilized IPW has mean one on selected records in the supported target.
    for c in supported:
        c['raw_ipw']=c['population_n']/c['linked_n']
    mean_raw=sum(c['linked_n']*c['raw_ipw'] for c in supported)/max(1,link)
    for c in supported:c['stabilized_ipw']=c['raw_ipw']/mean_raw
    sw=sum(c['linked_n']*c['stabilized_ipw'] for c in supported)
    sw2=sum(c['linked_n']*(c['stabilized_ipw']**2) for c in supported)
    ess=sw*sw/sw2 if sw2 else 0
    weight_dist=[(c['stabilized_ipw'],c['linked_n']) for c in supported]
    sensitivity=[]
    target_mass={tuple(c[k] for k in cols):c['population_n']/pop for c in supported} if pop else {}
    for cap in [5,10,25,50,100]:
        masses={}; wsum=0; w2=0
        for c in supported:
            w=min(c['stabilized_ipw'],cap); m=c['linked_n']*w
            key=tuple(c[k] for k in cols); masses[key]=m; wsum+=m; w2+=c['linked_n']*w*w
        tv=0.5*sum(abs((masses.get(k,0)/wsum if wsum else 0)-v) for k,v in target_mass.items())
        sensitivity.append({'cap':cap,'ess':wsum*wsum/w2 if w2 else 0,'cell_distribution_tv':tv,'max_weight_after_cap':min(cap,max((c['stabilized_ipw'] for c in supported),default=0))})
    return {'name':name,'dimensions':cols,'cells_total':len(cells),'cells_positive':len(positive),'cells_supported_min5':len(supported),
            'population_supported_n':pop,'population_supported_fraction':pop/TOTAL_POP,'linked_supported_n':link,'linked_supported_fraction':link/max(1,TOTAL_LINK),
            'raw_ipw_mean':mean_raw,'stabilized_weight':{
                'min':min((c['stabilized_ipw'] for c in supported),default=None),'p50':weighted_quantile(weight_dist,.5),'p90':weighted_quantile(weight_dist,.9),
                'p95':weighted_quantile(weight_dist,.95),'p99':weighted_quantile(weight_dist,.99),'max':max((c['stabilized_ipw'] for c in supported),default=None),
                'ess':ess,'ess_fraction_of_linked_supported':ess/max(1,link)},
            'trim_sensitivity':sensitivity,'cells':cells}

schemes=[scheme('speed_only',['speed']),scheme('speed_x_era',['speed','era']),scheme('speed_x_era_x_roundmedian',['speed','era','perf'])]
# Explicit candidate target courts, chosen prospectively from R1.6 support diagnostics.
targets=[]
for name,where in [
 ('ALL_VALID','1=1'),
 ('UNDER15','attempt_value<1500'),
 ('UNDER10','attempt_value<1000'),
 ('MODERN_2023_26_UNDER15','comp_year>=2023 and attempt_value<1500'),
 ('MODERN_2023_26_UNDER10','comp_year>=2023 and attempt_value<1000')]:
    n,linked=con.execute(f'select count(*),sum(selected) from selection_frame where {where}').fetchone()
    targets.append({'name':name,'population_n':int(n),'linked_n':int(linked or 0),'selection_rate':float((linked or 0)/n) if n else 0.0})

# For every speed×era×performance cell, quantify hard zero-overlap mass.
full=schemes[-1]['cells']
zero_pop=sum(c['population_n'] for c in full if c['linked_n']==0)
low5_pop=sum(c['population_n'] for c in full if 0<c['linked_n']<5)
out={
 'schema_version':'CR0105R17-SELECTION-COURT-1','status':'PASS',
 'parent_db_sha256':'a04f1d2fd351e34ec7406e63524b7b8ceb166bf8a53d4630f94c9d6a792848f1',
 'population_valid_attempts':TOTAL_POP,'linked_distinct_attempts_in_db':TOTAL_LINK,
 'schemes':schemes,'candidate_targets':targets,
 'full_cell_overlap':{'zero_link_population_n':zero_pop,'zero_link_population_fraction':zero_pop/TOTAL_POP,'positive_but_lt5_link_population_n':low5_pop,'positive_but_lt5_link_population_fraction':low5_pop/TOTAL_POP},
 'adjudication_rule':'Full-population prevalence is inadmissible if hard zero-overlap or stabilized-weight instability is material. Prefer the broadest explicitly defined target whose support and ESS remain defensible, and report trimmed sensitivity rather than silently clipping.',
 'human_observations':0
}
(OUT/'SELECTION_CORRECTION_COURT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'population':TOTAL_POP,'linked':TOTAL_LINK,'targets':targets,'scheme_summary':[{k:s[k] for k in ['name','population_supported_fraction','linked_supported_fraction','stabilized_weight']} for s in schemes],'full_cell_overlap':out['full_cell_overlap']},indent=2))
