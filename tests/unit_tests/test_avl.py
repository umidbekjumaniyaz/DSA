"""Comprehensive unit tests for the AVL tree module.

Tests cover: AVLTree insertion, search, range search, in-order traversal,
rotation correctness (LL, LR, RR, RL), edge cases (empty tree, single node,
duplicate keys), and error conditions (non-existent key delete, out-of-range
search, invalid item types).

Requirements: 13.12, 13.13
"""

import pytest

from skynet.tree.avl_tree import AVLTree
from skynet.tree.avl_node import AVLNode
from skynet.models.price_record import PriceRecord


# ============================================================
# Helper utilities
# ============================================================


def verify_avl_balance(node):
    """Recursively verify the AVL balance property for all nodes.

    For every node in the tree: |height(left) - height(right)| <= 1.
    Returns the height of the subtree rooted at node.
    """
    if node is None:
        return 0

    left_height = verify_avl_balance(node.left)
    right_height = verify_avl_balance(node.right)

    balance = left_height - right_height
    assert abs(balance) <= 1, (
        f"AVL violation at node key={node.key}: "
        f"left_height={left_height}, right_height={right_height}, balance={balance}"
    )

    expected_height = 1 + max(left_height, right_height)
    assert node.height == expected_height, (
        f"Height mismatch at node key={node.key}: "
        f"stored={node.height}, computed={expected_height}"
    )

    return expected_height


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def empty_tree():
    """Return an empty AVLTree."""
    return AVLTree()


@pytest.fixture
def single_node_tree():
    """Return an AVLTree with a single price record."""
    tree = AVLTree()
    tree.insert(PriceRecord("LHR", "JFK", 499.99))
    return tree


@pytest.fixture
def populated_tree():
    """Return an AVLTree with multiple price records at various prices.

    Records inserted: 499.99, 250.00, 750.50, 150.00, 350.00, 600.00, 900.00
    """
    tree = AVLTree()
    records = [
        PriceRecord("LHR", "JFK", 499.99),
        PriceRecord("LHR", "CDG", 250.00),
        PriceRecord("DXB", "SIN", 750.50),
        PriceRecord("CDG", "DXB", 150.00),
        PriceRecord("JFK", "LAX", 350.00),
        PriceRecord("SIN", "HKG", 600.00),
        PriceRecord("HKG", "NRT", 900.00),
    ]
    for record in records:
        tree.insert(record)
    return tree


# ============================================================
# Normal Operation Tests
# ============================================================


class TestAVLTreeNormal:
    """Normal operation tests for AVLTree."""

    def test_insert_records_and_search_by_price(self, empty_tree):
        """Insert records and verify search returns correct record."""
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 499.99))
        tree.insert(PriceRecord("LHR", "CDG", 250.00))

        result = tree.search(499.99)
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0].origin == "LHR"
        assert result.data[0].destination == "JFK"
        assert result.data[0].price == 499.99

    def test_search_returns_all_records_at_price(self, empty_tree):
        """Search returns all records stored at a given price point."""
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 499.99))
        tree.insert(PriceRecord("CDG", "DXB", 499.99))

        result = tree.search(499.99)
        assert result.success is True
        assert len(result.data) == 2

    def test_range_search_returns_records_in_range(self, populated_tree):
        """Range search returns all records within the specified price bounds."""
        tree = populated_tree

        result = tree.range_search(200.00, 500.00)
        assert result.success is True
        # Should include 250.00, 350.00, 499.99
        prices = [r.price for r in result.data]
        assert 250.00 in prices
        assert 350.00 in prices
        assert 499.99 in prices
        assert 150.00 not in prices
        assert 750.50 not in prices

    def test_in_order_traversal_returns_sorted(self, populated_tree):
        """In-order traversal returns all records sorted by price ascending."""
        tree = populated_tree
        records = tree.in_order_traversal()

        prices = [r.price for r in records]
        assert prices == sorted(prices), "In-order traversal must return prices in ascending order"

    def test_insert_returns_success_result(self, empty_tree):
        """Insert operation returns OperationResult with success=True."""
        tree = empty_tree
        result = tree.insert(PriceRecord("LHR", "JFK", 499.99))

        assert result.success is True
        assert result.data is not None
        assert "499.99" in result.message

    def test_size_increases_on_insert(self, empty_tree):
        """Size increases by 1 after each insertion."""
        tree = empty_tree
        assert tree.size() == 0

        tree.insert(PriceRecord("LHR", "JFK", 499.99))
        assert tree.size() == 1

        tree.insert(PriceRecord("LHR", "CDG", 250.00))
        assert tree.size() == 2

    def test_delete_existing_price_succeeds(self, populated_tree):
        """Deleting an existing price node removes it and tree stays balanced."""
        tree = populated_tree
        initial_size = tree.size()

        result = tree.delete(250.00)
        assert result.success is True
        assert tree.size() == initial_size - 1

        # Confirm it's gone
        search_result = tree.search(250.00)
        assert search_result.success is False

        # AVL property maintained
        verify_avl_balance(tree._root)

    def test_display_returns_non_empty_string(self, populated_tree):
        """Display returns a formatted tree representation."""
        tree = populated_tree
        display_str = tree.display()
        assert "AVL Tree" in display_str
        assert len(display_str) > 0


# ============================================================
# Edge Case Tests
# ============================================================


class TestAVLTreeEdgeCases:
    """Edge case tests for AVLTree."""

    def test_empty_tree_search_returns_failure(self, empty_tree):
        """Searching an empty tree returns failure OperationResult."""
        result = empty_tree.search(100.00)
        assert result.success is False
        assert "No record" in result.message

    def test_empty_tree_is_empty(self, empty_tree):
        """An empty tree reports is_empty as True and size as 0."""
        assert empty_tree.is_empty() is True
        assert empty_tree.size() == 0

    def test_empty_tree_in_order_returns_empty_list(self, empty_tree):
        """In-order traversal of empty tree returns empty list."""
        records = empty_tree.in_order_traversal()
        assert records == []

    def test_empty_tree_display(self, empty_tree):
        """Display on empty tree returns appropriate message."""
        display_str = empty_tree.display()
        assert "empty" in display_str.lower()

    def test_single_node_tree_search_succeeds(self, single_node_tree):
        """Searching the only price in a single-node tree succeeds."""
        result = single_node_tree.search(499.99)
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0].price == 499.99

    def test_single_node_tree_in_order(self, single_node_tree):
        """In-order traversal of single node tree returns one record."""
        records = single_node_tree.in_order_traversal()
        assert len(records) == 1
        assert records[0].price == 499.99

    def test_duplicate_price_keys_stored_in_same_node(self, empty_tree):
        """Multiple records with the same price are stored in the same node."""
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 499.99))
        tree.insert(PriceRecord("CDG", "DXB", 499.99))
        tree.insert(PriceRecord("SIN", "HKG", 499.99))

        result = tree.search(499.99)
        assert result.success is True
        assert len(result.data) == 3

        # Size should be 3 (total records)
        assert tree.size() == 3

    def test_range_search_boundaries_are_inclusive(self, populated_tree):
        """Range search includes records at exactly min and max price."""
        tree = populated_tree

        # Range from 250.00 to 350.00 should include both boundary values
        result = tree.range_search(250.00, 350.00)
        assert result.success is True
        prices = [r.price for r in result.data]
        assert 250.00 in prices
        assert 350.00 in prices

    def test_delete_from_node_with_multiple_records(self, empty_tree):
        """Deleting from a node with duplicate keys removes one record."""
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 499.99))
        tree.insert(PriceRecord("CDG", "DXB", 499.99))

        result = tree.delete(499.99)
        assert result.success is True
        assert tree.size() == 1

        # One record should remain
        search_result = tree.search(499.99)
        assert search_result.success is True
        assert len(search_result.data) == 1


# ============================================================
# Error Condition Tests
# ============================================================


class TestAVLTreeErrors:
    """Error condition tests for AVLTree."""

    def test_delete_non_existent_price(self, populated_tree):
        """Deleting a price that doesn't exist returns failure."""
        tree = populated_tree
        result = tree.delete(9999.99)
        assert result.success is False
        assert "No record" in result.message or "9999.99" in result.message

    def test_delete_from_empty_tree(self, empty_tree):
        """Deleting from an empty tree returns failure."""
        result = empty_tree.delete(100.00)
        assert result.success is False
        assert "empty" in result.message.lower()

    def test_range_search_with_no_results(self, populated_tree):
        """Range search with no matching records returns failure."""
        tree = populated_tree
        # All prices are between 150 and 900, so search outside that range
        result = tree.range_search(1000.00, 2000.00)
        assert result.success is False
        assert "No records" in result.message

    def test_insert_non_price_record_returns_failure(self, empty_tree):
        """Inserting a non-PriceRecord item returns failure."""
        tree = empty_tree
        result = tree.insert("not a price record")
        assert result.success is False
        assert "PriceRecord" in result.message

    def test_insert_dict_returns_failure(self, empty_tree):
        """Inserting a dictionary returns failure."""
        tree = empty_tree
        result = tree.insert({"price": 100.0, "origin": "LHR"})
        assert result.success is False
        assert "PriceRecord" in result.message

    def test_insert_none_returns_failure(self, empty_tree):
        """Inserting None returns failure."""
        tree = empty_tree
        result = tree.insert(None)
        assert result.success is False


# ============================================================
# Rotation Tests (LL, LR, RR, RL)
# ============================================================


class TestAVLTreeRotations:
    """Tests verifying AVL tree rotations maintain balance.

    Each test triggers a specific rotation case and then verifies
    that the AVL balance property holds for all nodes.
    """

    def test_rr_rotation_right_heavy_insertions(self, empty_tree):
        """Inserting ascending prices triggers RR (left rotation) and stays balanced.

        Inserting 100, 200, 300 causes right-right imbalance at root,
        triggering a left rotation.
        """
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 100.00))
        tree.insert(PriceRecord("LHR", "CDG", 200.00))
        tree.insert(PriceRecord("LHR", "DXB", 300.00))

        # Verify balance property holds for entire tree
        verify_avl_balance(tree._root)

        # After rotation, root should be 200 (middle value)
        assert tree._root.key == 200.00
        assert tree._root.left.key == 100.00
        assert tree._root.right.key == 300.00

    def test_ll_rotation_left_heavy_insertions(self, empty_tree):
        """Inserting descending prices triggers LL (right rotation) and stays balanced.

        Inserting 300, 200, 100 causes left-left imbalance at root,
        triggering a right rotation.
        """
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 300.00))
        tree.insert(PriceRecord("LHR", "CDG", 200.00))
        tree.insert(PriceRecord("LHR", "DXB", 100.00))

        # Verify balance property holds for entire tree
        verify_avl_balance(tree._root)

        # After rotation, root should be 200 (middle value)
        assert tree._root.key == 200.00
        assert tree._root.left.key == 100.00
        assert tree._root.right.key == 300.00

    def test_lr_rotation_left_right_case(self, empty_tree):
        """Inserting values triggering LR case (left child right-heavy).

        Inserting 300, 100, 200 causes left-right imbalance,
        requiring double rotation (left on left child, then right on root).
        """
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 300.00))
        tree.insert(PriceRecord("LHR", "CDG", 100.00))
        tree.insert(PriceRecord("LHR", "DXB", 200.00))

        # Verify balance property holds for entire tree
        verify_avl_balance(tree._root)

        # After LR rotation, root should be 200 (middle value)
        assert tree._root.key == 200.00
        assert tree._root.left.key == 100.00
        assert tree._root.right.key == 300.00

    def test_rl_rotation_right_left_case(self, empty_tree):
        """Inserting values triggering RL case (right child left-heavy).

        Inserting 100, 300, 200 causes right-left imbalance,
        requiring double rotation (right on right child, then left on root).
        """
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 100.00))
        tree.insert(PriceRecord("LHR", "CDG", 300.00))
        tree.insert(PriceRecord("LHR", "DXB", 200.00))

        # Verify balance property holds for entire tree
        verify_avl_balance(tree._root)

        # After RL rotation, root should be 200 (middle value)
        assert tree._root.key == 200.00
        assert tree._root.left.key == 100.00
        assert tree._root.right.key == 300.00

    def test_balance_maintained_after_many_insertions(self, empty_tree):
        """AVL balance property holds after inserting many values."""
        tree = empty_tree
        prices = [50, 25, 75, 10, 30, 60, 90, 5, 15, 27, 35, 55, 65, 85, 95]
        for price in prices:
            tree.insert(PriceRecord("LHR", "JFK", float(price)))

        verify_avl_balance(tree._root)
        assert tree.size() == 15

    def test_balance_maintained_after_deletions(self, empty_tree):
        """AVL balance property holds after a sequence of insertions and deletions."""
        tree = empty_tree
        prices = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0]
        for price in prices:
            tree.insert(PriceRecord("LHR", "JFK", price))

        # Delete several nodes
        tree.delete(300.0)
        tree.delete(600.0)
        tree.delete(100.0)

        verify_avl_balance(tree._root)
        assert tree.size() == 4

        # Verify remaining records searchable
        assert tree.search(200.0).success is True
        assert tree.search(400.0).success is True
        assert tree.search(500.0).success is True
        assert tree.search(700.0).success is True

    def test_height_correct_after_rr_rotation(self, empty_tree):
        """Node heights are correct after RR rotation."""
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 100.00))
        tree.insert(PriceRecord("LHR", "CDG", 200.00))
        tree.insert(PriceRecord("LHR", "DXB", 300.00))

        # Root (200) should have height 2
        assert tree._root.height == 2
        # Leaves should have height 1
        assert tree._root.left.height == 1
        assert tree._root.right.height == 1

    def test_height_correct_after_ll_rotation(self, empty_tree):
        """Node heights are correct after LL rotation."""
        tree = empty_tree
        tree.insert(PriceRecord("LHR", "JFK", 300.00))
        tree.insert(PriceRecord("LHR", "CDG", 200.00))
        tree.insert(PriceRecord("LHR", "DXB", 100.00))

        # Root (200) should have height 2
        assert tree._root.height == 2
        # Leaves should have height 1
        assert tree._root.left.height == 1
        assert tree._root.right.height == 1
