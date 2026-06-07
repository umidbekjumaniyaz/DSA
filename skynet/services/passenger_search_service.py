"""Passenger search service using KMP string matching algorithm.

Provides search capabilities across passenger registry data, supporting
pattern matching on passenger names, PNR codes, and flight numbers.
"""

from skynet.models.operation_result import OperationResult
from skynet.string_matching import KMPMatcher
from skynet.utils.validators import validate_non_empty_string


class PassengerSearchService:
    """Service for searching passenger records using KMP pattern matching.

    Composes a KMPMatcher instance for efficient O(n + m) substring matching
    and references a PassengerRegistryService to access stored passenger data.

    Attributes:
        _kmp: KMPMatcher instance for pattern searching.
        _registry: PassengerRegistryService instance providing access to records.
    """

    def __init__(self, registry_service) -> None:
        """Initialize with a PassengerRegistryService instance.

        Args:
            registry_service: A PassengerRegistryService instance that provides
                a get_all_records() method returning either:
                - A list of (pnr, record_dict) tuples (real registry), or
                - A list of flat dicts with keys 'name', 'pnr', 'flight' (testing).
        """
        self._kmp = KMPMatcher()
        self._registry = registry_service

    def _normalize_records(self, raw_records: list) -> list:
        """Normalize records from registry into flat dicts with name, pnr, flight keys.

        Handles both tuple format from real PassengerRegistryService and flat
        dict format from test stubs.

        Args:
            raw_records: List of either (pnr, record_dict) tuples or flat dicts.

        Returns:
            List of dicts with keys 'name', 'pnr', 'flight'.
        """
        normalized = []
        for record in raw_records:
            if isinstance(record, tuple):
                pnr, data = record
                normalized.append({
                    "name": data.get("name", ""),
                    "pnr": pnr,
                    "flight": data.get("flight", ""),
                })
            else:
                normalized.append(record)
        return normalized

    def search_by_name(self, pattern: str) -> OperationResult:
        """Search all passenger names for the given pattern.

        Validates the pattern is non-empty and non-whitespace, then performs
        case-insensitive KMP matching against each passenger's name field.

        Args:
            pattern: The search pattern to match against passenger names.

        Returns:
            OperationResult with success=True and data containing a list of
            matching records (each a dict with 'name', 'pnr', 'flight'),
            or a no-match message if no records contain the pattern.
        """
        if not validate_non_empty_string(pattern):
            return OperationResult(
                success=False,
                message="Search pattern must be a non-empty, non-whitespace string.",
                data=None,
            )

        raw_records = self._registry.get_all_records()
        records = self._normalize_records(raw_records)
        matches = []

        for record in records:
            indices = self._kmp.search(record["name"], pattern)
            if len(indices) > 0:
                matches.append(record)

        if not matches:
            return OperationResult(
                success=True,
                message=f"No matching records found for pattern '{pattern}' in passenger names.",
                data=[],
            )

        return OperationResult(
            success=True,
            message=f"Found {len(matches)} matching record(s) for pattern '{pattern}' in passenger names.",
            data=matches,
        )

    def search_by_pnr(self, pattern: str) -> OperationResult:
        """Search all PNR codes for the given pattern.

        Validates the pattern is non-empty and non-whitespace, then performs
        case-insensitive KMP matching against each passenger's PNR field.

        Args:
            pattern: The search pattern to match against PNR codes.

        Returns:
            OperationResult with success=True and data containing a list of
            matching records (each a dict with 'name', 'pnr', 'flight'),
            or a no-match message if no records contain the pattern.
        """
        if not validate_non_empty_string(pattern):
            return OperationResult(
                success=False,
                message="Search pattern must be a non-empty, non-whitespace string.",
                data=None,
            )

        raw_records = self._registry.get_all_records()
        records = self._normalize_records(raw_records)
        matches = []

        for record in records:
            indices = self._kmp.search(record["pnr"], pattern)
            if len(indices) > 0:
                matches.append(record)

        if not matches:
            return OperationResult(
                success=True,
                message=f"No matching records found for pattern '{pattern}' in PNR codes.",
                data=[],
            )

        return OperationResult(
            success=True,
            message=f"Found {len(matches)} matching record(s) for pattern '{pattern}' in PNR codes.",
            data=matches,
        )

    def search_by_flight(self, pattern: str) -> OperationResult:
        """Search all flight numbers for the given pattern.

        Validates the pattern is non-empty and non-whitespace, then performs
        case-insensitive KMP matching against each passenger's flight number field.

        Args:
            pattern: The search pattern to match against flight numbers.

        Returns:
            OperationResult with success=True and data containing a list of
            matching records (each a dict with 'name', 'pnr', 'flight'),
            or a no-match message if no records contain the pattern.
        """
        if not validate_non_empty_string(pattern):
            return OperationResult(
                success=False,
                message="Search pattern must be a non-empty, non-whitespace string.",
                data=None,
            )

        raw_records = self._registry.get_all_records()
        records = self._normalize_records(raw_records)
        matches = []

        for record in records:
            indices = self._kmp.search(record["flight"], pattern)
            if len(indices) > 0:
                matches.append(record)

        if not matches:
            return OperationResult(
                success=True,
                message=f"No matching records found for pattern '{pattern}' in flight numbers.",
                data=[],
            )

        return OperationResult(
            success=True,
            message=f"Found {len(matches)} matching record(s) for pattern '{pattern}' in flight numbers.",
            data=matches,
        )
