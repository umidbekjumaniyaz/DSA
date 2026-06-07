"""Comprehensive unit tests for the KMP string matching module.

Tests cover: KMP failure function computation, normal search operations
(pattern found, multiple matches, single char), edge cases (pattern equals
text, pattern at start/end, case-insensitive matching), and error conditions
(no match, empty pattern).

Requirements: 10.5, 10.7, 13.12, 13.13
"""

import pytest

from skynet.string_matching.kmp import KMPMatcher


# ============================================================
# Helper fixtures
# ============================================================


@pytest.fixture
def kmp():
    """Return a KMPMatcher instance."""
    return KMPMatcher()


# ============================================================
# TestKMPFailureFunction
# ============================================================


class TestKMPFailureFunction:
    """Unit tests for KMP failure (partial match) function computation."""

    def test_failure_function_ababc(self, kmp):
        """Failure function for 'ABABC' produces [0, 0, 1, 2, 0]."""
        result = kmp.compute_failure_function("ABABC")
        assert result == [0, 0, 1, 2, 0]

    def test_failure_function_aabaaab(self, kmp):
        """Failure function for 'AABAAAB' produces [0, 1, 0, 1, 2, 2, 3]."""
        result = kmp.compute_failure_function("AABAAAB")
        assert result == [0, 1, 0, 1, 2, 2, 3]

    def test_failure_function_abcabd(self, kmp):
        """Failure function for 'ABCABD' produces [0, 0, 0, 1, 2, 0]."""
        result = kmp.compute_failure_function("ABCABD")
        assert result == [0, 0, 0, 1, 2, 0]

    def test_failure_function_single_char(self, kmp):
        """Failure function for single character pattern produces [0]."""
        result = kmp.compute_failure_function("A")
        assert result == [0]

    def test_failure_function_all_same_chars(self, kmp):
        """Failure function for 'AAAA' produces [0, 1, 2, 3]."""
        result = kmp.compute_failure_function("AAAA")
        assert result == [0, 1, 2, 3]

    def test_failure_function_no_prefix_suffix(self, kmp):
        """Failure function for 'ABCDE' (no repeated prefixes) produces all zeros."""
        result = kmp.compute_failure_function("ABCDE")
        assert result == [0, 0, 0, 0, 0]

    def test_failure_function_abab(self, kmp):
        """Failure function for 'ABAB' produces [0, 0, 1, 2]."""
        result = kmp.compute_failure_function("ABAB")
        assert result == [0, 0, 1, 2]


# ============================================================
# TestKMPSearchNormal
# ============================================================


class TestKMPSearchNormal:
    """Unit tests for KMP search under normal operating conditions."""

    def test_pattern_found_at_correct_position(self, kmp):
        """KMP search finds pattern at the correct starting index."""
        text = "HELLO WORLD"
        pattern = "WORLD"
        result = kmp.search(text, pattern)
        assert result == [6]

    def test_multiple_matches(self, kmp):
        """KMP search finds all occurrences of a pattern."""
        text = "ABABABABAB"
        pattern = "ABAB"
        result = kmp.search(text, pattern)
        assert result == [0, 2, 4, 6]

    def test_single_char_pattern(self, kmp):
        """KMP search finds all occurrences of a single character pattern."""
        text = "BANANA"
        pattern = "A"
        result = kmp.search(text, pattern)
        assert result == [1, 3, 5]

    def test_pattern_found_once_in_middle(self, kmp):
        """KMP search finds a pattern occurring once in the middle of text."""
        text = "THE QUICK BROWN FOX"
        pattern = "BROWN"
        result = kmp.search(text, pattern)
        assert result == [10]

    def test_pattern_found_multiple_non_overlapping(self, kmp):
        """KMP search finds multiple non-overlapping occurrences."""
        text = "CAT DOG CAT BIRD CAT"
        pattern = "CAT"
        result = kmp.search(text, pattern)
        assert result == [0, 8, 17]


# ============================================================
# TestKMPSearchEdgeCases
# ============================================================


class TestKMPSearchEdgeCases:
    """Unit tests for KMP search edge case scenarios."""

    def test_pattern_equals_text(self, kmp):
        """KMP search returns [0] when pattern equals text exactly."""
        text = "EXACT"
        pattern = "EXACT"
        result = kmp.search(text, pattern)
        assert result == [0]

    def test_pattern_at_start(self, kmp):
        """KMP search finds pattern at the beginning of text."""
        text = "HELLO WORLD"
        pattern = "HELLO"
        result = kmp.search(text, pattern)
        assert result == [0]

    def test_pattern_at_end(self, kmp):
        """KMP search finds pattern at the end of text."""
        text = "HELLO WORLD"
        pattern = "WORLD"
        result = kmp.search(text, pattern)
        assert result == [6]

    def test_case_insensitive_matching(self, kmp):
        """KMP search performs case-insensitive matching."""
        text = "Hello World"
        pattern = "hello"
        result = kmp.search(text, pattern)
        assert result == [0]

    def test_case_insensitive_mixed_case(self, kmp):
        """KMP search finds matches regardless of case differences."""
        text = "The Quick Brown Fox Jumps Over The Lazy Dog"
        pattern = "the"
        result = kmp.search(text, pattern)
        assert result == [0, 31]

    def test_case_insensitive_all_upper_pattern_lower_text(self, kmp):
        """KMP search matches uppercase pattern in lowercase text."""
        text = "aviation logistics system"
        pattern = "LOGISTICS"
        result = kmp.search(text, pattern)
        assert result == [9]

    def test_overlapping_matches(self, kmp):
        """KMP search correctly finds overlapping pattern occurrences."""
        text = "AAAAAA"
        pattern = "AAA"
        result = kmp.search(text, pattern)
        assert result == [0, 1, 2, 3]


# ============================================================
# TestKMPSearchErrors
# ============================================================


class TestKMPSearchErrors:
    """Unit tests for KMP search error and no-match conditions."""

    def test_no_match_returns_empty(self, kmp):
        """KMP search returns empty list when pattern is not found."""
        text = "HELLO WORLD"
        pattern = "XYZ"
        result = kmp.search(text, pattern)
        assert result == []

    def test_empty_pattern_returns_empty(self, kmp):
        """KMP search returns empty list for empty pattern."""
        text = "HELLO WORLD"
        pattern = ""
        result = kmp.search(text, pattern)
        assert result == []

    def test_pattern_longer_than_text(self, kmp):
        """KMP search returns empty list when pattern is longer than text."""
        text = "HI"
        pattern = "HELLO WORLD"
        result = kmp.search(text, pattern)
        assert result == []

    def test_no_match_similar_but_different(self, kmp):
        """KMP search correctly returns empty when text has similar but non-matching substrings."""
        text = "ABCABEABCABD"
        pattern = "ABCABCABD"
        result = kmp.search(text, pattern)
        assert result == []
