"""Cargo domain model for the SkyNet aviation logistics system."""

from dataclasses import dataclass


@dataclass
class Cargo:
    """Represents a cargo item.

    Attributes:
        item_id: Unique cargo identifier.
        description: Description of cargo contents.
        weight_kg: Weight in kilograms.
        flight_number: Associated flight number.
    """

    item_id: str
    description: str
    weight_kg: float
    flight_number: str = ""
