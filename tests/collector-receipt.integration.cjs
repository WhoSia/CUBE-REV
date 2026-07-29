"use strict";

const assert = require("node:assert/strict");

const messageListeners = new Set();
const fakeWindow = {
  addEventListener(type, listener) {
    if (type === "message") messageListeners.add(listener);
  },
  removeEventListener(type, listener) {
    if (type === "message") messageListeners.delete(listener);
  },
  open() { return {}; }
};

function element(tag) {
  return {
    tagName: tag.toUpperCase(),
    children: [],
    style: {},
    dataset: {},
    appendChild(child) { this.children.push(child); return child; },
    setAttribute() {},
    remove() {},
    submit() {
      const fields = Object.fromEntries(this.children.map((child) => [child.name, child.value]));
      const receipt = {
        type: "CUBE_REV_COLLECTOR_ACK",
        ok: true,
        status: "stored",
        submission_nonce: fields.submission_nonce,
        session_id: fields.session_id,
        checksum_fnv1a32: fields.checksum_fnv1a32,
        receipt_code: "TEST-RECEIPT",
        file_name: `${fields.session_id}.json`,
      };
      queueMicrotask(() => {
        for (const listener of messageListeners) listener({ data: receipt });
      });
    }
  };
}

global.window = fakeWindow;
global.document = {
  createElement: element,
  body: { appendChild() {} },
  head: {
    appendChild(script) {
      const url = new URL(script.src);
      const callback = url.searchParams.get("callback");
      queueMicrotask(() => fakeWindow[callback]({
        type: "CUBE_REV_COLLECTOR_HEALTH",
        ok: true,
        expected_version: "0.6.11",
        collector_id: "CUBE-REV-0611-MAIN",
        protocol_version: "receipt-v2",
        receipt_confirmation_available: true,
        deployment_id: "integration-test"
      }));
    }
  }
};

require("../js/collector-client.js");
const Client = fakeWindow.CubeRevCollectorClient;
const session = { project: "CUBE-REV", version: "0.6.11", session_id: "CR-INTEGRATION", data_submission: {} };
const events = [];
const statuses = [];
const hashString = (text) => {
  let hash = 0x811c9dc5;
  for (const ch of text) {
    hash ^= ch.charCodeAt(0);
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash >>> 0;
};
const config = Client.normalizeConfig({
  enabled: true,
  endpoint: "https://script.google.com/macros/s/TEST/exec",
  manualUploadUrl: "https://script.google.com/macros/s/TEST/exec",
  studyId: "CUBE-REV-0.6.11",
  collectorId: "CUBE-REV-0611-MAIN",
  protocolVersion: "receipt-v2",
  gzipWhenAvailable: false,
  timeoutMs: 30000,
  receiptPollIntervalMs: 700,
  healthCheckTimeoutMs: 5000
}, "0.6.11");
const client = new Client({
  config,
  version: "0.6.11",
  getSession: () => session,
  exportSession: () => session,
  logEvent: (type, extra) => events.push({ type, ...extra }),
  persist: () => {},
  setStatus: (message, kind, options) => statuses.push({ message, kind, options }),
  randomHex: () => "00112233445566778899aabb",
  hashString,
  translate: (key) => key
});

(async () => {
  const health = await client.checkHealth();
  assert.equal(health.expected_version, "0.6.11");
  const receipt = await client.submit();
  assert.equal(receipt.status, "stored");
  assert.equal(receipt.checksum_verified, true);
  assert.equal(session.data_submission.status, "received");
  assert.equal(session.data_submission.receipt_confirmed, true);
  assert.equal(session.data_submission.response_verification, "collector_receipt");
  assert.ok(events.some((event) => event.type === "collector_health_confirmed"));
  assert.ok(events.some((event) => event.type === "submission_receipt_confirmed"));
  assert.ok(statuses.some((status) => status.kind === "success" && status.options.confirmed === true));

  const locked = Client.normalizeConfig({ enabled: false, endpoint: "" }, "0.6.11");
  const lockedClient = new Client({ ...client, config: locked });
  assert.equal(lockedClient.isAutomaticConfigured(), false);
  console.log("CUBE-REV collector receipt integration test passed.");
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
