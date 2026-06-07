"""Abstract base class for all data structure implementations."""

from abc import ABC, abstractmethod
from typing import Any

from skynet.models.operation_result import OperationResult


class DataStructureBase(ABC):
    """Abstract base class for all linear and tree data structures.

    Defines the common interface that all concrete data structure
    implementations (MaxHeap, FIFOQueue, LIFOStack, AVLTree, HashTable)
    must implement. This enables polymorphic usage across the service
    layer and ensures consistent operation signatures.

    All mutation operations return an OperationResult indicating
    success or failure with a descriptive message.
    """

    @abstractmethod
    def insert(self, item: Any) -> OperationResult:
        """Insert an item into the data structure.

        Args:
            item: The item to insert. The concrete type depends on
                  the specific data structure implementation.

        Returns:
            OperationResult indicating success or failure of the insertion.
        """
        pass

    @abstractmethod
    def delete(self, key: Any) -> OperationResult:
        """Delete an item by key from the data structure.

        Args:
            key: The key identifying the item to remove. The key type
                 depends on the specific data structure implementation.

        Returns:
            OperationResult indicating success or failure of the deletion,
            with the deleted item in the data field on success.
        """
        pass

    @abstractmethod
    def search(self, key: Any) -> OperationResult:
        """Search for an item by key.

        Args:
            key: The key to search for. The key type depends on the
                 specific data structure implementation.

        Returns:
            OperationResult indicating whether the item was found,
            with the found item in the data field on success.
        """
        pass

    @abstractmethod
    def display(self) -> str:
        """Return a string representation of the structure's contents.

        Returns:
            A formatted string showing the current state of the
            data structure, suitable for console output.
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the structure contains no elements.

        Returns:
            True if the data structure has zero elements, False otherwise.
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """Return the number of elements in the structure.

        Returns:
            The current count of elements stored in the data structure.
        """
        pass
