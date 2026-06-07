"""Route planning service: airports, routes, cheapest route, backup network."""

from algorithms.dijkstra import dijkstra
from algorithms.mst import kruskal, prim
from data_structures.graph import Graph

from .results import ErrorCode, OperationResult


class RoutePlanningService:
    """Orchestrates Phase 1 graph use cases over a shared :class:`Graph`."""

    def __init__(self, graph: Graph) -> None:
        self.__graph = graph

    @property
    def graph(self) -> Graph:
        return self.__graph

    # ----- airports / routes -------------------------------------------
    def add_airport(self, code: str) -> OperationResult:
        try:
            self.__graph.add_airport(code)
        except KeyError:
            return OperationResult.failure(
                ErrorCode.DUPLICATE_AIRPORT, code=str(code).strip().upper()
            )
        except ValueError as exc:
            return OperationResult.failure(ErrorCode.INVALID_INPUT, detail=str(exc))
        return OperationResult.success(
            message=f"Airport '{str(code).strip().upper()}' added."
        )

    def add_route(self, source: str, destination: str, weight) -> OperationResult:
        try:
            weight_val = float(weight)
        except (TypeError, ValueError):
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT, detail="route weight must be numeric"
            )
        try:
            route = self.__graph.add_route(source, destination, weight_val)
        except KeyError as exc:
            return OperationResult.failure(
                ErrorCode.MISSING_AIRPORT, code=str(exc.args[0])
            )
        except ValueError as exc:
            if str(exc) == "duplicate-route":
                return OperationResult.failure(
                    ErrorCode.DUPLICATE_ROUTE,
                    a=str(source).strip().upper(),
                    b=str(destination).strip().upper(),
                )
            return OperationResult.failure(ErrorCode.INVALID_INPUT, detail=str(exc))
        return OperationResult.success(payload=route, message=f"Route added: {route}.")

    def display_network(self) -> OperationResult:
        if self.__graph.is_empty():
            return OperationResult.failure(ErrorCode.EMPTY_GRAPH)
        lines = []
        for code in self.__graph.airports():
            neighbours = self.__graph.neighbors(code)
            if neighbours:
                parts = ", ".join(
                    f"{r.other(code)}({r.weight:g})" for r in neighbours
                )
            else:
                parts = "(no routes)"
            lines.append(f"{code}: {parts}")
        return OperationResult.success(payload="\n".join(lines))

    # ----- algorithms ---------------------------------------------------
    def find_cheapest_route(self, source: str, destination: str) -> OperationResult:
        if self.__graph.is_empty():
            return OperationResult.failure(ErrorCode.EMPTY_GRAPH)
        src = str(source).strip().upper()
        dst = str(destination).strip().upper()
        if not self.__graph.has_airport(src):
            return OperationResult.failure(ErrorCode.MISSING_AIRPORT, code=src)
        if not self.__graph.has_airport(dst):
            return OperationResult.failure(ErrorCode.MISSING_AIRPORT, code=dst)
        result = dijkstra(self.__graph, src, dst)
        if result is None:
            return OperationResult.failure(
                ErrorCode.NO_AVAILABLE_ROUTE, src=src, dst=dst
            )
        path, total = result
        return OperationResult.success(
            payload={"path": path, "total_cost": total},
            message=f"Cheapest route: {' -> '.join(path)} (cost {total:g}).",
        )

    def generate_backup_network(self, algorithm: str = "prim") -> OperationResult:
        if self.__graph.is_empty():
            return OperationResult.failure(ErrorCode.EMPTY_GRAPH)
        algo = (algorithm or "prim").strip().lower()
        compute = kruskal if algo == "kruskal" else prim
        result = compute(self.__graph)
        if result is None:
            return OperationResult.failure(ErrorCode.DISCONNECTED_GRAPH)
        routes, total = result
        listing = "\n".join(str(r) for r in routes) if routes else "(single airport)"
        return OperationResult.success(
            payload={"routes": routes, "total_cost": total, "algorithm": algo},
            message=f"Backup network ({algo}), total cost {total:g}:\n{listing}",
        )
