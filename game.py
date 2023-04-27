from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QRect
from random import randint, choice

from game.winDialog import WinDialog
from game.loseDialog import LoseDialog


class Cell:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value


class Node:
    def __init__(self, row, col, parent=None, distance_from_start=0, heuristic_distance=0):
        self.row = row
        self.col = col
        self.parent = parent
        self.distance_from_start = distance_from_start
        self.heuristic_distance = heuristic_distance

    def cost(self):
        return self.distance_from_start + self.heuristic_distance


class PriorityQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def put(self, item):
        self.items.append(item)
        self.items.sort(key=lambda x: x.cost())

    def get(self):
        return self.items.pop(0)


class Game(QWidget):
    def __init__(self):
        super().__init__()

        self.score = 0
        self.board = [[None] * 5 for _ in range(5)]
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)
        self.setStyleSheet("background-color: rgb(79, 80, 78);")
        self.setWindowTitle('Twelve')
        self.setGeometry(700, 300, 500, 500)

        self.cells = []
        for i in range(5):
            rows = []
            for j in range(5):
                cell = QPushButton('')
                cell.setStyleSheet("background-color: #ffe4e1;\n"
                                   "color: black;\n"
                                   "font-size: 14px;\n"
                                   "font-weight: bold;\n""")
                cell.clicked.connect(lambda _, row=i, col=j: self.cell_click(row, col))
                self.grid.addWidget(cell, i, j, 1, 1, Qt.AlignCenter)
                rows.append(cell)
            self.cells.append(rows)

        self.score_label = QLabel('Score: 0')
        self.score_label.setStyleSheet("color: white;\n"
                                       "font-size: 20px;\n""")
        self.grid.addWidget(self.score_label, 5, 0, 3, 5, Qt.AlignCenter)

        self.restart_button = QPushButton("restart")
        self.restart_button.setGeometry(QRect(350, 520, 151, 51))
        self.restart_button.setStyleSheet("background-color: rgb(112, 193, 179);\n"
                                          "color: rgb(255, 224, 102);\n"
                                          "font-size: 20px;\n"
                                          "font-weight: bold;\n""")
        self.restart_button.setObjectName("restartButton")
        self.restart_button.clicked.connect(self.restart_game)
        self.grid.addWidget(self.restart_button, 5, 0, 1, 5, Qt.AlignCenter)

        self.selected_cell = None

        self.new_game()

    def new_game(self):
        # генерируем три случайные цифры со значением 1, 2 или 3 в случайных ячейках
        for i in range(3):
            row, col = self.random_empty_cell()
            self.set_cell(row, col, randint(1, 3))

        self.score = 0
        self.update_score()

    def random_empty_cell(self):
        empty_cells = [(i, j) for i in range(5) for j in range(5) if self.board[i][j] is None]
        return choice(empty_cells)

    def generate_new_cell(self):
        empty_cells = [(i, j) for i in range(5) for j in range(5) if self.board[i][j] is None]
        if len(empty_cells) > 0:
            for i in range(1):
                row, col = self.random_empty_cell()
                self.set_cell(row, col, randint(1, 3))

    def get_cell(self, row, col):
        if row < 0 or row >= 5 or col < 0 or col >= 5:
            return None
        return self.board[row][col]

    def set_cell(self, row, col, value):
        self.board[row][col] = value
        if value is None:
            self.cells[row][col].setText('')
        else:
            self.cells[row][col].setText(str(value))

    def cell_click(self, row, col):
        cell_value = self.get_cell(row, col)

        if self.selected_cell is not None:
            if self.selected_cell.row == row and self.selected_cell.col == col:
                self.deselect_cell(row, col)
                return

            if cell_value is None and self.is_path_clear_for_moving(self.selected_cell.row, self.selected_cell.col, row, col):
                self.move_selected_cell(row, col)

            elif cell_value == self.selected_cell.value and self.is_path_clear_for_merging(self.selected_cell.row, self.selected_cell.col, row, col):
                self.merge_cells(row, col)
                self.has_lose() and (self.hide(), self.show_lose_window())
                self.has_win() and (self.hide(), self.show_win_window())
            else:
                self.deselect_cell(self.selected_cell.row, self.selected_cell.col)
                self.select_cell(row, col)

        elif cell_value is not None:
            self.select_cell(row, col)

    def select_cell(self, row, col):
        self.selected_cell = Cell(row, col, self.get_cell(row, col))
        self.cells[row][col].setStyleSheet("background-color: #ffcc66;\n"
                                           "color: black;\n"
                                           "font-size: 14px;\n"
                                           "font-weight: bold;\n")

    def deselect_cell(self, row, col):
        self.cells[row][col].setStyleSheet("background-color: #ffe4e1;\n"
                                           "color: black;\n"
                                           "font-size: 14px;\n"
                                           "font-weight: bold;\n")
        self.selected_cell = None

    def move_selected_cell(self, row, col):
        self.set_cell(row, col, self.selected_cell.value)
        self.set_cell(self.selected_cell.row, self.selected_cell.col, None)
        self.deselect_cell(self.selected_cell.row, self.selected_cell.col)
        self.generate_new_cell()

    def is_path_clear_for_moving(self, r1, c1, r2, c2):
        start_node = Node(r1, c1)
        end_node = Node(r2, c2)
        open_list = PriorityQueue()
        closed_list = set()

        open_list.put(start_node)

        while not open_list.is_empty():
            current_node = open_list.get()

            # Целевая ячейка достигнута
            if current_node.row == end_node.row and current_node.col == end_node.col:
                return True

            closed_list.add((current_node.row, current_node.col))

            for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                row = current_node.row + i
                col = current_node.col + j

                # Выход за границы игрового поля
                if row < 0 or row > 4 or col < 0 or col > 4:
                    continue

                # Ячейка занята
                if self.board[row][col] is not None:
                    continue

                # Ячейка уже была посещена
                if (row, col) in closed_list:
                    continue

                g = current_node.distance_from_start + 1
                h = abs(row - end_node.row) + abs(col - end_node.col)
                node = Node(row, col, current_node, g, h)
                open_list.put(node)

        # Целевая ячейка не достигнута
        return False

    def merge_cells(self, row, col):
        new_value = self.selected_cell.value + 1
        self.set_cell(row, col, new_value)
        self.set_cell(self.selected_cell.row, self.selected_cell.col, None)
        self.deselect_cell(self.selected_cell.row, self.selected_cell.col)

        self.score += new_value
        self.update_score()

        self.generate_new_cell()

    def is_path_clear_for_merging(self, r1, c1, r2, c2):
        start_node = Node(r1, c1)
        end_node = Node(r2, c2)
        open_list = PriorityQueue()
        closed_list = set()

        open_list.put(start_node)

        while not open_list.is_empty():
            current_node = open_list.get()

            # Целевая ячейка достигнута
            if current_node.row == end_node.row and current_node.col == end_node.col:
                # Начальная и конечная ячейки равны по значению
                if self.get_cell(start_node.row, start_node.col) == self.get_cell(end_node.row, end_node.col):
                    return True

            closed_list.add((current_node.row, current_node.col))

            for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                row = current_node.row + i
                col = current_node.col + j

                # Выход за границы поля
                if row < 0 or row > 4 or col < 0 or col > 4:
                    continue

                # Ячейка уже посещена
                if (row, col) in closed_list:
                    continue

                # Ячейка занята, но это не конечная ячейка
                if self.board[row][col] is not None and (row != end_node.row or col != end_node.col):
                    continue

                g = current_node.distance_from_start + 1
                h = abs(row - end_node.row) + abs(col - end_node.col)
                node = Node(row, col, current_node, g, h)
                open_list.put(node)

        # Целевая ячейка не достигнута
        return False

    def update_score(self):
        self.score_label.setText('Score: {}'.format(self.score))

    def has_win(self):
        for i in range(5):
            for j in range(5):
                if self.board[i][j] is not None and self.board[i][j] == 12:
                    return True
        return False

    def show_win_window(self):
        win_dialog = WinDialog(self.score, self)
        win_dialog.exec_()
        return

    def has_lose(self):
        for i in range(5):
            for j in range(5):
                if self.get_cell(i, j) is None:
                    return False
                if i > 0 and self.get_cell(i, j) == self.get_cell(i - 1, j):
                    return False
                if j > 0 and self.get_cell(i, j) == self.get_cell(i, j - 1):
                    return False
                if i < 4 and self.get_cell(i, j) == self.get_cell(i + 1, j):
                    return False
                if j < 4 and self.get_cell(i, j) == self.get_cell(i, j + 1):
                    return False
        return True

    def show_lose_window(self):
        lose_dialog = LoseDialog(self.score, self)
        lose_dialog.exec_()
        return

    def restart_game(self):
        # очищаем поле
        for i in range(5):
            for j in range(5):
                self.set_cell(i, j, None)

        self.new_game()
