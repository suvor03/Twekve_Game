from PyQt5 import QtWidgets, QtCore


class LoseDialog(QtWidgets.QDialog):
    def __init__(self, score, parent=None):
        super().__init__(parent)

        self.setWindowTitle('You lose!')
        self.resize(300, 300)
        self.score_label = QtWidgets.QLabel(f"You Lose! Your score: {score}")
        self.score_label.setStyleSheet("font-size: 30px; color: red")
        self.score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.setStyleSheet("font-size: 18px;")
        self.close_button.clicked.connect(self.close)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.score_label)
        vbox.addWidget(self.close_button)
        vbox.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(vbox)
