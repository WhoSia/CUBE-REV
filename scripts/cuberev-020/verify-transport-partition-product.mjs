#!/usr/bin/env node
/** CUBE-REV 0.20 — independent finite transporter×partition witness.
 * This is a reversible toy transducer, NOT an original cube physical map.
 * Pure JS (no packages), falsifies unsound prefix-partition-only quotienting.
 */
import assert from 'node:assert/strict';

const S = Object.freeze([0, 1, 2, 3]);
const MOVES = Object.freeze({
  F: { sigma: [1, 0, 2, 3], cut: [0, 1] },
  P: { sigma: [0, 2, 1, 3], cut: [] },
  Q: { sigma: [0, 1, 3, 2], cut: [2] },
});
const sortCells = cells => cells.sort((a, b) => a[0] - b[0]);
function normalizePartition(traces) {
  const fibers = new Map();
  traces.forEach((trace, state) => {
    const key = trace.join('');
    if (!fibers.has(key)) fibers.set(key, []);
    fibers.get(key).push(state);
  });
  return sortCells([...fibers.values()]);
}
function initial() { return { perm: [...S], parts: [[...S]] }; }
function advance(state, action) {
  const {sigma, cut} = MOVES[action];
  const pulledCut = new Set(S.filter(s => cut.includes(state.perm[s])));
  const parts = [];
  for (const cell of state.parts) {
    const yes = cell.filter(s => pulledCut.has(s));
    const no = cell.filter(s => !pulledCut.has(s));
    if (yes.length) parts.push(yes);
    if (no.length) parts.push(no);
  }
  return {perm: S.map(s => sigma[state.perm[s]]), parts: sortCells(parts)};
}
function directReplay(word) {
  const pos = [...S], bit = S.map(() => 0), traces = S.map(() => []);
  for (const a of word) {
    const {sigma, cut} = MOVES[a];
    for (const s of S) {
      bit[s] ^= Number(cut.includes(pos[s]));
      traces[s].push(bit[s]);
      pos[s] = sigma[pos[s]];
    }
  }
  return {perm: pos, parts: normalizePartition(traces)};
}
function audit(maxLength = 6) {
  const alphabet = Object.keys(MOVES);
  const census = [];
  let total = 0;
  for (let length = 0; length <= maxLength; length++) {
    let words = [[]];
    for (let i = 0; i < length; i++) words = words.flatMap(w => alphabet.map(a => [...w, a]));
    const visited = new Set();
    for (const word of words) {
      let state = initial();
      for (const a of word) state = advance(state, a);
      assert.deepEqual(state, directReplay(word), 'DP and physical replay disagree');
      visited.add(JSON.stringify(state));
      total++;
    }
    census.push({length, realWords: words.length, quotientStates: visited.size,
      maxRank: Math.max(...[...visited].map(x => JSON.parse(x).parts.length))});
  }
  const ff = advance(advance(initial(), 'F'), 'F');
  const fp = advance(advance(initial(), 'F'), 'P');
  assert.deepEqual(ff.parts, fp.parts);
  assert.notDeepEqual(ff.perm, fp.perm);
  const fff = advance(ff, 'F'), fpf = advance(fp, 'F');
  assert.equal(fff.parts.length, 2);
  assert.equal(fpf.parts.length, 4);
  return {result: 'CUBE_REV_020_TRANSPORTER_PRODUCT_FINITE_COUNTERMODEL_PASS',
    exhaustiveWordsChecked: total, census, samePartitionPrefixes: ['FF', 'FP'],
    samePrefixPartition: ff.parts, distinctTransporters: [ff.perm, fp.perm],
    nextFTranscriptRank: [fff.parts.length, fpf.parts.length],
    proofScope: 'four-position synthetic reversible transducer, not cube physical data'};
}
const result = audit();
console.log(JSON.stringify(result, null, 2));
