"""MergeSort implementation with divide-and-conquer strategy."""

import time
import tracemalloc
from typing import Any, Callable, List

from skynet.sorting.sort_base import ComplexityInfo, SortAlgorithm, SortResult


class MergeSort(SortAlgorithm):
    """MergeSort algorithm using recursive divide-and-conquer.

    Implements stable MergeSort that recursively divides the array in half
    until single elements remain, then merges sorted halves back together.
    Tracks comparison count, execution time, and peak memory usage for
    performance analytics.

    Inherits from SortAlgorithm abstract base class, enabling polymorphic
    substitution with QuickSort through a common interface.
    """

    def __init__(self) -> None:
        """Initialize MergeSort with comparison counter."""
        self._comparisons: int = 0

    def sort(self, data: List[Any], key_func: Callable[[Any], float]) -> SortResult:
        """Sort data using MergeSort with divide-and-conquer strategy.

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

        sorted_arr = self._mergesort(arr, key_func)

        end_time = time.perf_counter()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time_ms = (end_time - start_time) * 1000.0

        return SortResult(
            sorted_data=sorted_arr,
            execution_time_ms=execution_time_ms,
            memory_bytes=peak_memory,
            comparisons=self._comparisons,
        )

    def get_name(self) -> str:
        """Return the algorithm name.

        Returns:
            The string "MergeSort".
        """
        return "MergeSort"

    def get_complexity(self) -> ComplexityInfo:
        """Return complexity information for MergeSort.

        Returns:
            ComplexityInfo with best O(n log n), average O(n log n),
            worst O(n log n), and space O(n).
        """
        return ComplexityInfo(
            best_case="O(n log n)",
            average_case="O(n log n)",
            worst_case="O(n log n)",
            space="O(n)",
        )

    def _mergesort(
        self, arr: List[Any], key_func: Callable[[Any], float]
    ) -> List[Any]:
        """Recursively sort the array using divide-and-conquer.

        Splits the array in half until single elements remain, then
        merges the sorted halves back together.

        Args:
            arr: The list to sort.
            key_func: A callable that extracts a numeric sort key.

        Returns:
            A new sorted list.
        """
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self._mergesort(arr[:mid], key_func)
        right = self._mergesort(arr[mid:], key_func)
        return self._merge(left, right, key_func)

    def _merge(
        self,
        left: List[Any],
        right: List[Any],
        key_func: Callable[[Any], float],
    ) -> List[Any]:
        """Merge two sorted lists into a single sorted list.

        Compares elements from the front of each list, appending the
        smaller element to the result. Tracks comparisons for analytics.

        Args:
            left: The sorted left half.
            right: The sorted right half.
            key_func: A callable that extracts a numeric sort key.

        Returns:
            A merged sorted list containing all elements from both halves.
        """
        result: List[Any] = []
        i = j = 0

        while i < len(left) and j < len(right):
            self._comparisons += 1
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result
