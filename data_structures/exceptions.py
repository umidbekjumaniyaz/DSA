"""Narrowly-typed internal exceptions raised by the data structures.

These live in the data-structures layer (the lowest layer) so that the
structures never depend on the services package. The services layer catches
them and translates them into user-facing ``ErrorCode`` values; they never
propagate to the console.
"""


class DataStructureError(Exception):
    """Base class for low-level data-structure errors."""


class EmptyStructureError(DataStructureError):
    """Raised when an element is requested from an empty queue/stack/heap."""


class KeyNotFoundError(DataStructureError):
    """Raised when a key is absent from a keyed structure (e.g. hash table)."""
