# Requirements Mapping — Grading Criteria to Code Implementation

## Overview

This document maps each grading criterion (P1–P7, M1–M5, D1–D4) to specific code implementations within the SkyNet Aviation Logistics System.

---

## Pass Criteria (P1–P7)

### P1: Examine Abstract Data Types and Specify ADT Operations

| ADT | Module | Key Operations | Specification |
|-----|--------|----------------|---------------|
| **Graph** | `skynet/graph/weighted_graph.py` | `add_node`, `remove_node`, `add_edge`, `remove_edge`, `get_neighbors`, `display` | Adjacency list representation; bidirectional weighted edges; O(V+E) storage |
| **Max-Heap** | `skynet/heap/max_heap.py` | `insert`, `extract_max`, `peek`, `is_empty`, `size`, `display` | Array-based complete binary tree; parent ≥ children invariant |
| **Queue** | `skynet/queue/fifo_queue.py` | `enqueue`, `dequeue`, `peek`, `contains`, `is_empty`, `size`, `display` | Singly linked list with head/tail pointers; FIFO ordering |
| **Stack** | `skynet/stack/lifo_stack.py` | `push`, `pop`, `peek`, `is_empty`, `size`, `display` | Python list as internal storage; LIFO ordering |
| **AVL Tree** | `skynet/tree/avl_tree.py` | `insert`, `delete`, `search`, `range_search`, `in_order_traversal`, `display` | Self-balancing BST; balance factor ∈ {-1, 0, 1} |
| **Hash Table** | `skynet/hashing/hash_table.py` | `insert`, `delete`, `search`, `update`, `is_empty`, `size`, `display` | Polynomial rolling hash; separate chaining for collisions |

**Abstract Base Class:** `skynet/models/base.py` — `DataStructureBase` defines the common interface (`insert`, `delete`, `search`, `display`, `is_empty`, `size`).

---

### P2: Discuss Algorithms with Pseudocode

| Algorithm | Module | Description |
|-----------|--------|-------------|
| **Dijkstra's Shortest Path** | `skynet/graph/dijkstra.py` | Greedy single-source shortest path using priority queue |
| **Prim's MST** | `skynet/graph/prim.py` | Greedy MST construction growing from start node |
| **Kruskal's MST** | `skynet/graph/kruskal.py` | Edge-sorting MST with Union-Find cycle detection |
| **Heap Insert (Sift-Up)** | `skynet/heap/max_heap.py` | Bubble element upward to restore heap property |
| **Heap Extract-Max (Sift-Down)** | `skynet/heap/max_heap.py` | Replace root with last element, bubble down |
| **AVL Rotations** | `skynet/tree/avl_tree.py` | LL, LR, RR, RL rotation cases for rebalancing |
| **QuickSort** | `skynet/sorting/quicksort.py` | Divide-and-conquer with last-element pivot partitioning |
| **MergeSort** | `skynet/sorting/mergesort.py` | Recursive divide-and-conquer with stable merge |
| **KMP String Matching** | `skynet/string_matching/kmp.py` | Pattern matching using failure function for backtrack avoidance |
| **Recursive Backtracking** | `skynet/backtracking/route_finder.py` | Exhaustive path enumeration with constraint pruning |

Pseudocode for each algorithm is provided in the `ALGORITHM_ANALYSIS.md` document.

---

### P3: Implement Working Data Structures

| Data Structure | File | Implementation Details |
|---------------|------|----------------------|
| Weighted Graph | `skynet/graph/weighted_graph.py` | `Dict[str, List[Tuple[str, int]]]` adjacency list |
| Max-Heap | `skynet/heap/max_heap.py` | `List[Tuple[int, int, Any]]` with (priority, -seq, item) |
| FIFO Queue | `skynet/queue/fifo_queue.py` | Singly linked list with `QueueNode` class |
| LIFO Stack | `skynet/stack/lifo_stack.py` | Python `list` with append/pop from end |
| AVL Tree | `skynet/tree/avl_tree.py` | Node-based tree with `AVLNode` (key, records, left, right, height) |
| Hash Table | `skynet/hashing/hash_table.py` | `List[List[Tuple[str, Any]]]` buckets with separate chaining |
| Union-Find | `skynet/graph/union_find.py` | Dict-based with path compression and union by rank |

---

### P4: Implement Algorithms Using Data Structures

| Algorithm | Data Structure Used | File |
|-----------|-------------------|------|
| Dijkstra's | WeightedGraph + MinHeap (heapq) | `skynet/graph/dijkstra.py` |
| Prim's MST | WeightedGraph + MinHeap (heapq) | `skynet/graph/prim.py` |
| Kruskal's MST | WeightedGraph + UnionFind | `skynet/graph/kruskal.py` |
| Priority Check-in | MaxHeap | `skynet/heap/max_heap.py` |
| Boarding Order | FIFOQueue | `skynet/queue/fifo_queue.py` |
| Cargo Loading | LIFOStack | `skynet/stack/lifo_stack.py` |
| Price Storage | AVLTree | `skynet/tree/avl_tree.py` |
| Record Lookup | HashTable | `skynet/hashing/hash_table.py` |
| Data Sorting | QuickSort / MergeSort | `skynet/sorting/quicksort.py`, `mergesort.py` |
| Text Search | KMP Failure Array | `skynet/string_matching/kmp.py` |
| Route Finding | Backtracking + Graph | `skynet/backtracking/route_finder.py` |

---

### P5: Test Correctness with Example Data

| Test Category | File | Coverage |
|--------------|------|----------|
| Graph Tests | `tests/unit_tests/test_graph.py` | Add/remove nodes/edges, shortest path, MST |
| Heap Tests | `tests/unit_tests/test_heap.py` | Insert, extract in priority order, FIFO among equals |
| Queue Tests | `tests/unit_tests/test_queue.py` | Enqueue/dequeue order, duplicate rejection |
| Stack Tests | `tests/unit_tests/test_stack.py` | Push/pop LIFO order, empty stack handling |
| AVL Tests | `tests/unit_tests/test_avl.py` | Insert, search, range search, rotation cases |
| Hash Tests | `tests/unit_tests/test_hash_table.py` | CRUD operations, collision handling |
| Sorting Tests | `tests/unit_tests/test_sorting.py` | Correctness, identical output, empty/single element |
| KMP Tests | `tests/unit_tests/test_kmp.py` | Pattern matching, failure function, no-match |
| Backtracking Tests | `tests/unit_tests/test_backtracking.py` | Path finding, closed airports, no alternatives |

---

### P6: Evaluate Implementations Against Requirements

Each implementation is evaluated against its specific requirements:

| Requirement | Implementation | Evaluation |
|-------------|---------------|------------|
| Req 1 (Graph) | WeightedGraph with bidirectional edges | All 10 acceptance criteria met: add/remove/display with validation |
| Req 2 (Dijkstra) | Priority queue-based implementation | All 5 criteria met: shortest path, no-path, invalid node handling |
| Req 3 (MST) | Prim's + Kruskal's implementations | All 6 criteria met: correct MST, disconnected detection, cost equality |
| Req 4 (Priority) | MaxHeap with stable ordering | All 7 criteria met: priority extraction, FIFO within priority |
| Req 5 (Queue) | Linked-list FIFOQueue | All 7 criteria met: FIFO order, duplicate rejection |
| Req 6 (Stack) | Array-based LIFOStack | All 8 criteria met: LIFO order, empty handling |
| Req 7 (AVL) | Self-balancing AVL tree | All 8 criteria met: balanced operations, range search |
| Req 8 (Hash) | Separate chaining hash table | All 9 criteria met: O(1) average CRUD, collision handling |
| Req 9 (Sorting) | QuickSort + MergeSort | All 9 criteria met: correct sorting, performance metrics |
| Req 10 (KMP) | Failure function + search | All 7 criteria met: O(n+m) matching, case-insensitive |
| Req 11 (Backtracking) | Recursive path finder | All 8 criteria met: all paths found, closed node exclusion |

---

### P7: Compare Different Implementations

| Comparison | Implementation A | Implementation B | Key Differences |
|-----------|-----------------|-----------------|-----------------|
| MST Algorithms | Prim's (vertex-growing) | Kruskal's (edge-sorting) | Prim's: O(E log V) with heap; Kruskal's: O(E log E) with sorting |
| Sorting | QuickSort (in-place, unstable) | MergeSort (extra space, stable) | QuickSort: O(n²) worst; MergeSort: O(n log n) guaranteed |
| Route Finding | Dijkstra's (optimal single path) | Backtracking (all paths) | Dijkstra: O((V+E) log V); Backtracking: O(V!) worst |

---

## Merit Criteria (M1–M5)

### M1: Illustrate Operations with Step-by-Step Walkthroughs

Covered in `merit_criteria.md` with walkthroughs for:
- Dijkstra's algorithm on a 5-airport network
- Prim's MST construction step-by-step
- MaxHeap insert and extract sequences
- AVL tree insertion with rotation triggers
- QuickSort partitioning on sample data
- KMP failure function computation and search execution

### M2: Determine Time Complexity with Justification

| Algorithm | Best | Average | Worst | Justification Location |
|-----------|------|---------|-------|----------------------|
| Dijkstra | O((V+E) log V) | O((V+E) log V) | O((V+E) log V) | `merit_criteria.md` §M2 |
| Prim's | O(E log V) | O(E log V) | O(E log V) | `merit_criteria.md` §M2 |
| Kruskal's | O(E log E) | O(E log E) | O(E log E) | `merit_criteria.md` §M2 |
| Heap Insert | O(1) | O(log n) | O(log n) | `merit_criteria.md` §M2 |
| Heap Extract | O(log n) | O(log n) | O(log n) | `merit_criteria.md` §M2 |
| AVL Insert | O(log n) | O(log n) | O(log n) | `merit_criteria.md` §M2 |
| QuickSort | O(n log n) | O(n log n) | O(n²) | `merit_criteria.md` §M2 |
| MergeSort | O(n log n) | O(n log n) | O(n log n) | `merit_criteria.md` §M2 |
| KMP | O(n + m) | O(n + m) | O(n + m) | `merit_criteria.md` §M2 |
| Backtracking | O(V + E) | Exponential | O(V!) | `merit_criteria.md` §M2 |
| Hash Lookup | O(1) | O(1) | O(n) | `merit_criteria.md` §M2 |

### M3: Determine Space Complexity with Justification

| Algorithm/Structure | Space Complexity | Justification |
|--------------------|-----------------|---------------|
| WeightedGraph | O(V + E) | Adjacency list stores V node entries + E edge entries |
| Dijkstra | O(V) | Distance/predecessor arrays + priority queue |
| Prim's/Kruskal's | O(V + E) | Edge list/heap + visited set |
| MaxHeap | O(n) | Array storage of n elements |
| FIFOQueue | O(n) | n linked list nodes |
| LIFOStack | O(n) | Array of n elements |
| AVL Tree | O(n) | n tree nodes with height metadata |
| Hash Table | O(n + m) | m buckets + n entries |
| QuickSort | O(log n) | Recursion stack depth |
| MergeSort | O(n) | Temporary arrays during merge |
| KMP | O(m) | Failure function array |
| Backtracking | O(V) | Recursion stack + visited set |

### M4: Compare Algorithm Efficiency Empirically

Empirical comparisons performed in `distinction_criteria.md` using datasets of size 100, 1,000, and 10,000:
- QuickSort vs MergeSort: execution time and memory
- Prim's vs Kruskal's: MST computation on varying graph densities
- Dijkstra vs Backtracking: single shortest path vs all paths

### M5: Discuss Trade-offs Between Implementations

| Comparison | Trade-off Discussion |
|-----------|---------------------|
| QuickSort vs MergeSort | QuickSort: better cache locality, in-place (O(log n) space), but O(n²) worst case. MergeSort: guaranteed O(n log n), stable, but O(n) extra space. |
| Prim's vs Kruskal's | Prim's: better for dense graphs (E ≈ V²). Kruskal's: better for sparse graphs; needs Union-Find. |
| AVL Tree vs Hash Table | AVL: O(log n) guaranteed, supports range queries, ordered traversal. Hash: O(1) average, no ordering, degrades with poor hash function. |
| Linked Queue vs Array Queue | Linked: O(1) enqueue/dequeue without resizing. Array: better cache locality but needs circular buffer or resizing. |

---

## Distinction Criteria (D1–D4)

### D1: Evaluate Efficiency of Complex Data Structures

Formal analysis covered in `distinction_criteria.md` for:
- **AVL Tree**: Height bounded by 1.44 log₂(n), guaranteeing O(log n) operations
- **Weighted Graph**: Adjacency list analysis — O(V+E) space, O(degree) edge queries
- **Hash Table**: Load factor analysis, expected chain length, amortized O(1)

### D2: Compare Asymptotic Complexity Between Algorithm Pairs

| Algorithm Pair | Complexity Comparison | Winner (Context) |
|---------------|----------------------|-----------------|
| QuickSort vs MergeSort | O(n log n) avg vs O(n log n) always | MergeSort (worst-case guarantee); QuickSort (practical average + space) |
| Prim's vs Kruskal's | O(E log V) vs O(E log E) | Prim's (dense); Kruskal's (sparse, with α(V) union-find) |
| Dijkstra vs Backtracking | O((V+E) log V) vs O(V!) | Dijkstra (single optimal); Backtracking (all paths needed) |

### D3: Assess Algorithmic Effectiveness Using Empirical Measurement

Performance measurement methodology:
- **Datasets**: 100, 1,000, and 10,000 records
- **Metrics**: Execution time (ms), peak memory (bytes), comparison count
- **Tool**: `skynet/utils/performance.py` timing decorator and memory measurement
- **Results**: Tabulated in `distinction_criteria.md` §D3

### D4: Critically Evaluate Relationship Between Data Structures and Algorithms

Analysis covered in `distinction_criteria.md` examining:
- How graph representation (adjacency list vs matrix) affects Dijkstra/Prim/Kruskal performance
- How heap implementation choice affects priority queue-based algorithms
- How hash function quality impacts lookup performance
- How AVL balancing overhead relates to query workload patterns
- How sorting algorithm choice depends on data characteristics (size, pre-sortedness, stability needs)
