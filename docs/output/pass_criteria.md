# Pass Criteria (P1–P7) — SkyNet Aviation Logistics

---

## P1: Examine Abstract Data Types and Specify ADT Operations

### 1.1 Graph ADT

**Definition**: A Graph is an abstract data type consisting of a finite set of vertices (nodes) and a collection of edges connecting pairs of vertices. In SkyNet, we use a weighted undirected graph where vertices represent airports and edges represent flight routes with distance weights.

**ADT Specification:**
```
ADT WeightedGraph:
    Data:
        - Set of vertices V (airport nodes identified by IATA codes)
        - Set of edges E ⊆ V × V × ℤ⁺ (bidirectional weighted connections)
    
    Operations:
        add_node(airport: Airport) → OperationResult
            Pre: airport.iata_code is valid 3-letter uppercase string
            Post: airport added to V; |V| increases by 1
            Error: if iata_code already exists in V
        
        remove_node(iata_code: String) → OperationResult
            Pre: iata_code exists in V
            Post: node removed from V; all edges involving node removed from E
            Error: if iata_code not in V
        
        add_edge(src: String, dest: String, weight: Integer) → OperationResult
            Pre: src ∈ V, dest ∈ V, 1 ≤ weight ≤ 99999
            Post: bidirectional edge (src, dest, weight) added to E
            Error: if src or dest not in V
        
        remove_edge(src: String, dest: String) → OperationResult
            Pre: edge (src, dest) exists in E
            Post: edge removed from E; both nodes preserved in V
            Error: if edge does not exist
        
        get_neighbors(iata_code: String) → List[Tuple[String, Integer]]
            Pre: iata_code ∈ V
            Post: returns list of (neighbor, weight) pairs
        
        display() → String
            Post: returns adjacency list representation of entire graph
        
        is_empty() → Boolean
            Post: returns True if |V| = 0
        
        node_count() → Integer
            Post: returns |V|
        
        edge_count() → Integer
            Post: returns |E|
```

### 1.2 Max-Heap ADT (Priority Queue)

**Definition**: A Max-Heap is a complete binary tree where every parent node has a value greater than or equal to its children. It efficiently supports insertion and extraction of the maximum element.

**ADT Specification:**
```
ADT MaxHeap:
    Data:
        - Array H[0..n-1] of elements ordered by priority
        - Each element: (priority_value, sequence_number, item)
        - Invariant: H[parent(i)] ≥ H[i] for all valid i
    
    Operations:
        insert(item: Any, priority: Integer) → OperationResult
            Pre: priority ∈ {1, 2, 3, 4} (Economy, Silver, Gold, Platinum)
            Post: item added; heap property maintained
            Error: if priority is invalid
        
        extract_max() → OperationResult
            Pre: heap is not empty
            Post: removes and returns element with highest priority
                  (FIFO among equal priorities)
            Error: if heap is empty
        
        peek() → OperationResult
            Pre: heap is not empty
            Post: returns max element WITHOUT removal; heap unchanged
            Error: if heap is empty
        
        is_empty() → Boolean
            Post: returns True if n = 0
        
        size() → Integer
            Post: returns n (number of elements)
        
        display() → String
            Post: returns string representation showing all elements
```

### 1.3 Queue ADT (FIFO)

**Definition**: A Queue is a linear data structure following First-In-First-Out (FIFO) ordering. Elements are added at the rear and removed from the front.

**ADT Specification:**
```
ADT FIFOQueue:
    Data:
        - Linked list of QueueNode elements
        - head: pointer to front (dequeue end)
        - tail: pointer to rear (enqueue end)
        - members: set of identifiers for duplicate detection
    
    Operations:
        enqueue(item: Any, identifier: String) → OperationResult
            Pre: identifier not already in members
            Post: item added at tail; size increases by 1
            Error: if identifier already exists (duplicate)
        
        dequeue() → OperationResult
            Pre: queue is not empty
            Post: removes and returns front element; size decreases by 1
            Error: if queue is empty
        
        peek() → OperationResult
            Pre: queue is not empty
            Post: returns front element without removal
            Error: if queue is empty
        
        contains(identifier: String) → Boolean
            Post: returns True if identifier in members set
        
        is_empty() → Boolean
            Post: returns True if size = 0
        
        size() → Integer
            Post: returns number of elements
        
        display() → String
            Post: returns all elements from front to rear with positions
```

### 1.4 Stack ADT (LIFO)

**Definition**: A Stack is a linear data structure following Last-In-First-Out (LIFO) ordering. Elements are added and removed only from the top.

**ADT Specification:**
```
ADT LIFOStack:
    Data:
        - Array items[0..n-1]
        - Top of stack at index n-1
    
    Operations:
        push(item: Any) → OperationResult
            Pre: none
            Post: item added at top; size increases by 1
        
        pop() → OperationResult
            Pre: stack is not empty
            Post: removes and returns top element; size decreases by 1
            Error: if stack is empty
        
        peek() → OperationResult
            Pre: stack is not empty
            Post: returns top element without removal
            Error: if stack is empty
        
        is_empty() → Boolean
            Post: returns True if n = 0
        
        size() → Integer
            Post: returns n
        
        display() → String
            Post: returns all items from top to bottom
```

### 1.5 AVL Tree ADT (Self-Balancing BST)

**Definition**: An AVL Tree is a self-balancing binary search tree where the height difference between left and right subtrees of any node is at most 1. This guarantees O(log n) operations.

**ADT Specification:**
```
ADT AVLTree:
    Data:
        - Root node of binary tree
        - Each node: (key, records[], left, right, height)
        - BST property: left.key < node.key < right.key
        - Balance property: |height(left) - height(right)| ≤ 1 for all nodes
    
    Operations:
        insert(record: PriceRecord) → OperationResult
            Pre: record has valid price value
            Post: record inserted at correct position; tree rebalanced
                  (duplicate keys stored as separate entries in same node)
        
        delete(price: Float) → OperationResult
            Pre: price exists in tree
            Post: node removed; tree rebalanced
            Error: if price not found
        
        search(price: Float) → OperationResult
            Pre: none
            Post: returns record if found; error message if not found
        
        range_search(min: Float, max: Float) → OperationResult
            Pre: min ≤ max
            Post: returns all records where min ≤ price ≤ max
        
        in_order_traversal() → List[PriceRecord]
            Post: returns all records in ascending price order
        
        display() → String
            Post: returns visual tree representation
```

### 1.6 Hash Table ADT

**Definition**: A Hash Table is a data structure that maps keys to values using a hash function. Collisions (multiple keys mapping to the same bucket) are resolved using separate chaining.

**ADT Specification:**
```
ADT HashTable:
    Data:
        - Array buckets[0..m-1] of linked lists
        - Each entry: (key, value) pair
        - hash_function: key → [0, m-1]
    
    Operations:
        insert(key: String, value: Any) → OperationResult
            Pre: key is valid (non-empty, alphanumeric)
            Post: (key, value) stored in buckets[hash(key)]
            Error: if key already exists (duplicate)
        
        delete(key: String) → OperationResult
            Pre: key exists in table
            Post: entry removed from bucket
            Error: if key not found
        
        search(key: String) → OperationResult
            Pre: none
            Post: returns value if key found; error if not
        
        update(key: String, value: Any) → OperationResult
            Pre: key exists in table
            Post: value associated with key is updated
            Error: if key not found
        
        is_empty() → Boolean
            Post: returns True if no entries stored
        
        size() → Integer
            Post: returns total number of entries
        
        display() → String
            Post: returns bucket structure showing indices and chains
```

---

## P2: Discuss Algorithms with Pseudocode

### 2.1 Dijkstra's Shortest Path

**Purpose**: Find the shortest path between a source and destination in a weighted graph with non-negative weights.

**Approach**: Greedy algorithm using a priority queue to always process the closest unvisited node.

```pseudocode
ALGORITHM Dijkstra(graph, source, destination):
    // Initialize distances to infinity
    FOR each node in graph:
        dist[node] ← INFINITY
        prev[node] ← NULL
    
    dist[source] ← 0
    priority_queue ← new MinHeap()
    priority_queue.INSERT((0, source))
    
    WHILE priority_queue is NOT empty:
        (current_dist, current) ← priority_queue.EXTRACT_MIN()
        
        IF current = destination:
            BREAK  // Found shortest path
        
        IF current_dist > dist[current]:
            CONTINUE  // Skip outdated entry
        
        FOR each (neighbor, weight) in graph.GET_NEIGHBORS(current):
            new_dist ← dist[current] + weight
            IF new_dist < dist[neighbor]:
                dist[neighbor] ← new_dist
                prev[neighbor] ← current
                priority_queue.INSERT((new_dist, neighbor))
    
    // Reconstruct path
    IF dist[destination] = INFINITY:
        RETURN "No path exists"
    
    path ← empty list
    node ← destination
    WHILE node ≠ NULL:
        path.PREPEND(node)
        node ← prev[node]
    
    RETURN (path, dist[destination])
```

### 2.2 Prim's MST

**Purpose**: Find the minimum spanning tree starting from a given node, growing the tree by adding the minimum-weight edge connecting the tree to an unvisited node.

```pseudocode
ALGORITHM PrimMST(graph, start_node):
    mst_edges ← empty list
    visited ← {start_node}
    edge_heap ← new MinHeap()
    
    // Add all edges from start node
    FOR each (neighbor, weight) in graph.GET_NEIGHBORS(start_node):
        edge_heap.INSERT((weight, start_node, neighbor))
    
    WHILE edge_heap is NOT empty AND |visited| < graph.NODE_COUNT():
        (weight, src, dest) ← edge_heap.EXTRACT_MIN()
        
        IF dest ∈ visited:
            CONTINUE  // Skip - would create cycle
        
        visited.ADD(dest)
        mst_edges.APPEND((src, dest, weight))
        
        // Add edges from newly visited node
        FOR each (neighbor, w) in graph.GET_NEIGHBORS(dest):
            IF neighbor ∉ visited:
                edge_heap.INSERT((w, dest, neighbor))
    
    IF |visited| < graph.NODE_COUNT():
        RETURN "Graph is disconnected"
    
    total_cost ← SUM of weights in mst_edges
    RETURN MSTResult(mst_edges, total_cost)
```

### 2.3 Kruskal's MST

**Purpose**: Find MST by sorting all edges and greedily adding the cheapest edge that doesn't form a cycle.

```pseudocode
ALGORITHM KruskalMST(graph):
    edges ← graph.GET_ALL_EDGES()
    SORT edges BY weight ASCENDING
    
    uf ← new UnionFind()
    FOR each node in graph.GET_ALL_NODES():
        uf.MAKE_SET(node)
    
    mst_edges ← empty list
    
    FOR each (src, dest, weight) in edges:
        IF uf.FIND(src) ≠ uf.FIND(dest):
            uf.UNION(src, dest)
            mst_edges.APPEND((src, dest, weight))
        
        IF |mst_edges| = graph.NODE_COUNT() - 1:
            BREAK  // MST complete
    
    IF |mst_edges| < graph.NODE_COUNT() - 1:
        RETURN "Graph is disconnected"
    
    total_cost ← SUM of weights in mst_edges
    RETURN MSTResult(mst_edges, total_cost)
```

### 2.4 Heap Insert (Sift-Up)

```pseudocode
ALGORITHM HeapInsert(heap, item, priority):
    sequence ← heap.next_sequence()
    entry ← (priority, -sequence, item)
    heap.array.APPEND(entry)
    index ← |heap.array| - 1
    
    // Sift up to restore heap property
    WHILE index > 0:
        parent ← (index - 1) / 2
        IF heap.array[index] > heap.array[parent]:
            SWAP(heap.array[index], heap.array[parent])
            index ← parent
        ELSE:
            BREAK
    
    RETURN success
```

### 2.5 Heap Extract-Max (Sift-Down)

```pseudocode
ALGORITHM HeapExtractMax(heap):
    IF heap is empty:
        RETURN "No elements in heap"
    
    max_item ← heap.array[0]
    last ← heap.array.POP()  // Remove last element
    
    IF heap is NOT empty:
        heap.array[0] ← last
        
        // Sift down to restore heap property
        index ← 0
        WHILE TRUE:
            largest ← index
            left ← 2 * index + 1
            right ← 2 * index + 2
            
            IF left < |heap.array| AND heap.array[left] > heap.array[largest]:
                largest ← left
            IF right < |heap.array| AND heap.array[right] > heap.array[largest]:
                largest ← right
            
            IF largest = index:
                BREAK
            
            SWAP(heap.array[index], heap.array[largest])
            index ← largest
    
    RETURN max_item[2]  // Return the stored item
```

### 2.6 AVL Insert with Rebalancing

```pseudocode
ALGORITHM AVLInsert(tree, record):
    tree.root ← _insert_recursive(tree.root, record)
    
FUNCTION _insert_recursive(node, record):
    IF node is NULL:
        RETURN new AVLNode(key=record.price, records=[record])
    
    IF record.price < node.key:
        node.left ← _insert_recursive(node.left, record)
    ELSE IF record.price > node.key:
        node.right ← _insert_recursive(node.right, record)
    ELSE:
        node.records.APPEND(record)  // Duplicate key
        RETURN node
    
    // Update height
    node.height ← 1 + MAX(HEIGHT(node.left), HEIGHT(node.right))
    
    // Check balance and rotate if needed
    balance ← HEIGHT(node.left) - HEIGHT(node.right)
    
    IF balance > 1 AND record.price < node.left.key:    // LL
        RETURN rotate_right(node)
    IF balance > 1 AND record.price > node.left.key:    // LR
        node.left ← rotate_left(node.left)
        RETURN rotate_right(node)
    IF balance < -1 AND record.price > node.right.key:  // RR
        RETURN rotate_left(node)
    IF balance < -1 AND record.price < node.right.key:  // RL
        node.right ← rotate_right(node.right)
        RETURN rotate_left(node)
    
    RETURN node
```

### 2.7 QuickSort

```pseudocode
ALGORITHM QuickSort(arr, low, high, key_func):
    IF low < high:
        pivot_index ← PARTITION(arr, low, high, key_func)
        QuickSort(arr, low, pivot_index - 1, key_func)
        QuickSort(arr, pivot_index + 1, high, key_func)

FUNCTION PARTITION(arr, low, high, key_func):
    pivot ← key_func(arr[high])  // Last element as pivot
    i ← low - 1
    
    FOR j ← low TO high - 1:
        IF key_func(arr[j]) ≤ pivot:
            i ← i + 1
            SWAP(arr[i], arr[j])
    
    SWAP(arr[i + 1], arr[high])
    RETURN i + 1
```

### 2.8 MergeSort

```pseudocode
ALGORITHM MergeSort(arr, key_func):
    IF |arr| ≤ 1:
        RETURN arr
    
    mid ← |arr| / 2
    left ← MergeSort(arr[0..mid-1], key_func)
    right ← MergeSort(arr[mid..end], key_func)
    RETURN MERGE(left, right, key_func)

FUNCTION MERGE(left, right, key_func):
    result ← empty list
    i ← 0, j ← 0
    
    WHILE i < |left| AND j < |right|:
        IF key_func(left[i]) ≤ key_func(right[j]):
            result.APPEND(left[i])
            i ← i + 1
        ELSE:
            result.APPEND(right[j])
            j ← j + 1
    
    result.EXTEND(left[i..end])
    result.EXTEND(right[j..end])
    RETURN result
```

### 2.9 KMP String Matching

```pseudocode
ALGORITHM KMPSearch(text, pattern):
    failure ← COMPUTE_FAILURE(pattern)
    matches ← empty list
    j ← 0  // Pattern index
    
    FOR i ← 0 TO |text| - 1:
        WHILE j > 0 AND text[i] ≠ pattern[j]:
            j ← failure[j - 1]
        
        IF text[i] = pattern[j]:
            j ← j + 1
        
        IF j = |pattern|:
            matches.APPEND(i - |pattern| + 1)
            j ← failure[j - 1]
    
    RETURN matches

FUNCTION COMPUTE_FAILURE(pattern):
    failure ← array of zeros, length |pattern|
    j ← 0
    
    FOR i ← 1 TO |pattern| - 1:
        WHILE j > 0 AND pattern[i] ≠ pattern[j]:
            j ← failure[j - 1]
        IF pattern[i] = pattern[j]:
            j ← j + 1
        failure[i] ← j
    
    RETURN failure
```

### 2.10 Recursive Backtracking

```pseudocode
ALGORITHM FindAllPaths(graph, source, destination, excluded):
    all_paths ← empty list
    visited ← {source}
    path ← [source]
    BACKTRACK(graph, source, destination, path, visited, excluded, all_paths)
    RETURN all_paths

FUNCTION BACKTRACK(graph, current, destination, path, visited, excluded, all_paths):
    IF current = destination:
        all_paths.APPEND(COPY(path))
        RETURN
    
    FOR each (neighbor, weight) in graph.GET_NEIGHBORS(current):
        IF neighbor ∉ visited AND neighbor ∉ excluded:
            visited.ADD(neighbor)
            path.APPEND(neighbor)
            
            BACKTRACK(graph, neighbor, destination, path, visited, excluded, all_paths)
            
            path.REMOVE_LAST()     // Backtrack
            visited.REMOVE(neighbor)  // Backtrack
```

---

## P3: Implement Working Data Structures

All data structures are implemented in pure Python without external libraries. See the following source files:

| Data Structure | Source File | Lines of Code |
|---------------|-------------|---------------|
| Weighted Graph | `skynet/graph/weighted_graph.py` | ~150 |
| Max-Heap | `skynet/heap/max_heap.py` | ~120 |
| FIFO Queue | `skynet/queue/fifo_queue.py` | ~100 |
| LIFO Stack | `skynet/stack/lifo_stack.py` | ~80 |
| AVL Tree | `skynet/tree/avl_tree.py` | ~250 |
| Hash Table | `skynet/hashing/hash_table.py` | ~130 |
| Union-Find | `skynet/graph/union_find.py` | ~50 |

Each implementation:
- Extends `DataStructureBase` (or `MSTAlgorithm`/`SortAlgorithm` where appropriate)
- Uses private internal storage (prefixed with `_`)
- Returns `OperationResult` for all public operations
- Includes docstrings describing purpose and complexity

---

## P4: Implement Algorithms Using Data Structures

Each algorithm leverages appropriate data structures:

| Algorithm | Primary Data Structure | Support Structure | File |
|-----------|----------------------|-------------------|------|
| Dijkstra's | WeightedGraph | heapq (min-heap) | `skynet/graph/dijkstra.py` |
| Prim's MST | WeightedGraph | heapq (min-heap) | `skynet/graph/prim.py` |
| Kruskal's MST | WeightedGraph | UnionFind | `skynet/graph/kruskal.py` |
| Priority Processing | MaxHeap | — | `skynet/heap/max_heap.py` |
| QuickSort | Array (in-place) | — | `skynet/sorting/quicksort.py` |
| MergeSort | Array (recursive) | Temp arrays | `skynet/sorting/mergesort.py` |
| KMP Search | Failure array | — | `skynet/string_matching/kmp.py` |
| Backtracking | Graph + Set | Recursion stack | `skynet/backtracking/route_finder.py` |

---

## P5: Test Correctness with Example Data

Testing demonstrates correctness across all subsystems. Example test scenarios:

**Graph**: Add airports LHR, CDG, JFK; add routes; verify shortest path LHR→JFK returns correct distance  
**Heap**: Insert Platinum, Gold, Economy passengers; verify extraction order  
**Queue**: Enqueue A, B, C; dequeue verifies A first  
**Stack**: Push X, Y, Z; pop verifies Z first  
**AVL**: Insert prices 500, 300, 700, 100; verify balance maintained  
**Hash**: Insert PNR "ABC123"; search returns correct record  
**Sorting**: Sort [5,3,8,1,9]; both algorithms produce [1,3,5,8,9]  
**KMP**: Search "SMITH" in "JOHN SMITH"; returns match at position 5  
**Backtracking**: Find all paths LHR→JFK avoiding closed CDG

Test files: `tests/unit_tests/test_*.py`

---

## P6: Evaluate Implementations Against Requirements

Each implementation satisfies its acceptance criteria:

1. **Graph (Req 1)**: All 10 criteria met — add/remove nodes/edges with validation and error handling
2. **Dijkstra (Req 2)**: All 5 criteria met — shortest path with priority queue processing
3. **MST (Req 3)**: All 6 criteria met — both algorithms produce correct MST, handle disconnected graphs
4. **Heap (Req 4)**: All 7 criteria met — priority ordering with FIFO stability
5. **Queue (Req 5)**: All 7 criteria met — FIFO with duplicate rejection
6. **Stack (Req 6)**: All 8 criteria met — LIFO with empty-stack handling
7. **AVL (Req 7)**: All 8 criteria met — balanced operations with range search
8. **Hash (Req 8)**: All 9 criteria met — O(1) average CRUD with collision handling
9. **Sorting (Req 9)**: All 9 criteria met — correct output, identical results, performance metrics
10. **KMP (Req 10)**: All 7 criteria met — O(n+m) case-insensitive matching
11. **Backtracking (Req 11)**: All 8 criteria met — all paths found excluding closed airports

---

## P7: Compare Different Implementations

### QuickSort vs MergeSort

| Criterion | QuickSort | MergeSort |
|-----------|-----------|-----------|
| Best Case | O(n log n) | O(n log n) |
| Average Case | O(n log n) | O(n log n) |
| Worst Case | O(n²) | O(n log n) |
| Space | O(log n) in-place | O(n) auxiliary |
| Stability | Unstable | Stable |
| Cache Performance | Excellent (sequential access) | Good (sequential merge) |
| Practical Speed | Often faster due to low overhead | Consistent but higher overhead |

**Conclusion**: QuickSort preferred for general-purpose sorting where average performance matters; MergeSort preferred when worst-case guarantees or stability are required.

### Prim's vs Kruskal's MST

| Criterion | Prim's | Kruskal's |
|-----------|--------|-----------|
| Complexity | O(E log V) | O(E log E) |
| Approach | Vertex-growing (greedy) | Edge-sorting (greedy) |
| Best For | Dense graphs (E ≈ V²) | Sparse graphs (E ≈ V) |
| Data Structure | Min-heap | Sorted edge list + Union-Find |
| Starting Point | Requires start node | No start node needed |
| Parallelism | Sequential by nature | Edge sorting parallelizable |

**Conclusion**: Both produce identical MST costs (proven by Property 6). Prim's is more efficient for dense graphs; Kruskal's is simpler and better for sparse graphs.

### Dijkstra's vs Backtracking

| Criterion | Dijkstra's | Backtracking |
|-----------|-----------|--------------|
| Purpose | Single shortest path | All possible paths |
| Complexity | O((V+E) log V) | O(V!) worst case |
| Optimality | Guaranteed shortest | Finds all (including shortest) |
| Use Case | Optimal routing | Emergency alternatives |
| Approach | Greedy (never revisits) | Exhaustive (explores everything) |

**Conclusion**: Dijkstra's for efficiency when only the optimal path is needed; Backtracking when all alternatives must be enumerated (emergency scenarios).
