"""Menu-driven console interface wiring services to user input.

The console owns the shared application state (one Graph, MaxHeap, Queue,
Stack, AVLTree, HashTable) and the service instances. Every dispatch is wrapped
in a try/except so an unexpected error prints a recovery message and returns to
the menu rather than terminating the application (Req 15.4).
"""

from data_structures.fifo_queue import Queue
from data_structures.graph import Graph
from data_structures.hash_table import HashTable
from data_structures.lifo_stack import Stack
from data_structures.max_heap import MaxHeap
from data_structures.price_tree import AVLTree
from models.flight_record import FlightRecord
from models.passenger import Passenger, PassengerProfile
from models.ticket_status import TicketStatus
from services.boarding_service import BoardingService
from services.cargo_service import CargoService
from services.checkin_service import CheckInService
from services.contingency_service import ContingencyService
from services.manifest_search_service import ManifestSearchService
from services.pricing_service import PricingService
from services.results import OperationResult
from services.route_planning_service import RoutePlanningService
from services.sort_comparison_service import SortComparisonService


class ConsoleMenu:
    """Interactive text menu for all five SkyNet phases."""

    def __init__(self, input_fn=input, output_fn=print) -> None:
        self._input = input_fn
        self._output = output_fn

        # Shared application state (encapsulated structures).
        self.__graph = Graph()
        self.__priority_queue = MaxHeap(priority_of=lambda p: int(p.status))
        self.__boarding_queue = Queue()
        self.__cargo_stack = Stack()
        self.__price_tree = AVLTree()
        self.__passenger_table = HashTable()

        # Services.
        self.__routes = RoutePlanningService(self.__graph)
        self.__checkin = CheckInService(self.__priority_queue, self.__passenger_table)
        self.__boarding = BoardingService(self.__boarding_queue)
        self.__cargo = CargoService(self.__cargo_stack)
        self.__pricing = PricingService(self.__price_tree)
        self.__manifest = ManifestSearchService()
        self.__contingency = ContingencyService(self.__graph)
        self.__sorting = SortComparisonService()

        self.__handlers = {
            "1": self._add_airport,
            "2": self._add_route,
            "3": self._display_network,
            "4": self._find_cheapest_route,
            "5": self._backup_network,
            "6": self._checkin_enqueue,
            "7": self._checkin_serve,
            "8": self._board_passenger,
            "9": self._board_next,
            "10": self._cargo_load,
            "11": self._cargo_unload,
            "12": self._register_passenger,
            "13": self._lookup_passenger,
            "14": self._delete_passenger,
            "15": self._insert_price,
            "16": self._range_search,
            "17": self._sort_compare,
            "18": self._manifest_search,
            "19": self._contingency_paths,
            "20": self._load_demo_data,
        }

    # ----- main loop ----------------------------------------------------
    def run(self) -> None:
        self._output("=" * 60)
        self._output(" SkyNet Global Aviation Logistics & Management System")
        self._output("=" * 60)
        while True:
            self._print_menu()
            try:
                choice = self._input("Select an option: ").strip()
            except (EOFError, KeyboardInterrupt):
                self._output("\nExiting SkyNet. Safe travels.")
                return
            if choice in ("0", "q", "Q"):
                self._output("Exiting SkyNet. Safe travels.")
                return
            handler = self.__handlers.get(choice)
            if handler is None:
                self._output("Invalid selection. Please choose a listed option.")
                continue
            try:
                handler()
            except Exception as exc:  # defence in depth (Req 15.4)
                self._output(f"Unexpected error: {exc}. Returning to menu.")

    def _print_menu(self) -> None:
        self._output(
            "\n--- Menu ---\n"
            "Phase 1 - Network:   1) Add airport  2) Add route  3) Display network\n"
            "                     4) Cheapest route  5) Backup network (MST)\n"
            "Phase 2 - Flow:      6) Check-in enqueue  7) Serve next check-in\n"
            "                     8) Board passenger  9) Board next\n"
            "                     10) Load cargo  11) Unload cargo\n"
            "Phase 3 - Records:   12) Register PNR  13) Lookup PNR  14) Delete PNR\n"
            "                     15) Insert price  16) Price range search\n"
            "Phase 4 - Analytics: 17) Sort & compare schedules  18) Manifest name search\n"
            "Phase 5 - Recovery:  19) Alternative paths (hub down)\n"
            "Utility:             20) Load demo data   0) Exit"
        )

    # ----- rendering ----------------------------------------------------
    def _render(self, result: OperationResult) -> None:
        prefix = "[OK] " if result.ok else "[ERROR] "
        message = result.message
        if result.ok and not message and result.payload is not None:
            message = str(result.payload)
        self._output(prefix + message)

    def _prompt(self, label: str) -> str:
        return self._input(label).strip()

    # ----- Phase 1 handlers --------------------------------------------
    def _add_airport(self) -> None:
        code = self._prompt("Airport code: ")
        self._render(self.__routes.add_airport(code))

    def _add_route(self) -> None:
        src = self._prompt("Source code: ")
        dst = self._prompt("Destination code: ")
        weight = self._prompt("Cost/weight: ")
        self._render(self.__routes.add_route(src, dst, weight))

    def _display_network(self) -> None:
        self._render(self.__routes.display_network())

    def _find_cheapest_route(self) -> None:
        src = self._prompt("From: ")
        dst = self._prompt("To: ")
        self._render(self.__routes.find_cheapest_route(src, dst))

    def _backup_network(self) -> None:
        algo = self._prompt("Algorithm (prim/kruskal) [prim]: ") or "prim"
        self._render(self.__routes.generate_backup_network(algo))

    # ----- Phase 2 handlers --------------------------------------------
    def _read_passenger(self) -> Passenger:
        pnr = self._prompt("PNR (6 alphanumeric): ")
        name = self._prompt("Name: ")
        status_raw = self._prompt("Status (Platinum/Gold/Silver/Economy): ")
        status = TicketStatus.from_name(status_raw)
        return Passenger(pnr=pnr, name=name, status=status)

    def _checkin_enqueue(self) -> None:
        try:
            passenger = self._read_passenger()
        except ValueError as exc:
            self._output(f"[ERROR] {exc}")
            return
        self._render(self.__checkin.enqueue_passenger(passenger))

    def _checkin_serve(self) -> None:
        self._render(self.__checkin.serve_next())

    def _board_passenger(self) -> None:
        name = self._prompt("Passenger name: ")
        self._render(self.__boarding.board_passenger(name))

    def _board_next(self) -> None:
        self._render(self.__boarding.call_next())

    def _cargo_load(self) -> None:
        item = self._prompt("Cargo item: ")
        self._render(self.__cargo.load_item(item))

    def _cargo_unload(self) -> None:
        self._render(self.__cargo.unload_item())

    # ----- Phase 3 handlers --------------------------------------------
    def _register_passenger(self) -> None:
        pnr = self._prompt("PNR (6 alphanumeric): ")
        name = self._prompt("Name: ")
        status_raw = self._prompt("Status [Economy]: ") or "Economy"
        try:
            status = TicketStatus.from_name(status_raw)
            passenger = Passenger(pnr=pnr, name=name, status=status,
                                  profile=PassengerProfile())
        except ValueError as exc:
            # Surface PNR/name validation via the service for a uniform message.
            from services.results import ErrorCode
            if not Passenger.is_valid_pnr(pnr):
                self._render(OperationResult.failure(ErrorCode.INVALID_PNR, pnr=pnr))
            else:
                self._output(f"[ERROR] {exc}")
            return
        self._render(self.__checkin.register_passenger(passenger))

    def _lookup_passenger(self) -> None:
        pnr = self._prompt("PNR: ")
        self._render(self.__checkin.lookup(pnr))

    def _delete_passenger(self) -> None:
        pnr = self._prompt("PNR: ")
        self._render(self.__checkin.delete(pnr))

    def _insert_price(self) -> None:
        price = self._prompt("Flight price: ")
        try:
            value = float(price)
        except ValueError:
            self._output("[ERROR] Price must be numeric.")
            return
        self._render(self.__pricing.insert_price(value))

    def _range_search(self) -> None:
        low = self._prompt("Lower bound: ")
        high = self._prompt("Upper bound: ")
        try:
            low_v, high_v = float(low), float(high)
        except ValueError:
            self._output("[ERROR] Bounds must be numeric.")
            return
        self._render(self.__pricing.range_search(low_v, high_v))

    # ----- Phase 4 handlers --------------------------------------------
    def _sort_compare(self) -> None:
        schedule = self.__demo_schedule()
        key = self._prompt("Sort key (departure_time/fuel_efficiency) "
                            "[departure_time]: ") or "departure_time"
        self._render(self.__sorting.compare(schedule, key))

    def _manifest_search(self) -> None:
        manifest = self._prompt("Manifest text: ")
        pattern = self._prompt("Name to find: ")
        self._render(self.__manifest.search(manifest, pattern))

    # ----- Phase 5 handlers --------------------------------------------
    def _contingency_paths(self) -> None:
        src = self._prompt("From: ")
        dst = self._prompt("To: ")
        hub = self._prompt("Unavailable hub (blank for none): ") or None
        self._render(self.__contingency.enumerate_paths(src, dst, hub))

    # ----- demo data ----------------------------------------------------
    def _load_demo_data(self) -> None:
        for code in ("LHR", "JFK", "DXB", "SIN", "FRA"):
            self.__routes.add_airport(code)
        for a, b, w in (
            ("LHR", "JFK", 450),
            ("LHR", "FRA", 120),
            ("FRA", "DXB", 380),
            ("DXB", "SIN", 410),
            ("JFK", "DXB", 700),
            ("FRA", "SIN", 900),
        ):
            self.__routes.add_route(a, b, w)
        for price in (199.0, 450.0, 320.0, 99.0, 780.0):
            self.__pricing.insert_price(price)
        self._output("[OK] Demo network, routes, and prices loaded.")

    @staticmethod
    def __demo_schedule():
        return [
            FlightRecord("SK101", 600, 0.82, "LHR", "JFK"),
            FlightRecord("SK205", 420, 0.91, "FRA", "DXB"),
            FlightRecord("SK330", 1080, 0.75, "DXB", "SIN"),
            FlightRecord("SK044", 90, 0.88, "SIN", "LHR"),
            FlightRecord("SK512", 720, 0.79, "JFK", "FRA"),
        ]
