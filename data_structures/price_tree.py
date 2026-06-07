"""Self-balancing AVL tree for flight prices with range queries.

Maintaining the AVL height-balance invariant keeps insertion, exact search,
and range search at O(log n) (Req 8.4). Each node stores a price key together
with the list of payloads inserted at that price so duplicate prices are
supported without breaking the balance guarantees.
"""

from typing import List, Optional


class _AVLNode:
    __slots__ = ("key", "payloads", "left", "right", "height")

    def __init__(self, key: float, payload: object) -> None:
        self.key = key
        self.payloads: List[object] = [payload]
        self.left: Optional["_AVLNode"] = None
        self.right: Optional["_AVLNode"] = None
        self.height = 1


class AVLTree:
    """An AVL tree keyed by numeric price."""

    def __init__(self) -> None:
        self.__root: Optional[_AVLNode] = None
        self.__count = 0

    # ----- public API ---------------------------------------------------
    def insert(self, price: float, payload: object = None) -> None:
        """Insert ``price`` (with optional payload) and rebalance."""
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise ValueError("price must be numeric.")
        self.__root = self.__insert(self.__root, float(price), payload)
        self.__count += 1

    def contains(self, price: float) -> bool:
        """Return whether ``price`` is present (O(log n))."""
        node = self.__root
        while node is not None:
            if price == node.key:
                return True
            node = node.left if price < node.key else node.right
        return False

    def search(self, price: float) -> Optional[List[object]]:
        """Return payloads stored at ``price`` or ``None`` if absent."""
        node = self.__root
        while node is not None:
            if price == node.key:
                return list(node.payloads)
            node = node.left if price < node.key else node.right
        return None

    def range_search(self, low: float, high: float) -> List[float]:
        """Return all stored prices within the inclusive ``[low, high]``.

        Returns an empty list when ``low > high`` (Req 8.5). Prices are
        returned in ascending order; a price inserted ``k`` times appears
        ``k`` times.
        """
        result: List[float] = []
        if low > high:
            return result
        self.__range(self.__root, low, high, result)
        return result

    def height(self) -> int:
        return self.__height(self.__root)

    def size(self) -> int:
        return self.__count

    def is_empty(self) -> bool:
        return self.__root is None

    # ----- AVL internals ------------------------------------------------
    def __insert(self, node: Optional[_AVLNode], key: float, payload: object):
        if node is None:
            return _AVLNode(key, payload)
        if key == node.key:
            node.payloads.append(payload)
            return node
        if key < node.key:
            node.left = self.__insert(node.left, key, payload)
        else:
            node.right = self.__insert(node.right, key, payload)

        node.height = 1 + max(self.__height(node.left), self.__height(node.right))
        return self.__rebalance(node, key)

    def __rebalance(self, node: _AVLNode, key: float) -> _AVLNode:
        balance = self.__balance_factor(node)
        # Left-heavy
        if balance > 1:
            if key < node.left.key:  # left-left
                return self.__rotate_right(node)
            node.left = self.__rotate_left(node.left)  # left-right
            return self.__rotate_right(node)
        # Right-heavy
        if balance < -1:
            if key > node.right.key:  # right-right
                return self.__rotate_left(node)
            node.right = self.__rotate_right(node.right)  # right-left
            return self.__rotate_left(node)
        return node

    def __rotate_left(self, z: _AVLNode) -> _AVLNode:
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        z.height = 1 + max(self.__height(z.left), self.__height(z.right))
        y.height = 1 + max(self.__height(y.left), self.__height(y.right))
        return y

    def __rotate_right(self, z: _AVLNode) -> _AVLNode:
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        z.height = 1 + max(self.__height(z.left), self.__height(z.right))
        y.height = 1 + max(self.__height(y.left), self.__height(y.right))
        return y

    def __range(self, node, low, high, out: List[float]) -> None:
        if node is None:
            return
        if low < node.key:
            self.__range(node.left, low, high, out)
        if low <= node.key <= high:
            out.extend([node.key] * len(node.payloads))
        if high > node.key:
            self.__range(node.right, low, high, out)

    @staticmethod
    def __height(node: Optional[_AVLNode]) -> int:
        return node.height if node else 0

    def __balance_factor(self, node: _AVLNode) -> int:
        return self.__height(node.left) - self.__height(node.right)
