"""Knuth-Morris-Pratt substring search.

Returns every start index at which ``pattern`` occurs in ``text``. Building the
failure function is O(m) and the scan is O(n), giving overall O(n + m) time and
O(m) space. An empty pattern matches at no position (treated as not found by
the service layer); a non-empty pattern with no occurrence returns an empty
list.
"""

from typing import List


def _failure_function(pattern: str) -> List[int]:
    """Compute the longest proper prefix-suffix table for ``pattern``."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def search(text: str, pattern: str) -> List[int]:
    """Return all start indices where ``pattern`` occurs in ``text``."""
    if pattern == "":
        return []
    if len(pattern) > len(text):
        return []

    lps = _failure_function(pattern)
    matches: List[int] = []
    i = j = 0  # i -> text, j -> pattern
    n, m = len(text), len(pattern)
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return matches
