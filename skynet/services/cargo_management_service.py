"""Cargo Management Service composing LIFOStack for cargo operations.

Provides business logic for loading, unloading, and viewing cargo items
using a Last-In-First-Out stack data structure.
"""

from skynet.models import Cargo
from skynet.models.operation_result import OperationResult
from skynet.stack import LIFOStack


class CargoManagementService:
    """Service layer for cargo management using a LIFO stack.

    Composes a LIFOStack to manage cargo loading and unloading operations.
    Cargo items are loaded onto the top of the stack and unloaded from the
    top, following LIFO ordering.

    Attributes:
        _stack: Internal LIFOStack storing Cargo objects.
    """

    def __init__(self) -> None:
        """Initialize the CargoManagementService with an empty stack."""
        self._stack = LIFOStack()

    def load_cargo(self, item_id: str, description: str, weight: float) -> OperationResult:
        """Create a Cargo object and push it onto the stack.

        Args:
            item_id: Unique identifier for the cargo item.
            description: Description of cargo contents.
            weight: Weight of the cargo in kilograms.

        Returns:
            OperationResult confirming the cargo was loaded successfully.
        """
        cargo = Cargo(item_id=item_id, description=description, weight_kg=weight)
        result = self._stack.push(cargo)
        return OperationResult(
            success=True,
            message=f"Cargo '{item_id}' ({description}, {weight}kg) loaded successfully",
            data=cargo,
        )

    def unload_cargo(self) -> OperationResult:
        """Pop cargo from the top of the stack.

        Returns:
            OperationResult with the unloaded cargo item details,
            or an error if the stack is empty.
        """
        result = self._stack.pop()
        if not result.success:
            return OperationResult(
                success=False,
                message="Cannot unload: no cargo is loaded",
                data=None,
            )
        cargo = result.data
        return OperationResult(
            success=True,
            message=f"Cargo '{cargo.item_id}' ({cargo.description}, {cargo.weight_kg}kg) unloaded successfully",
            data=cargo,
        )

    def peek_top(self) -> OperationResult:
        """View the top cargo item without removing it.

        Returns:
            OperationResult with the top cargo item details,
            or an error if the stack is empty.
        """
        result = self._stack.peek()
        if not result.success:
            return OperationResult(
                success=False,
                message="Cannot peek: no cargo is loaded",
                data=None,
            )
        cargo = result.data
        return OperationResult(
            success=True,
            message=f"Top cargo: '{cargo.item_id}' ({cargo.description}, {cargo.weight_kg}kg)",
            data=cargo,
        )

    def display_stack(self) -> str:
        """Display current cargo stack contents.

        Returns:
            A formatted string showing all cargo items from top to bottom,
            or a message indicating the stack is empty.
        """
        return self._stack.display()
