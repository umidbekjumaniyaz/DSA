"""Integration tests for all SkyNet services testing end-to-end workflows.

Tests full service-level operations ensuring data structures and business logic
work together correctly. Verifies cross-service interactions where applicable.

Requirements: 13.11, 13.12, 13.13
"""

import pytest

from skynet.services.flight_network_service import FlightNetworkService
from skynet.services.passenger_priority_service import PassengerPriorityService
from skynet.services.boarding_gate_service import BoardingGateService
from skynet.services.cargo_management_service import CargoManagementService
from skynet.services.flight_price_service import FlightPriceService
from skynet.services.passenger_registry_service import PassengerRegistryService
from skynet.services.analytics_service import AnalyticsService
from skynet.services.passenger_search_service import PassengerSearchService
from skynet.services.emergency_route_planner_service import EmergencyRoutePlannerService


class TestFlightNetworkServiceIntegration:
    """End-to-end flight network operations."""

    def test_full_network_workflow(self):
        """Add airports, add routes, compute shortest path, compute MST."""
        service = FlightNetworkService()

        # Add airports
        result = service.add_airport("LHR", "Heathrow", "London")
        assert result.success is True
        result = service.add_airport("CDG", "Charles de Gaulle", "Paris")
        assert result.success is True
        result = service.add_airport("JFK", "John F Kennedy", "New York")
        assert result.success is True
        result = service.add_airport("DXB", "Dubai International", "Dubai")
        assert result.success is True

        # Add routes
        result = service.add_route("LHR", "CDG", 340)
        assert result.success is True
        result = service.add_route("CDG", "JFK", 5800)
        assert result.success is True
        result = service.add_route("LHR", "JFK", 5500)
        assert result.success is True
        result = service.add_route("LHR", "DXB", 5500)
        assert result.success is True
        result = service.add_route("DXB", "JFK", 11000)
        assert result.success is True

        # Compute shortest path LHR -> JFK
        result = service.shortest_path("LHR", "JFK")
        assert result.success is True
        assert result.data["distance"] == 5500  # Direct route is shortest

        # Compute shortest path CDG -> DXB (must go through LHR)
        result = service.shortest_path("CDG", "DXB")
        assert result.success is True
        assert "CDG" in result.data["path"]
        assert "DXB" in result.data["path"]

        # Compute MST using Prim's
        mst_prim = service.compute_mst_prim("LHR")
        assert mst_prim.success is True
        assert len(mst_prim.edges) == 3  # V-1 = 4-1 = 3 edges

        # Compute MST using Kruskal's
        mst_kruskal = service.compute_mst_kruskal()
        assert mst_kruskal.success is True
        assert len(mst_kruskal.edges) == 3

        # Both should have same total cost
        assert mst_prim.total_cost == mst_kruskal.total_cost

    def test_network_with_disconnected_components(self):
        """Add airports without connecting routes, verify MST fails with components."""
        service = FlightNetworkService()

        # Create two disconnected groups
        service.add_airport("LHR", "Heathrow", "London")
        service.add_airport("CDG", "Charles de Gaulle", "Paris")
        service.add_airport("JFK", "John F Kennedy", "New York")
        service.add_airport("LAX", "Los Angeles International", "Los Angeles")

        # Connect only LHR-CDG and JFK-LAX (two disconnected pairs)
        service.add_route("LHR", "CDG", 340)
        service.add_route("JFK", "LAX", 3900)

        # MST should fail because graph is disconnected
        mst_prim = service.compute_mst_prim("LHR")
        assert mst_prim.success is False
        assert "disconnect" in mst_prim.message.lower() or "cannot" in mst_prim.message.lower()

        mst_kruskal = service.compute_mst_kruskal()
        assert mst_kruskal.success is False

    def test_shortest_path_same_source_dest(self):
        """Shortest path from airport to itself returns distance zero."""
        service = FlightNetworkService()
        service.add_airport("LHR", "Heathrow", "London")

        result = service.shortest_path("LHR", "LHR")
        assert result.success is True
        assert result.data["distance"] == 0

    def test_remove_airport_cascades_edges(self):
        """Removing an airport also removes all routes involving it."""
        service = FlightNetworkService()
        service.add_airport("LHR", "Heathrow", "London")
        service.add_airport("CDG", "Charles de Gaulle", "Paris")
        service.add_airport("JFK", "John F Kennedy", "New York")
        service.add_route("LHR", "CDG", 340)
        service.add_route("LHR", "JFK", 5500)

        # Remove LHR
        result = service.remove_airport("LHR")
        assert result.success is True

        # Routes through LHR should no longer exist
        result = service.shortest_path("CDG", "JFK")
        assert result.success is False  # No path exists


class TestPassengerPriorityServiceIntegration:
    """Full priority queue workflow."""

    def test_mixed_priority_processing_order(self):
        """Add passengers of all priorities, verify processing order."""
        service = PassengerPriorityService()

        # Add passengers in mixed order
        service.add_passenger("Economy Passenger", "Economy")
        service.add_passenger("Gold Passenger", "Gold")
        service.add_passenger("Platinum Passenger", "Platinum")
        service.add_passenger("Silver Passenger", "Silver")

        # Process should be in priority order: Platinum > Gold > Silver > Economy
        result = service.process_next()
        assert result.success is True
        assert result.data.name == "Platinum Passenger"

        result = service.process_next()
        assert result.success is True
        assert result.data.name == "Gold Passenger"

        result = service.process_next()
        assert result.success is True
        assert result.data.name == "Silver Passenger"

        result = service.process_next()
        assert result.success is True
        assert result.data.name == "Economy Passenger"

        # Queue should now be empty
        result = service.process_next()
        assert result.success is False

    def test_fifo_within_same_priority(self):
        """Passengers with same priority are processed in FIFO order."""
        service = PassengerPriorityService()

        service.add_passenger("First Gold", "Gold")
        service.add_passenger("Second Gold", "Gold")
        service.add_passenger("Third Gold", "Gold")

        result = service.process_next()
        assert result.data.name == "First Gold"
        result = service.process_next()
        assert result.data.name == "Second Gold"
        result = service.process_next()
        assert result.data.name == "Third Gold"

    def test_invalid_priority_rejected(self):
        """Invalid priority level is rejected at service boundary."""
        service = PassengerPriorityService()

        result = service.add_passenger("Test", "VIP")
        assert result.success is False
        assert "Invalid priority" in result.message

    def test_peek_does_not_remove(self):
        """Peek returns next passenger without changing queue state."""
        service = PassengerPriorityService()
        service.add_passenger("Only Passenger", "Platinum")

        peek_result = service.peek_next()
        assert peek_result.success is True
        assert peek_result.data.name == "Only Passenger"

        # Still there after peek
        process_result = service.process_next()
        assert process_result.success is True
        assert process_result.data.name == "Only Passenger"


class TestBoardingGateServiceIntegration:
    """Boarding queue workflow."""

    def test_full_boarding_workflow(self):
        """Add multiple passengers, board them all, verify FIFO."""
        service = BoardingGateService()

        # Add passengers in order
        result = service.add_to_boarding("P001", "Alice")
        assert result.success is True
        result = service.add_to_boarding("P002", "Bob")
        assert result.success is True
        result = service.add_to_boarding("P003", "Charlie")
        assert result.success is True

        # Board in FIFO order
        result = service.board_next()
        assert result.success is True
        assert result.data["name"] == "Alice"

        result = service.board_next()
        assert result.success is True
        assert result.data["name"] == "Bob"

        result = service.board_next()
        assert result.success is True
        assert result.data["name"] == "Charlie"

        # Queue empty
        result = service.board_next()
        assert result.success is False

    def test_duplicate_passenger_rejected(self):
        """Attempting to add the same passenger twice is rejected."""
        service = BoardingGateService()

        result = service.add_to_boarding("P001", "Alice")
        assert result.success is True

        result = service.add_to_boarding("P001", "Alice Again")
        assert result.success is False
        assert "Duplicate" in result.message or "already" in result.message

    def test_board_from_empty_queue(self):
        """Boarding from empty queue returns appropriate error."""
        service = BoardingGateService()

        result = service.board_next()
        assert result.success is False
        assert "No passengers" in result.message or "empty" in result.message.lower()


class TestCargoManagementServiceIntegration:
    """Cargo LIFO workflow."""

    def test_full_cargo_workflow(self):
        """Load multiple items, verify LIFO unloading order."""
        service = CargoManagementService()

        # Load cargo items
        service.load_cargo("C001", "Electronics", 50.0)
        service.load_cargo("C002", "Food Supplies", 30.0)
        service.load_cargo("C003", "Medical Equipment", 20.0)

        # Unload in LIFO order (last loaded first)
        result = service.unload_cargo()
        assert result.success is True
        assert result.data.item_id == "C003"

        result = service.unload_cargo()
        assert result.success is True
        assert result.data.item_id == "C002"

        result = service.unload_cargo()
        assert result.success is True
        assert result.data.item_id == "C001"

        # Stack empty
        result = service.unload_cargo()
        assert result.success is False

    def test_peek_top_shows_last_loaded(self):
        """Peek shows the most recently loaded item without removing."""
        service = CargoManagementService()

        service.load_cargo("C001", "Electronics", 50.0)
        service.load_cargo("C002", "Food Supplies", 30.0)

        result = service.peek_top()
        assert result.success is True
        assert result.data.item_id == "C002"

        # Still there after peek
        result = service.unload_cargo()
        assert result.data.item_id == "C002"

    def test_unload_from_empty_stack(self):
        """Unloading from empty stack returns appropriate error."""
        service = CargoManagementService()

        result = service.unload_cargo()
        assert result.success is False
        assert "no cargo" in result.message.lower() or "Cannot" in result.message


class TestFlightPriceServiceIntegration:
    """AVL tree price operations."""

    def test_full_price_workflow(self):
        """Add prices, range search, delete, verify balance."""
        service = FlightPriceService()

        # Add prices
        result = service.add_price("LHR", "JFK", 450.0)
        assert result.success is True
        result = service.add_price("LHR", "CDG", 120.0)
        assert result.success is True
        result = service.add_price("CDG", "JFK", 380.0)
        assert result.success is True
        result = service.add_price("DXB", "LHR", 600.0)
        assert result.success is True
        result = service.add_price("JFK", "LAX", 250.0)
        assert result.success is True

        # Search for a specific price
        result = service.search_price(450.0)
        assert result.success is True

        # Range search
        result = service.range_search(100.0, 400.0)
        assert result.success is True
        assert len(result.data) == 3  # 120, 250, 380

        # Delete a price
        result = service.remove_price(380.0)
        assert result.success is True

        # Verify deleted price is no longer found
        result = service.search_price(380.0)
        assert result.success is False

        # Range search after deletion
        result = service.range_search(100.0, 400.0)
        assert result.success is True
        assert len(result.data) == 2  # 120, 250

    def test_duplicate_price_key_stored_separately(self):
        """Multiple records at same price are stored as separate entries."""
        service = FlightPriceService()

        service.add_price("LHR", "JFK", 300.0)
        service.add_price("CDG", "DXB", 300.0)

        result = service.search_price(300.0)
        assert result.success is True
        # Should find records at this price
        assert result.data is not None

    def test_delete_nonexistent_price(self):
        """Deleting a non-existent price returns failure."""
        service = FlightPriceService()

        result = service.remove_price(999.0)
        assert result.success is False


class TestPassengerRegistryServiceIntegration:
    """CRUD operations via service."""

    def test_full_crud_workflow(self):
        """Create, search, update, delete record, verify at each step."""
        service = PassengerRegistryService()

        # Create
        result = service.create_record("ABC123", "John Smith", "BA256", "12A")
        assert result.success is True
        assert result.data["name"] == "John Smith"

        # Search
        result = service.search_record("ABC123")
        assert result.success is True
        assert result.data["name"] == "John Smith"
        assert result.data["flight"] == "BA256"
        assert result.data["seat"] == "12A"

        # Update
        result = service.update_record("ABC123", seat="14B", flight="BA257")
        assert result.success is True
        assert result.data["seat"] == "14B"
        assert result.data["flight"] == "BA257"

        # Verify update persisted
        result = service.search_record("ABC123")
        assert result.success is True
        assert result.data["seat"] == "14B"
        assert result.data["flight"] == "BA257"
        assert result.data["name"] == "John Smith"  # Unchanged field preserved

        # Delete
        result = service.delete_record("ABC123")
        assert result.success is True

        # Verify deleted
        result = service.search_record("ABC123")
        assert result.success is False

    def test_duplicate_pnr_rejected(self):
        """Creating a record with a duplicate PNR is rejected."""
        service = PassengerRegistryService()

        service.create_record("ABC123", "John Smith", "BA256", "12A")
        result = service.create_record("ABC123", "Jane Doe", "BA257", "14B")
        assert result.success is False
        assert "Duplicate" in result.message or "duplicate" in result.message

    def test_invalid_pnr_format_rejected(self):
        """Invalid PNR format is rejected for all operations."""
        service = PassengerRegistryService()

        # Empty PNR
        result = service.create_record("", "John", "BA256", "12A")
        assert result.success is False

        # Special characters
        result = service.create_record("AB-123", "John", "BA256", "12A")
        assert result.success is False

    def test_operations_on_nonexistent_pnr(self):
        """Search, update, delete on non-existent PNR return failure."""
        service = PassengerRegistryService()

        result = service.search_record("NOEXIST")
        assert result.success is False

        result = service.update_record("NOEXIST", name="New Name")
        assert result.success is False

        result = service.delete_record("NOEXIST")
        assert result.success is False


class TestAnalyticsServiceIntegration:
    """Sorting comparison workflow."""

    def test_comparison_report_generated(self):
        """Run comparison report, verify both algorithms run."""
        service = AnalyticsService()
        data = [42, 17, 93, 5, 64, 28, 81, 3, 55, 12]
        key_func = lambda x: x

        report = service.comparison_report(data, key_func)

        # Report should mention both algorithms
        assert "QuickSort" in report or "Quick" in report
        assert "MergeSort" in report or "Merge" in report
        assert "10" in report  # Dataset size

    def test_both_algorithms_produce_same_output(self):
        """QuickSort and MergeSort produce identical sorted output."""
        service = AnalyticsService()
        data = [42, 17, 93, 5, 64, 28, 81, 3, 55, 12]
        key_func = lambda x: x

        qs_result = service.sort_with_quicksort(list(data), key_func)
        ms_result = service.sort_with_mergesort(list(data), key_func)

        assert qs_result.sorted_data == ms_result.sorted_data
        assert qs_result.sorted_data == sorted(data)

    def test_sort_empty_dataset(self):
        """Sorting empty list succeeds without error."""
        service = AnalyticsService()
        data = []
        key_func = lambda x: x

        qs_result = service.sort_with_quicksort(data, key_func)
        ms_result = service.sort_with_mergesort(data, key_func)

        assert qs_result.sorted_data == []
        assert ms_result.sorted_data == []

    def test_sort_single_element(self):
        """Sorting single-element list returns it unchanged."""
        service = AnalyticsService()
        data = [42]
        key_func = lambda x: x

        qs_result = service.sort_with_quicksort(data, key_func)
        assert qs_result.sorted_data == [42]

    def test_performance_metrics_populated(self):
        """Sort results include execution time and comparison counts."""
        service = AnalyticsService()
        data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        key_func = lambda x: x

        qs_result = service.sort_with_quicksort(data, key_func)
        ms_result = service.sort_with_mergesort(data, key_func)

        assert qs_result.execution_time_ms >= 0
        assert ms_result.execution_time_ms >= 0
        assert qs_result.comparisons > 0
        assert ms_result.comparisons > 0


class TestPassengerSearchServiceIntegration:
    """KMP search through service with real registry."""

    def _setup_registry_and_search(self):
        """Helper to set up registry with test data and search service."""
        registry = PassengerRegistryService()
        registry.create_record("ABC123", "John Smith", "BA256", "12A")
        registry.create_record("DEF456", "Jane Doe", "EK101", "3B")
        registry.create_record("GHI789", "Alice Johnson", "BA256", "14C")
        registry.create_record("JKL012", "Bob Williams", "QF007", "22D")
        return registry, PassengerSearchService(registry)

    def test_search_across_multiple_records(self):
        """Add records to registry, search by various fields."""
        registry, search_service = self._setup_registry_and_search()

        # Search by name - case insensitive
        result = search_service.search_by_name("john")
        assert result.success is True
        # Should find "John Smith" and "Alice Johnson"
        assert len(result.data) >= 1

    def test_search_by_flight_number(self):
        """Search by flight number finds all passengers on that flight."""
        registry, search_service = self._setup_registry_and_search()

        result = search_service.search_by_flight("BA256")
        assert result.success is True
        # John Smith and Alice Johnson are on BA256
        assert len(result.data) == 2

    def test_search_by_pnr_fragment(self):
        """Search by PNR fragment finds matching records."""
        registry, search_service = self._setup_registry_and_search()

        result = search_service.search_by_pnr("ABC")
        assert result.success is True
        assert len(result.data) == 1

    def test_search_empty_pattern_rejected(self):
        """Empty search pattern is rejected."""
        registry, search_service = self._setup_registry_and_search()

        result = search_service.search_by_name("")
        assert result.success is False

    def test_search_no_match_returns_empty(self):
        """Pattern not found returns empty results."""
        registry, search_service = self._setup_registry_and_search()

        result = search_service.search_by_name("Zeppelin")
        assert result.success is True
        assert result.data == []

    def test_cross_service_registry_updates_reflect_in_search(self):
        """Adding records to registry makes them findable via search service."""
        registry, search_service = self._setup_registry_and_search()

        # Add a new record
        registry.create_record("NEW001", "Zara Thompson", "LH440", "8F")

        # Should now be findable
        result = search_service.search_by_name("Zara")
        assert result.success is True
        assert len(result.data) == 1


class TestEmergencyRoutePlannerServiceIntegration:
    """Backtracking with closures."""

    def _build_network(self):
        """Build a test network for emergency route planning."""
        fns = FlightNetworkService()
        fns.add_airport("LHR", "Heathrow", "London")
        fns.add_airport("CDG", "Charles de Gaulle", "Paris")
        fns.add_airport("FRA", "Frankfurt", "Frankfurt")
        fns.add_airport("AMS", "Schiphol", "Amsterdam")
        fns.add_airport("JFK", "John F Kennedy", "New York")

        fns.add_route("LHR", "CDG", 340)
        fns.add_route("LHR", "AMS", 370)
        fns.add_route("CDG", "FRA", 450)
        fns.add_route("AMS", "FRA", 400)
        fns.add_route("FRA", "JFK", 6200)
        fns.add_route("CDG", "JFK", 5800)
        fns.add_route("LHR", "JFK", 5500)

        return fns

    def test_emergency_route_workflow(self):
        """Build network, close airport, find alternatives, verify shortest marked."""
        fns = self._build_network()
        planner = EmergencyRoutePlannerService(fns.graph)

        # Close CDG - now paths through CDG should be excluded
        result = planner.close_airport("CDG")
        assert result.success is True

        # Find alternatives from LHR to JFK avoiding CDG
        result = planner.find_alternatives("LHR", "JFK")
        assert result.success is True
        paths = result.data

        # Should find at least the direct route and via AMS-FRA
        assert len(paths) >= 1

        # No path should contain CDG
        for path in paths:
            assert "CDG" not in path.nodes

        # Shortest path should be marked
        shortest_paths = [p for p in paths if p.is_shortest]
        assert len(shortest_paths) == 1

    def test_no_alternative_when_all_blocked(self):
        """When no alternative exists, service reports appropriately."""
        fns = FlightNetworkService()
        fns.add_airport("LHR", "Heathrow", "London")
        fns.add_airport("CDG", "Charles de Gaulle", "Paris")
        fns.add_airport("JFK", "John F Kennedy", "New York")

        # Only path: LHR -> CDG -> JFK
        fns.add_route("LHR", "CDG", 340)
        fns.add_route("CDG", "JFK", 5800)

        planner = EmergencyRoutePlannerService(fns.graph)
        planner.close_airport("CDG")

        # No alternative route exists from LHR to JFK
        result = planner.find_alternatives("LHR", "JFK")
        assert result.success is False
        assert "No alternative" in result.message or "no alternative" in result.message.lower()

    def test_reopen_airport_restores_routes(self):
        """Reopening an airport makes it available for routing again."""
        fns = self._build_network()
        planner = EmergencyRoutePlannerService(fns.graph)

        planner.close_airport("CDG")

        # Reopen
        result = planner.reopen_airport("CDG")
        assert result.success is True

        # Now CDG should be available in routes
        result = planner.find_alternatives("LHR", "JFK")
        assert result.success is True
        # CDG can appear in paths now
        all_nodes = set()
        for path in result.data:
            all_nodes.update(path.nodes)
        assert "CDG" in all_nodes  # CDG should be in at least one path

    def test_closed_endpoint_rejected(self):
        """Source or destination that is closed is rejected."""
        fns = self._build_network()
        planner = EmergencyRoutePlannerService(fns.graph)

        planner.close_airport("LHR")

        result = planner.find_alternatives("LHR", "JFK")
        assert result.success is False
        assert "closed" in result.message.lower()


class TestCrossServiceInteractions:
    """Tests verifying cross-service interaction patterns."""

    def test_search_service_uses_registry_service(self):
        """PassengerSearchService correctly interacts with PassengerRegistryService."""
        registry = PassengerRegistryService()
        registry.create_record("ABC123", "John Smith", "BA256", "12A")
        registry.create_record("DEF456", "Sarah Connor", "EK101", "3B")

        search = PassengerSearchService(registry)

        # Search should find records from the live registry
        result = search.search_by_name("Smith")
        assert result.success is True
        assert len(result.data) >= 1

    def test_emergency_planner_uses_network_graph(self):
        """EmergencyRoutePlannerService shares graph with FlightNetworkService."""
        fns = FlightNetworkService()
        fns.add_airport("LHR", "Heathrow", "London")
        fns.add_airport("CDG", "Charles de Gaulle", "Paris")
        fns.add_route("LHR", "CDG", 340)

        # Emergency planner uses the same graph instance
        planner = EmergencyRoutePlannerService(fns.graph)

        # Adding a new airport to network makes it available to planner
        fns.add_airport("FRA", "Frankfurt", "Frankfurt")
        fns.add_route("CDG", "FRA", 450)

        result = planner.find_alternatives("LHR", "FRA")
        assert result.success is True
        assert len(result.data) >= 1

    def test_network_and_planner_full_scenario(self):
        """Full scenario: build network, compute path, close airport, find alternative."""
        fns = FlightNetworkService()
        fns.add_airport("LHR", "Heathrow", "London")
        fns.add_airport("CDG", "Charles de Gaulle", "Paris")
        fns.add_airport("FRA", "Frankfurt", "Frankfurt")
        fns.add_route("LHR", "CDG", 340)
        fns.add_route("CDG", "FRA", 450)
        fns.add_route("LHR", "FRA", 650)

        # Normal shortest path
        result = fns.shortest_path("LHR", "FRA")
        assert result.success is True
        # LHR -> CDG -> FRA = 790 vs LHR -> FRA = 650
        assert result.data["distance"] == 650

        # Close CDG and find alternatives
        planner = EmergencyRoutePlannerService(fns.graph)
        planner.close_airport("CDG")
        result = planner.find_alternatives("LHR", "FRA")
        assert result.success is True
        # Only direct route available
        assert len(result.data) == 1
        assert result.data[0].total_distance == 650
