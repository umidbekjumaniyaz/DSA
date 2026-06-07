"""KMP (Knuth-Morris-Pratt) string matching algorithm implementation."""


class KMPMatcher:
    """KMP string matching algorithm with failure function for efficient pattern searching.
    
    Provides O(n + m) time complexity pattern matching where n is text length
    and m is pattern length. Supports case-insensitive matching.
    """

    def compute_failure_function(self, pattern: str) -> list:
        """Compute the KMP failure (partial match) function for a pattern.
        
        Returns list where failure[i] = length of longest proper prefix 
        of pattern[0..i] that is also a suffix of pattern[0..i].
        
        Args:
            pattern: The pattern string to compute the failure function for.
            
        Returns:
            A list of integers representing the failure function values.
        """
        m = len(pattern)
        failure = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            failure[i] = j
        return failure

    def search(self, text: str, pattern: str) -> list:
        """Search for all occurrences of pattern in text using KMP.
        
        Case-insensitive matching.
        Returns list of starting indices where pattern was found.
        O(n + m) time complexity.
        
        Args:
            text: The text string to search within.
            pattern: The pattern string to search for.
            
        Returns:
            A list of starting indices where the pattern was found in the text.
        """
        # Convert both to lowercase for case-insensitive matching
        text_lower = text.lower()
        pattern_lower = pattern.lower()

        n = len(text_lower)
        m = len(pattern_lower)

        if m == 0:
            return []

        failure = self.compute_failure_function(pattern_lower)
        matches = []
        j = 0

        for i in range(n):
            while j > 0 and text_lower[i] != pattern_lower[j]:
                j = failure[j - 1]
            if text_lower[i] == pattern_lower[j]:
                j += 1
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]

        return matches
