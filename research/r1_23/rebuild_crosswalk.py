#!/usr/bin/env python3
import argparse, csv, hashlib, json, statistics
from collections import Counter, defaultdict
from pathlib import Path

EVENT_MAP = {
    '3x3':'333','2x2':'222','4x4':'444','5x5':'555','6x6':'666','7x7':'777',
    'OH':'333oh','oh':'333oh',
    '3BLD':'333bf','3bld':'333bf','4BLD':'444bf','4bld':'444bf','5BLD':'555bf','5bld':'555bf',
    'FMC':'333fm','fmc':'333fm','MBLD':'333mbf','mbld':'333mbf',
    'Pyraminx':'pyram','pyra':'pyram','pyraminx':'pyram',
    'Skewb':'skewb','skewb':'skewb','SQ1':'sq1','sq1':'sq1',
    'Megaminx':'minx','megaminx':'minx','minx':'minx','Clock':'clock','clock':'clock',
}
# CubeRoot's current recon snapshot uses folded source tokens 1/2/3/f rather than
# preserving every WCA round_type_id. Expand only within the official WCA bucket.
ROUND_BUCKETS = {
    '1':['1','d','0','h'], 'R1':['1','d','0','h'],
    '2':['2','e','g'],     'R2':['2','e','g'],
    '3':['3'],             'R3':['3'],
    'f':['f','c','b'],     'Fi':['f','c','b'],
}
STANDARD_TIMED = {'333','222','444','555','666','777','333oh','333bf','444bf','555bf','pyram','skewb','sq1','minx','clock'}
EXACT_CLASSES = {'EXACT_ATTEMPT_LINK_DECLARED_SOLVENUM','EXACT_ATTEMPT_LINK_REPAIRED_SOLVENUM'}


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20), b''): h.update(b)
    return h.hexdigest()

def fnum(x):
    try: return float(x)
    except Exception: return None

def expected_attempt(event_id, raw_time):
    x=fnum(raw_time)
    if x is None: return None
    if event_id in STANDARD_TIMED: return int(round(x*100))
    if event_id == '333fm': return int(round(x))
    return None

def norm_round(x):
    if x is None: return [], 'MISSING'
    s=str(x).strip()
    if s in ROUND_BUCKETS:
        basis='FOLDED_SOURCE_BUCKET_TOKEN' if s in {'1','2','3','f'} else 'LEGACY_BUCKET_LABEL'
        return ROUND_BUCKETS[s], basis
    return [], 'UNRESOLVED_TOKEN'

def rankdata(vals):
    order=sorted(range(len(vals)), key=lambda i: vals[i]); ranks=[0.0]*len(vals); i=0
    while i<len(order):
        j=i+1
        while j<len(order) and vals[order[j]]==vals[order[i]]: j+=1
        r=(i+j-1)/2+1
        for k in range(i,j): ranks[order[k]]=r
        i=j
    return ranks

def pearson(x,y):
    if len(x)<3: return None
    mx=sum(x)/len(x); my=sum(y)/len(y)
    num=sum((a-mx)*(b-my) for a,b in zip(x,y))
    den=(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))**0.5
    return None if den==0 else num/den

def spearman(x,y):
    return pearson(rankdata(x),rankdata(y)) if len(x)>=3 else None

def med(xs): return statistics.median(xs) if xs else None

def write_csv(path,data):
    keys=list(data[0].keys()) if data else []
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(data)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--recons',required=True); ap.add_argument('--attempts',required=True); ap.add_argument('--out',required=True)
    args=ap.parse_args(); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    recons=json.load(open(args.recons,encoding='utf-8')); attempts=json.load(open(args.attempts,encoding='utf-8'))
    official_census=Counter(str(r.get('official')) for r in recons)
    wca=[r for r in recons if r.get('official')=='wca']; byid={str(r.get('id')):r for r in wca if r.get('id') is not None}

    rows=[]
    for r in wca:
        rid=str(r.get('id')); event_raw=r.get('event'); eid=EVENT_MAP.get(event_raw)
        rounds,round_basis=norm_round(r.get('round')); comp=r.get('compWcaId'); person=r.get('personId')
        solve=r.get('solveNum')
        try: solve_i=int(solve)
        except Exception: solve_i=None
        exp=expected_attempt(eid,r.get('rawTime')) if eid else None
        round_entries=[]; declared=[]; value_positions=[]
        if comp and person and eid and rounds:
            pdata=attempts.get(str(comp),{}).get(str(person),{})
            for rt in rounds:
                key=f'{eid}_{rt}'; ent=pdata.get(key)
                if not ent or not isinstance(ent.get('a'),list): continue
                arr=ent['a']; round_entries.append({'key':key,'round_type_id':rt,'a':arr})
                if solve_i and 1 <= solve_i <= len(arr):
                    declared.append({'key':key,'round_type_id':rt,'attempt_num':solve_i,'attempt_value':arr[solve_i-1]})
                if exp is not None:
                    for pos,val in enumerate(arr,1):
                        if val==exp:
                            value_positions.append({'key':key,'round_type_id':rt,'attempt_num':pos,'attempt_value':val})
        direct=[c for c in value_positions if solve_i is not None and c['attempt_num']==solve_i]
        admitted=None
        if not comp or not person or solve_i is None:
            cls='SOURCE_METADATA_INSUFFICIENT'
        elif eid is None:
            cls='EVENT_UNSUPPORTED'
        elif not rounds:
            cls='ROUND_TOKEN_UNRESOLVED'
        elif not round_entries:
            cls='NO_SIDECAR_ROUND_ENTRY'
        elif exp is None:
            if len(declared)==1:
                cls='STRUCTURAL_UNIQUE_UNVALIDATED'; admitted=declared[0]
            elif len(declared)>1: cls='ROUND_AMBIGUOUS_UNVALIDATED'
            else: cls='NO_DECLARED_ATTEMPT_IN_RANGE'
        elif len(direct)==1:
            cls='EXACT_ATTEMPT_LINK_DECLARED_SOLVENUM'; admitted=direct[0]
        elif len(direct)>1:
            cls='ROUND_AMBIGUOUS_AT_DECLARED_SOLVENUM'
        elif len(value_positions)==1:
            cls='EXACT_ATTEMPT_LINK_REPAIRED_SOLVENUM'; admitted=value_positions[0]
        elif len(value_positions)>1:
            cls='VALUE_COLLISION_ATTEMPT_AMBIGUOUS'
        elif len(declared)==1:
            cls='STRUCTURAL_LINK_TIME_MISMATCH'
        elif len(declared)>1:
            cls='ROUND_AMBIGUOUS_NO_VALUE_RESOLUTION'
        else:
            cls='NO_VALUE_MATCH_WITHIN_ROUND'

        declared_vals='|'.join(f"{c['key']}#{c['attempt_num']}={c['attempt_value']}" for c in declared)
        value_hits='|'.join(f"{c['key']}#{c['attempt_num']}={c['attempt_value']}" for c in value_positions)
        rows.append({
            'recon_id':rid,'event':event_raw,'event_id':eid,'date':r.get('date'),'year':str(r.get('date',''))[:4],
            'comp':r.get('comp'),'compWcaId':comp,'person':r.get('person'),'personId':person,
            'reconer':r.get('reconer'),'reconerId':r.get('reconerId'),'method':r.get('method'),
            'round_raw':r.get('round'),'round_basis':round_basis,'round_candidates':'|'.join(rounds),
            'declared_solveNum':solve_i,'rawTime':r.get('rawTime'),'expected_attempt_value':exp,'classification':cls,
            'round_entry_count':len(round_entries),'declared_candidate_count':len(declared),'value_hit_count':len(value_positions),
            'declared_candidates':declared_vals,'value_hits':value_hits,
            'admitted_key':admitted['key'] if admitted else '',
            'admitted_solveNum':admitted['attempt_num'] if admitted else '',
            'solveNum_repair_delta':(admitted['attempt_num']-solve_i) if admitted and solve_i is not None else '',
            'official_attempt_value':admitted['attempt_value'] if admitted else '',
            'stm':r.get('stm'),'tps':r.get('tps'),'completionStatus':r.get('completionStatus'),'value':r.get('value')
        })

    row_by_id={x['recon_id']:x for x in rows}
    legacy=[]
    for comp,ppl in attempts.items():
        for person,pdata in ppl.items():
            for key,ent in pdata.items():
                for sn,rid0 in (ent.get('r') or {}).items():
                    rid=str(rid0); cur=row_by_id.get(rid)
                    if not cur:
                        status='ORPHAN_NOT_IN_CURRENT_WCA_SNAPSHOT'
                    elif cur['classification'] in EXACT_CLASSES and cur['admitted_key']==key and str(cur['admitted_solveNum'])==str(sn):
                        status='AGREES_WITH_REGENERATED_EXACT'
                    else:
                        status='STALE_OR_UNVALIDATED'
                    legacy.append({'compWcaId':comp,'personId':person,'key':key,'solveNum':sn,'recon_id':rid,
                                   'present_in_current_wca_snapshot':rid in byid,
                                   'regenerated_classification':cur['classification'] if cur else 'ORPHAN_NOT_IN_CURRENT_WCA_SNAPSHOT',
                                   'regenerated_admitted_key':cur['admitted_key'] if cur else '',
                                   'regenerated_admitted_solveNum':cur['admitted_solveNum'] if cur else '',
                                   'legacy_status':status})

    write_csv(out/'crosswalk.csv',rows); write_csv(out/'legacy_r_audit.csv',legacy)
    exact_rows=[x for x in rows if x['classification'] in EXACT_CLASSES]

    # Linkage-support positivity only: this is NOT population reconstruction-selection positivity.
    pos=[]
    groupings=[('event',lambda x:(x['event_id'] or x['event'],)),('event_year',lambda x:(x['event_id'] or x['event'],x['year'])),('round',lambda x:(x['event_id'] or x['event'],x['round_raw']))]
    for level,fn in groupings:
        groups=defaultdict(list)
        for x in rows: groups[fn(x)].append(x)
        for k,g in sorted(groups.items(),key=lambda z:str(z[0])):
            ex=[x for x in g if x['classification'] in EXACT_CLASSES]
            comps={x['compWcaId'] for x in ex if x['compWcaId']}; persons={x['personId'] for x in ex if x['personId']}
            qualified=len(g)>=5 and len(ex)>=3 and len(comps)>=2 and len(persons)>=2
            pos.append({'level':level,'stratum':'|'.join('' if q is None else str(q) for q in k),'n_recons':len(g),'n_exact':len(ex),
                        'exact_link_rate':len(ex)/len(g) if g else None,'n_exact_competitions':len(comps),'n_exact_persons':len(persons),
                        'linkage_positivity_gate':'PASS' if qualified else 'HOLD'})
    write_csv(out/'linkage_positivity.csv',pos)

    # Descriptive macro-meso bridge on admitted exact links only.
    bridge=[]
    for ev in sorted({x['event_id'] for x in exact_rows if x['event_id']}):
        g=[x for x in exact_rows if x['event_id']==ev and fnum(x['rawTime']) is not None]
        times=[fnum(x['rawTime']) for x in g]
        stmp=[(fnum(x['rawTime']),fnum(x['stm'])) for x in g if fnum(x['stm']) is not None]
        tpsp=[(fnum(x['rawTime']),fnum(x['tps'])) for x in g if fnum(x['tps']) is not None]
        bridge.append({'event_id':ev,'n_exact':len(g),'n_declared_exact':sum(x['classification']=='EXACT_ATTEMPT_LINK_DECLARED_SOLVENUM' for x in g),
                       'n_repaired_solveNum':sum(x['classification']=='EXACT_ATTEMPT_LINK_REPAIRED_SOLVENUM' for x in g),
                       'median_time_s':med(times),'median_stm':med([b for a,b in stmp]),'median_tps':med([b for a,b in tpsp]),
                       'spearman_time_stm':spearman([a for a,b in stmp],[b for a,b in stmp]),
                       'spearman_time_tps':spearman([a for a,b in tpsp],[b for a,b in tpsp]),
                       'authority':'DESCRIPTIVE_EXACT_LINK_ONLY'})
    write_csv(out/'bridge_stats.csv',bridge)

    cc=Counter(x['classification'] for x in rows); round_tokens=Counter(str(x.get('round')) for x in wca); events=Counter(str(x.get('event')) for x in wca); legacy_status=Counter(x['legacy_status'] for x in legacy)
    exact=len(exact_rows); repaired=cc['EXACT_ATTEMPT_LINK_REPAIRED_SOLVENUM']
    summary={
        'version':'CUBE-REV 0.10.5-R1.23','title':'Crosswalk Regeneration, Referential-Integrity Repair & Positivity-Qualified Macro–Meso Bridge Rebuild',
        'source':{'recons_sha256':sha256(args.recons),'attempts_sha256':sha256(args.attempts)},
        'n_recons_all':len(recons),'official_census':dict(official_census),'n_wca_classified':len(wca),
        'classification_counts':dict(cc),'exact_link_total':exact,'exact_link_rate':exact/len(wca) if wca else 0,'solveNum_repairs':repaired,
        'round_token_census':dict(round_tokens),'event_census':dict(events),
        'legacy_r_entries':len(legacy),'legacy_r_unique_recon_ids':len({x['recon_id'] for x in legacy}),'legacy_status_counts':dict(legacy_status),
        'operator_findings':[
            'Byte-level full parse corrects the earlier search-count census: 2547 total = 1626 wca + 920 practice + 1 non_wca.',
            'Current source round tokens 1/2/3/f are treated as folded WCA round buckets; each expands only to its official round_type_id family.',
            'A mismatching declared solveNum may be repaired only when the official attempt value is unique within the same explicit competition + person + event + round-bucket candidate set.',
            'Legacy r is audit evidence only. It is never imported as linkage truth, and stale mappings are explicitly downgraded.',
            'Event aliases observed in the pinned snapshot (oh, 3bld, pyra, sq1, clock) are normalized explicitly rather than silently discarded.'
        ],
        'authority':{
            'exact_link':'Explicit compWcaId + personId + normalized event + bounded round bucket plus unique official attempt-value agreement; solveNum repair is admitted only inside that bounded key-space.',
            'positivity':'linkage-support positivity only; it does not identify or correct reconstruction selection from the WCA population.',
            'bridge':'descriptive on regenerated exact links only; no causal or population-prevalence claim.'
        }
    }
    verdict=[]
    verdict.append('PASS_BYTE_TRUTH_CENSUS_CORRECTION_1626' if len(wca)==1626 else 'HOLD_SOURCE_CENSUS_UNEXPECTED')
    verdict.append('PASS_CROSSWALK_REGENERATION_EXPANDS_BEYOND_LEGACY_CACHE' if exact>12 else 'HOLD_CROSSWALK_REGENERATION_DID_NOT_EXPAND')
    if repaired>0: verdict.append('PASS_REFERENTIAL_SOLVENUM_REPAIR_UNDER_UNIQUE_VALUE_GUARD')
    if legacy_status.get('STALE_OR_UNVALIDATED',0)>0 or legacy_status.get('ORPHAN_NOT_IN_CURRENT_WCA_SNAPSHOT',0)>0: verdict.append('PASS_STALE_LEGACY_R_DETECTED_AND_DOWNGRADED')
    verdict.append('PASS_LINKAGE_POSITIVITY_IN_QUALIFIED_STRATA_ONLY' if any(x['linkage_positivity_gate']=='PASS' for x in pos) else 'HOLD_LINKAGE_POSITIVITY_ALL_STRATA')
    verdict += ['NO_LEGACY_R_AS_TRUTH','NO_POPULATION_SELECTION_CORRECTION','NO_CAUSAL_BRIDGE','NO_GENERATION_ADVANCE']
    summary['verdict']=' / '.join(verdict)
    json.dump(summary,open(out/'summary.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

    court=f'''# CUBE-REV 0.10.5-R1.23 Court\n\n**Verdict:** {summary['verdict']}\n\n- Pinned recon snapshot: {len(recons)} rows = {len(wca)} WCA + {official_census.get('practice',0)} practice + {official_census.get('non_wca',0)} non-WCA.\n- Regenerated exact links: {exact} ({exact/len(wca):.3%}); solveNum repaired under unique-value guard: {repaired}.\n- Legacy `r`: {len(legacy)} entries; agreement/stale/orphan = {legacy_status.get('AGREES_WITH_REGENERATED_EXACT',0)}/{legacy_status.get('STALE_OR_UNVALIDATED',0)}/{legacy_status.get('ORPHAN_NOT_IN_CURRENT_WCA_SNAPSHOT',0)}.\n\nThe repaired operator never imports legacy `r` as truth. Round tokens are interpreted as bounded WCA buckets, and attempt-number repair is admitted only when one official attempt value is unique inside the already-bound competition/person/event/round candidate set.\n\n`linkage_positivity.csv` measures support for the linkage operator, not selection of reconstructed solves from the WCA population. Therefore the bridge remains descriptive and positivity-qualified, not population-representative or causal.\n'''
    (out/'COURT.md').write_text(court,encoding='utf-8')
    manifest={}
    for p in sorted(out.iterdir()):
        if p.is_file(): manifest[p.name]={'bytes':p.stat().st_size,'sha256':sha256(p)}
    json.dump(manifest,open(out/'manifest.json','w',encoding='utf-8'),indent=2)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
