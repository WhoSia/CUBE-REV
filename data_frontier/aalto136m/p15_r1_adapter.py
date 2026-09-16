"""Layer-L authoritative adapter and minimal collector emulator for P15-R1."""
from dataclasses import dataclass

CONTROL = {
    "BKSP": "BACKSPACE", "BACKSPACE": "BACKSPACE", "DELETE": "DELETE",
    "SHIFT": "SHIFT", "CTRL": "CTRL", "ALT": "ALT", "TAB": "TAB",
    "ENTER": "ENTER", "RETURN": "ENTER", "CAPS_LOCK": "NON_TEXT",
    "ESC": "NON_TEXT", "PAUSE": "NON_TEXT", "WIN": "NON_TEXT",
    "MENU": "NON_TEXT", "INSERT": "NON_TEXT", "HOME": "NON_TEXT",
    "END": "NON_TEXT", "PG_UP": "NON_TEXT", "PG_DOWN": "NON_TEXT",
    "ARW_LEFT": "NON_TEXT", "ARW_RIGHT": "NON_TEXT", "ARW_UP": "NON_TEXT",
    "ARW_DOWN": "NON_TEXT", "ARw_DOWN": "NON_TEXT",
}


def classify(letter, keycode):
    """Translate stored Layer L; Layer K is used only to classify controls."""
    # Some browsers deliver a keypress control character after the collector's
    # static keydown seed.  The collector then stores that character in Layer L.
    # Layer K resolves only the control operation here; it is never converted to
    # an ordinary output character.
    try:
        keycode_i = int(keycode)
    except (TypeError, ValueError):
        keycode_i = None
    if keycode_i == 8 and letter in {"BKSP", "BACKSPACE", "\b"}:
        return "BACKSPACE", None
    if keycode_i == 46 and letter in {"DELETE", "DEL", "\x7f"}:
        return "DELETE", None
    if letter is None or letter == "":
        return "UNKNOWN", None
    if letter in CONTROL:
        return CONTROL[letter], None
    if len(letter) == 1:
        return "EMIT_LITERAL", letter
    return "AMBIGUOUS_OUTPUT", None


@dataclass
class Pending:
    keycode: int
    down: int
    letter: str | None


class CollectorEmulator:
    def __init__(self, static_map=None, window_ms=20):
        self.static_map = static_map or {}
        self.window_ms = window_ms
        self.pending = []

    def keydown(self, keycode, time, repeated=False):
        if repeated:
            return
        self.pending.append(Pending(keycode, time, self.static_map.get(keycode)))

    def keypress(self, charcode, time):
        for p in self.pending:
            if time - self.window_ms <= p.down <= time:
                p.letter = chr(charcode)
                return True
        return False

    def keyup(self, keycode, time):
        for i, p in enumerate(self.pending):
            if p.letter is not None and p.keycode == keycode:
                self.pending.pop(i)
                return {"pressTime": p.down, "releaseTime": time,
                        "keycode": p.keycode, "letter": p.letter}
        return None


def apply_observable(buffer, op, literal=None):
    if op == "EMIT_LITERAL":
        return buffer + literal, True
    if op == "BACKSPACE":
        return buffer[:-1] if buffer else buffer, True
    if op in {"SHIFT", "CTRL", "ALT", "NON_TEXT"}:
        return buffer, True
    if op == "ENTER":
        return buffer, True
    return buffer, False
