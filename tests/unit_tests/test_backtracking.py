"""Unit tests for the backtracking route finder module."""

import pytest

from skynet.backtracking.route_finder import BacktrackingSolver
from skynet.graph.weighted_graph import WeightedGraph
from skynet.models.airport import Airport


def _make_airport(code: str) -> Airport:
    """Helper to create an Airport with default name/city."""
    return Airport(iata_code=code, name=f"{code} Airport", city=f"{code} City")


def _build_linear_graph() -> WeightedGraph:
    """Build a simple linear graph: A-B-C-D.

    Edges: AAA-BBB(100), BBB-CCC(200), CCC-DDD(300)
    Only one path from AAA to DDD: AAA -> BBB -> CCC -> DDD (distance 600)
    """
    graph = WeightedGraph()
    for code in ["AAA", "BBB", "CCC", "DDD"]:
        graph.add_node(_make_airport(code))
    graph.add_edge("AAA", "BBB", 100)
    graph.add_edge("BBB", "CCC", 200)
    graph.add_edge("CCC", "DDD", 300)
    return graph


def _build_diamond_graph() -> WeightedGraph:
    """Build a diamond graph: AAA connects to BBB and CCC, both connect to DDD.

    Edges: AAA-BBB(100), AAA-CCC(150), BBB-DDD(200), CCC-DDD(50)
    Two paths from AAA to DDD:
      - AAA -> BBB -> DDD (distance 300)
      - AAA -> CCC -> DDD (distance 200) <- shortest
    """
    graph = WeightedGraph()
    for code in ["AAA", "BBB", "CCC", "DDD"]:
        graph.add_node(_make_airport(code))
    graph.add_edge("AAA", "BBB", 100)
    graph.add_edge("AAA", "CCC", 150)
    graph.add_edge("BBB", "DDD", 200)
    graph.add_edge("CCC", "DDD", 50)
    return graph


def _build_graph_with_closed_airport() -> WeightedGraph:
    """Build a graph where closing an intermediate node blocks some paths.

    Topology:
      AAA -- BBB -- DDD
       |             |
      CCC ----------+

    Edges: AAA-BBB(100), BBB-DDD(200), AAA-CCC(300), CCC-DDD(400)
    If BBB is closed:
      - Only path: AAA -> CCC -> DDD (distance 700)
    If no closures:
      - Path 1: AAA -> BBB -> DDD (distance 300)
      - Path 2: AAA -> CCC -> DDD (distance 700)
    """
    graph = WeightedGraph()
    for code in ["AAA", "BBB", "CCC", "DDD"]:
        graph.add_node(_make_airport(code))
    graph.add_edge("AAA", "BBB", 100)
    graph.add_edge("BBB", "DDD", 200)
    graph.add_edge("AAA", "CCC", 300)
    graph.add_edge("CCC", "DDD", 400)
    return graph


class TestBacktrackingNormal:
    """Tests for normal backtracking route finding operations."""

    def test_find_all_paths_correct_count_diamond(self):
        """Diamond graph should yield exactly 2 paths from AAA to DDD."""
        graph = _build_diamond_graph()
        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded=set())
        assert len(paths) == 2

    def test_paths_are_valid_consecutive_nodes_have_edges(self):
        """Every consecutive pair of nodes in each path must have an edge in the graph."""
        graph = _build_diamond_graph()
        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded=set())

        for path in paths:
            for i in range(len(path.nodes) - 1):
                src = path.nodes[i]
                dest = path.nodes[i + 1]
                assert graph.has_edge(src, dest), (
                    f"No edge between consecutive nodes {src} and {dest}"
                )

    def test_shortest_path_correctly_marked(self):
        """The shortest path should have is_shortest=True, others False."""
        graph = _build_diamond_graph()
        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded=set())

        shortest_paths = [p for p in paths if p.is_shortest]
        non_shortest_paths = [p for p in paths if not p.is_shortest]

        # Exactly one should be marked shortest
        assert len(shortest_paths) == 1
        assert len(non_shortest_paths) == 1

        # The marked shortest should have the minimum distance
        assert shortest_paths[0].total_distance <= non_shortest_paths[0].total_distance

    def test_path_distances_match_sum_of_leg_weights(self):
        """Each path's total_distance must equal the sum of its leg weights."""
        graph = _build_diamond_graph()
        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded=set())

        for path in paths:
            leg_sum = sum(weight for _, _, weight in path.legs)
            assert path.total_distance == leg_sum, (
                f"Path {path.nodes}: total_distance={path.total_distance} "
                f"but sum of legs={leg_sum}"
            )

    def test_all_paths_are_acyclic(self):
        """No path should contain repeated nodes (acyclic)."""
        graph = _build_diamond_graph()
        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded=set())

        for path in paths:
            assert len(path.nodes) == len(set(path.nodes)), (
                f"Path contains repeated nodes: {path.nodes}"
            )

    def test_linear_graph_finds_single_path(self):
        """Linear graph AAA-BBB-CCC-DDD should yield exactly 1 path."""
        graph = _build_linear_graph()
        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded=set())

        assert len(paths) == 1
        assert paths[0].nodes == ["AAA", "BBB", "CCC", "DDD"]
        assert paths[0].total_distance == 600
        assert paths[0].is_shortest is True


class TestBacktrackingEdgeCases:
    """Tests for edge cases in backtracking route finding."""

    def test_direct_route_only(self):
        """When only a direct edge exists, should find exactly 1 path."""
        graph = WeightedGraph()
        graph.add_node(_make_airport("AAA"))
        graph.add_node(_make_airport("BBB"))
        graph.add_edge("AAA", "BBB", 500)

        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "BBB", excluded=set())

        assert len(paths) == 1
        assert paths[0].nodes == ["AAA", "BBB"]
        assert paths[0].total_distance == 500
        assert paths[0].is_shortest is True

    def test_no_path_exists_returns_empty_list(self):
        """When no path exists between source and destination, return empty list."""
        graph = WeightedGraph()
        graph.add_node(_make_airport("AAA"))
        graph.add_node(_make_airport("BBB"))
        # No edge between them

        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "BBB", excluded=set())

        assert paths == []

    def test_closed_airport_excludes_paths_through_it(self):
        """Paths through a closed airport should not be returned."""
        graph = _build_graph_with_closed_airport()
        solver = BacktrackingSolver()

        # Without closure: should find 2 paths
        all_paths = solver.find_all_paths(graph, "AAA", "DDD", excluded=set())
        assert len(all_paths) == 2

        # With BBB closed: only the path via CCC remains
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded={"BBB"})
        assert len(paths) == 1
        assert "BBB" not in paths[0].nodes
        assert paths[0].nodes == ["AAA", "CCC", "DDD"]
        assert paths[0].total_distance == 700

    def test_all_paths_blocked_by_closed_airports(self):
        """If all intermediate airports are closed, return empty list."""
        graph = _build_graph_with_closed_airport()
        solver = BacktrackingSolver()

        # Close both intermediate nodes BBB and CCC
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded={"BBB", "CCC"})
        assert paths == []

    def test_source_equals_destination(self):
        """When source equals destination, should find a trivial path."""
        graph = _build_linear_graph()
        solver = BacktrackingSolver()
        paths = solver.find_all_paths(graph, "AAA", "AAA", excluded=set())

        # Source == destination means immediate match
        assert len(paths) == 1
        assert paths[0].nodes == ["AAA"]
        assert paths[0].total_distance == 0


class TestBacktrackingErrors:
    """Tests for error handling in backtracking route finding.

    Note: The BacktrackingSolver operates directly on graph data. Source/destination
    validation is expected at the service layer. These tests verify the solver's
    behavior when given nodes that exist or don't exist in the graph.
    """

    def test_source_not_in_graph_returns_empty(self):
        """If source is not in the graph, get_neighbors returns [] so no paths found."""
        graph = _build_linear_graph()
        solver = BacktrackingSolver()

        # "ZZZ" is not in the graph - the solver will have no neighbors to explore
        paths = solver.find_all_paths(graph, "ZZZ", "DDD", excluded=set())
        assert paths == []

    def test_destination_not_in_graph_returns_empty(self):
        """If destination is not in the graph, no path can reach it."""
        graph = _build_linear_graph()
        solver = BacktrackingSolver()

        # "ZZZ" is not in the graph - destination can never be reached
        paths = solver.find_all_paths(graph, "AAA", "ZZZ", excluded=set())
        assert paths == []

    def test_closed_airport_as_source_with_exclusion(self):
        """If source is in the excluded set, behavior depends on implementation.

        The solver adds source to visited first, so if source is excluded
        but still the starting point, it should still attempt to find paths
        from itself (since source is added to visited, not checked against excluded).
        """
        graph = _build_linear_graph()
        solver = BacktrackingSolver()

        # Excluding the source - the solver still starts from source
        # because excluded is only checked for neighbors
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded={"AAA"})
        # Source is the starting point; excluded only blocks neighbors from being visited
        # Since AAA is the source and is already added to visited (not neighbors check),
        # paths should still be found
        assert len(paths) == 1
        assert paths[0].nodes == ["AAA", "BBB", "CCC", "DDD"]

    def test_closed_airport_as_destination_blocks_paths(self):
        """If destination is in the excluded set, neighbors check prevents reaching it.

        Since neighbors are checked against excluded before being visited,
        and the destination must be reached as a neighbor, excluding destination
        means it can never be visited from any node.
        """
        graph = _build_linear_graph()
        solver = BacktrackingSolver()

        # DDD is excluded - since it's checked as a neighbor from CCC, it's blocked
        paths = solver.find_all_paths(graph, "AAA", "DDD", excluded={"DDD"})
        assert paths == []
