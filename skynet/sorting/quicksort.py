"""QuickSort implementation with last-element pivot strategy."""

import time
import tracemalloc
from typing import Any, Callable, List

from skynet.sorting.sort_base import ComplexityInfo, SortAlgorithm, SortResult


class QuickSort(SortAlgorithm):
    """QuickSort algorithm using last-element pivot partitioning.

    Implements in-place QuickSort with the last element chosen as the pivot
    in each partition step. Tracks comparison count, execution time, and
    peak memory usage for performance analytics.

    Inherits from SortAlgorithm abstract base class, enabling polymorphic
    substitution with MergeSort through a common interface.
    """

    def __init__(self) -> None:
        """Initialize QuickSort with comparison counter."""
        self._comparisons: int = 0

    def sort(self, data: List[Any], key_func: Callable[[Any], float]) -> SortResult:
        """Sort data using QuickSort with last-element pivot strategy.

        Args:
            data: The list of elements to sort. Can contain 0 to 10,000 elements.
            key_func: A callable that extracts a numeric sort key from each element.

        Returns:
            SortResult containing sorted data and performance metrics.
        """
        # Handle edge cases
        if len(data) == 0:
            return SortResult(
                sorted_data=[],
                execution_time_ms=0.0,
                memory_bytes=0,
                comparisons=0,
            )

        if len(data) == 1:
            return SortResult(
                sorted_data=list(data),
                execution_time_ms=0.0,
                memory_bytes=0,
                comparisons=0,
            )

        # Make a copy to avoid mutating input
        arr = list(data)
        self._comparisons = 0

        # Measure execution time and memory
        tracemalloc.start()
        start_time = time.perf_counter()

        self._quicksort(arr, 0, len(arr) - 1, key_func)

        end_time = time.perf_counter()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time_ms = (end_time - start_time) * 1000.0

        return SortResult(
            sorted_data=arr,
            execution_time_ms=execution_time_ms,
            memory_bytes=peak_memory,
            comparisons=self._comparisons,
        )

    def get_name(self) -> str:
        """Return the algorithm name.

        Returns:
            The string "QuickSort".
        """
        return "QuickSort"

    def get_complexity(self) -> ComplexityInfo:
        """Return complexity information for QuickSort.

        Returns:
            ComplexityInfo with best O(n log n), average O(n log n),
            worst O(n^2), and space O(log n).
        """
        return ComplexityInfo(
            best_case="O(n log n)",
            average_case="O(n log n)",
            worst_case="O(n²)",
            space="O(log n)",
        )

    def _quicksort(
        self, arr: List[Any], low: int, high: int, key_func: Callable[[Any], float]
    ) -> None:
        """Recursively sort the array using QuickSort.

        Args:
            arr: The list being sorted in-place.
            low: The starting index of the partition.
            high: The ending index of the partition.
            key_func: A callable that extracts a numeric sort key.
        """
        if low < high:
            pivot_index = self._partition(arr, low, high, key_func)
            self._quicksort(arr, low, pivot_index - 1, key_func)
            self._quicksort(arr, pivot_index + 1, high, key_func)

    def _partition(
        self, arr: List[Any], low: int, high: int, key_func: Callable[[Any], float]
    ) -> int:
        """Partition the array around the last element as pivot.

        Elements less than or equal to the pivot are moved to the left side,
        and elements greater than the pivot are moved to the right side.

        Args:
            arr: The list being partitioned in-place.
            low: The starting index of the partition.
            high: The ending index of the partition (pivot position).
            key_func: A callable that extracts a numeric sort key.

        Returns:
            The final index position of the pivot element.
        """
        pivot = key_func(arr[high])  # Last element as pivot
        i = low - 1

        for j in range(low, high):
            self._comparisons += 1
            if key_func(arr[j]) <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
