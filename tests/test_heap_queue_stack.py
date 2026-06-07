"""Unit tests for MaxHeap priority, FIFO queue, and LIFO stack (Req 16.2)."""

import unittest

from data_structures.exceptions import EmptyStructureError
from data_structures.fifo_queue import Queue
from data_structures.lifo_stack import Stack
from data_structures.max_heap import MaxHeap
from models.passenger import Passenger
from models.ticket_status import TicketStatus


def pax(pnr, name, status):
    return Passenger(pnr=pnr, name=name, status=status)


class TestPriorityQueue(unittest.TestCase):
    def test_priority_order(self):
        heap = MaxHeap(priority_of=lambda p: int(p.status))
        heap.push(pax("AAAAAA", "Eco", TicketStatus.ECONOMY))
        heap.push(pax("BBBBBB", "Plat", TicketStatus.PLATINUM))
        heap.push(pax("CCCCCC", "Gold", TicketStatus.GOLD))
        order = [heap.pop().status for _ in range(3)]
        self.assertEqual(
            order, [TicketStatus.PLATINUM, TicketStatus.GOLD, TicketStatus.ECONOMY]
        )

    def test_priority_collision_is_fifo(self):
        # Same status -> earliest enqueued served first (Req 5.3).
        heap = MaxHeap(priority_of=lambda p: int(p.status))
        heap.push(pax("AAAAAA", "First", TicketStatus.GOLD))
        heap.push(pax("BBBBBB", "Second", TicketStatus.GOLD))
        heap.push(pax("CCCCCC", "Third", TicketStatus.GOLD))
        self.assertEqual([heap.pop().name for _ in range(3)],
                         ["First", "Second", "Third"])

    def test_empty_heap_raises(self):
        with self.assertRaises(EmptyStructureError):
            MaxHeap().pop()


class TestQueue(unittest.TestCase):
    def test_fifo(self):
        q = Queue()
        for x in [1, 2, 3]:
            q.enqueue(x)
        self.assertEqual([q.dequeue() for _ in range(3)], [1, 2, 3])

    def test_empty_queue_raises(self):
        with self.assertRaises(EmptyStructureError):
            Queue().dequeue()


class TestStack(unittest.TestCase):
    def test_lifo(self):
        s = Stack()
        for x in [1, 2, 3]:
            s.push(x)
        self.assertEqual([s.pop() for _ in range(3)], [3, 2, 1])

    def test_empty_stack_raises(self):
        with self.assertRaises(EmptyStructureError):
            Stack().pop()


if __name__ == "__main__":
    unittest.main()
