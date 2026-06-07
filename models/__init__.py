"""Domain models for the SkyNet Global Aviation Logistics & Management System."""

from .ticket_status import TicketStatus
from .airport import Airport
from .route import Route
from .passenger import Passenger, PassengerProfile
from .flight_record import FlightRecord

__all__ = [
    "TicketStatus",
    "Airport",
    "Route",
    "Passenger",
    "PassengerProfile",
    "FlightRecord",
]
