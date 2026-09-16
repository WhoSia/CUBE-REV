import unittest
from .p15_r1_adapter import CollectorEmulator, apply_observable, classify

class AdapterTests(unittest.TestCase):
    def test_literal_authority(self):
        self.assertEqual(classify("A", 65), ("EMIT_LITERAL", "A"))
        self.assertEqual(classify("!", 49), ("EMIT_LITERAL", "!"))
    def test_controls(self):
        self.assertEqual(classify("BKSP", 8)[0], "BACKSPACE")
        self.assertEqual(classify("\b", 8)[0], "BACKSPACE")
        self.assertEqual(classify("DELETE", 46)[0], "DELETE")
        self.assertEqual(classify("\x7f", 46)[0], "DELETE")
        self.assertEqual(classify(".", 190), ("EMIT_LITERAL", "."))
    def test_no_keycode_character_fallback(self):
        self.assertEqual(classify(None, 65)[0], "UNKNOWN")
    def test_collector_overwrite_and_window(self):
        e=CollectorEmulator({65:"STATIC"}); e.keydown(65,100)
        self.assertTrue(e.keypress(ord("a"),115)); self.assertEqual(e.keyup(65,130)["letter"],"a")
        e.keydown(65,200); self.assertFalse(e.keypress(ord("A"),221))
    def test_multiple_rollover_and_unresolved(self):
        e=CollectorEmulator({65:"a",66:"b"}); e.keydown(65,0); e.keydown(66,5)
        self.assertEqual(e.keyup(66,10)["letter"],"b"); self.assertEqual(len(e.pending),1)
    def test_buffer(self):
        b,_=apply_observable("","EMIT_LITERAL","x"); b,_=apply_observable(b,"BACKSPACE")
        self.assertEqual(b,"")

if __name__ == "__main__": unittest.main()
