"""FIFO Queue implementation using a singly linked list.

Provides first-in-first-out queue semantics for the Boarding Gate System,
with duplicate prevention via identifier tracking.
"""

from typing import Any, Optional, Set

from skynet.models.base import DataStructureBase
from skynet.models.operation_result import OperationResult


class _QueueNode:
    """Internal node for the singly linked list backing the FIFO queue.

    Attributes:
        data: The item stored in this node.
        identifier: The unique identifier associated with this item.
        next: Reference to the next node in the list, or None if tail.
    """

    __slots__ = ("data", "identifier", "next")

    def __init__(self, data: Any, identifier: str) -> None:
        self.data: Any = data
        self.identifier: str = identifier
        self.next: Optional["_QueueNode"] = None


class FIFOQueue(DataStructureBase):
    """First-In-First-Out queue implemented with a singly linked list.

    Supports enqueue (add to rear), dequeue (remove from front), peek
    (view front without removal), and duplicate rejection via an
    identifier membership set.

    Used by the Boarding Gate System to manage passenger boarding order.
    """

    def __init__(self) -> None:
        """Initialise an empty FIFO queue."""
        self._head: Optional[_QueueNode] = None
        self._tail: Optional[_QueueNode] = None
        self._size: int = 0
        self._members: Set[str] = set()

    # ------------------------------------------------------------------
    # Primary queue operations
    # ------------------------------------------------------------------

    def enqueue(self, item: Any, identifier: str) -> OperationResult:
        """Add an item to the rear of the queue.

        Args:
            item: The item to enqueue.
            identifier: A unique string identifier for duplicate detection.

        Returns:
            OperationResult indicating success or duplicate rejection.
        """
        if identifier in self._members:
            return OperationResult(
                success=False,
                message=f"Duplicate entry: '{identifier}' is already in the queue",
                data=None,
            )

        new_node = _QueueNode(item, identifier)

        if self._tail is None:
            # Queue is empty
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1
        self._members.add(identifier)

        return OperationResult(
            success=True,
            message=f"'{identifier}' added to queue at position {self._size}",
            data=item,
        )

    def dequeue(self) -> OperationResult:
        """Remove and return the item at the front of the queue.

        Returns:
            OperationResult with the dequeued item, or failure if empty.
        """
        if self._head is None:
            return OperationResult(
                success=False,
                message="Queue is empty: no passengers in the queue",
                data=None,
            )

        removed_node = self._head
        self._head = self._head.next

        if self._head is None:
            # Queue is now empty
            self._tail = None

        self._size -= 1

        # Remove identifier from members set
        self._members.discard(removed_node.identifier)

        return OperationResult(
            success=True,
            message="Passenger boarded successfully",
            data=removed_node.data,
        )

    def peek(self) -> OperationResult:
        """View the item at the front of the queue without removal.

        Returns:
            OperationResult with the front item, or failure if empty.
        """
        if self._head is None:
            return OperationResult(
                success=False,
                message="Queue is empty: no passengers in the queue",
                data=None,
            )

        return OperationResult(
            success=True,
            message="Front of queue",
            data=self._head.data,
        )

    def contains(self, identifier: str) -> bool:
        """Check if an identifier is currently in the queue.

        Args:
            identifier: The string identifier to check.

        Returns:
            True if the identifier is in the queue, False otherwise.
        """
        return identifier in self._members

    # ------------------------------------------------------------------
    # DataStructureBase abstract method implementations
    # ------------------------------------------------------------------

    def insert(self, item: Any) -> OperationResult:
        """Insert an item into the queue (maps to enqueue).

        Uses str(item) as the identifier for duplicate detection.

        Args:
            item: The item to insert.

        Returns:
            OperationResult indicating success or failure.
        """
        identifier = str(item)
        return self.enqueue(item, identifier)

    def delete(self, key: Any) -> OperationResult:
        """Delete an item from the queue (maps to dequeue).

        In FIFO queue semantics, delete removes from the front
        regardless of the key provided.

        Args:
            key: Ignored; dequeue always removes from front.

        Returns:
            OperationResult with the dequeued item.
        """
        return self.dequeue()

    def search(self, key: Any) -> OperationResult:
        """Search the queue (maps to peek).

        In FIFO queue semantics, search returns the front item.

        Args:
            key: Ignored; peek always returns the front.

        Returns:
            OperationResult with the front item.
        """
        return self.peek()

    def is_empty(self) -> bool:
        """Check if the queue contains no elements.

        Returns:
            True if the queue has zero elements, False otherwise.
        """
        return self._size == 0

    def size(self) -> int:
        """Return the number of elements in the queue.

        Returns:
            The current count of elements in the queue.
        """
        return self._size

    def display(self) -> str:
        """Return a string representation of all items front to rear.

        Shows each item with its position number (1-indexed from front).

        Returns:
            A formatted string showing the queue contents, or a message
            indicating the queue is empty.
        """
        if self._head is None:
            return "Queue is empty"

        lines = ["Boarding Queue (front to rear):"]
        current = self._head
        position = 1

        while current is not None:
            lines.append(f"  {position}. {current.data}")
            current = current.next
            position += 1

        return "\n".join(lines)
