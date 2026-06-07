"""Menu display functions for SkyNet console application.

Provides formatted menu strings for the main menu and all nine
subsystem menus. Each menu displays numbered options with a return
or exit option.
"""


def display_main_menu() -> str:
    """Return main menu string with numbered options 1-9 plus 0 for exit."""
    return """
╔══════════════════════════════════════════════════╗
║   SkyNet - Global Aviation Logistics System      ║
╠══════════════════════════════════════════════════╣
║  1. Flight Network System                        ║
║  2. Passenger Priority System                    ║
║  3. Boarding Gate System                         ║
║  4. Cargo Management System                      ║
║  5. Flight Price Database                        ║
║  6. Passenger Registry                           ║
║  7. Analytics System                             ║
║  8. Passenger Search                             ║
║  9. Emergency Route Planner                      ║
║  0. Exit                                         ║
╚══════════════════════════════════════════════════╝
"""


def display_flight_network_menu() -> str:
    """Return the Flight Network System submenu."""
    return """
╔══════════════════════════════════════════════════╗
║         Flight Network System                    ║
╠══════════════════════════════════════════════════╣
║  1. Add Airport                                  ║
║  2. Remove Airport                               ║
║  3. Add Route                                    ║
║  4. Remove Route                                 ║
║  5. Find Shortest Path (Dijkstra)                ║
║  6. Compute MST (Prim's)                         ║
║  7. Compute MST (Kruskal's)                      ║
║  8. Display Network                              ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_passenger_priority_menu() -> str:
    """Return the Passenger Priority System submenu."""
    return """
╔══════════════════════════════════════════════════╗
║       Passenger Priority System                  ║
╠══════════════════════════════════════════════════╣
║  1. Add Passenger                                ║
║  2. Process Next Passenger                       ║
║  3. Peek Next Passenger                          ║
║  4. Display Priority Queue                       ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_boarding_gate_menu() -> str:
    """Return the Boarding Gate System submenu."""
    return """
╔══════════════════════════════════════════════════╗
║         Boarding Gate System                     ║
╠══════════════════════════════════════════════════╣
║  1. Add Passenger to Queue                       ║
║  2. Board Next Passenger                         ║
║  3. Display Boarding Queue                       ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_cargo_management_menu() -> str:
    """Return the Cargo Management System submenu."""
    return """
╔══════════════════════════════════════════════════╗
║        Cargo Management System                   ║
╠══════════════════════════════════════════════════╣
║  1. Load Cargo                                   ║
║  2. Unload Cargo                                 ║
║  3. Peek Top Cargo                               ║
║  4. Display Cargo Stack                          ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_flight_price_menu() -> str:
    """Return the Flight Price Database submenu."""
    return """
╔══════════════════════════════════════════════════╗
║         Flight Price Database                    ║
╠══════════════════════════════════════════════════╣
║  1. Add Price Record                             ║
║  2. Remove Price Record                          ║
║  3. Search by Price                              ║
║  4. Range Search                                 ║
║  5. Display All Prices                           ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_passenger_registry_menu() -> str:
    """Return the Passenger Registry submenu."""
    return """
╔══════════════════════════════════════════════════╗
║          Passenger Registry                      ║
╠══════════════════════════════════════════════════╣
║  1. Create Record                                ║
║  2. Search Record                                ║
║  3. Update Record                                ║
║  4. Delete Record                                ║
║  5. Display Registry                             ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_analytics_menu() -> str:
    """Return the Analytics System submenu."""
    return """
╔══════════════════════════════════════════════════╗
║           Analytics System                       ║
╠══════════════════════════════════════════════════╣
║  1. Sort with QuickSort                          ║
║  2. Sort with MergeSort                          ║
║  3. Comparison Report                            ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_passenger_search_menu() -> str:
    """Return the Passenger Search submenu."""
    return """
╔══════════════════════════════════════════════════╗
║          Passenger Search (KMP)                  ║
╠══════════════════════════════════════════════════╣
║  1. Search by Name                               ║
║  2. Search by PNR                                ║
║  3. Search by Flight Number                      ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""


def display_emergency_route_menu() -> str:
    """Return the Emergency Route Planner submenu."""
    return """
╔══════════════════════════════════════════════════╗
║       Emergency Route Planner                    ║
╠══════════════════════════════════════════════════╣
║  1. Close Airport                                ║
║  2. Reopen Airport                               ║
║  3. Find Alternative Routes                      ║
║  0. Return to Main Menu                          ║
╚══════════════════════════════════════════════════╝
"""
