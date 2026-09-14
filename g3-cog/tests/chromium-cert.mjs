import {chromium} from 'playwright';
import {createHash} from 'node:crypto';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';

const BASE=process.env.G3_BASE_URL||'http://127.0.0.1:4173';
const raw=readFileSync('g3-cog/packets/p7-presentation.v2.json');
const packet=JSON.parse(raw);
const packetSha=createHash('sha256').update(raw).digest('hex');
const surfaces=['CE58350B7296','CE19C568F125','CDFFBCD6318B','C8110F5ACF15','CB00BE672FAA'];
const cells=packet.cells.map(x=>x.cell);
const adversaries=['packet_mismatch','start_state_mismatch','probe_mismatch','prearm_response','duplicate_response','hidden_during_history','hidden_at_probe','reload_before_response','reload_after_response_before_persistence','stale_prior_receipt','marker_state_mutation','unsupported_action_token'];
const receipt={schema:'CUBE-REV-G3-P10-R1-CHROMIUM-CERT-v1',git_sha:process.env.GITHUB_SHA||null,packet_sha256:packetSha,predecessor_declared_sha256:packet.predecessor_declared_sha256,predecessor_exact_bytes_status:packet.predecessor_exact_bytes_status,browser:null,state_checks:{pass:0,total:35},dom_actions:{pass:0,total:108},adversarial:{pass:0,total:72},render_pairs:[],probe_runtime_digest:null,probe_declared_p7_digest:packet.declared_probe_sha256,notes:[]};

function assert(x,msg){if(!x)throw new Error(msg);}
const browser=await chromium.launch({headless:true});
receipt.browser=await browser.version();
const page=await browser.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1});

try{
  // H1: five render surfaces x seven checkpoints.
  let commonProbe=null;
  for(const id of surfaces){
    await page.goto(`${BASE}/?cell=${id}`,{waitUntil:'networkidle'});
    await page.waitForFunction(()=>window.G3Runtime&&window.G3Runtime.cell);
    const cps=await page.evaluate(async()=>{
      const r=window.G3Runtime,out=[];
      for(const s of r.checkpoints()) out.push({serialization:window.G3State.serializeState(s),digest:await window.G3State.stateDigest(s)});
      return out;
    });
    assert(cps.length===7,`${id}: checkpoint count`);
    for(const cp of cps){assert(cp.digest?.length===64,`${id}: digest`);receipt.state_checks.pass++;}
    if(commonProbe===null)commonProbe=cps[6].serialization;else assert(cps[6].serialization===commonProbe,`${id}: probe divergence`);
  }
  receipt.probe_runtime_digest=createHash('sha256').update(commonProbe).digest('hex');

  // Render declared-difference checks: same history, R off/on.
  for(const [a,b] of [['CE58350B7296','C8110F5ACF15'],['CDFFBCD6318B','CB00BE672FAA']]){
    const snaps=[];
    for(const id of [a,b]){
      await page.goto(`${BASE}/?cell=${id}&autorun=1`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.G3Runtime?.phase==='RESPONSE_ARM');
      snaps.push(await page.evaluate(()=>({cube:document.querySelector('#cube-net').innerHTML,box:document.querySelector('#cube-net').getBoundingClientRect().toJSON(),markerHidden:document.querySelector('#marker-layer').hidden,state:window.G3Runtime.snapshot().state})));
    }
    assert(snaps[0].cube===snaps[1].cube,`${a}/${b}: cube DOM changed by marker`);assert(snaps[0].state===snaps[1].state,`${a}/${b}: state changed by marker`);assert(snaps[0].markerHidden&&!snaps[1].markerHidden,`${a}/${b}: marker visibility`);receipt.render_pairs.push({a,b,pass:true});
  }

  // H2: 6 x 18 real DOM click activations.
  for(const id of cells)for(const action of packet.actions){
    await page.goto(`${BASE}/?cell=${id}&autorun=1`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.G3Runtime?.phase==='RESPONSE_ARM');
    await page.evaluate(a=>[...document.querySelectorAll('#response-grid button')].find(b=>b.dataset.action===a).click(),action);
    const snap=await page.evaluate(()=>window.G3Runtime.snapshot());
    assert(snap.phase==='END',`${id}/${action}: not END`);assert(snap.locked?.action===action,`${id}/${action}: lock mismatch`);receipt.dom_actions.pass++;
  }

  // H3: 6 x 12 fail-closed browser-trigger cases.
  for(const id of cells)for(const kind of adversaries){
    await page.goto(`${BASE}/?cell=${id}`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.G3Runtime&&window.G3Runtime.cell);
    const ok=await page.evaluate(k=>window.G3Runtime.adversary(k),kind);const phase=await page.evaluate(()=>window.G3Runtime.phase);
    assert(ok&&phase==='FAIL_CLOSED',`${id}/${kind}: fail-open`);receipt.adversarial.pass++;
  }

  assert(receipt.state_checks.pass===35,'35-checkpoint total');
  assert(receipt.dom_actions.pass===108,'108-action total');
  assert(receipt.adversarial.pass===72,'72-adversarial total');
  receipt.notes.push(packetSha===packet.predecessor_declared_sha256?'unexpected predecessor byte identity':'v2 successor bytes differ from unavailable predecessor as declared');
  receipt.result='PASS_BROWSER_SEMANTIC_CERT_WITH_P7_PREDECESSOR_BYTE_SUPERSESSION';
} catch(err){receipt.result='FAIL';receipt.error=String(err?.stack||err);throw err;
} finally{
  mkdirSync('g3-cog/certification',{recursive:true});writeFileSync('g3-cog/certification/receipt.json',JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify(receipt,null,2));await browser.close();
}
