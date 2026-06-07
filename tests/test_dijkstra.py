"""Unit tests for Dijkstra on connected, cyclic, and disconnected graphs."""

import unittest

from algorithms.dijkstra import dijkstra
from data_structures.graph import Graph


def build(edges, airports):
    g = Graph()
    for a in airports:
        g.add_airport(a)
    for a, b, w in edges:
        g.add_route(a, b, w)
    return g


class TestDijkstra(unittest.TestCase):
    def test_connected_shortest_path(self):
        g = build([("A", "B", 1), ("B", "C", 2), ("A", "C", 5)], "ABC")
        path, cost = dijkstra(g, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 3.0)

    def test_self_distance_zero(self):
        g = build([("A", "B", 1)], "AB")
        self.assertEqual(dijkstra(g, "A", "A"), (["A"], 0.0))

    def test_no_path_disconnected(self):
        g = build([("A", "B", 1), ("C", "D", 1)], "ABCD")
        self.assertIsNone(dijkstra(g, "A", "D"))

    def test_cyclic_graph(self):
        g = build([("A", "B", 1), ("B", "C", 1), ("C", "A", 1)], "ABC")
        path, cost = dijkstra(g, "A", "C")
        self.assertEqual(cost, 1.0)
        self.assertEqual(path, ["A", "C"])


if __name__ == "__main__":
    unittest.main()
