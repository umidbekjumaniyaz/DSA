"""Unit tests for the services layer error handling and console dispatch."""

import unittest

from data_structures.fifo_queue import Queue
from data_structures.graph import Graph
from data_structures.hash_table import HashTable
from data_structures.lifo_stack import Stack
from data_structures.max_heap import MaxHeap
from data_structures.price_tree import AVLTree
from models.passenger import Passenger
from models.ticket_status import TicketStatus
from services.boarding_service import BoardingService
from services.cargo_service import CargoService
from services.checkin_service import CheckInService
from services.contingency_service import ContingencyService
from services.pricing_service import PricingService
from services.results import ErrorCode
from services.route_planning_service import RoutePlanningService


class TestRoutePlanningService(unittest.TestCase):
    def setUp(self):
        self.svc = RoutePlanningService(Graph())

    def test_empty_graph_display(self):
        r = self.svc.display_network()
        self.assertFalse(r.ok)
        self.assertEqual(r.error, ErrorCode.EMPTY_GRAPH)

    def test_duplicate_airport(self):
        self.svc.add_airport("LHR")
        r = self.svc.add_airport("LHR")
        self.assertEqual(r.error, ErrorCode.DUPLICATE_AIRPORT)

    def test_missing_airport_route(self):
        self.svc.add_airport("A")
        r = self.svc.add_route("A", "B", 10)
        self.assertEqual(r.error, ErrorCode.MISSING_AIRPORT)

    def test_duplicate_route(self):
        self.svc.add_airport("A")
        self.svc.add_airport("B")
        self.svc.add_route("A", "B", 10)
        r = self.svc.add_route("A", "B", 5)
        self.assertEqual(r.error, ErrorCode.DUPLICATE_ROUTE)

    def test_no_available_route(self):
        for c in "ABCD":
            self.svc.add_airport(c)
        self.svc.add_route("A", "B", 1)
        self.svc.add_route("C", "D", 1)
        r = self.svc.find_cheapest_route("A", "D")
        self.assertEqual(r.error, ErrorCode.NO_AVAILABLE_ROUTE)

    def test_disconnected_mst(self):
        for c in "ABCD":
            self.svc.add_airport(c)
        self.svc.add_route("A", "B", 1)
        self.svc.add_route("C", "D", 1)
        r = self.svc.generate_backup_network("prim")
        self.assertEqual(r.error, ErrorCode.DISCONNECTED_GRAPH)


class TestCheckInService(unittest.TestCase):
    def setUp(self):
        self.svc = CheckInService(
            MaxHeap(priority_of=lambda p: int(p.status)), HashTable()
        )

    def test_serve_empty_queue(self):
        self.assertEqual(self.svc.serve_next().error, ErrorCode.EMPTY_QUEUE)

    def test_register_lookup_delete(self):
        p = Passenger("ABC123", "Alice", TicketStatus.GOLD)
        self.assertTrue(self.svc.register_passenger(p).ok)
        self.assertTrue(self.svc.lookup("ABC123").ok)
        self.assertTrue(self.svc.delete("ABC123").ok)
        self.assertEqual(self.svc.lookup("ABC123").error,
                         ErrorCode.PASSENGER_NOT_FOUND)

    def test_duplicate_pnr(self):
        p = Passenger("ABC123", "Alice", TicketStatus.GOLD)
        self.svc.register_passenger(p)
        self.assertEqual(self.svc.register_passenger(p).error,
                         ErrorCode.DUPLICATE_PNR)

    def test_invalid_pnr(self):
        self.assertEqual(self.svc.lookup("bad").error, ErrorCode.INVALID_PNR)


class TestQueueStackServices(unittest.TestCase):
    def test_boarding_empty(self):
        svc = BoardingService(Queue())
        self.assertEqual(svc.call_next().error, ErrorCode.EMPTY_QUEUE)

    def test_cargo_empty(self):
        svc = CargoService(Stack())
        self.assertEqual(svc.unload_item().error, ErrorCode.EMPTY_STACK)


class TestPricingService(unittest.TestCase):
    def test_inverted_range_empty(self):
        svc = PricingService(AVLTree())
        svc.insert_price(10)
        r = svc.range_search(100, 0)
        self.assertTrue(r.ok)
        self.assertEqual(r.payload, [])


class TestContingencyService(unittest.TestCase):
    def test_missing_airport(self):
        g = Graph()
        g.add_airport("A")
        svc = ContingencyService(g)
        self.assertEqual(svc.enumerate_paths("A", "Z").error,
                         ErrorCode.MISSING_AIRPORT)


class TestConsoleDispatch(unittest.TestCase):
    def test_error_renders_and_loop_continues(self):
        from console.console_menu import ConsoleMenu
        outputs = []
        # Choose "display network" on empty graph (error), then exit.
        inputs = iter(["3", "0"])
        menu = ConsoleMenu(input_fn=lambda _="": next(inputs),
                           output_fn=outputs.append)
        menu.run()
        joined = "\n".join(outputs)
        self.assertIn("[ERROR]", joined)
        self.assertIn("Exiting SkyNet", joined)


if __name__ == "__main__":
    unittest.main()
