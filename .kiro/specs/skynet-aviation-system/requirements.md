# Requirements Document

## Introduction

The SkyNet Global Aviation Logistics & Management System is a Python 3, object-oriented console application developed for a BTEC HND Unit 26 (Data Structures & Algorithms) assignment targeting a Distinction grade. The system demonstrates the design, implementation, and analysis of classic data structures and algorithms applied to a realistic aviation logistics domain.

The application is organised into five technical phases: (1) global navigation and infrastructure using graphs and shortest-path / minimum-spanning-tree algorithms; (2) passenger priority and check-in using heaps, queues, and stacks; (3) high-speed search and retrieval using trees and hashing; (4) data analytics and string processing using comparative sorting and pattern matching; and (5) contingency planning using recursive backtracking. The system additionally satisfies explicit error-handling, testing, complexity-analysis, and Pearson BTEC academic documentation criteria (P1–P7, M1–M5, D1–D4).

The deliverables include formal Abstract Data Type (ADT) specifications, asymptotic (Big-O) analysis, an encapsulation and OOP design explanation, an evaluation with edge-case test cases, and a 2000–2500 word documentation report using Harvard referencing, all delivered within a professional Python project structure.

## Glossary

- **SkyNet_System**: The complete SkyNet Global Aviation Logistics & Management System console application.
- **Console_Menu**: The text-based interactive interface through which the User issues commands and reads output.
- **User**: The human operator (assessor or aviation logistics operator) interacting with the Console_Menu.
- **Airport**: A graph node representing a single airport, identified by a unique airport code.
- **Route**: A weighted, directed or undirected graph edge representing a direct flight between two Airports, carrying a weight attribute (cost, distance, or time).
- **Flight_Network**: The graph data structure holding all Airports and Routes, represented as an Adjacency List and optionally an Adjacency Matrix.
- **Dijkstra_Module**: The component implementing Dijkstra's shortest-path algorithm over the Flight_Network.
- **MST_Module**: The component implementing a Minimum Spanning Tree algorithm (Kruskal's or Prim's) over the Flight_Network.
- **Backup_Network**: The set of Routes forming the Minimum Spanning Tree connecting all Airports at lowest total weight.
- **Priority_Queue**: A check-in queue implemented with a Max-Heap, ordered by Ticket_Status.
- **Ticket_Status**: A passenger priority rank with the ordering Platinum > Gold > Silver > Economy.
- **Boarding_Queue**: A First-In-First-Out (FIFO) queue managing passengers at the boarding gate.
- **Cargo_Stack**: A Last-In-First-Out (LIFO) stack managing luggage in the cargo hold.
- **Price_Tree**: A self-balancing AVL Tree (or Binary Search Tree) storing flight prices and supporting range queries.
- **PNR**: A Passenger Name Record, a unique identifier string for a passenger booking.
- **PNR_Hash_Table**: A hash table mapping each PNR to a Passenger profile for average O(1) retrieval.
- **Passenger**: A record containing passenger profile details including a PNR and Ticket_Status.
- **Sort_Module**: The component implementing QuickSort and MergeSort for organising flight schedules.
- **Flight_Schedule**: A collection of flight records sortable by departure time or fuel efficiency.
- **KMP_Module**: The component implementing the Knuth-Morris-Pratt string-matching algorithm.
- **Manifest**: A large text collection of passenger names searched by the KMP_Module.
- **Backtracking_Module**: The component implementing recursive backtracking to enumerate alternative flight paths.
- **Hub**: An Airport designated as a primary connecting point whose unavailability triggers contingency routing.
- **Complexity_Report**: The documentation artifact stating time and space complexity for each algorithm.
- **Test_Report**: The generated artifact recording test cases and their results.
- **Documentation_Report**: The 2000–2500 word academic report using Harvard referencing covering ADT specifications, asymptotic analysis, encapsulation, and evaluation.

## Requirements

### Requirement 1: Airport Management (Phase 1 — Graph Nodes)

**User Story:** As an aviation logistics operator, I want to add and view airports in the network, so that I can model the global set of locations the system serves.

#### Acceptance Criteria

1. WHEN the User submits an add-airport command with a unique airport code, THE SkyNet_System SHALL add the Airport as a node in the Flight_Network and confirm the addition.
2. IF the User submits an add-airport command with an airport code that already exists in the Flight_Network, THEN THE SkyNet_System SHALL reject the command and return a duplicate-airport error message.
3. WHEN the User submits a display-network command, THE SkyNet_System SHALL output every Airport and every associated Route with its weight.
4. IF the User submits a display-network command while the Flight_Network contains no Airports, THEN THE SkyNet_System SHALL return an empty-graph message.

### Requirement 2: Route Management (Phase 1 — Weighted Graph Edges)

**User Story:** As an aviation logistics operator, I want to add weighted routes between airports, so that I can model direct flights with cost, distance, or time.

#### Acceptance Criteria

1. WHEN the User submits an add-route command specifying two existing Airports and a positive numeric weight, THE SkyNet_System SHALL add a Route between the two Airports in the Flight_Network and confirm the addition.
2. IF the User submits an add-route command referencing an airport code that does not exist in the Flight_Network, THEN THE SkyNet_System SHALL return a missing-airport error message.
3. IF the User submits an add-route command for a pair of Airports that already has a Route, THEN THE SkyNet_System SHALL return a duplicate-route error message.
4. THE Flight_Network SHALL represent Airports and Routes using an Adjacency List.

### Requirement 3: Cheapest Route Calculation (Phase 1 — Dijkstra's Algorithm)

**User Story:** As an aviation logistics operator, I want to find the most cost-effective route between two cities, so that I can minimise travel cost.

#### Acceptance Criteria

1. WHEN the User submits a find-cheapest-route command specifying a source Airport and a destination Airport that are connected, THE Dijkstra_Module SHALL return the minimum-weight path and its total weight.
2. IF the User submits a find-cheapest-route command for a source and destination with no connecting path, THEN THE Dijkstra_Module SHALL return a no-available-route message.
3. IF the User submits a find-cheapest-route command referencing an airport code that does not exist in the Flight_Network, THEN THE SkyNet_System SHALL return a missing-airport error message.
4. WHEN the source Airport equals the destination Airport, THE Dijkstra_Module SHALL return a path of total weight zero.

### Requirement 4: Backup Communication Network (Phase 1 — Minimum Spanning Tree)

**User Story:** As an aviation logistics operator, I want to generate a backup communication network connecting all airports at the lowest infrastructure cost, so that I can plan resilient infrastructure.

#### Acceptance Criteria

1. WHEN the User submits a generate-backup-network command while the Flight_Network is connected and contains at least two Airports, THE MST_Module SHALL return the Backup_Network and its total weight using Kruskal's or Prim's algorithm.
2. THE MST_Module SHALL produce a Backup_Network containing exactly one fewer Route than the number of Airports it connects.
3. IF the User submits a generate-backup-network command while the Flight_Network is disconnected, THEN THE MST_Module SHALL return a message identifying that a spanning tree covering all Airports cannot be formed.
4. IF the User submits a generate-backup-network command while the Flight_Network contains no Airports, THEN THE SkyNet_System SHALL return an empty-graph message.

### Requirement 5: Priority Check-in Queue (Phase 2 — Max-Heap)

**User Story:** As a check-in agent, I want passengers served by ticket priority rather than arrival order, so that premium passengers are processed first.

#### Acceptance Criteria

1. WHEN the User enqueues a Passenger into the Priority_Queue, THE Priority_Queue SHALL store the Passenger ordered by Ticket_Status using a Max-Heap.
2. WHEN the User dequeues from the Priority_Queue, THE Priority_Queue SHALL return the Passenger with the highest Ticket_Status rank, where the rank order is Platinum, then Gold, then Silver, then Economy.
3. WHEN two Passengers in the Priority_Queue share the same Ticket_Status, THE Priority_Queue SHALL return one of the equal-ranked Passengers and retain the other in the Priority_Queue.
4. IF the User dequeues from the Priority_Queue while it contains no Passengers, THEN THE Priority_Queue SHALL return an empty-queue error message.

### Requirement 6: Boarding Gate Queue (Phase 2 — FIFO Queue)

**User Story:** As a boarding agent, I want passengers boarded in arrival order at the gate, so that boarding is fair and orderly.

#### Acceptance Criteria

1. WHEN the User enqueues a Passenger into the Boarding_Queue, THE Boarding_Queue SHALL append the Passenger to the tail of the queue.
2. WHEN the User dequeues from the Boarding_Queue, THE Boarding_Queue SHALL return the Passenger that has been in the queue longest in First-In-First-Out order.
3. IF the User dequeues from the Boarding_Queue while it contains no Passengers, THEN THE Boarding_Queue SHALL return an empty-queue error message.

### Requirement 7: Cargo Hold Stack (Phase 2 — LIFO Stack)

**User Story:** As a cargo handler, I want to load and unload luggage in last-in-first-out order, so that the cargo hold reflects physical loading constraints.

#### Acceptance Criteria

1. WHEN the User pushes a luggage item onto the Cargo_Stack, THE Cargo_Stack SHALL place the item at the top of the stack.
2. WHEN the User pops from the Cargo_Stack, THE Cargo_Stack SHALL return the most recently pushed item in Last-In-First-Out order.
3. IF the User pops from the Cargo_Stack while it contains no items, THEN THE Cargo_Stack SHALL return an empty-stack error message.

### Requirement 8: Flight Price Tree (Phase 3 — AVL/BST with Range Queries)

**User Story:** As an analyst, I want to store and filter flight prices with logarithmic-time range queries, so that I can retrieve price bands efficiently.

#### Acceptance Criteria

1. WHEN the User inserts a flight price into the Price_Tree, THE Price_Tree SHALL store the price while maintaining sorted ordering.
2. WHEN the User searches the Price_Tree for a specific price, THE Price_Tree SHALL return whether the price is present.
3. WHEN the User submits a range-search command with a lower bound and an upper bound, THE Price_Tree SHALL return every stored price that falls within the inclusive bounds.
4. WHERE the Price_Tree is implemented as an AVL Tree, THE Price_Tree SHALL maintain a height-balanced structure after every insertion so that search and range operations execute in O(log n) time.
5. IF the User submits a range-search command where the lower bound exceeds the upper bound, THEN THE Price_Tree SHALL return an empty result set.

### Requirement 9: Passenger Record Hash Table (Phase 3 — Hashing)

**User Story:** As a check-in agent, I want to retrieve passenger profiles by PNR in constant average time, so that lookups are fast at scale.

#### Acceptance Criteria

1. WHEN the User stores a Passenger with a unique PNR, THE PNR_Hash_Table SHALL map the PNR to the Passenger profile.
2. WHEN the User searches the PNR_Hash_Table by a PNR that is present, THE PNR_Hash_Table SHALL return the associated Passenger profile in average O(1) time.
3. WHEN the User deletes a PNR that is present, THE PNR_Hash_Table SHALL remove the mapping and confirm the deletion.
4. IF the User searches or deletes the PNR_Hash_Table by a PNR that is not present, THEN THE PNR_Hash_Table SHALL return a passenger-not-found error message.
5. WHEN two distinct PNRs hash to the same bucket, THE PNR_Hash_Table SHALL store both mappings using a collision-resolution strategy and retrieve each correctly.

### Requirement 10: PNR Validation (Phase 3 — Input Integrity)

**User Story:** As a check-in agent, I want invalid PNRs rejected, so that the system maintains data integrity.

#### Acceptance Criteria

1. IF the User submits a PNR that does not conform to the defined PNR format, THEN THE SkyNet_System SHALL return an invalid-PNR error message and SHALL reject the operation.

### Requirement 11: Comparative Sorting of Schedules (Phase 4 — QuickSort vs MergeSort)

**User Story:** As an analyst, I want to sort daily flight schedules using two algorithms and compare them, so that I can evaluate sorting performance.

#### Acceptance Criteria

1. WHEN the User submits a sort command selecting a sort key of departure time or fuel efficiency, THE Sort_Module SHALL order the Flight_Schedule by the selected key using QuickSort.
2. WHEN the User submits a sort command selecting MergeSort, THE Sort_Module SHALL order the Flight_Schedule by the selected key using MergeSort.
3. FOR any input Flight_Schedule, QuickSort and MergeSort SHALL produce identical ordered output.
4. WHEN the User runs the sorting comparison, THE Sort_Module SHALL report the measured execution time for QuickSort and for MergeSort over the same input.
5. WHEN the Flight_Schedule contains no records, THE Sort_Module SHALL return an empty ordered result.

### Requirement 12: Passenger Name Search (Phase 4 — KMP String Matching)

**User Story:** As an operator, I want to search passenger names within large manifests, so that I can locate passengers quickly.

#### Acceptance Criteria

1. WHEN the User submits a name-search command with a search pattern that occurs in the Manifest, THE KMP_Module SHALL return every position at which the pattern occurs.
2. WHEN the User submits a name-search command with a search pattern that does not occur in the Manifest, THE KMP_Module SHALL return an empty result set.
3. WHEN the User submits a name-search command with an empty Manifest, THE KMP_Module SHALL return an empty result set.

### Requirement 13: KMP Search Round-Trip Verification

**User Story:** As a developer, I want confidence that the KMP search returns correct match positions, so that the string-matching implementation is verifiably correct.

#### Acceptance Criteria

1. FOR any Manifest text and any pattern, every position returned by the KMP_Module SHALL mark a substring of the Manifest equal to the pattern.
2. FOR any Manifest text and any pattern, the set of positions returned by the KMP_Module SHALL equal the set of positions found by a naive substring scan of the same Manifest and pattern.

### Requirement 14: Contingency Path Enumeration (Phase 5 — Recursive Backtracking)

**User Story:** As an operations planner, I want to enumerate all alternative flight paths when a primary hub is unavailable, so that I can plan contingencies.

#### Acceptance Criteria

1. WHEN the User submits a contingency command specifying a source Airport, a destination Airport, and an unavailable Hub, THE Backtracking_Module SHALL return every valid path from source to destination that excludes the unavailable Hub.
2. THE Backtracking_Module SHALL return only paths in which no Airport appears more than once.
3. IF the User submits a contingency command for which no valid path exists that excludes the unavailable Hub, THEN THE Backtracking_Module SHALL return a no-available-route message.
4. IF the User submits a contingency command referencing an airport code that does not exist in the Flight_Network, THEN THE SkyNet_System SHALL return a missing-airport error message.

### Requirement 15: Consolidated Error Handling

**User Story:** As a User, I want clear, consistent error messages for invalid operations, so that I understand and can recover from failures.

#### Acceptance Criteria

1. IF an operation is requested against an empty Flight_Network, THEN THE SkyNet_System SHALL return an empty-graph error message.
2. IF an operation references an Airport that does not exist, THEN THE SkyNet_System SHALL return a missing-airport error message.
3. IF an operation requests a route between two Airports with no connecting path, THEN THE SkyNet_System SHALL return a no-available-route error message.
4. WHEN any error condition defined in Requirements 1 through 14 occurs, THE SkyNet_System SHALL display the error message and SHALL return control to the Console_Menu without terminating the application.

### Requirement 16: Test Suite and Test Report

**User Story:** As an assessor, I want extensive test cases covering edge cases with recorded results, so that I can confirm correctness and robustness (satisfies P5).

#### Acceptance Criteria

1. THE SkyNet_System SHALL include automated test cases covering empty graph, cyclic graph, and disconnected graph scenarios for the Flight_Network.
2. THE SkyNet_System SHALL include automated test cases covering Priority_Queue priority collision, empty Boarding_Queue, and empty Cargo_Stack scenarios.
3. THE SkyNet_System SHALL include automated test cases covering Price_Tree edge cases, PNR_Hash_Table collision, sorting worst-case input, and backtracking failure scenarios.
4. WHEN the test suite is executed, THE SkyNet_System SHALL generate a Test_Report recording each test case and its pass or fail result.

### Requirement 17: Complexity Analysis Report

**User Story:** As an assessor, I want documented complexity analysis for every algorithm, so that I can assess analytical understanding (supports P6, P7, D3).

#### Acceptance Criteria

1. THE Complexity_Report SHALL state the time complexity and space complexity for each of Dijkstra's algorithm, the MST algorithm, the Max-Heap Priority_Queue, the FIFO Boarding_Queue, the LIFO Cargo_Stack, the Price_Tree, the PNR_Hash_Table, QuickSort, MergeSort, the KMP_Module, and the Backtracking_Module.
2. THE Complexity_Report SHALL state the best-case, average-case, and worst-case behaviour for each algorithm listed in acceptance criterion 1.
3. THE Documentation_Report SHALL discuss how asymptotic analysis assesses algorithm effectiveness and SHALL present two ways to measure algorithm efficiency, each illustrated with an example.

### Requirement 18: Formal ADT Specifications

**User Story:** As an assessor, I want formal ADT specifications for the core structures, so that design intent and valid operations are explicit (satisfies P1, P3, M5).

#### Acceptance Criteria

1. THE Documentation_Report SHALL provide a design specification for the system's data structures explaining the valid operations of each.
2. THE Documentation_Report SHALL specify the Abstract Data Type for a stack using an imperative definition.
3. THE Documentation_Report SHALL provide formal ADT specifications for the Stack, the Queue, and the Graph.
4. THE Documentation_Report SHALL interpret a trade-off encountered when specifying an ADT, illustrated with an example.

### Requirement 19: Memory Stack and Function Calls Explanation

**User Story:** As an assessor, I want an explanation of memory stack operation, so that I can confirm understanding of call mechanics (satisfies P2).

#### Acceptance Criteria

1. THE Documentation_Report SHALL explain the operations of a memory stack and how a memory stack implements function calls.

### Requirement 20: Encapsulation, Information Hiding, and OOP Design

**User Story:** As an assessor, I want the OOP design and encapsulation benefits explained and demonstrated, so that I can assess design quality (satisfies M3, D2, D4).

#### Acceptance Criteria

1. THE SkyNet_System SHALL implement each data structure as an encapsulated class that exposes its operations through public methods and hides its internal representation.
2. THE Documentation_Report SHALL describe the advantages of encapsulation and information hiding when using an ADT.
3. THE Documentation_Report SHALL discuss, with justification, the view that imperative ADTs are a basis for object orientation.
4. THE Documentation_Report SHALL evaluate three benefits of implementation-independent data structures.

### Requirement 21: Problem-Solving Demonstration

**User Story:** As an assessor, I want the implementation shown to solve a well-defined problem, so that I can confirm applied competence (satisfies P4, M4).

#### Acceptance Criteria

1. THE SkyNet_System SHALL implement a complex ADT and algorithm in executable Python 3 that solves the aviation logistics routing and management problem.
2. THE Documentation_Report SHALL demonstrate how the ADT and algorithm implementation solves the defined aviation logistics problem.

### Requirement 22: FIFO Queue Illustration and Sorting Comparison Reporting

**User Story:** As an assessor, I want a concrete FIFO queue illustration and a sorting performance comparison, so that I can assess merit criteria (satisfies M1, M2).

#### Acceptance Criteria

1. THE Documentation_Report SHALL illustrate a concrete data structure for a FIFO queue with a worked example.
2. THE Documentation_Report SHALL compare the performance of QuickSort and MergeSort, referencing the execution times measured by the Sort_Module.

### Requirement 23: Shortest Path Algorithm Analysis

**User Story:** As an assessor, I want an analysis of two network shortest-path algorithms with worked examples, so that I can assess distinction criteria (satisfies D1).

#### Acceptance Criteria

1. THE Documentation_Report SHALL analyse, with illustrations, the operation of two network shortest-path algorithms, providing a worked example of each.

### Requirement 24: Documentation Report Deliverable

**User Story:** As an assessor, I want a complete academic report within a professional project layout, so that the submission meets formatting and structural standards.

#### Acceptance Criteria

1. THE Documentation_Report SHALL contain between 2000 and 2500 words.
2. THE Documentation_Report SHALL use Harvard referencing for all cited sources.
3. THE SkyNet_System SHALL be delivered with a project structure containing main.py, README.md, requirements.txt, and the directories models, data_structures, algorithms, services, tests, and docs.
4. WHEN the User runs main.py, THE SkyNet_System SHALL present the Console_Menu listing the available operations across all five phases.
