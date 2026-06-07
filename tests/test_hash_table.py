"""Unit tests for the hash table, including forced collisions (Req 16.3)."""

import unittest

from data_structures.exceptions import KeyNotFoundError
from data_structures.hash_table import HashTable


class TestHashTable(unittest.TestCase):
    def test_put_get_delete(self):
        t = HashTable()
        t.put("ABC123", "Alice")
        self.assertEqual(t.get("ABC123"), "Alice")
        self.assertTrue(t.contains("ABC123"))
        t.delete("ABC123")
        self.assertFalse(t.contains("ABC123"))

    def test_missing_key_raises(self):
        t = HashTable()
        with self.assertRaises(KeyNotFoundError):
            t.get("NOPE12")
        with self.assertRaises(KeyNotFoundError):
            t.delete("NOPE12")

    def test_forced_collisions(self):
        # Use a tiny capacity so distinct keys share buckets.
        t = HashTable(capacity=2)
        keys = [f"K{i:05d}" for i in range(20)]
        for i, k in enumerate(keys):
            t.put(k, i)
        # Every key remains retrievable despite collisions.
        for i, k in enumerate(keys):
            self.assertEqual(t.get(k), i)
        self.assertEqual(t.size(), 20)

    def test_update_existing_key(self):
        t = HashTable()
        t.put("ABC123", "Alice")
        is_new = t.put("ABC123", "Bob")
        self.assertFalse(is_new)
        self.assertEqual(t.get("ABC123"), "Bob")
        self.assertEqual(t.size(), 1)


if __name__ == "__main__":
    unittest.main()
