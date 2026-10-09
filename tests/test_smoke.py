import sys
import unittest
from pathlib import Path

from smoke import inspect


class SmokeTests(unittest.TestCase):
    def test_additive_field_regression(self):
        decoder = [sys.executable, str(Path(__file__).parents[1] / "examples" / "strict_decoder.py")]
        report = inspect({"items": []}, "total", 1, decoder)
        self.assertEqual(report["status"], "regression")
        self.assertEqual(report["baseline_exit"], 0)
        self.assertEqual(report["added_exit"], 2)


if __name__ == "__main__":
    unittest.main()
