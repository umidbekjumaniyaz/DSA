#!/usr/bin/env python3
"""Test report generator for SkyNet Aviation Logistics System.

Runs the full pytest suite programmatically and generates a markdown test report
showing pass/fail counts by subsystem with timestamps.

Usage:
    python tests/test_report_generator.py

Output:
    docs/output/TEST_REPORT.md
"""
import subprocess
import sys
import re
from datetime import datetime
from pathlib import Path


# Map test file names to subsystem names
SUBSYSTEM_MAP = {
    "test_graph.py": "Graph",
    "test_heap.py": "Heap",
    "test_queue.py": "Queue",
    "test_stack.py": "Stack",
    "test_avl.py": "Tree (AVL)",
    "test_hash_table.py": "Hashing",
    "test_sorting.py": "Sorting",
    "test_kmp.py": "String Matching (KMP)",
    "test_backtracking.py": "Backtracking",
    "test_services_integration.py": "Integration",
    "test_models.py": "Models",
    "test_utils.py": "Utilities",
    "test_passenger_search_service.py": "Passenger Search",
}


def parse_verbose_output(output: str) -> dict:
    """Parse pytest verbose output to extract per-file results.

    Args:
        output: The stdout from pytest -v run.

    Returns:
        Dictionary mapping test file basenames to (passed, failed) tuples.
    """
    file_results = {}
    # Match lines like:
    # tests/unit_tests/test_graph.py::TestClass::test_method PASSED [  0%]
    test_line_pattern = re.compile(
        r"^(tests/[\w/]+/(test_\w+\.py))::.+\s(PASSED|FAILED|ERROR)\s",
        re.MULTILINE,
    )

    for match in test_line_pattern.finditer(output):
        filepath = match.group(1)
        filename = Path(filepath).name
        status = match.group(3)

        if filename not in file_results:
            file_results[filename] = {"passed": 0, "failed": 0}

        if status == "PASSED":
            file_results[filename]["passed"] += 1
        else:
            file_results[filename]["failed"] += 1

    return file_results


def parse_summary_line(output: str) -> tuple:
    """Parse the pytest summary line for total counts.

    Args:
        output: The stdout from pytest run.

    Returns:
        Tuple of (total_passed, total_failed, total_errors).
    """
    passed = 0
    failed = 0
    errors = 0

    # Match patterns like "377 passed", "2 failed", "1 error"
    passed_match = re.search(r"(\d+)\s+passed", output)
    failed_match = re.search(r"(\d+)\s+failed", output)
    error_match = re.search(r"(\d+)\s+error", output)

    if passed_match:
        passed = int(passed_match.group(1))
    if failed_match:
        failed = int(failed_match.group(1))
    if error_match:
        errors = int(error_match.group(1))

    return passed, failed, errors


def generate_report():
    """Run tests and generate markdown report.

    Executes the full pytest suite with verbose output, parses results,
    and writes a formatted markdown report to docs/output/TEST_REPORT.md.
    """
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "docs" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Running full test suite...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=str(project_root),
    )

    output = result.stdout
    stderr = result.stderr

    # Parse results
    file_results = parse_verbose_output(output)
    total_passed, total_failed, total_errors = parse_summary_line(output)
    total_tests = total_passed + total_failed + total_errors

    if total_tests == 0:
        # Fallback: try to parse from collected count
        collected_match = re.search(r"collected\s+(\d+)\s+item", output)
        if collected_match:
            total_tests = int(collected_match.group(1))

    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0.0

    # Build subsystem table
    subsystem_rows = []
    for filename, subsystem_name in SUBSYSTEM_MAP.items():
        if filename in file_results:
            data = file_results[filename]
            tests = data["passed"] + data["failed"]
            subsystem_rows.append(
                (subsystem_name, tests, data["passed"], data["failed"])
            )

    # Sort by subsystem name
    subsystem_rows.sort(key=lambda x: x[0])

    # Generate markdown report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# SkyNet Test Report

## Summary

- **Date:** {timestamp}
- **Total Tests:** {total_tests}
- **Passed:** {total_passed}
- **Failed:** {total_failed}
- **Errors:** {total_errors}
- **Pass Rate:** {pass_rate:.1f}%
- **Status:** {"ALL PASSING" if total_failed == 0 and total_errors == 0 else "FAILURES DETECTED"}

## Results by Subsystem

| Subsystem | Tests | Passed | Failed | Status |
|-----------|-------|--------|--------|--------|
"""

    for name, tests, passed, failed in subsystem_rows:
        status = "PASS" if failed == 0 else "FAIL"
        report += f"| {name} | {tests} | {passed} | {failed} | {status} |\n"

    report += f"""
## Test Coverage Summary

- **Subsystems Tested:** {len(subsystem_rows)}
- **Subsystems Passing:** {sum(1 for _, _, _, f in subsystem_rows if f == 0)}
- **Subsystems with Failures:** {sum(1 for _, _, _, f in subsystem_rows if f > 0)}

## Test Categories

| Category | Description |
|----------|-------------|
| Unit Tests | Individual data structure and algorithm verification |
| Integration Tests | Cross-service interaction and workflow testing |
| Property Tests | Hypothesis-based invariant verification |

## Environment

- **Python Version:** {sys.version.split()[0]}
- **Test Framework:** pytest
- **Property Testing:** hypothesis

---

*Report generated automatically by `tests/test_report_generator.py`*
"""

    # Write report
    report_path = output_dir / "TEST_REPORT.md"
    report_path.write_text(report)
    print(f"Test report written to: {report_path}")
    print(f"\nSummary: {total_passed}/{total_tests} tests passed ({pass_rate:.1f}%)")

    # Return exit code based on test results
    return 0 if total_failed == 0 and total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(generate_report())
