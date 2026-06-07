"""Price record domain model for the SkyNet aviation logistics system."""

from dataclasses import dataclass


@dataclass
class PriceRecord:
    """Represents a flight price record stored in the AVL tree.

    Attributes:
        origin: Origin IATA code.
        destination: Destination IATA code.
        price: Price value (used as AVL tree key).
        currency: Currency code (defaults to GBP).
    """

    origin: str
    destination: str
    price: float
    currency: str = "GBP"
