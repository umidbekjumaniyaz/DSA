"""Hash table with separate chaining and load-factor resizing.

Maps string keys (PNRs) to arbitrary payloads with average O(1) put/get/delete
(Req 9). Collisions are resolved by separate chaining so distinct keys hashing
to the same bucket remain independently retrievable (Req 9.5).
"""

from typing import List, Optional, Tuple

from data_structures.exceptions import KeyNotFoundError

_INITIAL_CAPACITY = 8
_MAX_LOAD_FACTOR = 0.75


class HashTable:
    """A separate-chaining hash table keyed by string."""

    def __init__(self, capacity: int = _INITIAL_CAPACITY) -> None:
        self.__capacity = max(capacity, _INITIAL_CAPACITY)
        self.__buckets: List[List[Tuple[str, object]]] = [
            [] for _ in range(self.__capacity)
        ]
        self.__size = 0

    # ----- public API ---------------------------------------------------
    def put(self, key: str, value: object) -> bool:
        """Insert or update ``key``.

        Returns ``True`` for a new insertion, ``False`` when an existing key
        was updated.
        """
        idx = self.__index(key)
        bucket = self.__buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return False
        bucket.append((key, value))
        self.__size += 1
        if self.__load_factor() > _MAX_LOAD_FACTOR:
            self.__resize(self.__capacity * 2)
        return True

    def get(self, key: str) -> object:
        """Return the value for ``key``.

        Raises:
            KeyNotFoundError: if ``key`` is absent.
        """
        bucket = self.__buckets[self.__index(key)]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyNotFoundError(key)

    def contains(self, key: str) -> bool:
        bucket = self.__buckets[self.__index(key)]
        return any(k == key for k, _ in bucket)

    def delete(self, key: str) -> None:
        """Remove ``key``.

        Raises:
            KeyNotFoundError: if ``key`` is absent.
        """
        bucket = self.__buckets[self.__index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.__size -= 1
                return
        raise KeyNotFoundError(key)

    def keys(self) -> List[str]:
        return [k for bucket in self.__buckets for k, _ in bucket]

    def size(self) -> int:
        return self.__size

    def is_empty(self) -> bool:
        return self.__size == 0

    def bucket_index(self, key: str) -> int:
        """Expose the bucket index for a key (used in collision tests)."""
        return self.__index(key)

    # ----- internals ----------------------------------------------------
    def __index(self, key: str) -> int:
        return hash(key) % self.__capacity

    def __load_factor(self) -> float:
        return self.__size / self.__capacity

    def __resize(self, new_capacity: int) -> None:
        old = self.__buckets
        self.__capacity = new_capacity
        self.__buckets = [[] for _ in range(new_capacity)]
        self.__size = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)
