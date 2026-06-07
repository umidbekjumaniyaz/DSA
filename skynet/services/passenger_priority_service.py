"""Passenger priority queue service for the SkyNet aviation logistics system.

Composes MaxHeap to manage passenger check-in priority ordering.
Higher priority passengers (Platinum > Gold > Silver > Economy) are
processed first, with FIFO ordering within the same priority level.
"""

from dataclasses import dataclass

from skynet.heap import MaxHeap
from skynet.models import PriorityLevel
from skynet.models.operation_result import OperationResult
from skynet.utils.validators import validate_priority_level


# Map priority level strings (lowercase) to PriorityLevel enum members
_PRIORITY_MAP = {
    "platinum": PriorityLevel.PLATINUM,
    "gold": PriorityLevel.GOLD,
    "silver": PriorityLevel.SILVER,
    "economy": PriorityLevel.ECONOMY,
}


@dataclass
class _PriorityPassenger:
    """Lightweight passenger representation for heap storage.

    Attributes:
        name: Passenger name.
        priority: PriorityLevel enum value (has .value int for heap ordering).
    """

    name: str
    priority: PriorityLevel


class PassengerPriorityService:
    """Service managing passenger check-in priority using a max-heap.

    Provides operations to add passengers with priority levels,
    process the next highest-priority passenger, peek at the next
    passenger, and display the current queue.

    The service validates priority level strings at the boundary
    before delegating to the underlying MaxHeap data structure.
    """

    def __init__(self) -> None:
        """Initialize the service with an empty MaxHeap."""
        self._heap = MaxHeap()

    def add_passenger(self, name: str, priority: str) -> OperationResult:
        """Add a passenger to the priority queue.

        Validates the priority level string (case-insensitive), creates a
        passenger object, and inserts it into the max-heap.

        Args:
            name: The passenger's name.
            priority: Priority level string ('Platinum', 'Gold', 'Silver',
                or 'Economy', case-insensitive).

        Returns:
            OperationResult indicating success with passenger details,
            or failure if the priority level is invalid.
        """
        if not validate_priority_level(priority):
            return OperationResult(
                success=False,
                message=(
                    f"Invalid priority level: '{priority}'. "
                    "Must be one of: Platinum, Gold, Silver, Economy."
                ),
                data=None,
            )

        priority_enum = _PRIORITY_MAP[priority.strip().lower()]
        passenger = _PriorityPassenger(name=name, priority=priority_enum)

        result = self._heap.insert(passenger)

        if result.success:
            return OperationResult(
                success=True,
                message=(
                    f"Passenger '{name}' added with priority "
                    f"{priority_enum.name.capitalize()}."
                ),
                data=passenger,
            )

        return result  # pragma: no cover

    def process_next(self) -> OperationResult:
        """Process (remove) the next highest-priority passenger.

        Extracts the passenger with the maximum priority from the heap.
        Among passengers with equal priority, the one added earliest
        is processed first (FIFO).

        Returns:
            OperationResult with passenger details on success,
            or failure if the queue is empty.
        """
        result = self._heap.extract_max()

        if not result.success:
            return OperationResult(
                success=False,
                message="No passengers are waiting in the priority queue.",
                data=None,
            )

        passenger = result.data
        return OperationResult(
            success=True,
            message=(
                f"Processed passenger '{passenger.name}' "
                f"with priority {passenger.priority.name.capitalize()}."
            ),
            data=passenger,
        )

    def peek_next(self) -> OperationResult:
        """View the next highest-priority passenger without removing them.

        Returns:
            OperationResult with passenger details on success,
            or failure if the queue is empty.
        """
        result = self._heap.peek()

        if not result.success:
            return OperationResult(
                success=False,
                message="No passengers are waiting in the priority queue.",
                data=None,
            )

        passenger = result.data
        return OperationResult(
            success=True,
            message=(
                f"Next passenger: '{passenger.name}' "
                f"with priority {passenger.priority.name.capitalize()}."
            ),
            data=passenger,
        )

    def display_queue(self) -> str:
        """Display the current priority queue contents.

        Returns:
            A formatted string showing all passengers in the queue
            with their priority levels, or a message if empty.
        """
        if self._heap.is_empty():
            return "Priority queue is empty. No passengers are waiting."

        lines = [f"Passenger Priority Queue (size={self._heap.size()}):"]
        # Access internal heap to display in priority order information
        for i, (priority_val, neg_seq, passenger) in enumerate(self._heap._heap):
            seq = -neg_seq
            lines.append(
                f"  [{i + 1}] {passenger.name} - "
                f"{passenger.priority.name.capitalize()} "
                f"(Priority={priority_val}, Seq={seq})"
            )

        return "\n".join(lines)
