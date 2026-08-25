#!/usr/bin/env python3
import argparse, csv, hashlib, json, math, statistics
from collections import Counter, defaultdict
from pathlib import Path

EVENT_MAP = {
    '3x3':'333','2x2':'222','4x4':'444','5x5':'555','6x6':'666','7x7':'777',
    'OH':'333oh','3BLD':'333bf','4BLD':'444bf','5BLD':'555bf','FMC':'333fm',
    'MBLD':'333mbf','Pyraminx':'pyram','Skewb':'skewb','SQ1':'sq1','Megaminx':'minx','Clock':'clock',
}
RAW_ROUNDS = {'0','1','2','3','f','d','e','g','c','b','h'}
LABEL_ROUNDS = {
    'R1':['1','d','0','h'],
    'R2':['2','e','g'],
    'R3':['3'],
    'Fi':['f','c','b'],
}
STANDARD_TIMED = {'333','222','444','555','666','777','333oh','333bf','444bf','555bf','pyram','skewb','sq1','minx','clock'}


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
    if s in RAW_ROUNDS: return [s], 'RAW_WCA_ROUND_TYPE_ID'
    if s in LABEL_ROUNDS: return LABEL_ROUNDS[s], 'LEGACY_BUCKET_LABEL'
    return [], 'UNRESOLVED_TOKEN'

def rankdata(vals):
    order=sorted(range(len(vals)), key=lambda i: vals[i])
    ranks=[0.0]*len(vals); i=0
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
    return pearson(rankdata(x), rankdata(y)) if len(x)>=3 else None

def med(xs):
    return statistics.median(xs) if xs else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--recons', required=True); ap.add_argument('--attempts', required=True); ap.add_argument('--out', required=True)
    args=ap.parse_args(); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    recons=json.load(open(args.recons,encoding='utf-8'))
    attempts=json.load(open(args.attempts,encoding='utf-8'))
    wca=[r for r in recons if r.get('official')=='wca']
    byid={str(r.get('id')):r for r in wca if r.get('id') is not None}

    rows=[]
    for r in wca:
        rid=str(r.get('id'))
        event_raw=r.get('event'); eid=EVENT_MAP.get(event_raw)
        rounds,round_basis=norm_round(r.get('round'))
        solve=r.get('solveNum')
        try: solve_i=int(solve)
        except Exception: solve_i=None
        comp=r.get('compWcaId'); person=r.get('personId')
        exp=expected_attempt(eid,r.get('rawTime')) if eid else None
        structural=[]; time_matches=[]; candidates=[]
        if comp and person and eid and rounds and solve_i and solve_i>0:
            pdata=attempts.get(str(comp),{}).get(str(person),{})
            for rt in rounds:
                key=f'{eid}_{rt}'
                ent=pdata.get(key)
                if not ent or not isinstance(ent.get('a'),list): continue
                a=ent['a']
                if solve_i>len(a): continue
                val=a[solve_i-1]
                c={'key':key,'round_type_id':rt,'attempt_value':val}
                candidates.append(c); structural.append(c)
                if exp is not None and val==exp: time_matches.append(c)
        if not comp or not person or solve_i is None:
            cls='SOURCE_METADATA_INSUFFICIENT'
        elif eid is None:
            cls='EVENT_UNSUPPORTED'
        elif not rounds:
            cls='ROUND_TOKEN_UNRESOLVED'
        elif not structural:
            cls='NO_SIDECAR_ATTEMPT_ENTRY'
        elif len(time_matches)==1:
            cls='EXACT_ATTEMPT_LINK_TIME_VALIDATED'
        elif len(time_matches)>1:
            cls='VALUE_COLLISION_ROUND_AMBIGUOUS'
        elif len(structural)==1 and exp is None:
            cls='STRUCTURAL_UNIQUE_UNVALIDATED'
        elif len(structural)==1:
            cls='STRUCTURAL_LINK_TIME_MISMATCH'
        else:
            cls='ROUND_AMBIGUOUS_NO_VALUE_RESOLUTION'
        exact=time_matches[0] if len(time_matches)==1 else None
        rows.append({
            'recon_id':rid,'event':event_raw,'event_id':eid,'date':r.get('date'),'year':str(r.get('date',''))[:4],
            'comp':r.get('comp'),'compWcaId':comp,'person':r.get('person'),'personId':person,
            'reconer':r.get('reconer'),'reconerId':r.get('reconerId'),'method':r.get('method'),
            'round_raw':r.get('round'),'round_basis':round_basis,'round_candidates':'|'.join(rounds),'solveNum':solve_i,
            'rawTime':r.get('rawTime'),'expected_attempt_value':exp,'classification':cls,
            'structural_candidate_count':len(structural),'time_match_count':len(time_matches),
            'structural_keys':'|'.join(c['key'] for c in structural),
            'candidate_attempt_values':'|'.join(str(c['attempt_value']) for c in structural),
            'exact_key':exact['key'] if exact else '', 'official_attempt_value':exact['attempt_value'] if exact else '',
            'stm':r.get('stm'),'tps':r.get('tps'),'completionStatus':r.get('completionStatus')
        })

    # legacy r cache audit
    legacy=[]
    for comp,ppl in attempts.items():
        for person,pdata in ppl.items():
            for key,ent in pdata.items():
                rr=ent.get('r') or {}
                for sn,rid in rr.items():
                    rid=str(rid); cur=next((x for x in rows if x['recon_id']==rid),None)
                    legacy.append({'compWcaId':comp,'personId':person,'key':key,'solveNum':sn,'recon_id':rid,
                                   'present_in_current_wca_snapshot':rid in byid,
                                   'regenerated_classification':cur['classification'] if cur else 'ORPHAN_NOT_IN_CURRENT_WCA_SNAPSHOT',
                                   'regenerated_exact_key':cur['exact_key'] if cur else '',
                                   'legacy_status':('AGREES_WITH_REGENERATED_EXACT' if cur and cur['classification']=='EXACT_ATTEMPT_LINK_TIME_VALIDATED' and cur['exact_key']==key else 'STALE_OR_UNVALIDATED')})

    def write_csv(name, data):
        p=out/name
        keys=list(data[0].keys()) if data else []
        with open(p,'w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(data)
        return p
    write_csv('crosswalk.csv',rows); write_csv('legacy_r_audit.csv',legacy)

    # linkage-support positivity: descriptive support only; not population-selection positivity
    pos=[]
    groupings=[('event',lambda x:(x['event'],)),('event_year',lambda x:(x['event'],x['year'])),('round',lambda x:(x['event'],x['round_raw']))]
    for level,fn in groupings:
        groups=defaultdict(list)
        for x in rows: groups[fn(x)].append(x)
        for k,g in sorted(groups.items(),key=lambda z:str(z[0])):
            ex=[x for x in g if x['classification']=='EXACT_ATTEMPT_LINK_TIME_VALIDATED']
            comps={x['compWcaId'] for x in ex if x['compWcaId']}; persons={x['personId'] for x in ex if x['personId']}
            qualified=len(g)>=5 and len(ex)>=3 and len(comps)>=2 and len(persons)>=2
            pos.append({'level':level,'stratum':'|'.join('' if q is None else str(q) for q in k),'n_recons':len(g),'n_exact':len(ex),
                        'exact_link_rate':len(ex)/len(g) if g else None,'n_exact_competitions':len(comps),'n_exact_persons':len(persons),
                        'linkage_positivity_gate':'PASS' if qualified else 'HOLD'})
    write_csv('linkage_positivity.csv',pos)

    # bridge statistics on admitted exact links only
    bridge=[]
    for ev,g0 in sorted(defaultdict(list, {e:[x for x in rows if x['event']==e and x['classification']=='EXACT_ATTEMPT_LINK_TIME_VALIDATED'] for e in sorted({x['event'] for x in rows})}).items()):
        g=[x for x in g0 if fnum(x['rawTime']) is not None]
        times=[fnum(x['rawTime']) for x in g]
        stmp=[(fnum(x['rawTime']),fnum(x['stm'])) for x in g if fnum(x['stm']) is not None]
        tpsp=[(fnum(x['rawTime']),fnum(x['tps'])) for x in g if fnum(x['tps']) is not None]
        bridge.append({'event':ev,'n_exact':len(g),'median_time_s':med(times),
                       'median_stm':med([b for a,b in stmp]),'median_tps':med([b for a,b in tpsp]),
                       'spearman_time_stm':spearman([a for a,b in stmp],[b for a,b in stmp]),
                       'spearman_time_tps':spearman([a for a,b in tpsp],[b for a,b in tpsp]),
                       'authority':'DESCRIPTIVE_EXACT_LINK_ONLY'})
    write_csv('bridge_stats.csv',bridge)

    cc=Counter(x['classification'] for x in rows)
    round_tokens=Counter(str(x.get('round')) for x in wca)
    events=Counter(str(x.get('event')) for x in wca)
    legacy_status=Counter(x['legacy_status'] for x in legacy)
    exact=cc['EXACT_ATTEMPT_LINK_TIME_VALIDATED']
    summary={
        'version':'CUBE-REV 0.10.5-R1.23',
        'title':'Crosswalk Regeneration, Referential-Integrity Repair & Positivity-Qualified Macro–Meso Bridge Rebuild',
        'source':{'recons_sha256':sha256(args.recons),'attempts_sha256':sha256(args.attempts)},
        'n_recons_all':len(recons),'n_wca_classified':len(wca),'classification_counts':dict(cc),
        'exact_link_rate': exact/len(wca) if wca else 0,
        'round_token_census':dict(round_tokens),'event_census':dict(events),
        'legacy_r_entries':len(legacy),'legacy_r_unique_recon_ids':len({x['recon_id'] for x in legacy}),
        'legacy_status_counts':dict(legacy_status),
        'operator_findings':[
            'Current snapshot stores raw WCA round_type_id tokens for most WCA reconstructions; legacy builder expects R1/R2/R3/Fi labels.',
            'Legacy builder preserves old r mappings because it starts from existing JSON and does not delete r when current recon_index no longer contains the key.',
            'Regeneration treats legacy r as audit evidence, never as authoritative input.',
            '4x4 is admitted through explicit 4x4->444 mapping in the repaired research operator; this is broader than the legacy builder EVENT_MAP.'
        ],
        'authority':{
            'exact_link':'Requires explicit compWcaId + personId + event + round + solveNum plus exact official-attempt value agreement when value encoding is supported.',
            'positivity':'linkage-support positivity only; does not identify or correct selection of reconstructed solves from the WCA population.',
            'bridge':'descriptive on regenerated exact links only; no causal or population-prevalence claim.'
        }
    }
    json.dump(summary,open(out/'summary.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

    verdict=[]
    if exact>12: verdict.append('PASS_CROSSWALK_REGENERATION_EXPANDS_BEYOND_LEGACY_CACHE')
    else: verdict.append('HOLD_CROSSWALK_REGENERATION_DID_NOT_EXPAND')
    if legacy_status.get('STALE_OR_UNVALIDATED',0)>0: verdict.append('PASS_STALE_LEGACY_R_DETECTED_AND_DOWNGRADED')
    if any(x['linkage_positivity_gate']=='PASS' for x in pos): verdict.append('PASS_LINKAGE_POSITIVITY_IN_QUALIFIED_STRATA_ONLY')
    else: verdict.append('HOLD_LINKAGE_POSITIVITY_ALL_STRATA')
    verdict += ['NO_LEGACY_R_AS_TRUTH','NO_POPULATION_SELECTION_CORRECTION','NO_CAUSAL_BRIDGE','NO_GENERATION_ADVANCE']
    summary['verdict']=' / '.join(verdict)
    json.dump(summary,open(out/'summary.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

    court=f'''# CUBE-REV 0.10.5-R1.23 Court\n\n**Verdict:** {summary['verdict']}\n\n- WCA-classified reconstructions: {len(wca)}\n- Regenerated exact, time-validated links: {exact} ({exact/len(wca):.3%})\n- Legacy `r` entries: {len(legacy)}; unique recon ids: {summary['legacy_r_unique_recon_ids']}\n- Legacy stale/unvalidated entries: {legacy_status.get('STALE_OR_UNVALIDATED',0)}\n\nThe repaired operator never imports legacy `r` as truth. It regenerates linkage from the current reconstruction snapshot and the pinned official-attempt sidecar, then uses value agreement as an independent validation plane where the WCA result encoding is directly comparable.\n\n`linkage_positivity.csv` is a support diagnostic, not a population-selection correction. A PASS means only that a reconstruction stratum has nontrivial exact-link support across at least two competitions and two persons under the fixed minimum cell rule.\n'''
    (out/'COURT.md').write_text(court,encoding='utf-8')

    manifest={}
    for p in sorted(out.iterdir()):
        if p.is_file(): manifest[p.name]={'bytes':p.stat().st_size,'sha256':sha256(p)}
    json.dump(manifest,open(out/'manifest.json','w',encoding='utf-8'),indent=2)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
