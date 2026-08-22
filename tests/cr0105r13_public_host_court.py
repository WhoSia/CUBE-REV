#!/usr/bin/env python3
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ART=Path(os.environ.get('CR0105R13_ARTIFACT_DIR','cr0105r13-artifact')); ART.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('CR0105R13_PUBLIC_URL','https://whosia.github.io/CUBE-REV/?cr0105r13=manual')
async def main():
 log={'url':URL,'console':[],'pageerror':[],'requestfailed':[],'responses':[],'blocked_external':[]}
 async with async_playwright() as pw:
  b=await pw.chromium.launch(headless=True,args=['--no-sandbox'])
  c=await b.new_context()
  p=await c.new_page()
  p.on('console',lambda m:log['console'].append({'type':m.type,'text':m.text}))
  p.on('pageerror',lambda e:log['pageerror'].append(str(e)))
  p.on('requestfailed',lambda r:log['requestfailed'].append({'url':r.url,'failure':r.failure}))
  p.on('response',lambda r:log['responses'].append({'url':r.url,'status':r.status}) if 'whosia.github.io/CUBE-REV/' in r.url else None)
  async def route_handler(route):
   u=route.request.url
   if u.startswith('https://whosia.github.io/CUBE-REV/'):
    await route.continue_()
   else:
    log['blocked_external'].append(u)
    await route.abort()
  await p.route('**/*',route_handler)
  await p.goto(URL,wait_until='domcontentloaded',timeout=45000)
  await p.wait_for_timeout(4500)
  state=await p.evaluate("""() => ({
    title:document.title,
    readyState:document.readyState,
    selftest:window.__CUBEREV_SELFTEST__||null,
    selftestText:document.querySelector('#selfTestStatus')?.textContent||null,
    hasStart:!!document.querySelector('#startButton'),
    telemetryPresent:!!window.CubeRevNaturalisticTelemetry0105R1,
    telemetryVersion:window.CubeRevNaturalisticTelemetry0105R1?.TELEMETRY_VERSION||null
  })""")
  log['state']=state
  checks={
   'ready_complete':state.get('readyState')=='complete',
   'start_present':state.get('hasStart') is True,
   'selftest_passed':bool((state.get('selftest') or {}).get('passed') is True),
   'selftest_100':int((state.get('selftest') or {}).get('check_count') or 0)==100,
   'telemetry_helper_present':state.get('telemetryPresent') is True,
   'telemetry_version_exact':state.get('telemetryVersion')=='CR0105R1-NATURALISTIC-TELEMETRY-1',
   'no_page_errors':len(log['pageerror'])==0,
   'main_document_200':any(x.get('status')==200 and 'whosia.github.io/CUBE-REV/' in x.get('url','') for x in log['responses'])
  }
  log['checks']=checks; log['status']='PASS' if all(checks.values()) else 'HOLD'
  await b.close()
 (ART/'PUBLIC_HOST_BROWSER_COURT.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
 print(json.dumps(log,indent=2))
 raise SystemExit(0 if log['status']=='PASS' else 2)
if __name__=='__main__': asyncio.run(main())
