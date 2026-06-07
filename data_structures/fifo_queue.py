"""First-In-First-Out queue backed by ``collections.deque``."""

from collections import deque

from data_structures.exceptions import EmptyStructureError


class Queue:
    """A FIFO queue. Internal storage is fully encapsulated."""

    def __init__(self) -> None:
        self.__items = deque()

    def enqueue(self, item: object) -> None:
        """Append ``item`` at the rear of the queue."""
        self.__items.append(item)

    def dequeue(self) -> object:
        """Remove and return the front item.

        Raises:
            EmptyStructureError: if the queue is empty.
        """
        if not self.__items:
            raise EmptyStructureError("dequeue from empty queue")
        return self.__items.popleft()

    def peek(self) -> object:
        if not self.__items:
            raise EmptyStructureError("peek from empty queue")
        return self.__items[0]

    def is_empty(self) -> bool:
        return not self.__items

    def size(self) -> int:
        return len(self.__items)
