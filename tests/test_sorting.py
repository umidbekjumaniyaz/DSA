"""Unit tests for QuickSort and MergeSort, including worst-case input."""

import unittest

from algorithms.sorting import mergesort, quicksort


class TestSorting(unittest.TestCase):
    def test_basic_sort(self):
        data = [5, 3, 8, 1, 9, 2]
        self.assertEqual(quicksort(data), sorted(data))
        self.assertEqual(mergesort(data), sorted(data))

    def test_empty_and_single(self):
        self.assertEqual(quicksort([]), [])
        self.assertEqual(mergesort([]), [])
        self.assertEqual(quicksort([42]), [42])
        self.assertEqual(mergesort([42]), [42])

    def test_worst_case_sorted_input(self):
        data = list(range(200))
        self.assertEqual(quicksort(data), data)  # already sorted
        self.assertEqual(mergesort(data), data)

    def test_worst_case_reverse_sorted(self):
        data = list(range(200, 0, -1))
        expected = sorted(data)
        self.assertEqual(quicksort(data), expected)
        self.assertEqual(mergesort(data), expected)

    def test_does_not_mutate_input(self):
        data = [3, 1, 2]
        quicksort(data)
        mergesort(data)
        self.assertEqual(data, [3, 1, 2])

    def test_with_key(self):
        data = [("a", 3), ("b", 1), ("c", 2)]
        self.assertEqual(
            [x[0] for x in quicksort(data, key=lambda t: t[1])], ["b", "c", "a"]
        )


if __name__ == "__main__":
    unittest.main()
