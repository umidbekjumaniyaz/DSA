"""Prim's Minimum Spanning Tree algorithm implementation."""

import heapq
from collections import deque
from typing import Dict, List, Optional, Set, Tuple

from skynet.graph.mst_base import MSTAlgorithm, MSTResult
from skynet.graph.weighted_graph import WeightedGraph


class PrimMST(MSTAlgorithm):
    """Prim's algorithm for computing the Minimum Spanning Tree.

    Uses a min-heap (priority queue) to greedily select the minimum-weight
    edge crossing the cut between visited and unvisited nodes at each step.
    Starts from a specified node and grows the MST one edge at a time.

    Handles edge cases:
    - Graphs with fewer than 2 nodes (insufficient for spanning tree)
    - Start node not present in graph
    - Disconnected graphs (reports connected components)
    """

    def compute_mst(self, graph: WeightedGraph, start_node: Optional[str] = None) -> MSTResult:
        """Compute MST using Prim's algorithm starting from start_node.

        Args:
            graph: The weighted graph to compute the MST for.
            start_node: The node to start building the MST from.
                        If None, uses the first node in the graph.

        Returns:
            MSTResult with the MST edges, total cost, and status message.
        """
        # Edge case: fewer than 2 nodes
        if graph.node_count() < 2:
            return MSTResult(
                success=False,
                edges=[],
                total_cost=0,
                message="Insufficient nodes to form a spanning tree.",
            )

        all_nodes = graph.get_all_nodes()

        # Default start_node if not specified
        if start_node is None:
            start_node = all_nodes[0]

        # Validate start_node exists
        if not graph.has_node(start_node):
            return MSTResult(
                success=False,
                edges=[],
                total_cost=0,
                message=f"Airport '{start_node}' does not exist in the network.",
            )

        # Prim's algorithm using min-heap
        visited: Set[str] = {start_node}
        mst_edges: List[Tuple[str, str, int]] = []
        total_cost = 0

        # Min-heap entries: (weight, source, destination)
        edge_heap: List[Tuple[int, str, str]] = []
        for neighbor, weight in graph.get_neighbors(start_node):
            heapq.heappush(edge_heap, (weight, start_node, neighbor))

        while edge_heap and len(visited) < graph.node_count():
            weight, src, dest = heapq.heappop(edge_heap)

            if dest in visited:
                continue

            # Add destination to visited set and edge to MST
            visited.add(dest)
            mst_edges.append((src, dest, weight))
            total_cost += weight

            # Add all edges from new node to unvisited neighbors
            for neighbor, w in graph.get_neighbors(dest):
                if neighbor not in visited:
                    heapq.heappush(edge_heap, (w, dest, neighbor))

        # Check if all nodes are connected
        if len(visited) < graph.node_count():
            # Graph is disconnected - find components using BFS
            components = self._find_components(graph)
            components_str = ", ".join(
                "{" + ",".join(sorted(component)) + "}"
                for component in components
            )
            return MSTResult(
                success=False,
                edges=[],
                total_cost=0,
                message=f"Graph is disconnected. Components: {components_str}",
            )

        # Build success message
        edge_descriptions = [
            f"  {src} -- {dest} (weight: {w})" for src, dest, w in mst_edges
        ]
        message = (
            f"MST computed successfully using Prim's Algorithm.\n"
            f"Edges ({len(mst_edges)}):\n"
            + "\n".join(edge_descriptions)
            + f"\nTotal MST cost: {total_cost}"
        )

        return MSTResult(
            success=True,
            edges=mst_edges,
            total_cost=total_cost,
            message=message,
        )

    def get_name(self) -> str:
        """Return the name of the algorithm."""
        return "Prim's Algorithm"

    def _find_components(self, graph: WeightedGraph) -> List[Set[str]]:
        """Find all connected components in the graph using BFS.

        Args:
            graph: The weighted graph to analyze.

        Returns:
            A list of sets, where each set contains the nodes of one
            connected component.
        """
        all_nodes = set(graph.get_all_nodes())
        visited: Set[str] = set()
        components: List[Set[str]] = []

        for node in graph.get_all_nodes():
            if node not in visited:
                # BFS from this node
                component: Set[str] = set()
                queue = deque([node])
                visited.add(node)

                while queue:
                    current = queue.popleft()
                    component.add(current)

                    for neighbor, _ in graph.get_neighbors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)

        return components
