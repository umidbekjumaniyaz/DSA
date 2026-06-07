"""Route model: a weighted edge in the flight network."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    """A weighted connection between two airports.

    ``weight`` represents the route cost (money, distance, or time) and must be
    strictly positive. The graph treats routes as undirected, so ``endpoints``
    returns the unordered pair used for duplicate detection and comparison.
    """

    source: str
    destination: str
    weight: float

    def __post_init__(self) -> None:
        src = str(self.source).strip().upper()
        dst = str(self.destination).strip().upper()
        if not src or not dst:
            raise ValueError("Route endpoints must be non-empty airport codes.")
        if src == dst:
            raise ValueError("A route cannot connect an airport to itself.")
        if not isinstance(self.weight, (int, float)) or isinstance(self.weight, bool):
            raise ValueError("Route weight must be numeric.")
        if self.weight <= 0:
            raise ValueError("Route weight must be a positive number.")
        object.__setattr__(self, "source", src)
        object.__setattr__(self, "destination", dst)
        object.__setattr__(self, "weight", float(self.weight))

    def endpoints(self) -> frozenset:
        """Return the unordered pair of endpoints for undirected comparison."""
        return frozenset((self.source, self.destination))

    def other(self, code: str) -> str:
        """Return the endpoint opposite to ``code``."""
        code = str(code).strip().upper()
        if code == self.source:
            return self.destination
        if code == self.destination:
            return self.source
        raise ValueError(f"Airport '{code}' is not an endpoint of this route.")

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return f"{self.source} <-> {self.destination} (cost {self.weight:g})"
