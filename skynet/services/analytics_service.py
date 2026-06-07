"""Analytics service for sorting algorithm comparison and reporting."""

from typing import Any, Callable, List

from skynet.sorting import QuickSort, MergeSort
from skynet.sorting.sort_base import SortResult
from skynet.utils.formatters import format_table


class AnalyticsService:
    """Service providing sorting analytics and algorithm comparison.

    Composes QuickSort and MergeSort algorithm instances to provide
    sorting operations and performance comparison reports. Demonstrates
    polymorphic substitution through the common SortAlgorithm interface.

    Attributes:
        _quicksort: QuickSort algorithm instance.
        _mergesort: MergeSort algorithm instance.
    """

    def __init__(self) -> None:
        """Initialize AnalyticsService with QuickSort and MergeSort instances."""
        self._quicksort = QuickSort()
        self._mergesort = MergeSort()

    def sort_with_quicksort(self, data: List[Any], key_func: Callable[[Any], float]) -> SortResult:
        """Sort data using QuickSort algorithm.

        Args:
            data: The list of elements to sort (0 to 10,000 elements).
            key_func: A callable that extracts a numeric sort key from each element.

        Returns:
            SortResult containing sorted data and performance metrics
            (execution time, memory usage, comparisons).
        """
        return self._quicksort.sort(data, key_func)

    def sort_with_mergesort(self, data: List[Any], key_func: Callable[[Any], float]) -> SortResult:
        """Sort data using MergeSort algorithm.

        Args:
            data: The list of elements to sort (0 to 10,000 elements).
            key_func: A callable that extracts a numeric sort key from each element.

        Returns:
            SortResult containing sorted data and performance metrics
            (execution time, memory usage, comparisons).
        """
        return self._mergesort.sort(data, key_func)

    def comparison_report(self, data: List[Any], key_func: Callable[[Any], float]) -> str:
        """Run both sorting algorithms and generate a formatted comparison report.

        Executes QuickSort and MergeSort on the same dataset, measures
        performance metrics for each, and produces a formatted table
        comparing algorithm name, dataset size, execution time, memory
        usage, comparisons, and theoretical complexity.

        Args:
            data: The list of elements to sort (0 to 10,000 elements).
            key_func: A callable that extracts a numeric sort key from each element.

        Returns:
            A formatted string containing the comparison report with an
            ASCII table showing performance metrics for both algorithms.
        """
        # Run both algorithms on the same data
        quicksort_result = self._quicksort.sort(data, key_func)
        mergesort_result = self._mergesort.sort(data, key_func)

        # Get complexity information
        qs_complexity = self._quicksort.get_complexity()
        ms_complexity = self._mergesort.get_complexity()

        dataset_size = len(data)

        # Build the report header
        header = f"Algorithm Comparison Report\nDataset Size: {dataset_size}\n"

        # Build the table
        headers = [
            "Algorithm",
            "Time (ms)",
            "Memory (bytes)",
            "Comparisons",
            "Best",
            "Average",
            "Worst",
        ]

        rows = [
            [
                self._quicksort.get_name(),
                f"{quicksort_result.execution_time_ms:.2f}",
                str(quicksort_result.memory_bytes),
                str(quicksort_result.comparisons),
                qs_complexity.best_case,
                qs_complexity.average_case,
                qs_complexity.worst_case,
            ],
            [
                self._mergesort.get_name(),
                f"{mergesort_result.execution_time_ms:.2f}",
                str(mergesort_result.memory_bytes),
                str(mergesort_result.comparisons),
                ms_complexity.best_case,
                ms_complexity.average_case,
                ms_complexity.worst_case,
            ],
        ]

        table = format_table(headers, rows)

        return f"{header}\n{table}"
