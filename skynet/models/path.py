"""Path domain model for the SkyNet aviation logistics system."""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Path:
    """Represents a route through the flight network.

    Attributes:
        nodes: Ordered list of IATA codes forming the route.
        legs: List of (source, destination, distance) tuples for each leg.
        total_distance: Sum of all leg distances.
        is_shortest: Whether this is the shortest alternative route.
    """

    nodes: List[str] = field(default_factory=list)
    legs: List[Tuple[str, str, int]] = field(default_factory=list)
    total_distance: int = 0
    is_shortest: bool = False
