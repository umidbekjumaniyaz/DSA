"""Passenger and passenger profile models."""

import re
from dataclasses import dataclass, field

from .ticket_status import TicketStatus

# Industry-style record locator: 6 alphanumeric upper-case characters.
_PNR_PATTERN = re.compile(r"^[A-Z0-9]{6}$")


@dataclass(frozen=True)
class PassengerProfile:
    """Extended profile details stored against a PNR in the hash table."""

    frequent_flyer_id: str = ""
    contact: str = ""
    nationality: str = ""


@dataclass(frozen=True)
class Passenger:
    """A passenger booking identified by a PNR.

    ``pnr`` must match the canonical record-locator format ``^[A-Z0-9]{6}$``.
    The validation logic is centralised in :meth:`is_valid_pnr` so every layer
    shares one definition of a well-formed PNR.
    """

    pnr: str
    name: str
    status: TicketStatus = TicketStatus.ECONOMY
    profile: PassengerProfile = field(default_factory=PassengerProfile)

    def __post_init__(self) -> None:
        if not self.is_valid_pnr(self.pnr):
            raise ValueError(f"PNR '{self.pnr}' is not a valid record locator.")
        if not str(self.name).strip():
            raise ValueError("Passenger name must be non-empty.")
        if not isinstance(self.status, TicketStatus):
            raise ValueError("status must be a TicketStatus value.")
        object.__setattr__(self, "pnr", str(self.pnr).strip().upper())

    @staticmethod
    def is_valid_pnr(pnr: object) -> bool:
        """Return ``True`` iff ``pnr`` is a 6-character alphanumeric locator."""
        if not isinstance(pnr, str):
            return False
        return bool(_PNR_PATTERN.match(pnr.strip().upper()))

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return f"{self.pnr} {self.name} [{self.status}]"
