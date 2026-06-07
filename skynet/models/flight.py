"""Flight domain model for the SkyNet aviation logistics system."""

from dataclasses import dataclass


@dataclass
class Flight:
    """Represents a flight route (edge) between two airports.

    Attributes:
        origin: Origin IATA code.
        destination: Destination IATA code.
        distance_km: Distance in kilometers (must be between 1 and 99999 inclusive).
    """

    origin: str
    destination: str
    distance_km: int

    def __post_init__(self):
        if not (1 <= self.distance_km <= 99999):
            raise ValueError(
                f"Invalid distance: {self.distance_km}. "
                "Must be between 1 and 99999 inclusive."
            )
