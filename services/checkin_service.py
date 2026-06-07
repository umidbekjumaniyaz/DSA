"""Check-in service: priority queue (Max-Heap) plus PNR hash table."""

from data_structures.hash_table import HashTable
from data_structures.max_heap import MaxHeap
from models.passenger import Passenger

from .exceptions import EmptyStructureError, KeyNotFoundError
from .results import ErrorCode, OperationResult


class CheckInService:
    """Phase 2 priority check-in and Phase 3 PNR record storage."""

    def __init__(self, priority_queue: MaxHeap, passenger_table: HashTable) -> None:
        self.__queue = priority_queue
        self.__table = passenger_table

    # ----- priority check-in -------------------------------------------
    def enqueue_passenger(self, passenger: Passenger) -> OperationResult:
        if not isinstance(passenger, Passenger):
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT, detail="expected a Passenger"
            )
        self.__queue.push(passenger)
        return OperationResult.success(
            message=f"{passenger.name} queued for check-in ({passenger.status})."
        )

    def serve_next(self) -> OperationResult:
        try:
            passenger = self.__queue.pop()
        except EmptyStructureError:
            return OperationResult.failure(ErrorCode.EMPTY_QUEUE)
        return OperationResult.success(
            payload=passenger,
            message=f"Now serving {passenger.name} ({passenger.status}).",
        )

    def queue_size(self) -> int:
        return self.__queue.size()

    # ----- PNR record storage ------------------------------------------
    def register_passenger(self, passenger: Passenger) -> OperationResult:
        if not isinstance(passenger, Passenger):
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT, detail="expected a Passenger"
            )
        if not Passenger.is_valid_pnr(passenger.pnr):
            return OperationResult.failure(ErrorCode.INVALID_PNR, pnr=passenger.pnr)
        if self.__table.contains(passenger.pnr):
            return OperationResult.failure(ErrorCode.DUPLICATE_PNR, pnr=passenger.pnr)
        self.__table.put(passenger.pnr, passenger)
        return OperationResult.success(
            message=f"Passenger {passenger.name} registered under {passenger.pnr}."
        )

    def lookup(self, pnr: str) -> OperationResult:
        if not Passenger.is_valid_pnr(pnr):
            return OperationResult.failure(ErrorCode.INVALID_PNR, pnr=pnr)
        try:
            passenger = self.__table.get(str(pnr).strip().upper())
        except KeyNotFoundError:
            return OperationResult.failure(
                ErrorCode.PASSENGER_NOT_FOUND, pnr=str(pnr).strip().upper()
            )
        return OperationResult.success(payload=passenger, message=str(passenger))

    def delete(self, pnr: str) -> OperationResult:
        if not Passenger.is_valid_pnr(pnr):
            return OperationResult.failure(ErrorCode.INVALID_PNR, pnr=pnr)
        key = str(pnr).strip().upper()
        try:
            self.__table.delete(key)
        except KeyNotFoundError:
            return OperationResult.failure(ErrorCode.PASSENGER_NOT_FOUND, pnr=key)
        return OperationResult.success(message=f"Passenger {key} deleted.")
