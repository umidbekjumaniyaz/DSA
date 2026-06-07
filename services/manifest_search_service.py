"""Manifest search service: KMP passenger-name search."""

from algorithms.kmp import search as kmp_search

from .results import ErrorCode, OperationResult


class ManifestSearchService:
    """Phase 4 KMP search over a passenger manifest."""

    def search(self, manifest_text: str, pattern: str) -> OperationResult:
        if not isinstance(manifest_text, str) or not isinstance(pattern, str):
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT, detail="manifest and pattern must be text"
            )
        if pattern == "":
            return OperationResult.failure(
                ErrorCode.INVALID_INPUT, detail="search term must be non-empty"
            )
        positions = kmp_search(manifest_text, pattern)
        if not positions:
            return OperationResult.success(
                payload=[], message=f"'{pattern}' not found in the manifest."
            )
        return OperationResult.success(
            payload=positions,
            message=(
                f"'{pattern}' found at {len(positions)} position(s): "
                f"{', '.join(map(str, positions))}."
            ),
        )
