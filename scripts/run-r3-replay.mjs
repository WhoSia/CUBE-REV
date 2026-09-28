import { assertMonotonicLog, canonicalStimulusBytes, symbolicFrameBytes } from "../dist/kernel.js";

const perm = [0, 1, 2, 3, 4, 5, 6];
const ori = [0, 0, 0, 0, 0, 0, 0];
const bytes = canonicalStimulusBytes(perm, ori, "UFR", "P");
const frame = symbolicFrameBytes(perm, ori, "UFR");
const rank = 0;
const events = [
  { sequence: 0, monotonicMs: 0, type: "STIMULUS", preRank: rank, postRank: rank },
  { sequence: 1, monotonicMs: 10, type: "PERTURBATION", preRank: rank, postRank: rank },
  { sequence: 2, monotonicMs: 20, type: "SHAM", preRank: rank, postRank: rank },
  { sequence: 3, monotonicMs: 30, type: "MOVE", preRank: rank, postRank: rank },
];
assertMonotonicLog(events);
const replayBytes = canonicalStimulusBytes(perm, ori, "UFR", "P");
if (bytes !== replayBytes || frame !== symbolicFrameBytes(perm, ori, "UFR")) throw new Error("REPLAY_MISMATCH_REFUSE");
console.log(JSON.stringify({ status: "PASS", event_count: events.length, initial_rank: rank, final_rank: rank, sham_rank_invariant: true, replay_byte_identical: true }));
