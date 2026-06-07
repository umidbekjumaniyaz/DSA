"""LIFO Stack implementation for cargo management.

Implements a Last-In-First-Out stack using a Python list as internal
storage. The top of the stack corresponds to the end of the list,
providing O(1) push and pop operations.
"""

from typing import Any, List

from skynet.models.base import DataStructureBase
from skynet.models.operation_result import OperationResult


class LIFOStack(DataStructureBase):
    """Last-In-First-Out stack for the Cargo Management System.

    Uses a Python list as internal storage where the top of the stack
    is the end of the list. This ensures O(1) amortized time for
    push (append) and pop operations.

    Attributes:
        _items: Internal list storing stack elements (top = end of list).
    """

    def __init__(self) -> None:
        """Initialize an empty LIFO stack."""
        self._items: List[Any] = []

    def push(self, item: Any) -> OperationResult:
        """Push an item onto the top of the stack.

        Args:
            item: The item to push onto the stack.

        Returns:
            OperationResult indicating successful push with confirmation.
        """
        self._items.append(item)
        return OperationResult(
            success=True,
            message=f"Cargo '{item}' loaded successfully",
            data=item
        )

    def pop(self) -> OperationResult:
        """Remove and return the item from the top of the stack.

        Returns:
            OperationResult with the popped item on success,
            or failure if the stack is empty.
        """
        if self.is_empty():
            return OperationResult(
                success=False,
                message="no cargo is loaded",
                data=None
            )
        item = self._items.pop()
        return OperationResult(
            success=True,
            message=f"Cargo '{item}' unloaded successfully",
            data=item
        )

    def peek(self) -> OperationResult:
        """View the top item without removing it.

        Returns:
            OperationResult with the top item on success,
            or failure if the stack is empty.
        """
        if self.is_empty():
            return OperationResult(
                success=False,
                message="no cargo is loaded",
                data=None
            )
        item = self._items[-1]
        return OperationResult(
            success=True,
            message=f"Top cargo: '{item}'",
            data=item
        )

    def insert(self, item: Any) -> OperationResult:
        """Insert an item into the stack (maps to push).

        Args:
            item: The item to insert.

        Returns:
            OperationResult indicating success of the insertion.
        """
        return self.push(item)

    def delete(self, key: Any) -> OperationResult:
        """Delete an item from the stack (maps to pop).

        Args:
            key: Unused parameter (stack always pops from top).

        Returns:
            OperationResult with the removed item or failure if empty.
        """
        return self.pop()

    def search(self, key: Any) -> OperationResult:
        """Search the stack (maps to peek).

        Args:
            key: Unused parameter (stack always peeks at top).

        Returns:
            OperationResult with the top item or failure if empty.
        """
        return self.peek()

    def is_empty(self) -> bool:
        """Check if the stack contains no elements.

        Returns:
            True if the stack has zero elements, False otherwise.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the stack.

        Returns:
            The current count of elements in the stack.
        """
        return len(self._items)

    def display(self) -> str:
        """Return a string representation showing items from top to bottom.

        Returns:
            A formatted string showing the stack contents from top
            (most recent) to bottom (oldest), or a message indicating
            the stack is empty.
        """
        if self.is_empty():
            return "Cargo stack is empty"

        lines = ["Cargo Stack (top -> bottom):"]
        for i, item in enumerate(reversed(self._items)):
            lines.append(f"  [{i}] {item}")
        return "\n".join(lines)
