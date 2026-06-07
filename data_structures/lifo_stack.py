"""Last-In-First-Out stack backed by a Python list."""

from data_structures.exceptions import EmptyStructureError


class Stack:
    """A LIFO stack. Internal storage is fully encapsulated."""

    def __init__(self) -> None:
        self.__items: list = []

    def push(self, item: object) -> None:
        """Place ``item`` on the top of the stack."""
        self.__items.append(item)

    def pop(self) -> object:
        """Remove and return the top item.

        Raises:
            EmptyStructureError: if the stack is empty.
        """
        if not self.__items:
            raise EmptyStructureError("pop from empty stack")
        return self.__items.pop()

    def peek(self) -> object:
        if not self.__items:
            raise EmptyStructureError("peek from empty stack")
        return self.__items[-1]

    def is_empty(self) -> bool:
        return not self.__items

    def size(self) -> int:
        return len(self.__items)
