"""Run the full test suite and generate docs/Test_Report.md (Req 16.4).

Usage:
    python -m tests.test_report_generator
"""

import datetime
import os
import unittest


class _RecordingResult(unittest.TextTestResult):
    """Captures the outcome of every executed test case."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []  # (test_id, status)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append((test.id(), "PASS"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append((test.id(), "FAIL"))

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append((test.id(), "ERROR"))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append((test.id(), f"SKIP ({reason})"))


def generate_report(output_path: str = None) -> str:
    """Execute every test in ``tests/`` and write a Markdown report."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if output_path is None:
        output_path = os.path.join(repo_root, "docs", "Test_Report.md")

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(repo_root, "tests"), top_level_dir=repo_root
    )
    runner = unittest.TextTestRunner(resultclass=_RecordingResult, verbosity=0)
    result = runner.run(suite)

    total = len(result.records)
    passed = sum(1 for _, s in result.records if s == "PASS")
    failed = sum(1 for _, s in result.records if s == "FAIL")
    errored = sum(1 for _, s in result.records if s == "ERROR")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# SkyNet Test Report",
        "",
        f"Generated: {timestamp}",
        "",
        "## Summary",
        "",
        f"- Total test cases: {total}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Errors: {errored}",
        f"- Result: {'ALL PASSED' if failed == errored == 0 else 'FAILURES PRESENT'}",
        "",
        "## Test Cases",
        "",
        "| # | Test Case | Outcome |",
        "| --- | --- | --- |",
    ]
    for i, (test_id, status) in enumerate(sorted(result.records), start=1):
        short = test_id.replace("tests.", "")
        lines.append(f"| {i} | `{short}` | {status} |")
    lines.append("")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"Test report written to {output_path}")
    print(f"  {passed}/{total} passed, {failed} failed, {errored} errors.")
    return output_path


if __name__ == "__main__":
    generate_report()
