"""Contingency service: backtracking alternative-path enumeration."""

from algorithms.backtracking import enumerate_paths
from data_structures.graph import Graph

from .results import ErrorCode, OperationResult


class ContingencyService:
    """Phase 5 rerouting when a hub becomes unavailable."""

    def __init__(self, graph: Graph) -> None:
        self.__graph = graph

    def enumerate_paths(self, source: str, destination: str,
                        unavailable_hub: str = None) -> OperationResult:
        if self.__graph.is_empty():
            return OperationResult.failure(ErrorCode.EMPTY_GRAPH)
        src = str(source).strip().upper()
        dst = str(destination).strip().upper()
        for code in (src, dst):
            if not self.__graph.has_airport(code):
                return OperationResult.failure(ErrorCode.MISSING_AIRPORT, code=code)
        hub = str(unavailable_hub).strip().upper() if unavailable_hub else None
        if hub and not self.__graph.has_airport(hub):
            return OperationResult.failure(ErrorCode.MISSING_AIRPORT, code=hub)

        paths = enumerate_paths(self.__graph, src, dst, hub)
        if not paths:
            return OperationResult.failure(
                ErrorCode.NO_AVAILABLE_ROUTE, src=src, dst=dst
            )
        listing = "\n".join(" -> ".join(p) for p in paths)
        return OperationResult.success(
            payload=paths,
            message=f"{len(paths)} alternative path(s) found:\n{listing}",
        )
