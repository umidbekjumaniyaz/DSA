"""Ticket status priority ranking for passenger check-in."""

from enum import IntEnum


class TicketStatus(IntEnum):
    """Passenger service class used as the priority key for check-in.

    Implemented as an ``IntEnum`` so that the natural integer ordering
    gives a Max-Heap the correct priority: Platinum > Gold > Silver > Economy.
    """

    ECONOMY = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4

    @classmethod
    def from_name(cls, name: str) -> "TicketStatus":
        """Resolve a status from a case-insensitive name.

        Raises:
            ValueError: if the name does not match a known status.
        """
        try:
            return cls[name.strip().upper()]
        except KeyError as exc:
            valid = ", ".join(member.name.title() for member in cls)
            raise ValueError(
                f"Unknown ticket status '{name}'. Valid values: {valid}."
            ) from exc

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return self.name.title()
