"""Union-Find (Disjoint Set Union) data structure for cycle detection in MST algorithms."""

from typing import Dict


class UnionFind:
    """Union-Find data structure with path compression and union by rank.

    Used by Kruskal's MST algorithm to efficiently detect cycles
    when adding edges to the spanning tree.
    """

    def __init__(self):
        self._parent: Dict[str, str] = {}
        self._rank: Dict[str, int] = {}

    def make_set(self, item: str):
        """Create a new set containing only this item.

        Args:
            item: The element to create a singleton set for.
        """
        self._parent[item] = item
        self._rank[item] = 0

    def find(self, item: str) -> str:
        """Find the root representative of the set containing item.

        Uses path compression to flatten the tree structure,
        making subsequent lookups faster.

        Args:
            item: The element to find the root for.

        Returns:
            The root representative of the set containing item.
        """
        if self._parent[item] != item:
            self._parent[item] = self.find(self._parent[item])
        return self._parent[item]

    def union(self, a: str, b: str) -> bool:
        """Merge the sets containing elements a and b using union by rank.

        Attaches the shorter tree under the root of the taller tree
        to keep the structure balanced.

        Args:
            a: An element in the first set.
            b: An element in the second set.

        Returns:
            True if the sets were merged (elements were in different sets),
            False if both elements were already in the same set.
        """
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        if self._rank[root_a] < self._rank[root_b]:
            self._parent[root_a] = root_b
        elif self._rank[root_a] > self._rank[root_b]:
            self._parent[root_b] = root_a
        else:
            self._parent[root_b] = root_a
            self._rank[root_a] += 1
        return True
