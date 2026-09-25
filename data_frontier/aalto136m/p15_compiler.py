"""Fail-closed error-state compiler for G3-P15.

This module deliberately has no Aalto file-format knowledge. The ingestion
adapter supplies observable text-producing key output plus press/release times;
the compiler supplies a small, auditable state machine. It never treats a
correction key as an error by itself and never invents selection/cursor edits.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from typing import Iterable, Optional


TARGET_MATCH_KEY = "TARGET_MATCH_KEY"
TARGET_MISMATCH_KEY = "TARGET_MISMATCH_KEY"
CORRECTION_KEY = "CORRECTION_KEY"
CORRECTED_ERROR_EPISODE = "CORRECTED_ERROR_EPISODE"
UNCORRECTED_ERROR = "UNCORRECTED_ERROR"
AMBIGUOUS_EDIT = "AMBIGUOUS_EDIT"
STREAM_RECONSTRUCTION_MISMATCH = "STREAM_RECONSTRUCTION_MISMATCH"

CORRECTION_KEYS = {"BACKSPACE", "DELETE"}


@dataclass
class KeyEvent:
    raw_key: str
    press_ms: Optional[float]
    release_ms: Optional[float]
    output: Optional[str]


@dataclass
class CompiledEvent:
    ordinal: int
    raw_key: str
    output: Optional[str]
    press_ms: Optional[float]
    release_ms: Optional[float]
    state: str
    target_position: Optional[int]
    episode_id: Optional[int]
    correction_of: Optional[int]
    flags: tuple[str, ...] = ()

    def asdict(self):
        d = asdict(self)
        d["flags"] = list(self.flags)
        return d


def _online_expected(target: str, visible: list[int], emitted: list[CompiledEvent]) -> Optional[int]:
    """Return a unique, conservative expected target index for appending.

    A prior unresolved mismatch destroys a unique online target cursor. This is
    intentionally conservative: the affected event is ambiguous rather than
    heuristically realigned.
    """
    if any(emitted[i].state in {TARGET_MISMATCH_KEY, AMBIGUOUS_EDIT} for i in visible):
        return None
    return len(visible) if len(visible) < len(target) else None


def compile_stream(
    target: str,
    events: Iterable[KeyEvent],
    logged_final: Optional[str] = None,
    include_alignment: bool = True,
) -> dict:
    """Compile one observable end-edit stream.

    Only end-of-buffer Backspace is reconstructed as a unique edit. Delete and
    correction when no active key exists are recorded but ambiguous: they might
    refer to an unobserved cursor or selection state. A global final alignment
    is retained as a check, but never used to rewrite an online ambiguous state.
    """
    out: list[CompiledEvent] = []
    visible: list[int] = []
    open_episode: Optional[int] = None
    next_episode = 1

    for ordinal, ev in enumerate(events):
        key_norm = (ev.raw_key or "").upper()
        if key_norm in CORRECTION_KEYS:
            correction = CompiledEvent(
                ordinal, ev.raw_key, ev.output, ev.press_ms, ev.release_ms,
                CORRECTION_KEY, None, open_episode, None,
            )
            if key_norm != "BACKSPACE" or not visible:
                correction.flags = (AMBIGUOUS_EDIT,)
                out.append(correction)
                continue
            prior_i = visible.pop()
            prior = out[prior_i]
            correction.correction_of = prior_i
            if prior.state == TARGET_MISMATCH_KEY and prior.episode_id is not None:
                prior.state = CORRECTED_ERROR_EPISODE
                correction.episode_id = prior.episode_id
                if open_episode == prior.episode_id:
                    open_episode = None
            else:
                correction.flags = (AMBIGUOUS_EDIT,)
                prior.flags = tuple(sorted(set(prior.flags + (AMBIGUOUS_EDIT,))))
            out.append(correction)
            continue

        # Nontext observables cannot be converted into an unobserved edit.
        if ev.output is None or len(ev.output) != 1:
            out.append(CompiledEvent(
                ordinal, ev.raw_key, ev.output, ev.press_ms, ev.release_ms,
                AMBIGUOUS_EDIT, None, open_episode, None, ("NON_TEXT_KEY",),
            ))
            continue

        expected_pos = _online_expected(target, visible, out)
        if expected_pos is None:
            state = AMBIGUOUS_EDIT
            episode = open_episode
        elif ev.output == target[expected_pos]:
            state = TARGET_MATCH_KEY
            episode = None
        else:
            state = TARGET_MISMATCH_KEY
            episode = next_episode
            next_episode += 1
            open_episode = episode
        out.append(CompiledEvent(
            ordinal, ev.raw_key, ev.output, ev.press_ms, ev.release_ms,
            state, expected_pos, episode, None,
        ))
        visible.append(len(out) - 1)

    reconstructed = "".join(out[i].output or "" for i in visible)
    # Any unresolved online mismatch is an uncorrected error. We retain its
    # original state as well as a summary count so event-level and episode-level
    # analyses cannot be confused.
    uncorrected = [e for e in out if e.state == TARGET_MISMATCH_KEY]
    alignment_ok = reconstructed == target
    flags: list[str] = []
    if logged_final is not None and logged_final != reconstructed:
        flags.append(STREAM_RECONSTRUCTION_MISMATCH)

    return {
        "target": target,
        "reconstructed": reconstructed,
        "logged_final": logged_final,
        "stream_matches_target": alignment_ok,
        "stream_matches_logged_final": None if logged_final is None else logged_final == reconstructed,
        "alignment_opcodes": (SequenceMatcher(a=target, b=reconstructed, autojunk=False).get_opcodes()
                              if include_alignment else None),
        "uncorrected_error_count": len(uncorrected),
        "corrected_episode_count": len({e.episode_id for e in out if e.state == CORRECTED_ERROR_EPISODE}),
        "ambiguous_edit_count": sum(1 for e in out if e.state == AMBIGUOUS_EDIT or AMBIGUOUS_EDIT in e.flags),
        "stream_flags": flags,
        "events": [e.asdict() for e in out],
    }
