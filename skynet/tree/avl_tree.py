"""AVL tree implementation for the SkyNet flight price database."""

from typing import Any, List, Optional

from skynet.models.base import DataStructureBase
from skynet.models.operation_result import OperationResult
from skynet.models.price_record import PriceRecord
from skynet.tree.avl_node import AVLNode


class AVLTree(DataStructureBase):
    """Self-balancing AVL binary search tree for flight price records.

    Stores PriceRecord objects keyed by price value. Maintains the AVL
    balance property (|height(left) - height(right)| <= 1) for all nodes
    after every insertion and deletion, ensuring O(log n) operations.

    Multiple records with the same price are stored in the same node's
    records list, enabling duplicate key handling without additional nodes.
    """

    def __init__(self):
        """Initialise an empty AVL tree."""
        self._root: Optional[AVLNode] = None
        self._size: int = 0

    # ──────────────────────────────────────────────
    # Public interface (DataStructureBase overrides)
    # ──────────────────────────────────────────────

    def insert(self, item: Any) -> OperationResult:
        """Insert a PriceRecord into the AVL tree keyed by price.

        If a node with the same price already exists, the record is
        appended to that node's records list. Otherwise a new node is
        created and the tree is rebalanced via rotations.

        Args:
            item: A PriceRecord to insert.

        Returns:
            OperationResult indicating success with inserted record data.
        """
        if not isinstance(item, PriceRecord):
            return OperationResult(
                success=False,
                message="Item must be a PriceRecord instance.",
            )

        record: PriceRecord = item
        self._root = self._insert_node(self._root, record)
        self._size += 1
        return OperationResult(
            success=True,
            message=f"Inserted price record: {record.origin}->{record.destination} at {record.price} {record.currency}",
            data=record,
        )

    def delete(self, key: Any) -> OperationResult:
        """Delete a record by price value from the AVL tree.

        If the node at the given price contains multiple records, one
        record is removed. If it was the last record, the node itself
        is removed and the tree is rebalanced.

        Args:
            key: The price value to delete.

        Returns:
            OperationResult indicating success or failure.
        """
        if self._root is None:
            return OperationResult(
                success=False,
                message="Tree is empty. Nothing to delete.",
            )

        # Check if the key exists first
        node = self._search_node(self._root, key)
        if node is None:
            return OperationResult(
                success=False,
                message=f"No record found with price {key}.",
            )

        # If multiple records at this price, remove one
        if len(node.records) > 1:
            removed = node.records.pop()
            self._size -= 1
            return OperationResult(
                success=True,
                message=f"Removed one record at price {key}. {len(node.records)} record(s) remaining at this price.",
                data=removed,
            )

        # Last record at this price — remove the entire node
        removed = node.records[0]
        self._root = self._delete_node(self._root, key)
        self._size -= 1
        return OperationResult(
            success=True,
            message=f"Deleted price node {key} and rebalanced tree.",
            data=removed,
        )

    def search(self, key: Any) -> OperationResult:
        """Search for records by price value in O(log n) time.

        Args:
            key: The price value to search for.

        Returns:
            OperationResult with found records or failure message.
        """
        node = self._search_node(self._root, key)
        if node is None:
            return OperationResult(
                success=False,
                message=f"No record found with price {key}.",
            )
        return OperationResult(
            success=True,
            message=f"Found {len(node.records)} record(s) at price {key}.",
            data=node.records[:],
        )

    def range_search(self, min_price: float, max_price: float) -> OperationResult:
        """Return all records with prices in [min_price, max_price].

        Uses in-order traversal with pruning — branches outside the
        range are not explored.

        Args:
            min_price: Minimum price (inclusive).
            max_price: Maximum price (inclusive).

        Returns:
            OperationResult with list of matching records or failure.
        """
        results: List[PriceRecord] = []
        self._range_search_node(self._root, min_price, max_price, results)

        if not results:
            return OperationResult(
                success=False,
                message=f"No records found in price range [{min_price}, {max_price}].",
            )
        return OperationResult(
            success=True,
            message=f"Found {len(results)} record(s) in range [{min_price}, {max_price}].",
            data=results,
        )

    def in_order_traversal(self) -> List[PriceRecord]:
        """Return all records sorted by price ascending.

        Returns:
            List of PriceRecord objects in ascending price order.
        """
        results: List[PriceRecord] = []
        self._in_order(self._root, results)
        return results

    def display(self) -> str:
        """Return a visual string representation of the tree.

        Returns:
            Formatted string showing tree structure with node keys,
            heights, and balance factors.
        """
        if self._root is None:
            return "AVL Tree: (empty)"

        lines: List[str] = ["AVL Tree:"]
        self._build_display(self._root, "", True, lines)
        return "\n".join(lines)

    def is_empty(self) -> bool:
        """Check if the tree contains no records.

        Returns:
            True if the tree has zero records.
        """
        return self._size == 0

    def size(self) -> int:
        """Return the total number of records stored in the tree.

        Returns:
            Total count of PriceRecord objects across all nodes.
        """
        return self._size

    # ──────────────────────────────────────────────
    # Private helper methods — rotation and balance
    # ──────────────────────────────────────────────

    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Return the height of a node (0 for None).

        Args:
            node: The AVL node to check.

        Returns:
            Height of the node, or 0 if None.
        """
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """Return the balance factor of a node: height(left) - height(right).

        Args:
            node: The AVL node to check.

        Returns:
            Balance factor (positive = left-heavy, negative = right-heavy).
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """Perform a left rotation around the given node.

        Before:       After:
            x            y
             \\          / \\
              y   =>   x   T3
             / \\        \\
            T2  T3       T2

        Args:
            node: The root of the subtree to rotate (x above).

        Returns:
            New root of the rotated subtree (y above).
        """
        y = node.right
        t2 = y.left

        # Perform rotation
        y.left = node
        node.right = t2

        # Update heights (node first since it's now lower)
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """Perform a right rotation around the given node.

        Before:       After:
            y            x
           /            / \\
          x      =>   T1   y
         / \\              /
        T1  T2           T2

        Args:
            node: The root of the subtree to rotate (y above).

        Returns:
            New root of the rotated subtree (x above).
        """
        x = node.left
        t2 = x.right

        # Perform rotation
        x.right = node
        node.left = t2

        # Update heights (node first since it's now lower)
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """Rebalance a node after insertion or deletion.

        Handles all four rotation cases:
        - LL (Left-Left): Single right rotation
        - LR (Left-Right): Left rotation on left child, then right rotation
        - RR (Right-Right): Single left rotation
        - RL (Right-Left): Right rotation on right child, then left rotation

        Args:
            node: The node to rebalance.

        Returns:
            The new root of the rebalanced subtree.
        """
        balance = self._get_balance(node)

        # Left-Left (LL) case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Left-Right (LR) case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-Right (RR) case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Right-Left (RL) case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # ──────────────────────────────────────────────
    # Private helper methods — recursive operations
    # ──────────────────────────────────────────────

    def _insert_node(self, node: Optional[AVLNode], record: PriceRecord) -> AVLNode:
        """Recursively insert a record and rebalance.

        Args:
            node: Current subtree root.
            record: The PriceRecord to insert.

        Returns:
            The new root of the subtree after insertion and rebalancing.
        """
        # Base case: create new node
        if node is None:
            new_node = AVLNode(record.price)
            new_node.records.append(record)
            return new_node

        # Duplicate key: append to existing node's records
        if record.price == node.key:
            node.records.append(record)
            return node

        # Recurse into left or right subtree
        if record.price < node.key:
            node.left = self._insert_node(node.left, record)
        else:
            node.right = self._insert_node(node.right, record)

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Rebalance
        return self._rebalance(node)

    def _delete_node(self, node: Optional[AVLNode], key: float) -> Optional[AVLNode]:
        """Recursively delete a node by key and rebalance.

        Uses in-order successor (smallest node in right subtree) for
        nodes with two children.

        Args:
            node: Current subtree root.
            key: The price key to delete.

        Returns:
            The new root of the subtree after deletion and rebalancing.
        """
        if node is None:
            return None

        # Navigate to the target node
        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            # Found the node to delete
            # Case 1: Node with no children or one child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Case 2: Node with two children
            # Get in-order successor (smallest in right subtree)
            successor = self._find_min(node.right)
            node.key = successor.key
            node.records = successor.records
            node.right = self._delete_node(node.right, successor.key)

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Rebalance
        return self._rebalance(node)

    def _find_min(self, node: AVLNode) -> AVLNode:
        """Find the node with the minimum key in a subtree.

        Used to find the in-order successor during deletion.

        Args:
            node: Root of the subtree to search.

        Returns:
            The node with the smallest key in the subtree.
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _search_node(self, node: Optional[AVLNode], key: float) -> Optional[AVLNode]:
        """Search for a node by key.

        Args:
            node: Current subtree root.
            key: The price key to find.

        Returns:
            The matching AVLNode or None if not found.
        """
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._search_node(node.left, key)
        return self._search_node(node.right, key)

    def _range_search_node(
        self,
        node: Optional[AVLNode],
        min_price: float,
        max_price: float,
        results: List[PriceRecord],
    ) -> None:
        """Recursively collect records within the given price range.

        Prunes branches that cannot contain records in the range.

        Args:
            node: Current subtree root.
            min_price: Minimum price (inclusive).
            max_price: Maximum price (inclusive).
            results: Accumulator list for matching records.
        """
        if node is None:
            return

        # Prune left subtree only if current key > min_price
        if node.key > min_price:
            self._range_search_node(node.left, min_price, max_price, results)

        # Include current node if within range
        if min_price <= node.key <= max_price:
            results.extend(node.records)

        # Prune right subtree only if current key < max_price
        if node.key < max_price:
            self._range_search_node(node.right, min_price, max_price, results)

    def _in_order(self, node: Optional[AVLNode], results: List[PriceRecord]) -> None:
        """In-order traversal collecting all records.

        Args:
            node: Current subtree root.
            results: Accumulator list for records in sorted order.
        """
        if node is None:
            return
        self._in_order(node.left, results)
        results.extend(node.records)
        self._in_order(node.right, results)

    def _build_display(
        self,
        node: Optional[AVLNode],
        prefix: str,
        is_last: bool,
        lines: List[str],
    ) -> None:
        """Build a visual tree representation recursively.

        Args:
            node: Current node to display.
            prefix: Indentation prefix for the current level.
            is_last: Whether this node is the last child of its parent.
            lines: Accumulator for output lines.
        """
        if node is None:
            return

        connector = "└── " if is_last else "├── "
        balance = self._get_balance(node)
        lines.append(
            f"{prefix}{connector}[{node.key}] h={node.height} bf={balance} records={len(node.records)}"
        )

        child_prefix = prefix + ("    " if is_last else "│   ")

        # Display children (right first for visual tree representation)
        has_left = node.left is not None
        has_right = node.right is not None

        if has_right:
            self._build_display(node.right, child_prefix, not has_left, lines)
        if has_left:
            self._build_display(node.left, child_prefix, True, lines)
