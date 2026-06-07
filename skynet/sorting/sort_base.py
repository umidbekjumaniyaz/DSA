"""Abstract base class and result types for sorting algorithm implementations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, List


@dataclass
class ComplexityInfo:
    """Algorithm complexity information in Big-O notation.

    Provides theoretical complexity bounds for a sorting algorithm,
    used in the analytics comparison report.

    Attributes:
        best_case: Best-case time complexity (e.g., "O(n log n)").
        average_case: Average-case time complexity (e.g., "O(n log n)").
        worst_case: Worst-case time complexity (e.g., "O(n^2)").
        space: Space complexity (e.g., "O(log n)").
    """

    best_case: str
    average_case: str
    worst_case: str
    space: str


@dataclass
class SortResult:
    """Result of a sort operation with performance metrics.

    Encapsulates the sorted output along with measured performance
    data for algorithm comparison and analytics reporting.

    Attributes:
        sorted_data: The data sorted in ascending order by the key function.
        execution_time_ms: Wall-clock execution time in milliseconds.
        memory_bytes: Peak memory usage during the sort operation in bytes.
        comparisons: Total number of element comparisons performed.
    """

    sorted_data: List[Any]
    execution_time_ms: float
    memory_bytes: int
    comparisons: int


class SortAlgorithm(ABC):
    """Abstract base class for sorting algorithms.

    Defines the common interface for sorting algorithm implementations
    (QuickSort and MergeSort). Enables polymorphic substitution so that
    either algorithm can be used interchangeably through the same
    interface, fulfilling the OOP polymorphism requirement.

    Concrete implementations must provide the sorting logic, algorithm
    name, and complexity information.
    """

    @abstractmethod
    def sort(self, data: List[Any], key_func: Callable[[Any], float]) -> SortResult:
        """Sort the data using the specified key function.

        Args:
            data: The list of elements to sort. Elements can be of any type
                  as long as the key_func can extract a numeric value.
            key_func: A callable that extracts a numeric sort key from each
                      element. Elements are sorted in ascending order of
                      their key values.

        Returns:
            SortResult containing the sorted data and performance metrics
            (execution time, memory usage, and comparison count).
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the sorting algorithm.

        Returns:
            A string identifying this algorithm (e.g., "QuickSort",
            "MergeSort").
        """
        pass

    @abstractmethod
    def get_complexity(self) -> ComplexityInfo:
        """Return complexity information for this algorithm.

        Returns:
            ComplexityInfo containing best, average, and worst-case time
            complexity, as well as space complexity in Big-O notation.
        """
        pass
