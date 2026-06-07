"""Boarding Gate Service managing passenger boarding order via FIFO queue.

Provides first-come-first-served boarding queue management for the
Boarding Gate System subsystem. Composes a FIFOQueue to maintain
passenger boarding order with duplicate detection.
"""

from skynet.queue import FIFOQueue
from skynet.models.operation_result import OperationResult


class BoardingGateService:
    """Service layer for the Boarding Gate System.

    Manages passenger boarding in FIFO order, ensuring passengers
    board the aircraft sequentially in the order they joined the queue.
    Uses passenger_id as the unique identifier for duplicate detection.

    Attributes:
        _queue: Internal FIFOQueue instance managing boarding order.
    """

    def __init__(self) -> None:
        """Initialise the BoardingGateService with an empty FIFO queue."""
        self._queue = FIFOQueue()

    def add_to_boarding(self, passenger_id: str, name: str) -> OperationResult:
        """Add a passenger to the boarding queue.

        The passenger is placed at the rear of the queue. Duplicate
        passengers (same passenger_id) are rejected.

        Args:
            passenger_id: Unique identifier for the passenger (used for
                duplicate detection).
            name: The passenger's name for display purposes.

        Returns:
            OperationResult indicating success with queue position,
            or failure if the passenger is already in the queue.
        """
        passenger_data = {"passenger_id": passenger_id, "name": name}
        result = self._queue.enqueue(passenger_data, passenger_id)

        if result.success:
            return OperationResult(
                success=True,
                message=f"Passenger '{name}' ({passenger_id}) added to boarding queue at position {self._queue.size()}",
                data=passenger_data,
            )
        else:
            return OperationResult(
                success=False,
                message=f"Duplicate entry: passenger '{passenger_id}' is already in the boarding queue",
                data=None,
            )

    def board_next(self) -> OperationResult:
        """Board the next passenger by removing them from the front of the queue.

        Returns:
            OperationResult with the boarded passenger's details on success,
            or failure message if the queue is empty.
        """
        result = self._queue.dequeue()

        if result.success:
            passenger_data = result.data
            return OperationResult(
                success=True,
                message=f"Passenger '{passenger_data['name']}' ({passenger_data['passenger_id']}) has boarded",
                data=passenger_data,
            )
        else:
            return OperationResult(
                success=False,
                message="No passengers in the boarding queue",
                data=None,
            )

    def display_queue(self) -> str:
        """Display the current boarding queue from front to rear.

        Returns:
            A formatted string showing all passengers in queue order,
            or a message indicating the queue is empty.
        """
        return self._queue.display()
