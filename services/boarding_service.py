"""Boarding service: FIFO gate queue."""

from data_structures.fifo_queue import Queue

from .exceptions import EmptyStructureError
from .results import ErrorCode, OperationResult


class BoardingService:
    """Phase 2 boarding-gate management using a FIFO queue."""

    def __init__(self, queue: Queue) -> None:
        self.__queue = queue

    def board_passenger(self, passenger) -> OperationResult:
        self.__queue.enqueue(passenger)
        return OperationResult.success(
            message=f"{passenger} joined the boarding queue."
        )

    def call_next(self) -> OperationResult:
        try:
            passenger = self.__queue.dequeue()
        except EmptyStructureError:
            return OperationResult.failure(ErrorCode.EMPTY_QUEUE)
        return OperationResult.success(
            payload=passenger, message=f"Boarding {passenger}."
        )

    def size(self) -> int:
        return self.__queue.size()
