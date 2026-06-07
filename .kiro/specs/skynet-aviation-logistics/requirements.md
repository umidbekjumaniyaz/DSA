# Requirements Document

## Introduction

SkyNet is a Global Aviation Logistics & Management System implemented as a modular Python console application. The system demonstrates mastery of data structures and algorithms in a real-world aviation context, designed to achieve Distinction grade for an HNC/HND Data Structures and Algorithms unit. The application integrates nine interconnected subsystems, each showcasing a specific data structure or algorithmic technique, wrapped in clean object-oriented architecture with comprehensive testing and formal academic documentation.

## Glossary

- **Flight_Network_System**: The subsystem managing airports and flight routes using a weighted graph data structure
- **Airport_Node**: A vertex in the flight network graph representing a physical airport, identified by IATA code
- **Flight_Route**: A weighted edge in the flight network graph representing a direct flight connection between two airports
- **Passenger_Priority_System**: The subsystem managing passenger check-in priority using a max-heap priority queue
- **Boarding_Gate_System**: The subsystem managing passenger boarding order using a FIFO queue
- **Cargo_Management_System**: The subsystem managing cargo loading and unloading using a LIFO stack
- **Flight_Price_Database**: The subsystem storing and querying flight prices using an AVL tree
- **Passenger_Registry**: The subsystem managing passenger records using a hash table with chaining
- **Analytics_System**: The subsystem performing sorting algorithm comparisons using QuickSort and MergeSort
- **Passenger_Search_System**: The subsystem performing string matching on passenger data using the KMP algorithm
- **Emergency_Route_Planner**: The subsystem finding alternative flight routes using recursive backtracking
- **PNR**: Passenger Name Record — a unique alphanumeric identifier for a passenger booking
- **IATA_Code**: A three-letter code assigned by IATA to identify airports (e.g., LHR, JFK, DXB)
- **Priority_Level**: A passenger classification determining check-in order: Platinum (4), Gold (3), Silver (2), Economy (1)
- **MST**: Minimum Spanning Tree — a subset of edges connecting all airports with minimum total weight
- **AVL_Tree**: A self-balancing binary search tree where the height difference between left and right subtrees is at most one
- **KMP_Algorithm**: Knuth-Morris-Pratt string matching algorithm using a failure function for efficient pattern searching
- **Console_Application**: The main entry point providing a text-based menu interface to all subsystems
- **Testing_Framework**: The automated test suite validating correctness of all data structures and algorithms
- **Documentation_Generator**: The component producing academic reports covering all grading criteria

## Requirements

### Requirement 1: Flight Network Graph Construction

**User Story:** As a logistics manager, I want to build and modify a flight network of airports and routes, so that I can model real-world aviation connectivity.

#### Acceptance Criteria

1. WHEN an airport is added with an IATA_Code consisting of exactly 3 uppercase alphabetic characters, THE Flight_Network_System SHALL create a new Airport_Node in the graph and confirm creation
2. WHEN a duplicate IATA_Code is provided for airport creation, THE Flight_Network_System SHALL reject the addition and display an error message identifying the duplicate code
3. WHEN a Flight_Route is added between two existing Airport_Nodes with an integer weight between 1 and 99999 inclusive (representing distance in kilometers), THE Flight_Network_System SHALL create a bidirectional weighted edge connecting the two nodes
4. IF a Flight_Route is added referencing a non-existent Airport_Node, THEN THE Flight_Network_System SHALL reject the route and display an error message identifying the missing airport
5. WHEN an Airport_Node deletion is requested with a valid IATA_Code that exists in the graph, THE Flight_Network_System SHALL remove the node and all associated Flight_Routes from the graph
6. IF an Airport_Node deletion is requested with an IATA_Code that does not exist in the graph, THEN THE Flight_Network_System SHALL reject the deletion and display an error message identifying the missing airport
7. WHEN a Flight_Route deletion is requested between two existing Airport_Nodes that have a connecting edge, THE Flight_Network_System SHALL remove the edge while preserving both Airport_Nodes
8. IF a Flight_Route deletion is requested between two Airport_Nodes that have no connecting edge, THEN THE Flight_Network_System SHALL reject the deletion and display an error message indicating no route exists between the specified airports
9. WHEN the network display is requested and the graph contains at least one Airport_Node, THE Flight_Network_System SHALL output an adjacency list representation showing all airports and their connected routes with weights
10. IF the network display is requested and the graph contains zero Airport_Nodes, THEN THE Flight_Network_System SHALL display a message indicating the network is empty

### Requirement 2: Shortest Path Computation

**User Story:** As a logistics manager, I want to find the shortest path between any two airports, so that I can optimize flight routing.

#### Acceptance Criteria

1. WHEN a shortest path query is issued between two existing Airport_Nodes, THE Flight_Network_System SHALL compute the shortest path using Dijkstra's algorithm and display the route as an ordered sequence of IATA_Codes from source to destination, followed by the total cumulative edge weight of the path
2. IF no path exists between the source and destination Airport_Nodes, THEN THE Flight_Network_System SHALL report that no connection exists between the specified airports
3. IF the source or destination IATA_Code does not exist in the graph, THEN THE Flight_Network_System SHALL display an error message identifying the invalid airport code
4. WHEN Dijkstra's algorithm is executed, THE Flight_Network_System SHALL process edges in order of cumulative minimum weight using a priority queue
5. IF the source and destination IATA_Code are identical, THEN THE Flight_Network_System SHALL return the single airport as the path with a total distance of zero

### Requirement 3: Minimum Spanning Tree Computation

**User Story:** As a logistics manager, I want to compute the minimum spanning tree of the flight network, so that I can identify the most cost-efficient subset of routes connecting all airports.

#### Acceptance Criteria

1. WHEN an MST computation is requested using Prim's algorithm with a valid starting Airport_Node, THE Flight_Network_System SHALL produce a minimum spanning tree starting from that Airport_Node and display each selected edge as a pair of IATA_Codes with its weight, followed by the total MST cost
2. WHEN an MST computation is requested using Kruskal's algorithm, THE Flight_Network_System SHALL produce a minimum spanning tree using edge sorting and union-find, displaying each selected edge as a pair of IATA_Codes with its weight, followed by the total MST cost
3. IF the graph is disconnected when either Prim's or Kruskal's algorithm is invoked, THEN THE Flight_Network_System SHALL report that a spanning tree cannot be formed and list each disconnected component as a group of Airport_Node IATA_Codes
4. THE Flight_Network_System SHALL produce identical MST total costs from both Prim's and Kruskal's algorithms when applied to the same connected graph
5. IF an MST computation using Prim's algorithm is requested with a starting IATA_Code that does not exist in the graph, THEN THE Flight_Network_System SHALL display an error message identifying the invalid airport code
6. IF the graph contains fewer than 2 Airport_Nodes when an MST computation is requested, THEN THE Flight_Network_System SHALL report that insufficient nodes exist to form a spanning tree

### Requirement 4: Passenger Priority Queue Management

**User Story:** As a check-in agent, I want to manage passengers by priority class, so that higher-priority passengers are processed first.

#### Acceptance Criteria

1. WHEN a passenger is added with a valid Priority_Level (Platinum, Gold, Silver, or Economy) and a passenger name, THE Passenger_Priority_System SHALL insert the passenger into the max-heap according to their priority value (Platinum=4, Gold=3, Silver=2, Economy=1) and confirm the insertion by displaying the passenger name and assigned priority
2. WHEN two passengers share the same Priority_Level, THE Passenger_Priority_System SHALL order them by insertion sequence with earlier-inserted passengers processed first (FIFO within the same priority)
3. WHEN the highest-priority passenger is processed, THE Passenger_Priority_System SHALL remove and return the passenger with the maximum priority value from the heap, displaying the passenger name and Priority_Level
4. WHEN a check-in request is issued, THE Passenger_Priority_System SHALL display the current highest-priority passenger's name and Priority_Level without removing them from the queue
5. IF the priority queue is empty when a process or check-in request is issued, THEN THE Passenger_Priority_System SHALL display a message indicating no passengers are waiting
6. THE Passenger_Priority_System SHALL maintain the max-heap property after every insertion and extraction operation
7. IF a passenger is added with a Priority_Level value that is not one of Platinum, Gold, Silver, or Economy, THEN THE Passenger_Priority_System SHALL reject the insertion and display an error message identifying the invalid priority level provided

### Requirement 5: Boarding Gate Queue Management

**User Story:** As a gate agent, I want to manage the boarding queue in first-come-first-served order, so that passengers board the aircraft sequentially.

#### Acceptance Criteria

1. WHEN a passenger joins the boarding queue, THE Boarding_Gate_System SHALL add the passenger to the rear of the FIFO queue and confirm addition by displaying the passenger's identifier and their position in the queue
2. WHEN a passenger is boarded, THE Boarding_Gate_System SHALL remove and return the passenger at the front of the queue
3. WHEN the queue display is requested, THE Boarding_Gate_System SHALL output all passengers in their current queue order from front to rear, showing each passenger's position number and identifier
4. IF the boarding queue is empty when a board request is issued, THEN THE Boarding_Gate_System SHALL display a message indicating no passengers are in the queue
5. THE Boarding_Gate_System SHALL preserve insertion order for all passengers regardless of their Priority_Level
6. IF the boarding queue is empty when a queue display is requested, THEN THE Boarding_Gate_System SHALL display a message indicating the queue is empty
7. IF a passenger who is already in the boarding queue attempts to join again, THEN THE Boarding_Gate_System SHALL reject the duplicate entry and display an error message identifying the duplicate passenger

### Requirement 6: Cargo Stack Management

**User Story:** As a cargo handler, I want to load and unload cargo containers in last-in-first-out order, so that the most recently loaded item is unloaded first.

#### Acceptance Criteria

1. WHEN a cargo item is loaded, THE Cargo_Management_System SHALL push the item onto the top of the cargo stack and display a confirmation message indicating the item was loaded successfully
2. WHEN a cargo item is unloaded, THE Cargo_Management_System SHALL pop the item from the top of the stack and display the removed item's details to the user
3. WHEN the cargo display is requested and the stack contains one or more items, THE Cargo_Management_System SHALL output all cargo items in order from top to bottom of the stack
4. IF the cargo stack is empty when an unload request is issued, THEN THE Cargo_Management_System SHALL display a message indicating no cargo is loaded
5. IF the cargo stack is empty when a display request is issued, THEN THE Cargo_Management_System SHALL display a message indicating the cargo stack is empty
6. WHEN a peek request is issued and the stack contains one or more items, THE Cargo_Management_System SHALL display the item at the top of the stack without removing it
7. IF the cargo stack is empty when a peek request is issued, THEN THE Cargo_Management_System SHALL display a message indicating no cargo is loaded
8. THE Cargo_Management_System SHALL maintain LIFO ordering for all load and unload operations

### Requirement 7: Flight Price AVL Tree Database

**User Story:** As a pricing analyst, I want to store and query flight prices in a balanced search tree, so that I can perform efficient insertions, deletions, and range searches.

#### Acceptance Criteria

1. WHEN a flight price record containing a route (origin and destination IATA_Codes) and a numeric price value is inserted, THE Flight_Price_Database SHALL insert the record into the AVL_Tree keyed by price value and perform rotations to maintain balance
2. WHEN a flight price record is deleted using a specified price value that exists in the AVL_Tree, THE Flight_Price_Database SHALL remove the record and rebalance the AVL_Tree
3. IF a deletion is requested for a price value that does not exist in the AVL_Tree, THEN THE Flight_Price_Database SHALL display a message indicating no record matches the specified price
4. WHEN a search by price value is requested, THE Flight_Price_Database SHALL locate the record in O(log n) time and return the matching record, or display a message indicating no record matches the specified price
5. WHEN a range search is requested with minimum and maximum price bounds where minimum is less than or equal to maximum, THE Flight_Price_Database SHALL return all records with prices within the specified inclusive range, or display a message indicating no records fall within the range
6. WHEN the price display is requested, THE Flight_Price_Database SHALL output all records in ascending price order using an in-order traversal
7. WHEN a flight price record is inserted with a price value that already exists in the AVL_Tree, THE Flight_Price_Database SHALL store the record as a separate entry distinguishable by route information
8. THE Flight_Price_Database SHALL maintain the AVL balance property (height difference between left and right subtrees of any node is at most one) after every insertion and deletion

### Requirement 8: Passenger Registry Hash Table

**User Story:** As a reservations agent, I want to manage passenger records with fast lookup by PNR, so that I can create, search, update, and delete records efficiently.

#### Acceptance Criteria

1. WHEN a new passenger record is created with a unique PNR, THE Passenger_Registry SHALL store the record containing passenger name, flight number, and seat assignment in the hash table and display the stored record details as confirmation
2. WHEN a search by PNR is requested, THE Passenger_Registry SHALL locate and display the matching record with average-case O(1) time complexity
3. WHEN a passenger record update is requested with a valid PNR, THE Passenger_Registry SHALL modify the specified fields (passenger name, flight number, or seat assignment) and display the updated record as confirmation
4. WHEN a passenger record deletion is requested with a valid PNR, THE Passenger_Registry SHALL remove the record from the hash table and display the deleted record details as confirmation
5. IF a duplicate PNR is provided during creation, THEN THE Passenger_Registry SHALL reject the record and display an error identifying the duplicate
6. IF a search, update, or deletion is requested with a PNR that does not exist, THEN THE Passenger_Registry SHALL display an error indicating the PNR was not found
7. WHEN hash collisions occur, THE Passenger_Registry SHALL resolve them using separate chaining to maintain O(1) average-case lookup
8. IF a PNR is provided that is empty or contains non-alphanumeric characters, THEN THE Passenger_Registry SHALL reject the operation and display an error indicating the PNR format is invalid
9. WHEN the registry display is requested, THE Passenger_Registry SHALL output all stored passenger records showing the hash table structure including bucket indices and chained entries

### Requirement 9: Sorting Algorithm Analytics

**User Story:** As a data analyst, I want to sort flight and passenger data using multiple algorithms and compare their performance, so that I can evaluate algorithm efficiency empirically.

#### Acceptance Criteria

1. WHEN a QuickSort operation is requested on a dataset, THE Analytics_System SHALL sort the data in ascending order by the specified numeric sort key using the QuickSort algorithm with a last-element partition strategy and return the sorted result
2. WHEN a MergeSort operation is requested on a dataset, THE Analytics_System SHALL sort the data in ascending order by the specified numeric sort key using the MergeSort algorithm with divide-and-conquer merging and return the sorted result
3. WHEN a comparison report is requested, THE Analytics_System SHALL execute both QuickSort and MergeSort on the same dataset and measure execution time in milliseconds and peak memory usage in bytes for each algorithm
4. WHEN the comparison report is generated, THE Analytics_System SHALL display a report containing for each algorithm: algorithm name, dataset size (number of elements), execution time in milliseconds, memory usage in bytes, and theoretical time complexity for best, average, and worst cases in Big-O notation
5. THE Analytics_System SHALL produce identical sorted output from both QuickSort and MergeSort for any given input dataset when compared element by element in sequence
6. THE Analytics_System SHALL verify sorted output correctness by confirming that every element at position i has a sort key value less than or equal to the element at position i+1
7. IF a sort operation is requested on an empty dataset (zero elements), THEN THE Analytics_System SHALL return an empty result without error
8. IF a sort operation is requested on a dataset containing a single element, THEN THE Analytics_System SHALL return the dataset unchanged
9. WHEN a sort operation is requested, THE Analytics_System SHALL accept datasets containing between 0 and 10,000 numeric records as valid input

### Requirement 10: KMP String Matching for Passenger Search

**User Story:** As a customer service agent, I want to search passenger data by name, PNR fragment, or flight number, so that I can locate passenger records using partial text matching.

#### Acceptance Criteria

1. WHEN a search pattern of 1 to 50 characters is provided, THE Passenger_Search_System SHALL compute the KMP failure function for the pattern
2. WHEN a search is executed against passenger names, THE Passenger_Search_System SHALL perform case-insensitive substring matching and return all passengers whose name contains the search pattern, displaying each matching record's name, PNR, and flight number
3. WHEN a search is executed against PNR codes, THE Passenger_Search_System SHALL perform case-insensitive substring matching and return all passengers whose PNR contains the search pattern, displaying each matching record's name, PNR, and flight number
4. WHEN a search is executed against flight numbers, THE Passenger_Search_System SHALL perform case-insensitive substring matching and return all passengers whose flight number contains the search pattern, displaying each matching record's name, PNR, and flight number
5. IF no matches are found for the search pattern across the selected field, THEN THE Passenger_Search_System SHALL display a message indicating no matching records exist for the given pattern and field
6. THE Passenger_Search_System SHALL perform pattern matching in O(n + m) time per record where n is the text length of the field being searched and m is the pattern length
7. IF the search pattern is empty or contains only whitespace, THEN THE Passenger_Search_System SHALL reject the search and display a message indicating that a non-empty pattern is required

### Requirement 11: Emergency Route Planner with Backtracking

**User Story:** As an operations controller, I want to find all alternative routes when an airport is closed, so that I can redirect flights during emergencies.

#### Acceptance Criteria

1. WHEN an airport closure is declared with a valid IATA_Code, THE Emergency_Route_Planner SHALL mark the specified Airport_Node as unavailable and exclude it from route computation
2. WHEN alternative routes are requested between a source and destination avoiding the closed airport, THE Emergency_Route_Planner SHALL use recursive backtracking to enumerate all paths that do not traverse the closed Airport_Node and do not revisit any Airport_Node
3. WHEN alternative routes are found, THE Emergency_Route_Planner SHALL display each discovered route as an ordered sequence of IATA_Codes from source to destination, with the distance of each leg and the total route distance
4. WHEN multiple alternative routes are found, THE Emergency_Route_Planner SHALL mark the shortest alternative route (lowest total distance) with a distinct label in the output
5. IF no alternative route exists between the source and destination avoiding the closed airport, THEN THE Emergency_Route_Planner SHALL report that no alternative connection is available
6. THE Emergency_Route_Planner SHALL avoid revisiting nodes during path exploration to prevent infinite loops
7. IF the source or destination IATA_Code does not exist in the flight network, THEN THE Emergency_Route_Planner SHALL display an error message identifying the invalid airport code
8. IF the source or destination Airport_Node is the same as the closed airport, THEN THE Emergency_Route_Planner SHALL display an error message indicating that the specified endpoint is currently closed

### Requirement 12: Object-Oriented Architecture

**User Story:** As a developer, I want the system built with proper OOP principles, so that internal data structures are encapsulated and the codebase is maintainable and extensible.

#### Acceptance Criteria

1. THE Console_Application SHALL expose a public interface (abstract base class or protocol) for each of the nine subsystems (Flight_Network_System, Passenger_Priority_System, Boarding_Gate_System, Cargo_Management_System, Flight_Price_Database, Passenger_Registry, Analytics_System, Passenger_Search_System, Emergency_Route_Planner) such that the user interface layer depends only on public method signatures and never directly accesses internal data structure attributes
2. THE Console_Application SHALL define abstract base classes that declare at minimum insert, delete, search, and display operations, which concrete data structure implementations (heap, queue, stack, AVL_Tree, hash table) override with structure-specific behavior
3. THE Console_Application SHALL use inheritance hierarchies where subsystems sharing common behavior inherit from a parent class, with at least one hierarchy containing two or more concrete child classes (e.g., Prim and Kruskal extending a common MST base class, or QuickSort and MergeSort extending a common sorting base class)
4. THE Console_Application SHALL use polymorphism such that algorithm implementations sharing a common interface are substitutable at runtime without modifying calling code, demonstrated by at least two polymorphic groups: MST algorithms (Prim and Kruskal implementing a common MST interface) and sorting algorithms (QuickSort and MergeSort implementing a common sorting interface)
5. THE Console_Application SHALL organize source code into the modular package structure: graph, heap, queue, stack, tree, hashing, sorting, string_matching, backtracking, models, services, and utils, where each package contains only classes and modules related to its named concern
6. IF a concrete data structure class is instantiated, THEN THE Console_Application SHALL ensure that no client code outside the class directly reads or mutates internal storage attributes (e.g., internal arrays, linked list nodes, or tree node pointers) except through defined public methods

### Requirement 13: Automated Testing Suite

**User Story:** As a developer, I want comprehensive automated tests covering normal operation, edge cases, and error conditions, so that I can verify correctness and demonstrate quality assurance.

#### Acceptance Criteria

1. THE Testing_Framework SHALL include tests for an empty graph with zero Airport_Nodes verifying that path queries return an error message indicating no airports exist and MST queries return an error message indicating a spanning tree cannot be formed
2. THE Testing_Framework SHALL include tests for a single Airport_Node graph verifying that shortest path queries to the same node return a distance of zero and that route addition requests to non-existent destinations are rejected with an error message identifying the missing airport
3. THE Testing_Framework SHALL include tests for cyclic graphs verifying that Dijkstra's algorithm terminates and produces correct shortest paths matching manually computed expected distances
4. THE Testing_Framework SHALL include tests for disconnected graphs verifying that MST algorithms report that a spanning tree cannot be formed and identify the disconnected components
5. THE Testing_Framework SHALL include tests for an empty queue verifying that board operations return an error message indicating no passengers are in the queue
6. THE Testing_Framework SHALL include tests for an empty stack verifying that unload operations return an error message indicating no cargo is loaded
7. THE Testing_Framework SHALL include tests for duplicate passenger PNR verifying that the Passenger_Registry rejects the duplicate and displays an error identifying the duplicate PNR value
8. THE Testing_Framework SHALL include tests for invalid PNR lookup verifying that the Passenger_Registry returns an error indicating the PNR was not found
9. THE Testing_Framework SHALL include tests for heap priority collision verifying that passengers with equal Priority_Level are dequeued in arrival-time order with earlier arrivals returned first
10. THE Testing_Framework SHALL include tests for missing airport references verifying that route operations reject invalid IATA codes and display an error message identifying the invalid code
11. WHEN the test suite is executed, THE Testing_Framework SHALL generate a testing report containing: total number of tests executed, number of tests passed, number of tests failed, and percentage of subsystems with at least one passing test
12. THE Testing_Framework SHALL include at least one normal-operation test per subsystem verifying correct output for valid inputs (e.g., successful airport addition, successful passenger insertion, successful sort completion)
13. THE Testing_Framework SHALL include at least 3 tests per subsystem covering normal operation, edge case, and error condition categories

### Requirement 14: Academic Documentation

**User Story:** As a student, I want complete academic documentation covering all grading criteria, so that I can demonstrate understanding and achieve Distinction grade.

#### Acceptance Criteria

1. THE Documentation_Generator SHALL produce explanations for every implemented algorithm (Dijkstra's, Prim's, Kruskal's, heap insert/extract, enqueue/dequeue, push/pop, AVL insert/delete/rotate, hash insert/lookup with chaining, QuickSort, MergeSort, KMP pattern matching, and recursive backtracking) covering: purpose, step-by-step operation, and real-world application context within the aviation logistics domain
2. THE Documentation_Generator SHALL include time complexity analysis for every algorithm listed in criterion 1, specifying best-case, average-case, and worst-case Big-O notation with justification for each bound
3. THE Documentation_Generator SHALL include space complexity analysis for every algorithm listed in criterion 1, specifying auxiliary space usage in Big-O notation with justification for each bound
4. THE Documentation_Generator SHALL include flowchart diagrams (using Mermaid syntax) for the following algorithms: Dijkstra's shortest path, Prim's MST, Kruskal's MST, QuickSort partitioning, MergeSort divide-and-conquer, KMP pattern matching, AVL tree rotation, and recursive backtracking route exploration
5. THE Documentation_Generator SHALL address all Pass criteria (P1-P7) by examining each abstract data type (graph, heap, queue, stack, AVL tree, hash table) and specifying their associated algorithms using pseudocode notation
6. THE Documentation_Generator SHALL address all Merit criteria (M1-M5) by illustrating algorithm operation with step-by-step walkthroughs showing state changes on sample input data, and by stating and justifying time and space complexity for each algorithm
7. THE Documentation_Generator SHALL address all Distinction criteria (D1-D4) by evaluating efficiency of the AVL tree, graph, and hash table structures with comparative analysis, comparing asymptotic complexity between algorithm pairs (QuickSort vs MergeSort, Prim's vs Kruskal's, Dijkstra's vs backtracking), and assessing algorithmic effectiveness using measured execution time and memory usage data collected from datasets of at least three different sizes
8. THE Documentation_Generator SHALL structure the academic report with one dedicated section per grading criterion (P1 through P7, M1 through M5, D1 through D4) so that each criterion is individually identifiable and verifiable by a grader

### Requirement 15: Console Application Interface

**User Story:** As a user, I want a clear text-based menu system, so that I can navigate between all subsystems and perform operations without confusion.

#### Acceptance Criteria

1. WHEN the Console_Application starts, THE Console_Application SHALL display a main menu listing all nine subsystems (Flight_Network_System, Passenger_Priority_System, Boarding_Gate_System, Cargo_Management_System, Flight_Price_Database, Passenger_Registry, Analytics_System, Passenger_Search_System, Emergency_Route_Planner) with numbered options 1 through 9 and an exit option
2. WHEN a valid menu option is selected, THE Console_Application SHALL display the corresponding subsystem menu showing the available operations for that subsystem with numbered options and a return-to-main-menu option
3. WHEN an input is entered that is non-numeric or outside the range of displayed menu options, THE Console_Application SHALL display an error message indicating the valid range of options and re-display the current menu
4. WHEN a subsystem operation completes, THE Console_Application SHALL display the operation output and return to the subsystem menu
5. WHEN the user selects the exit option, THE Console_Application SHALL terminate without unhandled exceptions and display a confirmation message before closing
6. THE Console_Application SHALL validate all user inputs by checking for correct data type and permitted value range before passing them to subsystem operations, and IF validation fails, THEN THE Console_Application SHALL display an error message indicating the expected input format and re-prompt the user
7. WHEN the user selects the return-to-main-menu option from a subsystem menu, THE Console_Application SHALL display the main menu
