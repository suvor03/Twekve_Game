import unittest
from game.game import PriorityQueue, Node


class TestPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.queue = PriorityQueue()

    def test_put(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.put(Node(0, 0, None, 3, 4))
        self.assertFalse(self.queue.is_empty())

    def test_get(self):
        self.queue.put(Node(0, 0, None, 3, 4))
        self.assertEqual(self.queue.get().distance_from_start, 3)

if __name__ == '__main__':
    unittest.main()
