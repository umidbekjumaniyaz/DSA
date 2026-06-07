"""Unit tests for SkyNet domain models."""

import pytest

from skynet.models import (
    Airport,
    Cargo,
    Flight,
    Passenger,
    Path,
    PriceRecord,
    PriorityLevel,
)


class TestAirport:
    """Tests for Airport dataclass and IATA code validation."""

    def test_valid_airport_creation(self):
        airport = Airport("LHR", "Heathrow", "London")
        assert airport.iata_code == "LHR"
        assert airport.name == "Heathrow"
        assert airport.city == "London"

    def test_valid_three_letter_codes(self):
        codes = ["JFK", "CDG", "DXB", "SIN", "NRT"]
        for code in codes:
            airport = Airport(code, "Test Airport", "Test City")
            assert airport.iata_code == code

    def test_rejects_lowercase_iata(self):
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("lhr", "Heathrow", "London")

    def test_rejects_mixed_case_iata(self):
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("Lhr", "Heathrow", "London")

    def test_rejects_too_short_iata(self):
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("LH", "Heathrow", "London")

    def test_rejects_too_long_iata(self):
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("LHRO", "Heathrow", "London")

    def test_rejects_numeric_characters_in_iata(self):
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("L1R", "Heathrow", "London")

    def test_rejects_empty_iata(self):
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("", "Heathrow", "London")

    def test_rejects_special_characters_in_iata(self):
        with pytest.raises(ValueError, match="Invalid IATA code"):
            Airport("L-R", "Heathrow", "London")


class TestFlight:
    """Tests for Flight dataclass and distance validation."""

    def test_valid_flight_creation(self):
        flight = Flight("LHR", "JFK", 5500)
        assert flight.origin == "LHR"
        assert flight.destination == "JFK"
        assert flight.distance_km == 5500

    def test_minimum_valid_distance(self):
        flight = Flight("LHR", "JFK", 1)
        assert flight.distance_km == 1

    def test_maximum_valid_distance(self):
        flight = Flight("LHR", "JFK", 99999)
        assert flight.distance_km == 99999

    def test_rejects_zero_distance(self):
        with pytest.raises(ValueError, match="Invalid distance"):
            Flight("LHR", "JFK", 0)

    def test_rejects_negative_distance(self):
        with pytest.raises(ValueError, match="Invalid distance"):
            Flight("LHR", "JFK", -1)

    def test_rejects_distance_exceeding_maximum(self):
        with pytest.raises(ValueError, match="Invalid distance"):
            Flight("LHR", "JFK", 100000)


class TestPassenger:
    """Tests for Passenger dataclass and PNR validation."""

    def test_valid_passenger_creation(self):
        passenger = Passenger("ABC123", "John Doe", "BA101", "12A", PriorityLevel.GOLD)
        assert passenger.pnr == "ABC123"
        assert passenger.name == "John Doe"
        assert passenger.flight_number == "BA101"
        assert passenger.seat == "12A"
        assert passenger.priority == PriorityLevel.GOLD

    def test_default_priority_is_economy(self):
        passenger = Passenger("XYZ789", "Jane Smith", "EK201", "5B")
        assert passenger.priority == PriorityLevel.ECONOMY

    def test_valid_alphanumeric_pnr(self):
        passenger = Passenger("A1B2C3", "Test User", "FL100", "1A")
        assert passenger.pnr == "A1B2C3"

    def test_rejects_empty_pnr(self):
        with pytest.raises(ValueError, match="Invalid PNR format"):
            Passenger("", "John Doe", "BA101", "12A")

    def test_rejects_pnr_with_hyphen(self):
        with pytest.raises(ValueError, match="Invalid PNR format"):
            Passenger("ABC-123", "John Doe", "BA101", "12A")

    def test_rejects_pnr_with_spaces(self):
        with pytest.raises(ValueError, match="Invalid PNR format"):
            Passenger("ABC 123", "John Doe", "BA101", "12A")

    def test_rejects_pnr_with_special_chars(self):
        with pytest.raises(ValueError, match="Invalid PNR format"):
            Passenger("ABC@123", "John Doe", "BA101", "12A")


class TestPriorityLevel:
    """Tests for PriorityLevel enum."""

    def test_platinum_value(self):
        assert PriorityLevel.PLATINUM.value == 4

    def test_gold_value(self):
        assert PriorityLevel.GOLD.value == 3

    def test_silver_value(self):
        assert PriorityLevel.SILVER.value == 2

    def test_economy_value(self):
        assert PriorityLevel.ECONOMY.value == 1

    def test_priority_ordering(self):
        assert PriorityLevel.PLATINUM.value > PriorityLevel.GOLD.value
        assert PriorityLevel.GOLD.value > PriorityLevel.SILVER.value
        assert PriorityLevel.SILVER.value > PriorityLevel.ECONOMY.value


class TestCargo:
    """Tests for Cargo dataclass."""

    def test_valid_cargo_creation(self):
        cargo = Cargo("C001", "Medical Supplies", 250.5, "BA101")
        assert cargo.item_id == "C001"
        assert cargo.description == "Medical Supplies"
        assert cargo.weight_kg == 250.5
        assert cargo.flight_number == "BA101"

    def test_default_empty_flight_number(self):
        cargo = Cargo("C002", "Electronics", 100.0)
        assert cargo.flight_number == ""

    def test_zero_weight(self):
        cargo = Cargo("C003", "Documents", 0.0)
        assert cargo.weight_kg == 0.0


class TestPriceRecord:
    """Tests for PriceRecord dataclass."""

    def test_valid_price_record_creation(self):
        record = PriceRecord("LHR", "JFK", 499.99)
        assert record.origin == "LHR"
        assert record.destination == "JFK"
        assert record.price == 499.99
        assert record.currency == "GBP"

    def test_custom_currency(self):
        record = PriceRecord("LHR", "JFK", 299.99, "USD")
        assert record.currency == "USD"

    def test_default_currency_is_gbp(self):
        record = PriceRecord("CDG", "DXB", 750.00)
        assert record.currency == "GBP"


class TestPath:
    """Tests for Path dataclass."""

    def test_valid_path_creation(self):
        path = Path(
            nodes=["LHR", "CDG", "JFK"],
            legs=[("LHR", "CDG", 340), ("CDG", "JFK", 5860)],
            total_distance=6200,
            is_shortest=True,
        )
        assert path.nodes == ["LHR", "CDG", "JFK"]
        assert path.legs == [("LHR", "CDG", 340), ("CDG", "JFK", 5860)]
        assert path.total_distance == 6200
        assert path.is_shortest is True

    def test_default_is_shortest_false(self):
        path = Path(nodes=["LHR", "JFK"], legs=[("LHR", "JFK", 5500)], total_distance=5500)
        assert path.is_shortest is False

    def test_empty_path_defaults(self):
        path = Path()
        assert path.nodes == []
        assert path.legs == []
        assert path.total_distance == 0
        assert path.is_shortest is False
