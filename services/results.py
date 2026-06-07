"""Uniform operation result and error-code types.

Every service method returns an :class:`OperationResult` rather than raising
across the layer boundary. Each :class:`ErrorCode` maps to exactly one
canonical, human-readable message template, guaranteeing distinct and
consistent messaging for every error condition (Requirement 15).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ErrorCode(Enum):
    """Canonical catalogue of handled error conditions."""

    EMPTY_GRAPH = "empty-graph"
    MISSING_AIRPORT = "missing-airport"
    DUPLICATE_AIRPORT = "duplicate-airport"
    DUPLICATE_ROUTE = "duplicate-route"
    NO_AVAILABLE_ROUTE = "no-available-route"
    EMPTY_QUEUE = "empty-queue"
    EMPTY_STACK = "empty-stack"
    PASSENGER_NOT_FOUND = "passenger-not-found"
    INVALID_PNR = "invalid-pnr"
    DUPLICATE_PNR = "duplicate-pnr"
    DISCONNECTED_GRAPH = "disconnected-graph"
    INVALID_INPUT = "invalid-input"


# One canonical message template per error code. Distinct and non-empty.
_MESSAGES = {
    ErrorCode.EMPTY_GRAPH: "The flight network is empty.",
    ErrorCode.MISSING_AIRPORT: "Airport '{code}' does not exist in the network.",
    ErrorCode.DUPLICATE_AIRPORT: "Airport '{code}' already exists.",
    ErrorCode.DUPLICATE_ROUTE: "A route between '{a}' and '{b}' already exists.",
    ErrorCode.NO_AVAILABLE_ROUTE: "No available route between '{src}' and '{dst}'.",
    ErrorCode.EMPTY_QUEUE: "The queue is empty.",
    ErrorCode.EMPTY_STACK: "The cargo stack is empty.",
    ErrorCode.PASSENGER_NOT_FOUND: "No passenger found for PNR '{pnr}'.",
    ErrorCode.INVALID_PNR: "PNR '{pnr}' is not a valid record locator.",
    ErrorCode.DUPLICATE_PNR: "A passenger with PNR '{pnr}' already exists.",
    ErrorCode.DISCONNECTED_GRAPH: (
        "Cannot form a spanning tree: the network is disconnected."
    ),
    ErrorCode.INVALID_INPUT: "Invalid input: {detail}",
}


def message_for(error_code: "ErrorCode", **kwargs) -> str:
    """Render the canonical message for ``error_code`` with template fields."""
    template = _MESSAGES[error_code]
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        # Missing template fields should never blank out the message.
        return template


@dataclass(frozen=True)
class OperationResult:
    """The outcome of a service operation.

    A successful result carries an optional ``payload``; a failed result
    carries an :class:`ErrorCode` and a rendered ``message``.
    """

    ok: bool
    payload: object = None
    error: Optional[ErrorCode] = None
    message: str = ""

    @classmethod
    def success(cls, payload: object = None, message: str = "") -> "OperationResult":
        return cls(ok=True, payload=payload, error=None, message=message)

    @classmethod
    def failure(cls, error: "ErrorCode", message: str = "", **kwargs) -> "OperationResult":
        rendered = message or message_for(error, **kwargs)
        return cls(ok=False, payload=None, error=error, message=rendered)

    def __bool__(self) -> bool:  # pragma: no cover - convenience
        return self.ok
