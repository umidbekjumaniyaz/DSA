"""Minimum Spanning Tree algorithms: Prim's and Kruskal's.

Both return ``(routes, total_weight)`` for a connected graph, or ``None`` when
the graph is disconnected (no spanning tree covering every airport exists,
Req 4.3). On a connected graph of ``n`` airports each returns exactly
``n - 1`` routes (Req 4.2) and the same total weight (verified by Property 6).
"""

from typing import Dict, List, Optional, Tuple

from data_structures.graph import Graph
from data_structures.max_heap import MaxHeap
from models.route import Route


def prim(graph: Graph) -> Optional[Tuple[List[Route], float]]:
    """Compute an MST using Prim's algorithm. O(E log V)."""
    airports = graph.airports()
    if not airports:
        return None
    start = airports[0]
    in_tree = {start}
    chosen: List[Route] = []
    total = 0.0

    # Min-priority queue of candidate edges via negated weight.
    pq = MaxHeap(priority_of=lambda entry: -entry[0])
    for route in graph.neighbors(start):
        pq.push((route.weight, route))

    while not pq.is_empty() and len(in_tree) < len(airports):
        weight, route = pq.pop()
        a, b = route.source, route.destination
        # Determine the endpoint not yet in the tree.
        if a in in_tree and b in in_tree:
            continue
        new_node = b if a in in_tree else a
        in_tree.add(new_node)
        chosen.append(route)
        total += weight
        for nxt in graph.neighbors(new_node):
            if nxt.other(new_node) not in in_tree:
                pq.push((nxt.weight, nxt))

    if len(in_tree) != len(airports):
        return None  # disconnected
    return (chosen, total)


class _UnionFind:
    """Disjoint-set forest with path compression and union by rank."""

    def __init__(self, items: List[str]) -> None:
        self.__parent: Dict[str, str] = {x: x for x in items}
        self.__rank: Dict[str, int] = {x: 0 for x in items}

    def find(self, x: str) -> str:
        while self.__parent[x] != x:
            self.__parent[x] = self.__parent[self.__parent[x]]
            x = self.__parent[x]
        return x

    def union(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.__rank[ra] < self.__rank[rb]:
            ra, rb = rb, ra
        self.__parent[rb] = ra
        if self.__rank[ra] == self.__rank[rb]:
            self.__rank[ra] += 1
        return True


def kruskal(graph: Graph) -> Optional[Tuple[List[Route], float]]:
    """Compute an MST using Kruskal's algorithm. O(E log E)."""
    airports = graph.airports()
    if not airports:
        return None
    uf = _UnionFind(airports)
    chosen: List[Route] = []
    total = 0.0
    for route in sorted(graph.routes(), key=lambda r: r.weight):
        if uf.union(route.source, route.destination):
            chosen.append(route)
            total += route.weight
    if len(chosen) != len(airports) - 1:
        return None  # disconnected
    return (chosen, total)
