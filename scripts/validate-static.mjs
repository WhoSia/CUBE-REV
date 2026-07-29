import assert from 'node:assert/strict';
import { readFile, access } from 'node:fs/promises';
import { resolve } from 'node:path';
import vm from 'node:vm';

const root = resolve(import.meta.dirname, '..');
const release = Object.freeze({
  version: '0.6.11',
  versionDigits: '0611',
  buildId: '0.6.11-orbit-ui-1',
  cacheKey: '0611-orbit-ui-1',
  archiveHtml: 'CUBE-REV_0.6.11_GitHub_Pages_Pilot.html'
});

const read = path => readFile(resolve(root, path), 'utf8');
const index = await read('index.html');
const archive = await read(release.archiveHtml);
const config = await read('collector-config.js');
const dragController = await read('js/cube-drag-controller.js');
const readme = await read('README.md');
const scripts = [
  'js/i18n-controller.js',
  'js/collector-client.js',
  'js/cube-drag-controller.js',
  'js/camera-zoom-controller.js',
  'js/responsive-layout-controller.js'
];

assert.equal(index, archive, 'index.html and the versioned 0.6.11 HTML must be byte-identical');
assert.match(index, new RegExp(`const VERSION = '${release.version.replaceAll('.', '\\.')}'`));
assert.match(index, new RegExp(`const BUILD_ID = '${release.buildId.replaceAll('.', '\\.')}'`));
assert.match(index, new RegExp(`CUBE-REV-${release.version.replaceAll('.', '\\.')}`));
assert.match(config, new RegExp(`studyId: 'CUBE-REV-${release.version.replaceAll('.', '\\.')}'`));
assert.match(config, new RegExp(`CUBE-REV ${release.version.replaceAll('.', '\\.')}`));
assert.ok(readme.includes(`Current public version: ${release.version}`));
assert.ok(readme.includes(`현재 공개 버전: ${release.version}`));
assert.ok(!readme.includes('collector/google-apps-script/Code.gs'), 'README must describe the current public repository');
assert.ok(!dragController.includes('pitchLimit'), 'camera pitch must remain unrestricted');

const controllerWindow = {};
vm.runInNewContext(dragController, { window: controllerWindow });
let cameraProbe = { yaw: 0, pitch: 0, zoom: 1 };
const controller = new controllerWindow.CubeDragController({
  element: {
    dataset: {},
    style: {},
    getBoundingClientRect: () => ({ left: 0, top: 0 })
  },
  pickSticker: () => null,
  resolveStickerDrag: () => null,
  canTurnFace: () => false,
  applyFaceMove: () => false,
  getCamera: () => ({ ...cameraProbe }),
  setCamera: next => { cameraProbe = { ...cameraProbe, ...next }; },
  setPreview: () => {},
  clearPreview: () => {},
  logEvent: () => {}
});
controller.active = {
  id: 1,
  mode: 'camera',
  start: { x: 0, y: 0 },
  last: { x: 0, y: 0 },
  previous: { x: 0, y: 0 },
  cameraStart: { ...cameraProbe },
  pointerType: 'mouse',
  pathLength: 0,
  sampleCount: 1,
  maxDistance: 0
};
controller.onPointerMove({
  pointerId: 1,
  clientX: 0,
  clientY: 500,
  preventDefault: () => {}
});
assert.ok(cameraProbe.pitch > Math.PI, 'a vertical drag must pass the former U/D pitch limit');

for (const path of scripts) {
  await access(resolve(root, path));
  assert.ok(
    index.includes(`./${path}?v=${release.cacheKey}`),
    `${path} must use the shared ${release.cacheKey} cache key`
  );
  const source = await read(path);
  new Function(source);
}

for (const html of [index, archive]) {
  assert.ok(html.includes(`<meta name="theme-color" content="#080d15">`));
  assert.ok(html.includes(`camera_orbit_policy:'unbounded_yaw_pitch_full_vertical_orbit_v1'`));
}

console.log(`CUBE-REV ${release.version} static validation passed.`);
