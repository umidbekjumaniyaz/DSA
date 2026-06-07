"""AVL tree node for the SkyNet flight price database."""

from typing import List, Optional

from skynet.models.price_record import PriceRecord


class AVLNode:
    """A node in the AVL tree storing price records.

    Each node is keyed by price value and can hold multiple records
    at the same price point. The height field is used to compute
    balance factors for AVL rebalancing.

    Attributes:
        key: The price value used as the sort key.
        records: List of PriceRecord objects stored at this price.
        left: Reference to the left child node.
        right: Reference to the right child node.
        height: Height of this node in the tree (leaf = 1).
    """

    def __init__(self, key: float):
        """Initialise an AVL node with the given price key.

        Args:
            key: The price value to use as the sort key.
        """
        self.key: float = key
        self.records: List[PriceRecord] = []
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1

    def __repr__(self) -> str:
        """Return a string representation of the node."""
        return f"AVLNode(key={self.key}, records={len(self.records)}, height={self.height})"
