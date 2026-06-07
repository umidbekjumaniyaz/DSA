"""Console UI layer for menu-driven interaction."""

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

__all__ = [
    "display_main_menu",
    "display_flight_network_menu",
    "display_passenger_priority_menu",
    "display_boarding_gate_menu",
    "display_cargo_management_menu",
    "display_flight_price_menu",
    "display_passenger_registry_menu",
    "display_analytics_menu",
    "display_passenger_search_menu",
    "display_emergency_route_menu",
    "get_int_input",
    "get_float_input",
    "get_string_input",
    "get_iata_input",
    "get_priority_input",
]
