"""Undirected weighted graph backed by an adjacency list.

Internal storage is fully encapsulated (name-mangled ``__adjacency``); callers
interact only through public methods, satisfying information hiding (Req 20.1).
"""

from typing import Dict, List

from models.route import Route


class Graph:
    """Airport network as an undirected weighted adjacency list."""

    def __init__(self) -> None:
        # Maps airport code -> list of incident Route objects.
        self.__adjacency: Dict[str, List[Route]] = {}

    # ----- airports -----------------------------------------------------
    def add_airport(self, code: str) -> None:
        """Add an airport vertex.

        Raises:
            KeyError: if the airport already exists.
            ValueError: if ``code`` is empty.
        """
        code = self._normalise(code)
        if code in self.__adjacency:
            raise KeyError(code)
        self.__adjacency[code] = []

    def has_airport(self, code: str) -> bool:
        return self._normalise(code) in self.__adjacency

    def airports(self) -> List[str]:
        """Return a sorted snapshot of airport codes."""
        return sorted(self.__adjacency.keys())

    def airport_count(self) -> int:
        return len(self.__adjacency)

    # ----- routes -------------------------------------------------------
    def add_route(self, source: str, destination: str, weight: float) -> Route:
        """Add an undirected weighted route between two existing airports.

        Raises:
            KeyError: if either endpoint does not exist.
            ValueError: if a route between the pair already exists, or the
                weight is invalid.
        """
        src = self._normalise(source)
        dst = self._normalise(destination)
        if src not in self.__adjacency:
            raise KeyError(src)
        if dst not in self.__adjacency:
            raise KeyError(dst)
        if self.has_route(src, dst):
            raise ValueError("duplicate-route")
        route = Route(src, dst, weight)  # validates weight > 0 and src != dst
        self.__adjacency[src].append(route)
        self.__adjacency[dst].append(route)
        return route

    def has_route(self, source: str, destination: str) -> bool:
        src = self._normalise(source)
        dst = self._normalise(destination)
        if src not in self.__adjacency:
            return False
        pair = frozenset((src, dst))
        return any(r.endpoints() == pair for r in self.__adjacency[src])

    def neighbors(self, code: str) -> List[Route]:
        """Return a copy of the routes incident to ``code`` (read-only use)."""
        code = self._normalise(code)
        if code not in self.__adjacency:
            raise KeyError(code)
        return list(self.__adjacency[code])

    def routes(self) -> List[Route]:
        """Return each undirected route exactly once."""
        seen = set()
        result: List[Route] = []
        for incident in self.__adjacency.values():
            for route in incident:
                key = route.endpoints()
                if key not in seen:
                    seen.add(key)
                    result.append(route)
        return result

    def edge_count(self) -> int:
        return len(self.routes())

    # ----- status -------------------------------------------------------
    def is_empty(self) -> bool:
        return not self.__adjacency

    # ----- helpers ------------------------------------------------------
    @staticmethod
    def _normalise(code: str) -> str:
        normalised = str(code).strip().upper()
        if not normalised:
            raise ValueError("Airport code must be a non-empty string.")
        return normalised
