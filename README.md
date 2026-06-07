# SkyNet - Global Aviation Logistics & Management System

A modular Python 3.11 console application implementing nine interconnected aviation logistics subsystems, each showcasing specific data structures and algorithms. Designed for an HNC/HND Data Structures and Algorithms unit targeting Distinction grade.

## Subsystems

1. **Flight Network System** - Weighted graph with Dijkstra's shortest path, Prim's and Kruskal's MST
2. **Passenger Priority System** - Max-heap priority queue for check-in ordering
3. **Boarding Gate System** - FIFO queue for sequential boarding management
4. **Cargo Management System** - LIFO stack for cargo loading/unloading
5. **Flight Price Database** - AVL tree for balanced price storage and range queries
6. **Passenger Registry** - Hash table with separate chaining for record management
7. **Analytics System** - QuickSort and MergeSort with performance comparison
8. **Passenger Search System** - KMP string matching for pattern-based lookups
9. **Emergency Route Planner** - Recursive backtracking for alternative route discovery

## Architecture

- **Pure Python** - All data structures built from scratch; no external DS libraries
- **Service Layer Pattern** - Business logic separated from data structure internals
- **Abstract Base Classes** - Common interfaces enabling polymorphic substitution
- **Comprehensive Testing** - Unit tests, property-based tests (Hypothesis), and integration tests

## Getting Started

### Prerequisites

- Python 3.11+

### Installation

```bash
pip install -e ".[dev]"
```

### Running the Application

```bash
skynet
```

### Running Tests

```bash
pytest
```

## Project Structure

```
skynet/           # Main application package
tests/            # Test suite (unit, property, integration)
docs/             # Academic documentation and templates
```
