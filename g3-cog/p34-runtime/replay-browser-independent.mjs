/*
 * G3-P34-R2.  A Playwright-independent semantic replay for the frozen P34
 * bank.  This deliberately calls the canonical state adapter for every
 * transition: it does not import Lane A's generated move-permutation table
 * and it makes no DOM, pixel, or browser claim.
 */
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { applySequence, equalState, serializeState, solvedState } from '../state-adapter.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const AUTH = 'G3-P34-AUTH-v1';
const SALT = 'CUBE-REV-G3-P34-AUTH-v1';
const MOVES = ['U', "U'", 'D', "D'", 'L', "L'", 'R', "R'", 'F', "F'", 'B', "B'"];
const FAMILIES = [['R', 'L'], ['U', 'D'], ['F', 'B']];
const ORIENTATION = 'CANONICAL_IDENTITY';
const sha = (value) => createHash('sha256').update(value, 'utf8').digest('hex');
const stateSha = (state) => sha(serializeState(state));
const face = (token) => token[0];
const inverseToken = (token) => token.endsWith("'") ? token[0] : `${token[0]}'`;
const inverseWord = (word) => [...word].reverse().map(inverseToken);
const sameJson = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const moveMultiset = (word) => Object.fromEntries(MOVES.map((move) => [move, word.filter((token) => token === move).length]));

function enumerateWords(length) {
  const out = [];
  const walk = (prefix) => {
    if (prefix.length === length) { out.push(prefix); return; }
    for (const token of MOVES) if (!prefix.length || face(prefix.at(-1)) !== face(token)) walk([...prefix, token]);
  };
  walk([]);
  return out;
}

function selectWords(kind, length, count) {
  return enumerateWords(length)
    .map((tokens) => ({ tokens, word: tokens.join(' '), selection_sha256: sha(`${SALT}|${kind}|${length}|${tokens.join(' ')}`) }))
    .sort((a, b) => a.selection_sha256.localeCompare(b.selection_sha256) || a.word.localeCompare(b.word))
    .slice(0, count);
}

function selectTopRankedWords(kind, length, limit) {
  // The binding rule is total SHA-then-lexical order.  Keeping a bounded
  // ordered frontier yields its leading entries without materializing the
  // 1.9M length-six word list.
  const frontier = [];
  const insert = (entry) => {
    let lo = 0, hi = frontier.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      const order = frontier[mid].selection_sha256.localeCompare(entry.selection_sha256) || frontier[mid].word.localeCompare(entry.word);
      if (order <= 0) lo = mid + 1; else hi = mid;
    }
    if (lo >= limit && frontier.length >= limit) return;
    frontier.splice(lo, 0, entry);
    if (frontier.length > limit) frontier.pop();
  };
  const walk = (prefix) => {
    if (prefix.length === length) {
      const word = prefix.join(' ');
      insert({ tokens: [...prefix], word, selection_sha256: sha(`${SALT}|${kind}|${length}|${word}`) });
      return;
    }
    for (const token of MOVES) if (!prefix.length || face(prefix.at(-1)) !== face(token)) walk([...prefix, token]);
  };
  walk([]);
  return frontier;
}

function selectStarts() {
  const starts = [];
  for (const length of [4, 6]) {
    const ranked = selectTopRankedWords('START', length, 64);
    const seen = new Set();
    let rank = 0;
    for (const entry of ranked) {
      const state = applySequence(solvedState(), entry.tokens);
      const stateBytes = serializeState(state);
      if (seen.has(stateBytes)) continue;
      seen.add(stateBytes);
      starts.push({ id: `START-d${length}-${String(rank).padStart(2, '0')}`, stratum_length: length, rank,
        scramble: entry.tokens, scramble_string: entry.word, selection_sha256: entry.selection_sha256,
        state_sha256: sha(stateBytes), state_bytes: stateBytes, state });
      rank += 1;
      if (rank === 8) break;
    }
    if (rank !== 8) throw new Error(`START_STATE_TABLE_FAIL:d${length}:${rank}`);
  }
  return starts;
}

function relationCores() {
  const cores = [];
  for (const [familyIndex, [first, second]] of FAMILIES.entries()) {
    const outside = ['U', 'D', 'L', 'R', 'F', 'B'].filter((faceName) => faceName !== first && faceName !== second);
    for (const a of [first, `${first}'`]) for (const b of [second, `${second}'`]) for (const cFace of outside) for (const c of [cFace, `${cFace}'`]) {
      cores.push({ id: `CORE-${String(cores.length).padStart(3, '0')}`, family_index: familyIndex, family: `${first}/${second}`,
        a, b, c, order_A: [a, b, c], order_B: [b, a, c] });
    }
  }
  if (cores.length !== 96) throw new Error(`CORE_TABLE_FAIL:${cores.length}`);
  return cores;
}

function locallyAdmissible(word) { return word.every((token, index) => MOVES.includes(token) && (!index || face(word[index - 1]) !== face(token))); }
function duplicateKey(startBytes, terminalBytes, family, pathA, pathB) { return JSON.stringify([startBytes, terminalBytes, family, [pathA, pathB].sort(), ORIENTATION]); }
function alternativeReturn(inverse) {
  const token = MOVES.find((candidate) => face(candidate) !== face(inverse.at(-1) ?? 'X')) ?? 'U';
  return [...inverse, token, inverseToken(token)];
}
function findNegativeMove(terminal, start) {
  for (const token of MOVES) if (!equalState(applySequence(terminal, [token]), start)) return [token];
  throw new Error('SCORING_FAIL:NO_G_NEGATIVE');
}
function assert(condition, message) { if (!condition) throw new Error(message); }

const bankBytes = readFileSync(join(HERE, 'p34-bank.json'));
const bank = JSON.parse(bankBytes);
const laneAReceipt = JSON.parse(readFileSync(join(HERE, 'p34-receipt.json'), 'utf8'));
const failures = [];
const mismatch = (code, detail) => failures.push({ code, detail });
const starts = selectStarts();
const prefixes = [
  ...selectWords('PREFIX', 2, 8).map((entry, rank) => ({ ...entry, id: `PREFIX-p2-${String(rank).padStart(2, '0')}`, stratum_length: 2, rank })),
  ...selectWords('PREFIX', 3, 8).map((entry, rank) => ({ ...entry, id: `PREFIX-p3-${String(rank).padStart(2, '0')}`, stratum_length: 3, rank })),
];
const suffixes = [
  ...selectWords('SUFFIX', 1, 4).map((entry, rank) => ({ ...entry, id: `SUFFIX-s1-${String(rank).padStart(2, '0')}`, stratum_length: 1, rank })),
  ...selectWords('SUFFIX', 2, 4).map((entry, rank) => ({ ...entry, id: `SUFFIX-s2-${String(rank).padStart(2, '0')}`, stratum_length: 2, rank })),
];
const cores = relationCores();

// Freeze reconciliation: selected authority must be reproduced before rows are read.
assert(bank.authority.version === AUTH, 'AUTH_VERSION_MISMATCH');
assert(sameJson(bank.authority.move_alphabet, MOVES), 'MOVE_ORDER_MISMATCH');
assert(sameJson(bank.authority.starts, starts.map(({ state, state_bytes, ...entry }) => entry)), 'START_DOMAIN_MISMATCH');
assert(sameJson(bank.authority.prefixes, prefixes.map(({ tokens, ...entry }) => entry)), 'PREFIX_DOMAIN_MISMATCH');
assert(sameJson(bank.authority.suffixes, suffixes.map(({ tokens, ...entry }) => entry)), 'SUFFIX_DOMAIN_MISMATCH');
assert(sameJson(bank.authority.cores, cores), 'CORE_DOMAIN_MISMATCH');

const exclusionReasons = Object.fromEntries(Object.keys(laneAReceipt.census.exclusion_reasons).map((key) => [key, 0]));
const startById = new Map(starts.map((entry) => [entry.id, entry]));
const prefixById = new Map(prefixes.map((entry) => [entry.id, entry]));
const suffixById = new Map(suffixes.map((entry) => [entry.id, entry]));
const coreById = new Map(cores.map((entry) => [entry.id, entry]));
const laneAKeys = new Set();
for (const source of bank.rows) {
  const start = startById.get(source.start_id);
  assert(start, `UNKNOWN_START:${source.start_id}`);
  const terminal = applySequence(start.state, source.word_A.split(' '));
  laneAKeys.add(duplicateKey(start.state_bytes, serializeState(terminal), source.relation_family, source.word_A, source.word_B));
}
let candidates = 0;
let admittedPreDuplicate = 0;
let admittedFinal = 0;
for (const start of starts) for (const prefix of prefixes) for (const core of cores) for (const suffix of suffixes) {
  candidates += 1;
  const reasons = [];
  if (face(prefix.tokens.at(-1)) === face(core.order_A[0])) reasons.push('SAME_FACE_P_CORE_A');
  if (face(prefix.tokens.at(-1)) === face(core.order_B[0])) reasons.push('SAME_FACE_P_CORE_B');
  if (face(core.c) === face(suffix.tokens[0])) reasons.push('SAME_FACE_CORE_S');
  const wordA = [...prefix.tokens, ...core.order_A, ...suffix.tokens];
  const wordB = [...prefix.tokens, ...core.order_B, ...suffix.tokens];
  if (!locallyAdmissible(wordA)) reasons.push('ILLEGAL_A');
  if (!locallyAdmissible(wordB)) reasons.push('ILLEGAL_B');
  if (wordA.length !== wordB.length) reasons.push('LENGTH_MISMATCH');
  if (!sameJson(moveMultiset(wordA), moveMultiset(wordB))) reasons.push('MOVE_MULTISET_MISMATCH');
  const invA = inverseWord(wordA), invB = inverseWord(wordB);
  if (invA.join(' ') === invB.join(' ')) reasons.push('INVERSE_TARGET_IDENTITY');
  const terminalA = applySequence(start.state, wordA), terminalB = applySequence(start.state, wordB);
  if (!equalState(terminalA, terminalB)) reasons.push('ENDPOINT_MISMATCH');
  if (stateSha(start.state) !== start.state_sha256) reasons.push('START_AUTHORITY_MISMATCH');
  const uniqueReasons = [...new Set(reasons)];
  if (uniqueReasons.length) { for (const reason of uniqueReasons) exclusionReasons[reason] += 1; continue; }
  admittedPreDuplicate += 1;
  const terminalBytes = serializeState(terminalA), pathA = wordA.join(' '), pathB = wordB.join(' ');
  const key = duplicateKey(start.state_bytes, terminalBytes, core.family, pathA, pathB);
  if (!laneAKeys.delete(key)) mismatch('ENUMERATION_DOMAIN_MISMATCH', { start_id: start.id, relation_core_id: core.id, prefix_id: prefix.id, suffix_id: suffix.id });
  admittedFinal += 1;
}
if (laneAKeys.size) mismatch('LANE_A_ROW_NOT_REGENERATED', { remaining_keys: laneAKeys.size });

const control = Object.fromEntries(['S_positive', 'R_positive', 'R_negative_cross', 'R_negative_alternative', 'G_positive', 'G_negative'].map((name) => [name, { pass: 0, fail: 0 }]));
const familyCounters = new Map();
const terminalHashes = new Set();
for (let index = 0; index < bank.rows.length; index += 1) {
  const source = bank.rows[index];
  const start = startById.get(source.start_id), prefix = prefixById.get(source.prefix_id), suffix = suffixById.get(source.suffix_id), core = coreById.get(source.relation_core_id);
  if (!start || !prefix || !suffix || !core) { mismatch('ROW_AUTHORITY_LOOKUP_FAIL', { index, item_id: source.item_id }); continue; }
  const wordA = source.word_A.split(' '), wordB = source.word_B.split(' '), invA = inverseWord(wordA), invB = inverseWord(wordB);
  const terminalA = applySequence(start.state, wordA), terminalB = applySequence(start.state, wordB), terminalBytes = serializeState(terminalA);
  terminalHashes.add(sha(terminalBytes));
  const familyIndex = familyCounters.get(core.family) ?? 0;
  familyCounters.set(core.family, familyIndex + 1);
  const expected = {
    item_id: `P34-${String(index).padStart(6, '0')}`,
    start_id: start.id, start_state_sha256: start.state_sha256, terminal_state_sha256: sha(terminalBytes),
    relation_family: core.family, relation_core_id: core.id, prefix_id: prefix.id, suffix_id: suffix.id,
    prefix: prefix.word, suffix: suffix.word, word_A: wordA.join(' '), word_B: wordB.join(' '),
    inv_A: invA.join(' '), inv_B: invB.join(' '), displayed_length: wordA.length,
    move_multiset: moveMultiset(wordA), canonical_orientation: ORIENTATION,
    duplicate_key_sha256: sha(duplicateKey(start.state_bytes, terminalBytes, core.family, wordA.join(' '), wordB.join(' '))),
    trained_macro_order: familyIndex % 2 === 0 ? 'A' : 'B',
  };
  for (const [field, value] of Object.entries(expected)) if (!sameJson(source?.[field], value)) mismatch('ROW_FIELD_MISMATCH', { index, item_id: expected.item_id, field, expected: value, observed: source?.[field] });
  // Each result is recomputed from canonical adapter calls, independent of Lane A's acceleration table.
  const cases = [
    ['S_positive', equalState(terminalA, terminalB)], ['S_positive', sha(terminalBytes) === source.terminal_state_sha256],
    ['R_positive', equalState(applySequence(terminalA, invA), start.state)], ['R_positive', equalState(applySequence(terminalB, invB), start.state)],
    ['R_negative_cross', invA.join(' ') !== invB.join(' ') && equalState(applySequence(terminalA, invB), start.state)], ['R_negative_cross', invA.join(' ') !== invB.join(' ') && equalState(applySequence(terminalB, invA), start.state)],
    ['R_negative_alternative', equalState(applySequence(terminalA, alternativeReturn(invA)), start.state)], ['R_negative_alternative', equalState(applySequence(terminalB, alternativeReturn(invB)), start.state)],
    ['G_positive', equalState(applySequence(terminalA, invA), start.state)], ['G_positive', equalState(applySequence(terminalB, invB), start.state)],
    ['G_negative', !equalState(applySequence(terminalA, findNegativeMove(terminalA, start.state)), start.state)], ['G_negative', !equalState(applySequence(terminalB, findNegativeMove(terminalB, start.state)), start.state)],
  ];
  for (const [name, pass] of cases) { control[name][pass ? 'pass' : 'fail'] += 1; if (!pass) mismatch('FIXTURE_FAIL', { index, item_id: expected.item_id, control: name }); }
}

const laneACensus = laneAReceipt.census;
const census = {
  candidate_count: candidates,
  excluded_pre_duplicate: candidates - admittedPreDuplicate,
  exclusion_reasons: exclusionReasons,
  admitted_pre_duplicate: admittedPreDuplicate,
  duplicate_removed: admittedPreDuplicate - admittedFinal,
  admitted_final: admittedFinal,
  unique_start_state_hashes: new Set(bank.rows.map((row) => row.start_state_sha256)).size,
  unique_terminal_state_hashes: terminalHashes.size,
  family_counts: Object.fromEntries(FAMILIES.map(([first, second]) => {
    const family = `${first}/${second}`;
    return [family, familyCounters.get(family) ?? 0];
  })),
  distance_counts: Object.fromEntries([...new Set(bank.rows.map((row) => row.terminal_to_origin_qtm))].sort((a, b) => a - b).map((distance) => [distance, bank.rows.filter((row) => row.terminal_to_origin_qtm === distance).length])),
};
for (const [field, value] of Object.entries(census)) if (!sameJson(laneACensus[field], value)) mismatch('CENSUS_MISMATCH', { field, expected: value, observed: laneACensus[field] });
for (const [name, result] of Object.entries(control)) if (!sameJson(laneAReceipt.synthetic_controls[name], result)) mismatch('FIXTURE_CENSUS_MISMATCH', { name, expected: result, observed: laneAReceipt.synthetic_controls[name] });
if (sha(bankBytes) !== laneAReceipt.bank_json_sha256) mismatch('BANK_HASH_MISMATCH', { expected: laneAReceipt.bank_json_sha256, observed: sha(bankBytes) });

const receipt = {
  schema: 'CUBE-REV-G3-P34-R2-PLAYWRIGHT-INDEPENDENT-REPLAY-v1',
  authority: AUTH,
  method: 'CANONICAL_STATE_ADAPTER_DIRECT_REPLAY_NO_PLAYWRIGHT_NO_DOM_NO_PIXEL_CLAIM',
  node: process.version,
  input_hashes: {
    lane_a_bank_json_sha256: sha(bankBytes), lane_a_compiler_sha256: laneAReceipt.build.compiler_sha256,
    state_adapter_sha256: sha(readFileSync(join(HERE, '..', 'state-adapter.js'), 'utf8')),
    replay_script_sha256: sha(readFileSync(fileURLToPath(import.meta.url), 'utf8')),
  },
  semantic_parity: { move_order: sameJson(bank.authority.move_alphabet, MOVES), enumeration_authority: failures.every((entry) => !['START_DOMAIN_MISMATCH', 'PREFIX_DOMAIN_MISMATCH', 'SUFFIX_DOMAIN_MISMATCH', 'CORE_DOMAIN_MISMATCH'].includes(entry.code)), row_field_mismatches: failures.filter((entry) => entry.code === 'ROW_FIELD_MISMATCH').length, terminal_hashes: true, census: sameJson(laneACensus, census), fixture_outputs: sameJson(laneAReceipt.synthetic_controls, control) },
  census, synthetic_controls: control, residual_failures: failures,
  browser_dependency: failures.length ? 'HOLD_RETAINED' : 'CLOSED_FOR_SEMANTIC_REPLAY_ONLY',
  render_scope: 'NOT_EXECUTED_NO_DOM_OR_PIXEL_PARITY_CLAIM',
  p35_gate: failures.length ? 'NOT_AUTHORIZED' : 'AUTHORIZED_BY_EXACT_CROSS_LANE_SEMANTIC_EQUIVALENCE_ONLY',
  verdict: failures.length ? 'REPLAY_EQUIVALENCE_HOLD' : 'EXACT_CROSS_LANE_SEMANTIC_EQUIVALENCE_PASS',
};
writeFileSync(join(HERE, 'p34-r2-replay-receipt.json'), `${JSON.stringify(receipt, null, 2)}\n`);
console.log(JSON.stringify(receipt, null, 2));
