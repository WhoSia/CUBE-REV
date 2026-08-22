#!/usr/bin/env python3
import asyncio,json,os,shutil,socket,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]; ART=Path(os.environ.get('CR0105R11_ARTIFACT_DIR','cr0105r11-artifact')); ART.mkdir(exist_ok=True)
class Q(SimpleHTTPRequestHandler):
 def log_message(self,*a): pass
def port():
 s=socket.socket();s.bind(('127.0.0.1',0));p=s.getsockname()[1];s.close();return p
async def main():
 p0=port();srv=ThreadingHTTPServer(('127.0.0.1',p0),lambda *a,**k:Q(*a,directory=str(ROOT),**k));threading.Thread(target=srv.serve_forever,daemon=True).start()
 log={'console':[],'pageerror':[],'requestfailed':[],'responses':[]}
 try:
  async with async_playwright() as pw:
   b=await pw.chromium.launch(headless=True,args=['--no-sandbox']);c=await b.new_context();p=await c.new_page()
   p.on('console',lambda m:log['console'].append({'type':m.type,'text':m.text}))
   p.on('pageerror',lambda e:log['pageerror'].append(str(e)))
   p.on('requestfailed',lambda r:log['requestfailed'].append({'url':r.url,'failure':r.failure}))
   p.on('response',lambda r:log['responses'].append({'url':r.url,'status':r.status}) if '127.0.0.1' in r.url else None)
   await p.route('**/*',lambda route: route.continue_() if route.request.url.startswith('http://127.0.0.1:') else route.abort())
   await p.goto(f'http://127.0.0.1:{p0}/index.html?debug=1',wait_until='domcontentloaded',timeout=30000);await p.wait_for_timeout(3500)
   log['state']=await p.evaluate("() => ({title:document.title,selftest:window.__CUBEREV_SELFTEST__||null,status:document.querySelector('#selfTestStatus')?.textContent||null,hasStart:!!document.querySelector('#startButton'),readyState:document.readyState})")
   await b.close()
 finally:srv.shutdown()
 (ART/'BOOT_DIAGNOSTIC.json').write_text(json.dumps(log,indent=2),encoding='utf-8');print(json.dumps(log,indent=2))
if __name__=='__main__':asyncio.run(main())
