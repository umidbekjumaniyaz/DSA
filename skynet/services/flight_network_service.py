"""Flight Network Service composing graph data structures and algorithms.

Provides a high-level business interface for managing the flight network,
computing shortest paths, and finding minimum spanning trees. Validates all
inputs at the service boundary before delegating to underlying data structures.
"""

from skynet.graph import WeightedGraph, DijkstraSolver, PrimMST, KruskalMST
from skynet.graph.mst_base import MSTResult
from skynet.models import Airport
from skynet.models.operation_result import OperationResult
from skynet.utils.validators import validate_iata_code, validate_numeric_range


class FlightNetworkService:
    """Service layer for flight network management.

    Composes WeightedGraph, DijkstraSolver, PrimMST, and KruskalMST to provide
    validated, high-level operations for managing airports, routes, shortest
    paths, and minimum spanning trees.
    """

    def __init__(self):
        """Initialize the service with graph and algorithm instances."""
        self._graph = WeightedGraph()
        self._dijkstra = DijkstraSolver()
        self._prim = PrimMST()
        self._kruskal = KruskalMST()

    def add_airport(self, iata_code: str, name: str, city: str) -> OperationResult:
        """Validate IATA code, create Airport, and add to graph.

        Args:
            iata_code: Three uppercase alphabetic characters identifying the airport.
            name: Full name of the airport.
            city: City where the airport is located.

        Returns:
            OperationResult indicating success or failure with descriptive message.
        """
        if not validate_iata_code(iata_code):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid IATA code: '{iata_code}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        airport = Airport(iata_code=iata_code, name=name, city=city)
        return self._graph.add_node(airport)

    def remove_airport(self, iata_code: str) -> OperationResult:
        """Remove an airport and all associated routes from the network.

        Args:
            iata_code: IATA code of the airport to remove.

        Returns:
            OperationResult indicating success or failure with descriptive message.
        """
        if not validate_iata_code(iata_code):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid IATA code: '{iata_code}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        return self._graph.remove_node(iata_code)

    def add_route(self, src: str, dest: str, distance: int) -> OperationResult:
        """Validate and add a bidirectional route between two airports.

        Args:
            src: Source airport IATA code.
            dest: Destination airport IATA code.
            distance: Distance in kilometers (1 to 99999 inclusive).

        Returns:
            OperationResult indicating success or failure with descriptive message.
        """
        if not validate_iata_code(src):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid source IATA code: '{src}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        if not validate_iata_code(dest):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid destination IATA code: '{dest}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        if not validate_numeric_range(distance, 1, 99999):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid distance: {distance}. "
                    "Must be an integer between 1 and 99999 inclusive."
                ),
            )

        return self._graph.add_edge(src, dest, distance)

    def remove_route(self, src: str, dest: str) -> OperationResult:
        """Remove a route between two airports.

        Args:
            src: Source airport IATA code.
            dest: Destination airport IATA code.

        Returns:
            OperationResult indicating success or failure with descriptive message.
        """
        if not validate_iata_code(src):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid source IATA code: '{src}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        if not validate_iata_code(dest):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid destination IATA code: '{dest}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        return self._graph.remove_edge(src, dest)

    def shortest_path(self, src: str, dest: str) -> OperationResult:
        """Compute the shortest path between two airports using Dijkstra's algorithm.

        Args:
            src: Source airport IATA code.
            dest: Destination airport IATA code.

        Returns:
            OperationResult with data containing path and distance on success.
        """
        if not validate_iata_code(src):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid source IATA code: '{src}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        if not validate_iata_code(dest):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid destination IATA code: '{dest}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        return self._dijkstra.compute_shortest_path(self._graph, src, dest)

    def compute_mst_prim(self, start: str) -> MSTResult:
        """Compute the Minimum Spanning Tree using Prim's algorithm.

        Args:
            start: IATA code of the starting airport node.

        Returns:
            MSTResult with MST edges and total cost, or failure information.
        """
        if not validate_iata_code(start):
            return MSTResult(
                success=False,
                edges=[],
                total_cost=0,
                message=(
                    f"Invalid IATA code: '{start}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        return self._prim.compute_mst(self._graph, start)

    def compute_mst_kruskal(self) -> MSTResult:
        """Compute the Minimum Spanning Tree using Kruskal's algorithm.

        Returns:
            MSTResult with MST edges and total cost, or failure information.
        """
        return self._kruskal.compute_mst(self._graph)

    def display_network(self) -> str:
        """Display the flight network as an adjacency list representation.

        Returns:
            String representation of the network showing all airports and routes.
        """
        return self._graph.display()

    @property
    def graph(self) -> WeightedGraph:
        """Expose graph for other services (e.g., emergency route planner).

        Returns:
            The underlying WeightedGraph instance.
        """
        return self._graph
