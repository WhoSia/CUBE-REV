/** Synthetic instrument boundary. Rust exact-core output is authoritative. */
export type ExactRank = number & { readonly __exactRank: unique symbol };

export interface SymbolicFrame {
  readonly canonicalBytes: string;
  readonly scientificHash: string;
}

export interface CanonicalStimulus {
  readonly rank: ExactRank;
  readonly frame: SymbolicFrame;
  readonly pidSha256: string;
}

export interface LoggedEvent {
  readonly sequence: number;
  readonly monotonicMs: number;
  readonly type: "STIMULUS" | "PERTURBATION" | "SHAM" | "MOVE" | "FOCUS" | "VISIBILITY";
  readonly preRank: ExactRank;
  readonly postRank: ExactRank;
}

/** Rejects payloads whose stated identity does not match the Rust-issued PID. */
export function assertStimulusPid(stimulus: CanonicalStimulus, expectedPid: string): void {
  if (stimulus.pidSha256 !== expectedPid) throw new Error("PID_MISMATCH_REFUSE");
}

/** SHAM is explicit and may not change exact state. */
export function assertEventInvariant(event: LoggedEvent): void {
  if (event.type === "SHAM" && event.preRank !== event.postRank) throw new Error("SHAM_STATE_CHANGE_REFUSE");
  if (!Number.isSafeInteger(event.sequence) || !Number.isFinite(event.monotonicMs)) throw new Error("MALFORMED_EVENT_REFUSE");
}

/** The UI consumes SymbolicFrame; it never derives ExactRank from pixels or DOM. */
export function rendererInput(stimulus: CanonicalStimulus): SymbolicFrame {
  return stimulus.frame;
}

/** Rust-mirrored packed 7!×3^6 rank. This validates payloads; it is not an R2 oracle. */
export function rankCornerState(perm: readonly number[], ori: readonly number[]): ExactRank {
  if (perm.length !== 7 || ori.length !== 7) throw new Error("MALFORMED_CANONICAL_PAYLOAD_REFUSE");
  const seen = new Set<number>();
  for (const p of perm) { if (!Number.isInteger(p) || p < 0 || p > 6 || seen.has(p)) throw new Error("ILLEGAL_CUBIE_STATE_REFUSE"); seen.add(p); }
  let sum = 0;
  for (const o of ori) { if (!Number.isInteger(o) || o < 0 || o > 2) throw new Error("ILLEGAL_CUBIE_STATE_REFUSE"); sum = (sum + o) % 3; }
  if (sum !== 0) throw new Error("ILLEGAL_CUBIE_STATE_REFUSE");
  let lehmer = 0;
  for (let i = 0; i < 7; i += 1) { let lower = 0; for (let j = i + 1; j < 7; j += 1) if (perm[j] < perm[i]) lower += 1; lehmer += lower * factorial(6 - i); }
  let orientation = 0;
  for (const o of ori.slice(0, 6)) orientation = orientation * 3 + o;
  return (lehmer * 729 + orientation) as ExactRank;
}

export function symbolicFrameBytes(perm: readonly number[], ori: readonly number[], authorizedView: string): string {
  rankCornerState(perm, ori);
  return `sf1|view=${authorizedView}|perm=${perm.join(",")}|ori=${ori.join(",")}`;
}

export function canonicalStimulusBytes(perm: readonly number[], ori: readonly number[], authorizedView: string, arm: string): string {
  return `cs1|rank=${rankCornerState(perm, ori)}|frame=${symbolicFrameBytes(perm, ori, authorizedView)}|arm=${arm}`;
}

export function assertMonotonicLog(events: readonly LoggedEvent[]): void {
  let priorSequence = -1; let priorTime = -Infinity;
  for (const event of events) { assertEventInvariant(event); if (event.sequence <= priorSequence || event.monotonicMs < priorTime) throw new Error("NONMONOTONIC_EVENT_LOG_REFUSE"); priorSequence = event.sequence; priorTime = event.monotonicMs; }
}

function factorial(n: number): number { let value = 1; for (let i = 2; i <= n; i += 1) value *= i; return value; }
