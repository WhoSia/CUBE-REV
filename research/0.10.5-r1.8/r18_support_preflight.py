#!/usr/bin/env python3
import csv, hashlib, json, math, os, re, unicodedata
from collections import defaultdict, Counter
from pathlib import Path

import duckdb
import requests
from bs4 import BeautifulSoup

DB = Path(os.environ['R18_PARENT_DB'])
OUT = Path(os.environ.get('R18_ROOT', '/tmp/r18'))
OUT.mkdir(parents=True, exist_ok=True)
R17_MANIFEST = Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json')
HOLDOUT_N = 900
MIN_FRESH_MODERN_LINKED = 80
UA = 'CUBE-REV/0.10.5-R1.8 prospective-support preflight; low-rate public reconstruction audit'


def stable_hash(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def speed(v: int) -> str:
    if v < 500: return '<5'
    if v < 700: return '5-7'
    return '7-10'

def era(y: int) -> str:
    if y <= 2012: return '<=2012'
    if y <= 2016: return '2013-16'
    if y <= 2019: return '2017-19'
    if y <= 2022: return '2020-22'
    return '2023-26'

def norm(s):
    s = unicodedata.normalize('NFKD', str(s or ''))
    s = ''.join(c for c in s if not unicodedata.combining(c)).casefold()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' '.join(s.split())

def cs_from_result(s):
    s = str(s or '').strip()
    if not s or s.upper() in {'DNF', 'DNS'}: return None
    s = s.replace('+', '').strip()
    try:
        if ':' in s:
            m, x = s.split(':', 1)
            return int(round((int(m) * 60 + float(x)) * 100))
        return int(round(float(s) * 100))
    except Exception:
        return None

def extract_reco_rows(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table')
    if not table:
        raise RuntimeError('R18_RECO_TABLE_NOT_FOUND')
    out = []
    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        if len(td) < 11: continue
        vals = [' '.join(x.stripped_strings) for x in td]
        try: rid = int(vals[0])
        except Exception: continue
        if vals[1].strip() != '3x3': continue
        href = None
        for a in tr.find_all('a', href=True):
            if re.search(r'/solve/\d+', a['href']):
                href = a['href']; break
        out.append({
            'reco_id': rid,
            'puzzle': vals[1].strip(),
            'result_text': vals[2].strip(),
            'solver': vals[3].strip(),
            'method': vals[4].strip(),
            'date': vals[5].strip(),
            'competition': vals[6].strip(),
            'tags': vals[7].strip(),
            'movecount': vals[8].strip(),
            'tps': vals[9].strip(),
            'reconstructor': vals[10].strip(),
            'url': ('https://reco.nz' + href if href and href.startswith('/') else href or f'https://reco.nz/solve/{rid}')
        })
    return out


def allocate_proportional(target, pools, total_n):
    keys = [k for k in sorted(target) if target[k] >= 100 and len(pools.get(k, [])) >= 5]
    pop = sum(target[k] for k in keys)
    exact = {k: total_n * target[k] / pop for k in keys} if pop else {}
    alloc = {k: min(len(pools[k]), int(math.floor(exact[k]))) for k in keys}
    remaining = total_n - sum(alloc.values())
    while remaining > 0:
        eligible = [k for k in keys if alloc[k] < len(pools[k])]
        if not eligible: break
        k = max(eligible, key=lambda z: (exact[z] - alloc[z], target[z], z))
        alloc[k] += 1
        remaining -= 1
    return keys, pop, alloc

con = duckdb.connect(str(DB), read_only=True)
parent_db_sha = os.environ.get('R18_PARENT_DB_SHA256', '')

# --- R1.7 exact used-attempt set; membership only, no outcome fields are used. ---
r17 = json.loads(R17_MANIFEST.read_text(encoding='utf-8'))
r17_records = r17['records']
r17_used = {(int(r['result_id']), int(r['attempt_number'])) for r in r17_records}
if len(r17_used) != 900:
    raise RuntimeError(f'R18_R17_USED_KEY_COUNT_{len(r17_used)}')

# --- Canonical frozen linked under-10 universe, identical lineage to R1.7. ---
raw = con.execute("""
select r.reco_id,r.method,r.url,c.result_id,c.attempt_number,c.attempt_value,
       s.comp_year,s.competition_id,s.round_type_id,s.person_id,s.person_name,l.tier
from reco_index r join linkage_class l using(reco_id)
join linkage_candidates c using(reco_id)
join attempt_spine s on s.result_id=c.result_id and s.attempt_number=c.attempt_number
where l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE') and c.attempt_value>0 and c.attempt_value<1000
order by c.result_id,c.attempt_number,r.reco_id
""").fetchall()
cols = ['reco_id','method','url','result_id','attempt_number','attempt_value','comp_year','competition_id','round_type_id','person_id','person_name','tier']
by_attempt = defaultdict(list)
for z in raw:
    rr = dict(zip(cols, z))
    by_attempt[(int(rr['result_id']), int(rr['attempt_number']))].append(rr)
canonical = []
for key, rs in by_attempt.items():
    rs.sort(key=lambda r: stable_hash(f"{r['result_id']}:{r['attempt_number']}:{r['reco_id']}"))
    rr = rs[0]
    rr['duplicate_reconstruction_count'] = len(rs)
    rr['speed'] = speed(int(rr['attempt_value']))
    rr['era'] = era(int(rr['comp_year']))
    rr['cell'] = f"{rr['speed']}|{rr['era']}"
    canonical.append(rr)

# WCA target cells.
target_rows = con.execute("""
select case when attempt_value<500 then '<5' when attempt_value<700 then '5-7' else '7-10' end speed,
       case when comp_year<=2012 then '<=2012' when comp_year<=2016 then '2013-16' when comp_year<=2019 then '2017-19' when comp_year<=2022 then '2020-22' else '2023-26' end era,
       count(*) n
from phenotype_attempts where attempt_value>0 and attempt_value<1000
group by 1,2 order by 1,2
""").fetchall()
target = {(s,e): int(n) for s,e,n in target_rows}
target_total = sum(target.values())

all_pools = defaultdict(list)
remaining_pools = defaultdict(list)
used_by_cell = Counter()
for rr in canonical:
    k = (rr['speed'], rr['era'])
    all_pools[k].append(rr)
    key = (int(rr['result_id']), int(rr['attempt_number']))
    if key in r17_used:
        used_by_cell[k] += 1
    else:
        remaining_pools[k].append(rr)
for d in (all_pools, remaining_pools):
    for k in d:
        d[k].sort(key=lambda r: stable_hash(f"R18HOLDOUT:{r['result_id']}:{r['attempt_number']}"))

supported_keys, supported_pop, alloc = allocate_proportional(target, remaining_pools, HOLDOUT_N)
full_target_coverage = supported_pop / max(1, target_total)
allocated_n = sum(alloc.values())
selected = []
for k, n in alloc.items():
    selected.extend(remaining_pools[k][:n])
selected.sort(key=lambda r: stable_hash(f"R18ORDER:{r['result_id']}:{r['attempt_number']}"))
selected_keys = {(int(r['result_id']), int(r['attempt_number'])) for r in selected}
overlap = selected_keys & r17_used
if overlap:
    raise RuntimeError(f'R18_HOLDOUT_OVERLAP_{len(overlap)}')

holdout_manifest = {
    'schema_version': 'CR0105R18-HOLDOUT-A-MEMBERSHIP-1',
    'status': 'PASS_MEMBERSHIP_FROZEN' if allocated_n == HOLDOUT_N and not overlap else 'HOLD_MEMBERSHIP',
    'source': 'frozen R1.6 analytical DB; R1.7 used-attempt exclusion',
    'selection_salt': 'R18HOLDOUT / R18ORDER',
    'desired_n': HOLDOUT_N,
    'selected_n': allocated_n,
    'r17_used_attempt_keys_n': len(r17_used),
    'overlap_with_r17_n': len(overlap),
    'original_under10_target_population_n': target_total,
    'untouched_supported_target_population_n': supported_pop,
    'untouched_supported_target_fraction': full_target_coverage,
    'standardized_full_under10_gate': 'PASS' if full_target_coverage >= 0.90 else 'HOLD_TARGET_COVERAGE_LT_0_90',
    'records': selected,
    'human_observations': 0
}
(OUT/'HOLDOUT_A_MEMBERSHIP.json').write_text(json.dumps(holdout_manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

cell_rows = []
for k in sorted(target):
    cell_rows.append({
        'speed': k[0], 'era': k[1], 'population_n': target[k],
        'linked_total_n': len(all_pools.get(k, [])),
        'used_r17_n': used_by_cell[k],
        'untouched_linked_n': len(remaining_pools.get(k, [])),
        'untouched_supported': k in supported_keys,
        'holdout_A_n': alloc.get(k, 0)
    })

# --- Fresh reco.nz vintage: new reconstruction IDs only, then deterministic R1.6-style linkage. ---
sess = requests.Session(); sess.headers['User-Agent'] = UA
resp = sess.get('https://reco.nz/solve/', timeout=60); resp.raise_for_status()
live_rows = extract_reco_rows(resp.text)
frozen_ids = {int(x[0]) for x in con.execute('select reco_id from reco_index').fetchall()}
frozen_count = len(frozen_ids)
frozen_max = max(frozen_ids) if frozen_ids else None
new_rows = [r for r in live_rows if int(r['reco_id']) not in frozen_ids]

fresh_linked = []
fresh_tiers = Counter()
for r in new_rows:
    cs = cs_from_result(r['result_text'])
    if cs is not None and '[+2]' in str(r.get('tags','')):
        cs += 200
    if cs is None:
        fresh_tiers['U_UNMATCHED'] += 1
        continue
    sn, cn = norm(r['solver']), norm(r['competition'])
    cands = con.execute("""
        select s.result_id,s.attempt_number,s.attempt_value,s.comp_year,s.person_name,s.competition_name
        from attempt_spine s
        join person_norm_map pn on s.person_name=pn.person_name
        join competition_norm_map cnm on s.competition_name=cnm.competition_name
        where pn.solver_norm=? and cnm.competition_norm=? and s.attempt_value=?
    """, [sn, cn, int(cs)]).fetchall()
    exact = [x for x in cands if x[4] == r['solver'] and x[5] == r['competition']]
    if len(cands) == 1 and len(exact) == 1: tier = 'A_EXACT_UNIQUE'
    elif len(cands) == 1: tier = 'B_NORMALIZED_UNIQUE'
    elif len(cands) > 1: tier = 'C_AMBIGUOUS'
    else: tier = 'U_UNMATCHED'
    fresh_tiers[tier] += 1
    if tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE'):
        x = cands[0]
        z = {**r, 'tier': tier, 'result_id': int(x[0]), 'attempt_number': int(x[1]),
             'attempt_value': int(x[2]), 'comp_year': int(x[3])}
        z['speed'] = speed(z['attempt_value']); z['era'] = era(z['comp_year']); z['cell'] = f"{z['speed']}|{z['era']}"
        z['attempt_seen_in_r17'] = (z['result_id'], z['attempt_number']) in r17_used
        fresh_linked.append(z)

# One fresh reconstruction per unique official attempt by SHA rank.
fresh_by_attempt = defaultdict(list)
for r in fresh_linked:
    fresh_by_attempt[(r['result_id'], r['attempt_number'])].append(r)
fresh_canonical = []
for key, rs in fresh_by_attempt.items():
    rs.sort(key=lambda r: stable_hash(f"R18FRESH:{r['result_id']}:{r['attempt_number']}:{r['reco_id']}"))
    fresh_canonical.append(rs[0])

fresh_untouched = [r for r in fresh_canonical if not r['attempt_seen_in_r17']]
fresh_modern_7_10 = [r for r in fresh_untouched if r['speed']=='7-10' and r['era']=='2023-26']
index_fullness_ok = len(live_rows) >= frozen_count and (frozen_max is None or max([r['reco_id'] for r in live_rows], default=-1) >= frozen_max)
modern_gate = 'PASS_FRESH_MODERN_LINKED_GE_80' if index_fullness_ok and len(fresh_modern_7_10) >= MIN_FRESH_MODERN_LINKED else 'HOLD_FRESH_MODERN_CELL'

fresh = {
    'schema_version': 'CR0105R18-FRESH-RECO-PREFLIGHT-1',
    'status': 'PASS_CHARACTERIZED' if index_fullness_ok else 'HOLD_LIVE_INDEX_NOT_FULL_RELATIVE_TO_FROZEN',
    'retrieved_url': 'https://reco.nz/solve/',
    'http_status': resp.status_code,
    'html_bytes': len(resp.content),
    'html_sha256': hashlib.sha256(resp.content).hexdigest(),
    'live_3x3_rows': len(live_rows),
    'live_max_reco_id': max([r['reco_id'] for r in live_rows], default=None),
    'frozen_3x3_rows': frozen_count,
    'frozen_max_reco_id': frozen_max,
    'new_reco_id_rows': len(new_rows),
    'new_linkage_tiers': dict(fresh_tiers),
    'new_unique_linked_attempts': len(fresh_canonical),
    'new_unique_linked_attempts_untouched_by_r17': len(fresh_untouched),
    'fresh_modern_2023_26_7_10_untouched_n': len(fresh_modern_7_10),
    'fresh_modern_gate_min_n': MIN_FRESH_MODERN_LINKED,
    'fresh_modern_gate': modern_gate,
    'fresh_modern_records': fresh_modern_7_10,
    'human_observations': 0
}
(OUT/'FRESH_RECO_VINTAGE_PREFLIGHT.json').write_text(json.dumps(fresh, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

preflight = {
    'schema_version': 'CR0105R18-SUPPORT-PREFLIGHT-1',
    'status': 'PASS_CHARACTERIZED_WITH_BLOCKING_GATES_REPORTED',
    'parent_db_sha256': parent_db_sha,
    'r17_sample_manifest_sha256': hashlib.sha256(R17_MANIFEST.read_bytes()).hexdigest(),
    'canonical_linked_under10_attempts': len(canonical),
    'r17_used_attempts': len(r17_used),
    'untouched_linked_attempts': sum(len(v) for v in remaining_pools.values()),
    'target_population_under10': target_total,
    'untouched_supported_population': supported_pop,
    'untouched_supported_population_fraction': full_target_coverage,
    'holdout_A_selected_n': allocated_n,
    'holdout_A_overlap_n': len(overlap),
    'holdout_A_full_target_standardization_gate': holdout_manifest['standardized_full_under10_gate'],
    'fresh_modern_gate': modern_gate,
    'cell_support': cell_rows,
    'decision': {
        'attempt_disjoint_holdout_A': 'GO' if allocated_n == HOLDOUT_N and not overlap else 'HOLD',
        'full_under10_standardized_holdout_claim': 'GO' if full_target_coverage >= 0.90 else 'HOLD',
        'fresh_modern_7_10_replication': 'GO' if modern_gate.startswith('PASS') else 'HOLD'
    },
    'human_observations': 0,
    'authority': 'RESEARCH_ONLY'
}
(OUT/'SUPPORT_PREFLIGHT.json').write_text(json.dumps(preflight, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

print(json.dumps({
    'status': preflight['status'],
    'canonical_linked_under10_attempts': len(canonical),
    'untouched_linked_attempts': preflight['untouched_linked_attempts'],
    'untouched_supported_population_fraction': full_target_coverage,
    'holdout_A_selected_n': allocated_n,
    'fresh_live_rows': len(live_rows),
    'fresh_new_reco_ids': len(new_rows),
    'fresh_modern_7_10_untouched_n': len(fresh_modern_7_10),
    'decisions': preflight['decision']
}, indent=2))

if allocated_n != HOLDOUT_N or overlap:
    raise SystemExit(20)
