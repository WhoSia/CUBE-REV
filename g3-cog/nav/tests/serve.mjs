import http from 'node:http';
import {readFile} from 'node:fs/promises';
import {extname,join,normalize} from 'node:path';
const root='g3-cog/nav',port=4174;
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8'};
const server=http.createServer(async(req,res)=>{
  try{
    const u=new URL(req.url,'http://localhost');let p=u.pathname==='/'?'index.html':u.pathname.slice(1);p=normalize(p).replace(/^\.\.(\/|\\)/,'');
    const b=await readFile(join(root,p));res.writeHead(200,{'content-type':mime[extname(p)]||'application/octet-stream','cache-control':'no-store'});res.end(b);
  }catch{res.writeHead(404);res.end('not found');}
});
server.listen(port,'0.0.0.0',()=>console.log(`NAV_SERVER http://127.0.0.1:${port}`));
