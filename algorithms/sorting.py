"""QuickSort and MergeSort for ordering flight schedules.

Both accept a ``key`` callable, return a new list (the input is not mutated),
and preserve the multiset of input records. MergeSort is stable; QuickSort uses
median-of-three pivot selection to avoid quadratic blow-up on sorted input.
"""

from typing import Callable, List


def _identity(x):
    return x


def mergesort(items: List, key: Callable = _identity) -> List:
    """Stable MergeSort. Time O(n log n) all cases; space O(n)."""
    data = list(items)
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = mergesort(data[:mid], key)
    right = mergesort(data[mid:], key)
    return _merge(left, right, key)


def _merge(left: List, right: List, key: Callable) -> List:
    merged: List = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(right[j]) < key(left[i]):
            merged.append(right[j])
            j += 1
        else:  # <= keeps stability
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quicksort(items: List, key: Callable = _identity) -> List:
    """QuickSort with median-of-three pivot. Avg O(n log n), worst O(n^2)."""
    data = list(items)
    _quicksort(data, 0, len(data) - 1, key)
    return data


def _quicksort(data: List, low: int, high: int, key: Callable) -> None:
    while low < high:
        pivot_index = _partition(data, low, high, key)
        # Recurse into the smaller side, loop on the larger -> O(log n) stack.
        if pivot_index - low < high - pivot_index:
            _quicksort(data, low, pivot_index - 1, key)
            low = pivot_index + 1
        else:
            _quicksort(data, pivot_index + 1, high, key)
            high = pivot_index - 1


def _partition(data: List, low: int, high: int, key: Callable) -> int:
    mid = (low + high) // 2
    # Median-of-three: sort the three sample positions, then use the median
    # (now at ``mid``) as the pivot by moving it to ``high``.
    if key(data[mid]) < key(data[low]):
        data[low], data[mid] = data[mid], data[low]
    if key(data[high]) < key(data[low]):
        data[low], data[high] = data[high], data[low]
    if key(data[high]) < key(data[mid]):
        data[mid], data[high] = data[high], data[mid]
    data[mid], data[high] = data[high], data[mid]
    pivot = key(data[high])

    # Lomuto partition over [low, high-1] with the pivot parked at ``high``.
    i = low
    for j in range(low, high):
        if key(data[j]) < pivot:
            data[i], data[j] = data[j], data[i]
            i += 1
    data[i], data[high] = data[high], data[i]
    return i
