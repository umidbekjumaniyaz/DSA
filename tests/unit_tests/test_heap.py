"""Comprehensive unit tests for the heap module.

Tests cover: MaxHeap with passenger priority ordering, FIFO within
equal priorities, edge cases (empty/single element), and error conditions.

Requirements: 13.9, 13.12, 13.13
"""

import pytest

from skynet.heap.max_heap import MaxHeap
from skynet.models.passenger import Passenger, PriorityLevel


# ============================================================
# Helper fixtures
# ============================================================


@pytest.fixture
def empty_heap():
    """Return an empty MaxHeap."""
    return MaxHeap()


@pytest.fixture
def single_passenger_heap():
    """Return a heap with a single Gold passenger."""
    heap = MaxHeap()
    passenger = Passenger(
        pnr="ABC123", name="Alice", flight_number="SK100", seat="1A",
        priority=PriorityLevel.GOLD
    )
    heap.insert(passenger)
    return heap


@pytest.fixture
def multi_priority_heap():
    """Return a heap with one passenger of each priority level.

    Inserted in order: Economy, Gold, Platinum, Silver
    Expected extraction order: Platinum, Gold, Silver, Economy
    """
    heap = MaxHeap()
    passengers = [
        Passenger(pnr="ECO1", name="Economy Ed", flight_number="SK100", seat="30A",
                  priority=PriorityLevel.ECONOMY),
        Passenger(pnr="GLD1", name="Gold Grace", flight_number="SK100", seat="5B",
                  priority=PriorityLevel.GOLD),
        Passenger(pnr="PLT1", name="Platinum Pat", flight_number="SK100", seat="1A",
                  priority=PriorityLevel.PLATINUM),
        Passenger(pnr="SLV1", name="Silver Sam", flight_number="SK100", seat="12C",
                  priority=PriorityLevel.SILVER),
    ]
    for p in passengers:
        heap.insert(p)
    return heap


# ============================================================
# Normal Operation Tests
# ============================================================


class TestMaxHeapNormal:
    """Normal operation tests for MaxHeap."""

    def test_insert_passengers_extract_in_priority_order(self, multi_priority_heap):
        """Insert Platinum, Gold, Silver, Economy -> extract in descending priority order."""
        heap = multi_priority_heap

        result1 = heap.extract_max()
        assert result1.success is True
        assert result1.data.priority == PriorityLevel.PLATINUM

        result2 = heap.extract_max()
        assert result2.success is True
        assert result2.data.priority == PriorityLevel.GOLD

        result3 = heap.extract_max()
        assert result3.success is True
        assert result3.data.priority == PriorityLevel.SILVER

        result4 = heap.extract_max()
        assert result4.success is True
        assert result4.data.priority == PriorityLevel.ECONOMY

    def test_peek_returns_highest_priority_without_removal(self, multi_priority_heap):
        """Peek returns the same item as extract_max would, without changing size."""
        heap = multi_priority_heap
        initial_size = heap.size()

        peek_result = heap.peek()
        assert peek_result.success is True
        assert peek_result.data.priority == PriorityLevel.PLATINUM

        # Size unchanged after peek
        assert heap.size() == initial_size

        # Extract should return the same item
        extract_result = heap.extract_max()
        assert extract_result.data.pnr == peek_result.data.pnr

    def test_size_increases_on_insert(self, empty_heap):
        """Size increases by 1 after each insertion."""
        heap = empty_heap
        assert heap.size() == 0

        passenger = Passenger(
            pnr="ABC123", name="Alice", flight_number="SK100", seat="1A",
            priority=PriorityLevel.GOLD
        )
        heap.insert(passenger)
        assert heap.size() == 1

        passenger2 = Passenger(
            pnr="DEF456", name="Bob", flight_number="SK100", seat="2B",
            priority=PriorityLevel.SILVER
        )
        heap.insert(passenger2)
        assert heap.size() == 2

    def test_size_decreases_on_extract(self, multi_priority_heap):
        """Size decreases by 1 after each extraction."""
        heap = multi_priority_heap
        initial_size = heap.size()

        heap.extract_max()
        assert heap.size() == initial_size - 1

        heap.extract_max()
        assert heap.size() == initial_size - 2

    def test_insert_returns_success_result(self, empty_heap):
        """Insert operation returns OperationResult with success=True."""
        heap = empty_heap
        passenger = Passenger(
            pnr="ABC123", name="Alice", flight_number="SK100", seat="1A",
            priority=PriorityLevel.PLATINUM
        )
        result = heap.insert(passenger)

        assert result.success is True
        assert "4" in result.message  # Priority value in message
        assert result.data == passenger

    def test_display_returns_string_representation(self, multi_priority_heap):
        """Display returns a formatted string with heap contents."""
        heap = multi_priority_heap
        display_str = heap.display()

        assert "MaxHeap" in display_str
        assert "size=4" in display_str
        assert "Priority=" in display_str

    def test_is_empty_false_when_has_elements(self, single_passenger_heap):
        """is_empty returns False when heap has elements."""
        assert single_passenger_heap.is_empty() is False


# ============================================================
# Edge Case Tests
# ============================================================


class TestMaxHeapEdgeCases:
    """Edge case tests for MaxHeap."""

    def test_empty_heap_extract_returns_failure(self, empty_heap):
        """Extracting from empty heap returns failure OperationResult."""
        result = empty_heap.extract_max()
        assert result.success is False
        assert result.data is None
        assert "empty" in result.message.lower()

    def test_empty_heap_peek_returns_failure(self, empty_heap):
        """Peeking empty heap returns failure OperationResult."""
        result = empty_heap.peek()
        assert result.success is False
        assert result.data is None
        assert "empty" in result.message.lower()

    def test_empty_heap_is_empty(self, empty_heap):
        """An empty heap reports is_empty as True."""
        assert empty_heap.is_empty() is True
        assert empty_heap.size() == 0

    def test_single_element_insert_and_extract(self, empty_heap):
        """Insert and extract a single element successfully."""
        heap = empty_heap
        passenger = Passenger(
            pnr="SOLO1", name="Solo Traveler", flight_number="SK100", seat="1A",
            priority=PriorityLevel.SILVER
        )
        heap.insert(passenger)
        assert heap.size() == 1

        result = heap.extract_max()
        assert result.success is True
        assert result.data.pnr == "SOLO1"
        assert heap.is_empty() is True

    def test_equal_priority_fifo_ordering(self, empty_heap):
        """Passengers with same priority are extracted in FIFO order (first inserted first)."""
        heap = empty_heap
        passengers = [
            Passenger(pnr="G001", name="First Gold", flight_number="SK100",
                      seat="5A", priority=PriorityLevel.GOLD),
            Passenger(pnr="G002", name="Second Gold", flight_number="SK100",
                      seat="5B", priority=PriorityLevel.GOLD),
            Passenger(pnr="G003", name="Third Gold", flight_number="SK100",
                      seat="5C", priority=PriorityLevel.GOLD),
        ]
        for p in passengers:
            heap.insert(p)

        # Extract in insertion order (FIFO within same priority)
        result1 = heap.extract_max()
        assert result1.data.pnr == "G001"

        result2 = heap.extract_max()
        assert result2.data.pnr == "G002"

        result3 = heap.extract_max()
        assert result3.data.pnr == "G003"

    def test_heap_property_maintained_after_insertions(self, empty_heap):
        """Max-heap property (parent >= children) maintained after mixed insertions."""
        heap = empty_heap
        # Insert in non-optimal order
        priorities = [
            PriorityLevel.SILVER,
            PriorityLevel.PLATINUM,
            PriorityLevel.ECONOMY,
            PriorityLevel.GOLD,
            PriorityLevel.PLATINUM,
        ]
        for i, prio in enumerate(priorities):
            passenger = Passenger(
                pnr=f"P{i:03d}", name=f"Passenger {i}",
                flight_number="SK100", seat=f"{i}A", priority=prio
            )
            heap.insert(passenger)

        # Verify the internal heap property: parent tuple >= child tuples
        for i in range(len(heap._heap)):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < len(heap._heap):
                assert heap._heap[i] >= heap._heap[left]
            if right < len(heap._heap):
                assert heap._heap[i] >= heap._heap[right]

    def test_display_empty_heap(self, empty_heap):
        """Display on empty heap returns appropriate message."""
        display_str = empty_heap.display()
        assert "empty" in display_str.lower()

    def test_extract_until_empty_then_fails(self, single_passenger_heap):
        """Extracting all elements then trying again returns failure."""
        heap = single_passenger_heap
        result = heap.extract_max()
        assert result.success is True

        # Now heap is empty
        result = heap.extract_max()
        assert result.success is False


# ============================================================
# Error Condition Tests
# ============================================================


class TestMaxHeapErrors:
    """Error condition tests for MaxHeap."""

    def test_insert_item_without_priority_attribute(self, empty_heap):
        """Inserting item without .priority.value attribute returns failure."""
        heap = empty_heap
        # A plain string has no .priority attribute
        result = heap.insert("not a passenger")
        assert result.success is False
        assert "priority" in result.message.lower()

    def test_insert_item_with_priority_but_no_value(self, empty_heap):
        """Inserting item with .priority but no .value returns failure."""
        heap = empty_heap

        class FakeItem:
            priority = "HIGH"  # Has .priority but it's a string, no .value

        result = heap.insert(FakeItem())
        assert result.success is False
        assert "priority" in result.message.lower()

    def test_insert_none_returns_failure(self, empty_heap):
        """Inserting None returns failure."""
        heap = empty_heap
        result = heap.insert(None)
        assert result.success is False

    def test_delete_on_empty_heap_returns_failure(self, empty_heap):
        """Delete (extract_max) on empty heap returns failure."""
        result = empty_heap.delete(None)
        assert result.success is False
        assert "empty" in result.message.lower()

    def test_search_on_empty_heap_returns_failure(self, empty_heap):
        """Search (peek) on empty heap returns failure."""
        result = empty_heap.search(None)
        assert result.success is False
        assert "empty" in result.message.lower()

    def test_insert_dict_without_priority_returns_failure(self, empty_heap):
        """Inserting a dictionary (no .priority attribute) returns failure."""
        heap = empty_heap
        result = heap.insert({"name": "Test", "level": 3})
        assert result.success is False
        assert "priority" in result.message.lower()
