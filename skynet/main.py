"""SkyNet - Global Aviation Logistics System entry point.

This module instantiates all services, wires them to menu selections,
and runs the main application loop. Each subsystem has a dedicated
runner function that displays its menu, accepts input, calls service
methods, and displays results.
"""

from skynet.services.flight_network_service import FlightNetworkService
from skynet.services.passenger_priority_service import PassengerPriorityService
from skynet.services.boarding_gate_service import BoardingGateService
from skynet.services.cargo_management_service import CargoManagementService
from skynet.services.flight_price_service import FlightPriceService
from skynet.services.passenger_registry_service import PassengerRegistryService
from skynet.services.analytics_service import AnalyticsService
from skynet.services.passenger_search_service import PassengerSearchService
from skynet.services.emergency_route_planner_service import EmergencyRoutePlannerService

from skynet.ui.menu import (
    display_main_menu,
    display_flight_network_menu,
    display_passenger_priority_menu,
    display_boarding_gate_menu,
    display_cargo_management_menu,
    display_flight_price_menu,
    display_passenger_registry_menu,
    display_analytics_menu,
    display_passenger_search_menu,
    display_emergency_route_menu,
)
from skynet.ui.input_handler import (
    get_int_input,
    get_float_input,
    get_string_input,
    get_iata_input,
    get_priority_input,
)


def run_flight_network(service: FlightNetworkService) -> None:
    """Run the Flight Network System subsystem loop.

    Handles all flight network operations: add/remove airports,
    add/remove routes, shortest path, MST algorithms, and display.
    """
    while True:
        print(display_flight_network_menu())
        choice = get_int_input("Enter choice: ", 0, 8)

        if choice == 0:
            break
        elif choice == 1:
            # Add Airport
            iata = get_iata_input("Enter IATA code (3 letters): ")
            name = get_string_input("Enter airport name: ")
            city = get_string_input("Enter city: ")
            result = service.add_airport(iata, name, city)
            print(f"\n  {result.message}")
        elif choice == 2:
            # Remove Airport
            iata = get_iata_input("Enter IATA code to remove: ")
            result = service.remove_airport(iata)
            print(f"\n  {result.message}")
        elif choice == 3:
            # Add Route
            src = get_iata_input("Enter source IATA code: ")
            dest = get_iata_input("Enter destination IATA code: ")
            distance = get_int_input("Enter distance (km, 1-99999): ", 1, 99999)
            result = service.add_route(src, dest, distance)
            print(f"\n  {result.message}")
        elif choice == 4:
            # Remove Route
            src = get_iata_input("Enter source IATA code: ")
            dest = get_iata_input("Enter destination IATA code: ")
            result = service.remove_route(src, dest)
            print(f"\n  {result.message}")
        elif choice == 5:
            # Shortest Path
            src = get_iata_input("Enter source IATA code: ")
            dest = get_iata_input("Enter destination IATA code: ")
            result = service.shortest_path(src, dest)
            print(f"\n  {result.message}")
            if result.success and result.data:
                path_data = result.data
                if isinstance(path_data, dict):
                    path = path_data.get("path", [])
                    dist = path_data.get("distance", 0)
                    print(f"  Path: {' -> '.join(path)}")
                    print(f"  Total distance: {dist} km")
        elif choice == 6:
            # MST - Prim's
            start = get_iata_input("Enter starting IATA code: ")
            result = service.compute_mst_prim(start)
            print(f"\n  {result.message}")
            if result.success:
                print(f"  MST Edges:")
                for src_node, dest_node, weight in result.edges:
                    print(f"    {src_node} -- {dest_node}: {weight} km")
                print(f"  Total MST cost: {result.total_cost} km")
        elif choice == 7:
            # MST - Kruskal's
            result = service.compute_mst_kruskal()
            print(f"\n  {result.message}")
            if result.success:
                print(f"  MST Edges:")
                for src_node, dest_node, weight in result.edges:
                    print(f"    {src_node} -- {dest_node}: {weight} km")
                print(f"  Total MST cost: {result.total_cost} km")
        elif choice == 8:
            # Display Network
            print(f"\n{service.display_network()}")


def run_passenger_priority(service: PassengerPriorityService) -> None:
    """Run the Passenger Priority System subsystem loop.

    Handles adding passengers, processing next, peeking, and displaying queue.
    """
    while True:
        print(display_passenger_priority_menu())
        choice = get_int_input("Enter choice: ", 0, 4)

        if choice == 0:
            break
        elif choice == 1:
            # Add Passenger
            name = get_string_input("Enter passenger name: ")
            priority = get_priority_input("Enter priority (Platinum/Gold/Silver/Economy): ")
            result = service.add_passenger(name, priority)
            print(f"\n  {result.message}")
        elif choice == 2:
            # Process Next
            result = service.process_next()
            print(f"\n  {result.message}")
        elif choice == 3:
            # Peek Next
            result = service.peek_next()
            print(f"\n  {result.message}")
        elif choice == 4:
            # Display Queue
            print(f"\n{service.display_queue()}")


def run_boarding_gate(service: BoardingGateService) -> None:
    """Run the Boarding Gate System subsystem loop.

    Handles adding passengers to queue, boarding next, and displaying queue.
    """
    while True:
        print(display_boarding_gate_menu())
        choice = get_int_input("Enter choice: ", 0, 3)

        if choice == 0:
            break
        elif choice == 1:
            # Add Passenger to Queue
            passenger_id = get_string_input("Enter passenger ID: ")
            name = get_string_input("Enter passenger name: ")
            result = service.add_to_boarding(passenger_id, name)
            print(f"\n  {result.message}")
        elif choice == 2:
            # Board Next Passenger
            result = service.board_next()
            print(f"\n  {result.message}")
        elif choice == 3:
            # Display Boarding Queue
            print(f"\n{service.display_queue()}")


def run_cargo_management(service: CargoManagementService) -> None:
    """Run the Cargo Management System subsystem loop.

    Handles loading, unloading, peeking, and displaying cargo stack.
    """
    while True:
        print(display_cargo_management_menu())
        choice = get_int_input("Enter choice: ", 0, 4)

        if choice == 0:
            break
        elif choice == 1:
            # Load Cargo
            item_id = get_string_input("Enter cargo item ID: ")
            description = get_string_input("Enter description: ")
            weight = get_float_input("Enter weight (kg): ", min_val=0.0)
            result = service.load_cargo(item_id, description, weight)
            print(f"\n  {result.message}")
        elif choice == 2:
            # Unload Cargo
            result = service.unload_cargo()
            print(f"\n  {result.message}")
        elif choice == 3:
            # Peek Top
            result = service.peek_top()
            print(f"\n  {result.message}")
        elif choice == 4:
            # Display Stack
            print(f"\n{service.display_stack()}")


def run_flight_price(service: FlightPriceService) -> None:
    """Run the Flight Price Database subsystem loop.

    Handles adding, removing, searching, range searching, and displaying prices.
    """
    while True:
        print(display_flight_price_menu())
        choice = get_int_input("Enter choice: ", 0, 5)

        if choice == 0:
            break
        elif choice == 1:
            # Add Price Record
            origin = get_iata_input("Enter origin IATA code: ")
            destination = get_iata_input("Enter destination IATA code: ")
            price = get_float_input("Enter price: ", min_val=0.0)
            result = service.add_price(origin, destination, price)
            print(f"\n  {result.message}")
        elif choice == 2:
            # Remove Price Record
            price = get_float_input("Enter price value to remove: ")
            result = service.remove_price(price)
            print(f"\n  {result.message}")
        elif choice == 3:
            # Search by Price
            price = get_float_input("Enter price to search: ")
            result = service.search_price(price)
            print(f"\n  {result.message}")
            if result.success and result.data:
                if isinstance(result.data, list):
                    for record in result.data:
                        print(f"    {record.origin} -> {record.destination}: {record.price} {record.currency}")
                else:
                    record = result.data
                    print(f"    {record.origin} -> {record.destination}: {record.price} {record.currency}")
        elif choice == 4:
            # Range Search
            min_price = get_float_input("Enter minimum price: ", min_val=0.0)
            max_price = get_float_input("Enter maximum price: ", min_val=min_price)
            result = service.range_search(min_price, max_price)
            print(f"\n  {result.message}")
            if result.success and result.data:
                for record in result.data:
                    print(f"    {record.origin} -> {record.destination}: {record.price} {record.currency}")
        elif choice == 5:
            # Display All Prices
            print(f"\n{service.display_prices()}")


def run_passenger_registry(service: PassengerRegistryService) -> None:
    """Run the Passenger Registry subsystem loop.

    Handles creating, searching, updating, deleting, and displaying records.
    """
    while True:
        print(display_passenger_registry_menu())
        choice = get_int_input("Enter choice: ", 0, 5)

        if choice == 0:
            break
        elif choice == 1:
            # Create Record
            pnr = get_string_input("Enter PNR (alphanumeric): ")
            name = get_string_input("Enter passenger name: ")
            flight = get_string_input("Enter flight number: ")
            seat = get_string_input("Enter seat assignment: ")
            result = service.create_record(pnr, name, flight, seat)
            print(f"\n  {result.message}")
        elif choice == 2:
            # Search Record
            pnr = get_string_input("Enter PNR to search: ")
            result = service.search_record(pnr)
            print(f"\n  {result.message}")
            if result.success and result.data:
                data = result.data
                print(f"    PNR: {data['pnr']}")
                print(f"    Name: {data['name']}")
                print(f"    Flight: {data['flight']}")
                print(f"    Seat: {data['seat']}")
        elif choice == 3:
            # Update Record
            pnr = get_string_input("Enter PNR to update: ")
            print("  Leave fields blank to keep current value.")
            name = input("  New name (or press Enter to skip): ").strip()
            flight = input("  New flight (or press Enter to skip): ").strip()
            seat = input("  New seat (or press Enter to skip): ").strip()
            update_fields = {}
            if name:
                update_fields["name"] = name
            if flight:
                update_fields["flight"] = flight
            if seat:
                update_fields["seat"] = seat
            if not update_fields:
                print("\n  No fields to update.")
            else:
                result = service.update_record(pnr, **update_fields)
                print(f"\n  {result.message}")
        elif choice == 4:
            # Delete Record
            pnr = get_string_input("Enter PNR to delete: ")
            result = service.delete_record(pnr)
            print(f"\n  {result.message}")
        elif choice == 5:
            # Display Registry
            print(f"\n{service.display_registry()}")


def run_analytics(service: AnalyticsService) -> None:
    """Run the Analytics System subsystem loop.

    Handles sorting datasets with QuickSort, MergeSort, and comparison reports.
    Users enter comma-separated numeric values for sorting.
    """
    while True:
        print(display_analytics_menu())
        choice = get_int_input("Enter choice: ", 0, 3)

        if choice == 0:
            break
        elif choice in (1, 2, 3):
            # Get dataset from user
            raw = get_string_input("Enter comma-separated numeric values (e.g., 45,12,78,3,90): ")
            try:
                data = [float(x.strip()) for x in raw.split(",") if x.strip()]
            except ValueError:
                print("\n  Error: All values must be numeric.")
                continue

            if len(data) > 10000:
                print("\n  Error: Dataset cannot exceed 10,000 elements.")
                continue

            key_func = lambda x: x  # noqa: E731

            if choice == 1:
                # QuickSort
                result = service.sort_with_quicksort(data, key_func)
                print(f"\n  QuickSort Result:")
                print(f"    Sorted: {result.sorted_data}")
                print(f"    Time: {result.execution_time_ms:.2f} ms")
                print(f"    Memory: {result.memory_bytes} bytes")
                print(f"    Comparisons: {result.comparisons}")
            elif choice == 2:
                # MergeSort
                result = service.sort_with_mergesort(data, key_func)
                print(f"\n  MergeSort Result:")
                print(f"    Sorted: {result.sorted_data}")
                print(f"    Time: {result.execution_time_ms:.2f} ms")
                print(f"    Memory: {result.memory_bytes} bytes")
                print(f"    Comparisons: {result.comparisons}")
            elif choice == 3:
                # Comparison Report
                report = service.comparison_report(data, key_func)
                print(f"\n{report}")


def run_passenger_search(service: PassengerSearchService) -> None:
    """Run the Passenger Search subsystem loop.

    Handles KMP-based pattern matching searches by name, PNR, and flight number.
    """
    while True:
        print(display_passenger_search_menu())
        choice = get_int_input("Enter choice: ", 0, 3)

        if choice == 0:
            break
        elif choice == 1:
            # Search by Name
            pattern = get_string_input("Enter name search pattern: ")
            result = service.search_by_name(pattern)
            _display_search_results(result)
        elif choice == 2:
            # Search by PNR
            pattern = get_string_input("Enter PNR search pattern: ")
            result = service.search_by_pnr(pattern)
            _display_search_results(result)
        elif choice == 3:
            # Search by Flight Number
            pattern = get_string_input("Enter flight number search pattern: ")
            result = service.search_by_flight(pattern)
            _display_search_results(result)


def _display_search_results(result) -> None:
    """Display formatted search results from PassengerSearchService.

    Args:
        result: OperationResult from a search operation.
    """
    print(f"\n  {result.message}")
    if result.success and result.data:
        for record in result.data:
            pnr = record.get("pnr", "N/A")
            name = record.get("name", "N/A")
            flight = record.get("flight", "N/A")
            print(f"    PNR: {pnr} | Name: {name} | Flight: {flight}")


def run_emergency_route_planner(service: EmergencyRoutePlannerService) -> None:
    """Run the Emergency Route Planner subsystem loop.

    Handles closing/reopening airports and finding alternative routes.
    """
    while True:
        print(display_emergency_route_menu())
        choice = get_int_input("Enter choice: ", 0, 3)

        if choice == 0:
            break
        elif choice == 1:
            # Close Airport
            iata = get_iata_input("Enter IATA code of airport to close: ")
            result = service.close_airport(iata)
            print(f"\n  {result.message}")
        elif choice == 2:
            # Reopen Airport
            iata = get_iata_input("Enter IATA code of airport to reopen: ")
            result = service.reopen_airport(iata)
            print(f"\n  {result.message}")
        elif choice == 3:
            # Find Alternative Routes
            src = get_iata_input("Enter source IATA code: ")
            dest = get_iata_input("Enter destination IATA code: ")
            result = service.find_alternatives(src, dest)
            print(f"\n  {result.message}")


def main():
    """Application entry point - instantiate services and run main loop.

    Creates all service instances with their data structure dependencies,
    then enters the main menu loop dispatching to subsystem runners based
    on user selection.
    """
    # Instantiate all services
    flight_network = FlightNetworkService()
    passenger_priority = PassengerPriorityService()
    boarding_gate = BoardingGateService()
    cargo_management = CargoManagementService()
    flight_price = FlightPriceService()
    passenger_registry = PassengerRegistryService()
    analytics = AnalyticsService()
    passenger_search = PassengerSearchService(passenger_registry)
    emergency_planner = EmergencyRoutePlannerService(flight_network.graph)

    print("\n  Welcome to SkyNet - Global Aviation Logistics System")
    print("  =====================================================\n")

    # Main application loop
    while True:
        try:
            print(display_main_menu())
            choice = get_int_input("Enter choice: ", 0, 9)

            if choice == 0:
                print("\n  Thank you for using SkyNet. Goodbye!")
                break
            elif choice == 1:
                run_flight_network(flight_network)
            elif choice == 2:
                run_passenger_priority(passenger_priority)
            elif choice == 3:
                run_boarding_gate(boarding_gate)
            elif choice == 4:
                run_cargo_management(cargo_management)
            elif choice == 5:
                run_flight_price(flight_price)
            elif choice == 6:
                run_passenger_registry(passenger_registry)
            elif choice == 7:
                run_analytics(analytics)
            elif choice == 8:
                run_passenger_search(passenger_search)
            elif choice == 9:
                run_emergency_route_planner(emergency_planner)

        except KeyboardInterrupt:
            print("\n\n  Operation cancelled. Returning to main menu...")
            continue
        except Exception as e:
            print(f"\n  An unexpected error occurred: {e}")
            print("  Returning to main menu...")
            continue


if __name__ == "__main__":
    main()
