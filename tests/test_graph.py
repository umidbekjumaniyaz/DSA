"""Unit tests for the Graph data structure and its edge cases (Req 16.1)."""

import unittest

from data_structures.graph import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g = Graph()

    def test_empty_graph(self):
        self.assertTrue(self.g.is_empty())
        self.assertEqual(self.g.airport_count(), 0)
        self.assertEqual(self.g.edge_count(), 0)

    def test_add_airport_and_duplicate(self):
        self.g.add_airport("LHR")
        self.assertTrue(self.g.has_airport("lhr"))  # case-insensitive
        with self.assertRaises(KeyError):
            self.g.add_airport("LHR")

    def test_add_route_requires_existing_airports(self):
        self.g.add_airport("A")
        with self.assertRaises(KeyError):
            self.g.add_route("A", "B", 10)

    def test_duplicate_route_rejected(self):
        self.g.add_airport("A")
        self.g.add_airport("B")
        self.g.add_route("A", "B", 10)
        with self.assertRaises(ValueError):
            self.g.add_route("B", "A", 99)  # undirected duplicate

    def test_cyclic_graph(self):
        for c in "ABC":
            self.g.add_airport(c)
        self.g.add_route("A", "B", 1)
        self.g.add_route("B", "C", 1)
        self.g.add_route("C", "A", 1)  # cycle
        self.assertEqual(self.g.edge_count(), 3)
        self.assertEqual(len(self.g.neighbors("A")), 2)

    def test_disconnected_graph(self):
        for c in "ABCD":
            self.g.add_airport(c)
        self.g.add_route("A", "B", 1)
        self.g.add_route("C", "D", 1)  # two components
        self.assertEqual(self.g.edge_count(), 2)
        self.assertEqual(self.g.neighbors("A")[0].other("A"), "B")

    def test_invalid_weight_rejected(self):
        self.g.add_airport("A")
        self.g.add_airport("B")
        with self.assertRaises(ValueError):
            self.g.add_route("A", "B", -5)


if __name__ == "__main__":
    unittest.main()
