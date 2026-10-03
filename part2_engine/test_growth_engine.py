import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from growth_engine import mom_growth, is_flagged, validate_feed


class TestGrowthEngine(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(CURRENT_DIR, "fixtures")
        self.corrupted_feed = os.path.join(self.fixtures_dir, "corrupted_feed.csv")
        self.valid_feed = os.path.join(self.fixtures_dir, "monthly_category_revenue.csv")

    def test_gwt_case_1_may_ethnic_wear(self):
        growth = mom_growth(104520.77, 185107.61)
        self.assertEqual(growth, 77.1)
        self.assertEqual(is_flagged(growth), "flagged")

    def test_gwt_case_2_june_beauty_care(self):
        growth = mom_growth(35542.11, 37559.07)
        self.assertEqual(growth, 5.67)
        self.assertEqual(is_flagged(growth), "not_flagged")

    def test_gwt_case_3_boundary_escalation(self):
        growth = mom_growth(100000.0, 108000.0)
        self.assertEqual(growth, 8.0)
        self.assertEqual(is_flagged(growth), "escalate_exact_boundary")

    def test_gwt_case_4_corrupted_feed(self):
        is_valid, errors = validate_feed(self.corrupted_feed)
        self.assertFalse(is_valid)
        expected_errors = [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)"
        ]
        self.assertEqual(errors, expected_errors)

    def test_valid_feed_passes(self):
        is_valid, errors = validate_feed(self.valid_feed)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_full_may_vs_april_table(self):
        expected = {
            "Ethnic Wear": (77.1, "flagged"),
            "Western Wear": (-23.6, "flagged"),
            "Kids Wear": (-23.48, "flagged"),
            "Home & Kitchen": (-9.25, "flagged"),
            "Beauty & Personal Care": (-12.75, "flagged"),
        }
        april_rev = {
            "Ethnic Wear": 104520.77, "Western Wear": 113866.15, "Kids Wear": 59847.27,
            "Home & Kitchen": 100446.23, "Beauty & Personal Care": 40737.01,
        }
        may_rev = {
            "Ethnic Wear": 185107.61, "Western Wear": 86998.18, "Kids Wear": 45793.78,
            "Home & Kitchen": 91152.57, "Beauty & Personal Care": 35542.11,
        }
        for cat, (exp_pct, exp_status) in expected.items():
            pct = mom_growth(april_rev[cat], may_rev[cat])
            status = is_flagged(pct)
            self.assertEqual(pct, exp_pct)
            self.assertEqual(status, exp_status)

    def test_full_june_vs_may_table(self):
        expected = {
            "Ethnic Wear": (-58.74, "flagged"),
            "Western Wear": (11.97, "flagged"),
            "Kids Wear": (23.9, "flagged"),
            "Home & Kitchen": (42.59, "flagged"),
            "Beauty & Personal Care": (5.67, "not_flagged"),
        }
        may_rev = {
            "Ethnic Wear": 185107.61, "Western Wear": 86998.18, "Kids Wear": 45793.78,
            "Home & Kitchen": 91152.57, "Beauty & Personal Care": 35542.11,
        }
        june_rev = {
            "Ethnic Wear": 76371.53, "Western Wear": 97415.64, "Kids Wear": 56737.78,
            "Home & Kitchen": 129971.22, "Beauty & Personal Care": 37559.07,
        }
        for cat, (exp_pct, exp_status) in expected.items():
            pct = mom_growth(may_rev[cat], june_rev[cat])
            status = is_flagged(pct)
            self.assertEqual(pct, exp_pct)
            self.assertEqual(status, exp_status)


if __name__ == "__main__":
    unittest.main()