"""Cargo service: LIFO cargo-hold stack."""

from data_structures.lifo_stack import Stack

from .exceptions import EmptyStructureError
from .results import ErrorCode, OperationResult


class CargoService:
    """Phase 2 cargo loading/unloading using a LIFO stack."""

    def __init__(self, stack: Stack) -> None:
        self.__stack = stack

    def load_item(self, item) -> OperationResult:
        self.__stack.push(item)
        return OperationResult.success(message=f"Loaded cargo: {item}.")

    def unload_item(self) -> OperationResult:
        try:
            item = self.__stack.pop()
        except EmptyStructureError:
            return OperationResult.failure(ErrorCode.EMPTY_STACK)
        return OperationResult.success(payload=item, message=f"Unloaded cargo: {item}.")

    def size(self) -> int:
        return self.__stack.size()
