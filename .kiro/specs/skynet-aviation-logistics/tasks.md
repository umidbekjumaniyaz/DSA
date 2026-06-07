# Implementation Plan: SkyNet - Global Aviation Logistics & Management System

## Overview

This plan implements SkyNet as a modular Python 3.11 console application with nine interconnected aviation logistics subsystems. Each module is built incrementally: project scaffolding first, then data structures with tests, service layer, UI layer, integration tests, documentation generation, and final packaging. All data structures are implemented from scratch using pure Python with no external data structure libraries. Testing uses pytest with Hypothesis for property-based tests.

## Tasks

- [x] 1. Project scaffolding and foundation
  - [x] 1.1 Create project directory structure and package init files
    - Create the full `skynet/` package structure with all subpackages: `models/`, `graph/`, `heap/`, `queue/`, `stack/`, `tree/`, `hashing/`, `sorting/`, `string_matching/`, `backtracking/`, `services/`, `utils/`, `ui/`
    - Create `tests/` directory structure with `conftest.py`, `property_tests/`, `unit_tests/`, `integration_tests/`
    - Create `docs/` directory with `templates/` and `output/` subdirectories
    - Add `__init__.py` to all packages
    - Create `pyproject.toml` with pytest and hypothesis as dev dependencies
    - _Requirements: 12.5_

  - [x] 1.2 Implement domain models
    - Create `skynet/models/airport.py` with `Airport` dataclass and IATA code validation
    - Create `skynet/models/flight.py` with `Flight` dataclass and distance validation
    - Create `skynet/models/passenger.py` with `Passenger` dataclass, `PriorityLevel` enum, and PNR validation
    - Create `skynet/models/cargo.py` with `Cargo` dataclass
    - Create `skynet/models/price_record.py` with `PriceRecord` dataclass
    - Create `skynet/models/__init__.py` exporting all models
    - Create `Path` dataclass in appropriate location
    - _Requirements: 1.1, 4.1, 6.1, 7.1, 8.1_

  - [x] 1.3 Implement abstract base classes and shared result types
    - Create `skynet/models/operation_result.py` with `OperationResult` dataclass
    - Create `DataStructureBase` abstract class in `skynet/models/base.py` with abstract methods: `insert`, `delete`, `search`, `display`, `is_empty`, `size`
    - Create `MSTAlgorithm` abstract class in `skynet/graph/mst_base.py` with `compute_mst` and `get_name`
    - Create `SortAlgorithm` abstract class in `skynet/sorting/sort_base.py` with `sort`, `get_name`, `get_complexity` and related dataclasses (`ComplexityInfo`, `SortResult`)
    - Create `MSTResult` dataclass
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [x] 1.4 Implement utility modules
    - Create `skynet/utils/validators.py` with input validation functions (IATA code, PNR format, priority level, numeric range)
    - Create `skynet/utils/formatters.py` with output formatting helpers (table display, path display, tree display)
    - Create `skynet/utils/performance.py` with timing decorator and memory measurement utilities
    - _Requirements: 15.6_

- [x] 2. Graph module implementation
  - [x] 2.1 Implement WeightedGraph with adjacency list
    - Create `skynet/graph/weighted_graph.py` implementing adjacency list storage with `Dict[str, List[Tuple[str, int]]]`
    - Implement `add_node`, `remove_node`, `add_edge`, `remove_edge`, `get_neighbors`, `get_all_nodes`, `get_all_edges`, `has_node`, `has_edge`, `node_count`, `edge_count`, `display`
    - Bidirectional edges: adding edge (A, B, w) adds B to A's list and A to B's list
    - Node deletion cascades to all edges involving that node
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10_

  - [x] 2.2 Implement Dijkstra's shortest path algorithm
    - Create `skynet/graph/dijkstra.py` with `DijkstraSolver` class
    - Implement using a min-heap priority queue (Python `heapq` for internal algorithmic use only — this is infrastructure, not the assessed heap)
    - Handle: source equals destination (return 0), no path exists, invalid nodes
    - Return `OperationResult` with path list and total distance
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 2.3 Implement Union-Find data structure
    - Create `skynet/graph/union_find.py` with `UnionFind` class
    - Implement `make_set`, `find` with path compression, `union` with union by rank
    - _Requirements: 3.2_

  - [x] 2.4 Implement Prim's MST algorithm
    - Create `skynet/graph/prim.py` with `PrimMST` class extending `MSTAlgorithm`
    - Use min-heap to select minimum-weight edges
    - Handle disconnected graph detection and report components
    - Handle graph with fewer than 2 nodes
    - _Requirements: 3.1, 3.3, 3.4, 3.5, 3.6_

  - [x] 2.5 Implement Kruskal's MST algorithm
    - Create `skynet/graph/kruskal.py` with `KruskalMST` class extending `MSTAlgorithm`
    - Sort edges by weight, use Union-Find to detect cycles
    - Handle disconnected graph detection and report components
    - Handle graph with fewer than 2 nodes
    - _Requirements: 3.2, 3.3, 3.4, 3.6_

  - [x] 2.6 Write unit tests for graph module
    - Create `tests/unit_tests/test_graph.py`
    - Test normal operations: add/remove nodes, add/remove edges, display adjacency list
    - Test edge cases: empty graph, single node, self-referencing path query
    - Test error conditions: duplicate node, non-existent node, invalid IATA format
    - Test Dijkstra: correct shortest path, no path, same source/destination
    - Test Prim's: correct MST on connected graph, disconnected detection, insufficient nodes
    - Test Kruskal's: correct MST on connected graph, disconnected detection, cost equals Prim's
    - Test Union-Find: make_set, find with path compression, union by rank
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.10, 13.12, 13.13_

  - [ ]* 2.7 Write property tests for graph module
    - **Property 1: Graph Node Addition Idempotence** — adding a node twice leaves graph size unchanged after second attempt
    - **Validates: Requirements 1.1, 1.2**
    - **Property 2: Graph Edge Bidirectionality** — adding an edge makes both endpoints appear in each other's neighbor list
    - **Validates: Requirements 1.3**
    - **Property 3: Node Deletion Cascades to Edges** — deleting a node removes it from all adjacency lists
    - **Validates: Requirements 1.5**
    - **Property 4: Edge Deletion Preserves Nodes** — removing an edge keeps both nodes in the graph
    - **Validates: Requirements 1.7**
    - **Property 5: Dijkstra's Shortest Path Correctness** — returned path weight ≤ all other valid paths
    - **Validates: Requirements 2.1**
    - **Property 6: MST Algorithm Confluence** — Prim's total cost equals Kruskal's total cost
    - **Validates: Requirements 3.4**
    - **Property 7: MST Structural Validity** — MST has exactly V-1 edges connecting all V nodes
    - **Validates: Requirements 3.1, 3.2**

- [x] 3. Heap module implementation
  - [x] 3.1 Implement MaxHeap with stable priority ordering
    - Create `skynet/heap/max_heap.py` with `MaxHeap` class extending `DataStructureBase`
    - Store elements as `(priority_value, -sequence_number, item)` tuples for stable FIFO within same priority
    - Implement `insert`, `extract_max`, `peek`, `delete`, `search`, `is_empty`, `size`, `display`
    - Implement `_sift_up` and `_sift_down` for heap maintenance
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [x] 3.2 Write unit tests for heap module
    - Create `tests/unit_tests/test_heap.py`
    - Test normal: insert passengers, extract in priority order
    - Test edge cases: empty heap extract, single element, equal priorities (FIFO)
    - Test error conditions: invalid priority level
    - _Requirements: 13.9, 13.12, 13.13_

  - [ ]* 3.3 Write property tests for heap module
    - **Property 8: Heap Extraction Priority Ordering** — successive extracts return non-increasing priority with FIFO among equal
    - **Validates: Requirements 4.1, 4.2, 4.3**
    - **Property 9: Heap Peek Idempotence** — peek returns same value as extract_max without changing size
    - **Validates: Requirements 4.4**
    - **Property 10: Heap Structural Invariant** — after every operation, all parents ≥ children
    - **Validates: Requirements 4.6**

- [x] 4. Queue module implementation
  - [x] 4.1 Implement FIFOQueue with linked list
    - Create `skynet/queue/fifo_queue.py` with `FIFOQueue` class extending `DataStructureBase`
    - Implement using singly linked list with head and tail pointers
    - Implement `enqueue`, `dequeue`, `peek`, `contains`, `is_empty`, `size`, `display`
    - Track member identifiers in a set to prevent duplicates
    - Implement `insert`, `delete`, `search` abstract method overrides mapping to queue semantics
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [x] 4.2 Write unit tests for queue module
    - Create `tests/unit_tests/test_queue.py`
    - Test normal: enqueue multiple, dequeue in order, display
    - Test edge cases: empty queue dequeue, single element
    - Test error conditions: duplicate passenger enqueue
    - _Requirements: 13.5, 13.12, 13.13_

  - [ ]* 4.3 Write property tests for queue module
    - **Property 11: Queue FIFO Ordering** — dequeue order matches enqueue order exactly
    - **Validates: Requirements 5.1, 5.2, 5.5**
    - **Property 12: Queue Duplicate Rejection** — enqueuing existing identifier fails, size unchanged
    - **Validates: Requirements 5.7**

- [x] 5. Stack module implementation
  - [x] 5.1 Implement LIFOStack
    - Create `skynet/stack/lifo_stack.py` with `LIFOStack` class extending `DataStructureBase`
    - Implement using Python list as internal storage
    - Implement `push`, `pop`, `peek`, `is_empty`, `size`, `display`
    - Implement `insert`, `delete`, `search` abstract method overrides mapping to stack semantics
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

  - [x] 5.2 Write unit tests for stack module
    - Create `tests/unit_tests/test_stack.py`
    - Test normal: push items, pop in LIFO order, peek top
    - Test edge cases: empty stack pop, empty stack peek, single item
    - Test error conditions: pop from empty returns proper error
    - _Requirements: 13.6, 13.12, 13.13_

  - [ ]* 5.3 Write property tests for stack module
    - **Property 13: Stack LIFO Ordering** — popping all items returns them in reverse push order
    - **Validates: Requirements 6.1, 6.2, 6.8**
    - **Property 14: Stack Peek Non-Destructive** — peek returns same as pop would, without changing size
    - **Validates: Requirements 6.6**

- [x] 6. Tree module implementation
  - [x] 6.1 Implement AVL Tree with rotations
    - Create `skynet/tree/avl_node.py` with `AVLNode` class (key, records list, left, right, height)
    - Create `skynet/tree/avl_tree.py` with `AVLTree` class extending `DataStructureBase`
    - Implement `_rotate_left`, `_rotate_right`, `_get_balance`, `_get_height`, `_rebalance`
    - Handle all four rotation cases: LL, LR, RR, RL
    - Implement `insert` (keyed by price, stores multiple records at same key)
    - Implement `delete` with rebalancing
    - Implement `search` (O(log n) lookup by price)
    - Implement `range_search` (returns all records with price in [min, max])
    - Implement `in_order_traversal` returning sorted records
    - Implement `display` with visual tree representation
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8_

  - [x] 6.2 Write unit tests for tree module
    - Create `tests/unit_tests/test_avl.py`
    - Test normal: insert records, search by price, range search, in-order traversal sorted
    - Test edge cases: empty tree search, single node tree, duplicate price keys
    - Test error conditions: delete non-existent price, range with no results
    - Test rotations: verify LL, LR, RR, RL cases produce balanced tree
    - _Requirements: 13.12, 13.13_

  - [ ]* 6.3 Write property tests for tree module
    - **Property 15: AVL Balance Invariant** — after any sequence of operations, all nodes have balance factor in {-1, 0, 1}
    - **Validates: Requirements 7.1, 7.2, 7.8**
    - **Property 16: AVL In-Order Traversal Produces Sorted Output** — traversal yields non-decreasing prices
    - **Validates: Requirements 7.6**
    - **Property 17: AVL Range Search Completeness and Soundness** — range search returns exactly the correct subset
    - **Validates: Requirements 7.5**

- [x] 7. Hashing module implementation
  - [x] 7.1 Implement HashTable with separate chaining
    - Create `skynet/hashing/hash_table.py` with `HashTable` class extending `DataStructureBase`
    - Implement polynomial rolling hash function (prime=31)
    - Use list of lists (buckets) for separate chaining collision resolution
    - Implement `insert`, `delete`, `search`, `update`, `is_empty`, `size`, `display`
    - Display shows bucket indices and chained entries
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9_

  - [x] 7.2 Write unit tests for hashing module
    - Create `tests/unit_tests/test_hash_table.py`
    - Test normal: insert, search, update, delete records by PNR
    - Test edge cases: collision handling (multiple keys to same bucket), single entry
    - Test error conditions: duplicate PNR, non-existent PNR search/update/delete, invalid PNR format
    - _Requirements: 13.7, 13.8, 13.12, 13.13_

  - [ ]* 7.3 Write property tests for hashing module
    - **Property 18: Hash Table Insert-Lookup Round Trip** — insert then search returns stored record
    - **Validates: Requirements 8.1, 8.2, 8.7**
    - **Property 19: Hash Table Delete Then Search Fails** — delete then search returns not found
    - **Validates: Requirements 8.4**
    - **Property 20: Hash Table Duplicate PNR Rejection** — inserting duplicate PNR fails, existing record unchanged
    - **Validates: Requirements 8.5**

- [x] 8. Sorting module implementation
  - [x] 8.1 Implement QuickSort with last-element pivot
    - Create `skynet/sorting/quicksort.py` with `QuickSort` class extending `SortAlgorithm`
    - Implement in-place partitioning with last element as pivot
    - Track comparisons count during sort
    - Measure execution time and memory usage via `SortResult`
    - Provide `get_name` and `get_complexity` (best O(n log n), avg O(n log n), worst O(n²), space O(log n))
    - _Requirements: 9.1, 9.3, 9.4, 9.7, 9.8, 9.9_

  - [x] 8.2 Implement MergeSort with divide-and-conquer
    - Create `skynet/sorting/mergesort.py` with `MergeSort` class extending `SortAlgorithm`
    - Implement recursive divide-and-conquer with merge step
    - Track comparisons count during sort
    - Measure execution time and memory usage via `SortResult`
    - Provide `get_name` and `get_complexity` (best O(n log n), avg O(n log n), worst O(n log n), space O(n))
    - _Requirements: 9.2, 9.3, 9.4, 9.7, 9.8, 9.9_

  - [x] 8.3 Write unit tests for sorting module
    - Create `tests/unit_tests/test_sorting.py`
    - Test normal: sort numeric list correctly with both algorithms
    - Test edge cases: empty list, single element, already sorted, reverse sorted
    - Test error conditions: verify both produce identical output on same input
    - Test performance metrics: verify SortResult fields are populated
    - _Requirements: 9.5, 9.6, 13.12, 13.13_

  - [ ]* 8.4 Write property tests for sorting module
    - **Property 21: Sorting Correctness** — output is sorted (element[i] ≤ element[i+1])
    - **Validates: Requirements 9.1, 9.2, 9.6**
    - **Property 22: Sorting Algorithms Produce Identical Output** — QuickSort output == MergeSort output
    - **Validates: Requirements 9.5**
    - **Property 23: Sorting Preserves Elements** — output is a permutation of input
    - **Validates: Requirements 9.1, 9.2**

- [x] 9. String matching module implementation
  - [x] 9.1 Implement KMP algorithm
    - Create `skynet/string_matching/kmp.py` with `KMPMatcher` class
    - Implement `compute_failure_function` returning failure array
    - Implement `search(text, pattern)` returning list of match start indices
    - Support case-insensitive matching
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.6_

  - [x] 9.2 Write unit tests for KMP module
    - Create `tests/unit_tests/test_kmp.py`
    - Test normal: pattern found at correct positions, multiple matches
    - Test edge cases: pattern equals text, pattern at start/end, single character pattern
    - Test error conditions: no match found, empty/whitespace pattern validation
    - Test failure function: known patterns with expected failure arrays
    - _Requirements: 10.5, 10.7, 13.12, 13.13_

  - [ ]* 9.3 Write property tests for KMP module
    - **Property 24: KMP Search Matches Model** — KMP results identical to naive brute-force search
    - **Validates: Requirements 10.2, 10.3, 10.4**
    - **Property 25: KMP Failure Function Correctness** — failure[i] equals longest proper prefix-suffix length
    - **Validates: Requirements 10.1**

- [x] 10. Backtracking module implementation
  - [x] 10.1 Implement recursive route finder
    - Create `skynet/backtracking/route_finder.py` with `BacktrackingSolver` class
    - Implement `find_all_paths(graph, source, destination, excluded)` using recursive backtracking
    - Track visited nodes to prevent cycles
    - Exclude closed airports from traversal
    - Return list of `Path` objects with legs and total distances
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

  - [x] 10.2 Write unit tests for backtracking module
    - Create `tests/unit_tests/test_backtracking.py`
    - Test normal: find all paths between two nodes, correct path count
    - Test edge cases: direct route only, no path exists, closed airport excludes paths
    - Test error conditions: invalid source/destination, source/dest is closed airport
    - _Requirements: 11.7, 11.8, 13.12, 13.13_

  - [ ]* 10.3 Write property tests for backtracking module
    - **Property 26: Backtracking Paths Exclude Closed Nodes** — no path contains a closed airport
    - **Validates: Requirements 11.2**
    - **Property 27: Backtracking Paths Are Acyclic** — all nodes in any path are unique
    - **Validates: Requirements 11.6**
    - **Property 28: Backtracking Paths Are Valid** — consecutive nodes have corresponding graph edge
    - **Validates: Requirements 11.2, 11.3**
    - **Property 29: Backtracking Shortest Label Correctness** — labeled shortest has ≤ distance of all others
    - **Validates: Requirements 11.4**
    - **Property 30: Backtracking Distance Consistency** — total distance = sum of leg distances
    - **Validates: Requirements 11.3**

- [x] 11. Checkpoint - Data structures complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Service layer implementation
  - [x] 12.1 Implement FlightNetworkService
    - Create `skynet/services/flight_network_service.py`
    - Compose `WeightedGraph`, `DijkstraSolver`, `PrimMST`, `KruskalMST`
    - Implement: `add_airport`, `remove_airport`, `add_route`, `remove_route`, `shortest_path`, `compute_mst_prim`, `compute_mst_kruskal`, `display_network`
    - Validate IATA codes and distances at service boundary
    - _Requirements: 1.1–1.10, 2.1–2.5, 3.1–3.6_

  - [x] 12.2 Implement PassengerPriorityService
    - Create `skynet/services/passenger_priority_service.py`
    - Compose `MaxHeap` for priority queue management
    - Implement: `add_passenger`, `process_next`, `peek_next`, `display_queue`
    - Validate priority level at service boundary
    - _Requirements: 4.1–4.7_

  - [x] 12.3 Implement BoardingGateService
    - Create `skynet/services/boarding_gate_service.py`
    - Compose `FIFOQueue` for boarding order
    - Implement: `add_to_boarding`, `board_next`, `display_queue`
    - _Requirements: 5.1–5.7_

  - [x] 12.4 Implement CargoManagementService
    - Create `skynet/services/cargo_management_service.py`
    - Compose `LIFOStack` for cargo operations
    - Implement: `load_cargo`, `unload_cargo`, `peek_top`, `display_stack`
    - _Requirements: 6.1–6.8_

  - [x] 12.5 Implement FlightPriceService
    - Create `skynet/services/flight_price_service.py`
    - Compose `AVLTree` for price storage and queries
    - Implement: `add_price`, `remove_price`, `search_price`, `range_search`, `display_prices`
    - _Requirements: 7.1–7.8_

  - [x] 12.6 Implement PassengerRegistryService
    - Create `skynet/services/passenger_registry_service.py`
    - Compose `HashTable` for record storage
    - Implement: `create_record`, `search_record`, `update_record`, `delete_record`, `display_registry`
    - Validate PNR format at service boundary
    - _Requirements: 8.1–8.9_

  - [x] 12.7 Implement AnalyticsService
    - Create `skynet/services/analytics_service.py`
    - Compose `QuickSort` and `MergeSort` algorithm instances
    - Implement: `sort_with_quicksort`, `sort_with_mergesort`, `comparison_report`
    - Generate formatted performance comparison report
    - _Requirements: 9.1–9.9_

  - [x] 12.8 Implement PassengerSearchService
    - Create `skynet/services/passenger_search_service.py`
    - Compose `KMPMatcher` and reference `PassengerRegistryService`
    - Implement: `search_by_name`, `search_by_pnr`, `search_by_flight`
    - Validate pattern is non-empty/non-whitespace
    - _Requirements: 10.1–10.7_

  - [x] 12.9 Implement EmergencyRoutePlannerService
    - Create `skynet/services/emergency_route_planner_service.py`
    - Compose `BacktrackingSolver` and reference `WeightedGraph`
    - Implement: `close_airport`, `reopen_airport`, `find_alternatives`
    - Track closed airports, validate IATA codes, mark shortest alternative
    - _Requirements: 11.1–11.8_

- [x] 13. Checkpoint - Service layer complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 14. UI layer implementation
  - [x] 14.1 Implement menu system and input handler
    - Create `skynet/ui/menu.py` with main menu and 9 subsystem menus
    - Create `skynet/ui/input_handler.py` with input validation (numeric range, IATA format, priority level)
    - Main menu lists all 9 subsystems with numbered options plus exit
    - Each subsystem menu lists its operations with numbered options plus return to main
    - Handle invalid input gracefully with error messages and re-prompt
    - _Requirements: 15.1, 15.2, 15.3, 15.6, 15.7_

  - [x] 14.2 Implement main.py entry point and subsystem wiring
    - Create `skynet/main.py` as the application entry point
    - Instantiate all services with their data structure dependencies
    - Wire menu selections to service method calls
    - Handle operation output display and return to subsystem menu
    - Implement clean exit with confirmation message
    - Exception handling: catch all exceptions at top level, display user-friendly messages
    - _Requirements: 15.1, 15.4, 15.5_

- [x] 15. Integration tests
  - [x] 15.1 Write integration tests for all services
    - Create `tests/integration_tests/test_flight_network_service.py` — end-to-end flight network operations
    - Create `tests/integration_tests/test_passenger_priority_service.py` — full priority queue workflow
    - Create `tests/integration_tests/test_boarding_gate_service.py` — boarding queue workflow
    - Create `tests/integration_tests/test_cargo_management_service.py` — cargo LIFO workflow
    - Create `tests/integration_tests/test_flight_price_service.py` — AVL tree price operations
    - Create `tests/integration_tests/test_passenger_registry_service.py` — CRUD operations via service
    - Create `tests/integration_tests/test_analytics_service.py` — sorting comparison workflow
    - Create `tests/integration_tests/test_passenger_search_service.py` — KMP search through service
    - Create `tests/integration_tests/test_emergency_route_planner_service.py` — backtracking with closures
    - Test cross-service interactions where applicable
    - _Requirements: 13.11, 13.12, 13.13_

- [x] 16. Checkpoint - All tests passing
  - Ensure all tests pass, ask the user if questions arise.

- [x] 17. Documentation generation
  - [x] 17.1 Implement documentation generator
    - Create `docs/generate_docs.py` script that introspects algorithm classes
    - Create `docs/templates/algorithm_template.md` for algorithm explanations
    - Create `docs/templates/complexity_template.md` for complexity analysis
    - Create `docs/templates/flowchart_template.md` for Mermaid flowcharts
    - Generate `docs/output/pass_criteria.md` covering P1-P7 (ADT specifications with pseudocode)
    - Generate `docs/output/merit_criteria.md` covering M1-M5 (step-by-step walkthroughs, complexity)
    - Generate `docs/output/distinction_criteria.md` covering D1-D4 (comparative analysis, empirical data)
    - Generate `docs/output/full_report.md` combining all sections
    - Include Mermaid flowcharts for: Dijkstra's, Prim's, Kruskal's, QuickSort, MergeSort, KMP, AVL rotation, backtracking
    - Collect performance data from test runs at 3 dataset sizes (100, 1000, 10000)
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8_

- [ ] 18. Final testing report and packaging
  - [-] 18.1 Implement test report generator and run full suite
    - Create `tests/test_report_generator.py` that runs full pytest suite and generates report
    - Report includes: total tests, passed, failed, pass rate by subsystem, property test iterations
    - Verify all subsystems have minimum 3 tests (normal, edge case, error)
    - Verify property tests run minimum 100 iterations each
    - Generate final testing report as markdown
    - _Requirements: 13.11, 13.12, 13.13_

  - [-] 18.2 Final packaging and verification
    - Verify all `__init__.py` exports are correct
    - Verify `pyproject.toml` has correct entry point configured
    - Run complete test suite with `pytest --tb=short`
    - Verify documentation generation produces complete output
    - Ensure no external data structure libraries are imported
    - _Requirements: 12.5, 12.6_

- [~] 19. Final checkpoint - Project complete
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Python 3.11 with no external data structure libraries — only pytest and hypothesis for testing
- All data structures built from scratch to demonstrate understanding
- Service layer validates inputs; data structures assume pre-validated data
- Each module should be committed after completion for clean git history

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3", "1.4"] },
    { "id": 2, "tasks": ["2.1"] },
    { "id": 3, "tasks": ["2.2", "2.3"] },
    { "id": 4, "tasks": ["2.4", "2.5"] },
    { "id": 5, "tasks": ["2.6", "2.7", "3.1"] },
    { "id": 6, "tasks": ["3.2", "3.3", "4.1"] },
    { "id": 7, "tasks": ["4.2", "4.3", "5.1"] },
    { "id": 8, "tasks": ["5.2", "5.3", "6.1"] },
    { "id": 9, "tasks": ["6.2", "6.3", "7.1"] },
    { "id": 10, "tasks": ["7.2", "7.3", "8.1", "8.2"] },
    { "id": 11, "tasks": ["8.3", "8.4", "9.1"] },
    { "id": 12, "tasks": ["9.2", "9.3", "10.1"] },
    { "id": 13, "tasks": ["10.2", "10.3"] },
    { "id": 14, "tasks": ["12.1", "12.2", "12.3", "12.4", "12.5", "12.6", "12.7", "12.8", "12.9"] },
    { "id": 15, "tasks": ["14.1"] },
    { "id": 16, "tasks": ["14.2"] },
    { "id": 17, "tasks": ["15.1"] },
    { "id": 18, "tasks": ["17.1"] },
    { "id": 19, "tasks": ["18.1", "18.2"] }
  ]
}
```
