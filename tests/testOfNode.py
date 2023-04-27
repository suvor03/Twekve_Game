import unittest
from game.game import Node

class TestNode(unittest.TestCase):

    def setUp(self):
        self.node = Node(0, 0, None, 3, 4)

    def test_init(self):
        self.assertEqual(self.node.row, 0)
        self.assertEqual(self.node.col, 0)
        self.assertEqual(self.node.parent, None)
        self.assertEqual(self.node.distance_from_start, 3)
        self.assertEqual(self.node.heuristic_distance, 4)

    def test_cost(self):
        self.assertEqual(self.node.cost(), 7)

if __name__ == '__main__':
    unittest.main()
    