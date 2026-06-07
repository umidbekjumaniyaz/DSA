"""Binary Max-Heap with a parametrised comparator.

The same implementation backs both the ticket-priority check-in queue (max
ordering on ``TicketStatus``) and Dijkstra's min-priority queue (by supplying
an inverted comparator). Stability for equal-priority elements is guaranteed by
an internal monotonically increasing insertion sequence used as a tiebreak,
so equal-priority items leave in FIFO order (Req 5.3).
"""

from typing import Callable, List, Tuple

from data_structures.exceptions import EmptyStructureError


class MaxHeap:
    """A max-heap ordered by ``priority_of(item)`` with FIFO tiebreaking."""

    def __init__(self, priority_of: Callable[[object], object] = lambda x: x) -> None:
        # Each entry: (priority, -sequence, item). Larger priority first; for
        # equal priority, smaller sequence (earlier insert) wins -> stored as
        # -sequence so the max-heap surfaces the earliest insertion.
        self.__items: List[Tuple[object, int, object]] = []
        self.__priority_of = priority_of
        self.__sequence = 0

    def push(self, item: object) -> None:
        entry = (self.__priority_of(item), -self.__sequence, item)
        self.__sequence += 1
        self.__items.append(entry)
        self.__sift_up(len(self.__items) - 1)

    def pop(self) -> object:
        """Remove and return the highest-priority item.

        Raises:
            EmptyStructureError: if the heap is empty.
        """
        if not self.__items:
            raise EmptyStructureError("pop from empty heap")
        top = self.__items[0]
        last = self.__items.pop()
        if self.__items:
            self.__items[0] = last
            self.__sift_down(0)
        return top[2]

    def peek(self) -> object:
        if not self.__items:
            raise EmptyStructureError("peek from empty heap")
        return self.__items[0][2]

    def is_empty(self) -> bool:
        return not self.__items

    def size(self) -> int:
        return len(self.__items)

    # ----- heap internals ----------------------------------------------
    def _greater(self, a: Tuple, b: Tuple) -> bool:
        # Compare by priority first, then by the FIFO tiebreak field.
        if a[0] != b[0]:
            return a[0] > b[0]
        return a[1] > b[1]

    def __sift_up(self, idx: int) -> None:
        items = self.__items
        while idx > 0:
            parent = (idx - 1) // 2
            if self._greater(items[idx], items[parent]):
                items[idx], items[parent] = items[parent], items[idx]
                idx = parent
            else:
                break

    def __sift_down(self, idx: int) -> None:
        items = self.__items
        n = len(items)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx
            if left < n and self._greater(items[left], items[largest]):
                largest = left
            if right < n and self._greater(items[right], items[largest]):
                largest = right
            if largest == idx:
                break
            items[idx], items[largest] = items[largest], items[idx]
            idx = largest
