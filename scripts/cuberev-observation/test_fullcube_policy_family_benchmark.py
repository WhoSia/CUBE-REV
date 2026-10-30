#!/usr/bin/env python3
"""Recheck full-cube policy-family benchmark against 0.24 physical baseline."""
import unittest
from fullcube_policy_family_benchmark import Benchmark
from fullcube_goal_info_conflict import A

class FullCubeFamilyTest(unittest.TestCase):
    def test_u_uprime_exact_total_cost(self):
        model=Benchmark(radius=4)
        u=model.turn(model.solved,A.index("U"))
        up=model.turn(model.solved,A.index("U'"))
        outcome=model.evaluate((u,up),horizon=5)
        self.assertEqual(outcome["opt"],3)
        self.assertEqual(outcome["goal"]["action"],"U")
        self.assertEqual(outcome["goal"]["cost"],5)
        self.assertEqual(outcome["information"]["action"],"F")
        self.assertEqual(outcome["information"]["cost"],3)

    def test_original_ur_factor_is_closed_under_moves(self):
        model=Benchmark(radius=4)
        inert=["F","F'","F2","D","D'","D2","L","L'","L2","B","B'","B2"]
        originals=[model.turn(model.solved,A.index(s)) for s in inert]
        self.assertEqual(len({model.factor(s) for s in originals}),1)
        for move in range(18):
            self.assertEqual(len({model.factor(model.turn(s,move))
                                  for s in originals}),1)

if __name__=="__main__":
    unittest.main()
