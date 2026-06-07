"""Unit tests for the AVL price tree boundary cases (Req 16.3)."""

import unittest

from data_structures.price_tree import AVLTree


class TestPriceTree(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        for p in [50, 20, 70, 10, 30, 60, 80]:
            self.tree.insert(p)

    def test_membership(self):
        self.assertTrue(self.tree.contains(30))
        self.assertFalse(self.tree.contains(999))

    def test_range_inclusive_edges(self):
        self.assertEqual(self.tree.range_search(20, 60), [20, 30, 50, 60])

    def test_inverted_bounds_returns_empty(self):
        self.assertEqual(self.tree.range_search(60, 20), [])

    def test_single_point_range(self):
        self.assertEqual(self.tree.range_search(30, 30), [30])

    def test_duplicate_prices(self):
        t = AVLTree()
        t.insert(10)
        t.insert(10)
        self.assertEqual(t.range_search(0, 100), [10, 10])

    def test_balance_after_sorted_insert(self):
        t = AVLTree()
        for i in range(100):
            t.insert(i)
        # AVL height must stay logarithmic, not 100.
        self.assertLessEqual(t.height(), 10)


if __name__ == "__main__":
    unittest.main()
