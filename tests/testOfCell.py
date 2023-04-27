import unittest
from game.game import Cell

class TestCell(unittest.TestCase):

    def setUp(self):
        self.cell = Cell(0, 0, 1)

    def test_init(self):
        self.assertEqual(self.cell.row, 0)
        self.assertEqual(self.cell.col, 0)
        self.assertEqual(self.cell.value, 1)

if __name__ == '__main__':
    unittest.main()
