"""Standard result type for all data structure and service operations."""

from dataclasses import dataclass
from typing import Any


@dataclass
class OperationResult:
    """Standard result object for all data structure operations.

    Provides a consistent interface for returning operation outcomes,
    including success/failure status, a human-readable message, and
    optional data payload.

    Attributes:
        success: Whether the operation completed successfully.
        message: A human-readable description of the outcome.
        data: Optional payload containing operation-specific result data.
    """

    success: bool
    message: str
    data: Any = None
