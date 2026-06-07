"""Recursive backtracking route finder for emergency route planning."""

from typing import List, Set

from skynet.graph.weighted_graph import WeightedGraph
from skynet.models.path import Path


class BacktrackingSolver:
    """Finds all paths between two airports using recursive backtracking.

    Uses depth-first search with backtracking to enumerate all possible
    paths from source to destination, avoiding excluded (closed) airports
    and preventing cycles via a visited set. Marks the shortest path found.
    """

    def find_all_paths(
        self,
        graph: WeightedGraph,
        source: str,
        destination: str,
        excluded: Set[str],
    ) -> List[Path]:
        """Find all paths from source to destination avoiding excluded nodes.

        Uses recursive backtracking with a visited set to prevent cycles.
        Returns list of Path objects with legs and total distances.
        Marks the shortest path with is_shortest=True.

        Args:
            graph: The weighted graph representing the flight network.
            source: IATA code of the source airport.
            destination: IATA code of the destination airport.
            excluded: Set of IATA codes for closed airports to avoid.

        Returns:
            List of Path objects representing all valid paths found.
            The shortest path (by total_distance) has is_shortest=True.
            Returns empty list if no paths exist.
        """
        all_paths: List[Path] = []
        visited: Set[str] = set()
        visited.add(source)
        self._backtrack(
            graph, source, destination, [source], [], 0, visited, excluded, all_paths
        )

        # Mark the shortest path
        if all_paths:
            shortest_idx = min(
                range(len(all_paths)), key=lambda i: all_paths[i].total_distance
            )
            all_paths[shortest_idx].is_shortest = True

        return all_paths

    def _backtrack(
        self,
        graph: WeightedGraph,
        current: str,
        destination: str,
        path: List[str],
        legs: List,
        distance: int,
        visited: Set[str],
        excluded: Set[str],
        all_paths: List[Path],
    ) -> None:
        """Recursive backtracking helper.

        Explores all neighbors of the current node that are not visited
        and not excluded. When the destination is reached, a Path object
        is appended to all_paths. Backtracks by removing the current node
        from the path and visited set after exploring all possibilities.

        Args:
            graph: The weighted graph.
            current: Current node being explored.
            destination: Target node to reach.
            path: Current path of nodes being built.
            legs: Current list of (source, dest, weight) leg tuples.
            distance: Cumulative distance of the current path.
            visited: Set of already-visited nodes in this path.
            excluded: Set of closed airports to avoid.
            all_paths: Accumulator list for all complete paths found.
        """
        if current == destination:
            all_paths.append(
                Path(
                    nodes=list(path),
                    legs=list(legs),
                    total_distance=distance,
                    is_shortest=False,
                )
            )
            return

        for neighbor, weight in graph.get_neighbors(current):
            if neighbor not in visited and neighbor not in excluded:
                visited.add(neighbor)
                path.append(neighbor)
                legs.append((current, neighbor, weight))
                self._backtrack(
                    graph,
                    neighbor,
                    destination,
                    path,
                    legs,
                    distance + weight,
                    visited,
                    excluded,
                    all_paths,
                )
                legs.pop()
                path.pop()
                visited.remove(neighbor)
