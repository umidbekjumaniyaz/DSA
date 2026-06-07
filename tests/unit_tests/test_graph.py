"""Comprehensive unit tests for the graph module.

Tests cover: WeightedGraph, DijkstraSolver, PrimMST, KruskalMST, and UnionFind.
Organized by pytest classes for normal operations, edge cases, error conditions,
and algorithm-specific behavior.

Requirements: 13.1, 13.2, 13.3, 13.4, 13.10, 13.12, 13.13
"""

import pytest

from skynet.graph.weighted_graph import WeightedGraph
from skynet.graph.dijkstra import DijkstraSolver
from skynet.graph.prim import PrimMST
from skynet.graph.kruskal import KruskalMST
from skynet.graph.union_find import UnionFind
from skynet.models.airport import Airport


# ============================================================
# Helper fixtures
# ============================================================


@pytest.fixture
def empty_graph():
    """Return an empty WeightedGraph."""
    return WeightedGraph()


@pytest.fixture
def single_node_graph():
    """Return a graph containing a single airport node."""
    g = WeightedGraph()
    g.add_node(Airport("LHR", "Heathrow", "London"))
    return g


@pytest.fixture
def triangle_graph():
    """Return a connected graph with 3 nodes forming a triangle.

    LHR --340-- CDG
     \\          /
      5500   5200
       \\    /
        JFK
    """
    g = WeightedGraph()
    g.add_node(Airport("LHR", "Heathrow", "London"))
    g.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
    g.add_node(Airport("JFK", "John F Kennedy", "New York"))
    g.add_edge("LHR", "CDG", 340)
    g.add_edge("LHR", "JFK", 5500)
    g.add_edge("CDG", "JFK", 5200)
    return g


@pytest.fixture
def linear_graph():
    """Return a linear graph: LHR -- CDG -- DXB -- SIN (no shortcuts)."""
    g = WeightedGraph()
    g.add_node(Airport("LHR", "Heathrow", "London"))
    g.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
    g.add_node(Airport("DXB", "Dubai International", "Dubai"))
    g.add_node(Airport("SIN", "Changi", "Singapore"))
    g.add_edge("LHR", "CDG", 340)
    g.add_edge("CDG", "DXB", 5200)
    g.add_edge("DXB", "SIN", 5800)
    return g


@pytest.fixture
def disconnected_graph():
    """Return a disconnected graph with two components: {LHR, CDG} and {DXB, SIN}."""
    g = WeightedGraph()
    g.add_node(Airport("LHR", "Heathrow", "London"))
    g.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
    g.add_node(Airport("DXB", "Dubai International", "Dubai"))
    g.add_node(Airport("SIN", "Changi", "Singapore"))
    g.add_edge("LHR", "CDG", 340)
    g.add_edge("DXB", "SIN", 5800)
    return g


# ============================================================
# TestWeightedGraphNormal - Normal operations
# ============================================================


class TestWeightedGraphNormal:
    """Test normal operations of WeightedGraph: add/remove nodes, add/remove edges, display."""

    def test_add_node_success(self, empty_graph):
        """Adding a valid airport node succeeds."""
        result = empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        assert result.success is True
        assert empty_graph.has_node("LHR")
        assert empty_graph.node_count() == 1

    def test_add_multiple_nodes(self, empty_graph):
        """Adding multiple distinct nodes increases node count."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        empty_graph.add_node(Airport("JFK", "John F Kennedy", "New York"))
        assert empty_graph.node_count() == 3

    def test_add_edge_success(self, empty_graph):
        """Adding an edge between two existing nodes succeeds."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        result = empty_graph.add_edge("LHR", "CDG", 340)
        assert result.success is True
        assert empty_graph.has_edge("LHR", "CDG")
        assert empty_graph.has_edge("CDG", "LHR")  # Bidirectional
        assert empty_graph.edge_count() == 1

    def test_edge_bidirectional_neighbors(self, empty_graph):
        """Adding an edge makes both endpoints appear in each other's neighbor list."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        empty_graph.add_edge("LHR", "CDG", 340)

        lhr_neighbors = empty_graph.get_neighbors("LHR")
        cdg_neighbors = empty_graph.get_neighbors("CDG")
        assert ("CDG", 340) in lhr_neighbors
        assert ("LHR", 340) in cdg_neighbors

    def test_remove_node_success(self, triangle_graph):
        """Removing a node removes it and all associated edges."""
        result = triangle_graph.remove_node("CDG")
        assert result.success is True
        assert not triangle_graph.has_node("CDG")
        assert not triangle_graph.has_edge("LHR", "CDG")
        assert not triangle_graph.has_edge("CDG", "JFK")
        assert triangle_graph.node_count() == 2

    def test_remove_edge_success(self, triangle_graph):
        """Removing an edge preserves both endpoint nodes."""
        result = triangle_graph.remove_edge("LHR", "CDG")
        assert result.success is True
        assert not triangle_graph.has_edge("LHR", "CDG")
        assert not triangle_graph.has_edge("CDG", "LHR")
        assert triangle_graph.has_node("LHR")
        assert triangle_graph.has_node("CDG")
        assert triangle_graph.edge_count() == 2

    def test_display_adjacency_list(self, triangle_graph):
        """Display returns a string with adjacency list representation."""
        output = triangle_graph.display()
        assert "Flight Network (Adjacency List):" in output
        assert "LHR" in output
        assert "CDG" in output
        assert "JFK" in output

    def test_get_all_edges(self, triangle_graph):
        """get_all_edges returns all unique edges without duplicates."""
        edges = triangle_graph.get_all_edges()
        assert len(edges) == 3
        # Each edge is unique (no bidirectional duplication)
        edge_set = {(e[0], e[1]) for e in edges}
        assert len(edge_set) == 3

    def test_get_all_nodes(self, triangle_graph):
        """get_all_nodes returns list of all IATA codes."""
        nodes = triangle_graph.get_all_nodes()
        assert set(nodes) == {"LHR", "CDG", "JFK"}


# ============================================================
# TestWeightedGraphEdgeCases - Edge cases
# ============================================================


class TestWeightedGraphEdgeCases:
    """Test edge cases: empty graph, single node, boundary weights."""

    def test_empty_graph_node_count(self, empty_graph):
        """Empty graph has zero nodes and edges."""
        assert empty_graph.node_count() == 0
        assert empty_graph.edge_count() == 0

    def test_empty_graph_display(self, empty_graph):
        """Display on empty graph returns empty network message."""
        output = empty_graph.display()
        assert "empty" in output.lower()

    def test_empty_graph_get_all_nodes(self, empty_graph):
        """get_all_nodes on empty graph returns empty list."""
        assert empty_graph.get_all_nodes() == []

    def test_empty_graph_get_all_edges(self, empty_graph):
        """get_all_edges on empty graph returns empty list."""
        assert empty_graph.get_all_edges() == []

    def test_single_node_no_edges(self, single_node_graph):
        """Single node graph has one node and no edges."""
        assert single_node_graph.node_count() == 1
        assert single_node_graph.edge_count() == 0
        assert single_node_graph.get_neighbors("LHR") == []

    def test_single_node_display(self, single_node_graph):
        """Single node graph display shows the node with no routes."""
        output = single_node_graph.display()
        assert "LHR" in output
        assert "no routes" in output

    def test_minimum_weight_edge(self, empty_graph):
        """Edge with minimum weight 1 is accepted."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        result = empty_graph.add_edge("LHR", "CDG", 1)
        assert result.success is True

    def test_maximum_weight_edge(self, empty_graph):
        """Edge with maximum weight 99999 is accepted."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        result = empty_graph.add_edge("LHR", "CDG", 99999)
        assert result.success is True

    def test_get_neighbors_nonexistent_node(self, empty_graph):
        """get_neighbors for non-existent node returns empty list."""
        assert empty_graph.get_neighbors("XYZ") == []

    def test_has_edge_nonexistent_nodes(self, empty_graph):
        """has_edge returns False when nodes don't exist."""
        assert empty_graph.has_edge("LHR", "CDG") is False


# ============================================================
# TestWeightedGraphErrors - Error conditions
# ============================================================


class TestWeightedGraphErrors:
    """Test error conditions: duplicate node, non-existent node, invalid IATA, invalid weight."""

    def test_duplicate_node_rejected(self, single_node_graph):
        """Adding a node with duplicate IATA code is rejected."""
        result = single_node_graph.add_node(Airport("LHR", "London Heathrow", "London"))
        assert result.success is False
        assert "already exists" in result.message

    def test_remove_nonexistent_node(self, empty_graph):
        """Removing a non-existent node returns failure."""
        result = empty_graph.remove_node("XYZ")
        assert result.success is False
        assert "does not exist" in result.message

    def test_add_edge_nonexistent_source(self, single_node_graph):
        """Adding an edge with non-existent source is rejected."""
        result = single_node_graph.add_edge("XYZ", "LHR", 100)
        assert result.success is False
        assert "does not exist" in result.message

    def test_add_edge_nonexistent_destination(self, single_node_graph):
        """Adding an edge with non-existent destination is rejected."""
        result = single_node_graph.add_edge("LHR", "XYZ", 100)
        assert result.success is False
        assert "does not exist" in result.message

    def test_add_edge_invalid_weight_zero(self, empty_graph):
        """Adding an edge with weight 0 is rejected."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        result = empty_graph.add_edge("LHR", "CDG", 0)
        assert result.success is False
        assert "invalid" in result.message.lower()

    def test_add_edge_invalid_weight_exceeds_max(self, empty_graph):
        """Adding an edge with weight > 99999 is rejected."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        result = empty_graph.add_edge("LHR", "CDG", 100000)
        assert result.success is False
        assert "invalid" in result.message.lower()

    def test_add_duplicate_edge_rejected(self, empty_graph):
        """Adding a duplicate edge between same nodes is rejected."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        empty_graph.add_edge("LHR", "CDG", 340)
        result = empty_graph.add_edge("LHR", "CDG", 500)
        assert result.success is False
        assert "already exists" in result.message

    def test_remove_edge_no_route_exists(self, empty_graph):
        """Removing an edge that doesn't exist is rejected."""
        empty_graph.add_node(Airport("LHR", "Heathrow", "London"))
        empty_graph.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        result = empty_graph.remove_edge("LHR", "CDG")
        assert result.success is False
        assert "No route exists" in result.message

    def test_invalid_iata_code_raises_error(self):
        """Creating Airport with invalid IATA code raises ValueError."""
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("lhr", "Heathrow", "London")

    def test_invalid_iata_code_too_short(self):
        """IATA code with fewer than 3 characters raises ValueError."""
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("LH", "Heathrow", "London")

    def test_invalid_iata_code_numeric(self):
        """IATA code with numeric characters raises ValueError."""
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("L1R", "Heathrow", "London")


# ============================================================
# TestDijkstra - Shortest path algorithm tests
# ============================================================


class TestDijkstra:
    """Test Dijkstra's shortest path: correct path, no path, same src/dest, multi-hop."""

    def test_direct_route_shortest_path(self, triangle_graph):
        """Direct edge is the shortest path when it has lowest weight."""
        solver = DijkstraSolver()
        result = solver.compute_shortest_path(triangle_graph, "LHR", "CDG")
        assert result.success is True
        assert result.data["path"] == ["LHR", "CDG"]
        assert result.data["distance"] == 340

    def test_multi_hop_shortest_path(self):
        """Multi-hop path chosen when shorter than direct route."""
        g = WeightedGraph()
        g.add_node(Airport("LHR", "Heathrow", "London"))
        g.add_node(Airport("CDG", "Charles de Gaulle", "Paris"))
        g.add_node(Airport("JFK", "John F Kennedy", "New York"))
        # Direct LHR->JFK = 10000, via CDG = 340 + 5200 = 5540
        g.add_edge("LHR", "JFK", 10000)
        g.add_edge("LHR", "CDG", 340)
        g.add_edge("CDG", "JFK", 5200)

        solver = DijkstraSolver()
        result = solver.compute_shortest_path(g, "LHR", "JFK")
        assert result.success is True
        assert result.data["path"] == ["LHR", "CDG", "JFK"]
        assert result.data["distance"] == 5540

    def test_same_source_destination(self, triangle_graph):
        """Source equals destination returns path of single node with distance 0."""
        solver = DijkstraSolver()
        result = solver.compute_shortest_path(triangle_graph, "LHR", "LHR")
        assert result.success is True
        assert result.data["path"] == ["LHR"]
        assert result.data["distance"] == 0

    def test_no_path_disconnected(self, disconnected_graph):
        """No path between disconnected components returns failure."""
        solver = DijkstraSolver()
        result = solver.compute_shortest_path(disconnected_graph, "LHR", "DXB")
        assert result.success is False
        assert "No connection" in result.message

    def test_nonexistent_source_node(self, triangle_graph):
        """Non-existent source node returns failure with error message."""
        solver = DijkstraSolver()
        result = solver.compute_shortest_path(triangle_graph, "XYZ", "LHR")
        assert result.success is False
        assert "does not exist" in result.message

    def test_nonexistent_destination_node(self, triangle_graph):
        """Non-existent destination node returns failure with error message."""
        solver = DijkstraSolver()
        result = solver.compute_shortest_path(triangle_graph, "LHR", "XYZ")
        assert result.success is False
        assert "does not exist" in result.message

    def test_linear_multi_hop_path(self, linear_graph):
        """Multi-hop path through a linear graph returns correct total distance."""
        solver = DijkstraSolver()
        result = solver.compute_shortest_path(linear_graph, "LHR", "SIN")
        assert result.success is True
        assert result.data["path"] == ["LHR", "CDG", "DXB", "SIN"]
        assert result.data["distance"] == 340 + 5200 + 5800

    def test_cyclic_graph_correct_result(self):
        """Dijkstra terminates correctly on cyclic graph and finds optimal path."""
        g = WeightedGraph()
        g.add_node(Airport("AAA", "Airport A", "City A"))
        g.add_node(Airport("BBB", "Airport B", "City B"))
        g.add_node(Airport("CCC", "Airport C", "City C"))
        g.add_node(Airport("DDD", "Airport D", "City D"))
        # Cycle: AAA-BBB-CCC-AAA, with shortcut via DDD
        g.add_edge("AAA", "BBB", 100)
        g.add_edge("BBB", "CCC", 100)
        g.add_edge("CCC", "AAA", 100)
        g.add_edge("AAA", "DDD", 50)
        g.add_edge("DDD", "CCC", 30)

        solver = DijkstraSolver()
        result = solver.compute_shortest_path(g, "AAA", "CCC")
        assert result.success is True
        # Via DDD: 50 + 30 = 80 < direct CCC: 100
        assert result.data["distance"] == 80
        assert result.data["path"] == ["AAA", "DDD", "CCC"]


# ============================================================
# TestPrimMST - Prim's algorithm tests
# ============================================================


class TestPrimMST:
    """Test Prim's MST: correct MST, disconnected detection, insufficient nodes."""

    def test_correct_mst_triangle(self, triangle_graph):
        """Prim's produces correct MST on a connected triangle graph."""
        prim = PrimMST()
        result = prim.compute_mst(triangle_graph, "LHR")
        assert result.success is True
        assert len(result.edges) == 2  # V-1 edges
        # MST should include LHR-CDG (340) and CDG-JFK (5200) = 5540
        # Not LHR-JFK (5500) because 340+5200=5540 < 5500+5200 or 340+5500
        assert result.total_cost == 340 + 5200

    def test_disconnected_graph_detection(self, disconnected_graph):
        """Prim's detects disconnected graph and reports components."""
        prim = PrimMST()
        result = prim.compute_mst(disconnected_graph, "LHR")
        assert result.success is False
        assert "disconnected" in result.message.lower()

    def test_insufficient_nodes_empty_graph(self, empty_graph):
        """Prim's on graph with 0 nodes returns insufficient nodes error."""
        prim = PrimMST()
        result = prim.compute_mst(empty_graph)
        assert result.success is False
        assert "Insufficient" in result.message

    def test_insufficient_nodes_single_node(self, single_node_graph):
        """Prim's on graph with 1 node returns insufficient nodes error."""
        prim = PrimMST()
        result = prim.compute_mst(single_node_graph, "LHR")
        assert result.success is False
        assert "Insufficient" in result.message

    def test_invalid_start_node(self, triangle_graph):
        """Prim's with non-existent start node returns error."""
        prim = PrimMST()
        result = prim.compute_mst(triangle_graph, "XYZ")
        assert result.success is False
        assert "does not exist" in result.message

    def test_mst_linear_graph(self, linear_graph):
        """Prim's on linear graph returns all edges (only spanning tree possible)."""
        prim = PrimMST()
        result = prim.compute_mst(linear_graph, "LHR")
        assert result.success is True
        assert len(result.edges) == 3  # 4 nodes -> 3 edges
        assert result.total_cost == 340 + 5200 + 5800


# ============================================================
# TestKruskalMST - Kruskal's algorithm tests
# ============================================================


class TestKruskalMST:
    """Test Kruskal's MST: correct MST, disconnected detection, cost agreement."""

    def test_correct_mst_triangle(self, triangle_graph):
        """Kruskal's produces correct MST on a connected triangle graph."""
        kruskal = KruskalMST()
        result = kruskal.compute_mst(triangle_graph)
        assert result.success is True
        assert len(result.edges) == 2  # V-1 edges
        # MST: LHR-CDG (340) + CDG-JFK (5200) = 5540
        assert result.total_cost == 340 + 5200

    def test_disconnected_graph_detection(self, disconnected_graph):
        """Kruskal's detects disconnected graph and reports components."""
        kruskal = KruskalMST()
        result = kruskal.compute_mst(disconnected_graph)
        assert result.success is False
        assert "disconnected" in result.message.lower()

    def test_insufficient_nodes_empty_graph(self, empty_graph):
        """Kruskal's on graph with 0 nodes returns insufficient nodes error."""
        kruskal = KruskalMST()
        result = kruskal.compute_mst(empty_graph)
        assert result.success is False
        assert "Insufficient" in result.message

    def test_insufficient_nodes_single_node(self, single_node_graph):
        """Kruskal's on graph with 1 node returns insufficient nodes error."""
        kruskal = KruskalMST()
        result = kruskal.compute_mst(single_node_graph)
        assert result.success is False
        assert "Insufficient" in result.message

    def test_cost_equals_prim(self, triangle_graph):
        """Kruskal's total cost equals Prim's total cost on same graph."""
        prim = PrimMST()
        kruskal = KruskalMST()
        prim_result = prim.compute_mst(triangle_graph, "LHR")
        kruskal_result = kruskal.compute_mst(triangle_graph)
        assert prim_result.total_cost == kruskal_result.total_cost

    def test_cost_equals_prim_linear(self, linear_graph):
        """Kruskal's and Prim's produce same cost on linear graph."""
        prim = PrimMST()
        kruskal = KruskalMST()
        prim_result = prim.compute_mst(linear_graph, "LHR")
        kruskal_result = kruskal.compute_mst(linear_graph)
        assert prim_result.total_cost == kruskal_result.total_cost

    def test_mst_larger_graph(self):
        """Kruskal's on a larger graph with multiple choices picks minimum edges."""
        g = WeightedGraph()
        g.add_node(Airport("AAA", "Airport A", "City A"))
        g.add_node(Airport("BBB", "Airport B", "City B"))
        g.add_node(Airport("CCC", "Airport C", "City C"))
        g.add_node(Airport("DDD", "Airport D", "City D"))
        # Edges: AAA-BBB(1), AAA-CCC(4), BBB-CCC(2), BBB-DDD(5), CCC-DDD(3)
        g.add_edge("AAA", "BBB", 1)
        g.add_edge("AAA", "CCC", 4)
        g.add_edge("BBB", "CCC", 2)
        g.add_edge("BBB", "DDD", 5)
        g.add_edge("CCC", "DDD", 3)

        kruskal = KruskalMST()
        result = kruskal.compute_mst(g)
        assert result.success is True
        assert len(result.edges) == 3  # 4 nodes -> 3 edges
        # MST should be: AAA-BBB(1), BBB-CCC(2), CCC-DDD(3) = 6
        assert result.total_cost == 6


# ============================================================
# TestUnionFind - Union-Find data structure tests
# ============================================================


class TestUnionFind:
    """Test UnionFind: make_set, find with path compression, union by rank."""

    def test_make_set_and_find(self):
        """make_set creates a set where element is its own root."""
        uf = UnionFind()
        uf.make_set("LHR")
        assert uf.find("LHR") == "LHR"

    def test_union_merges_sets(self):
        """union merges two different sets and returns True."""
        uf = UnionFind()
        uf.make_set("LHR")
        uf.make_set("CDG")
        result = uf.union("LHR", "CDG")
        assert result is True
        assert uf.find("LHR") == uf.find("CDG")

    def test_union_same_set_returns_false(self):
        """union of elements already in the same set returns False."""
        uf = UnionFind()
        uf.make_set("LHR")
        uf.make_set("CDG")
        uf.union("LHR", "CDG")
        result = uf.union("LHR", "CDG")
        assert result is False

    def test_path_compression(self):
        """After find, path compression flattens the tree."""
        uf = UnionFind()
        uf.make_set("AAA")
        uf.make_set("BBB")
        uf.make_set("CCC")
        uf.make_set("DDD")
        # Create chain: AAA <- BBB <- CCC <- DDD
        uf.union("AAA", "BBB")
        uf.union("BBB", "CCC")
        uf.union("CCC", "DDD")
        # Find DDD should compress the path
        root = uf.find("DDD")
        # After path compression, DDD's parent should point directly to root
        assert uf._parent["DDD"] == root

    def test_union_by_rank_balances(self):
        """Union by rank attaches smaller tree under root of larger tree."""
        uf = UnionFind()
        uf.make_set("AAA")
        uf.make_set("BBB")
        uf.make_set("CCC")
        uf.make_set("DDD")
        # Build one larger group
        uf.union("AAA", "BBB")  # rank of root becomes 1
        uf.union("CCC", "DDD")  # rank of root becomes 1
        # Union two rank-1 trees
        uf.union("AAA", "CCC")
        # All should be in same set
        root = uf.find("AAA")
        assert uf.find("BBB") == root
        assert uf.find("CCC") == root
        assert uf.find("DDD") == root

    def test_multiple_disjoint_sets(self):
        """Multiple disjoint sets remain separate until explicitly unioned."""
        uf = UnionFind()
        uf.make_set("AAA")
        uf.make_set("BBB")
        uf.make_set("CCC")
        uf.union("AAA", "BBB")
        # CCC should remain separate
        assert uf.find("AAA") == uf.find("BBB")
        assert uf.find("CCC") != uf.find("AAA")

    def test_find_single_element(self):
        """Find on a single element set returns the element itself."""
        uf = UnionFind()
        uf.make_set("XYZ")
        assert uf.find("XYZ") == "XYZ"

    def test_union_chain_all_connected(self):
        """Unioning multiple elements in chain results in all sharing same root."""
        uf = UnionFind()
        nodes = ["AAA", "BBB", "CCC", "DDD", "EEE"]
        for n in nodes:
            uf.make_set(n)
        for i in range(len(nodes) - 1):
            uf.union(nodes[i], nodes[i + 1])
        # All should have same root
        root = uf.find(nodes[0])
        for n in nodes:
            assert uf.find(n) == root
