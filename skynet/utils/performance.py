"""Performance measurement utility functions for SkyNet.

Provides timing and memory measurement utilities using standard library modules.
All functions handle exceptions gracefully and return sensible defaults on failure.
"""

import time
import tracemalloc
from typing import Any, Tuple


def measure_time(func, *args, **kwargs) -> Tuple[Any, float]:
    """Execute a function and measure its execution time in milliseconds.

    Args:
        func: The callable to execute.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        A tuple of (result, time_ms) where result is the function's return value
        and time_ms is the execution time in milliseconds.
    """
    try:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed_ms = (end - start) * 1000.0
        return result, elapsed_ms
    except Exception as e:
        return None, 0.0


def measure_memory(func, *args, **kwargs) -> Tuple[Any, int]:
    """Execute a function and measure its peak memory usage in bytes.

    Args:
        func: The callable to execute.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        A tuple of (result, bytes_used) where result is the function's return value
        and bytes_used is the peak memory usage in bytes during execution.
    """
    try:
        tracemalloc.start()
        result = func(*args, **kwargs)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return result, peak
    except Exception as e:
        if tracemalloc.is_tracing():
            tracemalloc.stop()
        return None, 0


def measure_performance(func, *args, **kwargs) -> Tuple[Any, float, int]:
    """Execute a function and measure both time and memory usage.

    Args:
        func: The callable to execute.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        A tuple of (result, time_ms, bytes_used) where result is the function's
        return value, time_ms is execution time in milliseconds, and bytes_used
        is the peak memory usage in bytes.
    """
    try:
        tracemalloc.start()
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        elapsed_ms = (end - start) * 1000.0
        return result, elapsed_ms, peak
    except Exception as e:
        if tracemalloc.is_tracing():
            tracemalloc.stop()
        return None, 0.0, 0
