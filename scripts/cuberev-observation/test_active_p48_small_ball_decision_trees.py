#!/usr/bin/env python3
"""Small radius B1/B2 exact adaptive/nonadaptive query solver regressions."""
import unittest
from audit_active_p48_small_ball_decision_trees import (
    ball, observations, nonadaptive_witness, can_adapt, audit, BudgetExceeded
)

class ActiveSmallBallDecisionTreeTests(unittest.TestCase):
    def test_exact_b1_b2_physical_state_count(self):
        self.assertEqual(len(ball(1)[0]),19)
        self.assertEqual(len(ball(2)[0]),262)

    def test_toy_adaptive_decision_tree_needs_two_queries(self):
        rows=((0,0,1,1),(0,1,0,1))
        self.assertFalse(can_adapt(rows,1)[0])
        self.assertTrue(can_adapt(rows,2)[0])
        self.assertFalse(can_adapt(((0,0,0),),3)[0])

    def test_exact_b1_b2_audit_consistency(self):
        outcomes=audit()
        self.assertEqual(len(outcomes),2)
        for r,n,adaptive,nonadaptive in outcomes:
            self.assertEqual(n,{1:19,2:262}[r])
            self.assertLessEqual(adaptive,nonadaptive)
            factors,queries,rows=observations(ball(r)[0])
            w=nonadaptive_witness(factors,nonadaptive)
            self.assertIsNotNone(w)
            edges,corners=w
            idx=edges+tuple(12+i for i in corners)
            self.assertEqual(len({tuple(f[i] for i in idx) for f in factors}),n)

if __name__=="__main__":
    unittest.main()
