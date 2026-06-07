"""Recursive backtracking enumeration of alternative flight paths.

Enumerates every simple path (no repeated airport) from ``source`` to
``destination`` while treating an unavailable hub as removed from the network
(Req 14). Worst-case time is exponential in the number of airports, which is
inherent to enumerating all simple paths.
"""

from typing import List, Optional

from data_structures.graph import Graph


def enumerate_paths(graph: Graph, source: str, destination: str,
                    excluded: Optional[str] = None) -> List[List[str]]:
    """Return all simple paths from ``source`` to ``destination``.

    ``excluded`` (the unavailable hub) is omitted from every path. Endpoints
    are assumed to exist in ``graph`` (validated by the caller).
    """
    src = str(source).strip().upper()
    dst = str(destination).strip().upper()
    blocked = str(excluded).strip().upper() if excluded else None

    paths: List[List[str]] = []
    if src == blocked or dst == blocked:
        return paths

    visited = {src}
    path = [src]

    def _backtrack(node: str) -> None:
        if node == dst:
            paths.append(list(path))
            return
        for route in graph.neighbors(node):
            nxt = route.other(node)
            if nxt == blocked or nxt in visited:
                continue
            visited.add(nxt)
            path.append(nxt)
            _backtrack(nxt)
            path.pop()
            visited.remove(nxt)

    if src == dst:
        return [[src]]
    _backtrack(src)
    return paths
