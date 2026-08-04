import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize, resolve, sep } from "node:path";

const root = resolve(import.meta.dirname, "..");
const args = process.argv.slice(2);

function printUsage(stream = process.stdout) {
  stream.write([
    "Usage: node scripts/serve-static.mjs [port]",
    "",
    "Serve the repository root on 127.0.0.1 (default port: 4173).",
    ""
  ].join("\n"));
}

if (args.includes("--help") || args.includes("-h")) {
  printUsage();
  process.exit(0);
}

if (args.length > 1 || (args.length === 1 && !/^\d+$/.test(args[0]))) {
  printUsage(process.stderr);
  process.stderr.write("error: port must be one integer between 1 and 65535\n");
  process.exit(2);
}

const port = args.length === 0 ? 4173 : Number(args[0]);
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  printUsage(process.stderr);
  process.stderr.write("error: port must be one integer between 1 and 65535\n");
  process.exit(2);
}
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
