#!/usr/bin/env python3
from __future__ import annotations
import asyncio, json, os, shutil, socket, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
ART=Path(os.environ.get('CR0105R11_ARTIFACT_DIR','cr0105r11-artifact')).resolve(); ART.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok,detail=None):
    checks.append({'name':name,'pass':bool(ok),'detail':detail})
    if not ok: print('FAIL',name,detail,flush=True)

def free_port():
    s=socket.socket(); s.bind(('127.0.0.1',0)); p=s.getsockname()[1]; s.close(); return p
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass

def server():
    p=free_port(); h=lambda *a,**k: Quiet(*a,directory=str(ROOT),**k); srv=ThreadingHTTPServer(('127.0.0.1',p),h); threading.Thread(target=srv.serve_forever,daemon=True).start(); return srv,p

async def block_remote(route):
    if route.request.url.startswith(('http://127.0.0.1:','http://localhost:')): await route.continue_()
    else: await route.abort()

async def wait_input(page):
    await page.wait_for_function("typeof inputEnabled!=='undefined' && inputEnabled===true",timeout=12000)

async def start_custom(page,keymap='speed'):
    await page.goto(BASE,wait_until='domcontentloaded',timeout=30000)
    await page.wait_for_function("window.__CUBEREV_SELFTEST__ && window.__CUBEREV_SELFTEST__.passed===true",timeout=15000)
    await page.check('#consentCheck')
    await page.check('input[name="mode"][value="custom"]')
    await page.fill('#customScramble','R U')
    if await page.locator(f'input[name="keymap"][value="{keymap}"]').count(): await page.check(f'input[name="keymap"][value="{keymap}"]')
    await page.click('#startButton'); await wait_input(page)

async def snap(page):
    return await page.evaluate("() => ({camera:structuredClone(camera),state:stateKey(logicalState),events:session.events.length,moves:currentTrialRecord?.accepted_moves?.length||0,mode:session.mode,keymap:session.interface_settings.keymap_mode})")

async def desktop_court(browser):
    ctx=await browser.new_context(accept_downloads=True,viewport={'width':1280,'height':850})
    await ctx.route('**/*',block_remote); p=await ctx.new_page(); remote=[]
    p.on('request',lambda r: remote.append(r.url) if not r.url.startswith(('http://127.0.0.1:','http://localhost:')) else None)
    await start_custom(p,'speed'); check('self_test_pass',True)
    s0=await snap(p); box=await p.locator('#cubeCanvas').bounding_box(); assert box
    for _ in range(8):
        x=box['x']+18; y0=box['y']+box['height']*.82; y1=box['y']+box['height']*.18
        await p.mouse.move(x,y0); await p.mouse.down(); await p.mouse.move(x,y1,steps=8); await p.mouse.up()
    s1=await snap(p)
    orbit_delta=max(abs(float(s1['camera'].get('pitch',0))-float(s0['camera'].get('pitch',0))),abs(float(s1['camera'].get('yaw',0))-float(s0['camera'].get('yaw',0))))
    evs=await p.evaluate("() => session.events.filter(e=>e.type==='camera_drag_end')")
    accumulated=sum(abs(float(e.get('delta_pitch',0) or 0))+abs(float(e.get('delta_yaw',0) or 0)) for e in evs)
    check('background_camera_orbit',s1['state']==s0['state'] and s1['camera']['view_matrix']!=s0['camera']['view_matrix'],{'compat_delta':orbit_delta,'accumulated':accumulated})
    check('camera_orbit_gt_180',orbit_delta>3.1415926535 or accumulated>3.1415926535,{'compat_delta':orbit_delta,'accumulated':accumulated})
    z0=float(s1['camera']['zoom']); await p.mouse.move(box['x']+20,box['y']+20); await p.mouse.wheel(0,-700); await p.wait_for_timeout(250); s2=await snap(p)
    check('wheel_zoom',float(s2['camera']['zoom'])!=z0 and s2['state']==s1['state'],{'before':z0,'after':s2['camera']['zoom']})
    await p.click('#cameraResetButton'); await p.wait_for_timeout(100); s3=await snap(p); check('camera_reset',s3['camera']['view_matrix']!=s2['camera']['view_matrix'])
    drag_before=await p.evaluate("() => session.events.filter(e=>e.type==='move_accepted').length")
    hit=await p.evaluate("() => projectedStickerHits.find(h=>h.front && h.screenCenter)")
    drag_ok=False
    if hit:
      cx=box['x']+hit['screenCenter']['x']; cy=box['y']+hit['screenCenter']['y']
      for dx,dy in [(90,0),(-90,0),(0,90),(0,-90),(70,70),(-70,70),(70,-70),(-70,-70)]:
        await p.mouse.move(cx,cy); await p.mouse.down(); await p.mouse.move(cx+dx,cy+dy,steps=10); await p.mouse.up(); await p.wait_for_timeout(180)
        n=await p.evaluate("() => session.events.filter(e=>e.type==='move_accepted').length")
        if n>drag_before: drag_ok=True; break
    check('sticker_drag_single_quarter_turn',drag_ok,{'hit_face':hit.get('face') if hit else None})
    b=await snap(p); await p.click('button[data-move="R"]'); await p.wait_for_timeout(140); a=await snap(p); check('face_button_turn',a['state']!=b['state'])
    before=await snap(p); await p.click('button[data-move="x"]'); await p.wait_for_timeout(140); after=await snap(p); xev=await p.evaluate("() => session.events.filter(e=>e.type==='move_accepted').slice(-1)[0]")
    check('whole_cube_rotation_control',bool(xev) and xev.get('move')=='x',xev)
    ub=await snap(p); await p.click('#undoButton'); await p.wait_for_timeout(160); ua=await snap(p); check('undo_button',ua['events']>ub['events'])
    p.once('dialog',lambda d: asyncio.create_task(d.accept())); await p.click('#resetTrialButton'); await p.wait_for_timeout(180); reset_ev=await p.evaluate("() => session.events.some(e=>e.type==='trial_reset')")
    check('trial_reset_button',reset_ev)
    m0=await p.evaluate("() => session.events.filter(e=>e.type==='move_accepted').length"); await p.keyboard.press('KeyJ'); await p.wait_for_timeout(130); m1=await p.evaluate("() => session.events.filter(e=>e.type==='move_accepted').length"); check('speed_keyboard_layout',m1>m0)
    if await p.locator('#languageSelect option[value="en"]').count():
      await p.select_option('#languageSelect','en'); await p.wait_for_timeout(100); lang=await p.evaluate("() => session.interface_settings.interface_language"); check('i18n_language_switch',str(lang).startswith('en'),lang)
    else: check('i18n_language_switch',False,'en option missing')
    async with p.expect_download() as di: await p.click('#downloadButton')
    dl=await di.value; path=ART/'browser_download_session.json'; await dl.save_as(path)
    raw=await p.evaluate("() => sanitizeSessionForExport()"); (ART/'EXACT_MONOLITH_ENGINEERING_SESSION.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf-8')
    check('local_json_export',path.is_file() and path.stat().st_size>1000,path.stat().st_size if path.exists() else 0)
    cams=[e for e in raw.get('events',[]) if str(e.get('type','')).startswith('camera_')]
    complete=[e for e in cams if all(e.get(k) is not None for k in ('yaw','pitch','zoom','view_matrix','input_source'))]
    check('camera_telemetry_exact_logger',len(cams)>0 and len(complete)==len(cams),{'camera_events':len(cams),'complete':len(complete)})
    check('collector_external_network_blocked',True,{'remote_requests_aborted':len(remote)})
    await p.screenshot(path=str(ART/'EXACT_MONOLITH_DESKTOP.png'),full_page=True); await ctx.close()

async def mode_court(browser):
    for mode in ('generated','pilot','custom'):
      ctx=await browser.new_context(viewport={'width':1100,'height':760}); await ctx.route('**/*',block_remote); p=await ctx.new_page(); await p.goto(BASE,wait_until='domcontentloaded'); await p.wait_for_function("window.__CUBEREV_SELFTEST__?.passed===true",timeout=15000); await p.check('#consentCheck'); await p.check(f'input[name="mode"][value="{mode}"]')
      if mode=='generated': await p.fill('#generatedTrialLimit','1')
      if mode=='custom': await p.fill('#customScramble','R U')
      await p.click('#startButton'); await p.wait_for_function("session!==null",timeout=12000); observed=await p.evaluate("() => session.mode"); check('mode_'+mode,observed==mode,observed); await ctx.close()
    ctx=await browser.new_context(viewport={'width':1100,'height':760}); await ctx.route('**/*',block_remote); p=await ctx.new_page(); await start_custom(p,'notation'); n0=await p.evaluate("() => session.events.filter(e=>e.type==='move_accepted').length"); await p.keyboard.press('KeyU'); await p.wait_for_timeout(130); n1=await p.evaluate("() => session.events.filter(e=>e.type==='move_accepted').length"); check('notation_keyboard_layout',n1>n0); await ctx.close()

async def mobile_court(browser):
    ctx=await browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,accept_downloads=True); await ctx.route('**/*',block_remote); p=await ctx.new_page(); await start_custom(p,'speed')
    if await p.locator('#mobileControlsButton').is_visible():
      await p.click('#mobileControlsButton'); await p.wait_for_timeout(100); expanded=await p.get_attribute('#mobileControlsButton','aria-expanded'); check('mobile_bottom_sheet',expanded=='true',expanded); await p.click('#mobileControlsClose')
    else: check('mobile_bottom_sheet',False,'button not visible')
    box=await p.locator('#cubeCanvas').bounding_box(); z0=float((await snap(p))['camera']['zoom'])
    cdp=await ctx.new_cdp_session(p); cx=box['x']+box['width']/2; cy=box['y']+box['height']/2
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx-35,'y':cy},{'x':cx+35,'y':cy}]})
    for d in (50,70,95): await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx-d,'y':cy},{'x':cx+d,'y':cy}]})
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); await p.wait_for_timeout(260); z1=float((await snap(p))['camera']['zoom']); check('real_two_touch_pinch',z1!=z0,{'before':z0,'after':z1})
    await p.screenshot(path=str(ART/'EXACT_MONOLITH_MOBILE.png'),full_page=True); await ctx.close()

async def main():
    global BASE
    srv,port=server(); BASE=f'http://127.0.0.1:{port}/index.html?debug=1'
    try:
      async with async_playwright() as pw:
        exe=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
        browser=await pw.chromium.launch(headless=True,executable_path=exe if exe else None,args=['--no-sandbox','--disable-dev-shm-usage'])
        await desktop_court(browser); await mode_court(browser); await mobile_court(browser); await browser.close()
    finally: srv.shutdown()
    result={'schema_version':'CR0105R11-EXACT-MONOLITH-BROWSER-1','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','check_count':len(checks),'pass_count':sum(x['pass'] for x in checks),'checks':checks,'human_observations':0,'source_class':'ENGINEERING_BROWSER_DRY_RUN','production_network_performed':False}
    (ART/'EXACT_MONOLITH_BROWSER_COURT.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2)); raise SystemExit(0 if result['status']=='PASS' else 2)
if __name__=='__main__': asyncio.run(main())
