// CUBE-REV 0.23 P3-R3 — exact robust observation court.
// Input: preserved 62 physical full-cubie/9-sticker face fixture from P3-R1B.
// Claim: finite code geometry, not a human-error rate or full-cube replay.
import fs from "node:fs";
import assert from "node:assert/strict";
const fixture = "data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv";
const lines = fs.readFileSync(fixture, "utf8").trim().split(/\r?\n/);
assert.equal(lines.shift(), "index,U,R,F,D,L,B,source_HTM,cubie_sha256");
assert.equal(lines.length, 62);
const rows = lines.map((line, i) => {
  const c = line.split(",");
  assert.equal(c.length, 9);
  assert.equal(Number(c[0]), i);
  assert.ok(Number.isInteger(+c[7]) && +c[7] >= 0 && +c[7] <= 5);
  assert.match(c[8], /^[a-f0-9]{64}$/);
  const face = c.slice(1, 7);
  assert.ok(face.every(s => s.length === 9 && /^[URFDLB]+$/.test(s)));
  const counts = Object.fromEntries("URFDLB".split("").map(f => [f, 0]));
  for (const f of face.join("")) counts[f]++;
  assert.ok(Object.values(counts).every(n => n === 9));
  return { face, digest: c[8] };
});
assert.equal(new Set(rows.map(r => r.digest)).size, 62);
assert.equal(new Set(rows.map(r => r.face.join(""))).size, 62);
const dist = (i, j, mask = 63) => {
  let n = 0;
  for (let f = 0; f < 6; f++) if ((mask & (1 << f)) && rows[i].face[f] !== rows[j].face[f]) n++;
  return n;
};
const hist = Array(7).fill(0), best = Array(7).fill(0), erasureMasks = [];
const adj = Array(62).fill(0n);
for (let mask = 0; mask < 64; mask++) {
  let minDist = 7;
  for (let i = 0; i < 62; i++) for (let j = i + 1; j < 62; j++) {
    const d = dist(i, j, mask);
    minDist = Math.min(minDist, d);
    if (mask === 63) {
      hist[d]++;
      if (d <= 2) {
        adj[i] |= 1n << BigInt(j);
        adj[j] |= 1n << BigInt(i);
      }
    }
  }
  const q = mask.toString(2).replaceAll("0", "").length;
  best[q] = Math.max(best[q], minDist);
  if (minDist >= 2) erasureMasks.push(mask);
}
assert.deepEqual(hist, [0, 0, 142, 216, 390, 400, 743]);
assert.deepEqual(best, [0, 0, 0, 0, 1, 1, 2]);
assert.deepEqual(erasureMasks, [63]);
const pop = n => { let v = 0; while (n) { n &= n - 1n; v++; } return v; };
// Exact min vertex cover on each connected component, independently of
// the C++ maximum-independent-set branch-and-bound implementation.
let unseen = (1n << 62n) - 1n, coverTotal = 0;
const sizes = [];
while (unseen) {
  const root = Array.from({length: 62}, (_,i)=>i).find(i => (unseen & (1n << BigInt(i))) !== 0n);
  let group = 1n << BigInt(root), old;
  do {
    old = group;
    for (let i = 0; i < 62; i++) if (group & (1n << BigInt(i))) group |= adj[i];
  } while (group !== old);
  unseen &= ~group;
  const vertices = Array.from({length: 62}, (_,i)=>i).filter(i => (group & (1n << BigInt(i))) !== 0n);
  sizes.push(vertices.length);
  assert.ok(vertices.length <= 23);
  const edge = vertices.map(u => vertices.reduce((m, v, j) => m | ((adj[u] & (1n << BigInt(v))) ? 1n << BigInt(j) : 0n), 0n));
  const memo = new Map();
  function vertexCover(mask) {
    if (memo.has(mask)) return memo.get(mask);
    let p = -1, deg = 0;
    for (let i = 0; i < edge.length; i++) if (mask & (1n << BigInt(i))) {
      const d = pop(edge[i] & mask);
      if (d > deg) { p = i; deg = d; }
    }
    if (p < 0) return 0;
    const q = edge.findIndex((_, i) => (edge[p] & mask & (1n << BigInt(i))) !== 0n);
    const result = 1 + Math.min(
      vertexCover(mask & ~(1n << BigInt(p))),
      vertexCover(mask & ~(1n << BigInt(q)))
    );
    memo.set(mask, result);
    return result;
  }
  coverTotal += vertexCover((1n << BigInt(vertices.length)) - 1n);
}
assert.equal(62 - coverTotal, 26);
assert.equal(hist.reduce((a,b)=>a+b,0), 1891);
// Full exact adaptive policy game: one located adversarial erasure, with
// each of six physical faces queryable at most once; state-mask DP has all
// source states and every possible observed face-symbol partition.
const ALL = (1n << 62n) - 1n;
function adaptiveErasure(q) {
  const memo = new Map();
  function win(mask, used, remaining, erasures) {
    if (pop(mask) === 1) return true;
    if (remaining === 0) return false;
    const key = [mask.toString(), used, remaining, erasures].join(":");
    if (memo.has(key)) return memo.get(key);
    for (let f = 0; f < 6; f++) {
      if (used & (1 << f)) continue;
      const nextUsed = used | (1 << f);
      // Worst-case first branch: the current face is erased, with location known.
      if (erasures && !win(mask, nextUsed, remaining - 1, 0)) continue;
      const parts = new Map();
      for (let i = 0; i < 62; i++) if (mask & (1n << BigInt(i))) {
        const pattern = rows[i].face[f];
        parts.set(pattern, (parts.get(pattern) || 0n) | (1n << BigInt(i)));
      }
      if (parts.size === 1) continue;
      if ([...parts.values()].every(part => win(part, nextUsed, remaining - 1, erasures))) {
        memo.set(key, true);
        return true;
      }
    }
    memo.set(key, false);
    return false;
  }
  return win(ALL, 0, q, 1);
}
const adaptiveLocatedErasure = Array.from({length: 7}, (_, q) => adaptiveErasure(q));
assert.deepEqual(adaptiveLocatedErasure, [false,false,false,false,false,false,true]);
console.log(JSON.stringify({
  status: "PASS_FINITE_FACE_CODE_ONLY",
  source: fixture, human_process: "NOT_IDENTIFIED",
  states:62, pairs:1891, distance_histogram:hist,
  maximum_min_distance_by_face_budget:best,
  exact_fixed_one_erasure_robust_masks:erasureMasks,
  one_adversarial_substitution_all62: "IMPOSSIBLE",
  maximum_one_error_correctable_subset:26,
  exact_algorithm: "componentwise_minimum_vertex_cover",
  component_sizes:sizes
}));
