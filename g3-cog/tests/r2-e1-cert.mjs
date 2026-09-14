import {chromium} from 'playwright';
import {createHash} from 'node:crypto';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';

const BASE=(process.env.G3_E1_URL||'https://cube-rev-g3-cog-e1.onrender.com').replace(/\/$/,'');
const expectedCandidate=JSON.parse(readFileSync('g3-cog/candidate.json','utf8'));
const crosswalk=JSON.parse(readFileSync('g3-cog/certification/p7-hash-crosswalk.json','utf8'));
const packet=JSON.parse(readFileSync('g3-cog/packets/p7-presentation.v2.json','utf8'));
const markerCells=['C8110F5ACF15','CB00BE672FAA'];
const matchedPairs=[['CE58350B7296','C8110F5ACF15'],['CDFFBCD6318B','CB00BE672FAA']];
const hash=b=>createHash('sha256').update(b).digest('hex');
const assert=(x,m)=>{if(!x)throw new Error(m);};
function perms(xs){if(xs.length<=1)return[xs];const out=[];for(let i=0;i<xs.length;i++){const x=xs[i],rest=xs.slice(0,i).concat(xs.slice(i+1));for(const p of perms(rest))out.push(x+p);}return out;}
const permutations=perms('ABCD');

const receipt={schema:'CUBE-REV-G3-P10-R2-E1-CERT-v1',base_url:BASE,candidate_id:expectedCandidate.candidate_id,browser:null,served_https:false,candidate_binding:false,marker_permutations:{pass:0,total:markerCells.length*permutations.length},manifest_commits:{pass:0,total:markerCells.length*permutations.length},response_manifest_bindings:{pass:0,total:permutations.length},cube_pixel_invariance:{pass:0,total:markerCells.length*permutations.length},matched_r0_r1_pixel_pairs:{pass:0,total:matchedPairs.length},crosswalk:null,generalization:null,result:'PENDING'};

async function waitCandidate(){
  for(let i=0;i<60;i++){
    try{const r=await fetch(`${BASE}/candidate.json`,{cache:'no-store'});if(r.ok){const j=await r.json();if(j.candidate_id===expectedCandidate.candidate_id)return j;}}catch{}
    await new Promise(r=>setTimeout(r,2000));
  }
  throw new Error('served candidate did not converge');
}

const browser=await chromium.launch({headless:true});receipt.browser=await browser.version();
const page=await browser.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1});
try{
  assert(new URL(BASE).protocol==='https:','E1 not HTTPS');receipt.served_https=true;
  const servedCandidate=await waitCandidate();assert(servedCandidate.candidate_id===expectedCandidate.candidate_id,'candidate mismatch');receipt.candidate_binding=true;

  for(const cell of markerCells){
    let baselineState=null,baselineCubePixel=null;const manifestHashes=new Set();
    for(const perm of permutations){
      await page.goto(`${BASE}/?cell=${cell}&perm=${perm}&autorun=1`,{waitUntil:'networkidle'});
      await page.waitForFunction(()=>window.G3Runtime?.phase==='RESPONSE_ARM');
      const snap=await page.evaluate(()=>window.G3Runtime.snapshot());
      const labels=await page.locator('#marker-layer [data-pair]').allTextContents();
      const cubePixel=hash(await page.locator('#cube-net').screenshot());
      assert(labels.join('')===perm,`${cell}/${perm}: label permutation`);
      assert(snap.permutation===perm,`${cell}/${perm}: runtime permutation`);
      assert(snap.manifest?.candidate_id===expectedCandidate.candidate_id,`${cell}/${perm}: candidate manifest`);
      assert(snap.manifest?.served_origin===new URL(BASE).origin,`${cell}/${perm}: origin manifest`);
      assert(snap.manifest_hash?.length===64,`${cell}/${perm}: manifest hash`);
      assert(Object.values(snap.manifest.asset_hashes||{}).every(x=>typeof x==='string'&&x.length===64),`${cell}/${perm}: asset hashes`);
      manifestHashes.add(snap.manifest_hash);receipt.marker_permutations.pass++;receipt.manifest_commits.pass++;
      if(baselineState===null){baselineState=snap.state;baselineCubePixel=cubePixel;}else{assert(snap.state===baselineState,`${cell}/${perm}: physical state changed`);assert(cubePixel===baselineCubePixel,`${cell}/${perm}: cube pixels changed`);}
      receipt.cube_pixel_invariance.pass++;
      if(cell===markerCells[0]){await page.locator('[data-action="D2"]').click();const post=await page.evaluate(()=>window.G3Runtime.snapshot());assert(post.locked?.manifest_hash===snap.manifest_hash,`${cell}/${perm}: response/manifest join`);receipt.response_manifest_bindings.pass++;}
    }
    assert(manifestHashes.size===permutations.length,`${cell}: permutation did not alter manifest identity`);
  }

  for(const [r0,r1] of matchedPairs){
    const pix=[];const states=[];
    for(const id of [r0,r1]){await page.goto(`${BASE}/?cell=${id}&perm=ABCD&autorun=1`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.G3Runtime?.phase==='RESPONSE_ARM');pix.push(hash(await page.locator('#cube-net').screenshot()));states.push((await page.evaluate(()=>window.G3Runtime.snapshot())).state);}
    assert(pix[0]===pix[1],`${r0}/${r1}: cube pixel mismatch`);assert(states[0]===states[1],`${r0}/${r1}: state mismatch`);receipt.matched_r0_r1_pixel_pairs.pass++;
  }

  await page.goto(`${BASE}/?cell=CE58350B7296&autorun=1`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.G3Runtime?.phase==='RESPONSE_ARM');
  const probeDigest=await page.evaluate(async()=>window.G3State.stateDigest(window.G3Runtime.state));
  assert(probeDigest===crosswalk.successor_probe_sha256,'crosswalk successor probe drift');
  assert(crosswalk.crosswalk_type==='SEMANTIC_RELATION_NOT_HASH_TRANSFORM','crosswalk type');
  assert(crosswalk.predecessor_probe_sha256!==crosswalk.successor_probe_sha256,'false namespace identity');
  receipt.crosswalk={pass:true,type:crosswalk.crosswalk_type,predecessor_probe_sha256:crosswalk.predecessor_probe_sha256,successor_probe_sha256:probeDigest};

  const nonCube=JSON.parse(execFileSync(process.execPath,['g3-cog/generalization/torus-witness.mjs'],{encoding:'utf8'}));
  assert(nonCube.result==='PASS','non-Cube RSTP witness failed');receipt.generalization=nonCube;

  for(const k of ['marker_permutations','manifest_commits','response_manifest_bindings','cube_pixel_invariance','matched_r0_r1_pixel_pairs'])assert(receipt[k].pass===receipt[k].total,`${k} total`);
  receipt.result='PASS_E1_R2_WITH_RSTP_GENERALIZATION';
} catch(e){receipt.result='FAIL';receipt.error=String(e?.stack||e);process.exitCode=1;
} finally{mkdirSync('g3-cog/certification',{recursive:true});writeFileSync('g3-cog/certification/r2-receipt.json',JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt,null,2));await browser.close();}
