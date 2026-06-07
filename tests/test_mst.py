"""Unit tests for Prim and Kruskal MST algorithms (Req 16.1)."""

import unittest

from algorithms.mst import kruskal, prim
from data_structures.graph import Graph


def build(edges, airports):
    g = Graph()
    for a in airports:
        g.add_airport(a)
    for a, b, w in edges:
        g.add_route(a, b, w)
    return g


class TestMST(unittest.TestCase):
    def test_connected_edge_count_and_cost(self):
        g = build(
            [("A", "B", 1), ("B", "C", 2), ("A", "C", 5), ("C", "D", 1)], "ABCD"
        )
        routes_p, cost_p = prim(g)
        routes_k, cost_k = kruskal(g)
        self.assertEqual(len(routes_p), 3)  # n - 1
        self.assertEqual(len(routes_k), 3)
        self.assertEqual(cost_p, cost_k)
        self.assertEqual(cost_p, 4.0)

    def test_disconnected_returns_none(self):
        g = build([("A", "B", 1), ("C", "D", 1)], "ABCD")
        self.assertIsNone(prim(g))
        self.assertIsNone(kruskal(g))

    def test_empty_graph_returns_none(self):
        g = Graph()
        self.assertIsNone(prim(g))
        self.assertIsNone(kruskal(g))

    def test_single_airport(self):
        g = build([], "A")
        routes, cost = prim(g)
        self.assertEqual(routes, [])
        self.assertEqual(cost, 0.0)


if __name__ == "__main__":
    unittest.main()
