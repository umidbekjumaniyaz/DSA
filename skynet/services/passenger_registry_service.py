"""Passenger registry service composing HashTable for record storage."""

from skynet.hashing import HashTable
from skynet.models.operation_result import OperationResult
from skynet.utils.validators import validate_pnr


class PassengerRegistryService:
    """Service layer for managing passenger records using a hash table.

    Provides business logic for creating, searching, updating, and
    deleting passenger records. Composes a HashTable internally for
    average-case O(1) lookup by PNR (Passenger Name Record).

    All public methods validate PNR format at the service boundary
    before delegating to the hash table.
    """

    def __init__(self):
        """Initialise the passenger registry service with an empty hash table."""
        self._hash_table = HashTable()

    def create_record(self, pnr: str, name: str, flight: str, seat: str) -> OperationResult:
        """Create a new passenger record and insert into the hash table.

        Validates PNR format (non-empty alphanumeric), builds a record
        dictionary, and inserts it as a (pnr, record) tuple.

        Args:
            pnr: Passenger Name Record identifier (alphanumeric).
            name: Passenger full name.
            flight: Flight number.
            seat: Seat assignment.

        Returns:
            OperationResult indicating success with stored record details,
            or failure with an error message (invalid PNR or duplicate).
        """
        if not validate_pnr(pnr):
            return OperationResult(
                success=False,
                message="Invalid PNR format: PNR must be a non-empty alphanumeric string.",
                data=None,
            )

        record = {"name": name, "flight": flight, "seat": seat}
        result = self._hash_table.insert((pnr, record))

        if not result.success:
            return OperationResult(
                success=False,
                message=f"Duplicate PNR rejected: '{pnr}' already exists in the registry.",
                data=None,
            )

        return OperationResult(
            success=True,
            message=f"Successfully created record for PNR '{pnr}'.",
            data={"pnr": pnr, **record},
        )

    def search_record(self, pnr: str) -> OperationResult:
        """Search for a passenger record by PNR.

        Validates PNR format and searches the hash table for the
        matching record.

        Args:
            pnr: Passenger Name Record identifier to search for.

        Returns:
            OperationResult with found record data, or failure if
            PNR is invalid or not found.
        """
        if not validate_pnr(pnr):
            return OperationResult(
                success=False,
                message="Invalid PNR format: PNR must be a non-empty alphanumeric string.",
                data=None,
            )

        result = self._hash_table.search(pnr)

        if not result.success:
            return OperationResult(
                success=False,
                message=f"PNR '{pnr}' not found in the registry.",
                data=None,
            )

        # result.data is a (pnr, record) tuple
        _, record = result.data
        return OperationResult(
            success=True,
            message=f"Found record for PNR '{pnr}'.",
            data={"pnr": pnr, **record},
        )

    def update_record(self, pnr: str, **fields) -> OperationResult:
        """Update an existing passenger record with new field values.

        Validates PNR format, retrieves the existing record, merges
        the provided fields, and updates the hash table entry.
        Only the fields provided (name, flight, seat) are updated.

        Args:
            pnr: Passenger Name Record identifier to update.
            **fields: Keyword arguments for fields to update.
                Supported keys: name, flight, seat.

        Returns:
            OperationResult with updated record data, or failure if
            PNR is invalid or not found.
        """
        if not validate_pnr(pnr):
            return OperationResult(
                success=False,
                message="Invalid PNR format: PNR must be a non-empty alphanumeric string.",
                data=None,
            )

        # Find existing record
        search_result = self._hash_table.search(pnr)

        if not search_result.success:
            return OperationResult(
                success=False,
                message=f"PNR '{pnr}' not found in the registry. Cannot update.",
                data=None,
            )

        # Merge fields into existing record
        _, existing_record = search_result.data
        updated_record = dict(existing_record)

        valid_fields = {"name", "flight", "seat"}
        for key, value in fields.items():
            if key in valid_fields:
                updated_record[key] = value

        # Update the hash table entry
        update_result = self._hash_table.update(pnr, updated_record)

        if not update_result.success:
            return OperationResult(
                success=False,
                message=f"Failed to update record for PNR '{pnr}'.",
                data=None,
            )

        return OperationResult(
            success=True,
            message=f"Successfully updated record for PNR '{pnr}'.",
            data={"pnr": pnr, **updated_record},
        )

    def delete_record(self, pnr: str) -> OperationResult:
        """Delete a passenger record by PNR from the hash table.

        Validates PNR format and deletes the matching record.

        Args:
            pnr: Passenger Name Record identifier to delete.

        Returns:
            OperationResult with deleted record details, or failure
            if PNR is invalid or not found.
        """
        if not validate_pnr(pnr):
            return OperationResult(
                success=False,
                message="Invalid PNR format: PNR must be a non-empty alphanumeric string.",
                data=None,
            )

        result = self._hash_table.delete(pnr)

        if not result.success:
            return OperationResult(
                success=False,
                message=f"PNR '{pnr}' not found in the registry. Cannot delete.",
                data=None,
            )

        # result.data is a (pnr, record) tuple
        _, record = result.data
        return OperationResult(
            success=True,
            message=f"Successfully deleted record for PNR '{pnr}'.",
            data={"pnr": pnr, **record},
        )

    def display_registry(self) -> str:
        """Display all records in hash table bucket format.

        Returns:
            A formatted string showing the hash table structure with
            bucket indices and chained entries, or a message indicating
            the registry is empty.
        """
        return self._hash_table.display()

    def get_all_records(self) -> list:
        """Return list of all (pnr, record) tuples for search service use.

        Iterates through all hash table buckets and collects non-empty
        entries for use by the PassengerSearchService.

        Returns:
            List of (pnr, record_dict) tuples for all stored records.
        """
        records = []
        for bucket in self._hash_table._buckets:
            for pnr, record in bucket:
                records.append((pnr, record))
        return records
