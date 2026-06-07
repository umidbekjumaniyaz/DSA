"""Sort comparison service: QuickSort vs MergeSort timing and ordering."""

import time
from typing import List

from algorithms.sorting import mergesort, quicksort
from models.flight_record import SORT_KEYS, FlightRecord

from .results import ErrorCode, OperationResult


class SortComparisonService:
    """Phase 4 schedule sorting and QuickSort/MergeSort comparison."""

    def sort(self, schedule: List[FlightRecord], key: str = "departure_time",
             algorithm: str = "quicksort") -> OperationResult:
        validation = self.__validate_key(key)
        if validation is not None:
            return validation
        keyfn = lambda record: record.sort_value(key)
        algo = (algorithm or "quicksort").strip().lower()
        sorter = mergesort if algo == "mergesort" else quicksort
        ordered = sorter(schedule, keyfn)
        return OperationResult.success(
            payload=ordered,
            message=f"Sorted {len(ordered)} record(s) by {key} using {algo}.",
        )

    def compare(self, schedule: List[FlightRecord],
                key: str = "departure_time") -> OperationResult:
        validation = self.__validate_key(key)
        if validation is not None:
            return validation
        keyfn = lambda record: record.sort_value(key)

        start = time.perf_counter()
        quick_out = quicksort(schedule, keyfn)
        quick_time = time.perf_counter() - start

        start = time.perf_counter()
        merge_out = mergesort(schedule, keyfn)
        merge_time = time.perf_counter() - start

        identical = [keyfn(r) for r in quick_out] == [keyfn(r) for r in merge_out]
        payload = {
            "quicksort": quick_out,
            "mergesort": merge_out,
            "quick_seconds": quick_time,
            "merge_seconds": merge_time,
            "identical_ordering": identical,
        }
        message = (
            f"n={len(schedule)} sorted by {key}\n"
            f"  QuickSort: {quick_time * 1000:.4f} ms\n"
            f"  MergeSort: {merge_time * 1000:.4f} ms\n"
            f"  Identical ordering: {identical}"
        )
        return OperationResult.success(payload=payload, message=message)

    @staticmethod
    def __validate_key(key: str):
        if key not in SORT_KEYS:
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT,
                detail=f"sort key must be one of {', '.join(SORT_KEYS)}",
            )
        return None
