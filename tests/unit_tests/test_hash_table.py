"""Comprehensive unit tests for the hashing module.

Tests cover: HashTable with separate chaining — insert, search, update,
delete operations by PNR key, collision handling, edge cases, and error
conditions.

Requirements: 13.7, 13.8, 13.12, 13.13
"""

import pytest

from skynet.hashing.hash_table import HashTable


# ============================================================
# Helper fixtures
# ============================================================


@pytest.fixture
def empty_table():
    """Return an empty HashTable with default capacity."""
    return HashTable()


@pytest.fixture
def single_entry_table():
    """Return a HashTable containing a single passenger record."""
    table = HashTable()
    table.insert(("PNR123", {"name": "Alice Smith", "flight": "SK100", "seat": "1A"}))
    return table


@pytest.fixture
def populated_table():
    """Return a HashTable with several passenger records."""
    table = HashTable()
    records = [
        ("PNR001", {"name": "Alice Smith", "flight": "SK100", "seat": "1A"}),
        ("PNR002", {"name": "Bob Jones", "flight": "SK200", "seat": "5B"}),
        ("PNR003", {"name": "Charlie Brown", "flight": "SK300", "seat": "12C"}),
        ("PNR004", {"name": "Diana Prince", "flight": "SK400", "seat": "8D"}),
        ("PNR005", {"name": "Eve Wilson", "flight": "SK500", "seat": "20E"}),
    ]
    for record in records:
        table.insert(record)
    return table


# ============================================================
# Normal Operation Tests
# ============================================================


class TestHashTableNormal:
    """Normal operation tests for HashTable."""

    def test_insert_single_record(self, empty_table):
        """Insert a single record and verify success."""
        table = empty_table
        result = table.insert(("PNR123", {"name": "Alice", "flight": "SK100", "seat": "1A"}))

        assert result.success is True
        assert "PNR123" in result.message
        assert result.data == ("PNR123", {"name": "Alice", "flight": "SK100", "seat": "1A"})

    def test_insert_multiple_records(self, empty_table):
        """Insert multiple records increases size accordingly."""
        table = empty_table
        table.insert(("PNR001", {"name": "Alice", "flight": "SK100", "seat": "1A"}))
        table.insert(("PNR002", {"name": "Bob", "flight": "SK200", "seat": "2B"}))
        table.insert(("PNR003", {"name": "Charlie", "flight": "SK300", "seat": "3C"}))

        assert table.size() == 3

    def test_search_existing_key(self, populated_table):
        """Search for an existing key returns the correct record."""
        table = populated_table
        result = table.search("PNR003")

        assert result.success is True
        assert result.data[0] == "PNR003"
        assert result.data[1]["name"] == "Charlie Brown"
        assert result.data[1]["flight"] == "SK300"

    def test_search_returns_correct_data(self, single_entry_table):
        """Search returns the full (key, value) tuple for matching key."""
        table = single_entry_table
        result = table.search("PNR123")

        assert result.success is True
        assert result.data == ("PNR123", {"name": "Alice Smith", "flight": "SK100", "seat": "1A"})

    def test_update_existing_record(self, populated_table):
        """Update an existing record replaces the value."""
        table = populated_table
        new_data = {"name": "Alice Johnson", "flight": "SK101", "seat": "2A"}
        result = table.update("PNR001", new_data)

        assert result.success is True
        assert result.data == ("PNR001", new_data)

        # Verify the update persisted
        search_result = table.search("PNR001")
        assert search_result.data[1]["name"] == "Alice Johnson"
        assert search_result.data[1]["flight"] == "SK101"
        assert search_result.data[1]["seat"] == "2A"

    def test_delete_existing_record(self, populated_table):
        """Delete an existing record removes it and returns the deleted data."""
        table = populated_table
        initial_size = table.size()
        result = table.delete("PNR003")

        assert result.success is True
        assert result.data[0] == "PNR003"
        assert result.data[1]["name"] == "Charlie Brown"
        assert table.size() == initial_size - 1

        # Verify it's gone
        search_result = table.search("PNR003")
        assert search_result.success is False

    def test_insert_then_search_round_trip(self, empty_table):
        """Insert a record and immediately search for it."""
        table = empty_table
        data = {"name": "Test User", "flight": "SK999", "seat": "99Z"}
        table.insert(("TESTABC", data))

        result = table.search("TESTABC")
        assert result.success is True
        assert result.data[1] == data

    def test_is_empty_false_after_insert(self, single_entry_table):
        """is_empty returns False when table has entries."""
        assert single_entry_table.is_empty() is False

    def test_is_empty_true_initially(self, empty_table):
        """is_empty returns True for a new table."""
        assert empty_table.is_empty() is True

    def test_size_tracks_insertions(self, empty_table):
        """Size correctly tracks number of entries."""
        table = empty_table
        assert table.size() == 0

        table.insert(("KEY1", "val1"))
        assert table.size() == 1

        table.insert(("KEY2", "val2"))
        assert table.size() == 2

    def test_size_tracks_deletions(self, populated_table):
        """Size correctly decreases after deletions."""
        table = populated_table
        initial_size = table.size()

        table.delete("PNR001")
        assert table.size() == initial_size - 1

        table.delete("PNR002")
        assert table.size() == initial_size - 2


# ============================================================
# Edge Case Tests
# ============================================================


class TestHashTableEdgeCases:
    """Edge case tests for HashTable."""

    def test_collision_handling_same_bucket(self):
        """Keys that hash to the same bucket are stored correctly via chaining."""
        # Use a small capacity to force collisions
        table = HashTable(capacity=3)

        # Insert multiple keys — with capacity 3, collisions are very likely
        keys_data = [
            ("AAA", {"name": "Record A"}),
            ("BBB", {"name": "Record B"}),
            ("CCC", {"name": "Record C"}),
            ("DDD", {"name": "Record D"}),
            ("EEE", {"name": "Record E"}),
        ]
        for key, data in keys_data:
            result = table.insert((key, data))
            assert result.success is True

        # All records should be retrievable despite collisions
        for key, data in keys_data:
            result = table.search(key)
            assert result.success is True
            assert result.data[1] == data

    def test_collision_keys_same_bucket_verification(self):
        """Explicitly verify two keys hash to the same bucket and both are retrievable."""
        table = HashTable(capacity=53)

        # Find two keys that hash to the same bucket
        key1 = None
        key2 = None
        for i in range(1000):
            test_key = f"KEY{i:04d}"
            bucket = table._hash(test_key)
            if key1 is None:
                key1 = test_key
                target_bucket = bucket
            elif bucket == target_bucket and key2 is None:
                key2 = test_key
                break

        assert key2 is not None, "Could not find two keys with same bucket"

        # Insert both — they collide in the same bucket
        table.insert((key1, {"name": "First"}))
        table.insert((key2, {"name": "Second"}))

        # Both should be searchable
        result1 = table.search(key1)
        assert result1.success is True
        assert result1.data[1] == {"name": "First"}

        result2 = table.search(key2)
        assert result2.success is True
        assert result2.data[1] == {"name": "Second"}

    def test_single_entry_operations(self, empty_table):
        """All operations work correctly on a table with a single entry."""
        table = empty_table
        table.insert(("ONLY1", {"name": "Solo Record"}))

        # Search
        result = table.search("ONLY1")
        assert result.success is True
        assert result.data[1]["name"] == "Solo Record"

        # Update
        result = table.update("ONLY1", {"name": "Updated Solo"})
        assert result.success is True

        # Verify update
        result = table.search("ONLY1")
        assert result.data[1]["name"] == "Updated Solo"

        # Delete
        result = table.delete("ONLY1")
        assert result.success is True
        assert table.is_empty() is True

    def test_display_format_non_empty(self, populated_table):
        """Display shows bucket structure with entries."""
        table = populated_table
        display_str = table.display()

        assert "Bucket [" in display_str
        assert "->" in display_str
        # Should contain at least one of the keys
        assert "PNR" in display_str

    def test_display_empty_table(self, empty_table):
        """Display on empty table returns appropriate message."""
        display_str = empty_table.display()
        assert "empty" in display_str.lower()

    def test_update_preserves_size(self, populated_table):
        """Updating a record does not change table size."""
        table = populated_table
        initial_size = table.size()

        table.update("PNR002", {"name": "Updated Bob", "flight": "SK201", "seat": "6C"})
        assert table.size() == initial_size

    def test_delete_then_reinsert(self, empty_table):
        """A deleted key can be re-inserted successfully."""
        table = empty_table
        table.insert(("REUSE1", {"name": "Original"}))
        table.delete("REUSE1")
        assert table.search("REUSE1").success is False

        result = table.insert(("REUSE1", {"name": "Reinserted"}))
        assert result.success is True

        search_result = table.search("REUSE1")
        assert search_result.success is True
        assert search_result.data[1]["name"] == "Reinserted"


# ============================================================
# Error Condition Tests
# ============================================================


class TestHashTableErrors:
    """Error condition tests for HashTable."""

    def test_duplicate_key_insert_rejected(self, populated_table):
        """Inserting a duplicate key returns failure and preserves original."""
        table = populated_table
        original_size = table.size()

        result = table.insert(("PNR001", {"name": "Imposter", "flight": "XX", "seat": "XX"}))
        assert result.success is False
        assert "duplicate" in result.message.lower() or "already exists" in result.message.lower()
        assert table.size() == original_size

        # Original record is unchanged
        search_result = table.search("PNR001")
        assert search_result.data[1]["name"] == "Alice Smith"

    def test_search_non_existent_key(self, populated_table):
        """Searching for a non-existent key returns failure."""
        table = populated_table
        result = table.search("NONEXIST")

        assert result.success is False
        assert "not found" in result.message.lower()
        assert result.data is None

    def test_update_non_existent_key(self, populated_table):
        """Updating a non-existent key returns failure."""
        table = populated_table
        result = table.update("NONEXIST", {"name": "Ghost"})

        assert result.success is False
        assert "not found" in result.message.lower()
        assert result.data is None

    def test_delete_non_existent_key(self, populated_table):
        """Deleting a non-existent key returns failure."""
        table = populated_table
        initial_size = table.size()
        result = table.delete("NONEXIST")

        assert result.success is False
        assert "not found" in result.message.lower()
        assert table.size() == initial_size

    def test_non_string_key_search(self, populated_table):
        """Search with a non-string key returns failure."""
        table = populated_table
        result = table.search(12345)

        assert result.success is False
        assert "string" in result.message.lower()

    def test_non_string_key_delete(self, populated_table):
        """Delete with a non-string key returns failure."""
        table = populated_table
        result = table.delete(999)

        assert result.success is False
        assert "string" in result.message.lower()

    def test_non_string_key_update(self, populated_table):
        """Update with a non-string key returns failure."""
        table = populated_table
        result = table.update(42, {"name": "Numeric Key"})

        assert result.success is False
        assert "string" in result.message.lower()

    def test_non_tuple_insert(self, empty_table):
        """Insert with a non-tuple item returns failure."""
        table = empty_table
        result = table.insert("not a tuple")

        assert result.success is False
        assert "tuple" in result.message.lower()

    def test_insert_tuple_wrong_length(self, empty_table):
        """Insert with a tuple of wrong length returns failure."""
        table = empty_table

        # Single element tuple
        result = table.insert(("only_key",))
        assert result.success is False

        # Three element tuple
        result = table.insert(("key", "val", "extra"))
        assert result.success is False

    def test_insert_with_non_string_key_in_tuple(self, empty_table):
        """Insert with a tuple where key is not a string returns failure."""
        table = empty_table
        result = table.insert((123, {"name": "Numeric Key"}))

        assert result.success is False
        assert "string" in result.message.lower()

    def test_insert_list_instead_of_tuple(self, empty_table):
        """Insert with a list instead of tuple returns failure."""
        table = empty_table
        result = table.insert(["PNR123", {"name": "List Item"}])

        assert result.success is False
        assert "tuple" in result.message.lower()
