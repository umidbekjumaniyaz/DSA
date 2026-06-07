"""Pricing service: AVL price tree with range queries."""

from data_structures.price_tree import AVLTree

from .results import ErrorCode, OperationResult


class PricingService:
    """Phase 3 flight-price storage and range search over an AVL tree."""

    def __init__(self, tree: AVLTree) -> None:
        self.__tree = tree

    def insert_price(self, price, payload=None) -> OperationResult:
        try:
            self.__tree.insert(price, payload)
        except ValueError as exc:
            return OperationResult.failure(ErrorCode.INVALID_INPUT, detail=str(exc))
        return OperationResult.success(message=f"Price {float(price):g} inserted.")

    def contains_price(self, price) -> OperationResult:
        try:
            value = float(price)
        except (TypeError, ValueError):
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT, detail="price must be numeric"
            )
        present = self.__tree.contains(value)
        return OperationResult.success(
            payload=present,
            message=f"Price {value:g} is {'present' if present else 'absent'}.",
        )

    def range_search(self, low, high) -> OperationResult:
        try:
            low_v, high_v = float(low), float(high)
        except (TypeError, ValueError):
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT, detail="bounds must be numeric"
            )
        found = self.__tree.range_search(low_v, high_v)
        return OperationResult.success(
            payload=found,
            message=(
                f"Found {len(found)} price(s) in [{low_v:g}, {high_v:g}]: "
                f"{', '.join(f'{p:g}' for p in found) if found else 'none'}."
            ),
        )
