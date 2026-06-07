"""Flight record model used for schedule sorting."""

from dataclasses import dataclass

# Valid sort keys exposed to the sorting services.
SORT_KEYS = ("departure_time", "fuel_efficiency")


@dataclass(frozen=True)
class FlightRecord:
    """A single scheduled flight.

    ``departure_time`` is stored as minutes since midnight (0..1439) and
    ``fuel_efficiency`` as a positive ratio. Records are sortable by a
    selectable key via :meth:`sort_value`.
    """

    flight_no: str
    departure_time: int
    fuel_efficiency: float
    origin: str = ""
    destination: str = ""

    def __post_init__(self) -> None:
        if not str(self.flight_no).strip():
            raise ValueError("flight_no must be non-empty.")
        if not isinstance(self.departure_time, int) or isinstance(
            self.departure_time, bool
        ):
            raise ValueError("departure_time must be an integer (minutes).")
        if not 0 <= self.departure_time <= 1439:
            raise ValueError("departure_time must be within 0..1439 minutes.")
        if not isinstance(self.fuel_efficiency, (int, float)) or isinstance(
            self.fuel_efficiency, bool
        ):
            raise ValueError("fuel_efficiency must be numeric.")
        if self.fuel_efficiency <= 0:
            raise ValueError("fuel_efficiency must be positive.")

    def sort_value(self, key: str):
        """Return the value used to order this record for ``key``."""
        if key not in SORT_KEYS:
            raise ValueError(
                f"Unknown sort key '{key}'. Valid keys: {', '.join(SORT_KEYS)}."
            )
        return getattr(self, key)

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        hh, mm = divmod(self.departure_time, 60)
        return (
            f"{self.flight_no} {hh:02d}:{mm:02d} "
            f"fuel={self.fuel_efficiency:g} {self.origin}->{self.destination}"
        )
