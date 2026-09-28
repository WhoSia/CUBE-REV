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
