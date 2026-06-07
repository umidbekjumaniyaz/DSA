# SkyNet — Global Aviation Logistics & Management System

A Python 3, object-oriented console application demonstrating the design,
implementation, and analysis of classic data structures and algorithms applied
to an aviation logistics domain. Built for **Pearson BTEC HND Unit 26 — Data
Structures & Algorithms**.

The system is organised into five technical phases:

| Phase | Theme | Structures / Algorithms |
| --- | --- | --- |
| 1 | Global navigation & infrastructure | Graph (adjacency list), Dijkstra, Prim & Kruskal (MST) |
| 2 | Passenger priority & logistics | Max-Heap priority queue, FIFO queue, LIFO stack |
| 3 | High-speed search & retrieval | AVL price tree (range search), hash table (PNR records) |
| 4 | Data analytics & string processing | QuickSort, MergeSort, Knuth-Morris-Pratt |
| 5 | Contingency planning | Recursive backtracking path enumeration |

## Requirements

- Python 3.10 or later
- `hypothesis` (only for the property-based test suite — the application itself
  uses only the standard library)

Install the test dependency:

```bash
pip install -r requirements.txt
```

## Running the application

```bash
python main.py
```

You will see a menu spanning all five phases. Choose **option 20** first to load
a small demo network, routes, and prices, then explore the other operations
(cheapest route, backup network, priority check-in, cargo stack, price range
search, schedule sorting comparison, manifest name search, and contingency
re-routing).

## Running the tests

Run the entire suite (unit + property-based):

```bash
python -m unittest discover -s tests
```

Generate a Markdown test report at `docs/Test_Report.md`:

```bash
python -m tests.test_report_generator
```

## Project structure

```
.
├── main.py                  # Entry point: launches the console menu
├── README.md
├── requirements.txt
├── models/                  # Plain domain models (Airport, Route, Passenger, ...)
├── data_structures/         # Encapsulated structures (Graph, MaxHeap, Queue, ...)
├── algorithms/              # Stateless algorithms (Dijkstra, MST, sorting, KMP, ...)
├── services/                # Use-case orchestration + uniform result/error types
├── console/                 # Menu-driven console interface
├── tests/                   # unittest + hypothesis property tests + report generator
└── docs/                    # ADT specs, complexity report, academic report, matrix
```

## Design highlights

- **Encapsulation & information hiding.** Every data structure hides its
  internal state behind name-mangled private attributes and exposes behaviour
  only through public methods.
- **Layered architecture.** Console → services → algorithms/data structures →
  models, with a strict downward-dependency rule.
- **Uniform error handling.** Services return an `OperationResult` carrying an
  `ErrorCode`; the console never terminates on a handled error.
- **Verifiable correctness.** Oracle-based property tests cross-check Dijkstra
  against brute force, QuickSort against MergeSort, Prim against Kruskal, and
  KMP against a naive scan.

## Documentation

The `docs/` folder contains the academic deliverables:

- `adt_specifications.md` — formal ADT specifications (Stack, Queue, Graph)
- `complexity_report.md` — Big-O analysis for every algorithm and structure
- `documentation_report.md` — the 2000–2500 word Harvard-referenced report
- `traceability_matrix.md` — mapping of BTEC criteria P1–P7, M1–M5, D1–D4
- `Test_Report.md` — generated test results
