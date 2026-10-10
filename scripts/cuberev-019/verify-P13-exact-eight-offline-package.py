#!/usr/bin/env python3
"""CUBE-REV 0.19 P13: offline physical 8-word / no-7 finite verifier.

--quick: SHA256 verify full P13 proof package and independently replay its
        8-word witness; checks stage receipts, but DOES NOT redo exclusions.
--full:  regenerate P9/P12 dual-and-high-rank checks and ALL P13 t=0..7 finite
        proof stages (including 14 four-rank7 symmetry chunks) before the
        final original physical witness, entirely offline and without SAT/LP.

No network access, SAT solver or external files required beyond P13 ZIP.
Usage: python CUBE_REV_019_P13_offline_proof_runner.py --package path.zip --full
"""
import argparse, concurrent.futures, hashlib, json, os, pathlib, subprocess, sys, tempfile, zipfile
P=argparse.ArgumentParser()
P.add_argument('--package',required=True)
g=P.add_mutually_exclusive_group();g.add_argument('--full',action='store_true');g.add_argument('--quick',action='store_true')
P.add_argument('--workers',type=int,default=4)
P.add_argument('--output',help='Optional JSON receipt path')
a=P.parse_args()

def sha(raw):return hashlib.sha256(raw).hexdigest()
def jread(p):return json.loads(pathlib.Path(p).read_text())
def execute(script,*args,env=None):
 cmd=[sys.executable,str(script),*map(str,args)]
 p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
 if p.returncode!=0:raise RuntimeError(f'VERIFIER_FAILED {script}\nSTDOUT:\n{p.stdout[-2000:]}\nSTDERR:\n{p.stderr[-2000:]}')
 print('FINITE_STAGE_PASS',script.name,p.stdout.strip().splitlines()[-1][:190],flush=True)
 return p

with tempfile.TemporaryDirectory(prefix='cuberev019_p13_') as tmp:
 root=pathlib.Path(tmp);pkg=pathlib.Path(a.package)
 with zipfile.ZipFile(pkg) as z:
  assert z.testzip() is None
  z.extractall(root)
 manifest=jread(root/'SHA256_MANIFEST.json')
 assert manifest['source_physical_sha256']=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
 for name,entry in manifest['files'].items():
  raw=(root/name).read_bytes()
  assert sha(raw)==entry['sha256'] and len(raw)==entry['bytes'],f'CORRUPTED_CERTIFICATE {name}'
 original=root/'SOURCE/original_physical.json';parts=root/'SOURCE/original_L5_partitions.tsv';maps=root/'SOURCE/original_move_maps.txt'
 assert sha(original.read_bytes())==manifest['source_physical_sha256']
 nested=root/'PRIOR/P12_exact_R5_seven_complete_reproducibility.zip'
 with zipfile.ZipFile(nested) as z:
  assert z.testzip() is None
  z.extractall(root/'PRIOR/p12')
 prior=root/'PRIOR/p12'
 assert (prior/'original_physical.json').read_bytes()==original.read_bytes()
 assert (prior/'original_L5_partitions.tsv').read_bytes()==parts.read_bytes()
 assert (prior/'original_move_maps.txt').read_bytes()==maps.read_bytes()
 out=root/'OUTPUT';out.mkdir()
 if a.full:
  dual=prior/'original_R5_fractional_dual.json'
  execute(prior/'P9_five_source_k5_exact_verifier.py','--physical',original,'--maps',maps,'--partitions',parts,'--dual',dual,'--output',out/'P9.json')
  extra=[ '--physical',original,'--maps',maps,'--partitions',parts,
         '--duals_first',prior/'P12_rank_sensitive_integer_duals.json',
         '--duals_rank6',prior/'P12_raw_rank6_70_integer_duals.json',
         '--duals_rank7',prior/'P12_rank7_pair_triple_integer_duals.json']
  execute(prior/'P12_verify_integer_duals.py',*extra,'--output',out/'P12_DUALS.json')
  execute(prior/'P12_verify_high_rank_finite_cases.py',*extra,'--output',out/'P12_HIGH.json')
  execute(prior/'P12_compile_exact_theorem.py','--physical',original,'--p9',out/'P9.json', '--duals',out/'P12_DUALS.json', '--rank7',out/'P12_HIGH.json','--output',out/'P12_EXACT.json')
  execute(root/'T0/verify_t0_rank5_rank6_exhaustive.py','--physical',original,'--partitions',parts,
          '--cert0',root/'T0/dual_0_24.json','--cert1',root/'T0/dual_24_49.json', '--cert2',root/'T0/dual_49_74.json',
          '--nine',root/'T0/nine_branch_weight_filters.json','--output',out/'T0.json')
  execute(root/'T1_3/verify_rank7_1to3_integer_duals.py','--physical',original,'--partitions',parts,
          '--certificates',root/'T1_3/original_source_integer_certificates.json','--output',out/'T123.json')
  execute(root/'T5_7/verify_R7_count_5_6_7.py','--physical',original,'--partitions',parts,'--output',out/'T567.json')
  ranges=[(i,min(i+180,2361)) for i in range(0,2361,180)]
  def run_chunk(pair):
   lo,hi=pair;dest=out/f'T4_{lo}_{hi}.json';env=os.environ.copy();env.update(P13_BEGIN=str(lo),P13_END=str(hi))
   subprocess.run([sys.executable,str(root/'T4/verify_rank7_four_chunked_independent.py'),'--physical',str(original),'--partitions',str(parts),'--output',str(dest)],env=env,check=True,stdout=subprocess.DEVNULL)
   doc=jread(dest)
   assert doc['result']=='NO_FULL_SEVEN_WITH_EXACTLY_FOUR_RANK7'
   assert doc['orbits_checked']==hi-lo and doc['first_orbit_in_slice']==lo and doc['end_orbit_exclusive']==hi
   return lo,hi,doc['attempted_first_low_words']
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as ex:records=sorted(ex.map(run_chunk,ranges))
  assert [(a,b) for a,b,n in records]==ranges
  assert sum(b-a for a,b,n in records)==2361
  assert sum(n for a,b,n in records)==359004
  print('FINITE_STAGE_PASS t4_2361_orbit_fresh_complete 359004',flush=True)
  t4={'result':'P13_T4_ALL_2361_ORBITS_FRESH_INDEPENDENT_COMPLETE_PASS',
      'physical_source_sha256':manifest['source_physical_sha256'],
      'rechecked_orbits':2361,'rechecked_first_low_trials':359004}
  (out/'T4.json').write_text(json.dumps(t4)+'\n')
  t4=out/'T4.json'
  p12,t0,t123,t567=out/'P12_EXACT.json',out/'T0.json',out/'T123.json',out/'T567.json'
 else:
  p12=root/'PRIOR/p12/P12_final_exact_R5_7_receipt.json'
  t0=root/'T0/FRESH_receipt.json';t123=root/'T1_3/FRESH_receipt.json';t567=root/'T5_7/FRESH_receipt.json'
  t4=root/'T4/FRESH_all_2361_composite.json'
 execute(root/'FINAL/P13_compile_full_exact_Mstar5.py','--physical',original,'--maps',maps,
         '--p12',p12,'--t0',t0,'--t123',t123,'--t4',t4,'--t567',t567,
         '--output',out/'THEOREM.json')
 receipt=jread(out/'THEOREM.json')
 assert receipt['exact_minimum']==8 and receipt['witness_union_all_1192']==1192
 assert receipt['result']=='CUBE_REV_019_P13_ORIGINAL_FULL_1192_PHYSICAL_MSTAR5_EXACT_EIGHT_LOCAL_FINITE_PROOF_PASS'
 receipt['offline_runner_mode']='FULL_INDEPENDENT_FINITE_REEXECUTION' if a.full else 'QUICK_MANIFEST_AND_WITNESS_REPLAY_ONLY'
 receipt['package_sha256']=sha(pkg.read_bytes())
 if a.output:pathlib.Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
 print('CUBE_REV_019_P13_OFFLINE_PACKAGE_'+('FULL_PROOF' if a.full else 'QUICK_AUDIT')+'_PASS',sha(pkg.read_bytes()),flush=True)