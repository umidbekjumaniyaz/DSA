"""Comprehensive unit tests for the stack module.

Tests cover: LIFOStack with LIFO ordering, push/pop/peek operations,
size tracking, edge cases (empty/single element), and error conditions.

Requirements: 13.6, 13.12, 13.13
"""

import pytest

from skynet.stack.lifo_stack import LIFOStack


# ============================================================
# Helper fixtures
# ============================================================


@pytest.fixture
def empty_stack():
    """Return an empty LIFOStack."""
    return LIFOStack()


@pytest.fixture
def single_item_stack():
    """Return a stack with a single item."""
    stack = LIFOStack()
    stack.push("Container-A")
    return stack


@pytest.fixture
def multi_item_stack():
    """Return a stack with three items pushed in order: A, B, C.

    Expected pop order: C, B, A (LIFO).
    """
    stack = LIFOStack()
    stack.push("Container-A")
    stack.push("Container-B")
    stack.push("Container-C")
    return stack


# ============================================================
# Normal Operation Tests
# ============================================================


class TestLIFOStackNormal:
    """Normal operation tests for LIFOStack."""

    def test_push_items_pop_in_lifo_order(self, multi_item_stack):
        """Items pushed A, B, C are popped in reverse order C, B, A (LIFO)."""
        stack = multi_item_stack

        result1 = stack.pop()
        assert result1.success is True
        assert result1.data == "Container-C"

        result2 = stack.pop()
        assert result2.success is True
        assert result2.data == "Container-B"

        result3 = stack.pop()
        assert result3.success is True
        assert result3.data == "Container-A"

    def test_peek_returns_top_without_removal(self, multi_item_stack):
        """Peek returns the top item without changing the stack size."""
        stack = multi_item_stack
        initial_size = stack.size()

        peek_result = stack.peek()
        assert peek_result.success is True
        assert peek_result.data == "Container-C"

        # Size unchanged after peek
        assert stack.size() == initial_size

    def test_peek_matches_subsequent_pop(self, multi_item_stack):
        """Peek returns the same item that pop would return next."""
        stack = multi_item_stack

        peek_result = stack.peek()
        pop_result = stack.pop()

        assert peek_result.data == pop_result.data

    def test_size_tracking_on_push(self, empty_stack):
        """Size increases by 1 after each push operation."""
        stack = empty_stack
        assert stack.size() == 0

        stack.push("Item-1")
        assert stack.size() == 1

        stack.push("Item-2")
        assert stack.size() == 2

        stack.push("Item-3")
        assert stack.size() == 3

    def test_size_tracking_on_pop(self, multi_item_stack):
        """Size decreases by 1 after each pop operation."""
        stack = multi_item_stack
        assert stack.size() == 3

        stack.pop()
        assert stack.size() == 2

        stack.pop()
        assert stack.size() == 1

        stack.pop()
        assert stack.size() == 0

    def test_push_returns_success_result(self, empty_stack):
        """Push operation returns OperationResult with success=True."""
        stack = empty_stack
        result = stack.push("Cargo-X")

        assert result.success is True
        assert "Cargo-X" in result.message
        assert result.data == "Cargo-X"

    def test_pop_returns_success_with_item_data(self, single_item_stack):
        """Pop operation returns OperationResult with success=True and the item."""
        stack = single_item_stack
        result = stack.pop()

        assert result.success is True
        assert result.data == "Container-A"
        assert "Container-A" in result.message

    def test_is_empty_false_when_has_elements(self, single_item_stack):
        """is_empty returns False when stack has elements."""
        assert single_item_stack.is_empty() is False

    def test_lifo_ordering_with_numeric_items(self, empty_stack):
        """LIFO ordering works correctly with numeric items."""
        stack = empty_stack
        for i in range(1, 6):
            stack.push(i)

        # Pop in reverse order
        for i in range(5, 0, -1):
            result = stack.pop()
            assert result.data == i


# ============================================================
# Edge Case Tests
# ============================================================


class TestLIFOStackEdgeCases:
    """Edge case tests for LIFOStack."""

    def test_empty_stack_pop_returns_failure(self, empty_stack):
        """Popping from empty stack returns failure OperationResult."""
        result = empty_stack.pop()
        assert result.success is False
        assert result.data is None

    def test_empty_stack_peek_returns_failure(self, empty_stack):
        """Peeking at empty stack returns failure OperationResult."""
        result = empty_stack.peek()
        assert result.success is False
        assert result.data is None

    def test_empty_stack_is_empty(self, empty_stack):
        """An empty stack reports is_empty as True and size as 0."""
        assert empty_stack.is_empty() is True
        assert empty_stack.size() == 0

    def test_single_item_push_and_pop(self, empty_stack):
        """Push and pop a single element successfully, stack becomes empty."""
        stack = empty_stack
        stack.push("Solo-Cargo")
        assert stack.size() == 1
        assert stack.is_empty() is False

        result = stack.pop()
        assert result.success is True
        assert result.data == "Solo-Cargo"
        assert stack.is_empty() is True
        assert stack.size() == 0

    def test_display_format_with_items(self, multi_item_stack):
        """Display returns formatted string showing items from top to bottom."""
        stack = multi_item_stack
        display_str = stack.display()

        # Should contain reference to top -> bottom ordering
        assert "top" in display_str.lower()
        # Should contain all items
        assert "Container-C" in display_str
        assert "Container-B" in display_str
        assert "Container-A" in display_str

    def test_display_empty_stack(self, empty_stack):
        """Display on empty stack returns appropriate message."""
        display_str = empty_stack.display()
        assert "empty" in display_str.lower()

    def test_push_pop_push_sequence(self, empty_stack):
        """Push, pop, then push again correctly tracks state."""
        stack = empty_stack

        stack.push("First")
        stack.pop()
        stack.push("Second")

        result = stack.peek()
        assert result.data == "Second"
        assert stack.size() == 1


# ============================================================
# Error Condition Tests
# ============================================================


class TestLIFOStackErrors:
    """Error condition tests for LIFOStack."""

    def test_pop_from_empty_returns_no_cargo_loaded(self, empty_stack):
        """Pop from empty stack returns message 'no cargo is loaded'."""
        result = empty_stack.pop()
        assert result.success is False
        assert "no cargo is loaded" in result.message

    def test_peek_from_empty_returns_no_cargo_loaded(self, empty_stack):
        """Peek from empty stack returns message 'no cargo is loaded'."""
        result = empty_stack.peek()
        assert result.success is False
        assert "no cargo is loaded" in result.message

    def test_pop_all_then_pop_again_returns_error(self, multi_item_stack):
        """After popping all items, further pop returns error."""
        stack = multi_item_stack

        # Pop all three items
        stack.pop()
        stack.pop()
        stack.pop()

        # Now stack is empty, next pop should fail
        result = stack.pop()
        assert result.success is False
        assert "no cargo is loaded" in result.message

    def test_peek_after_emptying_returns_error(self, single_item_stack):
        """After popping the only item, peek returns error."""
        stack = single_item_stack
        stack.pop()

        result = stack.peek()
        assert result.success is False
        assert "no cargo is loaded" in result.message
