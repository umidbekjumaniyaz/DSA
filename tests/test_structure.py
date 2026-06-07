"""Structural smoke test asserting required artifacts exist (Req 24.3)."""

import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestProjectStructure(unittest.TestCase):
    def _exists(self, *parts):
        return os.path.exists(os.path.join(ROOT, *parts))

    def test_entry_point_and_metadata(self):
        self.assertTrue(self._exists("main.py"))
        self.assertTrue(self._exists("README.md"))
        self.assertTrue(self._exists("requirements.txt"))

    def test_source_directories(self):
        for d in ("models", "data_structures", "algorithms", "services",
                  "console", "tests", "docs"):
            self.assertTrue(self._exists(d), f"missing directory: {d}")

    def test_documentation_files(self):
        for f in ("adt_specifications.md", "complexity_report.md",
                  "documentation_report.md", "traceability_matrix.md"):
            self.assertTrue(self._exists("docs", f), f"missing doc: {f}")


if __name__ == "__main__":
    unittest.main()
