# System Design — SkyNet Aviation Logistics

## Architecture Overview

SkyNet follows a **three-layer architecture** pattern separating concerns across UI, Service, and Data Structure layers, with a shared Domain Model layer providing data transfer objects.

---

## High-Level System Architecture

```mermaid
graph TB
    subgraph UI["Console UI Layer"]
        Main["main.py<br/>Application Entry Point"]
        MenuHandler["menu.py<br/>Menu Navigation"]
        InputHandler["input_handler.py<br/>Input Validation"]
    end

    subgraph Services["Service Layer (Business Logic)"]
        FNS["FlightNetworkService<br/>Graph + Dijkstra + MST"]
        PPS["PassengerPriorityService<br/>Max-Heap Management"]
        BGS["BoardingGateService<br/>FIFO Queue Management"]
        CMS["CargoManagementService<br/>LIFO Stack Management"]
        FPD["FlightPriceService<br/>AVL Tree Operations"]
        PRS["PassengerRegistryService<br/>Hash Table CRUD"]
        ANS["AnalyticsService<br/>Sorting Comparisons"]
        PSS["PassengerSearchService<br/>KMP Pattern Matching"]
        ERP["EmergencyRoutePlannerService<br/>Backtracking Routes"]
    end

    subgraph DataStructures["Data Structure Layer"]
        WG["WeightedGraph<br/>Adjacency List"]
        DS["DijkstraSolver"]
        PM["PrimMST"]
        KM["KruskalMST"]
        UF["UnionFind"]
        MH["MaxHeap"]
        FQ["FIFOQueue"]
        LS["LIFOStack"]
        AT["AVLTree"]
        HT["HashTable"]
        QS["QuickSort"]
        MS["MergeSort"]
        KMP["KMPMatcher"]
        BT["BacktrackingSolver"]
    end

    subgraph Models["Domain Models"]
        Airport["Airport"]
        Passenger["Passenger"]
        Cargo["Cargo"]
        PriceRecord["PriceRecord"]
        Path["Path"]
    end

    Main --> MenuHandler
    MenuHandler --> InputHandler
    MenuHandler --> FNS
    MenuHandler --> PPS
    MenuHandler --> BGS
    MenuHandler --> CMS
    MenuHandler --> FPD
    MenuHandler --> PRS
    MenuHandler --> ANS
    MenuHandler --> PSS
    MenuHandler --> ERP

    FNS --> WG
    FNS --> DS
    FNS --> PM
    FNS --> KM
    KM --> UF
    PPS --> MH
    BGS --> FQ
    CMS --> LS
    FPD --> AT
    PRS --> HT
    ANS --> QS
    ANS --> MS
    PSS --> KMP
    ERP --> BT
    ERP --> WG
```

---

## Class Hierarchy

### Abstract Base Classes

```mermaid
classDiagram
    class DataStructureBase {
        <<abstract>>
        +insert(item) OperationResult
        +delete(key) OperationResult
        +search(key) OperationResult
        +display() str
        +is_empty() bool
        +size() int
    }

    class MSTAlgorithm {
        <<abstract>>
        +compute_mst(graph, start_node) MSTResult
        +get_name() str
    }

    class SortAlgorithm {
        <<abstract>>
        +sort(data, key_func) SortResult
        +get_name() str
        +get_complexity() ComplexityInfo
    }

    DataStructureBase <|-- MaxHeap
    DataStructureBase <|-- FIFOQueue
    DataStructureBase <|-- LIFOStack
    DataStructureBase <|-- AVLTree
    DataStructureBase <|-- HashTable

    MSTAlgorithm <|-- PrimMST
    MSTAlgorithm <|-- KruskalMST

    SortAlgorithm <|-- QuickSort
    SortAlgorithm <|-- MergeSort
```

### Data Structure Classes

```mermaid
classDiagram
    class WeightedGraph {
        -_adjacency: Dict~str, List~
        -_nodes: Dict~str, Airport~
        +add_node(airport) OperationResult
        +remove_node(iata_code) OperationResult
        +add_edge(src, dest, weight) OperationResult
        +remove_edge(src, dest) OperationResult
        +get_neighbors(iata_code) List
        +get_all_nodes() List~str~
        +get_all_edges() List~Tuple~
        +has_node(iata_code) bool
        +has_edge(src, dest) bool
        +node_count() int
        +edge_count() int
        +display() str
    }

    class MaxHeap {
        -_heap: List~Tuple~
        -_sequence: int
        +insert(item, priority) OperationResult
        +extract_max() OperationResult
        +peek() OperationResult
        +delete(key) OperationResult
        +search(key) OperationResult
        +is_empty() bool
        +size() int
        +display() str
        -_sift_up(index) void
        -_sift_down(index) void
    }

    class FIFOQueue {
        -_head: QueueNode
        -_tail: QueueNode
        -_size: int
        -_members: Set~str~
        +enqueue(item, identifier) OperationResult
        +dequeue() OperationResult
        +peek() OperationResult
        +contains(identifier) bool
        +is_empty() bool
        +size() int
        +display() str
    }

    class LIFOStack {
        -_items: List
        +push(item) OperationResult
        +pop() OperationResult
        +peek() OperationResult
        +is_empty() bool
        +size() int
        +display() str
    }

    class AVLTree {
        -_root: AVLNode
        -_size: int
        +insert(record) OperationResult
        +delete(price) OperationResult
        +search(price) OperationResult
        +range_search(min, max) OperationResult
        +in_order_traversal() List
        +is_empty() bool
        +size() int
        +display() str
        -_rotate_left(node) AVLNode
        -_rotate_right(node) AVLNode
        -_get_balance(node) int
        -_rebalance(node) AVLNode
    }

    class HashTable {
        -_buckets: List~List~
        -_capacity: int
        -_size: int
        +insert(key, value) OperationResult
        +delete(key) OperationResult
        +search(key) OperationResult
        +update(key, value) OperationResult
        +is_empty() bool
        +size() int
        +display() str
        -_hash(key) int
    }

    class AVLNode {
        +key: float
        +records: List
        +left: AVLNode
        +right: AVLNode
        +height: int
    }

    class QueueNode {
        +data: Any
        +identifier: str
        +next: QueueNode
    }

    AVLTree --> AVLNode
    FIFOQueue --> QueueNode
```

### Algorithm Classes

```mermaid
classDiagram
    class DijkstraSolver {
        +compute(graph, source, destination) OperationResult
    }

    class PrimMST {
        +compute_mst(graph, start_node) MSTResult
        +get_name() str
    }

    class KruskalMST {
        -_union_find: UnionFind
        +compute_mst(graph, start_node) MSTResult
        +get_name() str
    }

    class UnionFind {
        -_parent: Dict~str, str~
        -_rank: Dict~str, int~
        +make_set(item) void
        +find(item) str
        +union(a, b) bool
    }

    class KMPMatcher {
        +search(text, pattern) List~int~
        +compute_failure_function(pattern) List~int~
    }

    class BacktrackingSolver {
        +find_all_paths(graph, source, dest, excluded) List~Path~
        -_backtrack(current, dest, path, visited, excluded, graph) void
    }

    class QuickSort {
        +sort(data, key_func) SortResult
        +get_name() str
        +get_complexity() ComplexityInfo
        -_quicksort(arr, low, high, key_func) void
        -_partition(arr, low, high, key_func) int
    }

    class MergeSort {
        +sort(data, key_func) SortResult
        +get_name() str
        +get_complexity() ComplexityInfo
        -_mergesort(arr, key_func) List
        -_merge(left, right, key_func) List
    }

    KruskalMST --> UnionFind
```

### Service Layer Classes

```mermaid
classDiagram
    class FlightNetworkService {
        -_graph: WeightedGraph
        -_dijkstra: DijkstraSolver
        -_prim: PrimMST
        -_kruskal: KruskalMST
        +add_airport(iata, name, city) OperationResult
        +remove_airport(iata) OperationResult
        +add_route(src, dest, distance) OperationResult
        +remove_route(src, dest) OperationResult
        +shortest_path(src, dest) OperationResult
        +compute_mst_prim(start) MSTResult
        +compute_mst_kruskal() MSTResult
        +display_network() str
    }

    class PassengerPriorityService {
        -_heap: MaxHeap
        +add_passenger(name, priority) OperationResult
        +process_next() OperationResult
        +peek_next() OperationResult
        +display_queue() str
    }

    class BoardingGateService {
        -_queue: FIFOQueue
        +add_to_boarding(passenger_id, name) OperationResult
        +board_next() OperationResult
        +display_queue() str
    }

    class CargoManagementService {
        -_stack: LIFOStack
        +load_cargo(item_id, description, weight) OperationResult
        +unload_cargo() OperationResult
        +peek_top() OperationResult
        +display_stack() str
    }

    class FlightPriceService {
        -_avl_tree: AVLTree
        +add_price(origin, dest, price) OperationResult
        +remove_price(price) OperationResult
        +search_price(price) OperationResult
        +range_search(min, max) OperationResult
        +display_prices() str
    }

    class PassengerRegistryService {
        -_hash_table: HashTable
        +create_record(pnr, name, flight, seat) OperationResult
        +search_record(pnr) OperationResult
        +update_record(pnr, fields) OperationResult
        +delete_record(pnr) OperationResult
        +display_registry() str
    }

    class AnalyticsService {
        -_quicksort: QuickSort
        -_mergesort: MergeSort
        +sort_with_quicksort(data, key_func) SortResult
        +sort_with_mergesort(data, key_func) SortResult
        +comparison_report(data, key_func) str
    }

    class PassengerSearchService {
        -_kmp: KMPMatcher
        -_registry: PassengerRegistryService
        +search_by_name(pattern) OperationResult
        +search_by_pnr(pattern) OperationResult
        +search_by_flight(pattern) OperationResult
    }

    class EmergencyRoutePlannerService {
        -_solver: BacktrackingSolver
        -_graph: WeightedGraph
        -_closed_airports: Set
        +close_airport(iata) OperationResult
        +reopen_airport(iata) OperationResult
        +find_alternatives(src, dest) OperationResult
    }
```

---

## Entity Relationship Diagram

```mermaid
erDiagram
    AIRPORT {
        string iata_code PK
        string name
        string city
    }

    FLIGHT_ROUTE {
        string origin FK
        string destination FK
        int distance_km
    }

    PASSENGER {
        string pnr PK
        string name
        string flight_number
        string seat
        enum priority_level
    }

    CARGO {
        string item_id PK
        string description
        float weight_kg
        string flight_number
    }

    PRICE_RECORD {
        string origin FK
        string destination FK
        float price
        string currency
    }

    AIRPORT ||--o{ FLIGHT_ROUTE : "origin"
    AIRPORT ||--o{ FLIGHT_ROUTE : "destination"
    AIRPORT ||--o{ PRICE_RECORD : "origin"
    AIRPORT ||--o{ PRICE_RECORD : "destination"
```

---

## Sequence Diagrams

### Shortest Path Query

```mermaid
sequenceDiagram
    participant User
    participant UI as Console UI
    participant FNS as FlightNetworkService
    participant Graph as WeightedGraph
    participant Dijkstra as DijkstraSolver

    User->>UI: Select "Shortest Path"
    UI->>UI: Prompt for source and destination
    User->>UI: Enter "LHR" and "JFK"
    UI->>FNS: shortest_path("LHR", "JFK")
    FNS->>Graph: has_node("LHR")
    Graph-->>FNS: True
    FNS->>Graph: has_node("JFK")
    Graph-->>FNS: True
    FNS->>Dijkstra: compute(graph, "LHR", "JFK")
    Dijkstra->>Graph: get_neighbors("LHR")
    Graph-->>Dijkstra: [("CDG", 340), ("DXB", 5500)]
    Note over Dijkstra: Process priority queue...
    Dijkstra-->>FNS: Path(["LHR","CDG","JFK"], total=6200)
    FNS-->>UI: OperationResult(success, path_display)
    UI-->>User: "LHR -> CDG -> JFK (6200 km)"
```

### Emergency Route Planning

```mermaid
sequenceDiagram
    participant User
    participant UI as Console UI
    participant ERP as EmergencyRoutePlannerService
    participant BT as BacktrackingSolver
    participant Graph as WeightedGraph

    User->>UI: Select "Close Airport"
    User->>UI: Enter "CDG"
    UI->>ERP: close_airport("CDG")
    ERP->>Graph: has_node("CDG")
    Graph-->>ERP: True
    ERP->>ERP: Add "CDG" to closed set
    ERP-->>UI: "CDG marked as closed"

    User->>UI: Select "Find Alternatives"
    User->>UI: Enter source "LHR", dest "DXB"
    UI->>ERP: find_alternatives("LHR", "DXB")
    ERP->>BT: find_all_paths(graph, "LHR", "DXB", {"CDG"})
    Note over BT: Recursive backtracking with visited set
    BT->>Graph: get_neighbors(current)
    Note over BT: Explore all valid paths avoiding CDG
    BT-->>ERP: [Path1, Path2, Path3]
    ERP->>ERP: Mark shortest path
    ERP-->>UI: All routes with shortest labeled
    UI-->>User: Display all alternatives
```

### Priority Queue Passenger Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Console UI
    participant PPS as PassengerPriorityService
    participant Heap as MaxHeap

    User->>UI: Select "Add Passenger"
    UI->>UI: Prompt for name and priority
    User->>UI: "John Smith", "Gold"
    UI->>PPS: add_passenger("John Smith", "Gold")
    PPS->>PPS: Validate priority level
    PPS->>Heap: insert(Passenger, priority=3)
    Note over Heap: Store as (3, -seq, passenger)<br/>Call _sift_up()
    Heap-->>PPS: OperationResult(success)
    PPS-->>UI: "John Smith (Gold) added"
    UI-->>User: Confirmation message
```

---

## Package Dependencies

```mermaid
graph TD
    UI["ui/"] -->|imports| Services["services/"]
    Services -->|imports| Graph["graph/"]
    Services -->|imports| Heap["heap/"]
    Services -->|imports| Queue["queue/"]
    Services -->|imports| Stack["stack/"]
    Services -->|imports| Tree["tree/"]
    Services -->|imports| Hashing["hashing/"]
    Services -->|imports| Sorting["sorting/"]
    Services -->|imports| StringMatch["string_matching/"]
    Services -->|imports| Backtrack["backtracking/"]
    Services -->|imports| Models["models/"]
    Services -->|imports| Utils["utils/"]
    Graph -->|imports| Models
    Heap -->|imports| Models
    Tree -->|imports| Models
    Hashing -->|imports| Models
```

---

## Design Patterns Used

| Pattern | Application | Benefit |
|---------|-------------|---------|
| **Strategy** | MSTAlgorithm, SortAlgorithm interfaces | Swap algorithms at runtime without changing service code |
| **Template Method** | DataStructureBase defining abstract operations | Common interface, specific implementations |
| **Composition** | Services compose data structures | Loose coupling, easy testing |
| **Facade** | Service layer hides data structure complexity | Simple API for UI layer |
| **Result Object** | OperationResult for all operations | Consistent error handling without exceptions |
