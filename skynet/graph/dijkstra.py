"""Dijkstra's shortest path algorithm implementation for flight network routing."""

import heapq
from typing import Dict, List, Optional, Tuple

from skynet.graph.weighted_graph import WeightedGraph
from skynet.models.operation_result import OperationResult


class DijkstraSolver:
    """Computes shortest paths in a weighted graph using Dijkstra's algorithm.

    Uses a min-heap priority queue (Python heapq) to process nodes in order
    of cumulative minimum distance from the source. Reconstructs the optimal
    path via a predecessor map.
    """

    def compute_shortest_path(
        self, graph: WeightedGraph, source: str, destination: str
    ) -> OperationResult:
        """Compute the shortest path between two airports using Dijkstra's algorithm.

        Args:
            graph: The weighted graph representing the flight network.
            source: IATA code of the source airport.
            destination: IATA code of the destination airport.

        Returns:
            OperationResult with data being a dict:
            {'path': ['LHR', 'CDG', 'JFK'], 'distance': 6200}
            On failure, returns success=False with descriptive error message.
        """
        # Validate that source exists in graph
        if not graph.has_node(source):
            return OperationResult(
                success=False,
                message=f"Source airport '{source}' does not exist in the network.",
            )

        # Validate that destination exists in graph
        if not graph.has_node(destination):
            return OperationResult(
                success=False,
                message=f"Destination airport '{destination}' does not exist in the network.",
            )

        # Handle source equals destination
        if source == destination:
            return OperationResult(
                success=True,
                message=f"Source and destination are the same airport '{source}'. Distance is 0.",
                data={"path": [source], "distance": 0},
            )

        # Initialize distances to infinity for all nodes, 0 for source
        all_nodes = graph.get_all_nodes()
        distances: Dict[str, float] = {node: float("inf") for node in all_nodes}
        distances[source] = 0

        # Predecessor map for path reconstruction
        predecessors: Dict[str, Optional[str]] = {node: None for node in all_nodes}

        # Min-heap priority queue with (distance, node) entries
        # Using a counter to break ties deterministically
        counter = 0
        priority_queue: List[Tuple[float, int, str]] = [(0, counter, source)]

        # Track visited nodes
        visited: set = set()

        while priority_queue:
            current_distance, _, current_node = heapq.heappop(priority_queue)

            # Skip if already visited (stale entry in the queue)
            if current_node in visited:
                continue

            visited.add(current_node)

            # Early termination if we reached the destination
            if current_node == destination:
                break

            # Process each neighbor
            for neighbor, weight in graph.get_neighbors(current_node):
                if neighbor in visited:
                    continue

                new_distance = current_distance + weight

                # If new distance is better, update
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    counter += 1
                    heapq.heappush(priority_queue, (new_distance, counter, neighbor))

        # Check if destination is reachable
        if distances[destination] == float("inf"):
            return OperationResult(
                success=False,
                message=f"No connection exists between '{source}' and '{destination}'.",
            )

        # Reconstruct path from predecessor map
        path = self._reconstruct_path(predecessors, source, destination)
        total_distance = int(distances[destination])

        return OperationResult(
            success=True,
            message=(
                f"Shortest path from '{source}' to '{destination}': "
                f"{' -> '.join(path)} (total distance: {total_distance} km)."
            ),
            data={"path": path, "distance": total_distance},
        )

    def _reconstruct_path(
        self,
        predecessors: Dict[str, Optional[str]],
        source: str,
        destination: str,
    ) -> List[str]:
        """Reconstruct the shortest path from predecessor map.

        Traces back from destination to source using the predecessor map,
        then reverses to get the path in source-to-destination order.

        Args:
            predecessors: Map of each node to its predecessor on shortest path.
            source: The starting node.
            destination: The ending node.

        Returns:
            Ordered list of IATA codes from source to destination.
        """
        path: List[str] = []
        current: Optional[str] = destination

        while current is not None:
            path.append(current)
            current = predecessors[current]

        path.reverse()
        return path
