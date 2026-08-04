const assert = require("node:assert/strict");
const { existsSync, readFileSync } = require("node:fs");
const { resolve } = require("node:path");
const { spawnSync } = require("node:child_process");

const root = resolve(__dirname, "..");
const read = path => readFileSync(resolve(root, path), "utf8");

const deployment = read("docs/CUBE-REV_0.7.12_DEPLOYMENT.md");
const workflow = read(".github/workflows/validate-static.yml");
const readme = read("README.md");
const historicalDeployment = read("docs/CUBE-REV_0.7.11_DEPLOYMENT.md");

const commandBlock = deployment.match(
  /<!-- validation-cli:start -->\s*```(?:shell|sh)\s*([\s\S]*?)```\s*<!-- validation-cli:end -->/
);
assert.ok(commandBlock, "0.7.12 deployment guide must contain the validation CLI contract block");

const documentedCommands = commandBlock[1]
  .split(/\r?\n/)
  .map(line => line.trim())
  .filter(Boolean);

const workflowCommands = workflow
  .split(/\r?\n/)
  .map(line => line.trim().replace(/^run:\s*/, ""))
  .filter(line => /^(?:node|python)\s+/.test(line));

assert.deepEqual(
  documentedCommands,
  workflowCommands,
  "deployment validation commands must remain identical to the GitHub Actions CLI sequence"
);

for (const command of documentedCommands) {
  const path = command.match(/(?:node\s+|tests\/)([^\s]+\.(?:mjs|cjs|py))\b/)?.[1]
    ?? command.match(/(tests\/[^\s]+\.py)\b/)?.[1];
  assert.ok(path, `unable to identify a repository entry point in: ${command}`);
  const normalized = path.startsWith("tests/") || path.startsWith("scripts/")
    ? path
    : `tests/${path}`;
  assert.ok(existsSync(resolve(root, normalized)), `documented CLI target is missing: ${normalized}`);
}

assert.match(readme, /node scripts\/serve-static\.mjs \[port\]/);
assert.match(readme, /node scripts\/serve-static\.mjs --help/);
assert.match(
  historicalDeployment,
  /Historical record — not a current execution guide/,
  "the 0.7.11 deployment snapshot must not present its old branch procedure as current"
);

const server = resolve(root, "scripts/serve-static.mjs");
const help = spawnSync(process.execPath, [server, "--help"], { encoding: "utf8" });
assert.equal(help.status, 0, help.stderr);
assert.match(help.stdout, /^Usage: node scripts\/serve-static\.mjs \[port\]/);

for (const invalid of ["not-a-port", "0", "65536"]) {
  const result = spawnSync(process.execPath, [server, invalid], { encoding: "utf8" });
  assert.equal(result.status, 2, `invalid port ${invalid} must fail with CLI usage status`);
  assert.match(result.stderr, /port must be one integer between 1 and 65535/);
}

console.log("CUBE-REV documented CLI contract validation passed.");
