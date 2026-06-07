"""Airport domain model for the SkyNet aviation logistics system."""

from dataclasses import dataclass


@dataclass
class Airport:
    """Represents an airport node in the flight network.

    Attributes:
        iata_code: Exactly 3 uppercase alphabetic characters (e.g., LHR, JFK, DXB).
        name: Full airport name.
        city: City where airport is located.
    """

    iata_code: str
    name: str
    city: str

    def __post_init__(self):
        if not (
            len(self.iata_code) == 3
            and self.iata_code.isalpha()
            and self.iata_code.isupper()
        ):
            raise ValueError(
                f"Invalid IATA code: '{self.iata_code}'. "
                "Must be exactly 3 uppercase alphabetic characters."
            )
