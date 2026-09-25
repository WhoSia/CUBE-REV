import unittest

from .p15_compiler import (
    AMBIGUOUS_EDIT,
    CORRECTED_ERROR_EPISODE,
    STREAM_RECONSTRUCTION_MISMATCH,
    TARGET_MATCH_KEY,
    TARGET_MISMATCH_KEY,
    KeyEvent,
    compile_stream,
)


def keys(chars):
    return [KeyEvent(c, i * 100, i * 100 + 30, c) for i, c in enumerate(chars)]


class CompilerTests(unittest.TestCase):
    def test_match(self):
        x = compile_stream("cat", keys("cat"), "cat")
        self.assertTrue(x["stream_matches_target"])
        self.assertEqual([e["state"] for e in x["events"]], [TARGET_MATCH_KEY] * 3)

    def test_substitution_then_backspace_is_one_corrected_episode(self):
        ev = keys("c") + [KeyEvent("X", 100, 130, "x"), KeyEvent("Backspace", 140, 170, None)] + keys("at")
        x = compile_stream("cat", ev, "cat")
        self.assertEqual(x["corrected_episode_count"], 1)
        self.assertIn(CORRECTED_ERROR_EPISODE, [e["state"] for e in x["events"]])

    def test_uncorrected_substitution(self):
        x = compile_stream("cat", keys("cot"), "cot")
        self.assertEqual(x["uncorrected_error_count"], 1)
        self.assertIn(TARGET_MISMATCH_KEY, [e["state"] for e in x["events"]])

    def test_insertion_then_backspace_is_corrected(self):
        ev = keys("ca") + [KeyEvent("X", 200, 230, "x"), KeyEvent("Backspace", 240, 260, None)] + keys("t")
        x = compile_stream("cat", ev, "cat")
        self.assertEqual(x["corrected_episode_count"], 1)

    def test_delete_is_not_repaired(self):
        x = compile_stream("cat", [KeyEvent("Delete", 0, 1, None)] + keys("cat"), "cat")
        self.assertGreater(x["ambiguous_edit_count"], 0)
        self.assertTrue(any(AMBIGUOUS_EDIT in e["flags"] for e in x["events"]))

    def test_final_input_disagreement_is_retained(self):
        x = compile_stream("cat", keys("cat"), "cot")
        self.assertIn(STREAM_RECONSTRUCTION_MISMATCH, x["stream_flags"])


if __name__ == "__main__":
    unittest.main()
