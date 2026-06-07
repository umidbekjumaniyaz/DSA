"""Unit tests for domain models and the error catalogue."""

import unittest

from models.airport import Airport
from models.flight_record import FlightRecord
from models.passenger import Passenger
from models.route import Route
from models.ticket_status import TicketStatus
from services.results import ErrorCode, OperationResult, message_for


class TestModels(unittest.TestCase):
    def test_airport_normalises_code(self):
        self.assertEqual(Airport("lhr").code, "LHR")
        with self.assertRaises(ValueError):
            Airport("   ")

    def test_route_validation(self):
        with self.assertRaises(ValueError):
            Route("A", "B", -1)
        with self.assertRaises(ValueError):
            Route("A", "A", 5)
        r = Route("a", "b", 3)
        self.assertEqual(r.endpoints(), frozenset({"A", "B"}))
        self.assertEqual(r.other("A"), "B")

    def test_ticket_status_order(self):
        self.assertGreater(TicketStatus.PLATINUM, TicketStatus.GOLD)
        self.assertGreater(TicketStatus.GOLD, TicketStatus.SILVER)
        self.assertGreater(TicketStatus.SILVER, TicketStatus.ECONOMY)
        self.assertEqual(TicketStatus.from_name("platinum"), TicketStatus.PLATINUM)

    def test_passenger_pnr(self):
        self.assertTrue(Passenger.is_valid_pnr("ABC123"))
        self.assertFalse(Passenger.is_valid_pnr("abc"))
        self.assertFalse(Passenger.is_valid_pnr("ABC12$"))
        with self.assertRaises(ValueError):
            Passenger("bad", "X")

    def test_flight_record_sort_value(self):
        f = FlightRecord("SK1", 600, 0.8)
        self.assertEqual(f.sort_value("departure_time"), 600)
        with self.assertRaises(ValueError):
            f.sort_value("unknown")


class TestErrorCatalogue(unittest.TestCase):
    def test_every_error_has_unique_nonempty_message(self):
        messages = set()
        for code in ErrorCode:
            msg = message_for(code, code="X", a="A", b="B", src="S",
                              dst="D", pnr="P", detail="d")
            self.assertTrue(msg)
            messages.add(msg)
        self.assertEqual(len(messages), len(list(ErrorCode)))

    def test_operation_result_factories(self):
        ok = OperationResult.success(payload=1, message="done")
        self.assertTrue(ok.ok)
        fail = OperationResult.failure(ErrorCode.EMPTY_GRAPH)
        self.assertFalse(fail.ok)
        self.assertEqual(fail.error, ErrorCode.EMPTY_GRAPH)


if __name__ == "__main__":
    unittest.main()
