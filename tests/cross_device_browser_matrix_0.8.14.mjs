import {chromium,firefox,webkit,devices} from 'playwright';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PORT=8140;
const ROUTE_URL=`http://127.0.0.1:${PORT}/participant-cognitive-mode-0.8.13.html?test_mode=1&staging=0814`;
const engines={chromium,firefox,webkit};
const cells=[
  {id:'chromium-desktop',engine:'chromium',context:{viewport:{width:1365,height:900},locale:'ko-KR'}},
  {id:'chromium-pixel7',engine:'chromium',context:{...devices['Pixel 7'],locale:'ko-KR'}},
  {id:'firefox-desktop',engine:'firefox',context:{viewport:{width:1365,height:900},locale:'ko-KR'}},
  {id:'firefox-mobile',engine:'firefox',context:{viewport:{width:412,height:915},deviceScaleFactor:2,isMobile:true,hasTouch:true,locale:'ko-KR'}},
  {id:'webkit-desktop',engine:'webkit',context:{viewport:{width:1365,height:900},locale:'ko-KR'}},
  {id:'webkit-iphone14',engine:'webkit',context:{...devices['iPhone 14'],locale:'ko-KR'}}
];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function waitServer(){const deadline=Date.now()+15000;while(Date.now()<deadline){try{const r=await fetch(`http://127.0.0.1:${PORT}/`);if(r.ok||r.status===404)return}catch{}await sleep(100)}throw new Error('STATIC_SERVER_TIMEOUT')}
async function waitConvergence(a,b){const deadline=Date.now()+10000;while(Date.now()<deadline){const [x,y]=await Promise.all([a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState())]);if(x.session_id===y.session_id&&x.revision===y.revision&&x.cursor===y.cursor)return {a:x,b:y};await sleep(100)}throw new Error('STATE_CONVERGENCE_TIMEOUT')}
async function op(page,display,tag){return page.evaluate(({display,tag})=>{const h=CUBE_REV_0813_TEST_HOOKS,s=h.getState(),p=h.responseAt(display,19);return {type:'RESPONSE',mutation_id:`CR0814-${tag}`,expected_revision:s.revision,expected_position:p.position,response:p.response}}, {display,tag})}
async function runCell(cell){
  const startedAt=new Date().toISOString();
  const browser=await engines[cell.engine].launch({headless:true});
  const context=await browser.newContext(cell.context);
  const errors=[];
  const [a,b]=await Promise.all([context.newPage(),context.newPage()]);
  for(const [label,p] of [['a',a],['b',b]]){p.on('pageerror',e=>errors.push({label,type:'pageerror',text:String(e.message||e)}));p.on('console',m=>{if(m.type()==='error')errors.push({label,type:'console',text:m.text()})})}
  try{
    await Promise.all([a.goto(ROUTE_URL,{waitUntil:'domcontentloaded'}),b.goto(ROUTE_URL,{waitUntil:'domcontentloaded'})]);
    await Promise.all([a.click('#begin'),b.click('#begin')]);
    await Promise.all([a.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS),b.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS)]);
    const capabilities=await a.evaluate(()=>({
      web_locks:!!(navigator.locks&&navigator.locks.request),
      local_storage:typeof localStorage!=='undefined',
      storage_event:'onstorage' in window,
      pagehide_event:'onpagehide' in window,
      user_agent:navigator.userAgent,
      viewport:{width:innerWidth,height:innerHeight},
      touch_points:navigator.maxTouchPoints||0
    }));
    if(!capabilities.web_locks)throw new Error('WEB_LOCKS_UNAVAILABLE');
    const initial=await waitConvergence(a,b);
    if(initial.a.cursor!==0)throw new Error(`INITIAL_CURSOR:${initial.a.cursor}`);
    const [oa,ob]=await Promise.all([op(a,'U',`${cell.id}-A`),op(b,'R',`${cell.id}-B`)]);
    const [ra,rb]=await Promise.all([a.evaluate(x=>CUBE_REV_0813_TEST_HOOKS.apply(x),oa),b.evaluate(x=>CUBE_REV_0813_TEST_HOOKS.apply(x),ob)]);
    const actions=[ra.action,rb.action].sort();
    if(JSON.stringify(actions)!==JSON.stringify(['RESPONSE_APPLIED','RESPONSE_CONFLICT'].sort()))throw new Error(`CONFLICT_ACTIONS:${actions.join(',')}`);
    const converged=await waitConvergence(a,b);
    const stored=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
    const conflicts=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getConflictJournal());
    if(stored.cursor!==1||stored.responses.length!==1||conflicts.length!==1)throw new Error(`SERIALIZATION_RESULT:${stored.cursor}/${stored.responses.length}/${conflicts.length}`);
    const responseBytes=JSON.stringify(stored.responses);
    await b.evaluate(()=>dispatchEvent(typeof PageTransitionEvent==='function'?new PageTransitionEvent('pagehide',{persisted:false}):new Event('pagehide')));
    await b.close();await sleep(350);
    const afterHide=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
    if(JSON.stringify(afterHide.responses)!==responseBytes)throw new Error('PAGEHIDE_RESPONSE_MUTATION');
    return {id:cell.id,engine:cell.engine,status:'PASS',started_at:startedAt,completed_at:new Date().toISOString(),capabilities,revision:converged.a.revision,cursor:afterHide.cursor,conflict_count:conflicts.length,pagehide_response_bytes_preserved:true,pagehide_telemetry_observed:afterHide.telemetry.some(e=>e.type==='PAGEHIDE'),errors};
  }finally{await context.close().catch(()=>{});await browser.close().catch(()=>{})}
}

const server=spawn('python3',['-m','http.server',String(PORT),'--bind','127.0.0.1'],{cwd:ROOT,stdio:'ignore'});
const results=[];
try{
  await waitServer();
  for(const cell of cells){
    try{const r=await runCell(cell);results.push(r);console.log(`CR0814_DEVICE_CELL_PASS cell=${cell.id} revision=${r.revision} pagehide=${r.pagehide_telemetry_observed}`)}
    catch(error){results.push({id:cell.id,engine:cell.engine,status:'FAIL',error:String(error&&error.stack||error)});console.error(`CR0814_DEVICE_CELL_FAIL cell=${cell.id} error=${String(error&&error.message||error)}`)}
  }
}finally{if(!server.killed)server.kill('SIGTERM')}
const passed=results.filter(x=>x.status==='PASS').length;
const report={schema_version:'CR0814-CROSS-DEVICE-BROWSER-MATRIX-1',route:'participant-cognitive-mode-0.8.13.html',matrix_kind:'PLAYWRIGHT_ENGINE_AND_DEVICE_EMULATION_NOT_PHYSICAL_DEVICE',required_cells:cells.map(x=>x.id),passed_cells:passed,failed_cells:results.length-passed,results,physical_device_certified:false,result:passed===cells.length?'PASS_AUTOMATED_CROSS_ENGINE_DEVICE_EMULATION':'FAIL_AUTOMATED_CROSS_ENGINE_DEVICE_EMULATION'};
fs.mkdirSync(path.join(ROOT,'artifacts/0.8.14'),{recursive:true});
fs.writeFileSync(path.join(ROOT,'artifacts/0.8.14/cross_device_browser_matrix.json'),JSON.stringify(report,null,2));
if(passed!==cells.length)throw new Error(`DEVICE_MATRIX_INCOMPLETE:${passed}/${cells.length}`);
console.log(`CR0814_CROSS_DEVICE_MATRIX_PASS ${passed}/${cells.length} physical_device_certified=false`);
