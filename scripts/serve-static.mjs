import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize, resolve, sep } from "node:path";

const root = resolve(import.meta.dirname, "..");
const port = Number(process.argv[2]) || 4173;
const types = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".md": "text/markdown; charset=utf-8"
};

createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, `http://${request.headers.host}`).pathname);
    const relative = normalize(pathname === "/" ? "index.html" : pathname.replace(/^\/+/, ""));
    const target = resolve(join(root, relative));
    if (target !== root && !target.startsWith(root + sep)) throw new Error("path outside root");
    const info = await stat(target);
    const file = info.isDirectory() ? join(target, "index.html") : target;
    response.writeHead(200, {
      "content-type": types[extname(file)] || "application/octet-stream",
      "cache-control": "no-store"
    });
    response.end(await readFile(file));
  } catch (error) {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("Not found");
  }
}).listen(port, "127.0.0.1", () => {
  console.log(`CUBE-REV static server: http://127.0.0.1:${port}`);
});
