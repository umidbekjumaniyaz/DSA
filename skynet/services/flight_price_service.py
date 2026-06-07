"""Flight price service composing AVL tree for price storage and queries."""

from skynet.models.operation_result import OperationResult
from skynet.models.price_record import PriceRecord
from skynet.tree import AVLTree


class FlightPriceService:
    """Service layer for managing flight prices using an AVL tree.

    Provides business logic for adding, removing, searching, and
    displaying flight price records. Composes an AVLTree internally
    for balanced O(log n) operations on price data.
    """

    def __init__(self):
        """Initialise the flight price service with an empty AVL tree."""
        self._avl_tree = AVLTree()

    def add_price(self, origin: str, destination: str, price: float) -> OperationResult:
        """Create a PriceRecord and insert it into the AVL tree.

        Args:
            origin: Origin airport IATA code.
            destination: Destination airport IATA code.
            price: The flight price value (used as AVL tree key).

        Returns:
            OperationResult indicating success with inserted record data,
            or failure with an error message.
        """
        record = PriceRecord(origin=origin, destination=destination, price=price)
        return self._avl_tree.insert(record)

    def remove_price(self, price: float) -> OperationResult:
        """Remove a price record by price value from the AVL tree.

        Args:
            price: The price value to remove.

        Returns:
            OperationResult indicating success with removed record data,
            or failure if no record exists at that price.
        """
        return self._avl_tree.delete(price)

    def search_price(self, price: float) -> OperationResult:
        """Search for records at a specific price value.

        Args:
            price: The price value to search for.

        Returns:
            OperationResult with found records or failure message.
        """
        return self._avl_tree.search(price)

    def range_search(self, min_price: float, max_price: float) -> OperationResult:
        """Find all records in the price range [min_price, max_price].

        Args:
            min_price: Minimum price (inclusive).
            max_price: Maximum price (inclusive).

        Returns:
            OperationResult with list of matching records or failure
            if no records fall within the range.
        """
        return self._avl_tree.range_search(min_price, max_price)

    def display_prices(self) -> str:
        """Display all prices in sorted order using in-order traversal.

        Returns:
            A formatted string showing all price records in ascending
            price order, or a message indicating the database is empty.
        """
        if self._avl_tree.is_empty():
            return "Flight Price Database: (empty)"

        records = self._avl_tree.in_order_traversal()
        lines = ["Flight Price Database (sorted by price):"]
        for record in records:
            lines.append(
                f"  {record.origin} -> {record.destination}: "
                f"{record.price} {record.currency}"
            )
        return "\n".join(lines)
