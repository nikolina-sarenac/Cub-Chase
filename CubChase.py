from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QLineEdit, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class CubChase(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("rsz_lion.jpg")
        self.setMaximumSize(640, 480)
        self.setMinimumSize(640, 480)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

        self.move(150, 100)
        self.setWindowTitle('Start window')

        self.btn = QPushButton('Start', self)
        self.btn.clicked.connect(self.showDialog)
        self.btn.resize(90, 50)
        self.btn.move(150, 340)

        self.btn1 = QPushButton('', self)
        self.btn1.setVisible(False)
        self.show()

    def showDialog(self):
        self.pixmap = QPixmap("rsz_lion.jpg")
        self.lbl.setPixmap(self.pixmap)

        self.btn.setText('Single player')
        self.btn.resize(150, 50)
        self.btn.move(100, 400)

        self.btn1.setText('Multiplayer')
        self.btn1.setVisible(True)
        self.btn1.resize(150, 50)
        self.btn1.move(420, 400)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubChase = CubChase()
    sys.exit(app.exec_())