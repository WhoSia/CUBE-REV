#!/usr/bin/env python3
import argparse, csv, io, json, re, zipfile
from collections import Counter, defaultdict
from pathlib import Path
from p15_r1_adapter import classify

csv.field_size_limit(10_000_000)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--zip',required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--shard',type=int,default=0); ap.add_argument('--shards',type=int,default=1); a=ap.parse_args()
    pairs=Counter(); ops=Counter(); missing=Counter(); timing=Counter(); by_k=defaultdict(set); by_l=defaultdict(set)
    with zipfile.ZipFile(a.zip) as z:
        names=sorted(n for n in z.namelist() if n.endswith('_keystrokes.txt'))[a.shard::a.shards]
        for fi,n in enumerate(names):
            with z.open(n) as f:
                rd=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',errors='replace',newline=''),delimiter='\t')
                prev=None
                for r in rd:
                    k=r.get('KEYCODE'); l=r.get('LETTER'); pairs[(k,l)]+=1; by_k[k].add(l); by_l[l].add(k)
                    op,_=classify(l,k); ops[op]+=1
                    if k in (None,''): missing['keycode']+=1
                    if l in (None,''): missing['letter']+=1
                    try: p=float(r['PRESS_TIME']); q=float(r['RELEASE_TIME'])
                    except (TypeError,ValueError): missing['timestamp']+=1; continue
                    if q<p: timing['negative_dwell']+=1
                    if q==p: timing['zero_dwell']+=1
                    if prev is not None and p<prev: timing['press_order_violation']+=1
                    if prev==p: timing['duplicate_press_timestamp']+=1
                    prev=p
            if fi and fi%10000==0: print(fi,flush=True)
    out={'shard':a.shard,'shards':a.shards,'rows':sum(pairs.values()),'ops':ops,'missing':missing,'timing':timing,
         'keycodes':len(by_k),'letters':len(by_l),'one_to_many_keycodes':sum(len(v)>1 for v in by_k.values()),
         'many_to_one_letters':sum(len(v)>1 for v in by_l.values()),
         'top_pairs':[{'keycode':k,'letter':l,'n':n} for (k,l),n in pairs.most_common(500)]}
    Path(a.out).mkdir(parents=True,exist_ok=True); Path(a.out,'census.json').write_text(json.dumps(out,indent=2,default=dict),encoding='utf-8')
if __name__=='__main__': main()
