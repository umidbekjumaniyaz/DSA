"""Hash table implementation with separate chaining for collision resolution."""

from typing import Any, List, Optional, Tuple

from skynet.models.base import DataStructureBase
from skynet.models.operation_result import OperationResult


class HashTable(DataStructureBase):
    """Hash table using separate chaining for collision resolution.

    Stores key-value pairs in an array of buckets, where each bucket
    is a list of (key, value) tuples. Collisions are handled by
    appending to the same bucket's list (separate chaining).

    Uses a polynomial rolling hash function with prime multiplier 31
    for good distribution of alphanumeric keys (e.g., PNR codes).

    Attributes:
        _buckets: List of lists, each containing (key, value) tuples.
        _capacity: Number of buckets (prime number for better distribution).
        _size: Number of stored key-value entries.
    """

    def __init__(self, capacity: int = 53) -> None:
        """Initialize hash table with given capacity.

        Args:
            capacity: Number of buckets. Defaults to 53 (a prime number).
        """
        self._capacity: int = capacity
        self._buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self._capacity)]
        self._size: int = 0

    def _hash(self, key: str) -> int:
        """Compute bucket index for the given key using polynomial rolling hash.

        Uses prime multiplier 31 and modulo capacity to distribute keys
        across buckets. The polynomial rolling approach ensures different
        character orderings produce different hash values.

        Args:
            key: The string key to hash.

        Returns:
            An integer bucket index in the range [0, capacity).
        """
        hash_value = 0
        prime = 31
        for char in key:
            hash_value = (hash_value * prime + ord(char)) % self._capacity
        return hash_value

    def _find_in_bucket(self, bucket_idx: int, key: str) -> Optional[int]:
        """Find the index of a key within a specific bucket.

        Args:
            bucket_idx: The bucket index to search in.
            key: The key to find.

        Returns:
            The index within the bucket list if found, None otherwise.
        """
        bucket = self._buckets[bucket_idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                return i
        return None

    def insert(self, item: Any) -> OperationResult:
        """Insert a key-value pair into the hash table.

        The item must be a tuple of (key, value). Duplicate keys are
        rejected to maintain uniqueness.

        Args:
            item: A tuple of (key, value) where key is a string.

        Returns:
            OperationResult indicating success or failure. On success,
            data contains the inserted (key, value) tuple.
        """
        if not isinstance(item, tuple) or len(item) != 2:
            return OperationResult(
                success=False,
                message="Insert requires a (key, value) tuple.",
                data=None,
            )

        key, value = item

        if not isinstance(key, str):
            return OperationResult(
                success=False,
                message="Key must be a string.",
                data=None,
            )

        bucket_idx = self._hash(key)
        existing_idx = self._find_in_bucket(bucket_idx, key)

        if existing_idx is not None:
            return OperationResult(
                success=False,
                message=f"Duplicate key rejected: '{key}' already exists in the hash table.",
                data=None,
            )

        self._buckets[bucket_idx].append((key, value))
        self._size += 1

        return OperationResult(
            success=True,
            message=f"Successfully inserted key '{key}' into bucket {bucket_idx}.",
            data=(key, value),
        )

    def delete(self, key: Any) -> OperationResult:
        """Delete a record by key from the hash table.

        Args:
            key: The string key identifying the record to remove.

        Returns:
            OperationResult indicating success or failure. On success,
            data contains the deleted (key, value) tuple.
        """
        if not isinstance(key, str):
            return OperationResult(
                success=False,
                message="Key must be a string.",
                data=None,
            )

        bucket_idx = self._hash(key)
        item_idx = self._find_in_bucket(bucket_idx, key)

        if item_idx is None:
            return OperationResult(
                success=False,
                message=f"Key '{key}' not found in the hash table.",
                data=None,
            )

        deleted_entry = self._buckets[bucket_idx].pop(item_idx)
        self._size -= 1

        return OperationResult(
            success=True,
            message=f"Successfully deleted key '{key}' from bucket {bucket_idx}.",
            data=deleted_entry,
        )

    def search(self, key: Any) -> OperationResult:
        """Search for a record by key with O(1) average-case time complexity.

        Args:
            key: The string key to search for.

        Returns:
            OperationResult indicating whether the key was found. On success,
            data contains the (key, value) tuple.
        """
        if not isinstance(key, str):
            return OperationResult(
                success=False,
                message="Key must be a string.",
                data=None,
            )

        bucket_idx = self._hash(key)
        item_idx = self._find_in_bucket(bucket_idx, key)

        if item_idx is None:
            return OperationResult(
                success=False,
                message=f"Key '{key}' not found in the hash table.",
                data=None,
            )

        entry = self._buckets[bucket_idx][item_idx]
        return OperationResult(
            success=True,
            message=f"Found key '{key}' in bucket {bucket_idx}.",
            data=entry,
        )

    def update(self, key: str, value: Any) -> OperationResult:
        """Update the value for an existing key.

        Args:
            key: The string key to update.
            value: The new value to associate with the key.

        Returns:
            OperationResult indicating success or failure. On success,
            data contains the updated (key, value) tuple.
        """
        if not isinstance(key, str):
            return OperationResult(
                success=False,
                message="Key must be a string.",
                data=None,
            )

        bucket_idx = self._hash(key)
        item_idx = self._find_in_bucket(bucket_idx, key)

        if item_idx is None:
            return OperationResult(
                success=False,
                message=f"Key '{key}' not found in the hash table. Cannot update.",
                data=None,
            )

        self._buckets[bucket_idx][item_idx] = (key, value)

        return OperationResult(
            success=True,
            message=f"Successfully updated key '{key}' in bucket {bucket_idx}.",
            data=(key, value),
        )

    def display(self) -> str:
        """Display the hash table bucket structure.

        Shows each non-empty bucket with its index and chained entries
        in the format: "Bucket [i]: key1 -> val1, key2 -> val2"

        Returns:
            A formatted string showing the hash table structure.
        """
        if self._size == 0:
            return "Hash Table is empty."

        lines = []
        for i, bucket in enumerate(self._buckets):
            if bucket:
                entries = ", ".join(f"{k} -> {v}" for k, v in bucket)
                lines.append(f"Bucket [{i}]: {entries}")

        return "\n".join(lines)

    def is_empty(self) -> bool:
        """Check if the hash table contains no entries.

        Returns:
            True if the hash table has zero entries, False otherwise.
        """
        return self._size == 0

    def size(self) -> int:
        """Return the number of key-value entries stored.

        Returns:
            The current count of entries in the hash table.
        """
        return self._size
