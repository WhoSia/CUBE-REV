#!/usr/bin/env python3
import json,re,os
from collections import Counter,defaultdict
from pathlib import Path

SRC=Path('research/0.10.5-r1.7/evidence-grammar/DETAIL_GRAMMAR_PROBE.json')
OUT=Path(os.environ.get('R17_OUT','research/0.10.5-r1.7/evidence-phase-taxonomy'))
OUT.mkdir(parents=True,exist_ok=True)
x=json.loads(SRC.read_text(encoding='utf-8'))

PAT={
 'INSPECTION':[r'\binspection\b'],
 'CROSS':[r'\b(?:cross|xcross|xxcross|xxxcross)\b',r'\bpseudo\s+cross\b',r'\bmissed\s+cross\b'],
 'F2L':[r'\bf2l\b',r'\b(?:1st|2nd|3rd|4th|first|second|third|fourth)\s*(?:/\s*)?pair',r'\bpairs?\b',r'\bzbls\b',r'\bsvls\b'],
 'LL_ORIENT':[r'\boll(?:\b|cp)',r'\beoll\b',r'\bcoll\b',r'\bollcp\b'],
 'LL_PERMUTE':[r'\bpll\b',r'\bepll\b',r'\bauf\b'],
 'LL_ONELOOK':[r'\bzbll\b',r'\b2gll\b',r'\bell\b',r'\bcll\b'],
 'ROUX_FB':[r'\bfb\b',r'\bfbdr\b',r'\bpseudo\s+fb\b'],
 'ROUX_SB':[r'\bsb\b',r'\bss\b',r'\bsp\b',r'\bflipped\s+sp\b'],
 'ROUX_CMLL':[r'\bcmll\b'],
 'ROUX_LSE':[r'\blse\b',r'\beolr\b',r'\beolrb\b',r'\bep\b'],
}
PAT={k:[re.compile(p,re.I) for p in ps] for k,ps in PAT.items()}

def classify(method,comment):
    c=' '.join(str(comment or '').lower().split())
    if not c:return 'EMPTY',[]
    hits=[]
    for phase,ps in PAT.items():
        if any(p.search(c) for p in ps): hits.append(phase)
    # Method-gate Roux abbreviations; remove likely accidental collisions outside Roux.
    if method!='Roux': hits=[h for h in hits if not h.startswith('ROUX_')]
    if method=='Roux':
        # Generic CLL on a Roux record is closer to CMLL-family but keep CLL itself uncertain.
        if 'LL_ONELOOK' in hits and re.search(r'\bcll\b',c) and 'ROUX_CMLL' not in hits:
            hits.remove('LL_ONELOOK'); hits.append('ROUX_CMLL')
        # Generic CFOP labels can occur in hybrids; retain them only if explicitly spelled.
    hits=list(dict.fromkeys(hits))
    if len(hits)==0:return 'UNKNOWN',[]
    if len(hits)>1:return 'AMBIGUOUS',hits
    return hits[0],hits

ORDER={
 'CFOP':{'INSPECTION':0,'CROSS':1,'F2L':2,'LL_ORIENT':3,'LL_ONELOOK':3,'LL_PERMUTE':4},
 'ZB':{'INSPECTION':0,'CROSS':1,'F2L':2,'LL_ORIENT':3,'LL_ONELOOK':3,'LL_PERMUTE':4},
 'CF':{'INSPECTION':0,'CROSS':1,'F2L':2,'LL_ORIENT':3,'LL_ONELOOK':3,'LL_PERMUTE':4},
 'Roux':{'INSPECTION':0,'ROUX_FB':1,'ROUX_SB':2,'ROUX_CMLL':3,'ROUX_LSE':4},
}
records=[]; phase_counts=Counter(); raw_unknown=Counter(); ambiguous=Counter(); method_stats=defaultdict(Counter)
for r in x['records']:
    method=r.get('method') or 'UNKNOWN'; seq=[]; line_out=[]
    for c in r.get('comments',[]):
        phase,hits=classify(method,c); line_out.append({'comment':c,'phase':phase,'hits':hits}); phase_counts[phase]+=1; method_stats[method][phase]+=1
        if phase=='UNKNOWN':raw_unknown[c]+=1
        if phase=='AMBIGUOUS':ambiguous[c]+=1
        if phase not in ('EMPTY','UNKNOWN','AMBIGUOUS','INSPECTION'):seq.append(phase)
    ordmap=ORDER.get(method,{})
    vals=[ordmap[p] for p in seq if p in ordmap]
    regress=sum(1 for a,b in zip(vals,vals[1:]) if b<a)
    classified=sum(1 for z in line_out if z['phase'] not in ('EMPTY','UNKNOWN','AMBIGUOUS'))
    post=[z for z in line_out if z['phase']!='INSPECTION']
    post_class=sum(1 for z in post if z['phase'] not in ('EMPTY','UNKNOWN','AMBIGUOUS'))
    records.append({'reco_id':r['reco_id'],'method':method,'lines':line_out,'phase_sequence':seq,'ordinal_regressions':regress,
                    'post_inspection_lines':len(post),'post_inspection_classified':post_class,'fully_classified_post_inspection':bool(post) and post_class==len(post)})

nlines=sum(r['post_inspection_lines'] for r in records); nclass=sum(r['post_inspection_classified'] for r in records)
out={
 'schema_version':'CR0105R17-PHASE-TAXONOMY-1','status':'PASS' if nlines and nclass/nlines>=0.85 else 'HOLD',
 'source_probe_records':len(records),'post_inspection_lines':nlines,'post_inspection_classified':nclass,
 'post_inspection_classification_rate':nclass/nlines if nlines else 0,
 'records_fully_classified_post_inspection':sum(r['fully_classified_post_inspection'] for r in records),
 'records_with_annotation_order_regression':sum(r['ordinal_regressions']>0 for r in records),
 'phase_counts':dict(phase_counts),'method_phase_counts':{m:dict(c) for m,c in method_stats.items()},
 'top_unknown_comments':raw_unknown.most_common(50),'top_ambiguous_comments':ambiguous.most_common(50),
 'taxonomy_rule':'Method-aware comment labels provide phase annotations; ambiguous/multi-phase comments are not force-classified. Annotation labels require independent cube-state replay before use in counterfactual phenotype claims.',
 'records':records,'human_observations':0
}
(OUT/'PHASE_TAXONOMY_COURT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','source_probe_records','post_inspection_classification_rate','records_fully_classified_post_inspection','records_with_annotation_order_regression','phase_counts','top_unknown_comments','top_ambiguous_comments']},indent=2,ensure_ascii=False))
if out['status']!='PASS':raise SystemExit(2)
