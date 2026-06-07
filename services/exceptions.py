"""Re-export the internal data-structure exceptions for the services layer.

The canonical definitions live in :mod:`data_structures.exceptions` so the
low-level structures do not depend on the services package (avoiding a circular
import). Services import them from here for readability.
"""

from data_structures.exceptions import (
    DataStructureError,
    EmptyStructureError,
    KeyNotFoundError,
)

__all__ = ["DataStructureError", "EmptyStructureError", "KeyNotFoundError"]
