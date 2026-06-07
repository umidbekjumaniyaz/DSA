"""Dijkstra's shortest-path algorithm over the airport network.

Reuses the project ``MaxHeap`` as a min-priority queue by negating the
distance key, avoiding a second heap implementation. Time complexity
O((V + E) log V); space O(V).
"""

from typing import List, Optional, Tuple

from data_structures.graph import Graph
from data_structures.max_heap import MaxHeap


def dijkstra(graph: Graph, source: str, destination: str
             ) -> Optional[Tuple[List[str], float]]:
    """Return the cheapest path and its total weight, or ``None``.

    The source and destination must exist in ``graph`` (validated by the
    caller). When ``source == destination`` the result is a zero-weight path
    containing only that airport (Req 3.4). Returns ``None`` when no path
    connects the two airports (Req 3.2).
    """
    src = str(source).strip().upper()
    dst = str(destination).strip().upper()

    if src == dst:
        return ([src], 0.0)

    # Min-priority queue via a max-heap on negated distance.
    pq = MaxHeap(priority_of=lambda entry: -entry[0])
    pq.push((0.0, src))
    best = {src: 0.0}
    previous = {}
    visited = set()

    while not pq.is_empty():
        dist, node = pq.pop()
        if node in visited:
            continue
        visited.add(node)
        if node == dst:
            break
        for route in graph.neighbors(node):
            neighbour = route.other(node)
            if neighbour in visited:
                continue
            candidate = dist + route.weight
            if candidate < best.get(neighbour, float("inf")):
                best[neighbour] = candidate
                previous[neighbour] = node
                pq.push((candidate, neighbour))

    if dst not in best:
        return None

    # Reconstruct path from destination back to source.
    path = [dst]
    while path[-1] != src:
        path.append(previous[path[-1]])
    path.reverse()
    return (path, best[dst])
