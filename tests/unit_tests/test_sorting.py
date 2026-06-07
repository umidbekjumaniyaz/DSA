"""Comprehensive unit tests for the sorting module.

Tests cover: QuickSort and MergeSort with numeric lists, edge cases
(empty list, single element, already sorted, reverse sorted),
algorithm comparison (identical output on same input, sorted order
verification), and performance metrics (SortResult fields populated).

Requirements: 9.5, 9.6, 13.12, 13.13
"""

import pytest

from skynet.sorting import QuickSort, MergeSort, SortResult


# ============================================================
# Helper fixtures
# ============================================================


@pytest.fixture
def quicksort():
    """Return a QuickSort instance."""
    return QuickSort()


@pytest.fixture
def mergesort():
    """Return a MergeSort instance."""
    return MergeSort()


@pytest.fixture
def unsorted_list():
    """Return an unsorted numeric list."""
    return [38, 27, 43, 3, 9, 82, 10]


@pytest.fixture
def already_sorted_list():
    """Return a list already in ascending order."""
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def reverse_sorted_list():
    """Return a list in descending order."""
    return [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


@pytest.fixture
def key_func():
    """Return identity key function for numeric sorting."""
    return lambda x: x


# ============================================================
# TestQuickSort
# ============================================================


class TestQuickSort:
    """Unit tests for QuickSort algorithm."""

    def test_sort_numeric_list(self, quicksort, unsorted_list, key_func):
        """QuickSort correctly sorts an unsorted numeric list in ascending order."""
        result = quicksort.sort(unsorted_list, key_func)

        assert isinstance(result, SortResult)
        assert result.sorted_data == [3, 9, 10, 27, 38, 43, 82]

    def test_sort_empty_list(self, quicksort, key_func):
        """QuickSort handles empty list without error and returns empty result."""
        result = quicksort.sort([], key_func)

        assert result.sorted_data == []
        assert result.comparisons == 0

    def test_sort_single_element(self, quicksort, key_func):
        """QuickSort handles single element list returning it unchanged."""
        result = quicksort.sort([42], key_func)

        assert result.sorted_data == [42]
        assert result.comparisons == 0

    def test_sort_already_sorted(self, quicksort, already_sorted_list, key_func):
        """QuickSort correctly handles an already-sorted list."""
        result = quicksort.sort(already_sorted_list, key_func)

        assert result.sorted_data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_sort_reverse_sorted(self, quicksort, reverse_sorted_list, key_func):
        """QuickSort correctly sorts a reverse-sorted list."""
        result = quicksort.sort(reverse_sorted_list, key_func)

        assert result.sorted_data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_sort_with_duplicates(self, quicksort, key_func):
        """QuickSort handles duplicate values correctly."""
        data = [5, 3, 5, 1, 3, 2, 5]
        result = quicksort.sort(data, key_func)

        assert result.sorted_data == [1, 2, 3, 3, 5, 5, 5]

    def test_does_not_mutate_input(self, quicksort, key_func):
        """QuickSort does not modify the original input list."""
        data = [5, 2, 8, 1, 4]
        original = data.copy()
        quicksort.sort(data, key_func)

        assert data == original

    def test_get_name(self, quicksort):
        """QuickSort reports its name correctly."""
        assert quicksort.get_name() == "QuickSort"

    def test_get_complexity(self, quicksort):
        """QuickSort reports correct complexity information."""
        complexity = quicksort.get_complexity()

        assert "n log n" in complexity.best_case
        assert "n log n" in complexity.average_case
        assert "n" in complexity.worst_case  # O(n^2) contains 'n'
        assert "log n" in complexity.space


# ============================================================
# TestMergeSort
# ============================================================


class TestMergeSort:
    """Unit tests for MergeSort algorithm."""

    def test_sort_numeric_list(self, mergesort, unsorted_list, key_func):
        """MergeSort correctly sorts an unsorted numeric list in ascending order."""
        result = mergesort.sort(unsorted_list, key_func)

        assert isinstance(result, SortResult)
        assert result.sorted_data == [3, 9, 10, 27, 38, 43, 82]

    def test_sort_empty_list(self, mergesort, key_func):
        """MergeSort handles empty list without error and returns empty result."""
        result = mergesort.sort([], key_func)

        assert result.sorted_data == []
        assert result.comparisons == 0

    def test_sort_single_element(self, mergesort, key_func):
        """MergeSort handles single element list returning it unchanged."""
        result = mergesort.sort([42], key_func)

        assert result.sorted_data == [42]
        assert result.comparisons == 0

    def test_sort_already_sorted(self, mergesort, already_sorted_list, key_func):
        """MergeSort correctly handles an already-sorted list."""
        result = mergesort.sort(already_sorted_list, key_func)

        assert result.sorted_data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_sort_reverse_sorted(self, mergesort, reverse_sorted_list, key_func):
        """MergeSort correctly sorts a reverse-sorted list."""
        result = mergesort.sort(reverse_sorted_list, key_func)

        assert result.sorted_data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_sort_with_duplicates(self, mergesort, key_func):
        """MergeSort handles duplicate values correctly."""
        data = [5, 3, 5, 1, 3, 2, 5]
        result = mergesort.sort(data, key_func)

        assert result.sorted_data == [1, 2, 3, 3, 5, 5, 5]

    def test_does_not_mutate_input(self, mergesort, key_func):
        """MergeSort does not modify the original input list."""
        data = [5, 2, 8, 1, 4]
        original = data.copy()
        mergesort.sort(data, key_func)

        assert data == original

    def test_get_name(self, mergesort):
        """MergeSort reports its name correctly."""
        assert mergesort.get_name() == "MergeSort"

    def test_get_complexity(self, mergesort):
        """MergeSort reports correct complexity information."""
        complexity = mergesort.get_complexity()

        assert "n log n" in complexity.best_case
        assert "n log n" in complexity.average_case
        assert "n log n" in complexity.worst_case
        assert "n" in complexity.space


# ============================================================
# TestSortingComparison
# ============================================================


class TestSortingComparison:
    """Tests verifying both algorithms produce identical results (Requirement 9.5)."""

    def test_both_produce_identical_output_unsorted(self, quicksort, mergesort, unsorted_list, key_func):
        """QuickSort and MergeSort produce identical sorted output on same unsorted input."""
        qs_result = quicksort.sort(unsorted_list, key_func)
        ms_result = mergesort.sort(unsorted_list, key_func)

        assert qs_result.sorted_data == ms_result.sorted_data

    def test_both_produce_identical_output_reverse(self, quicksort, mergesort, reverse_sorted_list, key_func):
        """QuickSort and MergeSort produce identical sorted output on reverse-sorted input."""
        qs_result = quicksort.sort(reverse_sorted_list, key_func)
        ms_result = mergesort.sort(reverse_sorted_list, key_func)

        assert qs_result.sorted_data == ms_result.sorted_data

    def test_both_produce_identical_output_with_duplicates(self, quicksort, mergesort, key_func):
        """QuickSort and MergeSort produce identical output on data with duplicates."""
        data = [7, 2, 7, 5, 3, 2, 8, 1, 5, 7]
        qs_result = quicksort.sort(data, key_func)
        ms_result = mergesort.sort(data, key_func)

        assert qs_result.sorted_data == ms_result.sorted_data

    def test_both_verify_sorted_order(self, quicksort, mergesort, unsorted_list, key_func):
        """Both algorithms verify sorted order: element[i] <= element[i+1] (Requirement 9.6)."""
        qs_result = quicksort.sort(unsorted_list, key_func)
        ms_result = mergesort.sort(unsorted_list, key_func)

        # Verify QuickSort output is sorted
        for i in range(len(qs_result.sorted_data) - 1):
            assert qs_result.sorted_data[i] <= qs_result.sorted_data[i + 1]

        # Verify MergeSort output is sorted
        for i in range(len(ms_result.sorted_data) - 1):
            assert ms_result.sorted_data[i] <= ms_result.sorted_data[i + 1]

    def test_both_produce_identical_output_large_dataset(self, quicksort, mergesort, key_func):
        """QuickSort and MergeSort produce identical output on a larger dataset."""
        import random
        random.seed(42)
        data = [random.randint(1, 1000) for _ in range(100)]

        qs_result = quicksort.sort(data, key_func)
        ms_result = mergesort.sort(data, key_func)

        assert qs_result.sorted_data == ms_result.sorted_data

    def test_both_produce_identical_output_empty(self, quicksort, mergesort, key_func):
        """Both algorithms produce identical (empty) output on empty input."""
        qs_result = quicksort.sort([], key_func)
        ms_result = mergesort.sort([], key_func)

        assert qs_result.sorted_data == ms_result.sorted_data == []


# ============================================================
# TestSortingPerformance
# ============================================================


class TestSortingPerformance:
    """Tests verifying SortResult performance metric fields are populated."""

    def test_quicksort_execution_time_populated(self, quicksort, key_func):
        """QuickSort SortResult execution_time_ms is >= 0."""
        data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        result = quicksort.sort(data, key_func)

        assert result.execution_time_ms >= 0

    def test_quicksort_memory_bytes_populated(self, quicksort, key_func):
        """QuickSort SortResult memory_bytes is >= 0."""
        data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        result = quicksort.sort(data, key_func)

        assert result.memory_bytes >= 0

    def test_quicksort_comparisons_populated(self, quicksort, key_func):
        """QuickSort SortResult comparisons is >= 0 for non-trivial input."""
        data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        result = quicksort.sort(data, key_func)

        assert result.comparisons >= 0
        # For a list of 9 elements, there should be actual comparisons
        assert result.comparisons > 0

    def test_mergesort_execution_time_populated(self, mergesort, key_func):
        """MergeSort SortResult execution_time_ms is >= 0."""
        data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        result = mergesort.sort(data, key_func)

        assert result.execution_time_ms >= 0

    def test_mergesort_memory_bytes_populated(self, mergesort, key_func):
        """MergeSort SortResult memory_bytes is >= 0."""
        data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        result = mergesort.sort(data, key_func)

        assert result.memory_bytes >= 0

    def test_mergesort_comparisons_populated(self, mergesort, key_func):
        """MergeSort SortResult comparisons is >= 0 for non-trivial input."""
        data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        result = mergesort.sort(data, key_func)

        assert result.comparisons >= 0
        # For a list of 9 elements, there should be actual comparisons
        assert result.comparisons > 0

    def test_empty_input_metrics_zero(self, quicksort, mergesort, key_func):
        """Empty input produces zero metrics for both algorithms."""
        qs_result = quicksort.sort([], key_func)
        ms_result = mergesort.sort([], key_func)

        assert qs_result.execution_time_ms == 0.0
        assert qs_result.memory_bytes == 0
        assert qs_result.comparisons == 0

        assert ms_result.execution_time_ms == 0.0
        assert ms_result.memory_bytes == 0
        assert ms_result.comparisons == 0

    def test_single_element_metrics_zero(self, quicksort, mergesort, key_func):
        """Single element input produces zero comparisons for both algorithms."""
        qs_result = quicksort.sort([42], key_func)
        ms_result = mergesort.sort([42], key_func)

        assert qs_result.comparisons == 0
        assert ms_result.comparisons == 0
