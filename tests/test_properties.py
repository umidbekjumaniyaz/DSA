"""Property-based tests for the SkyNet correctness properties.

Each test corresponds to one numbered correctness property from the design
document and runs a minimum of 100 generated examples.
"""

import unittest
from itertools import combinations

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from algorithms.backtracking import enumerate_paths
from algorithms.dijkstra import dijkstra
from algorithms.kmp import search as kmp_search
from algorithms.mst import kruskal, prim
from algorithms.sorting import mergesort, quicksort
from data_structures.fifo_queue import Queue
from data_structures.graph import Graph
from data_structures.hash_table import HashTable
from data_structures.lifo_stack import Stack
from data_structures.max_heap import MaxHeap
from data_structures.price_tree import AVLTree
from models.passenger import Passenger
from models.ticket_status import TicketStatus

SETTINGS = settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])

# ----- helpers -----------------------------------------------------------
AIRPORT_CODES = ["A", "B", "C", "D", "E", "F"]


def _make_pnr(i: int) -> str:
    base = f"{i:06d}"
    return base[-6:]


@st.composite
def connected_graphs(draw, min_n=2, max_n=6):
    """Generate a connected weighted graph by building a random spanning
    tree and then adding extra random edges."""
    n = draw(st.integers(min_value=min_n, max_value=max_n))
    nodes = AIRPORT_CODES[:n]
    g = Graph()
    for node in nodes:
        g.add_airport(node)
    # Spanning tree: connect node i to a random earlier node.
    for i in range(1, n):
        j = draw(st.integers(min_value=0, max_value=i - 1))
        w = draw(st.integers(min_value=1, max_value=20))
        g.add_route(nodes[i], nodes[j], w)
    # Extra edges.
    possible = [
        (a, b) for a, b in combinations(nodes, 2) if not g.has_route(a, b)
    ]
    extra = draw(st.integers(min_value=0, max_value=len(possible)))
    for k in range(extra):
        a, b = possible[k]
        w = draw(st.integers(min_value=1, max_value=20))
        g.add_route(a, b, w)
    return g, nodes


def _brute_force_min(graph, src, dst):
    """Minimum path cost via exhaustive simple-path enumeration."""
    best = [float("inf")]

    def dfs(node, visited, cost):
        if node == dst:
            best[0] = min(best[0], cost)
            return
        for route in graph.neighbors(node):
            nxt = route.other(node)
            if nxt not in visited:
                dfs(nxt, visited | {nxt}, cost + route.weight)

    dfs(src, {src}, 0.0)
    return best[0]


def _naive_search(text, pattern):
    if pattern == "":
        return []
    return [i for i in range(len(text) - len(pattern) + 1)
            if text[i:i + len(pattern)] == pattern]


def _dfs_simple_paths(graph, src, dst, excluded):
    paths = []

    def dfs(node, visited, path):
        if node == dst:
            paths.append(list(path))
            return
        for route in graph.neighbors(node):
            nxt = route.other(node)
            if nxt == excluded or nxt in visited:
                continue
            dfs(nxt, visited | {nxt}, path + [nxt])

    if src == excluded or dst == excluded:
        return []
    dfs(src, {src}, [src])
    return paths


class TestProperties(unittest.TestCase):

    # Feature: skynet-aviation-system, Property 1: Airport lifecycle — add is observable and duplicates are rejected
    @SETTINGS
    @given(st.lists(st.sampled_from(AIRPORT_CODES), min_size=1, max_size=6))
    def test_property_01_airport_lifecycle(self, codes):
        g = Graph()
        added = set()
        for code in codes:
            if code in added:
                with self.assertRaises(KeyError):
                    g.add_airport(code)
            else:
                before = g.airport_count()
                g.add_airport(code)
                added.add(code)
                self.assertTrue(g.has_airport(code))
                self.assertEqual(g.airport_count(), before + 1)

    # Feature: skynet-aviation-system, Property 2: Route addition is observable and duplicates are rejected
    @SETTINGS
    @given(st.integers(min_value=1, max_value=50))
    def test_property_02_route_addition(self, weight):
        g = Graph()
        g.add_airport("A")
        g.add_airport("B")
        before = g.edge_count()
        g.add_route("A", "B", weight)
        self.assertTrue(g.has_route("A", "B"))
        self.assertEqual(g.edge_count(), before + 1)
        with self.assertRaises(ValueError):
            g.add_route("B", "A", weight)
        self.assertEqual(g.edge_count(), before + 1)

    # Feature: skynet-aviation-system, Property 3: Dijkstra returns a true minimum-weight path
    @SETTINGS
    @given(connected_graphs())
    def test_property_03_dijkstra_minimal(self, data):
        g, nodes = data
        src, dst = nodes[0], nodes[-1]
        result = dijkstra(g, src, dst)
        self.assertIsNotNone(result)
        _, cost = result
        self.assertAlmostEqual(cost, _brute_force_min(g, src, dst))

    # Feature: skynet-aviation-system, Property 4: Dijkstra self-distance is zero
    @SETTINGS
    @given(connected_graphs())
    def test_property_04_dijkstra_self_distance(self, data):
        g, nodes = data
        for node in nodes:
            self.assertEqual(dijkstra(g, node, node), ([node], 0.0))

    # Feature: skynet-aviation-system, Property 5: MST has exactly (n - 1) edges
    @SETTINGS
    @given(connected_graphs())
    def test_property_05_mst_edge_count(self, data):
        g, nodes = data
        routes, _ = prim(g)
        self.assertEqual(len(routes), len(nodes) - 1)

    # Feature: skynet-aviation-system, Property 6: Prim and Kruskal agree on total cost
    @SETTINGS
    @given(connected_graphs())
    def test_property_06_prim_kruskal_agree(self, data):
        g, _ = data
        self.assertAlmostEqual(prim(g)[1], kruskal(g)[1])

    # Feature: skynet-aviation-system, Property 7: Priority queue dequeues in non-increasing ticket-status order
    @SETTINGS
    @given(st.lists(st.sampled_from(list(TicketStatus)), min_size=1, max_size=30))
    def test_property_07_priority_order(self, statuses):
        heap = MaxHeap(priority_of=lambda p: int(p.status))
        for i, s in enumerate(statuses):
            heap.push(Passenger(pnr=_make_pnr(i), name=f"P{i}", status=s))
        popped = [int(heap.pop().status) for _ in range(len(statuses))]
        self.assertEqual(popped, sorted((int(s) for s in statuses), reverse=True))
        self.assertEqual(popped[0], max(int(s) for s in statuses))

    # Feature: skynet-aviation-system, Property 8: Boarding queue preserves FIFO order
    @SETTINGS
    @given(st.lists(st.integers(), max_size=50))
    def test_property_08_fifo(self, items):
        q = Queue()
        for x in items:
            q.enqueue(x)
        self.assertEqual([q.dequeue() for _ in items], items)

    # Feature: skynet-aviation-system, Property 9: Cargo stack preserves LIFO order
    @SETTINGS
    @given(st.lists(st.integers(), max_size=50))
    def test_property_09_lifo(self, items):
        s = Stack()
        for x in items:
            s.push(x)
        self.assertEqual([s.pop() for _ in items], items[::-1])

    # Feature: skynet-aviation-system, Property 10: Price tree membership round-trip
    @SETTINGS
    @given(st.lists(st.integers(min_value=-1000, max_value=1000), max_size=50))
    def test_property_10_membership(self, prices):
        tree = AVLTree()
        for p in prices:
            tree.insert(p)
        for p in set(prices):
            self.assertTrue(tree.contains(p))
        self.assertFalse(tree.contains(99999))

    # Feature: skynet-aviation-system, Property 11: Range search equals the filtered set
    @SETTINGS
    @given(
        st.lists(st.integers(min_value=0, max_value=200), max_size=50),
        st.integers(min_value=0, max_value=200),
        st.integers(min_value=0, max_value=200),
    )
    def test_property_11_range_search(self, prices, a, b):
        tree = AVLTree()
        for p in prices:
            tree.insert(p)
        low, high = min(a, b), max(a, b)
        expected = sorted(p for p in prices if low <= p <= high)
        self.assertEqual(tree.range_search(low, high), expected)
        # Inverted bounds -> empty.
        if low != high:
            self.assertEqual(tree.range_search(high + 1, low), [])

    # Feature: skynet-aviation-system, Property 12: AVL tree stays height-balanced
    @SETTINGS
    @given(st.lists(st.integers(min_value=0, max_value=5000), min_size=1, max_size=200))
    def test_property_12_avl_balanced(self, prices):
        import math
        tree = AVLTree()
        for p in prices:
            tree.insert(p)
        n = tree.size()
        bound = 1.4405 * math.log2(n + 2)
        self.assertLessEqual(tree.height(), bound)

    # Feature: skynet-aviation-system, Property 13: Hash table round-trip with collisions
    @SETTINGS
    @given(st.lists(st.integers(min_value=0, max_value=999999),
                    min_size=1, max_size=40, unique=True))
    def test_property_13_hash_roundtrip(self, ints):
        t = HashTable(capacity=2)  # tiny capacity forces collisions
        mapping = {_make_pnr(i): i for i in ints}
        for k, v in mapping.items():
            t.put(k, v)
        for k, v in mapping.items():
            self.assertEqual(t.get(k), v)

    # Feature: skynet-aviation-system, Property 14: Hash table delete removes the mapping
    @SETTINGS
    @given(st.lists(st.integers(min_value=0, max_value=999999),
                    min_size=2, max_size=40, unique=True))
    def test_property_14_hash_delete(self, ints):
        t = HashTable()
        keys = [_make_pnr(i) for i in ints]
        for k in keys:
            t.put(k, k)
        victim = keys[0]
        t.delete(victim)
        self.assertFalse(t.contains(victim))
        for k in keys[1:]:
            self.assertTrue(t.contains(k))

    # Feature: skynet-aviation-system, Property 15: PNR validation accepts only the defined format
    @SETTINGS
    @given(st.text(max_size=10))
    def test_property_15_pnr_validation(self, s):
        import re
        expected = bool(re.match(r"^[A-Z0-9]{6}$", s.strip().upper())) \
            if isinstance(s, str) else False
        self.assertEqual(Passenger.is_valid_pnr(s), expected)

    # Feature: skynet-aviation-system, Property 16: Both sorts produce key-sorted output that preserves the input multiset
    @SETTINGS
    @given(st.lists(st.integers(), max_size=60))
    def test_property_16_sort_correct(self, data):
        for sorter in (quicksort, mergesort):
            out = sorter(data)
            self.assertEqual(out, sorted(data))
            self.assertEqual(sorted(out), sorted(data))  # multiset preserved

    # Feature: skynet-aviation-system, Property 17: QuickSort and MergeSort produce identical output
    @SETTINGS
    @given(st.lists(st.integers(), max_size=60))
    def test_property_17_sorts_identical(self, data):
        self.assertEqual(quicksort(data), mergesort(data))

    # Feature: skynet-aviation-system, Property 18: KMP match soundness
    @SETTINGS
    @given(st.text(alphabet="ab", max_size=40), st.text(alphabet="ab", min_size=1, max_size=5))
    def test_property_18_kmp_soundness(self, text, pattern):
        for pos in kmp_search(text, pattern):
            self.assertEqual(text[pos:pos + len(pattern)], pattern)

    # Feature: skynet-aviation-system, Property 19: KMP equals naive scan (oracle equivalence)
    @SETTINGS
    @given(st.text(alphabet="ab", max_size=40), st.text(alphabet="ab", max_size=5))
    def test_property_19_kmp_oracle(self, text, pattern):
        self.assertEqual(kmp_search(text, pattern), _naive_search(text, pattern))

    # Feature: skynet-aviation-system, Property 20: Backtracking enumerates exactly the simple paths that exclude the hub
    @SETTINGS
    @given(connected_graphs(min_n=2, max_n=5),
           st.sampled_from(AIRPORT_CODES))
    def test_property_20_backtracking_complete(self, data, hub):
        g, nodes = data
        src, dst = nodes[0], nodes[-1]
        excluded = hub if hub in nodes else None
        got = enumerate_paths(g, src, dst, excluded)
        expected = _dfs_simple_paths(g, src, dst, excluded)
        self.assertEqual(sorted(map(tuple, got)), sorted(map(tuple, expected)))
        for path in got:
            self.assertNotIn(excluded, path)

    # Feature: skynet-aviation-system, Property 21: Backtracking returns only simple paths
    @SETTINGS
    @given(connected_graphs(min_n=2, max_n=5))
    def test_property_21_simple_paths(self, data):
        g, nodes = data
        for path in enumerate_paths(g, nodes[0], nodes[-1]):
            self.assertEqual(len(path), len(set(path)))

    # Feature: skynet-aviation-system, Property 22: Handled errors never raise across the service boundary
    @SETTINGS
    @given(st.text(max_size=8))
    def test_property_22_service_never_raises(self, pnr):
        from services.checkin_service import CheckInService
        service = CheckInService(MaxHeap(priority_of=lambda p: int(p.status)),
                                 HashTable())
        result = service.lookup(pnr)  # arbitrary (often invalid) PNR
        self.assertFalse(result.ok)
        self.assertIsNotNone(result.error)


if __name__ == "__main__":
    unittest.main()
