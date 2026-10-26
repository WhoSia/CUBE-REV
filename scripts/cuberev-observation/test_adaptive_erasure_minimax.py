import unittest
from adaptive_erasure_minimax import solve
class TestAdaptive(unittest.TestCase):
    def test_singleton(self):
        self.assertEqual(solve((0,),2)["worst_case_turn_cost"],0)
    def test_one_step_erasure_bound(self):
        self.assertEqual(solve((0,1),1)["status"],"NO_POLICY_WITHIN_SPECIFIED_HORIZON")
if __name__=="__main__":
    unittest.main()
