"""Comprehensive unit tests for the queue module.

Tests cover: FIFOQueue with FIFO ordering, duplicate rejection via
identifier, edge cases (empty/single element), and error conditions.

Requirements: 13.5, 13.12, 13.13
"""

import pytest

from skynet.queue.fifo_queue import FIFOQueue


# ============================================================
# Helper fixtures
# ============================================================


@pytest.fixture
def empty_queue():
    """Return an empty FIFOQueue."""
    return FIFOQueue()


@pytest.fixture
def single_item_queue():
    """Return a queue with a single passenger."""
    queue = FIFOQueue()
    queue.enqueue("Alice", "PAX001")
    return queue


@pytest.fixture
def multi_item_queue():
    """Return a queue with multiple passengers in order.

    Enqueue order: Alice, Bob, Charlie
    Expected dequeue order: Alice, Bob, Charlie (FIFO)
    """
    queue = FIFOQueue()
    queue.enqueue("Alice", "PAX001")
    queue.enqueue("Bob", "PAX002")
    queue.enqueue("Charlie", "PAX003")
    return queue


# ============================================================
# Normal Operation Tests
# ============================================================


class TestFIFOQueueNormal:
    """Normal operation tests for FIFOQueue."""

    def test_enqueue_multiple_dequeue_in_fifo_order(self, multi_item_queue):
        """Enqueue Alice, Bob, Charlie -> dequeue in same order (FIFO)."""
        queue = multi_item_queue

        result1 = queue.dequeue()
        assert result1.success is True
        assert result1.data == "Alice"

        result2 = queue.dequeue()
        assert result2.success is True
        assert result2.data == "Bob"

        result3 = queue.dequeue()
        assert result3.success is True
        assert result3.data == "Charlie"

    def test_enqueue_returns_success_with_position(self, empty_queue):
        """Enqueue returns success result indicating position in queue."""
        queue = empty_queue

        result1 = queue.enqueue("Alice", "PAX001")
        assert result1.success is True
        assert "PAX001" in result1.message
        assert "1" in result1.message  # Position 1

        result2 = queue.enqueue("Bob", "PAX002")
        assert result2.success is True
        assert "PAX002" in result2.message
        assert "2" in result2.message  # Position 2

    def test_display_shows_queue_contents_in_order(self, multi_item_queue):
        """Display shows all passengers from front to rear with positions."""
        queue = multi_item_queue
        display_str = queue.display()

        assert "1." in display_str
        assert "2." in display_str
        assert "3." in display_str
        assert "Alice" in display_str
        assert "Bob" in display_str
        assert "Charlie" in display_str

    def test_contains_check_finds_existing_identifier(self, multi_item_queue):
        """Contains returns True for identifiers currently in the queue."""
        queue = multi_item_queue

        assert queue.contains("PAX001") is True
        assert queue.contains("PAX002") is True
        assert queue.contains("PAX003") is True

    def test_contains_check_returns_false_for_missing(self, multi_item_queue):
        """Contains returns False for identifiers not in the queue."""
        queue = multi_item_queue

        assert queue.contains("PAX999") is False
        assert queue.contains("UNKNOWN") is False

    def test_size_tracks_queue_length(self, empty_queue):
        """Size increases on enqueue and decreases on dequeue."""
        queue = empty_queue
        assert queue.size() == 0

        queue.enqueue("Alice", "PAX001")
        assert queue.size() == 1

        queue.enqueue("Bob", "PAX002")
        assert queue.size() == 2

        queue.dequeue()
        assert queue.size() == 1

    def test_peek_returns_front_without_removal(self, multi_item_queue):
        """Peek returns the front item without changing the queue size."""
        queue = multi_item_queue
        initial_size = queue.size()

        result = queue.peek()
        assert result.success is True
        assert result.data == "Alice"
        assert queue.size() == initial_size

    def test_is_empty_false_when_has_elements(self, single_item_queue):
        """is_empty returns False when queue has elements."""
        assert single_item_queue.is_empty() is False


# ============================================================
# Edge Case Tests
# ============================================================


class TestFIFOQueueEdgeCases:
    """Edge case tests for FIFOQueue."""

    def test_empty_queue_dequeue_returns_failure(self, empty_queue):
        """Dequeue from empty queue returns failure OperationResult."""
        result = empty_queue.dequeue()
        assert result.success is False
        assert result.data is None
        assert "empty" in result.message.lower()

    def test_empty_queue_peek_returns_failure(self, empty_queue):
        """Peek on empty queue returns failure OperationResult."""
        result = empty_queue.peek()
        assert result.success is False
        assert result.data is None
        assert "empty" in result.message.lower()

    def test_single_element_enqueue_and_dequeue(self, empty_queue):
        """Enqueue and dequeue a single element successfully."""
        queue = empty_queue

        queue.enqueue("Solo Traveler", "SOLO1")
        assert queue.size() == 1
        assert queue.is_empty() is False

        result = queue.dequeue()
        assert result.success is True
        assert result.data == "Solo Traveler"
        assert queue.is_empty() is True

    def test_re_enqueue_after_dequeue_succeeds(self, empty_queue):
        """After dequeue, the same identifier can be re-enqueued."""
        queue = empty_queue

        queue.enqueue("Alice", "PAX001")
        queue.dequeue()

        # Re-enqueue with same identifier should succeed
        result = queue.enqueue("Alice Returns", "PAX001")
        assert result.success is True
        assert queue.contains("PAX001") is True

    def test_contains_false_after_dequeue(self, single_item_queue):
        """Contains returns False for an identifier after it has been dequeued."""
        queue = single_item_queue
        assert queue.contains("PAX001") is True

        queue.dequeue()
        assert queue.contains("PAX001") is False

    def test_is_empty_true_for_new_queue(self, empty_queue):
        """A fresh queue reports is_empty as True."""
        assert empty_queue.is_empty() is True
        assert empty_queue.size() == 0


# ============================================================
# Error Condition Tests
# ============================================================


class TestFIFOQueueErrors:
    """Error condition tests for FIFOQueue."""

    def test_duplicate_passenger_enqueue_rejected(self, empty_queue):
        """Enqueuing a passenger with a duplicate identifier is rejected."""
        queue = empty_queue

        result1 = queue.enqueue("Alice", "PAX001")
        assert result1.success is True

        result2 = queue.enqueue("Alice Clone", "PAX001")
        assert result2.success is False
        assert "duplicate" in result2.message.lower() or "already" in result2.message.lower()

        # Size should not have increased
        assert queue.size() == 1

    def test_duplicate_rejection_preserves_original(self, empty_queue):
        """After duplicate rejection, the original item remains at front."""
        queue = empty_queue

        queue.enqueue("Original Alice", "PAX001")
        queue.enqueue("Duplicate Alice", "PAX001")

        result = queue.dequeue()
        assert result.data == "Original Alice"

    def test_empty_queue_display_message(self, empty_queue):
        """Display on empty queue shows appropriate empty message."""
        display_str = empty_queue.display()
        assert "empty" in display_str.lower()
