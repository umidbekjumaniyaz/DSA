"""Passenger domain model for the SkyNet aviation logistics system."""

from dataclasses import dataclass
from enum import Enum


class PriorityLevel(Enum):
    """Passenger priority classification.

    Higher numeric values indicate higher priority.
    """

    PLATINUM = 4
    GOLD = 3
    SILVER = 2
    ECONOMY = 1


@dataclass
class Passenger:
    """Represents a passenger record.

    Attributes:
        pnr: Passenger Name Record (must be non-empty and alphanumeric).
        name: Full passenger name.
        flight_number: Flight number.
        seat: Seat assignment.
        priority: Passenger priority level (defaults to ECONOMY).
    """

    pnr: str
    name: str
    flight_number: str
    seat: str
    priority: PriorityLevel = PriorityLevel.ECONOMY

    def __post_init__(self):
        if not self.pnr or not self.pnr.isalnum():
            raise ValueError(
                f"Invalid PNR format: '{self.pnr}'. "
                "Must be non-empty and contain only alphanumeric characters."
            )
