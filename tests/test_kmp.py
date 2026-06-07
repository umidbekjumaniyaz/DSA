"""Unit tests for KMP substring search."""

import unittest

from algorithms.kmp import search


class TestKMP(unittest.TestCase):
    def test_single_match(self):
        self.assertEqual(search("hello world", "world"), [6])

    def test_multiple_matches(self):
        self.assertEqual(search("ababab", "ab"), [0, 2, 4])

    def test_overlapping_matches(self):
        self.assertEqual(search("aaaa", "aa"), [0, 1, 2])

    def test_no_match(self):
        self.assertEqual(search("abcdef", "xyz"), [])

    def test_empty_manifest(self):
        self.assertEqual(search("", "abc"), [])

    def test_empty_pattern(self):
        self.assertEqual(search("abc", ""), [])

    def test_pattern_longer_than_text(self):
        self.assertEqual(search("ab", "abc"), [])


if __name__ == "__main__":
    unittest.main()
