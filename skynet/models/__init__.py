"""Domain models for the SkyNet aviation logistics system."""

from skynet.models.airport import Airport
from skynet.models.cargo import Cargo
from skynet.models.flight import Flight
from skynet.models.passenger import Passenger, PriorityLevel
from skynet.models.path import Path
from skynet.models.price_record import PriceRecord

__all__ = [
    "Airport",
    "Cargo",
    "Flight",
    "Passenger",
    "Path",
    "PriceRecord",
    "PriorityLevel",
]
