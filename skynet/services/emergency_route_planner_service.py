"""Emergency Route Planner Service composing BacktrackingSolver and WeightedGraph.

Provides a high-level business interface for managing airport closures and
finding alternative flight routes that avoid closed airports using recursive
backtracking. Validates all inputs at the service boundary before delegating
to the underlying BacktrackingSolver.
"""

from typing import Set

from skynet.backtracking import BacktrackingSolver
from skynet.graph import WeightedGraph
from skynet.models.operation_result import OperationResult
from skynet.utils.validators import validate_iata_code
from skynet.utils.formatters import format_path


class EmergencyRoutePlannerService:
    """Service layer for emergency route planning during airport closures.

    Composes BacktrackingSolver and references a shared WeightedGraph (from
    FlightNetworkService) to find all alternative routes between airports
    while avoiding closed airports. Tracks closed airports and marks the
    shortest alternative route.
    """

    def __init__(self, graph: WeightedGraph):
        """Initialize the service with a shared graph and backtracking solver.

        Args:
            graph: Shared WeightedGraph instance from FlightNetworkService.
        """
        self._solver = BacktrackingSolver()
        self._graph = graph
        self._closed_airports: Set[str] = set()

    def close_airport(self, iata_code: str) -> OperationResult:
        """Mark an airport as closed, excluding it from route computation.

        Validates the IATA code format, checks it exists in the graph,
        and adds it to the closed airports set.

        Args:
            iata_code: Three uppercase alphabetic characters identifying the airport.

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

        if not self._graph.has_node(iata_code):
            return OperationResult(
                success=False,
                message=f"Airport '{iata_code}' does not exist in the network.",
            )

        if iata_code in self._closed_airports:
            return OperationResult(
                success=False,
                message=f"Airport '{iata_code}' is already closed.",
            )

        self._closed_airports.add(iata_code)
        return OperationResult(
            success=True,
            message=f"Airport '{iata_code}' has been closed. It will be excluded from route planning.",
            data=iata_code,
        )

    def reopen_airport(self, iata_code: str) -> OperationResult:
        """Reopen a previously closed airport, allowing it in route computation.

        Args:
            iata_code: Three uppercase alphabetic characters identifying the airport.

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

        if iata_code not in self._closed_airports:
            return OperationResult(
                success=False,
                message=f"Airport '{iata_code}' is not currently closed.",
            )

        self._closed_airports.remove(iata_code)
        return OperationResult(
            success=True,
            message=f"Airport '{iata_code}' has been reopened. It is now available for route planning.",
            data=iata_code,
        )

    def find_alternatives(self, src: str, dest: str) -> OperationResult:
        """Find all alternative routes between source and destination avoiding closed airports.

        Validates source and destination IATA codes, checks they exist in the
        graph and are not closed, then uses recursive backtracking to enumerate
        all valid paths. Displays all routes with distances and marks the shortest.

        Args:
            src: Source airport IATA code.
            dest: Destination airport IATA code.

        Returns:
            OperationResult with data containing list of Path objects on success,
            or an appropriate error/no-alternative message.
        """
        # Validate source IATA code
        if not validate_iata_code(src):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid source IATA code: '{src}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        # Validate destination IATA code
        if not validate_iata_code(dest):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid destination IATA code: '{dest}'. "
                    "Must be exactly 3 uppercase alphabetic characters."
                ),
            )

        # Check source exists in graph
        if not self._graph.has_node(src):
            return OperationResult(
                success=False,
                message=f"Source airport '{src}' does not exist in the network.",
            )

        # Check destination exists in graph
        if not self._graph.has_node(dest):
            return OperationResult(
                success=False,
                message=f"Destination airport '{dest}' does not exist in the network.",
            )

        # Check source is not closed
        if src in self._closed_airports:
            return OperationResult(
                success=False,
                message=f"Source airport '{src}' is currently closed.",
            )

        # Check destination is not closed
        if dest in self._closed_airports:
            return OperationResult(
                success=False,
                message=f"Destination airport '{dest}' is currently closed.",
            )

        # Find all paths avoiding closed airports
        paths = self._solver.find_all_paths(
            self._graph, src, dest, self._closed_airports
        )

        if not paths:
            return OperationResult(
                success=False,
                message="No alternative connection available.",
            )

        # Build display output showing all routes with distances
        lines = [f"Alternative routes from {src} to {dest}:"]
        lines.append(f"Closed airports: {sorted(self._closed_airports) if self._closed_airports else 'None'}")
        lines.append("-" * 40)

        for i, path in enumerate(paths, 1):
            route_str = format_path(path.nodes, path.total_distance)
            if path.is_shortest:
                lines.append(f"  Route {i}: {route_str} [SHORTEST]")
            else:
                lines.append(f"  Route {i}: {route_str}")

            # Show individual legs
            for leg_src, leg_dest, leg_dist in path.legs:
                lines.append(f"    {leg_src} -> {leg_dest}: {leg_dist} km")

        lines.append("-" * 40)
        lines.append(f"Total alternatives found: {len(paths)}")

        return OperationResult(
            success=True,
            message="\n".join(lines),
            data=paths,
        )

    @property
    def closed_airports(self) -> Set[str]:
        """Get the set of currently closed airports.

        Returns:
            A copy of the set of closed airport IATA codes.
        """
        return set(self._closed_airports)
