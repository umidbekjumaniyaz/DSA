"""Unit tests for backtracking path enumeration, including failure (Req 16.3)."""

import unittest

from algorithms.backtracking import enumerate_paths
from data_structures.graph import Graph


def build(edges, airports):
    g = Graph()
    for a in airports:
        g.add_airport(a)
    for a, b, w in edges:
        g.add_route(a, b, w)
    return g


class TestBacktracking(unittest.TestCase):
    def test_all_simple_paths(self):
        g = build([("A", "B", 1), ("B", "C", 1), ("A", "C", 1)], "ABC")
        paths = enumerate_paths(g, "A", "C")
        self.assertIn(["A", "C"], paths)
        self.assertIn(["A", "B", "C"], paths)
        self.assertEqual(len(paths), 2)

    def test_hub_exclusion(self):
        g = build([("A", "B", 1), ("B", "C", 1), ("A", "C", 1)], "ABC")
        paths = enumerate_paths(g, "A", "C", excluded="B")
        self.assertEqual(paths, [["A", "C"]])

    def test_no_path_when_hub_removed(self):
        # Only route A-C goes through B; remove B -> failure.
        g = build([("A", "B", 1), ("B", "C", 1)], "ABC")
        paths = enumerate_paths(g, "A", "C", excluded="B")
        self.assertEqual(paths, [])

    def test_simple_paths_only(self):
        g = build([("A", "B", 1), ("B", "C", 1), ("C", "A", 1)], "ABC")
        for path in enumerate_paths(g, "A", "C"):
            self.assertEqual(len(path), len(set(path)))


if __name__ == "__main__":
    unittest.main()
