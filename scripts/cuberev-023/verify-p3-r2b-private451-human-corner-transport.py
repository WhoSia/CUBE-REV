#!/usr/bin/env python3
"""CUBE-REV P3-R2B: PRIVATE archival human reconstruction reanalysis.

Usage: python scripts/cuberev-023/verify-p3-r2b-private451-human-corner-transport.py PATH_TO_PRIVATE_ZIP
Requires an explicitly authorized local original ZIP. No network, individual records,
participant names, scramble paths, source IDs, or source-level rows are ever output.
Historical P4 reused for provenance, but these exact-CP/CO analyses are NEW and
EXPLORATORY, never prospectively held out or causal.
"""
import sys,zipfile,json,hashlib,collections
SHA='fb88827cce327d0021a0741e47dfa09670651083b8baaaa46cccc9051d73568e'
I=((1,0,0),(0,1,0),(0,0,1))
X=((1,0,0),(0,0,-1),(0,1,0))
Y=((0,0,1),(0,1,0),(-1,0,0))
Z=((0,-1,0),(1,0,0),(0,0,1))

def mul(a,b):
 return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)) for i in range(3))

def phasekey(r,i):
 c,f,s,h=r['corner'],r['frame'],r['stage'],r['previous']
 return [(c,),(c,f),(c,f,s),(c,f,s,h[-1:]),(c,f,s,h)][i]

def court(rows,i):
 grouped=collections.defaultdict(list)
 for r in rows:grouped[phasekey(r,i)].append(r)
 pairs=collections.Counter(); keys=0; both=[]
 for group in grouped.values():
  if len(group)<2:continue
  local=collections.Counter()
  for j,a in enumerate(group):
   for b in group[j+1:]:
    if a['source']==b['source']:continue
    cat='same' if a['whole']==b['whole'] else 'different'
    local[cat+'_pairs']+=1
    local[cat+'_disagree']+=a['next']!=b['next']
  if local['same_pairs'] or local['different_pairs']:keys+=1
  pairs.update(local)
  if local['same_pairs'] and local['different_pairs']:
   both.append((local['same_disagree']/local['same_pairs'],local['different_disagree']/local['different_pairs']))
 n=len(both)
 return {'level':['corner','corner_frame','corner_frame_prior_stage','corner_frame_prior_stage_last1','corner_frame_prior_stage_last3'][i],
  'cross_source_keys':keys,'matched_keys_support_both':n,
  'same_full_pairs':pairs['same_pairs'],'different_full_pairs':pairs['different_pairs'],
  'same_full_next_action_disagreements':pairs['same_disagree'],
  'different_full_next_action_disagreements':pairs['different_disagree'],
  'common_key_balanced_delta_different_minus_same':sum(b-a for a,b in both)/n if n else None,
  'full_key_matched_support_positive':n>0}

def run(path):
 with open(path,'rb') as fp: digest=hashlib.sha256(fp.read()).hexdigest()
 assert digest==SHA,'STOP: original ZIP digest mismatch'
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  assert set(z.namelist())=={'MANIFEST.json','exact-trajectories.json','prefix-states.jsonl'}
  m=json.loads(z.read('MANIFEST.json'));data=json.loads(z.read('exact-trajectories.json'))
 assert len(data['records'])==452 and m['distinct_source_ids']==452
 byid={r['source_id']:r for r in data['records']}
 assert byid[2778]['scramble_raw']==byid[2970]['scramble_raw']
 assert [(x['raw'],x['kind']) for x in byid[2778]['prefixes']]==[(x['raw'],x['kind']) for x in byid[2970]['prefixes']]
 assert byid[2778]['prefixes'][-1]['cubie']==byid[2970]['prefixes'][-1]['cubie']
 unique=[r for r in data['records'] if r['source_id']!=2970];assert len(unique)==451
 orientations={I};q=[I]
 for base in q:
  for rotation in (X,Y,Z):
   p=mul(base,rotation)
   if p not in orientations:orientations.add(p);q.append(p)
 assert len(orientations)==24
 events=[]; kinds=collections.Counter()
 for r in unique:
  cubie=r['start_cubie'];frame=I;stage=None;prior=[]
  for p in r['prefixes']:
   corner=tuple(cubie['cp']+cubie['co']);whole=corner+tuple(cubie['ep']+cubie['eo'])
   action=p['raw'].replace("2'",'2')
   events.append({'source':r['source_id'],'corner':corner,'whole':whole,'frame':frame,
                  'stage':stage,'previous':tuple(prior[-3:]),'next':action,'kind':p['kind']})
   kinds[p['kind']]+=1
   if p['kind']=='ROTATION' and p['raw'] and p['raw'][0].lower() in 'xyz':
    m={'x':X,'y':Y,'z':Z}[p['raw'][0].lower()]
    power=2 if '2' in p['raw'] else 3 if "'" in p['raw'] else 1
    for _ in range(power):frame=mul(frame,m)
   if p['boundary_after'] and p['annotation_after']:stage=p['annotation_after']
   prior.append(action);cubie=p['cubie']
 assert len(events)==25272
 assert dict(kinds)=={'ROTATION':1396,'FACE_TURN':21118,'WIDE_TURN':1424,'SLICE_TURN':1334}
 all_actions=[court(events,i) for i in range(5)]
 face=[e for e in events if e['kind']=='FACE_TURN']
 face_only=[court(face,i) for i in range(5)]
 assert [x['matched_keys_support_both'] for x in all_actions]==[181,120,43,9,0]
 assert [x['matched_keys_support_both'] for x in face_only]==[164,73,15,1,0]
 assert all_actions[-1]['common_key_balanced_delta_different_minus_same'] is None
 return {'marker':'CUBE_REV_023_P3_R2B_SOURCE_GRADED_PRIVATE_451_CORNER_SUPPORT_COURT',
  'private_archive_sha256':SHA,'original_sources':452,'deduplicated_complete_solve_reconstructions':451,
  'source_duplicate_bytewise_selected_fields_verified':True,'next_action_rows':len(events),
  'action_kind_counts':dict(kinds),'rotation_frame_right_composition_states':24,
  'rotation_is_explicit_annotated_token_proxy_NOT_observed_human_viewpoint':True,
  'cognitive_phase_prior_stage_is_retrospective_annotation_NOT_measured_contemporaneous':True,
  'exact_corner_cpco_vs_full_cpco_epeo_action_support_all_types':all_actions,
  'face_turn_only_sensitivity':face_only,
  'privacy':'AGGREGATES ONLY; DO NOT PUBLISH ARCHIVE OR PERSON/SOURCE RECORDS',
  'independent_heldout_sample':False,'human_neural_causal_mechanism_identified':False,
  'transport_to_P3R1_full_nine_sticker_face_oracle':False,
  'last_three_actions_common_key_matched_contrast_not_identifiable':True}
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Provide path to privately retained original ZIP')
 print(json.dumps(run(sys.argv[1]),ensure_ascii=False,indent=2))
