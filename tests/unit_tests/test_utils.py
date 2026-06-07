"""Unit tests for skynet.utils modules (validators, formatters, performance)."""

import pytest

from skynet.utils.validators import (
    validate_iata_code,
    validate_pnr,
    validate_priority_level,
    validate_numeric_range,
    validate_non_empty_string,
)
from skynet.utils.formatters import (
    format_path,
    format_table,
    format_mst_result,
    format_separator,
)
from skynet.utils.performance import (
    measure_time,
    measure_memory,
    measure_performance,
)


# =============================================================================
# Validator Tests
# =============================================================================


class TestValidateIataCode:
    """Tests for validate_iata_code."""

    def test_valid_iata_codes(self):
        assert validate_iata_code("LHR") is True
        assert validate_iata_code("JFK") is True
        assert validate_iata_code("DXB") is True

    def test_lowercase_rejected(self):
        assert validate_iata_code("lhr") is False
        assert validate_iata_code("Lhr") is False

    def test_wrong_length(self):
        assert validate_iata_code("LH") is False
        assert validate_iata_code("LHRS") is False
        assert validate_iata_code("") is False

    def test_non_alpha_rejected(self):
        assert validate_iata_code("LH1") is False
        assert validate_iata_code("12A") is False
        assert validate_iata_code("L-R") is False

    def test_non_string_input(self):
        assert validate_iata_code(123) is False
        assert validate_iata_code(None) is False
        assert validate_iata_code([]) is False


class TestValidatePnr:
    """Tests for validate_pnr."""

    def test_valid_pnrs(self):
        assert validate_pnr("ABC123") is True
        assert validate_pnr("X") is True
        assert validate_pnr("123456") is True

    def test_empty_string_rejected(self):
        assert validate_pnr("") is False

    def test_non_alphanumeric_rejected(self):
        assert validate_pnr("AB-C") is False
        assert validate_pnr("AB C") is False
        assert validate_pnr("AB@C") is False

    def test_non_string_input(self):
        assert validate_pnr(123) is False
        assert validate_pnr(None) is False


class TestValidatePriorityLevel:
    """Tests for validate_priority_level."""

    def test_valid_levels_case_insensitive(self):
        assert validate_priority_level("Platinum") is True
        assert validate_priority_level("gold") is True
        assert validate_priority_level("SILVER") is True
        assert validate_priority_level("economy") is True
        assert validate_priority_level("ECONOMY") is True

    def test_invalid_levels(self):
        assert validate_priority_level("VIP") is False
        assert validate_priority_level("") is False
        assert validate_priority_level("first") is False

    def test_non_string_input(self):
        assert validate_priority_level(123) is False
        assert validate_priority_level(None) is False


class TestValidateNumericRange:
    """Tests for validate_numeric_range."""

    def test_value_in_range(self):
        assert validate_numeric_range(5, 1, 10) is True
        assert validate_numeric_range(1, 1, 10) is True
        assert validate_numeric_range(10, 1, 10) is True

    def test_value_out_of_range(self):
        assert validate_numeric_range(0, 1, 10) is False
        assert validate_numeric_range(11, 1, 10) is False
        assert validate_numeric_range(-1, 0, 100) is False

    def test_non_comparable_input(self):
        assert validate_numeric_range("abc", 1, 10) is False
        assert validate_numeric_range(None, 1, 10) is False


class TestValidateNonEmptyString:
    """Tests for validate_non_empty_string."""

    def test_valid_strings(self):
        assert validate_non_empty_string("hello") is True
        assert validate_non_empty_string("a") is True
        assert validate_non_empty_string(" hi ") is True

    def test_empty_and_whitespace_rejected(self):
        assert validate_non_empty_string("") is False
        assert validate_non_empty_string("   ") is False
        assert validate_non_empty_string("\t\n") is False

    def test_non_string_input(self):
        assert validate_non_empty_string(123) is False
        assert validate_non_empty_string(None) is False


# =============================================================================
# Formatter Tests
# =============================================================================


class TestFormatPath:
    """Tests for format_path."""

    def test_normal_path(self):
        result = format_path(["LHR", "CDG", "JFK"], 6200)
        assert result == "LHR -> CDG -> JFK (6200 km)"

    def test_single_node(self):
        result = format_path(["LHR"], 0)
        assert result == "LHR (0 km)"

    def test_empty_path(self):
        result = format_path([], 0)
        assert result == "(empty path)"


class TestFormatTable:
    """Tests for format_table."""

    def test_normal_table(self):
        result = format_table(["Name", "City"], [["LHR", "London"], ["JFK", "New York"]])
        assert "Name" in result
        assert "City" in result
        assert "LHR" in result
        assert "London" in result
        assert "JFK" in result
        assert "New York" in result

    def test_empty_headers(self):
        result = format_table([], [["a", "b"]])
        assert result == ""

    def test_empty_rows(self):
        result = format_table(["Col1", "Col2"], [])
        assert "Col1" in result
        assert "Col2" in result

    def test_alignment(self):
        result = format_table(["A", "B"], [["short", "x"], ["a", "longer"]])
        lines = result.split("\n")
        # Header, separator, and two data lines
        assert len(lines) == 4


class TestFormatMstResult:
    """Tests for format_mst_result."""

    def test_normal_mst(self):
        edges = [("LHR", "CDG", 340), ("CDG", "JFK", 5800)]
        result = format_mst_result(edges, 6140)
        assert "LHR -- CDG (weight: 340)" in result
        assert "CDG -- JFK (weight: 5800)" in result
        assert "Total Cost: 6140 km" in result

    def test_empty_edges(self):
        result = format_mst_result([], 0)
        assert "Total Cost: 0 km" in result


class TestFormatSeparator:
    """Tests for format_separator."""

    def test_default(self):
        result = format_separator()
        assert result == "=" * 50

    def test_custom_char_and_length(self):
        result = format_separator("-", 30)
        assert result == "-" * 30
        assert len(result) == 30


# =============================================================================
# Performance Tests
# =============================================================================


class TestMeasureTime:
    """Tests for measure_time."""

    def test_returns_result_and_time(self):
        result, elapsed = measure_time(sum, [1, 2, 3])
        assert result == 6
        assert elapsed >= 0

    def test_handles_exception(self):
        result, elapsed = measure_time(lambda: 1 / 0)
        assert result is None
        assert elapsed == 0.0


class TestMeasureMemory:
    """Tests for measure_memory."""

    def test_returns_result_and_memory(self):
        result, mem = measure_memory(lambda: [i for i in range(100)])
        assert len(result) == 100
        assert mem >= 0

    def test_handles_exception(self):
        result, mem = measure_memory(lambda: 1 / 0)
        assert result is None
        assert mem == 0


class TestMeasurePerformance:
    """Tests for measure_performance."""

    def test_returns_result_time_and_memory(self):
        result, elapsed, mem = measure_performance(sum, [1, 2, 3, 4, 5])
        assert result == 15
        assert elapsed >= 0
        assert mem >= 0

    def test_handles_exception(self):
        result, elapsed, mem = measure_performance(lambda: 1 / 0)
        assert result is None
        assert elapsed == 0.0
        assert mem == 0
