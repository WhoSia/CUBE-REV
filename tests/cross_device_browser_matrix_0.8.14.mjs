import {chromium,firefox,webkit,devices} from 'playwright';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PORT=8140;
const PARENT_URL=`http://127.0.0.1:${PORT}/participant-cognitive-mode-0.8.13.html?test_mode=1&diagnostic=0814`;
const STAGING_URL=`http://127.0.0.1:${PORT}/participant-cognitive-mode-0.8.14.html?test_mode=1&staging=0814`;
const engines={chromium,firefox,webkit};
const cells=[
  {id:'chromium-desktop',engine:'chromium',policy:'ACTIVE',context:{viewport:{width:1365,height:900},locale:'ko-KR'}},
  {id:'chromium-pixel7',engine:'chromium',policy:'ACTIVE',context:{...devices['Pixel 7'],locale:'ko-KR'}},
  {id:'firefox-desktop',engine:'firefox',policy:'FAIL_CLOSED',expectedReason:'FIREFOX_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED',context:{viewport:{width:1365,height:900},locale:'ko-KR'}},
  {id:'firefox-compact-viewport',engine:'firefox',policy:'FAIL_CLOSED',expectedReason:'FIREFOX_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED',context:{viewport:{width:412,height:915},deviceScaleFactor:2,locale:'ko-KR',userAgent:'Mozilla/5.0 (Android 14; Mobile; rv:141.0) Gecko/141.0 Firefox/141.0'}},
  {id:'webkit-desktop',engine:'webkit',policy:'FAIL_CLOSED',expectedReason:'DESKTOP_WEBKIT_CROSS_TAB_STORAGE_COHERENCE_UNCERTIFIED',context:{viewport:{width:1365,height:900},locale:'ko-KR'}},
  {id:'webkit-iphone14',engine:'webkit',policy:'ACTIVE',context:{...devices['iPhone 14'],locale:'ko-KR'}}
];
const HISTORICAL_UNSAFE={
  firefox:{workflow_run:30752617882,observed:'RESPONSE_APPLIED,RESPONSE_APPLIED',lock_serialized:true,final_pages_coherent:true},
  webkit_desktop:{workflow_run:30752617882,observed:'RESPONSE_APPLIED,RESPONSE_APPLIED',cell:'webkit-desktop'}
};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function waitServer(){const deadline=Date.now()+15000;while(Date.now()<deadline){try{const r=await fetch(`http://127.0.0.1:${PORT}/`);if(r.ok||r.status===404)return}catch{}await sleep(100)}throw new Error('STATIC_SERVER_TIMEOUT')}
async function waitConvergence(a,b){const deadline=Date.now()+10000;while(Date.now()<deadline){const [x,y]=await Promise.all([a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState())]);if(x.session_id===y.session_id&&x.revision===y.revision&&x.cursor===y.cursor)return {a:x,b:y};await sleep(100)}throw new Error('STATE_CONVERGENCE_TIMEOUT')}
async function op(page,display,tag){return page.evaluate(({display,tag})=>{const h=CUBE_REV_0813_TEST_HOOKS,s=h.getState(),p=h.responseAt(display,19);return {type:'RESPONSE',mutation_id:`CR0814-${tag}`,expected_revision:s.revision,expected_position:p.position,response:p.response}}, {display,tag})}
async function capabilities(page){return page.evaluate(()=>({web_locks:!!(navigator.locks&&navigator.locks.request),local_storage:typeof localStorage!=='undefined',storage_event:'onstorage' in window,pagehide_event:'onpagehide' in window,user_agent:navigator.userAgent,viewport:{width:innerWidth,height:innerHeight},touch_points:navigator.maxTouchPoints||0}))}
async function attachErrors(p,label,errors){p.on('pageerror',e=>errors.push({label,type:'pageerror',text:String(e.message||e)}));p.on('console',m=>{if(m.type()==='error')errors.push({label,type:'console',text:m.text()})})}
async function bootPair(context,url){
  const a=await context.newPage(),b=await context.newPage();
  await a.goto(url,{waitUntil:'domcontentloaded'});await a.click('#begin');await a.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS);
  await b.goto(url,{waitUntil:'domcontentloaded'});await b.click('#begin');await b.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS);
  await waitConvergence(a,b);return {a,b};
}
async function scheduleLockProbe(a,b,name){
  await a.evaluate(lockName=>{window.__cr0814LockA={entered:false,done:false};navigator.locks.request(lockName,{mode:'exclusive'},async()=>{window.__cr0814LockA.entered=true;await new Promise(resolve=>{window.__cr0814LockA.release=resolve});window.__cr0814LockA.done=true})},name);
  await a.waitForFunction(()=>window.__cr0814LockA?.entered===true);
  await b.evaluate(lockName=>{window.__cr0814LockB={entered:false,done:false};navigator.locks.request(lockName,{mode:'exclusive'},async()=>{window.__cr0814LockB.entered=true;window.__cr0814LockB.done=true})},name);
  await sleep(200);const bEnteredBeforeRelease=await b.evaluate(()=>window.__cr0814LockB?.entered===true);
  await a.evaluate(()=>window.__cr0814LockA.release());await Promise.all([a.waitForFunction(()=>window.__cr0814LockA?.done===true),b.waitForFunction(()=>window.__cr0814LockB?.done===true)]);
  return {b_entered_before_a_release:bEnteredBeforeRelease,serialized:!bEnteredBeforeRelease};
}
async function raceOnce(a,b,tag){
  const [oa,ob]=await Promise.all([op(a,'U',`${tag}-A`),op(b,'R',`${tag}-B`)]);
  const [ra,rb]=await Promise.all([a.evaluate(x=>CUBE_REV_0813_TEST_HOOKS.apply(x),oa),b.evaluate(x=>CUBE_REV_0813_TEST_HOOKS.apply(x),ob)]);
  await sleep(500);
  const [sa,sb,storedA,storedB,conflictsA,conflictsB]=await Promise.all([
    a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),
    a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState()),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState()),
    a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getConflictJournal()),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getConflictJournal())
  ]);
  const actions=[ra.action,rb.action];
  return {actions,dual_response_applied:actions.every(x=>x==='RESPONSE_APPLIED'),one_winner_conflict:[...actions].sort().join('|')==='RESPONSE_APPLIED|RESPONSE_CONFLICT',final_pages_coherent:sa.revision===sb.revision&&sa.cursor===sb.cursor&&JSON.stringify(storedA)===JSON.stringify(storedB),page_a:{revision:sa.revision,cursor:sa.cursor,response_count:storedA.responses.length,conflict_count:conflictsA.length},page_b:{revision:sb.revision,cursor:sb.cursor,response_count:storedB.responses.length,conflict_count:conflictsB.length}};
}
async function diagnoseParentEngine(id,browserType,contextOptions,historical){
  const browser=await browserType.launch({headless:true});const iterations=[];let caps=null,lockProbe=null;const errors=[];
  try{
    for(let i=0;i<6;i++){
      const context=await browser.newContext(contextOptions);const {a,b}=await bootPair(context,`${PARENT_URL}&engine=${id}&iteration=${i}`);attachErrors(a,'a',errors);attachErrors(b,'b',errors);
      try{if(!caps)caps=await capabilities(a);if(i===0)lockProbe=await scheduleLockProbe(a,b,`cube-rev-0814-${id}-lock-probe`);iterations.push({iteration:i,...await raceOnce(a,b,`${id}-${i}`)})}finally{await context.close().catch(()=>{})}
    }
  }finally{await browser.close().catch(()=>{})}
  const dualCount=iterations.filter(x=>x.dual_response_applied).length;const safeCount=iterations.filter(x=>x.one_winner_conflict).length;const incoherentCount=iterations.filter(x=>!x.final_pages_coherent).length;
  return {schema_version:'CR0814-PARENT-CONCURRENCY-DIAGNOSTIC-2',engine_profile:id,parent_route:'participant-cognitive-mode-0.8.13.html',capabilities:caps,lock_probe:lockProbe,iterations,iteration_count:iterations.length,dual_apply_count:dualCount,one_winner_conflict_count:safeCount,incoherent_final_count:incoherentCount,historical_unsafe_observation:historical,staging_policy_required:true,errors,result:dualCount>0?'OBSERVED_UNSAFE_DUAL_RESPONSE_APPLIED_IN_CURRENT_RUN':'FAIL_CLOSED_RETAINED_FROM_PRIOR_UNSAFE_OBSERVATION'};
}
async function runActiveCell(cell){
  const startedAt=new Date().toISOString();const browser=await engines[cell.engine].launch({headless:true});const iterations=[];const errors=[];let caps=null,gate=null;
  try{
    for(let i=0;i<4;i++){
      const context=await browser.newContext(cell.context);const a=await context.newPage(),b=await context.newPage();attachErrors(a,'a',errors);attachErrors(b,'b',errors);
      try{
        await a.goto(`${STAGING_URL}&cell=${cell.id}&iteration=${i}`,{waitUntil:'domcontentloaded'});gate=await a.evaluate(()=>window.CUBE_REV_0814_BROWSER_GATE||null);if(!gate||gate.status!=='ACTIVE_ALLOWED')throw new Error(`ACTIVE_GATE_INVALID:${JSON.stringify(gate)}`);await a.click('#begin');await a.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS);
        await b.goto(`${STAGING_URL}&cell=${cell.id}&iteration=${i}`,{waitUntil:'domcontentloaded'});await b.click('#begin');await b.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS);await waitConvergence(a,b);if(!caps)caps=await capabilities(a);if(!caps.web_locks)throw new Error('WEB_LOCKS_UNAVAILABLE');
        const race=await raceOnce(a,b,`${cell.id}-${i}`);if(!race.one_winner_conflict)throw new Error(`CONFLICT_ACTIONS:${race.actions.join(',')}`);if(!race.final_pages_coherent||race.page_a.response_count!==1||race.page_a.conflict_count!==1)throw new Error(`SERIALIZATION_RESULT:${JSON.stringify(race)}`);
        const before=await a.evaluate(()=>JSON.stringify(CUBE_REV_0813_TEST_HOOKS.getStoredState().responses));await b.evaluate(()=>dispatchEvent(typeof PageTransitionEvent==='function'?new PageTransitionEvent('pagehide',{persisted:false}):new Event('pagehide')));await b.close();await sleep(350);const after=await a.evaluate(()=>({responses:JSON.stringify(CUBE_REV_0813_TEST_HOOKS.getStoredState().responses),pagehide:CUBE_REV_0813_TEST_HOOKS.getStoredState().telemetry.some(e=>e.type==='PAGEHIDE')}));if(after.responses!==before)throw new Error('PAGEHIDE_RESPONSE_MUTATION');iterations.push({iteration:i,...race,pagehide_response_bytes_preserved:true,pagehide_telemetry_observed:after.pagehide});
      }finally{await context.close().catch(()=>{})}
    }
  }finally{await browser.close().catch(()=>{})}
  return {id:cell.id,engine:cell.engine,required_policy:cell.policy,status:'PASS_ACTIVE',started_at:startedAt,completed_at:new Date().toISOString(),gate,capabilities:caps,iterations,iteration_count:iterations.length,errors};
}
async function runFailClosedCell(cell){
  const startedAt=new Date().toISOString();const browser=await engines[cell.engine].launch({headless:true});const context=await browser.newContext(cell.context);const page=await context.newPage();const errors=[];attachErrors(page,'blocked',errors);
  try{
    await page.goto(`${STAGING_URL}&cell=${cell.id}`,{waitUntil:'domcontentloaded'});await page.waitForURL(/unsupported-browser-0\.8\.14\.html/);const result=await page.evaluate(()=>({gate:window.CUBE_REV_0814_BROWSER_GATE||null,storage_keys:Object.keys(localStorage).filter(k=>k.startsWith('cube-rev')),test_hooks_present:!!window.CUBE_REV_0813_TEST_HOOKS,begin_present:!!document.querySelector('#begin'),visible_text:document.body.innerText}));
    if(!result.gate||result.gate.status!=='BLOCKED'||result.gate.reason!==cell.expectedReason)throw new Error(`FAIL_CLOSED_GATE_INVALID:${JSON.stringify(result.gate)}`);if(result.storage_keys.length!==0)throw new Error(`FAIL_CLOSED_STATE_MUTATION:${result.storage_keys.join(',')}`);if(result.test_hooks_present||result.begin_present)throw new Error('FAIL_CLOSED_RUNTIME_BOOTED');
    return {id:cell.id,engine:cell.engine,required_policy:cell.policy,status:'PASS_FAIL_CLOSED',started_at:startedAt,completed_at:new Date().toISOString(),gate:result.gate,storage_keys:result.storage_keys,test_hooks_present:false,begin_present:false,message_present:result.visible_text.includes('과제를 시작하지 않았습니다'),errors};
  }finally{await context.close().catch(()=>{});await browser.close().catch(()=>{})}
}

const server=spawn('python3',['-m','http.server',String(PORT),'--bind','127.0.0.1'],{cwd:ROOT,stdio:'ignore'});const results=[];let diagnostics=null;
try{
  await waitServer();
  diagnostics={
    firefox:await diagnoseParentEngine('firefox',firefox,{viewport:{width:1365,height:900},locale:'ko-KR'},HISTORICAL_UNSAFE.firefox),
    webkit_desktop:await diagnoseParentEngine('webkit-desktop',webkit,{viewport:{width:1365,height:900},locale:'ko-KR'},HISTORICAL_UNSAFE.webkit_desktop)
  };
  console.log(`CR0814_PARENT_DIAGNOSTICS firefox_dual=${diagnostics.firefox.dual_apply_count}/6 webkit_desktop_dual=${diagnostics.webkit_desktop.dual_apply_count}/6 firefox_lock=${diagnostics.firefox.lock_probe.serialized} webkit_lock=${diagnostics.webkit_desktop.lock_probe.serialized}`);
  for(const cell of cells){try{const r=cell.policy==='ACTIVE'?await runActiveCell(cell):await runFailClosedCell(cell);results.push(r);console.log(`CR0814_DEVICE_CELL_PASS cell=${cell.id} status=${r.status}${r.iteration_count?` iterations=${r.iteration_count}`:''}`)}catch(error){results.push({id:cell.id,engine:cell.engine,required_policy:cell.policy,status:'FAIL',error:String(error&&error.stack||error)});console.error(`CR0814_DEVICE_CELL_FAIL cell=${cell.id} error=${String(error&&error.message||error)}`)}}
}finally{if(!server.killed)server.kill('SIGTERM')}
const passed=results.filter(x=>x.status==='PASS_ACTIVE'||x.status==='PASS_FAIL_CLOSED').length;const activePassed=results.filter(x=>x.status==='PASS_ACTIVE').length;const failClosedPassed=results.filter(x=>x.status==='PASS_FAIL_CLOSED').length;const activeIterations=results.filter(x=>x.status==='PASS_ACTIVE').reduce((n,x)=>n+x.iteration_count,0);
const report={schema_version:'CR0814-CROSS-DEVICE-BROWSER-MATRIX-3',route:'participant-cognitive-mode-0.8.14.html',parent_diagnostic_route:'participant-cognitive-mode-0.8.13.html',matrix_kind:'PLAYWRIGHT_ENGINE_AND_DEVICE_EMULATION_WITH_CONSERVATIVE_FAIL_CLOSED_POLICY_NOT_PHYSICAL_DEVICE',required_cells:cells.map(x=>({id:x.id,policy:x.policy,expected_reason:x.expectedReason||null})),passed_cells:passed,failed_cells:results.length-passed,active_execution_passed_cells:activePassed,fail_closed_passed_cells:failClosedPassed,active_race_iterations_passed:activeIterations,parent_concurrency_diagnostics:diagnostics,results,physical_device_certified:false,chromium_active_execution_certified_automated:true,ios_webkit_emulation_active_execution_certified_automated:true,firefox_active_execution_certified:false,desktop_webkit_active_execution_certified:false,result:passed===cells.length&&activePassed===3&&failClosedPassed===3&&activeIterations===12?'PASS_CONTROLLED_STAGING_BROWSER_POLICY_MATRIX':'FAIL_CONTROLLED_STAGING_BROWSER_POLICY_MATRIX'};
fs.mkdirSync(path.join(ROOT,'artifacts/0.8.14'),{recursive:true});fs.writeFileSync(path.join(ROOT,'artifacts/0.8.14/cross_device_browser_matrix.json'),JSON.stringify(report,null,2));if(report.result!=='PASS_CONTROLLED_STAGING_BROWSER_POLICY_MATRIX')throw new Error(`DEVICE_POLICY_MATRIX_INCOMPLETE:${passed}/${cells.length};active=${activePassed};blocked=${failClosedPassed};iterations=${activeIterations}`);console.log(`CR0814_CROSS_DEVICE_POLICY_MATRIX_PASS active_cells=${activePassed} fail_closed_cells=${failClosedPassed} active_races=${activeIterations} physical_device_certified=false firefox_active=false desktop_webkit_active=false`);
