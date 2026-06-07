"""Max-heap priority queue implementation for passenger priority management.

Implements a binary max-heap from scratch using an array-based approach.
Elements are stored as (priority_value, -sequence_number, item) tuples to
provide stable FIFO ordering within the same priority level.

Python tuple comparison compares element-by-element:
- First by priority_value (higher = extracted first)
- Then by -sequence_number (more negative = inserted earlier = extracted first)

This ensures that among equal priorities, the earliest inserted item is
extracted first, maintaining FIFO within the same priority level.
"""

from typing import Any, List, Tuple

from skynet.models.base import DataStructureBase
from skynet.models.operation_result import OperationResult


class MaxHeap(DataStructureBase):
    """Array-based max-heap with stable priority ordering.

    Stores elements as (priority_value, -sequence_number, item) tuples.
    The heap property ensures parent >= children using tuple comparison.
    This guarantees:
      - Higher priority_value items are extracted first
      - Among equal priority items, earlier-inserted items are extracted first (FIFO)

    Attributes:
        _heap: Internal list storing heap entries as tuples.
        _sequence: Monotonically increasing counter for insertion order tracking.
    """

    def __init__(self) -> None:
        """Initialize an empty max-heap."""
        self._heap: List[Tuple[int, int, Any]] = []
        self._sequence: int = 0

    def insert(self, item: Any) -> OperationResult:
        """Insert an item into the max-heap based on its priority.

        The item must have a `priority` attribute with a `value` property
        (e.g., a PriorityLevel enum). The item is placed according to its
        priority value, with FIFO ordering for equal priorities.

        Args:
            item: The item to insert. Must have item.priority.value (int).

        Returns:
            OperationResult indicating success or failure of the insertion.
        """
        try:
            priority_value = item.priority.value
        except AttributeError:
            return OperationResult(
                success=False,
                message="Item must have a 'priority' attribute with a 'value' property.",
                data=None,
            )

        self._sequence += 1
        # Store as (priority_value, -sequence_number, item)
        # Higher priority_value = higher priority
        # More negative sequence = inserted earlier = higher priority among equals
        entry = (priority_value, -self._sequence, item)
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

        return OperationResult(
            success=True,
            message=f"Inserted with priority {priority_value}.",
            data=item,
        )

    def extract_max(self) -> OperationResult:
        """Remove and return the highest-priority item from the heap.

        Returns the item with the maximum priority value. Among items with
        equal priority, returns the one inserted earliest (FIFO).

        Returns:
            OperationResult with the extracted item in data field on success,
            or failure if the heap is empty.
        """
        if self.is_empty():
            return OperationResult(
                success=False,
                message="Heap is empty. No passengers are waiting.",
                data=None,
            )

        max_entry = self._heap[0]
        last_entry = self._heap.pop()

        if not self.is_empty():
            self._heap[0] = last_entry
            self._sift_down(0)

        return OperationResult(
            success=True,
            message=f"Extracted item with priority {max_entry[0]}.",
            data=max_entry[2],  # Return the item
        )

    def peek(self) -> OperationResult:
        """View the highest-priority item without removing it.

        Returns:
            OperationResult with the top item in data field on success,
            or failure if the heap is empty.
        """
        if self.is_empty():
            return OperationResult(
                success=False,
                message="Heap is empty. No passengers are waiting.",
                data=None,
            )

        top_entry = self._heap[0]
        return OperationResult(
            success=True,
            message=f"Next item has priority {top_entry[0]}.",
            data=top_entry[2],  # Return the item
        )

    def delete(self, key: Any) -> OperationResult:
        """Delete an item from the heap (maps to extract_max for interface compliance).

        Since a max-heap's primary operation is extracting the maximum,
        this method delegates to extract_max to fulfill the abstract
        DataStructureBase interface contract.

        Args:
            key: Unused parameter (maintained for interface compliance).

        Returns:
            OperationResult from extract_max operation.
        """
        return self.extract_max()

    def search(self, key: Any) -> OperationResult:
        """Search the heap (maps to peek for interface compliance).

        Since a max-heap's primary lookup is viewing the top element,
        this method delegates to peek to fulfill the abstract
        DataStructureBase interface contract.

        Args:
            key: Unused parameter (maintained for interface compliance).

        Returns:
            OperationResult from peek operation.
        """
        return self.peek()

    def is_empty(self) -> bool:
        """Check if the heap contains no elements.

        Returns:
            True if the heap has zero elements, False otherwise.
        """
        return len(self._heap) == 0

    def size(self) -> int:
        """Return the number of elements in the heap.

        Returns:
            The current count of elements stored in the heap.
        """
        return len(self._heap)

    def display(self) -> str:
        """Return a string representation of the heap contents.

        Shows all elements in array order with their priority values
        and sequence numbers.

        Returns:
            A formatted string showing the current heap state.
        """
        if self.is_empty():
            return "Heap is empty."

        lines = [f"MaxHeap (size={self.size()}):"]
        for i, (priority, neg_seq, item) in enumerate(self._heap):
            seq = -neg_seq
            lines.append(f"  [{i}] Priority={priority}, Seq={seq}, Item={item}")

        return "\n".join(lines)

    def _sift_up(self, index: int) -> None:
        """Move an element up the heap to restore the max-heap property.

        Compares the element at the given index with its parent and swaps
        if the element is larger (higher priority or earlier insertion for
        equal priority). Continues until the element is in its correct position.

        Args:
            index: The index of the element to sift up.
        """
        while index > 0:
            parent_index = (index - 1) // 2
            if self._heap[index] > self._heap[parent_index]:
                self._heap[index], self._heap[parent_index] = (
                    self._heap[parent_index],
                    self._heap[index],
                )
                index = parent_index
            else:
                break

    def _sift_down(self, index: int) -> None:
        """Move an element down the heap to restore the max-heap property.

        Compares the element at the given index with its children and swaps
        with the largest child if the element is smaller. Continues until
        the element is in its correct position.

        Args:
            index: The index of the element to sift down.
        """
        heap_size = len(self._heap)

        while True:
            largest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2

            if left_child < heap_size and self._heap[left_child] > self._heap[largest]:
                largest = left_child

            if (
                right_child < heap_size
                and self._heap[right_child] > self._heap[largest]
            ):
                largest = right_child

            if largest == index:
                break

            self._heap[index], self._heap[largest] = (
                self._heap[largest],
                self._heap[index],
            )
            index = largest
