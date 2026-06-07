"""Weighted graph implementation using adjacency list for flight network management."""

from typing import Dict, List, Tuple

from skynet.models.airport import Airport
from skynet.models.operation_result import OperationResult


class WeightedGraph:
    """Weighted undirected graph using adjacency list representation.

    Stores airport nodes and bidirectional weighted edges representing
    flight routes between airports. Each edge is stored in both endpoints'
    adjacency lists to represent bidirectionality.

    Attributes:
        _nodes: Dictionary mapping IATA codes to Airport objects.
        _adjacency: Dictionary mapping IATA codes to lists of (neighbor, weight) tuples.
    """

    def __init__(self) -> None:
        """Initialize an empty weighted graph."""
        self._nodes: Dict[str, Airport] = {}
        self._adjacency: Dict[str, List[Tuple[str, int]]] = {}

    def add_node(self, airport: Airport) -> OperationResult:
        """Add an airport node to the graph.

        Args:
            airport: Airport object with a valid IATA code.

        Returns:
            OperationResult indicating success or failure (duplicate node).
        """
        iata_code = airport.iata_code
        if iata_code in self._nodes:
            return OperationResult(
                success=False,
                message=f"Airport '{iata_code}' already exists in the network.",
            )

        self._nodes[iata_code] = airport
        self._adjacency[iata_code] = []
        return OperationResult(
            success=True,
            message=f"Airport '{iata_code}' ({airport.name}, {airport.city}) added to the network.",
            data=airport,
        )

    def remove_node(self, iata_code: str) -> OperationResult:
        """Remove an airport node and all associated edges from the graph.

        Cascades deletion to remove the node from all other nodes' adjacency lists.

        Args:
            iata_code: The IATA code of the airport to remove.

        Returns:
            OperationResult indicating success or failure (node not found).
        """
        if iata_code not in self._nodes:
            return OperationResult(
                success=False,
                message=f"Airport '{iata_code}' does not exist in the network.",
            )

        # Remove this node from all other nodes' adjacency lists
        for neighbor_code in list(self._adjacency.keys()):
            if neighbor_code != iata_code:
                self._adjacency[neighbor_code] = [
                    (dest, weight)
                    for dest, weight in self._adjacency[neighbor_code]
                    if dest != iata_code
                ]

        # Remove the node's own adjacency list and node record
        del self._adjacency[iata_code]
        removed_airport = self._nodes.pop(iata_code)

        return OperationResult(
            success=True,
            message=f"Airport '{iata_code}' and all associated routes removed from the network.",
            data=removed_airport,
        )

    def add_edge(self, src: str, dest: str, weight: int) -> OperationResult:
        """Add a bidirectional weighted edge between two airport nodes.

        Args:
            src: Source airport IATA code.
            dest: Destination airport IATA code.
            weight: Edge weight (distance in km), must be between 1 and 99999 inclusive.

        Returns:
            OperationResult indicating success or failure.
        """
        # Validate that both nodes exist
        if src not in self._nodes:
            return OperationResult(
                success=False,
                message=f"Source airport '{src}' does not exist in the network.",
            )
        if dest not in self._nodes:
            return OperationResult(
                success=False,
                message=f"Destination airport '{dest}' does not exist in the network.",
            )

        # Validate weight range
        if not (1 <= weight <= 99999):
            return OperationResult(
                success=False,
                message=f"Edge weight {weight} is invalid. Must be between 1 and 99999 inclusive.",
            )

        # Check for duplicate edge
        if self.has_edge(src, dest):
            return OperationResult(
                success=False,
                message=f"Route between '{src}' and '{dest}' already exists.",
            )

        # Add bidirectional edge
        self._adjacency[src].append((dest, weight))
        self._adjacency[dest].append((src, weight))

        return OperationResult(
            success=True,
            message=f"Route added: {src} <-> {dest} (weight: {weight} km).",
        )

    def remove_edge(self, src: str, dest: str) -> OperationResult:
        """Remove a bidirectional edge between two airport nodes.

        Args:
            src: Source airport IATA code.
            dest: Destination airport IATA code.

        Returns:
            OperationResult indicating success or failure.
        """
        # Validate that both nodes exist
        if src not in self._nodes:
            return OperationResult(
                success=False,
                message=f"Source airport '{src}' does not exist in the network.",
            )
        if dest not in self._nodes:
            return OperationResult(
                success=False,
                message=f"Destination airport '{dest}' does not exist in the network.",
            )

        # Check that edge exists
        if not self.has_edge(src, dest):
            return OperationResult(
                success=False,
                message=f"No route exists between '{src}' and '{dest}'.",
            )

        # Remove from both adjacency lists
        self._adjacency[src] = [
            (d, w) for d, w in self._adjacency[src] if d != dest
        ]
        self._adjacency[dest] = [
            (d, w) for d, w in self._adjacency[dest] if d != src
        ]

        return OperationResult(
            success=True,
            message=f"Route removed: {src} <-> {dest}.",
        )

    def get_neighbors(self, iata_code: str) -> List[Tuple[str, int]]:
        """Get all adjacent nodes with their edge weights.

        Args:
            iata_code: The IATA code of the airport to query.

        Returns:
            List of (neighbor_iata_code, weight) tuples.
            Returns empty list if node does not exist.
        """
        if iata_code not in self._adjacency:
            return []
        return list(self._adjacency[iata_code])

    def get_all_nodes(self) -> List[str]:
        """Get all node IATA codes in the graph.

        Returns:
            List of all IATA codes currently in the graph.
        """
        return list(self._nodes.keys())

    def get_all_edges(self) -> List[Tuple[str, str, int]]:
        """Get all unique edges in the graph (no duplicates).

        Since edges are bidirectional, each edge is reported only once.
        The edge is reported with the lexicographically smaller node first.

        Returns:
            List of (src, dest, weight) tuples representing all unique edges.
        """
        edges: List[Tuple[str, str, int]] = []
        seen: set = set()

        for node, neighbors in self._adjacency.items():
            for neighbor, weight in neighbors:
                # Create a canonical edge representation to avoid duplicates
                edge_key = (min(node, neighbor), max(node, neighbor))
                if edge_key not in seen:
                    seen.add(edge_key)
                    edges.append((edge_key[0], edge_key[1], weight))

        return edges

    def has_node(self, iata_code: str) -> bool:
        """Check if a node exists in the graph.

        Args:
            iata_code: The IATA code to check.

        Returns:
            True if the node exists, False otherwise.
        """
        return iata_code in self._nodes

    def has_edge(self, src: str, dest: str) -> bool:
        """Check if an edge exists between two nodes.

        Args:
            src: Source airport IATA code.
            dest: Destination airport IATA code.

        Returns:
            True if the edge exists, False otherwise.
        """
        if src not in self._adjacency:
            return False
        return any(d == dest for d, _ in self._adjacency[src])

    def node_count(self) -> int:
        """Get the number of nodes in the graph.

        Returns:
            The number of airport nodes currently in the graph.
        """
        return len(self._nodes)

    def edge_count(self) -> int:
        """Get the number of unique edges in the graph.

        Since each edge is stored bidirectionally, the actual count is
        half the total number of entries across all adjacency lists.

        Returns:
            The number of unique edges (not double-counted).
        """
        total_entries = sum(len(neighbors) for neighbors in self._adjacency.values())
        return total_entries // 2

    def display(self) -> str:
        """Return an adjacency list representation of the graph.

        Returns:
            A string showing each node and its connections with weights.
            Returns a message indicating empty network if no nodes exist.
        """
        if not self._nodes:
            return "Flight network is empty. No airports registered."

        lines: List[str] = []
        lines.append("Flight Network (Adjacency List):")
        lines.append(f"Airports: {self.node_count()} | Routes: {self.edge_count()}")
        lines.append("-" * 40)

        for iata_code in sorted(self._nodes.keys()):
            airport = self._nodes[iata_code]
            neighbors = self._adjacency[iata_code]
            if neighbors:
                connections = ", ".join(
                    f"{dest}({weight})" for dest, weight in sorted(neighbors)
                )
                lines.append(f"  {iata_code} ({airport.name}) -> {connections}")
            else:
                lines.append(f"  {iata_code} ({airport.name}) -> [no routes]")

        return "\n".join(lines)

    def get_node(self, iata_code: str) -> Airport | None:
        """Get the Airport object for a given IATA code.

        Args:
            iata_code: The IATA code to look up.

        Returns:
            The Airport object if found, None otherwise.
        """
        return self._nodes.get(iata_code)
