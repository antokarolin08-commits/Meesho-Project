import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from masking import alias_for, assert_no_raw_names_leak


class TestMasking(unittest.TestCase):
    def test_alias_transformation(self):
        self.assertEqual(alias_for("RS019"), "ALIAS-19")
        self.assertEqual(alias_for("RS006"), "ALIAS-06")
        self.assertEqual(alias_for("RS022"), "ALIAS-22")
        self.assertEqual(alias_for("RS012"), "ALIAS-12")
        self.assertEqual(alias_for("RS005"), "ALIAS-05")

    def test_raw_names_leak_detection(self):
        raw_reseller_names = [
            "Mumbai Reseller 1",
            "Mumbai Reseller 4",
            "Hyderabad Reseller 6",
            "Lucknow Reseller 6",
            "Jaipur Reseller 5",
        ]

        # Case 1: Safe masked text from narrative_report.md
        safe_text = (
            "Top partners ALIAS-19 and ALIAS-22 in West region exceeded INR 50000."
        )
        self.assertTrue(assert_no_raw_names_leak(safe_text, raw_reseller_names))

        # Case 2: Leaked text containing raw name
        leaked_text = (
            "Top partner Mumbai Reseller 1 generated total spend of INR 75295.09."
        )
        self.assertFalse(assert_no_raw_names_leak(leaked_text, raw_reseller_names))


if __name__ == "__main__":
    unittest.main()