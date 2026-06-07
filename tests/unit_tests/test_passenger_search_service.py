"""Unit tests for PassengerSearchService."""

import pytest

from skynet.services.passenger_search_service import PassengerSearchService


class FakeRegistry:
    """Fake PassengerRegistryService providing test data."""

    def __init__(self, records=None):
        self._records = records if records is not None else []

    def get_all_records(self):
        return self._records


@pytest.fixture
def sample_records():
    """Sample passenger records for testing."""
    return [
        {"name": "John Smith", "pnr": "ABC123", "flight": "BA256"},
        {"name": "Jane Doe", "pnr": "XYZ789", "flight": "BA256"},
        {"name": "Alice Johnson", "pnr": "DEF456", "flight": "EK101"},
        {"name": "Bob Williams", "pnr": "GHI012", "flight": "QF007"},
    ]


@pytest.fixture
def search_service(sample_records):
    """PassengerSearchService with sample data."""
    registry = FakeRegistry(sample_records)
    return PassengerSearchService(registry)


@pytest.fixture
def empty_search_service():
    """PassengerSearchService with no records."""
    registry = FakeRegistry([])
    return PassengerSearchService(registry)


class TestSearchByName:
    """Tests for search_by_name method."""

    def test_search_by_name_single_match(self, search_service):
        """Normal: search finds exactly one matching passenger by name."""
        result = search_service.search_by_name("Alice")
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]["name"] == "Alice Johnson"

    def test_search_by_name_multiple_matches(self, search_service):
        """Normal: search finds multiple passengers with common name fragment."""
        result = search_service.search_by_name("o")
        assert result.success is True
        # "John Smith", "Jane Doe", "Alice Johnson", "Bob Williams" - John, Doe, Johnson, Bob
        matching_names = [r["name"] for r in result.data]
        assert "John Smith" in matching_names
        assert "Jane Doe" in matching_names
        assert "Alice Johnson" in matching_names
        assert "Bob Williams" in matching_names

    def test_search_by_name_case_insensitive(self, search_service):
        """Normal: search is case-insensitive."""
        result = search_service.search_by_name("john")
        assert result.success is True
        matching_names = [r["name"] for r in result.data]
        assert "John Smith" in matching_names
        assert "Alice Johnson" in matching_names

    def test_search_by_name_no_match(self, search_service):
        """Edge case: pattern matches no names."""
        result = search_service.search_by_name("Zebra")
        assert result.success is True
        assert result.data == []
        assert "No matching records" in result.message

    def test_search_by_name_empty_pattern(self, search_service):
        """Error: empty pattern is rejected."""
        result = search_service.search_by_name("")
        assert result.success is False
        assert "non-empty" in result.message

    def test_search_by_name_whitespace_pattern(self, search_service):
        """Error: whitespace-only pattern is rejected."""
        result = search_service.search_by_name("   ")
        assert result.success is False
        assert "non-empty" in result.message

    def test_search_by_name_empty_registry(self, empty_search_service):
        """Edge case: no records in registry."""
        result = empty_search_service.search_by_name("John")
        assert result.success is True
        assert result.data == []


class TestSearchByPnr:
    """Tests for search_by_pnr method."""

    def test_search_by_pnr_exact_match(self, search_service):
        """Normal: search finds exact PNR match."""
        result = search_service.search_by_pnr("ABC123")
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]["pnr"] == "ABC123"

    def test_search_by_pnr_partial_match(self, search_service):
        """Normal: partial PNR pattern matches multiple records."""
        # DEF456, GHI012 - the pattern "12" appears in ABC123 and GHI012
        result = search_service.search_by_pnr("12")
        assert result.success is True
        matching_pnrs = [r["pnr"] for r in result.data]
        assert "ABC123" in matching_pnrs
        assert "GHI012" in matching_pnrs

    def test_search_by_pnr_case_insensitive(self, search_service):
        """Normal: PNR search is case-insensitive."""
        result = search_service.search_by_pnr("abc")
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]["pnr"] == "ABC123"

    def test_search_by_pnr_no_match(self, search_service):
        """Edge case: pattern matches no PNRs."""
        result = search_service.search_by_pnr("ZZZ")
        assert result.success is True
        assert result.data == []
        assert "No matching records" in result.message

    def test_search_by_pnr_empty_pattern(self, search_service):
        """Error: empty pattern is rejected."""
        result = search_service.search_by_pnr("")
        assert result.success is False

    def test_search_by_pnr_whitespace_pattern(self, search_service):
        """Error: whitespace-only pattern is rejected."""
        result = search_service.search_by_pnr("  \t ")
        assert result.success is False


class TestSearchByFlight:
    """Tests for search_by_flight method."""

    def test_search_by_flight_multiple_matches(self, search_service):
        """Normal: pattern matches multiple passengers on same flight."""
        result = search_service.search_by_flight("BA256")
        assert result.success is True
        assert len(result.data) == 2
        matching_names = [r["name"] for r in result.data]
        assert "John Smith" in matching_names
        assert "Jane Doe" in matching_names

    def test_search_by_flight_single_match(self, search_service):
        """Normal: pattern matches a single flight number."""
        result = search_service.search_by_flight("QF007")
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]["name"] == "Bob Williams"

    def test_search_by_flight_partial_match(self, search_service):
        """Normal: partial flight pattern matches."""
        result = search_service.search_by_flight("BA")
        assert result.success is True
        assert len(result.data) == 2

    def test_search_by_flight_case_insensitive(self, search_service):
        """Normal: flight search is case-insensitive."""
        result = search_service.search_by_flight("ba256")
        assert result.success is True
        assert len(result.data) == 2

    def test_search_by_flight_no_match(self, search_service):
        """Edge case: no matching flight numbers."""
        result = search_service.search_by_flight("LH999")
        assert result.success is True
        assert result.data == []
        assert "No matching records" in result.message

    def test_search_by_flight_empty_pattern(self, search_service):
        """Error: empty pattern is rejected."""
        result = search_service.search_by_flight("")
        assert result.success is False

    def test_search_by_flight_whitespace_pattern(self, search_service):
        """Error: whitespace-only pattern is rejected."""
        result = search_service.search_by_flight("   ")
        assert result.success is False
